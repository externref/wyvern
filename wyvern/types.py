import typing

if typing.TYPE_CHECKING:
    from typing_extensions import TypeAlias

    from wyvern.events.base import Event

    AnyCallbackT: TypeAlias = typing.Callable[..., typing.Awaitable[typing.Any]]
    EventListenerCallbackT: TypeAlias = typing.Callable[[Event], typing.Awaitable[typing.Any]]
