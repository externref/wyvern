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

from wyvern.components import ActionRowContainer, Button, ButtonStyle

if typing.TYPE_CHECKING:

    from wyvern._types import ButtonCallbackT
    from wyvern.interactions import ComponentInteraction
    from wyvern.models.emojis import CustomEmoji
    from wyvern.models.messages import Message


@attrs.define(kw_only=True)
class CallableButton(Button):
    callback: ButtonCallbackT

    def __call__(self, button: CallableButton, inter: ComponentInteraction) -> typing.Awaitable[typing.Any]:
        return self.callback(button, inter)


@attrs.define(kw_only=True)
class MessageComponents:
    timeout: int = 180
    containers: list[ActionRowContainer] = attrs.field(default=[ActionRowContainer()] * 5, init=False)
    message: Message | None = attrs.field(default=None, init=False)

    async def _timeout(self) -> None:
        if self.timeout is not None:
            await asyncio.sleep(self.timeout)
            await self.on_timeout()

    async def on_timeout(self) -> None:
        ...

    def start(self, message: Message) -> None:
        self.message = message
        asyncio.create_task(self._timeout())

    def with_button(
        self,
        *,
        style: ButtonStyle = ButtonStyle.SECONDARY,
        label: str | None = None,
        emoji: str | CustomEmoji | None = None,
        custom_id: str | None = None,
        disabled: bool = False,
        url: str | None = None,
        row: int = 0,
    ) -> typing.Callable[[ButtonCallbackT], CallableButton]:
        """Adds a button to the component handler.

        Parameters
        ----------

        style : wyvern.components.base.ButtonStyle
            The style of button.
        label : str | None
            Button's label.
        emoji : str | wyvern.models.emojis.CustomEmoji
            A unicode emoji or a custom one.
        custom_id : str
            A custom id set to the button.
        disabled : bool
            Set this to [True][] to disable clicks on button.
        url : str
            The URL this button points to.

        Returns
        -------

        wyvern.components.buttons.Button
            The button that was created.

        """

        def decorator(callback: ButtonCallbackT) -> CallableButton:
            _button = CallableButton(
                callback=callback,
                style=style,
                label=label,
                emoji=emoji,
                custom_id=custom_id,
                disabled=disabled,
                url=url,
            )
            self.containers[row].items.append(_button)
            return _button

        return decorator

    def build(self) -> list[ActionRowContainer]:
        return self.containers
