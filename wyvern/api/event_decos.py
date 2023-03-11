from __future__ import annotations

import typing

from wyvern import events, types
from wyvern.api import event_handler as handler


class ImplementsEventDecos:
    """Interface for event decorators in :class:`.GatewayBot`,
    this class is purely for the bot class to inherit from.

    Example
    -------

    .. highlight:: python
    .. code-block:: python

        @bot.on_started()
        async def started(event: wyvern.StartedEvent) -> None:
            bot.logger.info(f"Logged in as {event.user.tag}")

    """

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
        """Used to create a :class:`.StartingEvent` listener.

        Returns
        -------
        EventListener
            The listener that was created."""
        return self._make_deco(events.StartingEvent, **kwargs)

    def on_started(
        self, **kwargs: typing.Any
    ) -> typing.Callable[[types.EventListenerCallbackT], handler.EventListener]:
        """Used to create a :class:`.StartedEvent` listener.

        Returns
        -------
        EventListener
            The listener that was created."""
        return self._make_deco(events.StartedEvent, **kwargs)
