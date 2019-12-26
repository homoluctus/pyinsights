from datetime import datetime, timedelta

import pytest
from botocore.exceptions import ParamValidationError

from pyinsights.aws import InsightsClient


class TestInsightsClient:
    @pytest.fixture()
    def client(self):
        return InsightsClient(profile='crm-stg-sls', region='ap-northeast-1')

    @pytest.fixture()
    def times(self):
        end_time = datetime.now()
        start_time = end_time + timedelta(minutes=-10)
        return (start_time, end_time)

    @pytest.fixture()
    def pattern(self):
        pattern = (
            'parse @message /time:(?<time>.*)\t'
            + 'severity:(?<severity>.*)\tmodule:(?<module>.*)\t'
            + 'lineno:(?<lineno>\\d+)\tmessage:(?<msg>.*)/'
        )
        return pattern

    def test_valid_query(self, client, times, pattern):
        client.start_query(
            pattern=pattern,
            start_time=times[0],
            end_time=times[1],
            log_group_name=['/ecs/ecwms-bat'],
        )
        result = client.end_query()
        assert result is True

    def test_invalid_parameter(self, client, times):
        with pytest.raises(ParamValidationError):
            client.start_query(
                pattern='12345678',
                start_time=times[0],
                end_time=times[1],
                log_group_name='invalid',
            )

    def test_end_query_with_non_query_id(self, client):
        result = client.end_query()
        assert result is True

    def test_fetch_result(self, client, times, pattern):
        client.start_query(
            pattern=pattern,
            start_time=times[0],
            end_time=times[1],
            log_group_name=['/ecs/ecwms-bat'],
            limit=1,
        )

        results = client.fetch_result()
        assert isinstance(results, dict) is True
        assert len(results['results']) == 1
        assert results['status'] == 'Complete'

    def test_not_match_query_pattern(self, client, times, pattern):
        client.start_query(
            pattern=f'{pattern} | filter severity = "NONE"',
            start_time=times[0],
            end_time=times[1],
            log_group_name=['/ecs/ecwms-bat'],
            limit=1,
        )

        results = client.fetch_result()
        assert len(results['results']) == 0

    def test_end_query_after_query_stop(self, client, times, pattern):
        client.start_query(
            pattern=f'{pattern} | filter severity = "NONE"',
            start_time=times[0],
            end_time=times[1],
            log_group_name=['/ecs/ecwms-bat'],
            limit=1,
        )
        client.fetch_result()
        result = client.end_query()
        assert result is True
