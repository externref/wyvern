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

import dataclasses
import typing

import aiohttp
import multidict

from wyvern import models
from wyvern.exceptions import HTTPException, Unauthorized

from .endpoints import Endpoints

if typing.TYPE_CHECKING:
    from wyvern.client import GatewayClient
    from wyvern.constructors.embed import EmbedConstructor


@dataclasses.dataclass
class RequestRoute:
    _url: str
    api_version: int = 10
    type: str = "GET"
    json: dict[str, typing.Any] | None = None

    @property
    def url(self) -> str:
        return f"https://discord.com/api/v{self.api_version}/{self._url}"


__all__: tuple[str, ...] = ("RESTClient",)


class RESTClient:
    def __init__(
        self,
        *,
        client: "GatewayClient",
        token: str,
        api_version: int = 10,
        client_session: aiohttp.ClientSession | None = None,
    ) -> None:
        self._client = client
        self._session: aiohttp.ClientSession
        self._token = token
        self._api_version = api_version
        self._headers: typing.Dict[str, multidict.istr] = {"Authorization": multidict.istr(f"Bot {token}")}

        if client_session is not None:
            self._session = client_session

    async def _create_websocket(self) -> aiohttp.ClientWebSocketResponse:
        if getattr(self, "_session", None) is None:
            self._session = aiohttp.ClientSession(headers=self._headers)
        return await self._session.ws_connect(f"wss://gateway.discord.gg/?v={self._api_version}&encoding=json")

    async def request(self, route: RequestRoute) -> typing.Any:
        headers = self._headers.copy()
        headers["Content-Type"] = multidict.istr("application/json")
        res = await self._session.request(route.type, route.url, headers=headers, json=route.json)
        if res.status in (200, 201):
            return await res.json()
        if res.status in (204, 304):
            return
        else:
            raise HTTPException.with_code(res.status, await res.text())

    async def fetch_client_user(self) -> "models.BotUser":
        """
        Fetch's the bot's user object.

        Returns:
            BotUser object representating the bot's user.
        """
        try:
            res = await self.request(RequestRoute(Endpoints.fetch_client_user()))
            return models.converters.payload_to_botuser(self._client, res)
        except HTTPException as e:
            if e.code == 401:
                raise Unauthorized("Improper token passed.")
            raise e

    async def edit_client_user(self, username: str | None = None, avatar: bytes | None = None) -> "models.BotUser":
        payload: dict[str, bytes | str] = {}
        if username is not None:
            payload["username"] = username
        if avatar is not None:
            payload["avatar"] = avatar
        res: dict[str, int | str | bool] = await self.request(
            RequestRoute(Endpoints.fetch_client_user(), type="PATCH", json=payload)
        )
        return models.converters.payload_to_botuser(self._client, res)

    async def create_message(
        self,
        channel_id: int,
        content: str | None = None,
        *,
        embeds: typing.Sequence["EmbedConstructor"] = (),
        reference: int | models.MessageReference | None = None,
    ) -> "models.message.Message":
        payload: dict[str, typing.Any] = {"content": content, "embeds": []}
        [payload["embeds"].append(embed._payload) for embed in embeds]
        if reference is not None:
            if isinstance(reference, models.MessageReference):
                payload["message_reference"] = reference.to_payload()
            else:
                payload["message_reference"] = models.MessageReference(message_id=reference).to_payload()

        res: dict[str, typing.Any] = await self.request(
            RequestRoute(Endpoints.create_message(channel_id), type="POST", json=payload),
        )
        return models.converters.payload_to_message(self._client, res)
