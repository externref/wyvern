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


@attrs.define(kw_only=True, slots=True, repr=True, eq=True)
class User(DiscordObject):
    _client: "GatewayClient"
    id: int
    username: str
    discriminator: int
    avatar_hash: str | None
    is_bot: bool
    is_system: bool
    is_mfa_enabled: bool
    banner_hash: str | None
    accent_color: int | None
    locale: str | None
    flags_value: int | None
    premium_type_value: int | None
    public_flags_value: int | None

    @property
    def created_at(self) -> datetime.datetime:
        return self.get_created_at(self.id)


@typing.final
class BotUser(User):
    async def edit(self, username: str | None = None, avatar: bytes | None = None) -> "BotUser":
        return await self._client.rest.edit_client_user(username, avatar)
