import dataclasses
import typing

import aiohttp
import multidict

from wyvern.helpers import HTTPException
from wyvern.models import BaseUser


@dataclasses.dataclass
class RequestRoute:
    url: str
    type: str

    def __init__(self, *, method: str = "GET", url: str, api_version: int = 10) -> None:
        self.url = f"https://discord.com/api/v{api_version}/{url}"
        self.method = method


class RestClient:
    def __init__(self, token: str, *, api_version: int = 10, session: aiohttp.ClientSession | None = None) -> None:
        self.token = token
        self.api_version = api_version
        self.session = session or aiohttp.ClientSession()
        self.headers: dict[str, multidict.istr] = {"Authorization": multidict.istr(f"Bot {self.token}")}

    async def create_session(self) -> None:
        self.session = aiohttp.ClientSession(headers=self.headers)
        return None

    async def connect_ws(self) -> aiohttp.ClientWebSocketResponse:
        return await self.session.ws_connect(f"wss://gateway.discord.gg/?v={self.api_version}&encoding=json")

    async def _request(self, route: RequestRoute) -> typing.Any:
        headers = self.headers.copy()
        headers["Content-Type"] = multidict.istr("application/json")
        result = await self.session.request(route.method, route.url, headers=headers)
        match result.status:
            case 200:
                return await result.json()
            case 201:
                return await result.json()
            case 204:
                return None
            case 304:
                return None
            case _:
                raise HTTPException.from_code(result.status, await result.text())

    async def get_bot_user(self) -> BaseUser:
        try:
            return BaseUser(await self._request(RequestRoute(url="users/@me")))
        except Exception as e:
            if isinstance(e, HTTPException) and e.status_code == 401:
                raise HTTPException.from_code(e.status_code, "Invalid token provided.")
            raise e
