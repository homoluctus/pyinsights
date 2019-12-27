import os
from datetime import datetime, timedelta

import pytest
from botocore.exceptions import ParamValidationError

from pyinsights.aws import InsightsClient


LOG_GROUP_NAME = os.getenv('LOG_GROUP_NAME')


@pytest.mark.skipif(
    LOG_GROUP_NAME is None,
    reason='Use AWS Resource'
)
class TestInsightsClient:
    @pytest.fixture()
    def client(self):
        return InsightsClient(profile='pyinsights', region='ap-northeast-1')

    @pytest.fixture()
    def times(self):
        end_time = datetime.now()
        start_time = end_time + timedelta(minutes=-10)
        return (start_time, end_time)

    @pytest.fixture()
    def query_string(self):
        query_string = (
            'parse @message /time:(?<time>.*)\t'
            + 'severity:(?<severity>.*)\tmodule:(?<module>.*)\t'
            + 'lineno:(?<lineno>\\d+)\tmessage:(?<msg>.*)/'
        )
        return query_string

    def test_valid_query(self, client, times, query_string):
        client.start_query(
            query_string=query_string,
            start_time=times[0],
            end_time=times[1],
            log_group_name=[LOG_GROUP_NAME],
        )
        result = client.end_query()
        assert result is True

    def test_invalid_parameter(self, client, times):
        with pytest.raises(ParamValidationError):
            client.start_query(
                query_string='12345678',
                start_time=times[0],
                end_time=times[1],
                log_group_name='invalid',
            )

    def test_end_query_with_non_query_id(self, client):
        result = client.end_query()
        assert result is True

    def test_fetch_result(self, client, times, query_string):
        client.start_query(
            query_string=query_string,
            start_time=times[0],
            end_time=times[1],
            log_group_name=[LOG_GROUP_NAME],
            limit=1,
        )

        results = client.fetch_result()
        assert isinstance(results, dict) is True
        assert len(results['results']) == 1
        assert results['status'] == 'Complete'

    def test_not_match_query_pattern(self, client, times, query_string):
        client.start_query(
            query_string=f'{query_string} | filter severity = "NONE"',
            start_time=times[0],
            end_time=times[1],
            log_group_name=[LOG_GROUP_NAME],
            limit=1,
        )

        results = client.fetch_result()
        assert len(results['results']) == 0

    def test_end_query_after_query_stop(self, client, times, query_string):
        client.start_query(
            query_string=f'{query_string} | filter severity = "NONE"',
            start_time=times[0],
            end_time=times[1],
            log_group_name=[LOG_GROUP_NAME],
            limit=1,
        )
        client.fetch_result()
        result = client.end_query()
        assert result is True
