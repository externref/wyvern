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

"""Slash commands support."""

from __future__ import annotations

import typing

import attrs

from wyvern import interactions, utils
from wyvern.interactions.base import InteractionCommandOptionType as OptionType

from .base import BaseCallable, HasAutoComplete, HasSubCommands, SlashOptionConverter

if typing.TYPE_CHECKING:
    from wyvern._types import AppCommandCallbackT
    from wyvern.clients import CommandsClient
    from wyvern.interactions import ApplicationCommandInteraction, Localizations
    from wyvern.models.channels import ChannelType

__all__: tuple[str, ...] = (
    "CommandChoice",
    "OptionType",
    "as_slash_command",
    "with_option",
    "SlashCommand",
    "SlashGroup",
)


@attrs.define(kw_only=True)
class CommandChoice:
    """Represents a slash command choice.

    Parameters
    ----------

    name : str
        Name to show on discord.
    value : str | int
        Value of the choice.

    """

    name: str
    value: str | int
    name_locales: dict[str, Localizations] | utils.Empty = utils.EMPTY

    def to_payload(self) -> dict[str, str | int | dict[str, dict[str, str]]]:
        return {
            "name": self.name,
            "value": self.value or self.name,
            "name_localizations": {name: local.final_data for name, local in _locale.items()}
            if not isinstance((_locale := self.name_locales), utils.Empty)
            else {},
        }


@attrs.define(kw_only=True)
class CommandOption:
    """Represents a slash command option. (In the constructor)"""

    name: str
    """Name of the option."""
    name_locales: Localizations | utils.Empty = utils.EMPTY
    """Name locales for the option."""
    description: str
    """Description of the option."""
    description_locales: Localizations | utils.Empty = utils.EMPTY
    """Description locales for the option."""
    default: typing.Any = utils.EMPTY
    """Default value for the option"""
    type: OptionType
    """Type of the option."""
    converter: SlashOptionConverter | None = None
    """A custom converter for the option, if any."""
    autocomplete: bool = False
    """Weather to enable autocomplete for this option or not."""
    choices: list[CommandChoice | str | int] = []
    """List of choices to add to the option."""
    channel_types: list[ChannelType] = []
    """List of channel types for channel options."""
    min_value: int | None = None
    """Minimum value for the option"""
    max_value: int | None = None
    """Maximum value for the option"""
    min_length: int | None = None
    """Minimum length acceptable for the option"""
    max_length: int | None = None
    """Maximum length acceptable for the option"""

    def to_payload(self) -> dict[str, typing.Any]:
        return {
            "name": self.name,
            "description": self.description,
            "required": False if self.default is utils.EMPTY else True,
            "type": self.type,
            "autocomplete": self.autocomplete,
            "choices": [
                (choice.to_payload() if isinstance(choice, CommandChoice) else {"name": choice, "value": choice})
                for choice in self.choices
            ],
            "channel_types": self.channel_types,
            "min_value": self.min_value,
            "min_length": self.min_length,
            "max_length": self.max_length,
            "max_value": self.max_value,
            "name_localizations": _locale.final_data
            if not isinstance((_locale := self.name_locales), utils.Empty)
            else {},
            "description_localizations": _locale.final_data
            if not isinstance((_locale := self.description_locales), utils.Empty)
            else {},
        }


@attrs.define(kw_only=True, slots=True, repr=True)
class SlashCommand(BaseCallable, HasAutoComplete):
    """Represents a slash command constructor."""

    name: str
    """Name of the command."""
    description: str
    """Description of the command."""
    options: list[CommandOption] = attrs.field(init=False, default=[])
    """List of command options."""
    guild_only: bool = False
    """Set to True for command to appear in guilds only."""
    client: CommandsClient | None = attrs.field(init=False, default=None)
    callback: AppCommandCallbackT
    guild_ids: list[int] = []
    """"""

    def __str__(self) -> str:
        return self.name

    async def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        await self.callback(*args, **kwargs)

    def _set_client(self, client: CommandsClient) -> "SlashCommand":
        self.client = client
        return self

    def to_payload(self) -> dict[str, typing.Any]:
        return {
            "name": self.name,
            "description": self.description,
            "options": [option.to_payload() for option in self.options],
            "dm_permissions": not self.guild_only,
            "type": interactions.base.InteractionCommandType.MESSAGE,
        }

    async def with_autocomplete(
        self, opt_name: str | None = None, *, opt_names: typing.Sequence[str] = ()
    ) -> typing.Callable[..., typing.Callable[..., typing.Awaitable[typing.Sequence[CommandChoice | str]]]]:
        """Interface for creating autocomplete callabcks.

        Parameters
        ----------

        opt_name : str
            Name of the option this autocomplete is for.
        opt_names : typing.Sequence[str]
            Sequence of options this autocomplete is for.

        !!! note
            opt_names overrides opt_name

        ??? example
            ```py

            from __future__ import annotations

            import wyvern
            from wyvern import commands

            client = wyvern.CommandsClient("TOKEN")


            @commands.with_option(
                name="color", description="name of color to show hex of.", type=commands.OptionType.INTEGER, autocomplete=True
            )
            @client.slash_command(name="color_hex", description="gives you color hexs")
            async def colors(inter: wyvern.ApplicationCommandInteraction, color: int) -> None:
                await inter.create_message_response(f"Hex for the color was {hex}")


            @colors.with_autocomplete(opt_name="color")
            async def autocomplete_inter(
                inter: wyvern.AutocompleteInteraction, option: wyvern.InteractionOption
            ) -> list[commands.CommandChoice]:
                colors = [commands.CommandChoice(name="blue", value=0x4F62A3), commands.CommandChoice(name="red", value=0xD11417)]
                return [color for color in colors if color.name in inter.data.value]


            client.run()

            ```

        """  # noqa: E501
        return await super().with_autocomplete(opt_name, opt_names=opt_names)

    async def create_command(self) -> SlashCommand:
        """Creates the command on discord ( if already doesnt exist ).

        Returns
        -------

        wyvern.commands.SlashCommand
            This same object
        """
        assert self.client
        await self.client.rest._create_app_command_from_payload(payload=self.to_payload())
        return self


@attrs.define(kw_only=True)
class SlashSubCommand(BaseCallable, HasAutoComplete):
    name: str
    description: str
    callback: AppCommandCallbackT

    options: list[CommandOption] = attrs.field(init=False, default=[])

    async def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        await self.callback(*args, **kwargs)

    def to_payload(self) -> dict[str, typing.Any]:
        return {
            "name": self.name,
            "description": self.description,
            "options": [option.to_payload() for option in self.options],
        }


@attrs.define(kw_only=True)
class SlashSubGroupCommand:
    name: str
    description: str
    callback: AppCommandCallbackT

    options: list[CommandOption] = attrs.field(init=False, default=[])

    async def __call__(self, inter: ApplicationCommandInteraction, **kwargs: typing.Any) -> typing.Any:
        await self.callback(inter, **kwargs)

    def to_payload(self) -> dict[str, typing.Any]:
        return {
            "name": self.name,
            "description": self.description,
            "options": [option.to_payload() for option in self.options],
        }


@attrs.define(kw_only=True)
class SlashSubGroup(HasSubCommands):
    name: str
    description: str
    subcommands: dict[str, SlashSubGroupCommand] = attrs.field(init=False, default={})

    def to_payload(self) -> dict[str, typing.Any]:
        return {
            "type": OptionType.SUB_COMMAND_GROUP,
            "name": self.name,
            "description": self.description,
            "options": [opt.to_payload() for opt in self.subcommands.values()],
        }

    def with_subcommand(
        self, *, name: str, description: str
    ) -> typing.Callable[[AppCommandCallbackT], SlashSubGroupCommand]:
        def inner(callback: AppCommandCallbackT) -> SlashSubGroupCommand:
            self.subcommands[name] = (
                subcmd := SlashSubGroupCommand(name=name, description=description, callback=callback)
            )
            return subcmd

        return inner


@attrs.define(kw_only=True)
class SlashGroup(HasSubCommands):
    name: str
    description: str
    guild_ids: list[int]
    guild_only: bool = False
    subcommands: dict[str, SlashSubCommand] = attrs.field(init=False, default={})
    subgroups: dict[str, SlashSubGroup] = attrs.field(init=False, default={})
    client: "CommandsClient" | None = attrs.field(init=False, default=None)

    def _set_client(self, client: "CommandsClient") -> "SlashGroup":
        self._client = client
        return self

    def to_payload(self) -> dict[str, typing.Any]:
        return {
            "name": self.name,
            "description": self.description,
            "options": self._options,
            "dm_permissions": not self.guild_only,
            "type": interactions.base.InteractionCommandType.MESSAGE,
        }

    @property
    def _options(self) -> list[dict[str, typing.Any]]:
        opts = list(self.subcommands.values()) + list(self.subgroups.values())
        return [opt.to_payload() for opt in opts]

    def with_subgroup(self, *, name: str, description: str) -> SlashSubGroup:
        self.subgroups[name] = (group := SlashSubGroup(name=name, description=description))
        return group

    def with_subcommand(
        self, *, name: str, description: str
    ) -> typing.Callable[[AppCommandCallbackT], SlashSubCommand]:
        def inner(callback: AppCommandCallbackT) -> SlashSubCommand:
            nonlocal name, description
            self.subcommands[name] = (cmd := SlashSubCommand(name=name, description=description, callback=callback))
            return cmd

        return inner


def as_slash_command(
    *,
    name: str,
    description: str,
    guild_ids: typing.Sequence[int] = (),
    guild_only: bool = False,
) -> typing.Callable[[AppCommandCallbackT], SlashCommand]:
    """Creates a slash command object.

    Parameters
    ----------

    name : str
        Name of the command.
    description : str
        Description of the command.

    Returns
    -------

    typing.Callable[[AppCommandCallbackT], SlashCommand]

        A [SlashCommand][] when called.


    """

    def inner(callback: AppCommandCallbackT) -> SlashCommand:
        return SlashCommand(
            name=name, description=description, callback=callback, guild_ids=list(guild_ids), guild_only=guild_only
        )

    return inner


def as_slash_group(
    *, name: str, description: str, guild_ids: typing.Sequence[int] = (), guild_only: bool = False
) -> SlashGroup:
    return SlashGroup(name=name, description=description, guild_ids=list(guild_ids), guild_only=guild_only)


def as_option(
    *,
    name: str,
    description: str,
    type: OptionType = OptionType.STRING,
    default: typing.Any = utils.EMPTY,
    converter: SlashOptionConverter | None = None,
    autocomplete: bool = False,
    choices: typing.Sequence[CommandChoice | str | int] = [],
    channel_types: typing.Sequence["ChannelType"] = [],
    min_value: int | None = None,
    max_value: int | None = None,
    min_length: int | None = None,
    max_length: int | None = None,
    name_locales: Localizations | utils.Empty = utils.EMPTY,
    description_locales: Localizations | utils.Empty = utils.EMPTY,
) -> CommandOption:
    return CommandOption(
        name=name,
        description=description,
        default=default,
        type=type,
        converter=converter,
        autocomplete=autocomplete,
        choices=list(choices),
        channel_types=list(channel_types),
        min_length=min_length,
        min_value=min_value,
        max_length=max_length,
        max_value=max_value,
        name_locales=name_locales,
        description_locales=description_locales,
    )


def with_option(
    *,
    name: str,
    description: str,
    type: OptionType = OptionType.STRING,
    default: typing.Any = utils.EMPTY,
    converter: SlashOptionConverter | None = None,
    autocomplete: bool = False,
    choices: typing.Sequence[CommandChoice | str | int] = [],
    channel_types: typing.Sequence["ChannelType"] = [],
    min_value: int | None = None,
    max_value: int | None = None,
    min_length: int | None = None,
    max_length: int | None = None,
    name_locales: Localizations | utils.Empty = utils.EMPTY,
    description_locales: Localizations | utils.Empty = utils.EMPTY,
) -> typing.Callable[[SlashCommand], SlashCommand]:
    """Adds an option to a slash command.

    Parameters
    ----------

    name : str
        Name of the option.
    description : str
        Description of the option.
    type : OptionType
        Type of the option.
    default : typing.Any
        Default value for the option.
    convertor : SlashOptionConvertor | None
        A custom convertor if any.
    autcomplete : bool
        Is autcomplete enabled for this option ( defaults to False )

    Returns
    -------

    typing.Callable[[SlashCommand], SlashCommand]

        The command this option was added to.
    """

    def inner(command: SlashCommand) -> SlashCommand:
        command.options.append(
            CommandOption(
                name=name,
                description=description,
                default=default,
                type=type,
                converter=converter,
                autocomplete=autocomplete,
                choices=list(choices),
                channel_types=list(channel_types),
                min_length=min_length,
                min_value=min_value,
                max_length=max_length,
                max_value=max_value,
                name_locales=name_locales,
                description_locales=description_locales,
            )
        )
        return command

    return inner
