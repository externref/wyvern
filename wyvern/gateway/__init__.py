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
import sys
import time
import typing

import aiohttp

from wyvern.events import Event
from wyvern.interactions import _converters as inter_convertors
from wyvern.models import _converters
from wyvern.presences import Activity, Status

from .enums import WSEventEnums
from .keep_alive import KeepAlive

if typing.TYPE_CHECKING:
    from wyvern.clients import GatewayClient


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
        "is_connected",
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

    async def update_presence(self, status: Status | None = None, activity: Activity | None = None) -> None:
        payload: dict[str, typing.Any] = {
            "op": WSEventEnums.PRESECNE_UPDATE.value,
            "d": {
                "since": int(datetime.datetime.now().timestamp()),
                "afk": False,
                "status": status.value if status else "online",
                "activities": [activity.to_event_payload()] if activity else [],
            },
        }

        await self.socket.send_json(payload)

    async def update_voice_state(
        self, guild_id: int, channel_id: int, /, *, self_mute: bool = False, self_deaf: bool = False
    ) -> None:
        payload: dict[str, typing.Any] = {
            "op": WSEventEnums.VOICE_STATE_UPDATE.value,
            "d": {"guild_id": guild_id, "channel_id": channel_id, "self_mute": self_mute, "self_deaf": self_deaf},
        }
        await self.socket.send_json(payload)

    @property
    def identify_payload(self) -> dict[str, typing.Any]:
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
        self._client._logger.debug("Starting listening to gateway.")
        async for message in self.socket:  # type: ignore
            if self.is_connected is False:
                self.is_connected = True
                self._client.event_handler.dispatch(Event("GATEWAY_CONNECTED"), self._client)

            if message.type == aiohttp.WSMsgType.TEXT:  # type: ignore
                await self._parse_payload_response(json.loads(message.data))  # type: ignore
            elif message.type == aiohttp.WSMsgType.ERROR:  # type: ignore
                "error from the gateway!"

    async def _get_socket_ready(self) -> None:
        self._socket = await self._client.rest._create_websocket()

    async def _hello_res(self, d: dict[str, typing.Any]) -> None:
        self._client._logger.debug("Sending identify payload.")
        await self.socket.send_json(self.identify_payload)
        self._heartbeat_interval = d["heartbeat_interval"] / 1000
        loop = asyncio.get_event_loop()
        loop.create_task(self.keep_alive.start(self))

    async def _dispatch_events(self, payload: dict[str, typing.Any]) -> None:
        try:
            event = Event(t := payload["t"])
        except ValueError:
            return
        if event is Event.MESSAGE_CREATE:
            self._client.event_handler.dispatch(event, _converters.payload_to_message(self._client, payload["d"]))
        elif event is event.INTERACTION_CREATE:
            self._client.event_handler.dispatch(
                event, inter_convertors.payload_to_interaction(self._client, payload["d"])
            )
        elif t == "GUILD_CREATE":
            self._client.event_handler.dispatch(event, payload)
            self._populate_guild_cache(payload["d"])

    async def _parse_payload_response(self, payload: dict[str, typing.Any]) -> None:
        op, s, d = payload["op"], payload["s"], payload["d"]
        if op == WSEventEnums.HEARTBEAT_ACK:
            self._latency = time.perf_counter() - self.keep_alive.last_heartbeat
            return

        if op == WSEventEnums.HELLO:
            await self._hello_res(d)

        elif op == WSEventEnums.DISPATCH:
            self.keep_alive.sequence = s
            await self._dispatch_events(payload)

    def _populate_guild_cache(self, payload: dict[str, typing.Any]) -> None:
        [
            self._client.members.add_member(_converters.payload_to_member(self._client, payload["id"], member))
            for member in payload["members"]
        ]
        self._client.members.update_user_state()
