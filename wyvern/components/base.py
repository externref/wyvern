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

__all__: tuple[str, ...] = ("ButtonStyle", "ComponentType")


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


class Component:
    """Represents a discord component.
    Is the base class for other components."""

    type: ComponentType
    """Type of the component."""

    def to_payload(self) -> dict[str, typing.Any]:
        return {}
