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

if typing.TYPE_CHECKING:
    from wyvern import assets, models


__all__: tuple[str, ...] = (
    "ApplicationCommandInteraction",
    "ApplicationCommandInteractionData",
    "InteractionOption",
    "AutocompleteInteraction",
    "ApplicationCommandInteractionResolvedData",
)


@typing.final
@attrs.define(kw_only=True, slots=True)
class InteractionOption:
    """Represents a interaction option for slash commands. (From the api.)

    !!! note
        This class is not the same as [commands.slash_commands.CommandOption][] class.
    """

    name: str
    """Name of the option."""
    type: InteractionCommandOptionType
    """Type of the option."""
    value: int | str | None
    """Value of the option."""
    options: list["InteractionOption"]
    """List of options in the options, if any"""
    is_focused: bool
    """If the current option focused in an autocomplete interaction."""

    def __str__(self) -> str:
        return self.name


@typing.final
@attrs.define(kw_only=True, slots=True)
class ApplicationCommandInteractionResolvedData:
    """Resloved data of the app command interaction."""

    users: dict["models.base.Snowflake", "models.User"]
    members: dict["models.base.Snowflake", "models.Member"]
    messages: dict["models.base.Snowflake", "models.Message"]
    attachments: dict["models.base.Snowflake", "assets.Attachment"]


@typing.final
@attrs.define(kw_only=True, slots=True, repr=True)
class ApplicationCommandInteractionData:
    """Data related to an application command interaction."""

    payload: dict[str, typing.Any]
    """Raw payload recieved from discord."""
    type = InteractionType.APPLICATION_COMMAND
    """Type of the interaction."""
    command_id: int
    """ID of the command."""
    command_name: str
    """Name of the command."""
    command_type: InteractionCommandType
    """Type of the interaction command."""
    guild_id: int | None
    """ID of the guild where interaction was triggered"""
    target_id: int | None
    """ID of the application command target."""
    options: list[InteractionOption]
    """List of options used in the interaction."""
    resoloved: ApplicationCommandInteractionResolvedData | None
    """The resolved interaction data."""


class ApplicationCommandInteraction(Interaction):
    """Represents an application command interaction."""

    data: ApplicationCommandInteractionData


class AutocompleteInteraction(Interaction):
    """Represents an autocomplete interaction."""

    ...
