import pytest

from pyinsights.config import load_config, load_schema, validate
from pyinsights.exceptions import (
    ConfigInvalidSyntaxError,
    ConfigNotFoundError,
    InvalidVersionError
)


class TestLoadConfig:
    def test_existing_config(self):
        filepath = 'examples/pyinsights1.yml'
        config = load_config(filepath)
        assert config.filename == filepath
        assert isinstance(config.version, str) is True

    def test_non_existing_config(self):
        with pytest.raises(ConfigNotFoundError):
            load_config('invalid')


class TestLoadSchema:
    def test_existing_schema(self):
        existing_version = '1.0'
        result = load_schema(existing_version)
        assert isinstance(result, dict) is True

    def test_non_existing_schema_version(self):
        with pytest.raises(InvalidVersionError):
            load_schema('invalid')


class TestValidator:
    @pytest.fixture()
    def config(self):
        return load_config('examples/pyinsights1.yml')

    def test_valid_config(self, config):
        result = validate(config.content, config.version)
        assert result is True

    def test_invalid_version(self, config):
        config.content['version'] = 'invalid'
        with pytest.raises(InvalidVersionError):
            validate(config.content, config.version)

    def test_invalid_config_content(self, config):
        config.content['test'] = 'this is test'
        with pytest.raises(ConfigInvalidSyntaxError):
            validate(config.content, config.version)
