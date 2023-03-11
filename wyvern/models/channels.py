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

import abc
import datetime
import enum
import typing

import attrs

from .base import DiscordObject, Snowflake

if typing.TYPE_CHECKING:
    from wyvern.clients import GatewayClient
    from wyvern.components.container import ActionRowContainer
    from wyvern.constructors.embeds import EmbedConstructor
    from wyvern.permissions import PermissionOverwrites

    from .messages import AllowedMentions, Message, MessageFlags, MessageReference
    from .users import User


class ChannelType(enum.IntFlag):
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_ANNOUNCEMENT = 5
    ANNOUNCEMENT_THREAD = 10
    PUBLIC_THREAD = 11
    PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13
    GUILD_DIRECTORY = 14
    GUILD_FORUM = 15


@attrs.define(kw_only=True, slots=True, repr=True)
class ChannelLike(DiscordObject):
    client: GatewayClient
    id: Snowflake
    """ID of the channel-like object."""
    raw: dict[str, typing.Any]
    """The raw payload for this channel."""
    type: ChannelType
    """Type of the channel."""


class ImplementsMessages(abc.ABC):
    id: Snowflake
    client: GatewayClient
    last_message_id: Snowflake | None

    async def fetch_message(self, message_id: int, /) -> Message:
        return await self.client.rest.fetch_message(self.id, message_id)

    async def delete_message(self, message_id: int, /) -> None:
        return await self.client.rest.delete_message(self.id, message_id)

    async def send(
        self,
        content: str | None = None,
        *,
        embed: EmbedConstructor | None = None,
        embeds: typing.Sequence["EmbedConstructor"] = (),
        components: typing.Sequence[ActionRowContainer] = (),
        reference: int | MessageReference | None = None,
        allowed_mentions: AllowedMentions | None = None,
        flags: MessageFlags | None = None,
        delete_after: int | None = None,
    ) -> Message:
        if embed:
            embeds = [embed]

        return await self.client.rest.create_message(
            self.id,
            content,
            embeds=embeds,
            components=components,
            reference=reference,
            allowed_mentions=allowed_mentions,
            delete_after=delete_after,
            flags=flags,
        )


class ImplementsVoice(abc.ABC):
    id: Snowflake
    guild_id: Snowflake
    client: GatewayClient

    async def connect(self, self_deaf: bool = False, self_mute: bool = False) -> None:
        await self.client.gateway.update_voice_state(self.guild_id, self.id, self_mute=self_mute, self_deaf=self_deaf)


@attrs.define(kw_only=True, slots=True, repr=True)
class GuildChannel(ChannelLike):
    name: str
    """Name of the channel."""
    guild_id: Snowflake
    """ID of the guild this channel belongs to."""
    position: int
    """Position of the channel."""
    permissions_overwrites: list[PermissionOverwrites]
    """List of Permission overwrites in this channel."""


@attrs.define(kw_only=True, slots=True, repr=True)
class DMChannel(ImplementsMessages, ChannelLike):
    type: ChannelType = attrs.field(init=False, default=ChannelType.DM)
    last_message_id: Snowflake | None
    """ID of the last message sent in the channel."""
    recipients: list[User]

    @property
    def user(self) -> User | None:
        return self.recipients[0] if self.recipients else None


@attrs.define(kw_only=True, slots=True, repr=True)
class GuildTextChannel(ImplementsMessages, GuildChannel):
    type: ChannelType = attrs.field(init=False, default=ChannelType.GUILD_TEXT)
    rate_limit_per_user: int
    """The cooldown in the channel per-user."""
    nsfw: bool
    """True if this channel is NSFW marked."""
    topic: str
    """Topic of the channel."""
    last_message_id: Snowflake | None
    """ID of the last message sent in the channel."""
    parent_id: Snowflake | None
    """ID of the category channel this channel belongs to. """
    default_auto_archive_duration: int
    """Time after which threads get archived by default."""


@attrs.define(kw_only=True, slots=True, repr=True)
class GuildVoiceChannel(GuildChannel, ImplementsMessages, ImplementsVoice):
    type: ChannelType = attrs.field(init=False, default=ChannelType.GUILD_VOICE)

    parent_id: Snowflake | None
    """ID of the category channel this channel belongs to. """
    bitrate: int
    """Bitrate for the channel."""
    user_limit: int
    """Max number of users allowed in the channel."""
    rtc_region: str | None
    """The rtc region."""
    rate_limit_per_user: int
    """The cooldown in the channel per-user."""
    nsfw: bool
    """True if the channel is marked NSFW"""


@attrs.define(kw_only=True, slots=True, repr=True)
class GuildCategoryChannel(GuildChannel):
    type: ChannelType = attrs.field(init=False, default=ChannelType.GUILD_CATEGORY)


@attrs.define(kw_only=True, slots=True, repr=True)
class GuildAnnouncmentChannel(GuildChannel, ImplementsMessages):
    type: ChannelType = attrs.field(init=False, default=ChannelType.GUILD_ANNOUNCEMENT)
    nsfw: bool
    """True if the channel is NSFW marked."""
    topic: str
    """Topic of the channel."""
    last_message_id: Snowflake | None
    """ID of the last message sent in the channel."""
    parent_id: Snowflake | None
    """ID of the category channel this channel belongs to. """
    default_auto_archive_duration: int
    """Time after which threads get archived by default."""


@attrs.define(kw_only=True, slots=True, repr=True)
class ThreadMetaData:
    archived: bool
    auto_archive_duration: int
    archive_timestamp: datetime.datetime | None
    locked: bool


@attrs.define(kw_only=True, slots=True, repr=True)
class ThreadChannel(GuildChannel, ImplementsMessages):
    type: ChannelType
    parent_id: Snowflake
    """ID of the parent channel."""
    owner_id: Snowflake
    """ID of the thread creator."""
    last_message_id: Snowflake | None
    """ID of last message created in the channel."""
    message_count: int
    """Number of messages in the thread."""
    member_count: int
    rate_limit_per_user: int
    total_message_sent: int

    @property
    def is_private(self) -> bool:
        return True if self.type is ChannelType.PRIVATE_THREAD else False


@attrs.define(kw_only=True, slots=True, repr=True)
class ThreadAnnouncementChannel(ThreadChannel):
    type: ChannelType = attrs.field(init=False, default=ChannelType.ANNOUNCEMENT_THREAD)


@attrs.define(kw_only=True, slots=True, repr=True)
class GuildStageVoiceChannel(GuildChannel, ImplementsVoice):
    type: ChannelType = attrs.field(init=False, default=ChannelType.GUILD_STAGE_VOICE)
    nsfw: bool


class GuildDirectoryChannel:  # not implemented by discord yet.
    ...


@attrs.define(kw_only=True, slots=True, repr=True)
class GuildForumChannel(GuildChannel):
    type: ChannelType = attrs.field(init=False, default=ChannelType.GUILD_FORUM)
