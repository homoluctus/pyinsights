# pylint: disable=R0913

import os
import sys
from time import sleep
from typing import Any, Dict, List, Optional, cast

import boto3
import botocore.errorfactory

from pyinsights.config import ConfigType
from pyinsights.exceptions import (
    NotFetchQueryResultError,
    QueryAlreadyCancelled,
    QueryNotYetStartError,
    QueryTimeoutError,
    QueryUnknownError,
)
from pyinsights.progress import Progress


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")


QueryResultResponse = Dict[str, Any]


class InsightsClient:
    def __init__(
        self, region: Optional[str] = None, profile: Optional[str] = None,
    ) -> None:
        """
        Keyword Arguments:
            region {Optional[str]}
            profile {Optional[str]}
        """

        region_name = region or AWS_DEFAULT_REGION

        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=region_name,
            profile_name=profile,
        )

        self.__client = session.client("logs")
        self.__query_id = None

    def start_query(
        self,
        query_string: str,
        start_time: int,
        end_time: int,
        log_group_name: List[str],
        limit: Optional[int] = 1000,
    ) -> bool:
        """Start query

        Arguments:
            query_string {str} -- query string
            start_time {int} -- POSIX timestamp
            end_time {int} -- POSIX timestamp
            log_group_name {List[str]} -- aws cloudwatch log group to query

        Keyword Arguments:
            limit {Optional[int] -- the maximum number of log events
                                    to return in the query. (default: {1000})

        Returns:
            bool
        """

        response = self.__client.start_query(
            logGroupNames=log_group_name,
            startTime=start_time,
            endTime=end_time,
            queryString=query_string,
            limit=limit,
        )

        self.__query_id = response["queryId"]
        return True

    def fetch_result(self) -> Optional[QueryResultResponse]:
        """Fetch the query result

        Raises:
            QueryNotYetStartError
            NotFetchQueryResultError
            QueryTimeoutError
            QueryAlreadyCancelled
            QueryUnknownError

        Returns:
            Optional[QueryResultResponse]
        """

        if self.__query_id is None:
            raise QueryNotYetStartError("The Query has not yet started")

        results = self.__client.get_query_results(queryId=self.__query_id)
        status = results["status"]

        if status in ["Scheduled", "Running"]:
            results = None

        elif status == "Failed":
            raise NotFetchQueryResultError("Could not fetch the query result.")

        elif status == "Timeout":
            raise QueryTimeoutError("The query is timeout.")

        elif status == "Cancelled":
            raise QueryAlreadyCancelled(
                "The query has already been cancelled."
            )

        elif status == "Unknown":
            raise QueryUnknownError("The query occurs unknown error.")

        return results

    def end_query(self) -> bool:
        """Gracefully terminate query

        Raises:
            err:
                raise exception if InvalidParameterException,
                ServiceUnavailableException or other error occurs

        Returns:
            bool
        """

        if self.__query_id is None:
            return True

        try:
            result = self.__client.stop_query(queryId=self.__query_id)
            return result["success"]
        except botocore.errorfactory.ClientError as err:
            already_stopped_msg = "Query is not in Running or Scheduled state"
            if (
                err.operation_name == "StopQuery"
                and already_stopped_msg in err.__str__()
            ):
                return True
            raise err
        except Exception as err:
            raise err


def query(
    region: str,
    profile: str,
    query_params: ConfigType,
    quiet: bool = False,
    interval: float = 0.05,
) -> QueryResultResponse:
    """Run query to CloudWath Logs Insights

    Arguments:
        region {str}
        profile {str}
        query_params {ConfigType}

    Keyword Arguments:
        quiet {bool} (default: {False})
        interval {float} (default: {0.05})

    Returns:
        QueryResultResponse
    """

    client = InsightsClient(region, profile)
    client.start_query(**query_params)

    counter = 0
    progress = Progress(
        processing_msg="Search for matching logs...",
        end_msg="Search completed!",
        quiet=quiet,
    )

    try:
        while True:
            progress.show(counter)

            if (results := client.fetch_result()) is not None:
                progress.done()
                return cast(QueryResultResponse, results)

            counter += 1
            sleep(interval)

    except (
        QueryNotYetStartError,
        NotFetchQueryResultError,
        QueryTimeoutError,
        QueryAlreadyCancelled,
        QueryUnknownError,
    ) as err:
        sys.exit(err)

    except KeyboardInterrupt:
        client.end_query()
        sys.exit("\nAbort")
