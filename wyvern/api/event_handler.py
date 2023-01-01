from __future__ import annotations

import asyncio
import typing

import attrs

from wyvern import types
from wyvern.events.base import Event
from wyvern.utils.consts import UNDEFINED, Undefined

if typing.TYPE_CHECKING:
    from wyvern.api.bot import Bot

__all__: tuple[str, ...] = ("EventListener", "EventHandler", "listener")


@attrs.define(kw_only=True)
class EventListener:
    type: type[Event]
    max_trigger: int | Undefined = UNDEFINED
    callback: types.EventListenerCallbackT
    bot: Bot | Undefined = UNDEFINED

    def __call__(self, event: Event) -> typing.Any:
        return self.callback(event)


@attrs.define(kw_only=True)
class EventHandler:
    bot: Bot
    listeners: dict[type[Event], list[EventListener]] = {}

    def add_listener(self, lsnr: EventListener) -> None:
        if lsnr.bot == UNDEFINED:
            lsnr.bot = self.bot
        self.listeners.setdefault(lsnr.type, []).append(lsnr)

    def dispatch(self, event: Event) -> None:
        asyncio.gather(*list(map(lambda elistener: elistener(event), self.listeners.get(type(event), []))))


def listener(
    event: type[Event], *, max_trigger: int | Undefined = UNDEFINED
) -> typing.Callable[[types.EventListenerCallbackT], EventListener]:
    def decorator(callback: types.EventListenerCallbackT) -> EventListener:
        return EventListener(
            type=event,
            max_trigger=max_trigger,
            callback=callback,
        )

    return decorator
