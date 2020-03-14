from typing import Any

import pytest

from pyinsights.config import load_config, load_schema, validate, ConfigFile
from pyinsights.exceptions import (
    ConfigInvalidSyntaxError,
    ConfigNotFoundError,
    InvalidVersionError,
)

from tests.utils import does_not_raise


@pytest.mark.parametrize(
    "filepath, expectation",
    (
        ("examples/pyinsights1.yml", does_not_raise()),
        ("invalid", pytest.raises(ConfigNotFoundError)),
    ),
)
def test_load_config(filepath: str, expectation: Any) -> None:
    with expectation:
        assert isinstance(load_config(filepath), ConfigFile) is True


@pytest.mark.parametrize(
    "version, expectation",
    (
        ("1.0", does_not_raise()),
        ("invalid", pytest.raises(InvalidVersionError)),
    ),
)
def test_load_schema(version: str, expectation: Any) -> None:
    with expectation:
        assert isinstance(load_schema(version), dict) is True


def test_valid_config() -> None:
    config = load_config("examples/pyinsights1.yml")
    result = validate(config.content, config.version)
    assert result is True


@pytest.mark.parametrize(
    "key, invalid_value, exception",
    (
        ("version", "invalid", InvalidVersionError),
        ("test", "this is test", ConfigInvalidSyntaxError),
    ),
)
def test_invalid_config(
    key: str, invalid_value: str, exception: Exception
) -> None:
    config = load_config("examples/pyinsights1.yml")
    config.content[key] = invalid_value
    with pytest.raises(exception):
        validate(config.content, config.version)
