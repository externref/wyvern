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
import dataclasses
import typing

from .events.base_events import GatewayEvent

if typing.TYPE_CHECKING:
    from asuka.bot import Bot


@dataclasses.dataclass
class ListenerConfig:
    guild_only: bool
    dms_only: bool
    bots_only: bool
    humans_only: bool
    ignore_self: bool


class Listener:
    def __init__(self, callback: typing.Callable[[GatewayEvent], typing.Any]) -> None:
        self._bot: "Bot"
        self._configs: ListenerConfig
        self._callback = callback

    async def __call__(self, event: GatewayEvent) -> typing.Any:
        if self._listener_checks(event) is True:
            await self._callback(event)
        else:
            pass

    def _listener_checks(self, event: GatewayEvent) -> bool:
        if getattr(self, "_configs", None) is None:
            return True
        if self._configs.guild_only is True and event.guild_id is None:
            return False
        if self._configs.dms_only is True and event.guild_id is not None:
            return False
        if self._configs.bots_only is True and event.is_bot is False:
            return False
        if self._configs.humans_only is True and event.is_human is False:
            return False
        if self._configs.ignore_self is True and event.author_id is not None and event.author_id == self._bot.user.id:
            return False

        return True

    def set_configs(self, configs: ListenerConfig) -> None:
        self._configs = configs

    @property
    def configs(self) -> ListenerConfig | None:
        return getattr(self, "_configs", None)


def listener_config(
    guild_only=False,
    dms_only=False,
    bots_only=False,
    humans_only=False,
    ignore_self=False,
) -> typing.Callable[[Listener], Listener]:
    def inner(listener: Listener) -> Listener:
        nonlocal guild_only, bots_only, dms_only, humans_only, ignore_self
        if guild_only is True and dms_only is True:
            raise ValueError("You can not have both guild_only and dms_only set to True.")
        if bots_only is True and humans_only is True:
            raise ValueError("You can not have both bots_only and dms_only set to True")
        configs = ListenerConfig(
            guild_only=guild_only,
            dms_only=dms_only,
            bots_only=bots_only,
            humans_only=humans_only,
            ignore_self=ignore_self,
        )
        listener.set_configs(configs)
        return listener

    return inner


class EventHandler:
    bot: "Bot"
    listeners: typing.Dict[
        typing.Type[GatewayEvent],
        typing.List[Listener],
    ] = {}
    once_listeners: typing.Dict[
        typing.Type[GatewayEvent],
        typing.List[
            Listener,
        ],
    ] = {}

    def add_listener(
        self,
        event_class: typing.Type[GatewayEvent],
        listener: Listener,
    ) -> None:
        listener._bot = self.bot
        if (lsnrs := self.listeners.get(event_class)) is not None:
            lsnrs.append(listener)
        else:
            self.listeners[event_class] = [listener]

    def add_once_listener(
        self,
        event_class: typing.Type[GatewayEvent],
        listener: Listener,
    ) -> None:

        listener._bot = self.bot
        if (lsnrs := self.once_listeners.get(event_class)) is not None:
            lsnrs.append(listener)
        else:
            self.once_listeners[event_class] = [listener]

    def dispatch(
        self,
        event_type: typing.Type[GatewayEvent],
        payload: typing.Dict[typing.Any, typing.Any],
    ) -> None:

        event = event_type(self.bot, payload)
        to_call = []
        to_call.extend([listener(event) for listener in self.listeners.get(event_type, [])])
        for listener in self.once_listeners.get(event_type, []):
            to_call.append(listener(event))
        self.once_listeners[event_type] = []

        asyncio.gather(*to_call)
