from __future__ import annotations

import datetime
import typing

import attrs

from .base import DiscordObject

if typing.TYPE_CHECKING:
    from wyvern.client import GatewayClient
    from wyvern.constructors.embed import Embed

    from .user import User


@attrs.define(kw_only=True)
class Message(DiscordObject):
    _client: "GatewayClient"
    id: int
    tts: bool
    pinned: bool
    mentions: list["User"]
    mention_roles: list[int]
    flags_value: int
    embeds: list["Embed"]
    edited_at: datetime.datetime | None
    content: str | None
    channel_id: int
    author: "User"
    attachments: list[typing.Any]
