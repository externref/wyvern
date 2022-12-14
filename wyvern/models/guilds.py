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
    from .channels import GuildChannel
    from .emojis import CustomEmoji
    from .roles import Role
    from .stickers import Sticker
    from .users import User


__all__: tuple[str, ...] = (
    "Guild",
    "GuildPreview",
    "GuildWidget",
    "GuildWidgetSettings",
    "WelcomeScreen",
    "WelcomeScreenChannel",
)


@attrs.define(kw_only=True, slots=True, repr=True)
class WelcomeScreenChannel(DiscordObject):
    raw: dict[str, typing.Any]
    channel_id: Snowflake
    description: str
    emoji_id: typing.Optional[Snowflake]
    emoji_name: typing.Optional[str]


@attrs.define(kw_only=True, slots=True, repr=True)
class WelcomeScreen(DiscordObject):
    raw: dict[str, typing.Any]
    description: str
    welcome_channels: list[WelcomeScreenChannel]

    @property
    def channels(self) -> list[WelcomeScreenChannel]:
        return self.welcome_channels


@attrs.define(kw_only=True, slots=True, repr=True)
class Guild(DiscordObject):
    raw: dict[str, typing.Any]
    id: Snowflake
    name: str
    icon: typing.Optional[str]
    splash: typing.Optional[str]
    discovery_splash: typing.Optional[str]
    owner: bool
    owner_id: Snowflake
    permissions: str
    region: str
    afk_channel_id: typing.Optional[Snowflake]
    afk_timeout: int
    widget_enabled: bool
    widget_channel_id: typing.Optional[Snowflake]
    verification_level: int
    default_message_notifications: int
    explicit_content_filter: int
    roles: list[Role]
    emojis: list[CustomEmoji]
    features: list[str]
    mfa_level: int
    application_id: typing.Optional[Snowflake]
    system_channel_id: typing.Optional[Snowflake]
    system_channel_flags: int
    rules_channel_id: typing.Optional[Snowflake]
    max_presences: typing.Optional[int]
    max_members: int
    vanity_url_code: typing.Optional[str]
    description: typing.Optional[str]
    banner: typing.Optional[str]
    premium_tier: int
    premium_subscription_count: int
    preferred_locale: str
    public_updates_channel_id: typing.Optional[Snowflake]
    max_video_channel_users: int
    approximate_member_count: int
    approximate_presence_count: int
    welcome_screen: typing.Optional[WelcomeScreen]
    nsfw_level: int
    stickers: list[Sticker]
    premium_progress_bar_enabled: bool

    @property
    def icon_url(self) -> str:
        return f"https://cdn.discordapp.com/icons/{self.id}/{self.icon}.png"

    @property
    def splash_url(self) -> str:
        return f"https://cdn.discordapp.com/splashes/{self.id}/{self.splash}.png"

    @property
    def discovery_splash_url(self) -> str:
        return f"https://cdn.discordapp.com/discovery-splashes/{self.id}/{self.discovery_splash}.png"

    @property
    def banner_url(self) -> str:
        return f"https://cdn.discordapp.com/banners/{self.id}/{self.banner}.png"

    @property
    def created_at(self) -> datetime.datetime:
        """Datetime at which sticker was created."""
        return super().created_at


@attrs.define(kw_only=True, slots=True, repr=True)
class GuildPreview(DiscordObject):
    raw: dict[str, typing.Any]
    id: Snowflake
    name: str
    icon: typing.Optional[str]
    splash: typing.Optional[str]
    discovery_splash: typing.Optional[str]
    emojis: list[CustomEmoji]
    features: list[str]
    approximate_member_count: int
    approximate_presence_count: int
    description: typing.Optional[str]

    @property
    def icon_url(self) -> str:
        return f"https://cdn.discordapp.com/icons/{self.id}/{self.icon}.png"

    @property
    def splash_url(self) -> str:
        return f"https://cdn.discordapp.com/splashes/{self.id}/{self.splash}.png"

    @property
    def discovery_splash_url(self) -> str:
        return f"https://cdn.discordapp.com/discovery-splashes/{self.id}/{self.discovery_splash}.png"

    @property
    def created_at(self) -> datetime.datetime:
        """Datetime at which sticker was created."""
        return super().created_at


@attrs.define(kw_only=True, slots=True, repr=True)
class GuildWidgetSettings(DiscordObject):
    raw: dict[str, typing.Any]
    enabled: bool
    channel_id: typing.Optional[Snowflake]


@attrs.define(kw_only=True, slots=True, repr=True)
class GuildWidget(DiscordObject):
    raw: dict[str, typing.Any]
    id: Snowflake
    name: str
    instant_invite: typing.Optional[str]
    channels: list[GuildChannel]
    members: list[User]
    presence_count: int

    @property
    def created_at(self) -> datetime.datetime:
        """Datetime at which sticker was created."""
        return super().created_at
