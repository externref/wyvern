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

from .base import DiscordObject

if typing.TYPE_CHECKING:
    from wyvern.clients import GatewayClient
    from wyvern.components.container import ActionRowContainer
    from wyvern.constructors.embeds import EmbedConstructor

    from .messages import AllowedMentions, Message, MessageFlags, MessageReference


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


@attrs.define(kw_only=True)
class ChannelLike(DiscordObject):
    client: GatewayClient
    raw: dict[str, typing.Any]
    type: ChannelType


class ImplementsMessages(ChannelLike):
    async def fetch_message(self, message_id: int) -> Message:
        return await self.client.rest.fetch_message(self.id, message_id)

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


@attrs.define(kw_only=True)
class GuildChannel(ChannelLike):
    guild_id: int


@attrs.define(kw_only=True)
class DMChannel(ImplementsMessages):
    type: ChannelType = attrs.field(init=False, default=ChannelType.DM)


@attrs.define(kw_only=True)
class GuildTextChannel(ImplementsMessages):
    type: ChannelType = attrs.field(init=False, default=ChannelType.GUILD_TEXT)


@attrs.define(kw_only=True)
class GuildVoiceChannel(ChannelLike):
    type: ChannelType = attrs.field(init=False, default=ChannelType.GUILD_VOICE)


@attrs.define(kw_only=True)
class GuildCategoryChannel(ChannelLike):
    type: ChannelType = attrs.field(init=False, default=ChannelType.GUILD_CATEGORY)
