import typing

if typing.TYPE_CHECKING:
    from wyvern import Bot


class BaseEvent:
    def __init__(self, bot: "Bot", payload: dict[str, typing.Any] | None = None) -> None:
        self.bot = bot
        self._payload: dict[str, typing.Any] = payload or {}

    def __repr__(self) -> str:
        return f"BaseEvent(payload={self._payload})"

    @property
    def payload(self) -> dict[str, typing.Any]:
        return self._payload


class OnSocketOpen(BaseEvent):
    pass


class OnSocketClose(BaseEvent):
    pass
