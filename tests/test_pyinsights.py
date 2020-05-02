import os
import sys

import pytest

from pyinsights.pyinsights import run


CONFIG_FILEPATH_FOR_TEST = os.getenv("CONFIG_FILEPATH_FOR_TEST", "")
PROFILE_FOR_TEST = os.getenv("PROFILE_FOR_TEST", "")
REGION_FOR_TEST = os.getenv("REGION_FOR_TEST", "")


@pytest.mark.skipif(CONFIG_FILEPATH_FOR_TEST == "", reason="Use AWS Resource")
@pytest.mark.parametrize(
    "format_type, expectation", (("json", True), ("table", True))
)
def test_format_options(format_type: str, expectation: bool) -> None:
    sys.argv = [
        "pyinsights",
        "-r",
        REGION_FOR_TEST,
        "-p",
        PROFILE_FOR_TEST,
        "-c",
        CONFIG_FILEPATH_FOR_TEST,
        "-f",
        format_type,
    ]
    result = run()
    assert result is expectation
