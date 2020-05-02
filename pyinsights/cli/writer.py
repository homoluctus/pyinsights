import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TextIO

from pyinsights.exceptions import OutputFileNotFoundError


@dataclass
class Writer:
    writer: TextIO

    def __del__(self) -> None:
        if self.writer is not sys.stdout:
            self.writer.close()

    @classmethod
    def from_filename(cls, filepath: str = None) -> "Writer":
        if filepath is None:
            writer = sys.stdout
        elif not isinstance(filepath, str):
            raise ValueError("output filename type is not str")
        elif cls.is_file(filepath) is False:
            raise OutputFileNotFoundError(f"Cloud not find {filepath!r}")
        else:
            writer = open(filepath, "w")

        return cls(writer)

    @staticmethod
    def is_file(filepath: str) -> bool:
        """filepathがfileなのかチェック

        Arguments:
            filepath {str}

        Returns:
            bool
        """

        path = Path(filepath)

        if path.is_file() or path.parent.is_dir():
            return True

        return False

    def write(self, contents: Any) -> None:
        self.writer.write(contents)
