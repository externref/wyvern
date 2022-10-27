import enum


class Endpoints(enum.Enum):
    @classmethod
    def fetch_client_user(cls) -> str:
        return "users/@me"
