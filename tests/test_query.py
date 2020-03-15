# pylint: disable=R0201

import os
from datetime import datetime, timedelta
from typing import Tuple

import pytest

from pyinsights.query import InsightsClient
from pyinsights.helper import convert_to_epoch


LOG_GROUP_NAME = os.getenv("LOG_GROUP_NAME", "")


@pytest.mark.skipif(LOG_GROUP_NAME == "", reason="Use AWS Resource")
class TestInsightsClient:
    @pytest.fixture()
    def client(self) -> InsightsClient:
        return InsightsClient(profile="pyinsights", region="ap-northeast-1")

    @pytest.fixture()
    def times(self) -> Tuple[int, int]:
        tmp_end_time = datetime.now()
        start_time = convert_to_epoch(tmp_end_time + timedelta(minutes=-10))
        end_time = convert_to_epoch(tmp_end_time)
        return (start_time, end_time)

    @pytest.fixture()
    def query_string(self) -> str:
        query_string = (
            "parse @message /time:(?<time>.*)\t"
            + "severity:(?<severity>.*)\tmodule:(?<module>.*)\t"
            + "lineno:(?<lineno>\\d+)\tmessage:(?<msg>.*)/"
        )
        return query_string

    def test_valid_query(
        self, client: InsightsClient, times: Tuple[int, int], query_string: str
    ) -> None:
        client.start_query(
            query_string=query_string,
            start_time=times[0],
            end_time=times[1],
            log_group_name=[LOG_GROUP_NAME],
        )
        result = client.end_query()
        assert result is True

    def test_end_query_with_non_query_id(self, client: InsightsClient) -> None:
        result = client.end_query()
        assert result is True

    def test_fetch_result(
        self, client: InsightsClient, times: Tuple[int, int], query_string: str
    ) -> None:
        client.start_query(
            query_string=query_string,
            start_time=times[0],
            end_time=times[1],
            log_group_name=[LOG_GROUP_NAME],
            limit=1,
        )

        results = client.fetch_result()
        assert results is None or isinstance(results, dict) is True

    def test_not_match_query_pattern(
        self, client: InsightsClient, times: Tuple[int, int], query_string: str
    ) -> None:
        client.start_query(
            query_string=f'{query_string} | filter severity = "NONE"',
            start_time=times[0],
            end_time=times[1],
            log_group_name=[LOG_GROUP_NAME],
            limit=1,
        )

        results = client.fetch_result()
        assert results is None or isinstance(results, dict) is True

    def test_end_query_after_query_stop(
        self, client: InsightsClient, times: Tuple[int, int], query_string: str
    ) -> None:
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
