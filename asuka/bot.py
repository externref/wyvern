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

import logging
import typing

import aiohttp

from asuka.builders import Intents
from asuka.event_handler import EventHandler
from asuka.events.base_events import GatewayEvent
from asuka.gateway.gateway import Gateway
from asuka.rest.client import RESTClient

_LOGGER = logging.getLogger(__name__)


class Bot:
    def __init__(
        self,
        token: str,
        intents: Intents | typing.SupportsInt | None = None,
        client_session: aiohttp.ClientSession | None = None,
        api_version: int = 10,
    ) -> None:
        self._rest = RESTClient(
            token=token, api_version=api_version, client_session=client_session
        )
        self._gateway = Gateway(self)
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
    def gateway(self) -> Gateway:
        return self._gateway

    @property
    def event_handler(self) -> EventHandler:
        return self._event_handler

    def listen(self, event: typing.Type[GatewayEvent] | None = None) -> typing.Callable:
        def inner(callback: typing.Callable) -> typing.Callable:
            nonlocal event
            if event is None:
                event = list(callback.__annotations__.values())[0]
            self._event_handler.add_listener(event, callback)
            return callback

        return inner

    def listen_once(
        self, event: typing.Type[GatewayEvent] | None = None
    ) -> typing.Callable:
        def inner(callback: typing.Callable) -> typing.Callable:
            nonlocal event
            if event is None:
                event = list(callback.__annotations__.values())[0]
            self._event_handler.add_once_listener(event, callback)
            return callback

        return inner

    async def start(self) -> None:
        self._event_handler.bot = self
        if getattr(self._rest, "_session", None) is None:
            await self._rest._create_session()

        await self._gateway._get_socket_ready()
        await self._gateway.listen_gateway()
