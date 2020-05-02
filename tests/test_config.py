from typing import Any

import pytest

from pyinsights.config import load_config, load_schema, validate
from pyinsights.exceptions import (
    ConfigInvalidSyntaxError,
    ConfigNotFoundError,
    InvalidVersionError,
    InvalidQueryStringError,
)

from tests.utils import BASE_DIR, does_not_raise


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


@pytest.mark.parametrize(
    "filename, expectation",
    (
        ("correct/config1.yml", does_not_raise()),
        ("correct/config2.yml", does_not_raise()),
        ("correct/config3.yml", does_not_raise()),
        ("invalid/version.yml", pytest.raises(InvalidVersionError)),
        (
            "invalid/additional_property.yml",
            pytest.raises(ConfigInvalidSyntaxError),
        ),
        ("non-existence", pytest.raises(ConfigNotFoundError)),
    ),
)
def test_load_config(filename: str, expectation: Any) -> None:
    with expectation:
        config = load_config(f"{BASE_DIR}/fixtures/config/{filename}")
        result = validate(config.content, config.version)
        assert result is True


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
    conf = load_config(f"{BASE_DIR}/fixtures/config/{filename}")

    with expectation:
        conf.format_query_string()
        assert isinstance(conf.content["query_string"], str) is True
