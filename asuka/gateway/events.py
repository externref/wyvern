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

import datetime
import typing

from asuka.events.messages import MessageCreate
from asuka.models.users import PartialUser

if typing.TYPE_CHECKING:
    from asuka.bot import Bot


class EventParser:
    @staticmethod
    def message_create(bot: "Bot", payload: typing.Dict[str, typing.Any]) -> MessageCreate:
        data = payload["d"]
        from_bot: bool = data["author"].get("bot")
        from_human: bool = not bot
        user = PartialUser(
            _raw_data=data,
            _bot=bot,
            id=data["author"]["id"],
            username=data["author"]["username"],
            discriminator=data["author"]["discriminator"],
            is_mfa_enabled=data["author"].get("mfa_enabled", False),
        )

        return MessageCreate(
            bot=bot,
            author_id=data["author"]["id"],
            message_id=data["id"],
            guild_id=data.get("guild_id"),
            created_at=datetime.datetime.fromisoformat(data["timestamp"]),
            from_bot=from_bot,
            from_human=from_human,
            channel_id=data["channel_id"],
            user=user,
        )
