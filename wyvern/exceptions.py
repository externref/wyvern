# MIT License

# Copyright (c) 2022 Sarthak

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from __future__ import annotations

import typing

import attrs

if typing.TYPE_CHECKING:
    from wyvern.rest import RequestRoute


class WyvernException(Exception):
    ...


@attrs.define
class HTTPException(WyvernException):
    message: str
    code: int
    route: "RequestRoute"

    def __str__(self) -> str:
        return self.message

    def create(self) -> HTTPException:
        return get_http_exception(self.code)(self.message, self.code, self.route)


class BadRequest(HTTPException):
    ...


class Unauthorized(HTTPException):
    ...


class Forbidden(HTTPException):
    ...


class NotFound(HTTPException):
    ...


class InvalidMethod(HTTPException):
    ...


class Ratelimited(HTTPException):
    ...


class UnknownError(HTTPException):
    ...


class UserNotFound(NotFound):
    """Raised when the targetted user was not found."""


class MemberNotFound(NotFound):
    """Raised when the targetted member was not found."""


excs: dict[int, typing.Type[HTTPException]] = {
    400: BadRequest,
    401: Unauthorized,
    403: Forbidden,
    404: NotFound,
    405: InvalidMethod,
    429: Ratelimited,
}


def get_http_exception(code: int) -> typing.Type[HTTPException]:
    return excs.get(code, UnknownError)


class CommandAlreadyExists(WyvernException):
    ...


class PluginException(WyvernException):
    ...
