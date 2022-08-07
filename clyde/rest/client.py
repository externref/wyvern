import typing

import aiohttp
import multidict


class RESTClient:
    def __init__(self, token: str, api_version: int = 10) -> None:
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
