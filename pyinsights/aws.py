import os
from typing import Any, Dict, List, Optional, Union

import boto3
import botocore.errorfactory

from pyinsights.exceptions import (
    QueryNotYetStartError,
    NotFetchQueryResultError,
)
from pyinsights.helper import convert_epoch, DatetimeType


AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')


class InsightsClient:
    def __init__(
        self,
        region: Optional[str] = None,
        profile: Optional[str] = None,
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

        self._client = session.client('logs')
        self._query_id = None

    def start_query(
        self,
        query_string: str,
        start_time: Union[str, DatetimeType],
        end_time: Union[str, DatetimeType],
        log_group_name: List[str],
        limit: Optional[int] = 1000,
    ) -> bool:
        """Start query

        Arguments:
            query_string {str} -- query string
            start_time {Union[str, DatetimeType]}
                -- datetime that format is `%Y-%m-%d %H:%M:%S`
            end_time {Union[str, DatetimeType]}
                -- datetime that format is `%Y-%m-%d %H:%M:%S`
            log_group_name {List[str]} -- aws cloudwatch log group to query

        Keyword Arguments:
            limit {Optional[int] -- the maximum number of log events
                                    to return in the query. (default: {1000})

        Returns:
            bool
        """

        start_time_epoch = convert_epoch(start_time)
        end_time_epoch = convert_epoch(end_time)

        response = self._client.start_query(
            logGroupNames=log_group_name,
            startTime=start_time_epoch,
            endTime=end_time_epoch,
            queryString=query_string,
            limit=limit,
        )

        self._query_id = response['queryId']
        return True

    def fetch_result(self) -> Dict[str, Any]:
        """Fetch the query result

        Raises:
            QueryNotYetStartError

        Returns:
            results {Dict[str, Any]}
        """

        if self._query_id is None:
            raise QueryNotYetStartError('The Query has not yet started')

        results = self._client.get_query_results(queryId=self._query_id)
        status = results['status']

        if status in ['Scheduled', 'Running']:
            results.update(self.fetch_result())

        elif status == 'Failed':
            raise NotFetchQueryResultError('Could not fetch the query result')

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

        if self._query_id is None:
            return True

        try:
            result = self._client.stop_query(queryId=self._query_id)
            return result['success']
        except botocore.errorfactory.ClientError as err:
            already_stopped_msg = 'Query is not in Running or Scheduled state'
            if err.operation_name == 'StopQuery' \
                    and already_stopped_msg in err.__str__():
                return True
            raise err
        except Exception as err:
            raise err
