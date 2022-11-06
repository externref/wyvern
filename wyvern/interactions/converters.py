from __future__ import annotations

import typing

from wyvern.models import converters

from .applications import ApplicationCommandInteraction, ApplicationCommandInteractionData, InteractionOption
from .base import Interaction, InteractionType
from .components import ComponentInteraction, ComponentInteractionData

if typing.TYPE_CHECKING:
    from wyvern.clients import GatewayClient


def payload_to_option(data: dict[str, typing.Any]) -> InteractionOption:
    return InteractionOption(
        name=data["name"],
        type=data["type"],
        value=data.get("value"),
        options=[payload_to_option(_data) for _data in data.get("options", [])],
        is_focused=data.get("focused", False),
    )


def payload_to_interaction(client: "GatewayClient", payload: dict[str, typing.Any]) -> Interaction:
    inter: Interaction
    if payload["type"] == InteractionType.MESSAGE_COMPONENT:
        inter = ComponentInteraction(
            client=client,
            id=payload["id"],
            application_id=payload["application_id"],
            type=payload["type"],
            data=ComponentInteractionData(**payload["data"]),
            token=payload["token"],
            version=payload["version"],
            message=converters.payload_to_message(client, msg) if (msg := payload["message"]) else None,
            user=converters.payload_to_user(client, user) if (user := payload["user"]) else None,
            guild_id=payload.get("guild_id"),
            channel_id=payload.get("guild_id"),
            guild_locale=payload.get("guild_locale"),
        )
    elif payload["type"] == InteractionType.APPLICATION_COMMAND:
        inter = ApplicationCommandInteraction(
            client=client,
            id=payload["id"],
            application_id=payload["application_id"],
            token=payload["token"],
            version=payload["version"],
            message=converters.payload_to_message(client, msg) if (msg := payload.get("message")) else None,
            type=InteractionType.APPLICATION_COMMAND,
            data=ApplicationCommandInteractionData(
                payload=payload["data"],
                command_id=((d := payload["data"])["id"]),
                command_name=d["name"],
                guild_id=d.get("guild_id"),
                command_type=d["type"],
                target_id=d.get("target_id"),
                options=[payload_to_option(data) for data in payload.get("options", [])],
            ),
            guild_id=payload.get("guild_id"),
            channel_id=payload.get("channel_id"),
            user=converters.payload_to_user(client, user) if (user := payload.get("user")) else None,
            guild_locale=payload.get("guild_locale"),
        )

    else:
        pass

    return inter
