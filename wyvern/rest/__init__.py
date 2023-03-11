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
import dataclasses
import datetime
import typing

import aiohttp
import multidict

from wyvern import commands, interactions, models
from wyvern.exceptions import HTTPException

from .endpoints import Endpoints

if typing.TYPE_CHECKING:
    from wyvern.clients import GatewayClient
    from wyvern.components import ActionRowContainer, Modal
    from wyvern.constructors.embeds import EmbedConstructor

__all__: tuple[str, ...] = ("RESTClient",)


@dataclasses.dataclass
class RequestRoute:
    _url: str
    api_version: int = 10
    type: str = "GET"
    json: dict[str, typing.Any] | None = None

    @property
    def url(self) -> str:
        return f"https://discord.com/api/v{self.api_version}/{self._url}"


class RESTClient:
    """The REST Client that deals with disocrd REST Api requests."""

    def __init__(
        self,
        *,
        client: "GatewayClient",
        token: str,
        api_version: int = 10,
        client_session: aiohttp.ClientSession | None = None,
    ) -> None:
        self._client = client
        self._session: aiohttp.ClientSession
        self._token = token
        self._api_version = api_version
        self._headers: dict[str, multidict.istr] = {"Authorization": multidict.istr(f"Bot {token}")}

        if client_session is not None:
            self._session = client_session

    async def _create_websocket(self) -> aiohttp.ClientWebSocketResponse:
        if getattr(self, "_session", None) is None:
            self._session = aiohttp.ClientSession(headers=self._headers)
        return await self._session.ws_connect(  # type: ignore
            f"wss://gateway.discord.gg/?v={self._api_version}&encoding=json"
        )

    async def request(self, route: RequestRoute) -> typing.Any:
        headers = self._headers.copy()
        headers["Content-Type"] = multidict.istr("application/json")
        self._client._logger.debug(f"Creating a {route.type} request to {route._url} endpoint.")
        res = await self._session.request(route.type, route.url, headers=headers, json=route.json)
        if res.status in (200, 201):
            return await res.json()
        if res.status in (204, 304):
            return
        else:
            self.handle_error(exc := HTTPException((await res.json())["message"], res.status, route).create())
            raise exc

    def handle_error(self, exc: HTTPException) -> None:
        self._client._logger.error(
            "Exception while creating a HTTP request.\nType: %s, Endpoint: %s\nException: %s ",
            exc.route.type,
            exc.route.url,
            exc.message,
        )

    async def fetch_user(self, user_id: int) -> models.User:
        """Fetchs a user using the REST api.

        Parameters
        ----------

        user_id : int
            ID of the user that is to be fetched.

        Returns
        -------

        wyvern.models.users.User
            The user object that was fetched.

        Raises
        ------

        wyvern.exceptions.NotFound
            The targetted user was not found.
        """
        res = await self.request(RequestRoute(Endpoints.get_user(user_id)))
        return models._converters.payload_to_user(self._client, res)

    async def fetch_client_user(self) -> "models.BotUser":
        """
        Fetchs the bot's user object.

        Returns
        -------

        wyvern.models.users.BotUser
            BotUser object representating the bot's user.
        """
        res = await self.request(RequestRoute(Endpoints.get_current_user()))
        return models._converters.payload_to_botuser(self._client, res)

    async def edit_client_user(self, username: str | None = None, avatar: bytes | None = None) -> "models.BotUser":
        """Edits the bot's user.

        Parameters
        ----------

        username : str
            The new username.
        avatar : bytes
            The new avatar bytes.

        Returns
        -------

        wyvern.models.users.BotUser
            The updated user of bot.
        """

        payload: dict[str, bytes | str] = {}
        if username is not None:
            payload["username"] = username
        if avatar is not None:
            payload["avatar"] = avatar
        res: dict[str, int | str | bool] = await self.request(
            RequestRoute(Endpoints.get_current_user(), type="PATCH", json=payload)
        )
        return models._converters.payload_to_botuser(self._client, res)

    async def fetch_member(self, guild_id: int, member_id: int) -> models.Member:

        res = await self.request(
            RequestRoute(
                Endpoints.get_guild_member(guild_id, member_id),
            )
        )
        return models._converters.payload_to_member(self._client, models.Snowflake.create(guild_id), res)

    async def create_message(
        self,
        channel_id: int,
        content: str | None = None,
        *,
        embeds: typing.Sequence["EmbedConstructor"] = (),
        components: typing.Sequence[ActionRowContainer] = (),
        reference: int | models.MessageReference | None = None,
        allowed_mentions: models.AllowedMentions | None = None,
        flags: models.messages.MessageFlags | None = None,
        delete_after: int | None = None,
    ) -> "models.messages.Message":
        """Create a new message.

        Parameters
        ----------

        channel_id : int
            ID of the channel where the message is to be sent.
        content : str | None
            The text content of the message.
        embeds : typing.Sequence[wyvern.constructors.embeds.EmbedConstructor]
            Sequence of embeds to send.
        components : typing.Sequence[wyvern.components.container.ActionRowContainer]
            Sequence of action rows to send.
        reference : int | wyvern.models.messages.MessageReference | None
            ID or a message reference to which this is a response to.
        allowed_mentions : wyvern.models.messages.AllowedMentions | None
            Allowed mentions configs.

        Returns
        -------

        wyvern.models.messages.Message
            The message object that got created.

        """
        payload: dict[str, typing.Any] = {
            "content": content,
            "embeds": [embed._payload for embed in embeds],
            "components": [comp.to_payload() for comp in components],
            "allowed_mentions": (allowed_mentions or self._client.allowed_mentions).to_payload(),
            "flags": flags.value if flags else None,
        }

        if reference is not None:
            if isinstance(reference, models.MessageReference):
                payload["message_reference"] = reference.to_payload()
            else:
                payload["message_reference"] = models.MessageReference(message_id=reference).to_payload()

        res: dict[str, typing.Any] = await self.request(
            RequestRoute(Endpoints.create_message(channel_id), type="POST", json=payload),
        )

        msg = models._converters.payload_to_message(self._client, res)

        async def _delete_after(sec: int) -> None:

            await asyncio.sleep(sec)
            await self.delete_message(msg.channel_id, msg.id)

        if delete_after is not None:
            asyncio.create_task(_delete_after(delete_after))

        return msg

    async def delete_message(self, channel_id: int, message_id: int) -> None:
        await self.request(RequestRoute(Endpoints.delete_message(channel_id, message_id), type="DELETE"))

    async def fetch_message(self, channel_id: int, message_id: int) -> models.Message:

        res = await self.request(RequestRoute(Endpoints.get_channel_message(channel_id, message_id)))
        return models._converters.payload_to_message(self._client, res)

    async def fetch_messages(
        self, channel_id: int, around: datetime.datetime
    ) -> dict[models.Snowflake, models.Message]:
        try:
            res = await self.request(RequestRoute(Endpoints.get_channel_messages(channel_id)))
            return {
                msg.id: msg for msg in [models._converters.payload_to_message(self._client, payload) for payload in res]
            }
        except HTTPException as e:
            raise e

    async def create_application_command(
        self,
        *,
        name: str,
        description: str,
        options: typing.Sequence[commands.slash_commands.CommandOption] = (),
        dm_permission: bool = True,
        type: interactions.base.InteractionCommandType,
    ) -> typing.Any:
        payload = {
            "name": name,
            "description": description,
            "options": [option.to_payload() for option in options],
            "dm_permission": dm_permission,
            "type": type,
        }
        return await self.request(
            RequestRoute(Endpoints.interaction_command(self._client._client_id), type="POST", json=payload)
        )

    async def _create_app_command_from_payload(self, payload: dict[str, typing.Any]) -> typing.Any:
        return await self.request(
            RequestRoute(Endpoints.interaction_command(self._client._client_id), type="POST", json=payload)
        )

    async def create_interaction_response(
        self,
        interaction: interactions.Interaction,
        response_type: interactions.InteractionResponseType,
        *,
        content: str | None = None,
        embeds: typing.Sequence[EmbedConstructor] = (),
        components: typing.Sequence[ActionRowContainer] = (),
        flags: models.messages.MessageFlags | None = None,
        allowed_mentions: models.messages.AllowedMentions | None = None,
        modal: Modal | None = None,
    ) -> None:
        payload: dict[str, typing.Any] = {"type": int(response_type), "data": {}}
        if response_type is interactions.InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE:
            pass
        elif response_type is interactions.InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE:
            payload["data"]["content"] = content
            payload["data"]["embeds"] = [embed._payload for embed in embeds]
            payload["data"]["components"] = [builder.to_payload() for builder in components]
            payload["data"]["allowed_mentions"] = (allowed_mentions or self._client.allowed_mentions).to_payload()
            payload["data"]["flags"] = flags.value if flags else None
        elif response_type is interactions.InteractionResponseType.MODAL:
            if modal is None:
                raise ValueError("No Modal instance provided to send.")
            payload["data"]["custom_id"] = modal.custom_id
            payload["data"]["title"] = modal.title
            payload["data"]["components"] = [{"type": 1}]
            payload["data"]["components"][0]["components"] = [comp.to_payload() for comp in modal.text_inputs]
        await self.request(
            RequestRoute(
                Endpoints.interaction_callback(
                    interaction.id,
                    interaction.token,
                ),
                type="POST",
                json=payload,
            )
        )
