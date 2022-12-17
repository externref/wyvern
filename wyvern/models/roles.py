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

from .base import DiscordObject, Snowflake

if typing.TYPE_CHECKING:
    from .guilds import Guild

__all__: tuple[str, ...] = (
    "Role",
    "RoleTags",
)


@attrs.define(kw_only=True, slots=True, repr=True)
class RoleTags(DiscordObject):
    raw: dict[str, Role]
    bot_id: typing.Optional[Snowflake]
    integration_id: typing.Optional[Snowflake]
    premium_subscriber: typing.Optional[bool]

    def is_bot_managed(self) -> bool:
        return self.bot_id is not None

    def is_integration_managed(self) -> bool:
        return self.integration_id is not None

    def is_premium_subscriber(self) -> bool:
        return self.premium_subscriber is not None

    @property
    def created_at(self) -> datetime.datetime:
        """Datetime at which role was created."""
        return super().created_at


@attrs.define(kw_only=True, slots=True, repr=True, order=False)
class Role(DiscordObject):
    raw: dict[str, typing.Any]
    id: Snowflake
    name: str
    color: int
    is_hoisted: bool
    icon: typing.Optional[str]
    unicode_emote: typing.Optional[str]
    position: int
    permissions: str
    is_managed: bool
    is_mentionable: bool
    tags: typing.Optional[RoleTags]
    guild: "Guild"

    def __lt__(self, other: typing.Any) -> bool:
        if not isinstance(other, Role) or not isinstance(self, Role):
            return NotImplemented
        if self.guild != other.guild:
            raise ValueError("Cannot compare roles from different guilds.")
        # everyone role is always at the bottom
        if self.id == self.guild.id:
            return other.id != self.guild.id
        if self.position < other.position:
            return True
        if self.position == other.position:
            return int(self.id) > int(other.id)
        return False

    def __le__(self, other: Role) -> bool:
        r = Role.__lt__(self, other)
        if r is NotImplemented:
            return NotImplemented
        return not r

    def __gt__(self, other: Role) -> bool:
        return Role.__le__(self, other)

    def __ge__(self, other: Role) -> bool:
        r = Role.__lt__(self, other)
        if r is NotImplemented:
            return NotImplemented
        return not r

    def is_bot_managed(self) -> bool:
        return self.tags.is_bot_managed() if self.tags else False

    def is_integration_managed(self) -> bool:
        return self.tags.is_integration_managed() if self.tags else False

    def is_premium_subscriber(self) -> bool:
        return self.tags.is_premium_subscriber() if self.tags else False

    @property
    def created_at(self) -> datetime.datetime:
        """Datetime at which role was created."""
        return super().created_at
