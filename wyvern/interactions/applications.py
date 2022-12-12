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

from wyvern import files

from .base import Interaction, InteractionCommandOptionType, InteractionCommandType, InteractionType

if typing.TYPE_CHECKING:
    from wyvern import models
    from wyvern.commands.slash_commands import CommandOption
    from wyvern.permissions import Permissions

    from .localizations import Localizations


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
    options: list[InteractionOption]
    """List of options in the options, if any."""
    required: bool = True
    """True if the option is required."""
    is_focused: bool
    """If the current option focused in an autocomplete interaction."""
    autocomplete: bool = False
    """Weather to enable autocomplete for this option or not."""
    choices: list[CommandOption] = []
    """List of choices to add to the option."""
    channel_types: list[models.ChannelType] = []
    """List of channel types for channel options."""
    min_value: int | None = None
    """Minimum value for the option"""
    max_value: int | None = None
    """Maximum value for the option"""
    min_length: int | None = None
    """Minimum length acceptable for the option"""
    max_length: int | None = None
    """Maximum length acceptable for the option"""
    name_locales: Localizations | None = None
    """Name locales for the option description"""
    description_locales: Localizations | None = None
    """Name locales for the option description"""

    def __str__(self) -> str:
        return self.name


@typing.final
@attrs.define(kw_only=True, slots=True)
class ApplicationCommandInteractionResolvedData:
    """Resloved data of the app command interaction."""

    users: dict[models.base.Snowflake, models.User]
    members: dict[models.base.Snowflake, models.Member]
    messages: dict[models.base.Snowflake, models.Message]
    attachments: dict[models.base.Snowflake, files.Attachment]
    channels: dict[models.base.Snowflake, models.ChannelLike]


@typing.final
@attrs.define(kw_only=True, slots=True, repr=True)
class ApplicationCommandInteractionData:
    """Data related to an application command interaction."""

    payload: dict[str, typing.Any]
    """Raw payload recieved from discord."""
    type = InteractionType.APPLICATION_COMMAND
    """Type of the interaction."""
    command_id: models.base.Snowflake
    """ID of the command."""
    command_name: str
    """Name of the command."""
    command_type: InteractionCommandType
    """Type of the interaction command."""
    guild_id: models.base.Snowflake | None
    """ID of the guild where interaction was triggered"""
    target_id: models.base.Snowflake | None
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


@attrs.define(kw_only=True)
class APIApplicationCommand:
    id: models.base.Snowflake
    type: InteractionCommandType = InteractionCommandType.MESSAGE
    application_id: models.base.Snowflake
    guild_id: models.base.Snowflake | None = None
    name: str
    name_locales: Localizations | None = None
    description: str
    description_locales: Localizations | None = None
    options: InteractionOption
    default_member_permissions: Permissions | None = None
    dm_permissions: bool = False
    version: models.base.Snowflake
