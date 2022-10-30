from __future__ import annotations

import datetime
import typing

import attrs

from .base import DiscordObject

if typing.TYPE_CHECKING:
    from wyvern.client import GatewayClient
    from wyvern.constructors.embed import Embed, EmbedConstructor

    from .user import User


@attrs.define(kw_only=True, slots=True, repr=True)
class MessageReference:
    channel_id: int | None = None
    """ID of the channel."""
    message_id: int | None = None
    """ID of the message."""
    guild_id: int | None = None
    """ID of the guild, if any."""
    fail_if_not_exists: bool = True
    """Weather to raise error if message does not exist."""

    def to_payload(self) -> dict[str, int | bool | None]:
        """Converts the object to a sendable payload.

        Returns
        -------

        dict[str, int| bool]
        """
        return {
            "channel_id": self.channel_id,
            "message_id": self.message_id,
            "guild_id": self.guild_id,
            "fail_if_not_exists": self.fail_if_not_exists,
        }


@attrs.define(kw_only=True, slots=True, repr=True, eq=True)
class Message(DiscordObject):
    """
    Represents a discord message.
    """

    _client: "GatewayClient"
    id: int
    """ID of the message."""
    tts: bool
    """True if the message was a TTS message."""
    pinned: bool
    """Is the message is pinned."""
    mentions: list["User"]
    """List of users mentioned in the message."""
    mention_roles: list[int]
    """List of ids for roles mentioned in the message."""
    flags_value: int
    """Value of message flags"""
    embeds: list["Embed"]
    """List of embeds attached to the message."""
    edited_at: datetime.datetime | None
    """When was the message last edited."""
    content: str | None
    """The message content.
    Needs [wyvern.intents.Intents.MESSAGE_CONTENT] to be access this in a guild context."""
    channel_id: int
    """ID of the channel where this message was sent."""
    author: "User"
    """The message author."""
    message_reference: MessageReference | None
    """The message reference, if any."""
    attachments: list[typing.Any]
    """File attachments in this message."""

    async def reply(
        self,
        content: str | None = None,
        *,
        embed: "EmbedConstructor" | None = None,
        embeds: typing.Sequence["EmbedConstructor"] = (),
    ) -> "Message":
        if all([embed, embeds]):
            raise ValueError("You cannot use both embed and embeds kwarg.")
        embeds = [embed] if embed else embeds
        return await self._client.rest.create_message(self.channel_id, content, embeds=embeds, reference=self.id)
