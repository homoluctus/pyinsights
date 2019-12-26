import json
from pathlib import Path
from typing import Any, Dict

from jsonschema import Draft7Validator
from jsonschema.exceptions import ValidationError
from yaml import safe_load

from pyinsights.exceptions import (
    ConfigInvalidSyntaxError,
    ConfigNotFoundError,
    ConfigVersionUnknownError,
    InvalidVersionError
)


ConfigType = Dict[str, Any]
SchemaType = Dict[str, Any]


def load_config(filepath: str) -> ConfigType:
    """Load the configuration file

    Arguments:
        filepath {str}

    Raises:
        ConfigNotFoundError

    Returns:
        config {ConfigType}
    """

    try:
        with open(filepath) as fd:
            config = safe_load(fd)

        return config
    except FileNotFoundError:
        raise ConfigNotFoundError('Could not find the configuration')


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
    filename = f'version_{version}.json'
    schema_filpath = f'{basepath}/schema/{filename}'

    try:
        with open(schema_filpath) as fd:
            schema = json.load(fd)

        return schema
    except FileNotFoundError:
        raise InvalidVersionError(f'The version {repr(version)} is invalid')


def validate(config: ConfigType) -> bool:
    """Validate the configuration

    Arguments:
        config {ConfigType}

    Raises:
        ConfigVersionUnknownError
        ConfigInvalidSyntaxError

    Returns:
        bool
    """

    try:
        version = config['version']
    except KeyError:
        raise ConfigVersionUnknownError('Please specify the version')

    schema = load_schema(version)

    try:
        Draft7Validator(schema).validate(config)
        config.pop('version')
    except ValidationError as err:
        raise ConfigInvalidSyntaxError(err)
    else:
        return True
