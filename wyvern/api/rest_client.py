# MIT License

# Copyright (c) 2023 Sarthak

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

from wyvern import builders, models, types
from wyvern.internals.rest import Endpoints, RequestRoute, RESTClient
from wyvern.utils.consts import NULL, Null

# if typing.TYPE_CHECKING:
#     import discord_typings

__all__: tuple[str, ...] = ("RESTClientImpl",)


class RESTClientImpl(RESTClient):
    async def create_message(
        self,
        channel_id: types.Snowflakish[models.ImplementsMessage],
        content: types.NullOr[str] = NULL,
        embed: types.NullOr[builders.Embed] = NULL,
        embeds: types.NullOr[typing.Sequence[builders.Embed]] = NULL,
        component: types.NullOr[builders.ActionRowBuilder] = NULL,
        components: types.NullOr[typing.Sequence[builders.ActionRowBuilder]] = NULL,
    ):
        data: dict[str, typing.Any] = {"content": str(content) if content is not NULL else None}
        if embed is not NULL and embeds is not NULL:
            raise ValueError("expected only embed or only embeds argument, got both.")
        elif not isinstance(embed, Null):
            data["embeds"] = [embed.to_dict()]
        elif not isinstance(embeds, Null):
            data["embeds"] = [embed.to_dict() for embed in embeds]
        if component is not NULL and components is not NULL:
            raise ValueError("expected only component or only components, got both.")
        elif not isinstance(component, Null):
            data["components"] = [component.to_payload()]
        elif not isinstance(components, Null):
            data["components"] = [component.to_payload() for component in components]

        await self.request(
            RequestRoute(
                Endpoints.create_message(channel_id if isinstance(channel_id, int) else channel_id.id),
                type="POST",
                json=data,
            ),
        )
