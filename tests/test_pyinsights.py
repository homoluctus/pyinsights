import os

import pytest

from pyinsights.pyinsights import run


LOG_GROUP_NAME = os.getenv('LOG_GROUP_NAME')


@pytest.mark.skipif(
    LOG_GROUP_NAME is None,
    reason='Use AWS Resource'
)
class TestPyInsights:
    @pytest.fixture()
    def kwargs(self):
        return {
            'profile': 'pyinsights',
            'region': 'ap-northeast-1',
            'config': 'examples/pyinsights1.yml'
        }

    def test_valid_kwargs(self, kwargs):
        result = run(kwargs)
        assert result is True
