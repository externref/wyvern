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


class DiscordObject:
    def __init__(
        self,
        *,
        id: int,
    ) -> None:
        self.id = id
        self._created_at = self.get_created_at(id)

    @classmethod
    def get_created_at(cls, id: int) -> datetime.datetime:
        timestamp = ((id >> 22) + 1420070400000) / 1000
        return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)

    @property
    def created_at(
        self,
    ) -> datetime.datetime:
        return self._created_at


@typing.final
class Intents:
    NONE = 0
    GUILDS = 1 << 0
    GUILD_MEMBERS = 1 << 1
    GUILD_BANS = 1 << 2
    GUILD_EMOJIS = 1 << 3
    GUILD_INTEGRATIONS = 1 << 4
    GUILD_WEBHOOKS = 1 << 5
    GUILD_INVITES = 1 << 6
    GUILD_VOICE_STATES = 1 << 7
    GUILD_PRESENCES = 1 << 8
    GUILD_MESSAGES = 1 << 9
    GUILD_MESSAGE_REACTIONS = 1 << 10
    GUILD_MESSAGE_TYPING = 1 << 11
    DM_MESSAGES = 1 << 12
    DM_MESSAGE_REACTIONS = 1 << 13
    DM_MESSAGE_TYPING = 1 << 14
    MESSAGE_CONTENT = 1 << 15
    GUILD_SCHEDULED_EVENTS = 1 << 16

    def __init__(
        self,
        *args: int,
    ) -> None:
        self._value = 0
        # self.enabled: typing.MutableSet = set()
        for value in args:
            self._value |= value

    @property
    def value(self) -> int:
        return self._value

    @classmethod
    def from_value(cls, value: int) -> "Intents":
        intents = Intents()
        intents._value = value
        return intents
