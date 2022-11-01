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

from .base import ButtonStyle, Component, ComponentType
from .buttons import Button

if typing.TYPE_CHECKING:
    from wyvern.models.emojis import CustomEmoji


__all__: tuple[str, ...] = ("ActionRowContainer",)


class ActionRowContainer(Component):
    """Interface to create an Action Row.
    This class accepts and stores. other discord components.
    """

    type = ComponentType.ACTION_ROW
    items: list[Component] = []
    """List of items stored in the container."""

    def __init__(self, *items: Component) -> None:
        for item in items:
            self.items.append(item)
        super().__init__()

    def to_payload(self) -> dict[str, typing.Any]:
        return {"type": int(self.type), "components": [item.to_payload() for item in self.items]}

    def add_button(
        self,
        *,
        style: ButtonStyle = ButtonStyle.SECONDARY,
        label: str | None = None,
        emoji: str | "CustomEmoji" | None = None,
        custom_id: str | None = None,
        disabled: bool = False,
        url: str | None = None,
    ) -> Button:
        """Adds a button to the container.

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
        self.items.append(
            button := Button(
                type=ComponentType.BUTTON,
                style=style,
                label=label,
                emoji=emoji,
                custom_id=custom_id,
                disabled=disabled,
                url=url,
            )
        )
        return button
