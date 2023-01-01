from __future__ import annotations

import typing

import attrs

from wyvern.utils.consts import UNDEFINED, Undefined

if typing.TYPE_CHECKING:
    import aiohttp

    from wyvern.api.bot import Bot

__all__: tuple[str, ...] = ("RESTClient",)


@attrs.define(kw_only=True)
class RESTClient:
    token: str
    bot: Bot
    api_version: int
    client_session: aiohttp.ClientSession | Undefined = UNDEFINED
