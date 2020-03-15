import sys
from random import randint
from typing import Union, ClassVar, Tuple
from dataclasses import dataclass


STREAM = sys.stdout


@dataclass
class Progress:
    spinners: ClassVar[Tuple[str, ...]] = (
        "⣾",
        "⣷",
        "⣯",
        "⣟",
        "⡿",
        "⢿",
        "⣻",
        "⣽",
    )
    snippers_length: ClassVar[int] = len(spinners)
    check_mark: ClassVar[str] = "\u2713"

    processing_msg: str
    end_msg: str
    quiet: bool = False

    def show(self, counter: int) -> None:
        if self.quiet is False:
            index = counter % (self.snippers_length - 1)
            spinner = self.spinners[index]
            color = Color.select_color_randomly()
            STREAM.write(
                f"\r{color}{spinner}{Color.disabled()} {self.processing_msg}"
            )
            STREAM.flush()

    def done(self) -> None:
        if self.quiet is False:
            color = Color.get_color_by_name("green")
            STREAM.write("\r")
            STREAM.write(" " * (len(self.processing_msg) + 5))
            STREAM.write(
                f"\r{color}{self.check_mark} {self.end_msg}{Color.disabled()}\n"
            )
            STREAM.flush()


class Color:
    default_color = "white"
    colors = ("red", "green", "yellow", "blue", "magenta", "cyan", "white")

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
    def color_ansi(cls, code: Union[str, int]) -> str:
        """Get color code

        Arguments:
            code {Union[str, int]}

        Returns:
            str
        """

        base_color_code = 30
        color_code = base_color_code + int(code)
        return cls.ansi(color_code)

    @classmethod
    def select_color_randomly(cls) -> str:
        """Select a color randomly

        Returns:
            str
        """

        code = randint(1, len(cls.colors))
        return cls.color_ansi(code)

    @classmethod
    def disabled(cls) -> str:
        """Disable color

        Returns:
            str
        """

        return cls.ansi("0")

    @classmethod
    def get_color_by_name(cls, color_name: str) -> str:
        """Get color code by name

        Arguments:
            color_name {str}

        Returns:
            str
        """

        color_name = color_name.lower()

        try:
            index = cls.colors.index(color_name)
        except ValueError:
            index = cls.colors.index(cls.default_color)

        return cls.color_ansi(index + 1)
