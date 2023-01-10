from __future__ import annotations

import abc
import typing

from wyvern.models import components as base


class ConstructedComponent:
    @abc.abstractmethod
    def to_payload(self) -> dict[str, typing.Any]:
        ...


class ConstructedButton(base.Button):
    def to_payload(self) -> dict[str, typing.Any]:
        return {
            "type": int(self.type),
            "style": int(self.style),
            "label": self.label,
            "custom_id": self.custom_id or "wyvern.NO_CUSTOM_ID",
            "disabled": self.disabled,
            "url": self.url,
            "emoji": self.emoji,
        }


class ActionRowBuilder(base.ActionRow):
    components: list[ConstructedButton]  # type: ignore

    @classmethod
    def acquire(cls) -> ActionRowBuilder:
        return cls(components=[])

    def to_payload(self) -> dict[str, typing.Any]:
        return {"type": int(self.type), "components": [item.to_payload() for item in self.components]}

    @typing.overload
    def add_button(self, *, style: base.ButtonStyle, url: str, disabled: bool) -> ActionRowBuilder:
        ...

    @typing.overload
    def add_button(
        self,
        *,
        style: base.ButtonStyle,
        label: str | None = None,
        emoji: typing.Any = None,
        custom_id: str | None = None,
        disabled: bool = False,
    ) -> ActionRowBuilder:
        ...

    def add_button(
        self,
        *,
        style: base.ButtonStyle = base.ButtonStyle.PRIMARY,
        label: str | None = None,
        emoji: typing.Any = None,
        custom_id: str | None = None,
        disabled: bool = False,
        url: str | None = None,
    ) -> ActionRowBuilder:
        self.components.append(
            ConstructedButton(style=style, label=label, emoji=emoji, custom_id=custom_id, disabled=disabled, url=url)
        )
        return self
