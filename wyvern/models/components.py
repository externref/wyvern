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

import abc
import enum
import typing

import attrs

if typing.TYPE_CHECKING:
    import discord_typings

__all__: tuple[str, ...] = ("ButtonStyle", "ComponentType", "Component")


class ButtonStyle(enum.IntEnum):
    """Enums for Button style."""

    PRIMARY = 1
    """A primary blurple discord button."""
    SECONDARY = 2
    """A secondary gray discord button."""
    SUCCESS = 3
    """Green discord button."""
    DANGER = 4
    """Red discord button."""
    LINK = 5
    """Button pointing to an URL"""
    BLURPLE = PRIMARY
    """Alias for PRIMARY"""
    GRAY = SECONDARY
    """Alias for SECONDARY"""
    GREY = SECONDARY
    """Alias for SECONDARY"""
    GREEN = SUCCESS
    """Alias for SUCCESS"""
    RED = DANGER
    """Alias for DANGER"""
    URL = LINK
    """Alias for LINK"""


class ComponentType(enum.IntEnum):
    ACTION_ROW = 1
    BUTTON = 2
    STRING_SELECT = 3
    TEXT_INPUT = 4
    USER_SELECT = 5
    ROLE_SELECT = 6
    MENTIONABLE_SELECT = 7
    CHANNEL_SELECT = 8


class Component(abc.ABC):
    """Represents a discord component.
    Is the base class for other components."""


@attrs.define(kw_only=True, slots=True, repr=True)
class Button(Component):
    """Represents a discord button.
    The properties mentioned below can be used to create a button.
    """

    type: ComponentType = attrs.field(init=False, default=ComponentType.BUTTON)
    style: ButtonStyle
    """Style of the button."""
    label: str | None = None
    """Button's label."""
    emoji: typing.Any = None
    """Emoji embedded in the button."""
    custom_id: str | None = None
    """Custom id for the component."""
    disabled: bool = False
    """True if the component is disabled."""
    url: str | None = None
    """The URL this button points to, if any."""

    @classmethod
    def from_payload(cls, payload: discord_typings.ButtonComponentData) -> Button:
        return Button(
            style=ButtonStyle(payload["style"]),
            label=payload.get("label"),
            emoji=payload.get("emoji"),
            custom_id=payload.get("custom_id"),
            disabled=payload.get("disabled", False),
            url=payload.get("url"),
        )


class TextInputStyle(enum.IntEnum):
    SHORT = 1
    """For single line text-inputs."""
    PARAGRAPH = 2
    """For multi line text-inputs."""


@typing.final
@attrs.define(kw_only=True, slots=True, repr=True)
class TextInput(Component):
    """Represents a modal text-input."""

    type: ComponentType = attrs.field(init=False, default=ComponentType.TEXT_INPUT)
    custom_id: str
    """Custom id of the textinput."""
    label: str
    """Label of the textinput."""
    style: TextInputStyle
    """Textinput style."""
    min_length: int | None = None
    """The maximum allowed length for textinput."""
    max_length: int | None = None
    """The minimum allowed length for textinput."""
    required: bool = True
    """Weather the field is required."""
    default_value: str | None = None
    """Default value for this textinput."""
    placeholder: str | None = None
    """The placeholder used, if any."""

    @classmethod
    def from_payload(cls, payload: discord_typings.TextInputComponentData) -> TextInput:
        return TextInput(
            custom_id=payload["custom_id"],
            label=payload["label"],
            style=TextInputStyle(payload["style"]),
            min_length=payload.get("min_length"),
            max_length=payload.get("max_length"),
            required=payload.get("required", True),
            default_value=payload.get("value"),
            placeholder=payload.get("placeholder"),
        )


@attrs.define(kw_only=True, slots=True)
class Modal:
    """Represents a discord modal form."""

    title: str
    """Title of the modal."""
    custom_id: str
    """Custom ID of the modal"""
    text_inputs: list[TextInput]
    """List of textinputs in the modal."""


@attrs.define(kw_only=True, slots=True)
class ActionRow(Component):
    type: ComponentType = attrs.field(init=False, default=ComponentType.ACTION_ROW)
    components: list[Component]
