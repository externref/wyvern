from __future__ import annotations

import typing

import attrs

from wyvern.utils import UNDEFINED, Undefined

if typing.TYPE_CHECKING:
    import aiohttp

    from wyvern.api.client import GatewayClient


@attrs.define(kw_only=True)
class RESTClient:
    token: str
    client: GatewayClient
    api_version: int
    client_session: aiohttp.ClientSession | Undefined = UNDEFINED
