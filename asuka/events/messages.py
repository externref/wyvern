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
import datetime
import typing

from ..models.users import PartialUser
from .base_events import GatewayEvent

if typing.TYPE_CHECKING:
    from asuka.bot import Bot


class MessageCreate(GatewayEvent):
    bot: "Bot"
    id: int
    author_id: int
    message_id: int
    created_at: datetime.datetime
    from_bot: bool
    from_human: bool
    from_webhook: bool
    shard: int
    channel_id: int | None
    webhook_id: int | None
    reference_message_id: int | None
    user: PartialUser

    message: typing.Any

    def __init__(self, bot: "Bot", payload: typing.Dict[typing.Any, typing.Any]) -> None:
        super().__init__(bot)

        self._payload_data = payload
        self._initialize_event_from_payload()

    @property
    def data(self) -> typing.Dict[str, typing.Any]:
        return self._payload_data["d"]

    def _initialize_event_from_payload(self) -> None:
        self.id = int(self.data["id"])
        self.author_id = int(self.data["author"]["id"])
        self.channel_id = int(self.data["channel_id"])
        self.created_at = datetime.datetime.fromisoformat(self.data["timestamp"])
        self.is_human = not self.data["author"].get("bot")
        self.is_bot = not self.is_human
        self.user = PartialUser(self.data["author"])
        self.guild_id = self.data.get("guild_id")
