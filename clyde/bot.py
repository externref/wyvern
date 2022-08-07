import typing

from clyde.builders import Intents
from clyde.events.event_handler import EventHandler
from clyde.rest.client import RESTClient
from clyde.websocket.ws import DiscordWebSocket


class Bot:
    def __init__(
        self, token: str, intents: Intents | typing.SupportsInt | None = None
    ) -> None:
        self._rest = RESTClient(token)
        self._websocket = DiscordWebSocket(self)
        self._event_handler = EventHandler()
        self._intents = (
            intents
            if isinstance(intents, Intents)
            else Intents.from_value(int(intents or 98045))
        )

    @property
    def intents(self) -> Intents:
        return self._intents

    @property
    def rest(self) -> RESTClient:
        return self._rest

    @property
    def websocket(self) -> DiscordWebSocket:
        return self._websocket

    async def start(self) -> None:
        self._event_handler.bot = self
        await self._rest._create_session()
        await self._websocket._get_socket_ready()
        await self._websocket.listen_gateway()
