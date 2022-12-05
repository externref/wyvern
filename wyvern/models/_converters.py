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
    user = payload_to_user(client, payload=payload)
    return Member(
        client=client,
        raw=payload,
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
        role_ids=[Snowflake.create(id) for id in payload["role_ids"]],
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
