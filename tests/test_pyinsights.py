import os

import pytest

from pyinsights.pyinsights import run


CONFIG_FILEPATH_FOR_TEST = os.getenv('CONFIG_FILEPATH_FOR_TEST')
PROFILE_FOR_TEST = os.getenv('PROFILE_FOR_TEST')
REGION_FOR_TEST = os.getenv('REGION_FOR_TEST')


@pytest.mark.skipif(
    CONFIG_FILEPATH_FOR_TEST is None,
    reason='Use AWS Resource'
)
class TestPyInsights:
    @pytest.fixture()
    def kwargs(self):
        return {
            'profile': PROFILE_FOR_TEST,
            'region': REGION_FOR_TEST,
            'config': CONFIG_FILEPATH_FOR_TEST
        }

    def test_valid_kwargs_with_json_format(self, kwargs):
        kwargs['format'] = 'json'
        result = run(kwargs)
        assert result is True

    def test_valid_kwargs_with_table_format(self, kwargs):
        kwargs['format'] = 'table'
        result = run(kwargs)
        assert result is True
