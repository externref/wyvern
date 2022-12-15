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
import typing

import attrs

from .base import DiscordObject, Snowflake

if typing.TYPE_CHECKING:
    from .users import User

__all__: tuple[str, ...] = (
    "VoiceState",
    "VoiceRegion",
)


@attrs.define(kw_only=True, slots=True, repr=True)
class VoiceState(DiscordObject):
    raw: dict[str, typing.Any]
    guild_id: Snowflake
    channel_id: Snowflake
    user_id: Snowflake
    member: typing.Optional[User]
    session_id: str
    deaf: bool
    mute: bool
    self_deaf: bool
    self_mute: bool
    self_stream: bool
    self_video: bool
    suppress: bool
    request_to_speak_timestamp: typing.Optional[datetime.datetime]

    @property
    def created_at(self) -> datetime.datetime:
        """Datetime at which voice state was created."""
        return super().created_at


@attrs.define(kw_only=True, slots=True, repr=True)
class VoiceRegion:
    raw: dict[str, typing.Any]
    name: str
    id: str
    vip: bool
    optimal: bool
    deprecated: bool
    custom: bool
