from __future__ import annotations

import inspect
import typing

if typing.TYPE_CHECKING:
    from wyvern.models.messages import Message


class CommandHandler:
    prefix_getter: typing.Any
    prefix_type: type

    async def get_prefix(self, message: "Message") -> typing.Any:
        if type(self.prefix_getter) in [str, set, list, tuple]:
            return self.prefix_getter
        else:
            if inspect.iscoroutinefunction(self.prefix_getter):
                return self.prefix_getter(self, message)
            elif inspect.isfunction(self.prefix_getter):
                return self.prefix_getter(self, message)
            else:
                return str(self.prefix_getter)
