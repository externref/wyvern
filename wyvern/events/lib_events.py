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

from wyvern.events.base import Event

if typing.TYPE_CHECKING:
    from wyvern.models.users import BotUser

__all__: tuple[str, ...] = ("StartingEvent", "StartedEvent")


@attrs.define(kw_only=True)
class StartingEvent(Event):
    """This event is dispatched when the bot is about to connect to the gateway.

    .. note::
        This event gets triggered only once in the runtime.
    """


@attrs.define(kw_only=True)
class StartedEvent(Event):
    """The StartedEvent is dispatched when the :any:`GatewayBot.start` method is called
    and the bot recieves first Websocket response from API after token verification.

    .. note::
        This event gets triggered only once in the runtime.
    """

    user: BotUser