import functools
import typing


@typing.final
class Intents:
    """
    Intents are a way to tell Discord what events you want to receive.
    You can specify which intents you want to receive by passing them to the constructor.
    You can also pass a single integer to the constructor to specify the intents you want to receive.
    You can also use the bitwise OR operator to combine intents.

    Example:
    intents = Intents(Intents.guilds, Intents.members)
    intents = Intents(1 << 0 | 1 << 1)
    intents = Intents(1 << 0) | Intents(1 << 1)

    """

    NONE = 0
    GUILDS = 1 << 0
    GUILD_MEMBERS = 1 << 1
    GUILD_BANS = 1 << 2
    GUILD_EMOJIS = 1 << 3
    GUILD_INTEGRATIONS = 1 << 4
    GUILD_WEBHOOKS = 1 << 5
    GUILD_INVITES = 1 << 6
    GUILD_VOICE_STATES = 1 << 7
    GUILD_PRESENCES = 1 << 8
    GUILD_MESSAGES = 1 << 9
    GUILD_MESSAGE_REACTIONS = 1 << 10
    GUILD_MESSAGE_TYPING = 1 << 11
    DM_MESSAGES = 1 << 12
    DM_MESSAGE_REACTIONS = 1 << 13
    DM_MESSAGE_TYPING = 1 << 14
    MESSAGE_CONTENT = 1 << 15
    GUILD_SCHEDULED_EVENTS = 1 << 16
    AUTO_MODERATION_CONFIGURATION = 1 << 20

    def __init__(self, *intents: int) -> None:
        """
        Initialize the intents class.
        :param intents: The intents you want to receive.
        """
        self.value = functools.reduce(lambda x, y: x | y, intents, 0)

    def __repr__(self) -> str:
        return f"Intent(intents={self.value})"

    @classmethod
    def all(cls) -> "Intents":
        """
        Get all intents.
        :return: All intents.
        """
        return cls(
            cls.GUILDS,
            cls.GUILD_MEMBERS,
            cls.GUILD_BANS,
            cls.GUILD_EMOJIS,
            cls.GUILD_INTEGRATIONS,
            cls.GUILD_WEBHOOKS,
            cls.GUILD_INVITES,
            cls.GUILD_VOICE_STATES,
            cls.GUILD_PRESENCES,
            cls.GUILD_MESSAGES,
            cls.GUILD_MESSAGE_REACTIONS,
            cls.GUILD_MESSAGE_TYPING,
            cls.DM_MESSAGES,
            cls.DM_MESSAGE_REACTIONS,
            cls.DM_MESSAGE_TYPING,
            cls.MESSAGE_CONTENT,
            cls.GUILD_SCHEDULED_EVENTS,
            cls.AUTO_MODERATION_CONFIGURATION,
        )

    @classmethod
    def from_int(cls, intent: int) -> "Intents":
        """
        Create an intents object from an integer.
        :param intent: The integer to create the intents object from.
        :return:
        """
        return cls(intent)

    @property
    def intent(self) -> typing.Generator[tuple[str, int], None, None]:
        """
        Get the intents as a tuple.
        :return:
        """
        for intent in self.__class__.__dict__:
            if intent.isupper() and intent != "NONE":
                if self.value & self.__class__.__dict__[intent]:
                    yield intent, self.__class__.__dict__[intent]
