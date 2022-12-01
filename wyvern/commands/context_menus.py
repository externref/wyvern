import typing

import attrs

from wyvern.interactions.base import InteractionCommandType

from .base import BaseCallable

if typing.TYPE_CHECKING:
    from .base import CallbackT


@attrs.define(kw_only=True)
class UserContextMenuCommand(BaseCallable):
    name: str
    callback: "CallbackT"
    type = InteractionCommandType.USER
