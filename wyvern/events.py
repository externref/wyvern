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

from wyvern.utils import get_arg_count

if typing.TYPE_CHECKING:
    from wyvern._types import AnyCallableT, CheckT
    from wyvern.clients import GatewayClient


__all__: tuple[str, ...] = ("Event", "EventListener", "EventHandler", "as_listener")


@typing.final
class Event(enum.Enum):
    """Event Enums."""

    READY = "READY"

    MESSAGE_CREATE = "MESSAGE_CREATE"
    """Triggered when a message is created.
    
    Arguments provided:

    * message ([wyvern.Message][])
    """
    INTERACTION_CREATE = "INTERACTION_CREATE"
    """Triggered when an interaction is created.
    
    Arguments provided:

    * interaction ([wyvern.Interaction])
    
    !!! note
        The interaction argument can be any derivative of interaction!.
    """
    GUILD_CREATE = "GUILD_CREATE"
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
    """Class representating a callable to be called when a specific event type is
    dispatched.

    Parameters
    ----------
    event_type : str | wyvern.events.Event
        The type of event this listener belongs to.
    callback : typing.Callable[..., typing.Awaitable[typing.Any]]
        The coroutine to run when event is dispatched
    max_trigger : int | float
        Max amount of time this listener will be triggered.
    checks: list[wyvern._types.CheckT]
        Checks added to the event listener.

    Attributes
    ----------
    trigger_count: int
        Number of times this listener has been triggered
    """

    __parent_identity__: str = attrs.field(init=False, default="-")
    event_type: Event
    callback: AnyCallableT
    max_trigger: int | float
    trigger_count: int = 0
    event_handler: EventHandler | None = None
    checks: list[CheckT] = attrs.field(init=False, default=[])

    def check(self, predicate: CheckT) -> CheckT:
        """Adds an check to the listener.
        The check callback accepts the same arguments as the related event.
        The predicate should return a bool ( strict to True or False ).

        Example
            import wyvern

            client = wyvern.GatewayClient("TOKEN")

            @client.with_listener(wyvern.Event.MESSAGE_CREATE)
            async def msg_create(msg: wyvern.Message) -> None:
                await msg.respond("This message was created when the check passed.")

            @msg_create.check
            async def msg_create_check(msg: wyvern.Message) -> bool:
                return msg.author.id == 1234567890123456789

            client.run()


        """

        def inner() -> CheckT:
            nonlocal predicate
            if not get_arg_count(predicate) == get_arg_count(self.callback):
                raise TypeError("EventListener and check callbacks should accept same number of arguments.")
            self.checks.append(predicate)
            return predicate

        return inner()

    async def process_checks(self, *args: typing.Any) -> bool:
        assert self.event_handler
        results = [await check(*args) for check in self.checks]
        if any(faulty_checks := [results.index(result) for result in results if result not in (True, False)]):
            self.event_handler.client._logger.warning(
                "Got non-bool return values from checks in %s: %s",
                self.__call__.__name__,
                ", ".join(map(lambda c: self.checks[c].__name__, faulty_checks)),
            )
        return all(results)

    async def __call__(self, *args: typing.Any) -> None:
        if (await self.process_checks(*args)) is False:
            return
        assert (handler := self.event_handler) is not None
        finalargs: tuple[typing.Any, ...] = tuple()
        if self.__parent_identity__ == "-":
            finalargs = args
        elif self.__parent_identity__ == "bot_class":
            finalargs = (handler.client,) + args
        elif self.__parent_identity__ == "event_handler_class":
            finalargs = (handler,) + args
        self.trigger_count += 1
        await self.callback(*finalargs)


class _InClassEventContainer:
    __identity__: str
    __internal_listeners__: dict[Event, list[EventListener]] = {}

    def __new__(cls: type[_InClassEventContainer], *args: typing.Any, **kwargs: typing.Any) -> _InClassEventContainer:
        inst = super().__new__(
            cls,
        )
        for _type in inst.__class__.__mro__:
            for item in _type.__dict__.values():
                if isinstance(item, EventListener):
                    inst.__internal_listeners__.setdefault(item.event_type, []).append(item)
                    item.__parent_identity__ = cls.__identity__
        return inst


class EventHandler(_InClassEventContainer):
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

    listeners: dict[Event, list[EventListener]] = {}
    __identity__: str = "event_handler_class"  # this is meant for callback signature verification, don't override.

    def __init__(self, client: "GatewayClient") -> None:
        self.client = client

    def setup_listeners(self) -> None:
        [[self.add_listener(listener) for listener in listeners] for listeners in self.__internal_listeners__.values()]

    def add_listener(self, event_listener: EventListener) -> EventListener:
        """Adds a listener to the handler.

        Parameters
        ----------
        event_listener: wyvern.events.EventListener
            The listener to be added.
        """
        self.listeners.setdefault(event_listener.event_type, []).append(event_listener)
        event_listener.event_handler = self
        return event_listener

    def dispatch(self, event: Event, *args: typing.Any) -> None:
        """Dispatches events from the gateway.
        This method runs all the listeners registered in the container
        for the specific event.

        Parameters
        ----------
        event: wyvern.events.Event
            Name of the event to be dispatched.
        *args: tuple[typing.Any, ...]
            Arguments to provide in callbacks.
        """
        self.client._logger.debug(f"Dispatching {event} event.")

        invokes = [lsnr(*args) for lsnr in self.listeners.get(event, []) if lsnr.max_trigger > lsnr.trigger_count]
        asyncio.gather(*invokes)


def as_listener(
    event: Event, *, max_trigger: int | float = float("inf")
) -> typing.Callable[[typing.Callable[..., typing.Awaitable[typing.Any]]], EventListener]:
    """Creates a [wyvern.events.EventListener][] object.

    Parameters
    ----------
    event: wyvern.events.Event
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
