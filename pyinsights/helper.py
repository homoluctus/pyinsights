import sys
from random import randint
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


class Color:
    @classmethod
    def ansi(cls, code: Union[str, int]) -> str:
        """Get ansi

        Arguments:
            code {Union[str, int]}

        Returns:
            str
        """

        return f"\033[{code}m"

    @classmethod
    def select_color_randomly(cls) -> str:
        """Select a color randomly

        Returns:
            str
        """

        code = randint(1, 6)
        return cls.ansi(30 + code)

    @classmethod
    def disabled(cls) -> str:
        """Disable color

        Returns:
            str
        """

        return cls.ansi("0")

    @classmethod
    def bold(cls) -> str:
        """Get bold code

        Returns:
            str
        """

        return cls.ansi("01")


def processing(msg: str, end: str = "") -> None:
    """Display processing on terminal

    Arguments:
        msg {str}

    Keyword Arguments:
        end {str} -- (default: {''})
    """

    processing_msg = f"{Color.bold()}{Color.select_color_randomly()}{msg}{Color.disabled()}{end}"
    sys.stdout.write(processing_msg)
    sys.stdout.flush()
