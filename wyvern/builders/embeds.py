# MIT License

# Copyright (c) 2023 Sarthak

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
import enum
import json
import typing

import attrs

from wyvern.colors import Color
from wyvern.utils.consts import EMPTY, Empty

__all__: tuple[str, ...] = ("Embed", "EmbedType")


class EmbedType(enum.Enum):
    RICH = "rich"
    IMAGE = "image"
    VIDEO = "video"
    GIFV = "gifv"
    ARTICLE = "article"
    LINK = "link"


# from wyvern.logger import main_logger
@attrs.define(kw_only=True, slots=True)
class EmbedAuthor:
    name: str | Empty = EMPTY
    url: str | Empty = EMPTY
    icon_url: str | Empty = EMPTY
    proxy_icon_url: str | Empty = EMPTY

    def to_dict(self) -> dict[str, typing.Any]:
        return {
            "name": Empty.verify(self.name),
            "url": Empty.verify(self.url),
            "icon_url": Empty.verify(self.icon_url),
        }


@attrs.define(kw_only=True, slots=True)
class EmbedFooter:
    name: str | Empty = EMPTY
    icon_url: str | Empty = EMPTY
    proxy_icon_url: str | None = None

    def to_dict(self) -> dict[str, typing.Any]:
        return {
            "name": Empty.verify(self.name),
            "icon_url": Empty.verify(self.icon_url),
        }


@attrs.define(kw_only=True, slots=True)
class EmbedField:
    name: str
    value: str
    inline: bool = False

    def to_dict(self) -> dict[str, typing.Any]:
        return {
            "name": self.name,
            "value": self.value,
            "inline": self.inline,
        }


@attrs.define(kw_only=True, slots=True)
class _Media:
    url: str | None
    proxy_url: str | Empty = EMPTY
    height: int | Empty = EMPTY
    width: int | Empty = EMPTY

    def to_dict(self) -> dict[str, typing.Any]:
        return {"url": self.url}


@attrs.define(kw_only=True, slots=True)
class EmbedThumbnail(_Media):
    url: str


@attrs.define(kw_only=True, slots=True)
class EmbedImage(_Media):
    url: str


@attrs.define(kw_only=True, slots=True)
class EmbedVideo(_Media):
    url: str | None


class Embed:
    type: EmbedType
    base_dict: dict[str, typing.Any]

    def __init__(
        self,
        title: typing.Any = EMPTY,
        description: typing.Any = EMPTY,
        type: EmbedType = EmbedType.RICH,
        url: str | Empty = EMPTY,
        color: Color | int | Empty = EMPTY,
        colour: Color | int | Empty = EMPTY,
        timestamp: datetime.datetime | Empty = EMPTY,
    ) -> None:
        self.type = type
        self.base_dict = {
            "title": Empty.verify(title),
            "description": Empty.verify(description),
            "url": Empty.verify(url),
            "color": int(c) if (c := Empty.verify(color) or Empty.verify(colour)) is not None else None,
            "timestamp": timestamp.timestamp() if not isinstance(timestamp, Empty) else None,
        }

    def to_dict(self) -> dict[str, typing.Any]:
        return self.base_dict

    @classmethod
    def from_dict(cls, data: dict[str, typing.Any] | str, *, loads: bool = False) -> Embed:
        instance = cls()
        instance.base_dict = data if isinstance(data, dict) else json.loads(data)
        return instance

    @property
    def title(self) -> str | None:
        return self.base_dict.get("title")

    @title.setter
    def set_title(self, value: typing.Any) -> None:
        self.base_dict["title"] = str(value)

    @property
    def description(self) -> str | None:
        return self.base_dict.get("description")

    @description.setter
    def set_desc(self, other: typing.Any) -> None:
        self.base_dict["description"] = str(other)

    @property
    def fields(self) -> list[EmbedField]:
        return [EmbedField(**field) for field in self.base_dict.get("fields", [])]

    @property
    def author(self) -> EmbedAuthor | None:
        return EmbedAuthor(**author) if (author := self.base_dict.get("author")) else None

    @property
    def footer(self) -> EmbedFooter | None:
        return EmbedFooter(**footer) if (footer := self.base_dict.get("footer")) else None

    @property
    def image(self) -> EmbedImage | None:
        return EmbedImage(**image) if (image := self.base_dict.get("image")) else None

    @property
    def video(self) -> EmbedVideo | None:
        return EmbedVideo(**video) if (video := self.base_dict.get("video")) else None

    @property
    def thumbnail(self) -> EmbedThumbnail | None:
        return EmbedThumbnail(**thumbnail) if (thumbnail := self.base_dict.get("thumbnail")) else None

    def set_author(self, *, name: str, icon_url: str | Empty = EMPTY, url: str | Empty = EMPTY) -> Embed:
        self.base_dict["author"] = EmbedAuthor(name=name, url=url, icon_url=icon_url).to_dict()
        return self

    def add_field(self, name: typing.Any, value: typing.Any, *, inline: bool = False) -> Embed:
        self.base_dict.setdefault("fields", []).append(EmbedField(name=name, value=value, inline=inline).to_dict())
        return self

    def set_image(self, url: str) -> Embed:
        self.base_dict["image"] = (EmbedImage(url=url)).to_dict()
        return self

    def set_thumbnail(self, url: str) -> Embed:
        self.base_dict["thumbnail"] = EmbedThumbnail(url=url).to_dict()
        return self
