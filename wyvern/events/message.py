import dataclasses
import datetime
import typing

from .base_events import BaseEvent

if typing.TYPE_CHECKING:
    from wyvern import Bot


@dataclasses.dataclass
class CreateMessage(BaseEvent):
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

    def __init__(self, bot: "Bot", payload: dict[str, dict[str, typing.Any]]) -> None:
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
