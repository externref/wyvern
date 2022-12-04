from __future__ import annotations

import abc
import typing

import attrs

if typing.TYPE_CHECKING:
    from typing_extensions import TypeAlias

    from .slash_commands import CommandChoice

    CallbackT: TypeAlias = typing.Callable[..., typing.Awaitable[typing.Any]]
    AutocompleteT: TypeAlias = typing.Callable[..., typing.Awaitable[typing.Sequence[typing.Union[CommandChoice, str]]]]

__all__: tuple[str,...] = ( "SlashOptionConverter",)

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
