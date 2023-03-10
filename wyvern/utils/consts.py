# MIT License

# Copyright (c) 2023 Sarthak

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

import typing


class Undefined:
    """An instance of this class is used as a placeholder to represent attributes and variables which
    are not defined *yet*."""


UNDEFINED = Undefined()
"""Instance of Undefined."""


class Empty:
    """This class is used for variables in an embed constructor to represent empty values."""

    def __xor__(self, other: object) -> object:
        return other

    @classmethod
    def verify(cls, other: typing.Any) -> typing.Any:
        return None if isinstance(other, Empty) else other


EMPTY = Empty()
"""Instance of Empty."""


class Null:
    """Class to simulate difference between an argument provided as None v/s a `null` value to send to the discord API.
    This class is used as a placeholder for arguments in REST methods.
    """


NULL = Null()
"""Instance of Null."""
