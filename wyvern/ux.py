# MIT License

# Copyright (c) 2022 Sarthak

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

import enum
import logging
import typing

__all__: tuple[str, ...] = ("LoggingFormatter", "create_logging_setup", "ANSI", "ANSIBuilder")


class LoggingFormatter(logging.Formatter):

    COLOR_CONFIGS = {
        logging.DEBUG: "\x1b[33;49m",
        logging.INFO: "\x1b[32;49m",
        logging.WARNING: "\x1b[35;49m",
        logging.ERROR: "\x1b[31;49m",
        logging.CRITICAL: "\x1b[33;41;1m",
    }

    def format(self, record: logging.LogRecord) -> str:
        log_format = f"[%(asctime)s : {record.levelname.rjust(7)}] | %(message)s "

        formatter = logging.Formatter(
            "".join((self.COLOR_CONFIGS.get(record.levelno, "\x1b[32;49m"), log_format, "\x1b[0m"))
        )
        return formatter.format(record)


def create_logging_setup(logger: logging.Logger) -> None:
    stream = logging.StreamHandler()
    stream.setFormatter(LoggingFormatter())
    logger.addHandler(stream)
    logger.setLevel(logging.INFO)


class ANSI(enum.IntEnum):
    NORMAL_FORMAT = 0
    BOLD_FORMAT = 1
    UNDERLINE_FORMAT = 4
    GRAY_TEXT = 30
    RED_TEXT = 31
    GREEN_TEXT = 32
    YELLOW_TEXT = 33
    BLUE_TEXT = 34
    PINK_TEXT = 35
    CYAN_TEXT = 36
    WHITE_TEXT = 37
    FIREFLY_DARK_BLUE_BACKGROUND = 40
    ORANGE_BACKGROUND = 41
    MARBLE_BLUE_BACKGROUND = 42
    GREYISH_TURQUOISE_BACKGROUND = 43
    GRAY_BACKGROUND = 44
    INDIGO_BACKGROUND = 45
    LIGHT_GRAY_BACKGROUND = 46
    WHITE_BACKGROUND = 0


class ANSIBuilder:
    bucket: list[str]
    current_cursor: str

    def __enter__(self) -> ANSIBuilder:
        self.bucket = []
        self.current_cursor = ""
        return self

    def __exit__(self, *args: typing.Any) -> None:
        ...

    def set_cursor(self, *args: ANSI | int) -> ANSIBuilder:
        self.current_cursor = (
            f"\033[{';'.join(map(lambda arg: str(arg.value) if isinstance(arg, ANSI) else str(arg), args))}m"
        )
        self.bucket.append(self.current_cursor)
        return self

    def write(self, text: str, *, newline: bool = False) -> ANSIBuilder:
        self.bucket.append(text + "\n" if newline is True else "")

        return self

    def reset(self) -> ANSIBuilder:
        self.current_cursor = "\033[0m"
        self.bucket.append(self.current_cursor)
        return self

    def get_str(self) -> str:
        return "".join(self.bucket)
