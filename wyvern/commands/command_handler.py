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

import inspect
import typing

if typing.TYPE_CHECKING:
    from wyvern.interactions.applications import ApplicationCommandInteraction
    from wyvern.models.messages import Message

    from .slash_commands import SlashCommand

__all__: tuple[str, ...] = ("CommandHandler",)


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
