from __future__ import annotations

import datetime
import typing

import attrs

from .base import DiscordObject

if typing.TYPE_CHECKING:
    from wyvern.client import GatewayClient


@attrs.define
class User(DiscordObject):
    _client: "GatewayClient"
    id: int
    username: str
    disciminator: int
    avatar_hash: str | None
    is_bot: bool
    is_system: bool
    is_mfa_enabled: bool
    banner_hash: str | None
    accent_color: int
    locale: str | None
    flags: int | None
    premium_type: int | None
    public_flags: int | None

    @property
    def created_at(self) -> datetime.datetime:
        return self.get_created_at(self.id)


class BotUser(User):
    async def edit(self, username: str | None = None, avatar: bytes | None = None) -> "BotUser":
        ...
