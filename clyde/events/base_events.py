import typing

if typing.TYPE_CHECKING:
    from clyde.bot import Bot


class GatewayEvent:
    bot: "Bot"

    def __init__(
        self, bot: "Bot", payload: typing.Dict[typing.Any, typing.Any] | None = None
    ) -> None:
        self._payload_data = payload or {}
        self.bot = bot
