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

import dataclasses
import typing

import aiohttp
import multidict

from asuka.exceptions import HTTPException, get_exception
from asuka.models.users import BotUser


@dataclasses.dataclass
class RequestRoute:
    url: str
    type: str

    def __init__(self, *, type: str = "GET", url: str, api_version=10) -> None:
        self.url = f"https://discord.com/api/v{api_version}/{url}"
        self.type = type


class RESTClient:
    def __init__(
        self,
        *,
        token: str,
        api_version: int = 10,
        client_session: aiohttp.ClientSession | None = None,
    ) -> None:
        if client_session is not None:
            self._session = client_session
        self._token = token
        self._api_version = api_version
        self._headers: typing.Dict[str, multidict.istr] = {
            "Authorization": multidict.istr(f"Bot {token}")
        }

    async def _create_session(self) -> None:
        self._session = aiohttp.ClientSession(headers=self._headers)

    async def _create_websocket(self) -> aiohttp.ClientWebSocketResponse:
        return await self._session.ws_connect(
            f"wss://gateway.discord.gg/?v={self._api_version}&encoding=json"
        )

    async def request(self, route: RequestRoute) -> typing.Any:
        headers = self._headers.copy()
        headers["Content-Type"] = multidict.istr("application/json")
        res = await self._session.request(route.type, route.url, headers=headers)
        if res.status in (200, 201):
            return await res.json()
        if res.status in (204, 304):
            return
        else:
            raise HTTPException.with_code(res.status, "Failed Request.")

    async def fetch_bot_user(self) -> BotUser:
        try:
            res = await self.request(RequestRoute(url="users/@me"))
        except Exception as e:
            if isinstance(e, HTTPException) and e.code is not None:
                raise get_exception(e.code)("Improper token was passed.")
        return BotUser(res)
