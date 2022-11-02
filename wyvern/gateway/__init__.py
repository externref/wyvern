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
import json
import logging
import sys
import time
import typing

import aiohttp

from wyvern.models import converters
from wyvern.presences import Activity, Status

from .enums import WSEventEnums
from .keep_alive import KeepAlive

if typing.TYPE_CHECKING:
    from wyvern.clients import GatewayClient


_LOGGER = logging.getLogger("wyvern.api.gateway")


__all__: tuple[str, ...] = ("Gateway",)


class Gateway:
    __slots__: typing.Tuple[str, ...] = (
        "_client",
        "_keep_alive",
        "_latency",
        "_heartbeat_interval",
        "_socket",
        "_start_activity",
        "_start_status",
        "is_connected"
    )

    

    def __init__(self, client: "GatewayClient") -> None:
        self._start_activity: "Activity" | None = None
        self._start_status: "Status" | None = None
        self._client = client
        self._keep_alive = KeepAlive()
        self._latency: float = 0
        self._heartbeat_interval: float = 0
        self._socket: "aiohttp.ClientWebSocketResponse"
        self.is_connected: bool = False

    @property
    def socket(self) -> "aiohttp.ClientWebSocketResponse":
        return self._socket

    @property
    def keep_alive(self) -> KeepAlive:
        return self._keep_alive

    @property
    def latency(self) -> float:
        return self._latency

    @property
    def identify_payload(self) -> typing.Dict[str, typing.Any]:
        return {
            "op": 2,
            "d": {
                "token": self._client.rest._token,
                "intents": self._client.intents.value,
                "properties": {
                    "os": sys.platform,
                    "browser": "wyvern",
                    "device": "wyvern",
                },
                "presence": {
                    "since": int(datetime.datetime.now().timestamp()),
                    "activities": [ac.to_event_payload() if isinstance(ac := self._start_activity, Activity) else {}],
                    "status": self._start_status.value if self._start_status else None,
                    "afk": False,
                },
            },
        }

    async def listen_gateway(self) -> None:
        _LOGGER.debug("Starting listening to gateway.")
        async for message in self.socket:
            if self.is_connected is False:
                self.is_connected = True 
                self._client.event_handler.dispatch("GATEWAY_CONNECTED", self._client)
            if message.type == aiohttp.WSMsgType.TEXT:
                await self._parse_payload_response(json.loads(message.data))

    async def _get_socket_ready(self) -> None:
        self._socket = await self._client.rest._create_websocket()

    async def _hello_res(self, d: typing.Dict[str, typing.Any]) -> None:
        _LOGGER.debug("Sending identify payload.")
        await self.socket.send_json(self.identify_payload)
        self._heartbeat_interval = d["heartbeat_interval"] / 1000
        loop = asyncio.get_event_loop()
        loop.create_task(self.keep_alive.start(self))

    async def _dispatch_events(self, payload: typing.Dict[str, typing.Any]) -> None:
        if payload["t"] == "MESSAGE_CREATE":
            self._client.event_handler.dispatch(payload["t"], converters.payload_to_message(self._client, payload["d"]))

    async def _parse_payload_response(self, payload: typing.Dict[str, typing.Any]) -> None:
        op, t, d = payload["op"], payload["t"], payload["d"]
        if op == WSEventEnums.HEARTBEAT_ACK:
            self._latency = time.perf_counter() - self.keep_alive.last_heartbeat
            return

        if op == WSEventEnums.HELLO:
            await self._hello_res(d)

        elif op == WSEventEnums.DISPATCH:
            self.keep_alive.sequence += 1
            await self._dispatch_events(payload)
