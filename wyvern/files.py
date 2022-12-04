from __future__ import annotations

import enum
import typing

import attrs

if typing.TYPE_CHECKING:
    from wyvern.clients import GatewayClient
    from wyvern.models.base import Snowflake


class AvatarType(enum.Flag):
    """Represents avatar type."""

    GUILD = "GUILD"
    """Guild avatar."""
    CUSTOM = "CUSTOM"
    """Global custom avatar."""
    DEFAULT = "DEFAULT"
    """Default discord avatar."""


class BaseAsset:
    _client: "GatewayClient" = attrs.field(kw_only=False)
    hash: str

    def __str__(self) -> str:
        return self.url

    @property
    def url(self) -> str:
        """Url of the asset."""
        return f"https://cdn.discordapp.com/{self.hash}.png"

    async def read(self) -> bytes:

        res = await self._client.rest._session.get(self.url)
        return await res.read()


@attrs.define(kw_only=True, slots=True, repr=True)
class Avatar(BaseAsset):
    """Represents an User's avatar."""

    _client: "GatewayClient"= attrs.field(kw_only=False)
    type: AvatarType
    """Type of avatar."""
    hash: str
    """Hash value of avatar."""


@attrs.define(kw_only=True, slots=True, repr=True)
class GuildIcon(BaseAsset):
    ...


@attrs.define(kw_only=True, slots=True, repr=True)
class Attachment(BaseAsset):
    """Represents a attachment in a message."""

    _client: "GatewayClient"= attrs.field(kw_only=False)
    id: "Snowflake"
    """ID of the attachment."""
    filename: str
    """Attachments' filename."""
    description: str | None
    """Description, if any."""
    content_type: str | None
    """Type of the attachment."""
    size: int
    """Size of the attachment"""
    proxy_url: str
    """Proxy url of attachment"""
    height: int | None
    """Height of image."""
    width: int | None
    """Width of image."""
    is_ephemeral: bool | None
    """True if the attachement was ephemeral."""

    @property
    def is_spoiler(self) -> bool:
        """True if the attachment was spoiler enabled."""
        return True if self.filename.startswith("SPOILER_") else False

    @classmethod
    def _from_payload(
        cls: type["Attachment"], client: "GatewayClient", sfc: type["Snowflake"], data: dict[str, typing.Any]
    ) -> "Attachment":
        return cls(
            client,
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
