# MIT License

# Copyright (c) 2023 Sarthak

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

import traceback
import typing

import aiohttp

from wyvern import logger, types
from wyvern.api.event_decos import ImplementsEventDecos
from wyvern.api.event_handler import EventHandler, EventListener
from wyvern.api.gateway import GatewayImpl
from wyvern.api.intents import Intents
from wyvern.api.rest_client import RESTClientImpl
from wyvern.events.base import Event
from wyvern.utils.consts import UNDEFINED, Undefined

__all__: tuple[str, ...] = ("GatewayBot",)


class GatewayBot(ImplementsEventDecos):
    """
    The main bot class that interacts with the discord API through both REST and gateway paths.

    Parameters
    ----------
    token: str
        The bot token to use while execution.
    api_version: int
        Discord API version in usage, defaults to 10.
    intents: typing.SupportsInt | Intents
        Library's :class:`Intents` builder or any object that returns the intent value when passed to :class:`int`

    Example
    -------
        .. highlight:: python
        .. code-block:: python

            import asyncio

            import wyvern

            bot = wyvern.GatewayBot(
                "BOT_TOKEN_HERE",
                intents=(
                    wyvern.Intents.GUILD_MEMBERS
                    | wyvern.Intents.GUILDS
                    | wyvern.Intents.GUILD_MESSAGES
                    | wyvern.Intents.DIRECT_MESSAGES
                ),
            )

            asyncio.run(bot.start())

    """

    def __init__(
        self, token: str, *, api_version: int = 10, intents: typing.SupportsInt | Intents = Intents.UNPRIVILEGED
    ) -> None:
        self.logger = logger.main_logger
        self.intents = Intents(int(intents))
        self.rest = RESTClientImpl(token=token, bot=self, api_version=api_version)
        self.gateway = GatewayImpl(self)
        self.event_handler = EventHandler(bot=self)

    async def __aenter__(self) -> None:
        self.rest.client_session = aiohttp.ClientSession()

    async def __aexit__(self, *args: typing.Any) -> None:
        await self.rest.client_session.close()  # type: ignore

    def listener(
        self, event: type[Event], *, max_trigger: int | Undefined = UNDEFINED
    ) -> typing.Callable[[types.EventListenerCallbackT], EventListener]:
        """Adds a listener to the bot's event handler

        Parameters
        ----------
        event : type[Event]
            Type of the event.
        max_trigger : int
            Maximum number of times this event should be triggered.

        Returns
        -------
        listener: EventListener
            The event listener that was constructed.
        """

        def decorator(callback: types.EventListenerCallbackT) -> EventListener:
            self.event_handler.add_listener(
                lsnr := EventListener(type=event, max_trigger=max_trigger, callback=callback, bot=self)
            )
            return lsnr

        return decorator

    async def start(self, raise_exception: bool = False) -> None:
        """|coro|

        Verifies the bot token and starts listening to the gateway.

        Parameters
        ----------
        raise_exception: bool
            Set to true if exceptions should be be raised at this entrypoint.

        Raises
        ------

        """
        try:
            await self.gateway.connect()
        except aiohttp.ClientResponseError as e:
            self.logger.error("".join(traceback.format_exception(e)))  # type: ignore
            self.logger.critical("Invalid token was passed to the GatewayBot constructor.")
            if raise_exception is True:
                raise e
        except AssertionError as e:
            self.logger.error("GatewayBot.start() should be used inside an async context manager. Example:")
            self.logger.error("async with bot:")
            self.logger.error("   await bot.start()")
            if raise_exception is True:
                raise e
