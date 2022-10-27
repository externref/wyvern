import datetime


class DiscordObject:
    def __init__(self, id: int) -> None:
        self.id = id

    @classmethod
    def get_created_at(cls, id: int) -> datetime.datetime:
        timestamp = ((id >> 22) + 1420070400000) / 1000
        return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)
