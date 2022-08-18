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

import dataclasses
import typing

from asuka.assets import Asset
from asuka.builders.base_objs import DiscordObject
from asuka.utils import default_avatar_for

if typing.TYPE_CHECKING:
    from asuka.bot import Bot


@dataclasses.dataclass
class PartialUser(DiscordObject):
    _raw_data: typing.Dict[str, typing.Any]
    _bot: "Bot"
    id: int
    username: str
    discriminator: str
    is_mfa_enabled: bool

    def __repr__(self) -> str:
        return f"{self.username}#{self.discriminator}"

    def __eq__(self, obj: object) -> bool:
        if not isinstance(obj, PartialUser):
            raise NotImplemented
        return self.id == obj.id

    @classmethod
    def from_payload(cls, bot: "Bot", data: typing.Dict[str, typing.Any]) -> "PartialUser":
        return cls(
            _raw_data=data,
            _bot=bot,
            id=data["author"]["id"],
            username=data["author"]["username"],
            discriminator=data["author"]["discriminator"],
            is_mfa_enabled=data["author"].get("mfa_enabled", False),
        )

    @property
    def avatar(self) -> Asset | None:
        return Asset(url, self._bot) if (url := self._raw_data["author"].get("avatar")) else None

    @property
    def default_avatar(self) -> Asset:
        return Asset(f"https://cdn.discordapp.com/embed/avatars/{default_avatar_for(self)}.png", self._bot)


class BotUser(PartialUser):
    @classmethod
    def from_payload(cls, bot: "Bot", data: typing.Dict[str, typing.Any]) -> "BotUser":
        base = typing.cast(BotUser, super().from_payload(bot, data))
        return base
