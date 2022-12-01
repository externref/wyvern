from __future__ import annotations

import enum
import typing

import attrs

from .base import Component

if typing.TYPE_CHECKING:
    from wyvern.models.channels import ChannelType
    from wyvern.models.emojis import CustomEmoji

__all__: tuple[str, ...] = ("SelectType", "Select", "SelectOption")


class SelectType(enum.IntEnum):
    """Type of the select option"""

    STRING = 3
    """String type select, this requires the `options` kwarg in the [Select][] class."""
    USER = 5
    """User type select menu."""
    ROLE = 6
    """Role type select menu."""
    MENTIONABLE = 7
    """Mentionable type select menu."""
    CHANNEL = 8
    """Channel type select menu."""


@attrs.define(kw_only=True, slots=True)
class SelectOption:
    """Represents a Select option."""

    label: str
    """Label of the option."""
    _value: str | None = None
    """Value of the option, defaults to the label."""
    description: str | None
    """Description of the option."""
    emoji: str | CustomEmoji | None = None
    """Emoji attached to the option."""
    default: bool = False
    """Set to `True` if the option is to be used as default."""

    @property
    def value(self) -> str:
        return self._value or self.label

    def to_payload(self) -> dict[str, typing.Any]:
        return {
            "label": self.label,
            "value": self.value,
            "description": self.description,
            "emoji": str(self.emoji),
            "default": self.default,
        }


@attrs.define(kw_only=True, slots=True)
class Select(Component):
    """Represents a discord Select menu."""

    type: SelectType = SelectType.STRING
    """Type of the select"""
    custom_id: str
    """Custom ID of the select."""
    options: list[SelectOption] = []
    """Options attached to the select."""
    channel_types: list[ChannelType] | None = None
    """Channel types for CHANNEL type select."""
    min_values: int | None = None
    """Minimum selections."""
    max_values: int | None = None
    """Maximum selections."""
    disabled: bool = False
    """True if the select is disabled."""

    def to_payload(self) -> dict[str, typing.Any]:
        return {
            "type": self.type,
            "custom_id": self.custom_id,
            "options": [opt.to_payload() for opt in self.options],
            "channel_types": self.channel_types,
            "min_values": self.max_values,
            "max_values": self.max_values,
            "disabled": self.disabled,
        }
