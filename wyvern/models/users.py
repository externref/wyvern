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

import attrs

from .base import DiscordObject

if typing.TYPE_CHECKING:
    from wyvern.clients import GatewayClient

__all__: tuple[str, ...] = ("User", "BotUser")


@attrs.define(kw_only=True, slots=True, repr=True)
class User(DiscordObject):
    """Represents a discord user."""

    _client: "GatewayClient"
    id: int
    """ID of the user."""
    username: str
    """Username of the user."""
    discriminator: int
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

    @property
    def created_at(self) -> datetime.datetime:
        """Datetime at which user was created."""
        return self.get_created_at(self.id)


@typing.final
class BotUser(User):
    """Represents the bot user on discord."""

    async def edit(self, username: str | None = None, avatar: bytes | None = None) -> "BotUser":
        """Edits the bot's user.

        Arguments
        ---------

        username : str
            The new username.
        avatar : bytes
            The new avatar bytes.

        Returns
        -------

        wyvern.models.users.BotUser
            The updated user of bot.
        """
        return await self._client.rest.edit_client_user(username, avatar)
