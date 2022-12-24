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
import enum
import typing

import attrs

from wyvern._internals import BitWiseFlag

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


class GuildFeatures(enum.Enum):
    ANIMATED_ICON = "ANIMATED_ICON"
    BANNER = "BANNER"
    COMMERCE = "COMMERCE"
    COMMUNITY = "COMMUNITY"
    DISCOVERABLE = "DISCOVERABLE"
    FEATURABLE = "FEATURABLE"
    INVITE_SPLASH = "INVITE_SPLASH"
    MEMBER_VERIFICATION_GATE_ENABLED = "MEMBER_VERIFICATION_GATE_ENABLED"
    MONETIZATION_ENABLED = "MONETIZATION_ENABLED"
    MORE_EMOJI = "MORE_EMOJI"
    NEWS = "NEWS"
    PARTNERED = "PARTNERED"
    PREVIEW_ENABLED = "PREVIEW_ENABLED"
    PUBLIC = "PUBLIC"
    PUBLIC_DISABLED = "PUBLIC_DISABLED"
    RELAY_ENABLED = "RELAY_ENABLED"
    SEVEN_DAY_THREAD_ARCHIVE = "SEVEN_DAY_THREAD_ARCHIVE"
    THREE_DAY_THREAD_ARCHIVE = "THREE_DAY_THREAD_ARCHIVE"
    TICKETED_EVENTS_ENABLED = "TICKETED_EVENTS_ENABLED"
    VANITY_URL = "VANITY_URL"
    VERIFIED = "VERIFIED"
    VIP_REGIONS = "VIP_REGIONS"
    WELCOME_SCREEN_ENABLED = "WELCOME_SCREEN_ENABLED"


class MutableGuildFeatures(enum.Enum):
    COMMUNITY = "COMMUNITY"
    INVITES_DISABLED = "INVITES_DISABLED"
    DISCOVERABLE = "DISCOVERABLE"


class GuildVerificationLevel(enum.IntEnum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4


class GuildDefaultMessageNotificationLevel(enum.IntEnum):
    ALL_MESSAGES = 0
    ONLY_MENTIONS = 1


class GuildExplicitContentFilterLevel(enum.IntEnum):
    DISABLED = 0
    MEMBERS_WITHOUT_ROLES = 1
    ALL_MEMBERS = 2


class GuildMFALevel(enum.IntEnum):
    NONE = 0
    ELEVATED = 1


class GuildPremiumTier(enum.IntEnum):
    NONE = 0
    TIER_1 = 1
    TIER_2 = 2
    TIER_3 = 3


class GuildNSFWLevel(enum.IntEnum):
    DEFAULT = 0
    EXPLICIT = 1
    SAFE = 2
    AGE_RESTRICTED = 3


class GuildSystemChannelFlags(BitWiseFlag):
    SUPPRESS_JOIN_NOTIFICATIONS = 1 << 0
    SUPPRESS_PREMIUM_SUBSCRIPTIONS = 1 << 1
    SUPPRESS_GUILD_REMINDER_NOTIFICATIONS = 1 << 2
    SUPPRESS_JOIN_NOTIFICATION_REPLIES = 1 << 3


class IntegrationExpireBehavior(enum.IntEnum):
    REMOVE_ROLE = 0
    KICK = 1


@attrs.define(kw_only=True, slots=True, repr=True)
class Ban:
    reason: str | None
    user: User


@attrs.define(kw_only=True, slots=True, repr=True)
class IntegrationAccount:
    id: str
    name: str


@attrs.define(kw_only=True, slots=True, repr=True)
class IntegrationApplication(DiscordObject):
    name: str
    icon: typing.Optional[str]
    description: str
    summary: str
    bot: typing.Optional[User]


@attrs.define(kw_only=True, slots=True, repr=True)
class Integration(DiscordObject):
    raw: typing.Dict[str, typing.Any]
    id: Snowflake
    name: str
    type: str
    is_enabled: bool
    is_syncing: bool
    role_id: typing.Optional[Snowflake]
    enable_emoticons: typing.Optional[bool]
    expire_behavior: typing.Optional[IntegrationExpireBehavior]
    expire_grace_period: typing.Optional[int]
    user: typing.Optional[User]
    account: typing.Optional[IntegrationAccount]
    synced_at: typing.Optional[datetime.datetime]
    subscriber_count: typing.Optional[int]
    revoked: typing.Optional[bool]
    application: typing.Optional[IntegrationApplication]
    scopes: typing.Optional[typing.List[str]]

    @property
    def created_at(self) -> datetime.datetime:
        return super().created_at


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
    verification_level: GuildVerificationLevel
    default_message_notifications: GuildDefaultMessageNotificationLevel
    explicit_content_filter: GuildExplicitContentFilterLevel
    roles: list[Role]
    emojis: list[CustomEmoji]
    features: list[GuildFeatures]
    mfa_level: GuildMFALevel
    application_id: typing.Optional[Snowflake]
    system_channel_id: typing.Optional[Snowflake]
    system_channel_flags: GuildSystemChannelFlags
    rules_channel_id: typing.Optional[Snowflake]
    max_presences: typing.Optional[int]
    max_members: int
    vanity_url_code: typing.Optional[str]
    description: typing.Optional[str]
    banner: typing.Optional[str]
    premium_tier: GuildPremiumTier
    premium_subscription_count: int
    preferred_locale: str
    public_updates_channel_id: typing.Optional[Snowflake]
    max_video_channel_users: int
    approximate_member_count: int
    approximate_presence_count: int
    welcome_screen: typing.Optional[WelcomeScreen]
    nsfw_level: GuildNSFWLevel
    stickers: list[Sticker]
    premium_progress_bar_enabled: bool

    @property
    def icon_url(self) -> str | None:
        return f"https://cdn.discordapp.com/icons/{self.id}/{self.icon}.png" if self.icon else None

    @property
    def splash_url(self) -> str | None:
        return f"https://cdn.discordapp.com/splashes/{self.id}/{self.splash}.png" if self.splash else None

    @property
    def discovery_splash_url(self) -> str | None:
        return (
            f"https://cdn.discordapp.com/discovery-splashes/{self.id}/{self.discovery_splash}.png"
            if self.discovery_splash
            else None
        )

    @property
    def banner_url(self) -> str | None:
        return f"https://cdn.discordapp.com/banners/{self.id}/{self.banner}.png" if self.banner else None

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
    def icon_url(self) -> str | None:
        return f"https://cdn.discordapp.com/icons/{self.id}/{self.icon}.png" if self.icon else None

    @property
    def splash_url(self) -> str | None:
        return f"https://cdn.discordapp.com/splashes/{self.id}/{self.splash}.png" if self.splash else None

    @property
    def discovery_splash_url(self) -> str | None:
        return (
            f"https://cdn.discordapp.com/discovery-splashes/{self.id}/{self.discovery_splash}.png"
            if self.discovery_splash
            else None
        )

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
