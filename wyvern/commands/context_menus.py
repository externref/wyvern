from __future__ import annotations
import typing

import attrs

from wyvern.interactions.base import InteractionCommandType

from .base import BaseCallable

if typing.TYPE_CHECKING:
    from .base import CallbackT

__all__: tuple[str, ...] = ("UserContextMenuCommand", )

@attrs.define(kw_only=True)
class UserContextMenuCommand(BaseCallable):
    name: str
    callback: CallbackT
    type = InteractionCommandType.USER
