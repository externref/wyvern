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


def default_avatar_for(discriminator: int) -> str:
    return f"embed/avatars{discriminator % 5}.png"


__all__: tuple[str, ...] = ("DiscordObject",)


class DiscordObject:
    """
    Represents a discord object.

    Parameters
    ----------

    _id: int
        ID of the entity.

    Attributes
    ----------

    id: int
        ID of the entity.

    """

    def __init__(self, _id: int) -> None:
        self.id = _id

    def __eq__(self, obj: object) -> bool:
        if not isinstance(obj, DiscordObject):
            return NotImplemented
        return self.id == obj.id

    @property
    def created_at(self) -> datetime.datetime:
        """
        The datetime at which this entity was created.

        Returns
        -------

        datetime.datetime
        """
        return self.get_created_at(self.id)

    @classmethod
    def get_created_at(cls, _id: int) -> datetime.datetime:
        """
        Get creation time of an entity using it's ID.
        """
        timestamp = ((_id >> 22) + 1420070400000) / 1000
        return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)
