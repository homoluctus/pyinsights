import json
from time import sleep
import concurrent.futures as confu
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Any, Dict

from pyinsights.aws import InsightsClient
from pyinsights.config import load_config, validate
from pyinsights.helper import get_times, processing


def query(params: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Query to CloudWatch Logs Insights

    Arguments:
        params {Dict[str, Dict[str, Any]]}

    Returns:
        results {Dict[str, Any]}
    """

    client = InsightsClient(**params['aws'])
    client.start_query(**params['query'])
    results = client.fetch_result()
    return results


def wait_result(thread) -> Dict[str, Any]:
    """Wait to get result

    Arguments:
        thread {[type]}

    Returns:
        results {Dict[str, Any]}
    """

    while True:
        try:
            results = thread.result(timeout=0.1)
        except confu.TimeoutError:
            processing('.', end='')
            sleep(0.5)
            pass
        else:
            if results:
                processing('.', end='\n')
                return results


def run_thread(params: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Run thread

    Arguments:
        params {Dict[str, Dict[str, Any]]}

    Returns:
        results = Dict[str, Any]
    """

    with ThreadPoolExecutor(max_workers=1) as executor:
        thread = executor.submit(query, params)
        processing('Waiting', end=' ')
        results = wait_result(thread)

    return results


def run(kwargs: Dict[str, str]) -> bool:
    """Run pyinsights

    Arguments:
        kwargs {Dict[str, Any]}

    Returns:
        bool
    """

    config = load_config(kwargs.pop('config'))
    validate(config)

    duration = config.pop('duration')
    if isinstance(duration, str):
        duration = get_times(duration)
    config.update(duration)
    params = {
        'aws': kwargs,
        'query': config
    }

    results = run_thread(params)

    for result in results['results']:
        for field in result:
            print(json.dumps(field, indent=2, ensure_ascii=False), flush=True)
            sleep(0.5)

    return True
