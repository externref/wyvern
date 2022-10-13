import datetime


class WyvernObject:
    _id: int
    _created_at: datetime.datetime

    def __init__(self, *, _id: int) -> None:
        self.id = _id
        self._created_at = self.get_created_at(_id)

    @classmethod
    def get_created_at(cls, _id: int) -> datetime.datetime:
        timestamp = ((int(_id) >> 22) + 1420070400000) / 1000
        return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)

    @property
    def created_at(self) -> datetime.datetime:
        return self._created_at
