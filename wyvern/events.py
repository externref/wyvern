from __future__ import annotations

import asyncio
import typing

import attrs

if typing.TYPE_CHECKING:
    from wyvern.client import GatewayClient


class Event:
    """Event Enums."""

    MESSAGE_CREATE = "MESSAGE_CREATE"


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

    client : wyvern.client.GatewayClient
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

    def listen(self) -> typing.Callable[[EventListener], EventListener]:
        """
        This decorator adds a listener object to the handler's container

        Example
        -------

            >>> import wyvern
            >>>
            >>> client = wyvern.GatewayClient("TOKEN")
            >>>
            >>> @client.event_handler.listen()
            >>> @wyvern.listener(wyvern.Event.MESSAGE_CREATE)
            >>> async def message_create(message: wyvern.Message) -> None:
            >>>     ...
            >>>
            >>> client.run()

        Returns
        -------
        wyvern.events.EventListener
            The listener that was created using @listener decorator.
        """

        def inner(listener_obj: EventListener) -> EventListener:
            self.add_listener(listener_obj)
            return listener_obj

        return inner

    def add_listener(self, event_listener: EventListener) -> None:
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
