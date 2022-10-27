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

from wyvern.exceptions import Unauthorized
from wyvern.gateway import Gateway
from wyvern.intents import Intents
from wyvern.rest import RESTClient

if typing.TYPE_CHECKING:
    import aiohttp

_LOGGER = logging.getLogger("wyvern")


class GatewayClient:
    def __init__(
        self, token: str, intents: typing.SupportsInt | Intents, rest_client: RESTClient | None = None
    ) -> None:

        self.rest = rest_client or RESTClient(client=self, token=token)
        self.intents = intents if isinstance(intents, Intents) else Intents(int(intents))
        self.gateway = Gateway(self)

    async def start(self) -> None:
        """Connects the bot with gateway and starts listening to events."""
        try:
            await self.gateway._get_socket_ready()
            _LOGGER.debug("Logging in with static token.")
            try:
                res = await self.rest.fetch_client_user()
            except Unauthorized as e:
                await self.rest._session.close()
                raise e
            await self.gateway.listen_gateway()
        except KeyboardInterrupt:
            print("yo")

    def run(self) -> None:
        """A non-async method which call ``GatewayClient.start``."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start())
