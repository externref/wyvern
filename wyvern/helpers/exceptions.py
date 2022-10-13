class WyvernException(Exception):
    pass


class HTTPException(WyvernException):
    message: str
    status_code: int

    def __init__(self, message: str | None = None) -> None:
        self.message = message or "An unknown error occurred."
        super().__init__(message)

    @classmethod
    def from_code(cls, status_code: int, message: str | None = None) -> "HTTPException":
        self = cls(message)
        self.status_code = status_code
        return self


class BadRequest(HTTPException):
    status_code = 400


class Unauthorized(HTTPException):
    status_code = 401


class Forbidden(HTTPException):
    status_code = 403


class NotFound(HTTPException):
    status_code = 404


class InvalidMethod(HTTPException):
    status_code = 405


class RateLimited(HTTPException):
    status_code = 429


class UknownError(HTTPException):
    status_code = 500
