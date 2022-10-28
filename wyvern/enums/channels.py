import enum


class ChannelType(enum.IntEnum):
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_ANNOUNCEMENT = 5
    ANNOUNCEMENT_THREAD = 10
    PUBLIC_THREAD = 11
    PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13
    GUILD_DIRECTORY = 14


class ChannelVideoQualityMode(enum.IntEnum):
    AUTO = 1
    FULL = 2


class ForumChannelFlags(enum.IntFlag):
    PINNED = 1 << 1
    REQUIRE_TAG = 1 << 4


class SortOrderTypes(enum.IntEnum):
    LATEST_ACTIVITY = 0
    CREATION_DATE = 1
