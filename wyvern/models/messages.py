from __future__ import annotations

import datetime
import typing

import attrs

from .base import DiscordObject

if typing.TYPE_CHECKING:
    from wyvern.clients import GatewayClient
    from wyvern.components.container import ActionRowContainer
    from wyvern.constructors.embeds import Embed, EmbedConstructor

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


class MessageFlags:
    CROSSPOSTED = 1 << 0
    IS_CROSSPOST = 1 << 1
    SUPPRESS_EMBEDS = 1 << 2
    SOURCE_MESSAGE_DELETED = 1 << 3
    URGENT = 1 << 4
    HAS_THREAD = 1 << 5
    EPHEMERAL = 1 << 6
    LOADING = 1 << 7
    FAILED_TO_MENTION_SOME_ROLES_IN_THREAD = 1 << 8
    value: int

    def __init__(self, value: int) -> None:
        self.value = value
        super().__init__()


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

    async def respond(
        self,
        content: str | None = None,
        *,
        embed: "EmbedConstructor" | None = None,
        embeds: typing.Sequence["EmbedConstructor"] = (),
        components: typing.Sequence["ActionRowContainer"] = (),
        allowed_mentions: AllowedMentions | None = None,
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
        return await self._client.rest.create_message(
            self.channel_id,
            content,
            embeds=embeds,
            components=components,
            allowed_mentions=allowed_mentions,
            reference=self.id if reply is True else None,
        )
