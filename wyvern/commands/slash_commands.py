from __future__ import annotations

import typing

import attrs

from wyvern import interactions, utils
from wyvern.interactions.base import InteractionCommandOptionType as OptionType

from .base import BaseCallable, CallbackT, HasAutoComplete, HasSubCommands, SlashOptionConverter

if typing.TYPE_CHECKING:
    from wyvern.clients import CommandsClient
    from wyvern.interactions.applications import ApplicationCommandInteraction
    from wyvern.models.channels import ChannelType

__all__: tuple[str, ...] = ("CommandChoice", "OptionType", "as_slash_command", "as_option")


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
    value: str | int | None = None


@attrs.define(kw_only=True)
class CommandOption:
    """Represents a slash command option. (In the constructor)"""

    name: str
    """Name of the option."""
    description: str
    """Description of the option."""
    default: typing.Any = utils.EMPTY
    """Default value for the option"""
    type: OptionType
    """Type of the option."""
    converter: SlashOptionConverter | None = None
    """A custom converter for the option, if any."""
    autocomplete: bool = False
    """Weather to enable autocomplete for this option or not."""
    choices: list[CommandChoice | str] = []
    """List of choices to add to the option."""
    channel_types: list["ChannelType"] = []
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
                (
                    {"name": choice.name, "value": choice.value or choice.name}
                    if isinstance(choice, CommandChoice)
                    else {"name": choice, "value": choice}
                )
                for choice in self.choices
            ],
            "channel_types": self.channel_types,
            "min_value": self.min_value,
            "min_length": self.min_length,
            "max_length": self.max_length,
            "min_value": self.min_value,
            "max_value": self.max_value,
        }


@attrs.define(kw_only=True, slots=True, repr=True)
class SlashCommand(BaseCallable, HasAutoComplete):
    """Represents a slash command constructor."""

    name: str
    """Name of the command."""
    description: str
    """Description of the command."""
    options: list[CommandOption] = []
    """List of command options."""
    _client: "CommandsClient" | None = None

    def __str__(self) -> str:
        return self.name

    async def __call__(self, inter: "ApplicationCommandInteraction", **kwargs: typing.Any) -> typing.Any:
        await self.callback(inter, **kwargs)

    def _set_client(self, client: "CommandsClient") -> "SlashCommand":
        self._client = client
        return self

    async def with_autocomplete(
        self, opt_name: str | None = None, *, opt_names: typing.Sequence[str] = ()
    ) -> typing.Callable[..., typing.Callable[..., typing.Awaitable[typing.Sequence["CommandChoice" | str]]]]:
        """Interface for creating autocomplete callabcks.

        Parameters
        ----------

        opt_name : str
            Name of the option this autocomplete is for.
        opt_names : typing.Sequence[str]
            Sequence of options this autocomplete is for.

        !!! note
            opt_names overrides opt_name

        Example
        -------

            from __future__ import annotations

            import wyvern
            from wyvern import commands

            client = wyvern.CommandsClient("TOKEN")


            @commands.as_option(
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
                return [color for color in colors if color.name == inter.data.value]


            client.run()



        """
        return await super().with_autocomplete(opt_name, opt_names=opt_names)

    async def create_command(self) -> SlashCommand:
        """Creates the command on discord ( if already doesnt exist ).

        Returns
        -------

        wyvern.commands.SlashCommand
            This same object
        """
        assert self._client
        await self._client.rest.create_application_command(
            name=self.name,
            description=self.description,
            options=self.options,
            type=interactions.base.InteractionCommandType.CHAT_INPUT,
        )
        return self


@attrs.define
class SlashSubCommand(BaseCallable, HasAutoComplete):
    name: str
    description: str
    callback: typing.Any

    async def __call__(self, inter: "ApplicationCommandInteraction", **kwargs: typing.Any) -> typing.Any:
        await self.callback(inter, **kwargs)


class SlashSubGroup(HasSubCommands):
    name: str
    description: str

    def __init__(self, *, name: str, description: str) -> None:
        self.name = name
        self.description = description
        super().__init__()


class SlashGroup(HasSubCommands):
    name: str
    description: str
    guild_ids: list[int]
    subcommands: dict[str, SlashSubCommand] = {}
    subgroups: dict[str, SlashSubGroup] = {}
    _client: "CommandsClient" | None = None

    def __init__(self, *, name: str, description: str, guild_ids: typing.Sequence[int] = ()) -> None:
        self.name = name
        self.description = description
        self.guild_ids = list(guild_ids)
        super().__init__()

    def _set_client(self, client: "CommandsClient") -> "SlashGroup":
        self._client = client
        return self

    def with_subgroup(self, *, name: str, description: str) -> SlashSubGroup:
        self.subgroups[name] = (group := SlashSubGroup(name=name, description=description))
        return group

    async def with_subcommand(self, name: str, description: str) -> typing.Callable[..., SlashSubCommand]:
        def inner(callback: CallbackT) -> SlashSubCommand:
            nonlocal name, description
            self.subcommands[name] = (cmd := SlashSubCommand(name=name, description=description, callback=callback))
            return cmd

        return inner


def as_slash_command(*, name: str, description: str) -> typing.Callable[[CallbackT], SlashCommand]:
    """Creates a slash command object.

    Parameters
    ----------

    name : str
        Name of the command.
    description : str
        Description of the command.

    Returns
    -------

    typing.Callable[[CallbackT], SlashCommand]

        A [SlashCommand][] when called.


    """

    def inner(callback: CallbackT) -> SlashCommand:
        return SlashCommand(name=name, description=description, callback=callback)

    return inner


def as_option(
    *,
    name: str,
    description: str,
    type: OptionType = OptionType.STRING,
    default: typing.Any = utils.EMPTY,
    converter: SlashOptionConverter | None = None,
    autocomplete: bool = False,
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
            )
        )
        return command

    return inner
