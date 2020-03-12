import os

import pytest

from pyinsights.cli import run


CONFIG_FILEPATH_FOR_TEST = os.getenv("CONFIG_FILEPATH_FOR_TEST", "")
PROFILE_FOR_TEST = os.getenv("PROFILE_FOR_TEST", "")
REGION_FOR_TEST = os.getenv("REGION_FOR_TEST", "")


@pytest.mark.skipif(CONFIG_FILEPATH_FOR_TEST == "", reason="Use AWS Resource")
@pytest.mark.parametrize(
    "format_type, expectation", (("json", True), ("table", True))
)
def test_format_options(format_type: str, expectation: bool) -> None:
    common_kwargs = {
        "profile": PROFILE_FOR_TEST,
        "region": REGION_FOR_TEST,
        "config": CONFIG_FILEPATH_FOR_TEST,
    }
    common_kwargs["format"] = format_type
    result = run(common_kwargs)
    assert result is expectation
