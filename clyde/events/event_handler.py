import asyncio
import typing

from .base_events import GatewayEvent

if typing.TYPE_CHECKING:
    from clyde.bot import Bot


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
        self, event_type: typing.Any, payload: typing.Dict[typing.Any, typing.Any]
    ) -> None:
        event = event_type(self.bot, payload)
        to_call = []
        to_call.extend(
            [listener(event) for listener in self.listeners.get(event_type, [])]
        )
        for listener in self.once_listeners.get(event_type, []):
            to_call.append(listener(event))

        asyncio.gather(*to_call)
