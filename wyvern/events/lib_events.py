from __future__ import annotations

import attrs

from wyvern.events.base import Event

__all__: tuple[str, ...] = ("StartingEvent", "StartedEvent")


@attrs.define(kw_only=True)
class StartingEvent(Event):
    ...


@attrs.define(kw_only=True)
class StartedEvent(Event):
    ...
