from __future__ import annotations

import enum
import typing

import attrs

if typing.TYPE_CHECKING:
    from wyvern import models
    from wyvern.clients import GatewayClient

    from .applications import ApplicationCommandInteractionData

__all__: tuple[str, ...] = ("Interaction", "InteractionCommandOptionType", "InteractionCommandType", "InteractionType")


@typing.final
class InteractionType(enum.IntEnum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODEL_SUBMIT = 5


@typing.final
class InteractionCommandType(enum.IntEnum):
    ...


@typing.final
class InteractionCommandOptionType:
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    NUMBER = 10
    ATTACHMENT = 11


@attrs.define(kw_only=True, slots=True, repr=True, init=True)
class Interaction:
    _client: "GatewayClient"
    id: int
    application_id: int
    type: InteractionType
    data: "ApplicationCommandInteractionData"
    guild_id: int | None
    channel_id: int | None
    user: models.users.User
    token: str
    version: int = 1
    message: "models.messages.Message" | None
    guild_locale: str | None
