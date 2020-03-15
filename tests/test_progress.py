import pytest

from pyinsights.progress import Color


@pytest.mark.parametrize(
    "color_name, expectation",
    (
        ("red", "\033[31m"),
        ("green", "\033[32m"),
        ("yellow", "\033[33m"),
        ("blue", "\033[34m"),
        ("magenta", "\033[35m"),
        ("cyan", "\033[36m"),
        ("white", "\033[37m"),
        # get default color (=white)
        ("invalid", "\033[37m"),
    ),
)
def test_get_color_by_name(color_name: str, expectation: str) -> None:
    result = Color.get_color_by_name(color_name)
    assert result == expectation


def test_color_disabled() -> None:
    result = Color.disabled()
    assert result == "\033[0m"
