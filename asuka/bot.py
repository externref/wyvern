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
import datetime
import logging
import sys
import typing

import aiohttp

from asuka.builders import Intents
from asuka.event_handler import EventHandler, Listener
from asuka.events.base_events import Event
from asuka.exceptions import Unauthorized
from asuka.gateway.gateway import Gateway
from asuka.models.users import BotUser
from asuka.rest.client import RESTClient

__version__ = "0.0.1"

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

logging.basicConfig(format=f"{datetime.datetime.now()} [%(levelname)s]: %(message)s")


class Bot:
    """The bot class used to connect with Discord API and interaction
    using the Discord Websocket and REST api.

    Parameters
    ----------

        token: :class:`str`
            The bot token to use.
        intents: :class:`Union[Intents, SupportsInt, None]`
            Intents to enable for the bot.
            An Intent object, or value can be passed here.
        log_self_info :class:`bool`
            Log basic info while logging-in.
        client_session: :class:`Optional[ClientSession]`.
            A custom ClientSession, if any.
        api_version: :class:`int`
            The Discord API version to use, defaults to 10.
        description: :class:`str`
            Description about the bot, can be accessed using `Bot.description`.

    Attributes
    ----------

        description: :class:`str`
            The bot description set by user in the code.

    """

    description: str

    def __init__(
        self,
        token: str,
        *,
        intents: Intents | typing.SupportsInt | None = None,
        log_self_info: bool = True,
        client_session: aiohttp.ClientSession | None = None,
        api_version: int = 10,
        description: typing.Any = "No description Provided",
    ) -> None:
        self.description = description
        self._boot_log = log_self_info
        self._rest = RESTClient(bot=self, token=token, api_version=api_version, client_session=client_session)
        self._gateway = Gateway(self)
        self._event_handler = EventHandler()

        self._event_handler.bot = self
        self._intents = intents if isinstance(intents, Intents) else Intents.from_value(int(intents or 98045))

    @property
    def intents(self) -> Intents:
        """Intents being used by the bot."""
        return self._intents

    @property
    def rest(self) -> RESTClient:
        """The RESTClient bot is binded with."""
        return self._rest

    @property
    def gateway(self) -> Gateway:
        """Gateway connection handler."""
        return self._gateway

    @property
    def event_handler(self) -> EventHandler:
        """An event handler which dispatches and manage gateway and other events"""
        return self._event_handler

    @property
    def user(self) -> BotUser:
        ...

    def listener(
        self, event: typing.Type[Event] | None = None
    ) -> typing.Callable[[typing.Callable[..., typing.Any]], Listener]:
        """This decorator is used to add an event listener to the bot.
        To create a listener, you can pass the event type in this decorator, or
        optionally annotated the first argument of the function with the event.

        !!! NOTE
            The callback should take exactly one parameter.

        Parameters
        ----------

            event: :class:`Type[.Event]`
                The gateway event to listen to.

        Example
        -------

            >>> import os
            >>>
            >>> import asuka
            >>>
            >>> bot = asuka.Bot(os.getenv('TOKEN'))
            >>>
            >>> @bot.listener(asuka.MessageCreate)
            >>> async def hello(event: asuka.MessageCreate) -> None:
            >>>     print(f"Message sent by {event.user.username}")
            >>>
            >>> bot.run()

        """

        def inner(callback: typing.Callable) -> Listener:
            nonlocal event
            if event is None:
                event = list(callback.__annotations__.values())[0]
            self._event_handler.add_listener(event, lsnr := Listener(callback))
            return lsnr

        return inner

    def listen_once(
        self, event: typing.Type[Event] | None = None
    ) -> typing.Callable[[typing.Callable[..., typing.Any]], Listener]:
        """Same as the .listener() decorator, but gets triggered only once in the complete runtime."""

        def inner(callback: typing.Callable) -> Listener:
            nonlocal event
            if event is None:
                event = list(callback.__annotations__.values())[0]
            self._event_handler.add_once_listener(event, lsnr := Listener(callback))
            return lsnr

        return inner

    async def start(self) -> None:
        """Connects the bot with gateway and starts listening to events."""

        await self._gateway._get_socket_ready()
        try:
            res = await self._rest.fetch_bot_user()
            if self._boot_log is True:
                self._log_self_info(res)
        except Unauthorized as e:
            await self._rest._session.close()
            raise e
        await self._gateway.listen_gateway()

    def run(self) -> None:
        """A non-async method which call ``Bot.start``."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start())

    def _log_self_info(self, user: BotUser) -> None:
        _LOGGER.info(f"Logged in as: {user}")
        _LOGGER.info(f"Asuka Version: {__version__} | Python Version: {sys.version}")
        _LOGGER.info(f"Bot Description: {self.description}")
