from __future__ import annotations

import enum
import typing

import attrs

from .base import Interaction

if typing.TYPE_CHECKING:
    from wyvern.components.base import ComponentType


@attrs.define(kw_only=True, repr=True, slots=True)
class ComponentInteractionData:
    custom_id: str
    component_type: ComponentType
    values: typing.Any = {}


class ComponentInteraction(Interaction):
    data: ComponentInteractionData
