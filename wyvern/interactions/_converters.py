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

from wyvern.files import Attachment
from wyvern.models import Snowflake, _converters

from .applications import (
    ApplicationCommandInteraction,
    ApplicationCommandInteractionData,
    ApplicationCommandInteractionResolvedData,
    InteractionOption,
)
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


def payload_to_resolved(
    client: "GatewayClient", guild_id: int | None, data: dict[str, typing.Any]
) -> ApplicationCommandInteractionResolvedData:
    users = [_converters.payload_to_user(client, payload=_data) for _data in data.get("users", {}).values()]
    members = []
    messages = [_converters.payload_to_message(client, _data) for _data in data.get("messages", {}).values()]
    attachments = [Attachment._from_payload(client, Snowflake, _data) for _data in data.get("attachments", {}).values()]
    channels = [_converters.payload_to_channel(client, _data) for _data in data.get("channels", {}).values()]
    if guild_id is not None:
        members = [
            _converters.payload_to_member(client, guild_id=Snowflake.create(guild_id), payload=_data)
            for _data in data.get("members", {}).values()
        ]

    res = ApplicationCommandInteractionResolvedData(
        users={u.id: u for u in users},
        members={m.id: m for m in members},
        messages={m.id: m for m in messages},
        attachments={a.id: a for a in attachments},
        channels={c.id: c for c in channels},
    )
    return res


def payload_to_interaction(client: "GatewayClient", payload: dict[str, typing.Any]) -> Interaction:
    inter: Interaction
    if payload["type"] == InteractionType.MESSAGE_COMPONENT:
        print(payload["data"])
        inter = ComponentInteraction(
            client=client,
            id=payload["id"],
            application_id=payload["application_id"],
            type=payload["type"],
            data=ComponentInteractionData(**payload["data"]),
            token=payload["token"],
            version=payload["version"],
            message=_converters.payload_to_message(client, msg) if (msg := payload.get("message")) else None,
            user=_converters.payload_to_user(client, user) if (user := payload.get("user")) else None,
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
            message=_converters.payload_to_message(client, msg) if (msg := payload.get("message")) else None,
            type=InteractionType.APPLICATION_COMMAND,
            data=ApplicationCommandInteractionData(
                payload=payload["data"],
                command_id=((d := payload["data"])["id"]),
                command_name=d["name"],
                guild_id=d.get("guild_id"),
                command_type=d["type"],
                target_id=d.get("target_id"),
                options=[payload_to_option(data) for data in payload.get("options", [])],
                resoloved=payload_to_resolved(client, payload.get("guild_id"), data)
                if (data := payload.get("resolved"))
                else None,
            ),
            guild_id=payload.get("guild_id"),
            channel_id=payload.get("channel_id"),
            user=_converters.payload_to_user(client, user) if (user := payload.get("user")) else None,
            guild_locale=payload.get("guild_locale"),
        )

    else:
        pass

    return inter  # type: ignore
