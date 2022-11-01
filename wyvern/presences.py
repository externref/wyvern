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

__all__: tuple[str, ...] = ("Status", "Activity", "ActivityType")


@typing.final
class Status(enum.Enum):
    """Enum for User's status"""

    ONLINE = "online"
    """Online status."""
    DND = "dnd"
    """DND status."""
    IDLE = "idle"
    """IDLE status."""
    INVISIBLE = "invisible"
    """Invisible status."""
    OFFLINE = "offline"
    """Offline status."""


@typing.final
class ActivityType(enum.IntEnum):
    """Type of activity."""

    GAME = 0
    """The user is playing a game."""
    STREAMING = 1
    """Activity where user is streaming."""
    LISTENING = 2
    """Listening activity."""
    WATCHING = 3
    """Watching activity."""
    CUSTOM = 4
    """This activity is a custom status."""
    COMPETING = 5
    """Compoeting activity."""


class Activity:
    """Represents a base activity with minumum info.
    Base class for all activities and for bot's gateway payload.

    Parameters
    ----------

    name : str
        Name of the activity.
    type : wyvern.presences.ActivityType
        Type of the activity.
    url : The URL this activity points to.

    """

    name: str
    """Name of the activity."""
    type: ActivityType
    """Type of activity."""
    url: str | None
    """URL this activity points to."""

    def __init__(self, *, name: str, type: ActivityType, url: str | None = None) -> None:
        self.name = name
        self.type = type
        self.url = url

    def to_event_payload(
        self,
    ) -> dict[str, str | int | None]:
        return {"name": self.name, "type": int(self.type), "url": self.url}
