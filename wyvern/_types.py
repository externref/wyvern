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

if typing.TYPE_CHECKING:
    from typing_extensions import TypeAlias

    from wyvern._internals import _ListenerArg
    from wyvern.clients import CommandsClient
    from wyvern.commands.slash_commands import CommandChoice
    from wyvern.components.buttons import Button
    from wyvern.interactions.applications import (
        ApplicationCommandInteraction,
        AutocompleteInteraction,
        InteractionOption,
    )
    from wyvern.interactions.components import ComponentInteraction

    CheckT: TypeAlias = typing.Callable[..., typing.Awaitable[bool]]
    AnyCallableT: TypeAlias = typing.Callable[..., typing.Awaitable[typing.Any]]
    CallbackT: TypeAlias = typing.Callable[..., typing.Awaitable[typing.Any]]
    AutocompleteT: TypeAlias = typing.Callable[
        [AutocompleteInteraction, InteractionOption],
        typing.Awaitable[typing.Sequence[typing.Union[CommandChoice, str]]],
    ]
    ButtonCallbackT: TypeAlias = typing.Callable[[Button, ComponentInteraction], typing.Awaitable[typing.Any]]

    class AppCommandCallbackT(typing.Protocol):
        @typing.overload
        def __call__(
            self, inter_or_client: CommandsClient, inter: ApplicationCommandInteraction, /, *args: typing.Any
        ) -> typing.Any:
            ...

        @typing.overload
        def __call__(self, inter_or_client: ApplicationCommandInteraction, /, *args: typing.Any) -> typing.Any:
            ...

        def __call__(
            self, inter_or_client: ApplicationCommandInteraction | CommandsClient, /, *args: typing.Any
        ) -> typing.Any:
            ...

    class EventListenerCallbackT(typing.Protocol):
        def __call__(self, *args: _ListenerArg) -> typing.Any:
            ...
