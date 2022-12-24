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

if typing.TYPE_CHECKING:
    from wyvern.clients import GatewayClient
    from wyvern.events import Event, EventListener, as_listener

__all__: tuple[str, ...] = ("Plugin",)


class Plugin:
    """Plugins for extendibility.

    Parameters
    ----------
    name: str
        Name of the plugin.
    description : str | None
        Description of the plugin.
    """

    name: str
    """Name of the plugin."""
    description: str | None = None
    """Description of the plugin."""
    client: GatewayClient
    """Client attached to the plugin."""
    listeners: list[EventListener] = []
    """EventListeners attached to the plugin."""

    def __init__(self, name: str, *, description: str | None = None) -> None:
        self.name = name
        self.description = description

    def setup_plugin(self, client: "GatewayClient") -> None:
        self.client = client
        for listener in self.listeners:
            client.event_handler.add_listener(listener)

    def with_listener(
        self, event: Event, *, max_trigger: int | float = float("inf")
    ) -> typing.Callable[[typing.Callable[..., typing.Awaitable[typing.Any]]], EventListener]:
        """
        Creates and adds a new listenet to the client's event handler.

        Parameters
        ----------
        event:  wyvern.events.Event
            The event to listen.
        max_trigger: int | float
            Maximum number of times this listener has to be triggered.

        Returns
        -------
        wyvern.events.EventListener
            A EventListener object.
        """

        def inner(callback: typing.Callable[..., typing.Awaitable[typing.Any]]) -> EventListener:
            lsnr = as_listener(event, max_trigger=max_trigger)(callback)
            self.listeners.append(lsnr)
            return lsnr

        return inner
