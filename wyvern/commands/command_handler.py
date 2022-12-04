from __future__ import annotations

import inspect
import typing

if typing.TYPE_CHECKING:
    from wyvern.interactions.applications import ApplicationCommandInteraction
    from wyvern.models.messages import Message

    from .slash_commands import SlashCommand

__all__: tuple[str,...] = ("CommandHandler",)
class CommandHandler:
    """Command Handler for interacting with interaction and prefix commands.

    !!! note
        This class is purely created to be implemented with the GatewayClient subclass
        for the [wyvern.CommandsClient][] class.
    """

    prefix_getter: typing.Any = None
    prefix_type: type | None = None
    slash_commands: dict[str, SlashCommand]

    async def get_prefixes(self, message: Message) -> typing.Any:
        """Get's a list of prefix with respect to the message.

        Parameters
        ----------

        message : wyvern.Message
            The message to get prefixes for.

        Returns
        -------

        typing.Any
        """
        if self.prefix_type is str:
            return [self.prefix_getter]
        elif type(self.prefix_getter) in [set, list, tuple]:
            return self.prefix_getter
        else:
            if inspect.iscoroutinefunction(self.prefix_getter):
                return [prefix] if isinstance((prefix := await self.prefix_getter(self, message)), str) else prefix
            elif inspect.isfunction(self.prefix_getter):
                return [prefix] if isinstance((prefix := self.prefix_getter(self, message)), str) else prefix

    async def process_application_commands(self, interaction: ApplicationCommandInteraction) -> None:
        """Processes application command interactions for app commands.

        Parameters
        ----------

        interaction : wyvern.ApplicationCommandInteraction
            The interaction to process.
        """
        command = self.slash_commands.get(interaction.data.command_name)
        if command is not None:
            await command(
                interaction,
            )
