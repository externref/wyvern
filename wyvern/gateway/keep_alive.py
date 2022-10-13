import asyncio
import time
import typing

from .enums import GatewayEvents

if typing.TYPE_CHECKING:
    from .gateway import Gateway


class KeepAlive:
    counter: int = 0
    interval: float

    async def start(self, gateway: "Gateway") -> None:
        while True:
            await gateway.socket.send_json(self.get_beat)
            self.interval = time.perf_counter()
            await asyncio.sleep(gateway.heartbeat_interval)

    @property
    def get_beat(self) -> dict[str, int | float]:
        return {"op": GatewayEvents.HEARTBEAT, "d": self.counter}
