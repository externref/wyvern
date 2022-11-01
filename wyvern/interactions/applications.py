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

import attrs

from .base import Interaction, InteractionCommandOptionType, InteractionCommandType, InteractionType


__all__: tuple[str, ...] = ("ApplicationCommandInteraction", "ApplicationCommandInteractionData", "InteractionOption")


@typing.final
@attrs.define(kw_only=True, slots=True)
class InteractionOption:
    name: str
    type: InteractionCommandOptionType
    value: int | str | None
    options: list["InteractionOption"]
    is_focused: bool

    def __str__(self) -> str:
        return self.name


@typing.final
@attrs.define(kw_only=True, slots=True, repr=True)
class ApplicationCommandInteractionData:
    payload: dict[str, typing.Any]
    type = InteractionType.APPLICATION_COMMAND
    command_id: int
    command_name: str
    command_type: InteractionCommandType
    guild_id: int | None
    target_id: int | None
    options: list[InteractionOption]


class ApplicationCommandInteraction(Interaction):
    ...
