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

import typing

import attrs

from .base import ButtonStyle, Component, ComponentType

if typing.TYPE_CHECKING:
    from wyvern.models.emojis import CustomEmoji

__all__: tuple[str, ...] = ("Button",)


@attrs.define(kw_only=True, slots=True, repr=True)
class Button(Component):
    """Represents a discord button.
    The properties mentioned below can be used to create a button.
    """

    style: ButtonStyle = ButtonStyle.SECONDARY
    """Style of the button."""
    label: str | None = None
    """Button's label."""
    emoji: str | "CustomEmoji" | None = None
    """Emoji embedded in the button."""
    custom_id: str | None = None
    """Custom id for the component."""
    disabled: bool = False
    """True if the component is disabled."""
    url: str | None = None
    """The URL this button points to, if any."""

    type: ComponentType = ComponentType.BUTTON

    def to_payload(self) -> dict[str, typing.Any]:
        payload: dict[str, typing.Any] = {
            "type": int(self.type),
            "style": int(self.style),
            "label": self.label,
            "custom_id": self.custom_id or "wyvern.NO_CUSTOM_ID",
            "disabled": self.disabled,
            "url": self.url,
        }
        if self.emoji is not None:
            payload["emoji"] = (
                {"name": self.emoji}
                if (not isinstance(self.emoji, CustomEmoji))
                else {"name": self.emoji.name, "id": self.emoji.id, "animated": self.emoji.is_animated}
            )
        return payload
