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

from wyvern.models.snowflake import DiscordObject, Snowflake


@attrs.define(kw_only=True, slots=True, frozen=True)
class AllowedMentions:
    """Allowed mentions in a message sent from bot.

    Parameters
    ----------
    users: bool
        Set to `True` to mention users.
    roles: bool
        Set to `True` to mention roles.
    everyone: bool
        Set to `True` to allow everyone/here mentions.
    replied_user: bool
        Weather the replied users should be pinged.
    """

    users: bool = False
    roles: bool = False
    everyone: bool = False
    replied_user: bool = False

    def to_dict(self) -> dict[str, typing.Any]:
        return {
            "parse": [t for t in ("roles", "users", "everyone") if getattr(self, t, False) is True],
            "replied_user": self.replied_user,
        }


@attrs.define(kw_only=True, slots=True, frozen=True)
class PartialMessage(DiscordObject):
    id: Snowflake
    """ID of the message."""
