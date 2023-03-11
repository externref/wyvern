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

import abc
import typing

import attrs

if typing.TYPE_CHECKING:
    from wyvern._types import AutocompleteT


__all__: tuple[str, ...] = ("SlashOptionConverter",)


@attrs.define(kw_only=True)
class BaseCallable(abc.ABC):
    callback: typing.Any

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        return self.callback(*args, **kwargs)


class HasAutoComplete(abc.ABC):
    autocompletes: dict[str, "AutocompleteT"] = {}

    async def with_autocomplete(
        self, opt_name: str | None = None, *, opt_names: typing.Sequence[str] = ()
    ) -> typing.Callable[..., "AutocompleteT"]:
        def inner(callback: "AutocompleteT") -> "AutocompleteT":
            nonlocal opt_name, opt_names
            if opt_name is not None and opt_names == ():
                self.autocompletes[opt_name] = callback
            elif opt_names != ():
                for opt in opt_names:
                    self.autocompletes[opt] = callback
            else:
                raise ValueError("You need to provide one of the `opt_name` or `opt_names` values.")

            return callback

        return inner


class HasSubCommands(abc.ABC):
    subcommands: dict[str, typing.Any] = {}

    @abc.abstractmethod
    def with_subcommand(self, *, name: str, description: str) -> typing.Any:
        ...


class SlashOptionConverter(abc.ABC):
    async def convert(self, arg: str) -> typing.Any:
        ...
