import pytest

from pyinsights.pyinsights import run


class TestPyInsights:
    @pytest.fixture()
    def kwargs(self):
        return {
            'profile': 'crm-stg-sls',
            'region': 'ap-northeast-1',
            'config': 'examples/pyinsights1.yml'
        }

    def test_valid_kwargs(self, kwargs):
        result = run(kwargs)
        assert result is True
