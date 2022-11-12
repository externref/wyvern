from __future__ import annotations

import enum
import typing

import attrs

if typing.TYPE_CHECKING:
    from wyvern.clients import GatewayClient
    from wyvern.models.base import Snowflake


class AvatarType(enum.Flag):
    GUILD = "GUILD"
    CUSTOM = "CUSTOM"
    DEFAULT = "DEFAULT"


class BaseAsset:
    _client: "GatewayClient"
    hash: str

    def __str__(self) -> str:
        return self.url

    @property
    def url(self) -> str:
        return f"https://cdn.discordapp.com/{self.hash}.png"

    async def read(self) -> bytes:
        res = await self._client.rest._session.get(self.url)
        return await res.read()


@attrs.define(kw_only=True, slots=True, repr=True)
class Avatar(BaseAsset):
    _client: "GatewayClient"
    type: AvatarType
    hash: str


@attrs.define(kw_only=True, slots=True, repr=True)
class GuildIcon(BaseAsset):
    ...


@attrs.define(kw_only=True, slots=True, repr=True)
class Attachment:
    _client: "GatewayClient"
    id: "Snowflake"
    filename: str
    description: str | None
    content_type: str | None
    size: int
    proxy_url: str
    height: int | None
    width: int | None
    is_ephemeral: bool | None

    @property
    def is_spoiler(self) -> bool:
        return True if self.filename.startswith("SPOILER_") else False

    @classmethod
    def _from_payload(
        cls: type["Attachment"], client: "GatewayClient", sfc: type["Snowflake"], data: dict[str, typing.Any]
    ) -> "Attachment":
        return cls(
            client=client,
            id=sfc.create(data["id"]),
            filename=data["filename"],
            description=data.get("description"),
            content_type=data.get("content_type"),
            size=data["size"],
            proxy_url=data["proxy_url"],
            height=data.get("height"),
            width=data.get("width"),
            is_ephemeral=data.get("ephemeral"),
        )
