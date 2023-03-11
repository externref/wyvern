from __future__ import annotations

import datetime

import attrs

from wyvern.files import Avatar, AvatarType

from .base import Snowflake
from .users import User


@attrs.define(kw_only=True, slots=True, repr=True)
class Member(User):
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

    def update_state(self) -> "Member" | None:
        return member if (member := self.client.members.get(self.guild_id, self.id)) else None

    @property
    def display_avatar(self) -> Avatar:
        """
        Returns
        -------
        str
            Member's visible avatar.
        """
        return self.guild_avatar or self.avatar or self.default_avatar

    @property
    def display_name(self) -> str:
        """
        Returns
        -------
        str
            Member's visible name.
        """
        return self.nickname or self.username

    @property
    def guild_avatar(self) -> Avatar | None:
        """
        Returns
        -------
        None | wyvern.Avatar
            The user's guild avatar.
        """
        return (
            Avatar(client=self.client, type=AvatarType.GUILD, hash=self.guild_avatar_hash)
            if self.guild_avatar_hash
            else None
        )
