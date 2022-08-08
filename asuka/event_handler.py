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

import asyncio
import typing

from .events.base_events import GatewayEvent

if typing.TYPE_CHECKING:
    from asuka.bot import Bot


class EventHandler:
    bot: "Bot"
    listeners: typing.Dict[
        typing.Type[GatewayEvent],
        typing.List[
            typing.Callable[[GatewayEvent], typing.Any],
        ],
    ] = {}
    once_listeners: typing.Dict[
        typing.Type[GatewayEvent],
        typing.List[
            typing.Callable[[GatewayEvent], typing.Any],
        ],
    ] = {}

    def add_listener(
        self,
        event_class: typing.Type[GatewayEvent],
        callback: typing.Callable[[GatewayEvent], typing.Any],
    ) -> None:
        if (lsnrs := self.listeners.get(event_class)) is not None:
            lsnrs.append(callback)
        else:
            self.listeners[event_class] = [callback]

    def add_once_listener(
        self,
        event_class: typing.Type[GatewayEvent],
        callback: typing.Callable[[GatewayEvent], typing.Any],
    ) -> None:
        if (lsnrs := self.once_listeners.get(event_class)) is not None:
            lsnrs.append(callback)
        else:
            self.once_listeners[event_class] = [callback]

    def dispatch(
        self,
        event_type: typing.Type[GatewayEvent],
        payload: typing.Dict[typing.Any, typing.Any],
    ) -> None:
        event = event_type(self.bot, payload)
        to_call = []
        to_call.extend(
            [listener(event) for listener in self.listeners.get(event_type, [])]
        )
        for listener in self.once_listeners.get(event_type, []):
            to_call.append(listener(event))
        self.once_listeners[event_type] = []

        asyncio.gather(*to_call)
