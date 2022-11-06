from __future__ import annotations

import typing

import attrs

if typing.TYPE_CHECKING:
    from .slash_commands import CommandChoice

CallbackT = typing.TypeVar("CallbackT", bound=typing.Callable[..., typing.Awaitable[typing.Any]])


@attrs.define(kw_only=True)
class BaseCallable:
    callback: typing.Any

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        return self.callback(*args, **kwargs)


class HasAutoComplete:
    autocompletes: dict[str, typing.Callable[..., typing.Awaitable[typing.Sequence["CommandChoice" | str]]]] = {}

    async def with_autocomplete(
        self, opt_name: str | None = None, *, opt_names: typing.Sequence[str] = ()
    ) -> typing.Callable[..., typing.Callable[..., typing.Awaitable[typing.Sequence["CommandChoice" | str]]]]:
        def inner(
            callback: typing.Callable[..., typing.Awaitable[typing.Sequence["CommandChoice" | str]]]
        ) -> typing.Callable[..., typing.Awaitable[typing.Sequence["CommandChoice" | str]]]:
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


class HasSubCommands:
    subcommands: dict[str, typing.Any] = {}

    async def with_subcommand(self, name: str, description: str) -> typing.Any:
        def inner(callback: typing.Callable[..., typing.Callable[..., typing.Awaitable[typing.Any]]]) -> typing.Any:
            ...


class SlashOptionConverter:
    async def convert(self, arg: str) -> typing.Any:
        ...
