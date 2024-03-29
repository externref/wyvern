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

import importlib
import typing

import attrs


@attrs.define
class Hook:
    name: str
    callback: typing.Callable[..., typing.Any]

    def __call__(self, *args: typing.Any, **kwds: typing.Any) -> None:
        self.callback(*args, **kwds)


def hook(name: str | None = None) -> typing.Callable[[typing.Callable[..., typing.Any]], Hook]:
    def decorator(callback: typing.Callable[..., typing.Any]) -> Hook:
        return Hook(name or callback.__name__, callback)

    return decorator


def parse_hooks(import_path: str) -> dict[str, Hook]:
    module = importlib.import_module(import_path)
    return {_hook.name: _hook for _hook in module.__dict__.values() if isinstance(_hook, Hook)}
