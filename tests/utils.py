from contextlib import contextmanager
from pathlib import Path
from typing import Generator

BASE_DIR = Path(__file__).parent


@contextmanager
def does_not_raise() -> Generator:
    yield
