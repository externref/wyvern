from __future__ import annotations

import typing

from wyvern import events, types
from wyvern.api import event_handler as handler


class ImplementsEventDecos:
    event_handler: handler.EventHandler

    def _make_deco(
        self, event: type[events.Event], **kwargs: typing.Any
    ) -> typing.Callable[[types.EventListenerCallbackT], handler.EventListener]:
        def decorator(callable: types.EventListenerCallbackT) -> handler.EventListener:
            self.event_handler.add_listener(lsnr := handler.EventListener(type=event, callback=callable, **kwargs))
            return lsnr

        return decorator

    def on_starting(
        self, **kwargs: typing.Any
    ) -> typing.Callable[[types.EventListenerCallbackT], handler.EventListener]:
        return self._make_deco(events.StartingEvent, **kwargs)

    def on_started(
        self, **kwargs: typing.Any
    ) -> typing.Callable[[types.EventListenerCallbackT], handler.EventListener]:
        return self._make_deco(events.StartedEvent, **kwargs)
