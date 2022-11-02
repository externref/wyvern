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
import enum
import typing

import attrs

if typing.TYPE_CHECKING:
    from wyvern.clients import GatewayClient

__all__: tuple[str, ...] = ("Event", "EventListener", "EventHandler", "listener")


@typing.final
class Event:
    """Event Enums."""

    MESSAGE_CREATE = "MESSAGE_CREATE"
    """Triggered when a message is created.

     Note: This event gets triggerd once in a runtime.
    
    Arguments provided:

    * message ([wyvern.Message][])
    """
    INTERACTION_CREATE = "INTERACTION_CREATE"

    # Library Events

    STARTING = "STARTING"
    """Triggered when bot is loaded and is starting.

    Note: This event gets triggerd once in a runtime.
    
    Arguments provided:
    
    * client ([wyvern.GatewayClient][])"""
    STARTED = "STARTED"
    """Triggered when the bot has successfully verified its token and is running.
    
    Arguments provided:
    
    * client ([wyvern.GatewayClient][])"""
    GATEWAY_CONNECTED = "GATEWAY_CONNECTED"
    """Triggered when the gateway initalises a connection.
    
    Arguments provided:

    * client ([wyvern.GatewayClient][])"""
    


@typing.final
@attrs.define
class EventListener:
    """
    Class representating a callable to be called when a specific event type is
    dispatched.

    Parameters
    ----------

    event_type : str | wyvern.events.Event
        The type of event this listener belongs to.
    callback : typing.Callable[..., typing.Awaitable[typing.Any]]
        The coroutine to run when event is dispatched
    max_trigger : int | float
        Max amount of time this listener will be triggered.

    Attributes
    ----------

    trigger_count: int
        Number of times this listener has been triggered
    """

    event_type: str | Event
    callback: typing.Callable[..., typing.Awaitable[typing.Any]]
    max_trigger: int | float
    trigger_count: int = 0

    def __call__(self, *args: typing.Any) -> typing.Awaitable[typing.Any]:
        self.trigger_count += 1
        return self.callback(*args)


class EventHandler:
    """
    Event handler to deal with incoming events from the Gateway.

    Parameters
    ----------

    client : wyvern.clients.GatewayClient
        The client binded with the event handler.

    Attributes
    ----------

    listeners: dict[str | [wyvern.events.Event], list[wyvern.events.EventListener]]
        A container for event listeners.
    """

    listeners: dict[str | Event, list[EventListener]] = {}

    def __new__(cls: type["EventHandler"], client: "GatewayClient") -> "EventHandler":

        inst = super().__new__(cls)
        for _obj in cls.__mro__:
            for item in _obj.__dict__.values():
                if isinstance(item, EventListener):
                    inst.add_listener(item)
        return inst

    def __init__(self, client: "GatewayClient") -> None:
        self.client = client

    def add_listener(self, event_listener: EventListener) -> None:
        """
        Adds a listener to the handler.

        Arguments
        ---------

        event_listener: wyvern.events.EventListener
            The listener to be added.
        """
        self.listeners.setdefault(event_listener.event_type, []).append(event_listener)

    def dispatch(self, event: str | Event, *args: typing.Any) -> None:
        """
        Dispatches events from the gateway.
        This method runs all the listeners registered in the container
        for the specific event.

        Parameters
        ----------

        event: str | wyvern.events.Event
            Name of the event to be dispatched.
        *args: tuple[typing.Any, ...]
            Arguments to provide in callbacks.


        """
        print(event)
        invokes = [
            (lsnr(self, *args) if (len(str(lsnr.callback).split(".")) > 1) else lsnr(*args))
            for lsnr in self.listeners.get(event, [])
            if lsnr.max_trigger > lsnr.trigger_count
        ]
        asyncio.gather(*invokes)


def listener(
    event: str | Event, *, max_trigger: int | float = float("inf")
) -> typing.Callable[[typing.Callable[..., typing.Awaitable[typing.Any]]], EventListener]:
    """Creates a [wyvern.events.EventListener][] object.

    Parameters
    ----------

    event: str | wyvern.events.Event
        The event to listen.
    max_trigger: int | float
        Maximum number of times this listener has to be triggered.

    Returns
    -------

    wyvern.events.EventListener
        A EventListener object.

    """

    def inner(callback: typing.Callable[..., typing.Awaitable[typing.Any]]) -> EventListener:
        nonlocal event, max_trigger
        return EventListener(event, callback, max_trigger, 0)

    return inner
