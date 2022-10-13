import typing

from .object import WyvernObject


class BaseUser(WyvernObject):
    id: int
    name: str
    discriminator: str
    mfa_enabled: bool
    about_me: str | None

    def __init__(self, data: dict[str, typing.Any]) -> None:
        super().__init__(_id=data["id"])
        self.name = data["username"]
        self.discriminator = data["discriminator"]
        self.mfa_enabled = data["mfa_enabled"]
        self.about_me = data["about_me"]

    def __repr__(self) -> str:
        return f"{self.name}#{self.discriminator}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BaseUser):
            return self.id == other.id
        raise NotImplemented

    @property
    def mention(self) -> str:
        return f"<@{self.id}>"
