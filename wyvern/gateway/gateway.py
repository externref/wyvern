import asyncio
import json
import sys
import time
import typing

import aiohttp

from wyvern.events import CreateMessage

from .enums import GatewayEvents
from .keep_alive import KeepAlive

if typing.TYPE_CHECKING:
    from wyvern import Bot


class Gateway:
    def __init__(self, bot: "Bot") -> None:
        self._bot = bot
        self._keep_alive = KeepAlive()
        self.latency: float = 0.0
        self.heartbeat_interval: float = 0.0
        self.socket: aiohttp.ClientWebSocketResponse

    @property
    def identify_payload(self) -> dict[str, typing.Any]:
        return {
            "op": GatewayEvents.IDENTIFY,
            "d": {
                "token": self._bot.client.token,
                "intents": self._bot.intents.value,
                "properties": {
                    "$os": sys.platform,
                    "$browser": "wyvern",
                    "$device": "wyvern",
                },
            },
        }

    async def listen_gateway(self) -> None:
        async for message in self.socket:
            if message.type == aiohttp.WSMsgType.TEXT:
                await self._parse_payload_response(json.loads(message.data))

    async def get_socket_ready(self) -> None:
        self.socket = await self._bot.client.connect_ws()
        return None

    async def _hello_res(self, d: typing.Dict[str, typing.Any]) -> None:
        await self.socket.send_json(self.identify_payload)
        self.heartbeat_interval = d["heartbeat_interval"] / 1000
        loop = asyncio.get_event_loop()
        loop.create_task(self._keep_alive.start(self))

    async def _dispatch_events(self, payload: typing.Dict[str, typing.Any]) -> None:
        if payload["op"] == "MESSAGE_CREATE":
            self._bot.event_handler.dispatch(CreateMessage, payload)
            return

    async def _parse_payload_response(self, payload: typing.Dict[str, typing.Any]) -> None:
        op, t, d = payload["op"], payload["t"], payload["d"]
        match op:
            case GatewayEvents.HELLO:
                await self._hello_res(d)
            case GatewayEvents.HEARTBEAT_ACK:
                self._latency = time.perf_counter() - self._keep_alive.interval
            case GatewayEvents.DISPATCH:
                await self._dispatch_events(payload)
            case _:
                pass
        return None
