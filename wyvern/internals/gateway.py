from __future__ import annotations

import asyncio
import enum
import json
import sys
import time
import typing

import aiohttp

if typing.TYPE_CHECKING:
    from wyvern.api.client import GatewayClient

import attrs


class OPCode(enum.IntEnum):
    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    PRESECNE_UPDATE = 3
    VOICE_STATE_UPDATE = 4
    RESUME = 6
    RECONNECT = 7
    REQUEST_GUILD_MEMBERS = 8
    INVALID_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11


@attrs.define
class Gateway:
    client: GatewayClient
    socket: aiohttp.ClientWebSocketResponse = attrs.field(init=False)
    latency: float = attrs.field(init=False, default=float("NaN"))
    heartbeat_interval: float = attrs.field(init=False, default=0)
    sequence: int = attrs.field(init=False, default=0)
    last_heartbeat: float = attrs.field(init=False, default=0)

    async def connect(self) -> None:
        self.socket = await self.client.rest.client_session.ws_connect(  # type: ignore
            f"wss://gateway.discord.gg/?v={self.client.rest.api_version}&encoding=json"
        )
        await self.listen_gateway()

    async def process_gw_event(self, payload: dict[str, typing.Any]) -> None:
        op = payload["op"]
        if op == OPCode.HELLO:
            await self.socket.send_json(self.identify_payload)
            self.heartbeat_interval = payload["d"]["heartbeat_interval"] / 1000
            asyncio.get_event_loop().create_task(self.keep_alive())
        if op == OPCode.HEARTBEAT_ACK:
            self.latency = time.perf_counter() - self.last_heartbeat

    async def keep_alive(self) -> None:
        while True:
            await self.socket.send_json({"op": OPCode.HEARTBEAT, "d": self.sequence})
            self.last_heartbeat = time.perf_counter()
            await asyncio.sleep(self.heartbeat_interval)

    @property
    def identify_payload(self) -> dict[str, typing.Any]:
        return {
            "op": 2,
            "d": {
                "token": self.client.rest.token,
                "intents": self.client.intents.value,
                "properties": {
                    "os": sys.platform,
                    "browser": "wyvern",
                    "device": "wyvern",
                },
            },
        }

    async def listen_gateway(self) -> None:
        async for msg in self.socket:
            print(msg)
            await self.process_gw_event(json.loads(msg.data))  # type: ignore
