from typing import Any
from pathlib import Path

import pytest

from pyinsights.config import load_config, load_schema, validate, ConfigFile
from pyinsights.exceptions import (
    ConfigInvalidSyntaxError,
    ConfigNotFoundError,
    InvalidVersionError,
    InvalidQueryStringError,
)

from tests.utils import does_not_raise


BASE_DIR = Path(__file__).parent


@pytest.mark.parametrize(
    "filepath, expectation",
    (
        (f"{BASE_DIR}/fixtures/correct/config1.yml", does_not_raise()),
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
    config = load_config(f"{BASE_DIR}/fixtures/correct/config1.yml")
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
    config = load_config(f"{BASE_DIR}/fixtures/correct/config1.yml")
    config.content[key] = invalid_value
    with pytest.raises(exception):
        validate(config.content, config.version)


@pytest.mark.parametrize(
    "filename, expectation",
    (
        ("correct/config1.yml", does_not_raise()),
        ("correct/config2.yml", does_not_raise()),
        ("correct/config3.yml", does_not_raise()),
        ("invalid/query_string1.yml", pytest.raises(InvalidQueryStringError)),
        ("invalid/query_string2.yml", pytest.raises(InvalidQueryStringError)),
    ),
)
def test_format_query_string(filename: str, expectation: Any) -> None:
    conf = load_config(f"{BASE_DIR}/fixtures/{filename}")

    with expectation:
        conf.format_query_string()
        assert isinstance(conf.content["query_string"], str) is True
