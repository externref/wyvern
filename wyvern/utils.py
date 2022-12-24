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
"""Utility functions and classes for the library."""
from __future__ import annotations

import ast
import datetime
import inspect
import typing

import attrs

__all__: tuple[str, ...] = ("Empty", "EMPTY", "get_arg_count", "create_timestamp", "Eval", "Hook", "as_hook")


class Empty:
    ...


EMPTY = Empty()


def get_arg_count(callable: typing.Callable[..., typing.Any]) -> int:
    """Counts the number of args in a callable.

    Parameters
    ----------
    callable : typing.Callable[..., typing.Any]
        The callable to get arg count of.

    Returns
    -------
    int
        Number of arguments in a callable.
    """
    return len(inspect.getargs(callable.__code__).args)


def copy_docs(_from: typing.Any, replace: dict[str, str] = {}) -> typing.Callable[[typing.Any], typing.Any]:
    def copy(_to: typing.Any) -> typing.Any:
        _to.__doc__ = _from.__doc__
        [_to.__doc__.replace(text, replacement) for text, replacement in replace.items()]
        return _to

    return copy


def create_timestamp(dt: datetime.datetime | datetime.timedelta, *, style: str = "t") -> str:
    """Creates an UNIX timestamp for provided datetime or timedelta object.

    Parameters
    ----------
    dt : datetime.datetime | datetime.timedelta
        The datetime or timedelta to convert.

    Returns
    -------
    str
        The UNIX timestamp.
    """
    if isinstance(dt, datetime.timedelta):
        dt = datetime.datetime.utcnow() + dt
    return f"<t:{int(dt.timestamp())}:{style}>"


@attrs.define(kw_only=True)
class CacheConfigurations:
    users: bool = True
    guilds: bool = True
    members: bool = True
    roles: bool = True
    channels: bool = True
    messages: bool = False


@attrs.define
class Hook:
    """Hooks for per-module setup. They can be loaded using `GatewayClient.load_hooks`"""

    callback: typing.Callable[..., typing.Any]
    """Callback of the hook."""
    name: str
    """Name of the hook."""

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        return self.callback(*args, **kwargs)


def as_hook(name: str | None = None) -> typing.Callable[..., Hook]:
    """Creates a [wyvern.utils.Hook][]

    Parameters
    ----------
    name : str
        Name of the hook.

    Returns
    -------
    wyvern.utils.Hook
        The hook that was created.
    """

    def inner(callback: typing.Callable[..., typing.Any]) -> Hook:
        return Hook(callback, name or callback.__name__)

    return inner


class Eval:
    """Class for code evaluation.

    !!! warning
        This class is not sandboxed so data like environmental variables
        will be evaluated when the methods gets executed as well.

    """

    def add_returns(self, body: typing.Any) -> None:
        if isinstance(body[-1], ast.Expr):
            body[-1] = ast.Return(body[-1].value)
            ast.fix_missing_locations(body[-1])

        # for if statements, we insert returns into the body and the orelse
        if isinstance(body[-1], ast.If):
            self.add_returns(body[-1].body)
            self.add_returns(body[-1].orelse)

        # for with blocks, again we insert returns into the body
        if isinstance(body[-1], ast.With):
            self.add_returns(body[-1].body)

    async def f_eval(self, *, code: str, renv: dict[str, typing.Any]) -> typing.Any:
        """Evaluates the code in the bot's namespace.

        Parameters
        ----------
        code : str
            The code to evaluate.
        renv: dict[str, typing.Any]
            Environment to evaluate code in.

        Returns
        -------
        typing.Any
            The result of the code.

        """
        _fn_name = "__wyvern_eval"
        code = "\n".join(f"    {i}" for i in code.strip().splitlines())
        parsed: typing.Any = ast.parse(f"async def {_fn_name}:\n{code}")
        self.add_returns(parsed.body[0].body)
        exec(compile(parsed, filename="<ast>", mode="exec"), renv)
        fn = renv[_fn_name]
        return await fn()
