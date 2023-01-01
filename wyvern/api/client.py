from __future__ import annotations

import typing

import aiohttp

from wyvern.api.gateway import GatewayImpl
from wyvern.api.intents import Intents
from wyvern.api.rest_client import RESTClientImpl

__all__: tuple[str, ...] = ("GatewayClient",)


class GatewayClient:
    aentered: bool = False

    def __init__(
        self, token: str, *, api_version: int = 10, intents: typing.SupportsInt | Intents = Intents.UNPRIVILEGED
    ) -> None:
        self.intents = Intents(int(intents))
        self.rest = RESTClientImpl(token=token, client=self, api_version=api_version)
        self.gateway = GatewayImpl(self)

    async def __aenter__(self) -> None:
        self.rest.client_session = aiohttp.ClientSession()
        self.aentered = True

    async def __aexit__(self, *args: typing.Any) -> None:
        ...

    async def start(self) -> None:
        if not self.aentered:
            async with self:
                ...
        await self.gateway.connect()
