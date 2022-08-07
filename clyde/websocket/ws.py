import asyncio
import json
import sys
import time
import typing

import aiohttp

from clyde import events

from .enums import WSEventEnums
from .keep_alive import KeepAlive

if typing.TYPE_CHECKING:
    from clyde.bot import Bot


class DiscordWebSocket:
    def __init__(self, bot: "Bot") -> None:
        self._bot = bot
        self._enums = WSEventEnums
        self._keep_alive = KeepAlive()
        self._latency: float = 0
        self._heartbeat_interval: float = 0
        self._socket: aiohttp.ClientWebSocketResponse

    @property
    def socket(self) -> aiohttp.ClientWebSocketResponse:
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
                "token": self._bot.rest._token,
                "intents": self._bot.intents.value,
                "properties": {
                    "$os": sys.platform,
                    "$browser": "clyde",
                    "$device": "clyde",
                },
            },
        }

    async def listen_gateway(self) -> None:
        async for message in self.socket:
            if message.type == aiohttp.WSMsgType.TEXT:
                await self._parse_payload_response(json.loads(message.data))

    async def _get_socket_ready(self) -> None:
        self._socket = await self._bot.rest._create_websocket()

    async def _hello_res(self, d: typing.Dict[str, typing.Any]) -> None:
        await self.socket.send_json(self.identify_payload)
        self._heartbeat_interval = d["heartbeat_interval"] / 1000
        loop = asyncio.get_event_loop()
        loop.create_task(self.keep_alive.start(self))

    async def _dispatch_events(self, payload: typing.Dict[str, typing.Any]) -> None:
        op, type, data = payload["op"], payload["t"], payload["d"]
        if type == "MESSAGE_CREATE":
            self._bot._event_handler.dispatch(events.MessageCreate, payload)
            return

    async def _parse_payload_response(
        self, payload: typing.Dict[str, typing.Any]
    ) -> None:
        op, t, d = payload["op"], payload["t"], payload["d"]
        if op == self._enums.HEARTBEAT_ACK:
            self._latency = time.perf_counter() - self.keep_alive.last_heartbeat
            return

        if op == self._enums.HELLO:
            await self._hello_res(d)

        elif op == self._enums.DISPATCH:
            self.keep_alive.sequence += 1
            await self._dispatch_events(payload)
