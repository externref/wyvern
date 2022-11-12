from __future__ import annotations

import datetime

import attrs

from wyvern.assets import Avatar, AvatarType

from .base import Snowflake
from .users import User


@attrs.define(kw_only=True, slots=True, repr=True)
class Member(User):
    guild_id: int
    nickname: str | None
    role_ids: list[Snowflake]
    joined_at: datetime.datetime
    premium_since: datetime.datetime | None
    deaf: bool | None
    mute: bool | None
    pending: bool
    communication_disabled_until: datetime.datetime | None
    guild_avatar_hash: str | None

    @property
    def guild_avatar(self) -> Avatar | None:
        return (
            Avatar(client=self._client, type=AvatarType.GUILD, hash=self.guild_avatar_hash)
            if self.guild_avatar_hash
            else None
        )
