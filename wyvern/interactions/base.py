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

import enum
import typing

import attrs

from wyvern._internals import _ListenerArg

if typing.TYPE_CHECKING:
    from wyvern import models
    from wyvern.clients import GatewayClient
    from wyvern.components import ActionRowContainer, Modal
    from wyvern.constructors.embeds import EmbedConstructor


__all__: tuple[str, ...] = (
    "Interaction",
    "InteractionCommandOptionType",
    "InteractionCommandType",
    "InteractionType",
    "InteractionResponseType",
)


@typing.final
class InteractionType(enum.IntEnum):
    """Type of the interaction."""

    PING = 1
    """A ping-pong interaction."""
    APPLICATION_COMMAND = 2
    """Interaction recieved on application command invocation"""
    MESSAGE_COMPONENT = 3
    """Interaction recieved when a message component is used."""
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    """Interaction for autocompletes."""
    MODAL_SUBMIT = 5
    """Interaction when a modal form is submitted."""


@typing.final
class InteractionResponseType(enum.IntEnum):
    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    DEFERRED_UPDATE_MESSAGE = 6
    UPDATE_MESSAGE = 7
    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8
    MODAL = 9


@typing.final
class InteractionCommandType(enum.IntEnum):
    CHAT_INPUT = 1
    USER = 2
    MESSAGE = 3


@typing.final
class InteractionCommandOptionType(enum.IntEnum):
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    NUMBER = 10
    ATTACHMENT = 11


@attrs.define(kw_only=True, slots=True, repr=True, init=True)
class Interaction(_ListenerArg):
    """Represents a discord interaction."""

    client: "GatewayClient"
    id: int
    """ID of the interaction."""
    application_id: models.base.Snowflake
    """ID of the application that recieved the interaction."""
    type: InteractionType
    """Type of the interaction."""
    data: typing.Any
    """Interaction data."""
    guild_id: int | None
    """ID of the guild where interaction was created."""
    channel_id: int | None
    """ID of channel where interaction was created."""
    user: models.users.User | None
    """User who invoked the interaction."""
    token: str
    """The interaction token."""
    version: int = 1
    message: "models.messages.Message" | None
    """The message related to this interaction."""
    guild_locale: str | None
    """Locale of the guild."""

    async def create_message_response(
        self,
        content: str | None = None,
        *,
        embed: "EmbedConstructor" | None = None,
        embeds: typing.Sequence["EmbedConstructor"] = (),
        components: typing.Sequence["ActionRowContainer"] = (),
        allowed_mentions: "models.AllowedMentions" | None = None,
    ) -> None:
        if all([embed, embeds]):
            raise ValueError("You cannot use both embed and embeds kwarg.")
        embeds = [embed] if embed else embeds
        await self.client.rest.create_interaction_response(
            self,
            InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            content=content,
            embeds=embeds,
            components=components,
            allowed_mentions=allowed_mentions,
        )

    async def create_defered_response(self) -> None:
        await self.client.rest.create_interaction_response(
            self,
            InteractionResponseType.DEFERRED_UPDATE_MESSAGE
            if self.type is InteractionType.MESSAGE_COMPONENT
            else InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE,
        )

    async def create_modal_response(self, modal: "Modal") -> None:
        await self.client.rest.create_interaction_response(self, InteractionResponseType.MODAL, modal=modal)
