import dataclasses
import datetime
import typing

from .base_events import GatewayEvent

if typing.TYPE_CHECKING:
    from clyde.bot import Bot


@dataclasses.dataclass
class MessageCreate(GatewayEvent):
    bot: "Bot"
    id: int
    author_id: int
    message_id: int
    created_at: datetime.datetime
    from_bot: bool
    from_human: bool
    from_webhook: bool
    shard: int
    channel_id: int | None
    webhook_id: int | None
    reference_message_id: int | None

    message: typing.Any

    def __init__(
        self, bot: "Bot", payload: typing.Dict[typing.Any, typing.Any]
    ) -> None:
        super().__init__(bot)

        self._payload_data = payload
        self._initialize_event_from_payload()

    @property
    def data(self) -> typing.Dict[str, typing.Any]:
        return self._payload_data["d"]

    def _initialize_event_from_payload(self) -> None:
        self.id = int(self.data["id"])
        self.author_id = int(self.data["author"]["id"])
        self.channel_id = int(self.data["channel_id"])
        self.created_at = datetime.datetime.fromisoformat(self.data["timestamp"])


{
    "type": 0,
    "tts": False,
    "timestamp": "2022-08-06T05:46:36.204000+00:00",
    "referenced_message": None,
    "pinned": False,
    "nonce": "1005351163752611840",
    "mentions": [],
    "mention_roles": [],
    "mention_everyone": False,
    "id": "1005351164776304702",
    "flags": 0,
    "embeds": [],
    "edited_timestamp": None,
    "content": ".",
    "components": [],
    "channel_id": "964215816696529026",
    "author": {
        "username": "sarth",
        "public_flags": 256,
        "id": "580034015759826944",
        "discriminator": "0460",
        "avatar_decoration": None,
        "avatar": "f6836db8bae44b223ec0929b892e5e71",
    },
    "attachments": [],
}
