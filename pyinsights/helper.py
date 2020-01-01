import sys
import random
from datetime import datetime, timedelta
from typing import Dict, Type, Union

from pyinsights.exceptions import InvalidDurationError


DatetimeType = Type[datetime]


def convert_to_epoch(duration: Union[str, DatetimeType]) -> int:
    """Convert datetime string to epoch (POSIX timestamp)

    Arguments:
        duration {Union[str, DatetimeType]}
            --  string format must be `%Y-%m-%d %H:%M:%S`
                if duration type is str

    Raises:
        InvalidDurationError

    Returns:
        epoch {int}
    """

    if isinstance(duration, str):
        time_format = '%Y-%m-%d %H:%M:%S'
        try:
            duration = datetime.strptime(duration, time_format)
        except ValueError:
            raise InvalidDurationError(
                f'{duration=} is invalid datetime format as \
                    duration parameter'
            )

    if not isinstance(duration, datetime):
        raise InvalidDurationError(
            f'Cloud not convert {duration=} to POSIX timestamp'
        )

    epoch = int(duration.timestamp())
    return epoch


TIME_UNITS = {
    's': 'seconds',
    'm': 'minutes',
    'h': 'hours',
    'd': 'days',
    'w': 'weeks'
}


def convert_string_duration_to_datetime(
    string_duration: str
) -> Dict[str, DatetimeType]:
    """Convert string duration to datetime

    Arguments:
        string_duration {str}

    Raises:
        InvalidDurationError

    Returns:
        Dict[str, DatetimeType] -- `start_time` and `end_time` are key
    """

    try:
        duration = {
            TIME_UNITS[string_duration[-1]]: int(string_duration[:-1])
        }
    except (ValueError, IndexError, KeyError):
        raise InvalidDurationError(
            f'{string_duration=} is invalid as duration parameter'
        )

    end_time = datetime.now()
    start_time = end_time - timedelta(**duration)
    duraion_map = {
        'start_time': start_time,
        'end_time': end_time
    }
    return duraion_map


def color() -> str:
    """Choice a color

    Returns:
        str
    """

    colors = [
        Color.Red,
        Color.Green,
        Color.Yellow,
        Color.Blue,
        Color.Purple,
        Color.Cyan
    ]
    color = random.choice(colors)
    return color


class Color:
    Red = '\033[31m'
    Green = '\033[32m'
    Yellow = '\033[33m'
    Blue = '\033[34m'
    Purple = '\033[35m'
    Cyan = '\033[36m'


class Accessory:
    End = '\033[0m'
    Accent = '\033[01m'


def processing(msg: str, end: str = '') -> None:
    """Display processing on terminal

    Arguments:
        msg {str}

    Keyword Arguments:
        end {str} - - (default: {''})
    """

    processing_msg = f'{Accessory.Accent}{color()}{msg}{Accessory.End}{end}'
    sys.stdout.write(processing_msg)
    sys.stdout.flush()
