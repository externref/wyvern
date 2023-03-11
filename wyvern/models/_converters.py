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

from wyvern.files import Attachment
from wyvern.permissions import PermissionOverwrites

from . import channels
from .base import Snowflake
from .members import Member
from .messages import Message, MessageReference
from .users import BotUser, User

if typing.TYPE_CHECKING:
    from wyvern.clients import GatewayClient


__all__: tuple[str, ...] = ("payload_to_user", "payload_to_member", "payload_to_botuser", "payload_to_message")


def payload_to_user(client: "GatewayClient", payload: dict[str, typing.Any]) -> "User":
    return User(
        client=client,
        raw=payload,
        id=Snowflake.create(payload["id"]),
        username=payload["username"],
        discriminator=payload["discriminator"],
        avatar_hash=payload.get("avatar"),
        is_bot=payload.get("bot", False),
        is_system=payload.get("system", False),
        is_mfa_enabled=payload.get("mfa_enabled", False),
        banner_hash=payload.get("banner"),
        accent_color=payload.get("accent_color"),
        locale=payload.get("locale"),
        flags_value=payload.get("flags"),
        premium_type_value=payload.get("premium_type"),
        public_flags_value=payload.get("public_flags"),
    )


def payload_to_member(client: "GatewayClient", guild_id: Snowflake, payload: dict[str, typing.Any]) -> Member:
    user = payload_to_user(client, payload=payload["user"])
    return Member(
        client=client,
        raw=payload,
        user=user,
        id=user.id,
        username=user.username,
        discriminator=user.discriminator,
        avatar_hash=user.avatar_hash,
        is_bot=user.is_bot,
        is_system=user.is_system,
        is_mfa_enabled=user.is_mfa_enabled,
        banner_hash=user.banner_hash,
        accent_color=user.accent_color,
        locale=user.locale,
        flags_value=user.flags_value,
        premium_type_value=user.premium_type_value,
        public_flags_value=user.public_flags_value,
        guild_id=guild_id,
        nickname=payload.get("nick"),
        premium_since=datetime.datetime.fromisoformat(p) if (p := payload.get("premium_since")) else None,
        role_ids=[Snowflake.create(id) for id in payload["roles"]],
        joined_at=datetime.datetime.fromisoformat(payload["joined_at"]),
        deaf=payload.get("deaf"),
        mute=payload.get("mute"),
        communication_disabled_until=datetime.datetime.fromisoformat(cdu)
        if (cdu := payload.get("communication_disabled_until"))
        else None,
        pending=payload.get("pending", None),
        guild_avatar_hash=payload.get("avatar"),
    )


def payload_to_botuser(client: "GatewayClient", payload: dict[str, typing.Any]) -> BotUser:
    return BotUser(
        client=client,
        raw=payload,
        id=Snowflake.create(payload["id"]),
        username=payload["username"],
        discriminator=payload["discriminator"],
        avatar_hash=payload.get("avatar"),
        is_bot=payload.get("bot", False),
        is_system=payload.get("system", False),
        is_mfa_enabled=payload.get("mfa_enabled", False),
        banner_hash=payload.get("banner"),
        accent_color=payload.get("accent_color"),
        locale=payload.get("locale"),
        flags_value=payload.get("flags"),
        premium_type_value=payload.get("premium_type"),
        public_flags_value=payload.get("public_flags"),
    )


def payload_to_message(client: "GatewayClient", payload: dict[str, typing.Any]) -> Message:
    return Message(
        client=client,
        raw=payload,
        id=Snowflake.create(payload["id"]),
        tts=payload["tts"],
        pinned=payload["pinned"],
        mentions=[payload_to_user(client, item) for item in payload["mentions"]],
        mention_roles=payload["mention_roles"],
        flags_value=payload["flags"],
        embeds=[],
        edited_at=datetime.datetime.fromisoformat(t) if (t := payload.get("edited_timestamp")) else None,
        content=payload["content"],
        channel_id=payload["channel_id"],
        author=payload_to_user(client, payload["author"]),
        attachments=[Attachment._from_payload(client, Snowflake, attc) for attc in payload["attachments"]],
        message_reference=MessageReference(**data) if (data := payload.get("message_reference")) else None,
    )


def payload_to_channel(client: GatewayClient, payload: dict[str, typing.Any]) -> channels.ChannelLike:
    channel: channels.ChannelLike
    if payload["type"] == channels.ChannelType.GUILD_TEXT.value:
        channel = channels.GuildTextChannel(
            client=client,
            raw=payload,
            id=Snowflake.create(payload["id"]),
            name=payload["name"],
            guild_id=Snowflake.create(payload["guild_id"]),
            position=payload["position"],
            permissions_overwrites=[PermissionOverwrites(**perm) for perm in payload.get("permission_overwrites", [])],
            rate_limit_per_user=payload["rate_limit_per_user"],
            nsfw=payload.get("nsfw", False),
            topic=payload.get("topic", None),
            last_message_id=Snowflake.create(id) if (id := payload.get("last_message_id")) else None,
            parent_id=Snowflake.create(id) if (id := payload.get("parent_id")) else None,
            default_auto_archive_duration=payload["default_auto_archive_duration"],
        )
    elif payload["type"] == channels.ChannelType.GUILD_VOICE.value:
        channel = channels.GuildVoiceChannel(
            client=client,
            raw=payload,
            id=Snowflake.create(payload["id"]),
            name=payload["name"],
            guild_id=Snowflake.create("guild_id"),
            position=payload["position"],
            permissions_overwrites=[PermissionOverwrites(**perm) for perm in payload.get("permission_overwrites", [])],
            nsfw=payload.get("nsfw", False),
            parent_id=Snowflake.create(id) if (id := payload.get("parent_id")) else None,
            rate_limit_per_user=payload["rate_limit_per_user"],
            rtc_region=payload.get("rtc_region"),
            bitrate=payload["birtate"],
            user_limit=payload["user_limit"],
        )
    elif payload["type"] == channels.ChannelType.DM.value:
        channel = channels.DMChannel(
            client=client,
            raw=payload,
            id=Snowflake.create(payload["id"]),
            last_message_id=Snowflake.create(id) if (id := payload.get("last_message_id")) else None,
            recipients=[payload_to_user(client, user) for user in payload["recipients"]],
        )
    elif payload["type"] in (channels.ChannelType.PUBLIC_THREAD.value, channels.ChannelType.PRIVATE_THREAD.value):
        channel = channels.ThreadChannel(
            client=client,
            raw=payload,
            type=channels.ChannelType.PUBLIC_THREAD if payload["type"] == 11 else channels.ChannelType.PRIVATE_THREAD,
            id=Snowflake.create(payload["id"]),
            name=payload["name"],
            guild_id=Snowflake.create(payload["guild_id"]),
            permissions_overwrites=[PermissionOverwrites(**perm) for perm in payload.get("permission_overwrites", [])],
            parent_id=payload["parent_id"],
            owner_id=payload["owner_id"],
            last_message_id=Snowflake.create(id) if (id := payload.get("last_message_id")) else None,
            position=payload["position"],
            message_count=payload["message_count"],
            rate_limit_per_user=payload["rate_limit_per_user"],
            total_message_sent=payload["total_message_sent"],
            member_count=payload["member_count"],
        )
    elif payload["type"] == channels.ChannelType.GUILD_CATEGORY.value:
        channel = channels.GuildCategoryChannel(
            client=client,
            raw=payload,
            name=payload["name"],
            id=Snowflake.create(payload["id"]),
            guild_id=Snowflake.create(payload["id"]),
            position=payload["position"],
            permissions_overwrites=[PermissionOverwrites(**perm) for perm in payload.get("permission_overwrites", [])],
        )
    elif payload["type"] == channels.ChannelType.ANNOUNCEMENT_THREAD.value:
        channel = channels.ThreadAnnouncementChannel(
            client=client,
            raw=payload,
            id=Snowflake.create(payload["id"]),
            name=payload["name"],
            guild_id=Snowflake.create(payload["guild_id"]),
            permissions_overwrites=[PermissionOverwrites(**perm) for perm in payload.get("permission_overwrites", [])],
            parent_id=payload["parent_id"],
            owner_id=payload["owner_id"],
            last_message_id=Snowflake.create(id) if (id := payload.get("last_message_id")) else None,
            position=payload["position"],
            message_count=payload["message_count"],
            rate_limit_per_user=payload["rate_limit_per_user"],
            total_message_sent=payload["total_message_sent"],
            member_count=payload["member_count"],
        )
    elif payload["type"] == channels.ChannelType.GUILD_ANNOUNCEMENT.value:
        channel = channels.GuildAnnouncmentChannel(
            client=client,
            raw=payload,
            id=Snowflake.create(payload["id"]),
            name=payload["name"],
            guild_id=Snowflake.create(payload["guild_id"]),
            position=payload["position"],
            permissions_overwrites=[PermissionOverwrites(**perm) for perm in payload.get("permission_overwrites", [])],
            nsfw=payload.get("nsfw", False),
            topic=payload.get("topic", None),
            last_message_id=Snowflake.create(id) if (id := payload.get("last_message_id")) else None,
            parent_id=Snowflake.create(id) if (id := payload.get("parent_id")) else None,
            default_auto_archive_duration=payload["default_auto_archive_duration"],
        )
    elif payload["type"] == channels.ChannelType.GUILD_STAGE_VOICE.value:
        channel = channels.GuildStageVoiceChannel(
            client=client,
            raw=payload,
            id=Snowflake.create(payload["id"]),
            name=payload["name"],
            permissions_overwrites=[PermissionOverwrites(**perm) for perm in payload.get("permission_overwrites", [])],
            guild_id=payload["guild_id"],
            position=payload["position"],
            nsfw=payload.get("nsfw", False),
        )
    else:
        raise ValueError("Unidenfitied channel type: %s", payload["type"])
    return channel
