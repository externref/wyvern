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
    client: "GatewayClient"
    hash: str

    def __str__(self) -> str:
        return self.url

    @property
    def url(self) -> str:
        """Url of the asset."""
        return f"https://cdn.discordapp.com/{self.hash}.png"

    async def read(self) -> bytes:

        res = await self.client.rest._session.get(self.url)
        return await res.read()


@attrs.define(kw_only=True, slots=True, repr=True)
class Avatar(BaseAsset):
    """Represents an User's avatar."""

    client: "GatewayClient"
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

    client: GatewayClient
    id: Snowflake
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
