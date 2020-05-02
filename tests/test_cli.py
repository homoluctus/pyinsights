from typing import Any

import pytest

from pyinsights.cli.writer import Writer
from pyinsights.exceptions import OutputFileNotFoundError

from tests.utils import BASE_DIR, does_not_raise


@pytest.mark.parametrize(
    "filepath, raises",
    (
        (None, does_not_raise()),
        (f"{BASE_DIR}/fixtures/writer.json", does_not_raise(),),
        (1, pytest.raises(ValueError)),
        ("/invalid/invalid.json", pytest.raises(OutputFileNotFoundError)),
    ),
)
def test_writer(filepath: Any, raises: Any) -> None:
    with raises:
        writer = Writer.from_filename(filepath)
        assert writer.writer.writable() is True
