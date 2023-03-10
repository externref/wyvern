# MIT License

# Copyright (c) 2023 Sarthak

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

import typing

import attrs

from wyvern.models.abc import ImplementsMessage
from wyvern.models.snowflake import DiscordObject, Snowflake
from wyvern.utils.consts import UNDEFINED, Undefined

if typing.TYPE_CHECKING:
    import datetime

    import discord_typings

    from wyvern.api.bot import GatewayBot


@attrs.define(kw_only=True)
class UserLike(DiscordObject):
    """Object representing a user like entity ( user, member, thread member, etc...)."""

    id: Snowflake
    """ID of the particular user."""
    username: str
    """Username of the user."""
    discriminator: str
    """Discriminator of the user."""

    def __str__(self) -> str:
        return self.tag

    @property
    def created_at(self) -> datetime.datetime:
        """
        Returns
        -------
        datetime.datetime
            The datetime when this user was created.
        """
        return super().created_at

    @property
    def tag(self) -> str:
        """Return user tag ( ``username#disciminator`` )"""
        return f"{self.username}#{self.discriminator}"


@attrs.define(kw_only=True)
class PartialUser(UserLike):
    """Object representing a user object."""

    raw: discord_typings.UserData
    """The raw data from discord this object was constructed from."""
    id: Snowflake
    """ID of the user."""
    username: str
    """Username of the user."""
    discriminator: str
    """User's discriminator."""
    avatar_hash: str | None
    """Hash of the user's avatar"""
    is_bot: bool
    """True if the user is a bot."""
    is_system: bool
    """True if the user is a system user."""
    is_mfa_enabled: bool
    """True if the user has mfa enabled ( can be false even if it's enabled )"""
    banner_hash: str | None
    """User's banner hash."""
    accent_color: int | None
    """User's accent color."""
    locale: str | None
    """User's locale."""
    flags_value: int | None
    """Integer value for user flags"""
    premium_type_value: int | None
    """Premium type integer."""
    public_flags_value: int | None
    """Integer value for user's public flags"""

    @classmethod
    def from_payload(cls, payload: discord_typings.UserData) -> PartialUser:
        return PartialUser(
            raw=payload,
            id=Snowflake(payload["id"]),
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


@attrs.define(kw_only=True)
class User(PartialUser, ImplementsMessage):
    bot: GatewayBot
    """The current bot application."""
    partial_user: Undefined | PartialUser = attrs.field(default=UNDEFINED)
    """The partial user this class was constructed from, if any."""

    async def create_message(self, content: str) -> ...:
        return await super().create_message(content)

    @classmethod
    def from_partial(cls, bot: GatewayBot, partial_user: PartialUser) -> User:
        return User(
            raw=partial_user.raw,
            id=partial_user.id,
            username=partial_user.username,
            discriminator=partial_user.discriminator,
            avatar_hash=partial_user.avatar_hash,
            is_bot=partial_user.is_bot,
            is_system=partial_user.is_system,
            is_mfa_enabled=partial_user.is_mfa_enabled,
            banner_hash=partial_user.banner_hash,
            accent_color=partial_user.accent_color,
            locale=partial_user.locale,
            flags_value=partial_user.flags_value,
            premium_type_value=partial_user.premium_type_value,
            public_flags_value=partial_user.public_flags_value,
            bot=bot,
            partial_user=partial_user,
        )


class BotUser(User):
    @classmethod
    def from_partial(cls, bot: GatewayBot, partial_user: PartialUser) -> BotUser:
        return BotUser(
            raw=partial_user.raw,
            id=partial_user.id,
            username=partial_user.username,
            discriminator=partial_user.discriminator,
            avatar_hash=partial_user.avatar_hash,
            is_bot=partial_user.is_bot,
            is_system=partial_user.is_system,
            is_mfa_enabled=partial_user.is_mfa_enabled,
            banner_hash=partial_user.banner_hash,
            accent_color=partial_user.accent_color,
            locale=partial_user.locale,
            flags_value=partial_user.flags_value,
            premium_type_value=partial_user.premium_type_value,
            public_flags_value=partial_user.public_flags_value,
            bot=bot,
            partial_user=partial_user,
        )
