import asyncio
import time
import typing

if typing.TYPE_CHECKING:
    from .ws import DiscordWebSocket


class KeepAlive:
    sequence: int = 0
    last_heartbeat: float

    async def start(self, ws: "DiscordWebSocket") -> None:
        while True:
            await ws.socket.send_json({"op": ws._enums.HEARTBEAT, "d": self.sequence})
            self.last_heartbeat = time.perf_counter()
            await asyncio.sleep(ws._heartbeat_interval)
