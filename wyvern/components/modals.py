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

from .base import Component, ComponentType

__all__: tuple[str, ...] = ("TextInputStyle", "TextInput", "Modal")


class TextInputStyle(enum.IntFlag):
    SHORT = 1
    """For single line text-inputs."""
    PARAGRAPH = 2
    """For multi line text-inputs."""


@typing.final
@attrs.define(kw_only=True, slots=True, repr=True)
class TextInput(Component):
    """Represents a modal text-input."""

    type: ComponentType = ComponentType.TEXT_INPUT
    custom_id: str
    """Custom id of the textinput."""
    label: str
    """Label of the textinput."""
    style: TextInputStyle = TextInputStyle.SHORT
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
    """The placeholder to use, if any."""

    def to_payload(self) -> dict[str, typing.Any]:
        return {
            "type": int(self.type),
            "custom_id": self.custom_id,
            "label": self.label,
            "style": int(self.style),
            "min_length": self.min_length,
            "max_length": self.max_length,
            "required": self.required,
            "value": self.default_value,
            "placeholder": self.placeholder,
        }


@attrs.define(kw_only=True, slots=True)
class Modal:
    """Represents a discord modal form."""

    title: str
    """Title of the modal."""
    custom_id: str
    """Custom ID of the modal"""
    text_inputs: list[TextInput] = []
    """A list of [TextInputs] to use in the modal."""

    def add_item(self, text_input: TextInput) -> None:
        """Method to add a textinput to the Modal."""
        self.text_inputs.append(text_input)
