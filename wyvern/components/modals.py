from __future__ import annotations

import enum
import typing

import attrs

from .base import Component, ComponentType


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
            "type": self.type,
            "custom_id": self.custom_id,
            "label": self.label,
            "style": self.style,
            "min_length": self.min_length,
            "max_length": self.max_length,
            "required": self.required,
            "value": self.default_value,
            "placeholder": self.placeholder,
        }


@attrs.define(kw_only=True, slots=True)
class Modal:
    title: str
    custom_id: str
    text_inputs: list[TextInput] = []

    def add_item(self, text_input: TextInput) -> None:
        self.text_inputs.append(text_input)
