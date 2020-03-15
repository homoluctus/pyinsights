from datetime import datetime, timedelta
from typing import Dict, Union

from pyinsights.exceptions import InvalidDurationError


def convert_to_epoch(duration: Union[str, datetime]) -> int:
    """Convert datetime string to epoch (POSIX timestamp)

    Arguments:
        duration {Union[str, datetime]}
            --  string format must be `%Y-%m-%d %H:%M:%S`
                if duration type is str

    Raises:
        InvalidDurationError

    Returns:
        epoch {int}
    """

    if isinstance(duration, str):
        time_format = "%Y-%m-%d %H:%M:%S"
        try:
            duration = datetime.strptime(duration, time_format)
        except ValueError:
            raise InvalidDurationError(
                f"{duration=} is invalid datetime format as \
                    duration parameter"
            )

    if not isinstance(duration, datetime):
        raise InvalidDurationError(
            f"Cloud not convert {duration=} to POSIX timestamp"
        )

    epoch = int(duration.timestamp())
    return epoch


TIME_UNITS = {
    "s": "seconds",
    "m": "minutes",
    "h": "hours",
    "d": "days",
    "w": "weeks",
}


def convert_string_duration_to_datetime(
    string_duration: str,
) -> Dict[str, datetime]:
    """Convert string duration to datetime

    Arguments:
        string_duration {str}

    Raises:
        InvalidDurationError

    Returns:
        Dict[str, datetime] -- `start_time` and `end_time` are key
    """

    try:
        duration = {TIME_UNITS[string_duration[-1]]: int(string_duration[:-1])}
    except (ValueError, IndexError, KeyError):
        raise InvalidDurationError(
            f"{string_duration=} is invalid as duration parameter"
        )

    end_time = datetime.now()
    start_time = end_time - timedelta(**duration)
    duraion_map = {"start_time": start_time, "end_time": end_time}
    return duraion_map
