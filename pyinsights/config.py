import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from jsonschema import Draft7Validator
from jsonschema.exceptions import ValidationError
from yaml import safe_load

from pyinsights.exceptions import (
    ConfigInvalidSyntaxError,
    ConfigNotFoundError,
    ConfigVersionUnknownError,
    InvalidVersionError,
)
from pyinsights.helper import (
    convert_to_epoch,
    convert_string_duration_to_datetime,
)


ConfigType = Dict[str, Any]
SchemaType = Dict[str, Any]


@dataclass
class ConfigFile:
    filename: str
    content: ConfigType

    @classmethod
    def from_filename(cls, filename: str) -> "ConfigFile":
        return cls(filename, load_yaml(filename))

    @property
    def version(self) -> str:
        try:
            return self.content["version"]
        except KeyError:
            raise ConfigVersionUnknownError(
                "Please Specify configuration version"
            )

    def convert_duration(self) -> Dict[str, int]:
        duration = self.content["duration"]

        if isinstance(duration, str):
            duration = convert_string_duration_to_datetime(duration)

        duration_epoch = {
            key: convert_to_epoch(value) for key, value in duration.items()
        }
        return duration_epoch

    def get_query_params(self) -> ConfigType:
        params = self.content.copy()
        new_duration = self.convert_duration()
        del params["version"]
        del params["duration"]
        params.update(new_duration)
        return params


def load_config(filepath: str) -> ConfigFile:
    """Load configuration

    Arguments:
        filepath {str}

    Returns:
        {ConfigFile} -- query parameters
    """

    config = ConfigFile.from_filename(filepath)
    validate(config.content, config.version)
    return config


def load_yaml(filepath: str) -> ConfigType:
    """Load YAML configuration file

    Arguments:
        filepath {str}

    Raises:
        ConfigNotFoundError

    Returns:
        config {ConfigType}
    """

    try:
        with open(filepath) as fobj:
            return safe_load(fobj)
    except FileNotFoundError:
        raise ConfigNotFoundError("Could not find the configuration")


def load_schema(version: str) -> SchemaType:
    """Load the schema json file

    Arguments:
        version {str}

    Raises:
        InvalidVersionError

    Returns:
        schema {SchemaType}
    """

    basepath = Path(__file__).parent.resolve()
    filename = f"version_{version}.json"
    schema_filpath = f"{basepath}/schema/{filename}"

    try:
        with open(schema_filpath) as fobj:
            return json.load(fobj)
    except FileNotFoundError:
        raise InvalidVersionError(f"The version {repr(version)} is invalid")


def validate(config: ConfigType, version: str) -> bool:
    """Validate the configuration

    Arguments:
        config {ConfigType}
        version {str}

    Raises:
        ConfigInvalidSyntaxError

    Returns:
        bool
    """

    try:
        schema = load_schema(version)
        Draft7Validator(schema).validate(config)
    except ValidationError as err:
        raise ConfigInvalidSyntaxError(err)
    except Exception as err:
        raise err
    else:
        return True
