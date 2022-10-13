import asyncio
import logging
import typing

import aiohttp

from wyvern.events import BaseEvent
from wyvern.gateway import Gateway
from wyvern.helpers import EventHandler, Intents, Unauthorized
from wyvern.models import BaseUser
from wyvern.rest import RestClient


class Bot:
    def __init__(
        self,
        token: str,
        *,
        intents: Intents | typing.SupportsInt | None = None,
        client: aiohttp.ClientSession | None = None,
        logger: logging.Logger | None = None,
        log: bool = True,
        api_version: int = 10,
        description: str = "No description provided.",
    ) -> None:
        self.event_handler = EventHandler()
        self.description = description
        self.intents = intents if isinstance(intents, Intents) else Intents.from_int(int(intents or 98045))
        self.logger = logger or logging.getLogger("wyvern")
        self.client = RestClient(token, api_version=api_version, session=client)
        self.gateway = Gateway(self)
        self.log = log

    def listener(
        self, event: typing.Type[BaseEvent] | None = None
    ) -> typing.Callable[[typing.Callable[..., typing.Any]], typing.Callable[..., typing.Any]]:
        def wrapper(callback: typing.Callable[[BaseEvent], typing.Any]) -> typing.Callable[[BaseEvent], typing.Any]:
            nonlocal event
            event = event or list(callback.__annotations__.values())[0]
            self.event_handler.add_listener(event, callback)
            return callback

        return wrapper

    def listen_once(
        self, event: typing.Type[BaseEvent] | None = None
    ) -> typing.Callable[[typing.Callable[..., typing.Any]], typing.Callable[..., typing.Any]]:
        def wrapper(callback: typing.Callable[[BaseEvent], typing.Any]) -> typing.Callable[[BaseEvent], typing.Any]:
            nonlocal event
            event = event or list(callback.__annotations__.values())[0]
            self.event_handler.add_one_time_listener(event, callback)
            return callback

        return wrapper

    async def start(self) -> None:
        self.event_handler.bot = self
        if getattr(self.client, "session", None) is None:
            await self.client.create_session()
        await self.gateway.get_socket_ready()
        try:
            res = await self.client.get_bot_user()
            if self.log:
                self._log_self_info(res)
        except Unauthorized:
            await self.client.session.close()
            raise Unauthorized
        await self.gateway.listen_gateway()

    def run(self) -> None:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start())

    def _log_self_info(self, user: BaseUser) -> None:
        self.logger.info(f"Logged in as {user.name}#{user.discriminator}")
        self.logger.info(f"Bot ID: {user.id}")
        self.logger.info(f"Intents: {self.intents}")
        self.logger.info(f"Description: {self.description}")
        return None
