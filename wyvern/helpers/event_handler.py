import asyncio
import typing

from wyvern.events import BaseEvent

if typing.TYPE_CHECKING:
    from wyvern import Bot


class EventHandler:
    bot: "Bot"
    listeners: typing.Dict[typing.Type[BaseEvent], list[typing.Callable[[BaseEvent], typing.Any]]]
    one_time_listeners: typing.Dict[typing.Type[BaseEvent], list[typing.Callable[[BaseEvent], typing.Any]]]

    def add_listener(self, event: typing.Type[BaseEvent], callback: typing.Callable[[BaseEvent], typing.Any]) -> None:
        self.listeners.setdefault(event, self.listeners.get(event, [])).append(callback)
        return None

    def add_one_time_listener(
        self, event: typing.Type[BaseEvent], callback: typing.Callable[[BaseEvent], typing.Any]
    ) -> None:
        self.one_time_listeners.setdefault(event, self.one_time_listeners.get(event, [])).append(callback)
        return None

    def dispatch(self, event_type: typing.Type[BaseEvent], payload: dict[str, typing.Any]) -> None:
        event = event_type(self.bot, payload)
        tasks = [listener(event) for listener in self.listeners.get(event_type, [])]
        tasks += [listener(event) for listener in self.one_time_listeners.get(event_type, [])]
        self.one_time_listeners.pop(event_type, None)
        asyncio.gather(*tasks)
        return None
