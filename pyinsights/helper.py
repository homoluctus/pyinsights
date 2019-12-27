import random
from datetime import datetime, timedelta
from typing import Dict, Type, Union

from pyinsights.exceptions import InvalidDurationError


DatetimeType = Type[datetime]


def convert_epoch(time: Union[str, DatetimeType]) -> int:
    """Convert datetime string to epoch (unix timestamp)

    Arguments:
        time {Union[str, DatetimeType]}
            -- datetime string that format is `%Y-%m-%d %H:%M:%S`

    Returns:
        epoch {int}
    """

    if isinstance(time, str):
        time_format = '%Y-%m-%d %H:%M:%S'
        try:
            time = datetime.strptime(time, time_format)
        except ValueError:
            raise InvalidDurationError(
                f'{repr(time)} is invalid as duration parameter'
            )

    epoch = int(time.timestamp())
    return epoch


time_unit_map = {
    's': 'seconds',
    'm': 'minutes',
    'h': 'hours'
}


def get_times(duration: str) -> Dict[str, DatetimeType]:
    try:
        unit = duration[-1]
        duration = int(duration[:-1])
        arg = {time_unit_map[unit]: duration}
    except (ValueError, IndexError, KeyError):
        raise InvalidDurationError(
            f'{repr(duration)} is invalid as duration parameter'
        )

    end_time = datetime.now()
    start_time = end_time - timedelta(**arg)
    times = {'start_time': start_time, 'end_time': end_time}
    return times


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
        end {str} -- (default: {''})
    """

    print(
        f'{Accessory.Accent}{color()}{msg}{Accessory.End}',
        flush=True,
        end=end
    )
