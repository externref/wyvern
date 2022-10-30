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
import logging
import typing

from wyvern.events import Event, EventHandler, EventListener, listener
from wyvern.exceptions import Unauthorized
from wyvern.gateway import Gateway
from wyvern.intents import Intents
from wyvern.rest import RESTClient

if typing.TYPE_CHECKING:
    import aiohttp

_LOGGER = logging.getLogger("wyvern")


class GatewayClient:
    """The main bot class which acts as an interface between the Discord API and your bot.

    Parameters
    ----------

    token : str
        The bot token to use.
    intents : typing.SupportsInt | wyvern.intents.Intents
        The intents to use while logging in to the gateway.
    event_handler type[EventHandler]
        A EventHandler subclass ( not instance ), if any.
    rest_client : RESTClient | None
        A custom RESTClient subclass to use, if any.
    api_version : int
        Discord API version to use.
    client_session : aiohttp.ClientSession | None
        ClientSession subclass to use, if any.

    """

    def __init__(
        self,
        token: str,
        *,
        intents: typing.SupportsInt | Intents = Intents.UNPRIVILEGED,
        event_handler: type[EventHandler] = EventHandler,
        rest_client: RESTClient | None = None,
        api_version: int = 10,
        client_session: "aiohttp.ClientSession" | None = None,
    ) -> None:
        self.event_handler = event_handler(self)
        self.rest = rest_client or RESTClient(
            client=self, token=token, api_version=api_version, client_session=client_session
        )
        self.intents = intents if isinstance(intents, Intents) else Intents(int(intents))
        self.gateway = Gateway(self)

    def listener(
        self, event: str | Event, *, max_trigger: int | float = float("inf")
    ) -> typing.Callable[[typing.Callable[..., typing.Awaitable[typing.Any]]], EventListener]:
        """
        Creates and adds a new listenet to the client's event handler.

        Parameters
        ----------

        event: str | wyvern.events.Event
            The event to listen.
        max_trigger: int | float
            Maximum number of times this listener has to be triggered.

        Returns
        -------

        wyvern.events.EventListener
            A EventListener object.

        """

        def inner(callback: typing.Callable[..., typing.Awaitable[typing.Any]]) -> EventListener:
            lsnr = listener(event, max_trigger=max_trigger)(callback)
            self.event_handler.add_listener(lsnr)
            return lsnr

        return inner

    async def start(self) -> None:
        """Connects the bot with gateway and starts listening to events."""

        await self.gateway._get_socket_ready()
        _LOGGER.debug("Logging in with static token.")
        try:
            await self.rest.fetch_client_user()
            await self.gateway.listen_gateway()
        except Unauthorized as e:
            await self.rest._session.close()
            raise e

    def run(self) -> None:
        """A non-async method which call [wyvern.client.GatewayClient.start][]."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start())
