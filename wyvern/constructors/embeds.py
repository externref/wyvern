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

import datetime
import typing

import attrs

__all__: tuple[str, ...] = ("EmbedAuthor", "EmbedFooter", "EmbedField", "Embed", "EmbedConstructor")


@typing.final
@attrs.define(slots=True)
class EmbedAuthor:
    """Represents an embed author."""

    name: str
    """Name of the author."""
    url: str | None = None
    """URL that the author points to."""
    icon_url: str | None = None
    """URL of the author icon"""
    proxy_icon_url: str | None = None
    """Proxy URL of icon."""

    def to_payload(self) -> dict[str, str | None]:
        """Converts the author to its payload."""
        return {"name": self.name, "url": self.url, "icon_url": self.icon_url}


@typing.final
@attrs.define(slots=True)
class EmbedFooter:
    """Represents an embed footer"""

    text: str
    """The text in the footer."""
    icon_url: str | None = None
    """URL of the footer icon."""
    proxy_icon_url: str | None = None
    """Proxy URL of the icon"""

    def to_payload(self) -> dict[str, str | None]:
        """Converts the footer to its payload."""
        return {"text": self.text, "icon_url": self.icon_url}


@typing.final
@attrs.define(slots=True)
class EmbedField:
    """Represnts an embed field."""

    name: str
    """Name of the field."""
    value: str
    """Value of the field."""
    inline: bool = True
    """Inline value for the file, defaults to True."""

    def to_payload(self) -> dict[str, str | bool]:
        return {"name": self.name, "value": self.value, "inline": self.inline}


class EmbedConstructor:
    """
    Creates an sendable discord embed.

    Parameters
    ----------

    title : str
        Name of the embed.
    description : str
        Description of the embed
    color : int
        Color of the embed.
    url : str
        URL which the title points to.
    timestamp : datetime.datetime
        Timestamp to put in the embed.

    """

    __slots__: tuple[str, ...] = ("_payload",)

    def __init__(
        self,
        *,
        title: str | None = None,
        description: str | None = None,
        color: int = 0,
        colour: int = 0,
        url: str | None = None,
        timestamp: datetime.datetime | None = None,
    ) -> None:

        self._payload: dict[str, typing.Any] = {
            "type": "rich",
            "fields": [],
            "title": title,
            "description": description,
            "color": color or colour,
            "url": url,
            "timestamp": timestamp,
        }

    def add_field(self, *, name: str, value: str, inline: bool = True) -> "EmbedConstructor":
        """Adds a field to the embed.

        Parameters
        ----------

        name: str
            Name of the field.
        value: str
            Value of the filed
        inline: bool
            Weather the field is inline or not, defaults to [True][]

        Returns
        -------

        wyvern.constructors.embeds.EmbedConstructor
            The constructor.
        """
        field = EmbedField(name, value, inline)
        self._payload["fields"].append(field.to_payload())
        return self

    def set_author(self, *, name: str, url: str, icon_url: str | None = None) -> "EmbedConstructor":
        """
        Set's the author for the embed.

        Parameters
        ----------

        name: str
            Name of the author field.
        url: str
            The URL author points to.
        icon_url: str
            URL for image to embed in the author.

        Returns
        -------

        wyvern.constructors.embeds.EmbedConstructor
            The constructor.
        """
        author = EmbedAuthor(name, url, icon_url)
        self._payload["author"] = author.to_payload()
        return self

    def set_footer(self, *, text: str, icon_url: str | None = None) -> "EmbedConstructor":
        """
        Set's the footer for the embed.

        Parameters
        ----------

        text: str
            The text to appear in the footer
        icon_url: str
            URL for image to embed in the footer.

        Returns
        -------

        wyvern.constructors.embeds.EmbedConstructor
            The constructor.
        """
        footer = EmbedFooter(text, icon_url)
        self._payload["footer"] = footer.to_payload()
        return self

    def edit_init(
        self,
        *,
        title: str | None = None,
        description: str | None = None,
        color: int = 0,
        colour: int = 0,
        url: str | None = None,
        timestamp: datetime.datetime | None = None,
    ) -> "EmbedConstructor":
        self._payload["title"] = title or self._payload.get("title")
        self._payload["description"] = description or self._payload.get("description")
        self._payload["color"] = color or colour or self._payload.get("color")
        self._payload["url"] = url or self._payload.get("url")
        self._payload["timestamp"] = timestamp or self._payload.get("timestamp")
        return self

    def build(self) -> "Embed":
        return Embed(
            payload=self._payload,
            title=self._payload.get("title"),
            description=self._payload.get("description"),
            url=self._payload.get("url"),
            color=self._payload.get("color", 0),
            fields=[EmbedField(**kargs.to_payload()) for kargs in self._payload.get("fields", [])],
            author=self._payload.get("author"),
            footer=self._payload.get("footer"),
        )


@typing.final
@attrs.define(slots=True, kw_only=True, eq=True, repr=True)
class Embed:
    """
    Read-only Embed class returned while parsing message objects.
    To create a sendable embed, use [wyvern.constructors.embeds.EmbedConstructor][] instead.
    """

    payload: dict[str, typing.Any]
    """The raw payload."""
    title: str | None = None
    """Title of the embed."""
    description: str | None = None
    """Description fo the embed"""
    url: str | None = None
    """URL of the embed"""
    color: int = 0
    """Color of the embed."""
    timestamp: datetime.datetime | None = None
    """Timestamp of the embed."""
    colour = color
    """Alias for color."""
    fields: list[EmbedField] = []
    """List of fields related to this embed."""
    author: EmbedAuthor | None = None
    """Author of the embed."""
    footer: EmbedFooter | None = None
    """Footer of the embed."""

    def to_constructor(self) -> EmbedConstructor:
        embed = EmbedConstructor()
        embed._payload = self.payload
        return embed
