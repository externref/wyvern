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

import asyncio
import typing

import attrs

from wyvern import types
from wyvern.events.base import Event
from wyvern.utils.consts import UNDEFINED, Undefined

if typing.TYPE_CHECKING:
    from wyvern.api.bot import GatewayBot

__all__: tuple[str, ...] = ("EventListener", "EventHandler", "listener")


@attrs.define(kw_only=True)
class EventListener:
    """Represents an event listener, the callback of this class gets triggered whenever the event
    this listener is bound to gets triggered."""

    type: type[Event]
    """Type of event this listener listens to."""
    max_trigger: int | Undefined = UNDEFINED
    """Maximum number of times this event can get triggered."""
    callback: types.EventListenerCallbackT
    """The callback for listener."""
    bot: GatewayBot | Undefined = UNDEFINED

    def __call__(self, event: Event) -> typing.Any:
        return self.callback(event)


@attrs.define(kw_only=True)
class EventHandler:
    """Class handling dispatches and containing of the event listeners.
    An instance of this class is bound to the :class:`.GatewayBot` to handle events.
    """

    bot: GatewayBot
    listeners: dict[type[Event], list[EventListener]] = {}
    """Mapping of :class:`.Event` types to list of :class:`EventListener` s listening to the event."""

    def add_listener(self, lsnr: EventListener) -> None:
        """Adds a listener to the container.

        Parameters
        ----------
        lsnr: EventListener
            The listener to add.
        """
        if lsnr.bot == UNDEFINED:
            lsnr.bot = self.bot
        self.listeners.setdefault(lsnr.type, []).append(lsnr)

    def dispatch(self, event: Event) -> None:
        asyncio.gather(*list(map(lambda elistener: elistener(event), self.listeners.get(type(event), []))))


def listener(
    event: type[Event], *, max_trigger: int | Undefined = UNDEFINED
) -> typing.Callable[[types.EventListenerCallbackT], EventListener]:
    """Used to create an :class:`EventListener`.

    Parameters
    ----------
    event: type[Event]
        Class of the event this listener is bound to.
    max_trigger: int
        Maximum trigger limit of the event callback.

    Returns
    -------
    EventListener
        The listener that was created.
    """

    def decorator(callback: types.EventListenerCallbackT) -> EventListener:
        return EventListener(
            type=event,
            max_trigger=max_trigger,
            callback=callback,
        )

    return decorator
