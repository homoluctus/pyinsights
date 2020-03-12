from datetime import datetime
from typing import Any, Union

import pytest

from pyinsights.exceptions import InvalidDurationError
from pyinsights.helper import (
    color,
    convert_to_epoch,
    convert_string_duration_to_datetime,
)

from tests.utils import does_not_raise


@pytest.mark.parametrize(
    "arg, expectation",
    (
        ("2019-12-25 00:00:00", does_not_raise()),
        (datetime.now(), does_not_raise()),
        ("invalid", pytest.raises(InvalidDurationError)),
    ),
)
def test_convert_to_epoch(arg: Union[str, datetime], expectation: Any) -> None:
    with expectation:
        assert isinstance(convert_to_epoch(arg), int) is True


@pytest.mark.parametrize(
    "duration, expectation_gt_time, expectation_lt_time",
    (("10s", 9, 11), ("10m", 540, 660), ("10h", 32400, 39600)),
)
def test_convert_string_duration_to_datetime_with_valid_arg(
    duration: str, expectation_gt_time: int, expectation_lt_time: int
) -> None:
    results = convert_string_duration_to_datetime(duration)
    tmp = {k: convert_to_epoch(v) for k, v in results.items()}
    time_diff = tmp["end_time"] - tmp["start_time"]
    assert time_diff > expectation_gt_time
    assert time_diff < expectation_lt_time


@pytest.mark.parametrize(
    "invalid_arg, exception",
    (
        ("invalid", InvalidDurationError),
        ("", InvalidDurationError),
        ("10", InvalidDurationError),
    ),
)
def test_convert_string_duration_to_datetime_with_invalid_arg(
    invalid_arg: str, exception: Exception
) -> None:
    with pytest.raises(exception):
        convert_string_duration_to_datetime(invalid_arg)


def test_color() -> None:
    result = color()
    assert result.startswith("\033[") is True
    assert result.endswith("m") is True
