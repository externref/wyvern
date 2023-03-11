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

import typing

__all__: tuple[str, ...] = ("BitWiseFlag", "_ListenerArg")


class BitWiseFlag:
    value: int

    def __init__(self, value: int) -> None:
        self.value = value

    _ignored_flags = ("ALL", "PRIVILEGED", "UNPRIVILEGED")

    def __iter__(self) -> typing.Generator[tuple[str, bool], None, None]:
        for flag in [attr for attr in dir(self) if attr.isupper() and attr not in self._ignored_flags]:
            if self.value & getattr(self, flag) != 0:
                yield flag, True
            else:
                yield flag, False

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(value={self.value})>"

    def __int__(self) -> int:
        return self.value

    def get_enabled(self, *, as_str: bool = False) -> tuple[int | str, ...]:
        return tuple((getattr(self, flag[0]) if as_str is False else flag[0]) for flag in list(self) if flag[1] is True)

    def get_disabled(self, *, as_str: bool = False) -> tuple[int | str, ...]:
        return tuple(
            (getattr(self, flag[0]) if as_str is False else flag[0]) for flag in list(self) if flag[1] is False
        )


class _ListenerArg:
    ...
