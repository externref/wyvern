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

import asyncio
import typing

import attrs

__all__: tuple[str, ...] = ("Task", "task")


@attrs.define(kw_only=True, slots=True)
class Task:
    """Represents a task that gets triggerd after some
    interval of time repeatedly."""

    trigger: typing.Callable[..., typing.Awaitable[typing.Any]]
    """The coro to trigger at every interval."""
    delay: float
    """Time delay between triggers ( in seconds )"""
    wait_until_complete: bool = True
    """Weather to wait before one trigger is complete."""
    is_running: bool = False
    """True if the task is running."""

    def update_delay(self, delay: float) -> None:
        self.delay = delay

    async def _runner(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        loop = asyncio.get_event_loop()
        while self.is_running is True:
            if self.wait_until_complete is False:
                loop.create_task(self.trigger(*args, **kwargs))  # type: ignore
            else:
                await self.trigger(*args, **kwargs)
            await asyncio.sleep(self.delay)

    def run(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        """Starts the task."""
        if self.is_running is False:
            self.is_running = True
        else:
            raise Exception("The task is already running.")
        loop = asyncio.get_event_loop()
        loop.create_task(self._runner(*args, *kwargs))

    def stop(self) -> None:
        """Stops the task."""
        self.is_running = False


def task(
    s: float | None = None, m: float | None = None, h: float | None = None, wait_until_complete: bool = True
) -> typing.Callable[..., Task]:
    """Interface to create a task.

    Parameters
    ----------

    WIP : typing.Any
        Docs to be added.
    """

    def inner(trigger: typing.Callable[..., typing.Awaitable[typing.Any]]) -> Task:
        nonlocal s, m, h
        if (delays := len([item for item in [s, m, h] if item is not None])) > 1 or delays == 0:
            raise ValueError("Only one delay field can be used for the decorator.")
        delay = 0.0
        if s:
            delay = s
        elif m:
            delay = m * 60.0
        elif h:
            delay = h * 60 * 60.0

        return Task(
            delay=delay,
            trigger=trigger,
            wait_until_complete=wait_until_complete,
        )

    return inner
