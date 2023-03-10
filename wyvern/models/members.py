from __future__ import annotations

import datetime
import typing

import attrs

from wyvern.models.snowflake import Snowflake
from wyvern.models.users import PartialUser, User

if typing.TYPE_CHECKING:
    import discord_typings

    from wyvern.api.bot import GatewayBot

__all__: tuple[str, ...] = ("GuildMember", )

@attrs.define(kw_only=True)
class GuildMember(User):
    raw: discord_typings.GuildMemberData  # type: ignore
    """Raw payload."""
    user: User
    """User of the member."""
    guild_id: Snowflake
    """ID of the guild this member belongs to."""
    nickname: str | None
    """Nickname of the member, if any."""
    role_ids: list[Snowflake]
    """List of role ids."""
    joined_at: datetime.datetime
    """Datetime on which the member joined the guild."""
    premium_since: datetime.datetime | None
    """Datetime since member has been boosting the guild."""
    deaf: bool | None
    """True if member is deafened."""
    mute: bool | None
    """True if member is muted."""
    pending: bool
    """True if member is in pending state."""
    communication_disabled_until: datetime.datetime | None
    """Timeout for the member."""
    guild_avatar_hash: str | None
    """Avatar hash for the guild."""

    @property
    def display_name(self) -> str:
        """
        Returns
        -------
        str
            Nickname of the user if exists, else the username.
        """
        return self.nickname or self.username

    @classmethod
    def from_payload(cls, bot: GatewayBot, guild_id: int, payload: discord_typings.GuildMemberData) -> GuildMember:
        user: User = User.from_partial(bot, PartialUser.from_payload(payload["user"]))  # type: ignore
        return GuildMember(
            user=user,
            id=user.id,
            username=user.username,
            discriminator=user.discriminator,
            raw=payload,
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
            bot=bot,
            partial_user=user.partial_user,
            guild_id=Snowflake(guild_id),
            nickname=payload.get("nick"),
            role_ids=[Snowflake(_id) for _id in payload["roles"]],
            joined_at=datetime.datetime.fromisoformat(payload["joined_at"]),
            premium_since=datetime.datetime.fromisoformat(ps) if (ps := payload.get("premium_since")) else None,
            deaf=payload["deaf"],
            mute=payload["mute"],
            pending=payload.get("pending") or False,
            communication_disabled_until=payload.get("communication_disabled_until"),
            guild_avatar_hash=av if (av := payload.get("avatar")) else None,
        )
