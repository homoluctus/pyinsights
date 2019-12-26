from datetime import datetime

import pytest

from pyinsights.exceptions import InvalidDurationError
from pyinsights.helper import convert_epoch, get_times, color


class TestConvertEpoch:
    def test_valid_str_arg(self):
        arg = '2019-12-25 00:00:00'
        result = convert_epoch(arg)
        assert isinstance(result, int) is True

    def test_invalid_str_arg(self):
        invalid_arg = 'invalid'
        with pytest.raises(InvalidDurationError):
            convert_epoch(invalid_arg)

    def test_valid_datetime_arg(self):
        result = convert_epoch(datetime.now())
        assert isinstance(result, int) is True


class TestGetTimes:
    def test_with_seconds_arg(self):
        duration = '10s'
        results = get_times(duration)
        tmp = {k: convert_epoch(v) for k, v in results.items()}
        time_diff = tmp['end_time'] - tmp['start_time']
        assert time_diff > 9  # > 9s
        assert time_diff < 11  # < 11s

    def test_with_minutes_arg(self):
        duration = '10m'
        results = get_times(duration)
        tmp = {k: convert_epoch(v) for k, v in results.items()}
        time_diff = tmp['end_time'] - tmp['start_time']
        assert time_diff > 540  # > 9m
        assert time_diff < 660  # < 11m

    def test_with_howiturs_arg(self):
        duration = '10h'
        results = get_times(duration)
        tmp = {k: convert_epoch(v) for k, v in results.items()}
        time_diff = tmp['end_time'] - tmp['start_time']
        assert time_diff > 32400  # > 9h
        assert time_diff < 39600  # < 11h

    def test_with_value_error_arg(self):
        with pytest.raises(InvalidDurationError):
            get_times('invalid')

    def test_with_index_error_arg(self):
        with pytest.raises(InvalidDurationError):
            get_times('')

    def test_with_key_error_arg(self):
        with pytest.raises(InvalidDurationError):
            get_times('10')


class TestColor:
    def test_color(self):
        result = color()
        assert result.startswith('\033[') is True
        assert result.endswith('m') is True
