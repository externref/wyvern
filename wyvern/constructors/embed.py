from __future__ import annotations

import dataclasses
import datetime
import typing


@dataclasses.dataclass
class EmbedAuthor:
    name: str
    url: str | None = None
    icon_url: str | None = None
    proxy_icon_url: str | None = None

    def to_payload(self) -> dict[str, str | None]:
        return {"name": self.name, "url": self.url, "icon_url": self.icon_url}


@dataclasses.dataclass
class EmbedFooter:
    text: str
    icon_url: str | None = None
    proxy_icon_url: str | None = None

    def to_payload(self) -> dict[str, str | None]:
        print("aaa")
        return {"text": self.text, "icon_url": self.icon_url}


@dataclasses.dataclass
class EmbedField:
    name: str
    value: str
    inline: bool = True

    def to_payload(self) -> dict[str, str | bool]:
        return {"name": self.name, "value": self.value, "inline": self.inline}


class EmbedConstructor:
    """
    Creates an sendable disocrd embed.

    Parameters
    ----------

    name : str
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

    _payload: dict[str, typing.Any] = {"type": "rich", "fields": []}
    _title: str | None = None
    _description: str | None = None
    _color: int = 0
    _url: str | None = None
    _timestamp: datetime.datetime | None = None

    def __init__(
        self,
        *,
        title: str | None = None,
        description: str | None = None,
        color: int = 0,
        url: str | None = None,
        timestamp: datetime.datetime | None = None,
    ) -> None:
        self._payload["title"] = title
        self._payload["description"] = description
        self._payload["color"] = color
        self._payload["url"] = url
        self._payload["timestamp"] = timestamp

    @property
    def title(self) -> str | None:
        """Title of the embed."""
        return self._payload.get("title")

    @property
    def description(self) -> str | None:
        """Description of the embed."""
        return self._payload.get("description")

    @property
    def color(self) -> int:
        """Colour of the embed."""
        return self._payload.get("color", 0)

    @property
    def url(self) -> str | None:
        """Embed's URL."""
        return self._payload.get("url")

    @property
    def timestamp(self) -> datetime.datetime | None:
        """Timestamp of the embed."""
        return datetime.datetime.fromtimestamp(ts) if (ts := self._payload.get("timestamp")) else None

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

        wyvern.constructors.embed.EmbedConstructor
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

        wyvern.constructors.embed.EmbedConstructor
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

        wyvern.constructors.embed.EmbedConstructor
            The constructor.
        """
        footer = EmbedFooter(text, icon_url)
        self._payload["footer"] = footer.to_payload()
        return self


class Embed:
    ...
