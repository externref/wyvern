import datetime
import typing

@typing.final
class DiscordObject:
    def __init__(
        self,
        *,
        id: int,
    ) -> None:
        self._id = id
        self._created_at = self.get_created_at(id)

    @classmethod
    def get_created_at(cls, id: int) -> datetime.datetime:
        timestamp = ((id >> 22) + 1420070400000) / 1000
        return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)

    @property
    def created_at(
        self,
    ) -> datetime.datetime:
        return self._created_at

    @property
    def id(self) -> int:
        return self._id

@typing.final
class Intents:
    NONE = 0
    UNPRIVILEGED = 

    GUILDS = 1 << 0
    GUILD_MEMBERS = 1 << 1
    GUILD_BANS = 1 << 2

    GUILD_EMOJIS_AND_STICKERS = 1 << 3
    GUILD_INTEGRATIONS = 1 << 4
    GUILD_WEBHOOKS = 1 << 5
    GUILD_INVITES = 1 << 6

    GUILD_VOICE_STATES = 1 << 7
    GUILD_PRESENCES = 1 << 8

    GUILD_MESSAGES = 1 << 9
    GUILD_MESSAGE_REACTIONS = 1 << 10
    GUILD_MESSAGE_TYPING = 1 << 11

    DIRECT_MESSAGES = 1 << 12
    DIRECT_MESSAGE_REACTIONS = 1 << 13
    DIRECT_MESSAGE_TYPING = 1 << 14

    GUILD_SCHEDULED_EVENTS = 1 << 16

    def __init__(
        self,
        *args: int,
    ) -> None:
        self._value = 0
        #self.enabled: typing.MutableSet = set()
        for value in args:
            self._value |= value

    @property
    def value(self) -> int:
        return self._value

    @classmethod
    def from_value(cls, value: int) -> "Intents":
        intents = Intents()
        intents._value = value
        return intents


