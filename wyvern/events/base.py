from __future__ import annotations

import typing

import attrs

if typing.TYPE_CHECKING:
    from wyvern.api.bot import Bot

__all__: tuple[str] = ("Event",)


@attrs.define(kw_only=True)
class Event:
    bot: Bot
