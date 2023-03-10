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

import asyncio
import enum
import json
import sys
import time
import typing

import aiohttp

from wyvern.events import lib_events

if typing.TYPE_CHECKING:
    from wyvern.api.bot import GatewayBot

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
    bot: GatewayBot
    socket: aiohttp.ClientWebSocketResponse = attrs.field(init=False)
    latency: float = attrs.field(init=False, default=float("NaN"))
    heartbeat_interval: float = attrs.field(init=False, default=0)
    sequence: int = attrs.field(init=False, default=0)
    last_heartbeat: float = attrs.field(init=False, default=0)

    async def connect(self) -> None:
        self.bot.event_handler.dispatch(lib_events.StartingEvent(bot=self.bot))
        self.socket = await self.bot.rest.client_session.ws_connect(  # type: ignore
            f"wss://gateway.discord.gg/?v={self.bot.rest.api_version}&encoding=json"
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
                "token": self.bot.rest.token,
                "intents": self.bot.intents.value,
                "properties": {
                    "os": sys.platform,
                    "browser": "wyvern",
                    "device": "wyvern",
                },
            },
        }

    async def listen_gateway(self) -> None:
        user = await self.bot.rest.fetch_current_user()

        async for msg in self.socket:
            if self.heartbeat_interval == 0:
                self.bot.event_handler.dispatch(lib_events.StartedEvent(bot=self.bot, user=user))
            await self.process_gw_event(json.loads(msg.data))  # type: ignore
