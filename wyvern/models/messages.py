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

import datetime
import typing

import attrs

from wyvern._internals import BitWiseFlag

from .base import DiscordObject, Snowflake

if typing.TYPE_CHECKING:
    from wyvern.clients import GatewayClient
    from wyvern.components.container import ActionRowContainer
    from wyvern.constructors.embeds import Embed, EmbedConstructor
    from wyvern.files import Attachment

    from .users import User

__all__: tuple[str, ...] = ("MessageReference", "MessageFlags", "Message", "AllowedMentions")


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


@attrs.define(kw_only=True, slots=True)
class AllowedMentions:
    """Represents an allowed mentions payload for discord."""

    roles: bool = False
    """Set to True if role mentions are allowed."""
    users: bool = False
    """Set to True if user mentions are allowed."""
    everyone: bool = False
    """Set to True if `@everyone` mentions are allowed."""
    replied_user: bool = False
    """Set to True if bot should ping message authors on replies."""

    def to_payload(self) -> dict[str, list[str] | bool]:
        payload: dict[str, list[str] | bool] = {"parse": [], "replied_user": self.replied_user}
        assert isinstance(payload["parse"], list)
        if self.roles is True:
            payload["parse"].append("roles")
        if self.users is True:
            payload["parse"].append("users")
        if self.everyone is True:
            payload["parse"].append("everyone")

        return payload


class MessageFlags(BitWiseFlag):
    CROSSPOSTED = 1 << 0
    IS_CROSSPOST = 1 << 1
    SUPPRESS_EMBEDS = 1 << 2
    SOURCE_MESSAGE_DELETED = 1 << 3
    URGENT = 1 << 4
    HAS_THREAD = 1 << 5
    EPHEMERAL = 1 << 6
    LOADING = 1 << 7
    FAILED_TO_MENTION_SOME_ROLES_IN_THREAD = 1 << 8


@attrs.define(kw_only=True, slots=True, repr=True, eq=True)
class Message(DiscordObject):
    """
    Represents a discord message.
    """

    client: "GatewayClient"

    raw: dict[str, typing.Any]
    id: Snowflake
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
    attachments: list[Attachment]
    """File attachments in this message."""

    async def respond(
        self,
        content: str | None = None,
        *,
        embed: "EmbedConstructor" | None = None,
        embeds: typing.Sequence["EmbedConstructor"] = (),
        components: typing.Sequence["ActionRowContainer"] = (),
        allowed_mentions: AllowedMentions | None = None,
        flags: MessageFlags | None = None,
        delete_after: int | None = None,
        reply: bool = False,
    ) -> "Message":
        """
        Parameters
        ----------

        content : str | None
            The text content of the message.
        embed : wyvern.constructors.embeds.EmbedConstructor
            An single embed object to send, for multiple use `embeds` kwarg instead.
        embeds : typing.Sequence[wyvern.constructors.embeds.EmbedConstructor]
            Sequence of embeds to send.
        components : typing.Sequence[wyvern.components.container.ActionRowContainer]
            Sequence of action rows to send.
        allowed_mentions : wyvern.models.messages.AllowedMentions | None
            Allowed mentions configs.
        reply : bool
            True if you the response should be created a reply.

        Returns
        -------

        wyvern.models.messages.Message
            The message object that got created.
        """

        if all([embed, embeds]):
            raise ValueError("You cannot use both embed and embeds kwarg.")
        embeds = [embed] if embed else embeds
        return await self.client.rest.create_message(
            self.channel_id,
            content,
            embeds=embeds,
            components=components,
            allowed_mentions=allowed_mentions,
            reference=self.id if reply is True else None,
            delete_after=delete_after,
            flags=flags,
        )
