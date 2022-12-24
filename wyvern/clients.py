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
import builtins
import importlib
import inspect
import logging
import typing

# isort: off
from wyvern import (
    commands,
    events,
    exceptions,
    gateway,
    interactions,
    models,
    presences,
    rest,
    state_handlers,
    utils,
    ux,
)

# isort: on
from wyvern import intents as _intents
from wyvern import plugins as _plugins

if typing.TYPE_CHECKING:
    import aiohttp

    from wyvern._types import AppCommandCallbackT


_LOGGER = logging.getLogger(__name__)

ux.create_logging_setup(_LOGGER)

__all__: tuple[str, ...] = ("GatewayClient", "CommandsClient")


class GatewayClient(events._InClassEventContainer):
    """The main bot class which acts as an interface between the Discord API and your bot.

    Parameters
    ----------
        token : str
        The bot token to use.
    intents : typing.SupportsInt | wyvern.intents.Intents
        The intents to use while logging in to the gateway.
    allowed_mentions : wyvern.models.messages.AllowedMentions
        The default mentions to allow in a message bot is sending.
    event_handler type[EventHandler]
        A EventHandler subclass ( not instance ), if any.
    rest_client : RESTClient | None
        A custom RESTClient subclass to use, if any.
    api_version : int
        Discord API version to use.
    client_session : aiohttp.ClientSession | None
        ClientSession subclass to use, if any.
    """

    __identity__: str = "bot_class"
    hooks: dict[str, utils.Hook] = {}
    """Mapping of loaded hook names to their objects."""
    plugins: dict[str, _plugins.Plugin] = {}
    """Mapping of loaded plugin names to their objects."""

    def __init__(
        self,
        token: str,
        *,
        intents: typing.SupportsInt | _intents.Intents = _intents.Intents.UNPRIVILEGED,
        event_handler: type[events.EventHandler] = events.EventHandler,
        allowed_mentions: models.AllowedMentions = models.messages.AllowedMentions(),
        rest_client: rest.RESTClient | None = None,
        api_version: int = 10,
        client_session: aiohttp.ClientSession | None = None,
    ) -> None:
        self._client_id: int = 0
        self.event_handler = event_handler(self)
        self.rest = rest_client or rest.RESTClient(
            client=self, token=token, api_version=api_version, client_session=client_session
        )
        self.intents = intents if isinstance(intents, _intents.Intents) else _intents.Intents(int(intents))
        self.gateway = gateway.Gateway(self)
        self.allowed_mentions = allowed_mentions
        self._users = state_handlers.UsersState(self)
        self._members = state_handlers.MembersState(self)
        self._logger = _LOGGER

    @property
    def users(self) -> state_handlers.UsersState:
        """The state handler for users stored in the bot's cache,
        Can also be used to perform fetch operations and parsing users from string.

        Returns
        -------
                wyvern.state_handlers.UsersState
            The handler.
        """
        return self._users

    @property
    def members(self) -> state_handlers.MembersState:
        """The member state for members in bot's cache. Similar to `users` cache.

        Returns
        -------
        wyvern.state_handlers.MembersState
                The member handler.
        """
        return self._members

    @property
    def latency(self) -> float:
        """The heartbeat latency of the gateway connection.

                Returns
                -------
        float
            The latency.
        """
        return self.gateway.latency

    async def wait_for(
        self, event: events.Event, *, timeout: int = 180, check: typing.Callable[..., bool] = lambda *_: True
    ) -> typing.Any:
        ...

    def with_listener(
        self, event: events.Event, *, max_trigger: int | float = float("inf")
    ) -> typing.Callable[[typing.Callable[..., typing.Awaitable[typing.Any]]], events.EventListener]:
        """Creates and adds a new listenet to the client's event handler.

        Parameters
        ----------
            event: str | wyvern.events.Event
            The event to listen.
        max_trigger: int | float
            Maximum number of times this listener has to be triggered.

        Returns
        -------
                wyvern.events.EventListener
            A EventListener object.

        ??? example

            ```py
            import wyvern

            client = wyvern.GatewayClient("TOKEN")


            @client.with_listener(wyvern.Event.MESSAGE_CREATE)
            async def message_create(message: wyvern.Message) -> None:
               if message.content == ".ping":
                   await message.respond("pong")


            client.run()
            ```
        """

        def inner(callback: typing.Callable[..., typing.Awaitable[typing.Any]]) -> events.EventListener:
            lsnr = events.as_listener(event, max_trigger=max_trigger)(callback)
            self.event_handler.add_listener(lsnr)
            return lsnr

        return inner

    async def start(
        self, *, activity: presences.Activity | None = None, status: presences.Status | None = None
    ) -> None:
        """Connects the bot with gateway and starts listening to events.

        Parameters
        ----------
            activity : wyvern.presences.Activity | None
            The activity bot boots up with.
        status : wyvern.presences.Status | None
            The status bot boots up with.
        """
        self.event_handler.setup_listeners()
        self.event_handler.dispatch(events.Event.STARTING, self)
        self.gateway._start_activity = activity
        self.gateway._start_status = status
        await self.gateway._get_socket_ready()
        _LOGGER.info("Logging in with bot token.")
        try:
            res = await self.rest.fetch_client_user()
            _LOGGER.info("Logged in to the gateway with bot token.")
            _LOGGER.info("(Session info) User ID: %s, Username: %s", res.id, res.username)
            self._client_id = res.id
            self.event_handler.dispatch(events.Event.STARTED, self)
            await self.gateway.listen_gateway()
        except exceptions.Unauthorized as e:
            await self.rest._session.close()
            e.message += ", Improper token was passed."
            raise e

    def run(self, *, activity: presences.Activity | None = None, status: presences.Status | None = None) -> None:
        """A non-async method which call [wyvern.clients.GatewayClient.start][].

        Parameters
        ----------
                activity : wyvern.presences.Activity | None
            The activity bot boots up with.
        status : wyvern.presences.Status | None
            The status bot boots up with.
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start(activity=activity, status=status))

    def load_hooks(self, path: str) -> dict[str, utils.Hook]:
        """Loads hooks from the provided path

        ??? note
            The path should be a python import path.

        Parameters
        ----------
        path : str
            Path to load hooks from.

        Returns
        -------
        dict[str, wyvern.utils.Hook]
            The hooks that were loaded.
        """
        module = importlib.import_module(path)
        hooks = {hook.name: hook for hook in module.__dict__.values() if isinstance(hook, utils.Hook)}
        if any(overrided := [hook for hook in hooks.keys() if hook in self.hooks.keys()]):
            self._logger.warning("Overring loaded hooks: %s", ", ".join(overrided))
        self.hooks.update(hooks)
        return hooks

    def get_hooks(self, *, awaitable: bool = True, non_awaitable: bool = True) -> list[utils.Hook]:
        """Get's loaded hooks.

        Parameters
        ----------
        awaitable : bool
            If awaitable hooks should be added to return value.
        non_awaitable : bool
            If non-awaitable hooks should be added to return value.

        Returns
        -------
        list[wyvern.utils.Hook]
            List of the hooks.
        """
        hooks: list[utils.Hook] = []
        if awaitable is True:
            hooks.extend([hook for hook in self.hooks.values() if inspect.isawaitable(hook.callback)])
        if non_awaitable is True:
            hooks.extend([hook for hook in self.hooks.values() if not inspect.isawaitable(hook.callback)])
        return hooks

    def add_plugin(self, plugin: _plugins.Plugin) -> None:
        """Adds a plugin to the bot.

        Parameters
        ----------
        plugin : wyvern.plugins.Plugin
            The plugin to be added.
        """
        if plugin.name in self.plugins.keys():
            raise exceptions.PluginException("Plugin %s is already loaded." % (plugin.name))
        self.plugins[plugin.name] = plugin
        plugin.setup_plugin(self)


class CommandsClient(GatewayClient, commands.CommandHandler):
    """Implementation of the [wyvern.GatewayClient][] class with a command handler."""

    slash_commands: dict[str, "commands.slash_commands.SlashCommand"] = {}
    """List of slash commands attached to the client in code."""
    slash_groups: dict[str, "commands.slash_commands.SlashGroup"] = {}
    """List of slash command groups attached to the client in code."""

    @events.as_listener(events.Event.INTERACTION_CREATE)
    async def _handle_inters(self, inter: interactions.Interaction) -> None:
        if isinstance(inter, interactions.ApplicationCommandInteraction):
            await self.process_application_commands(inter)

    def add_slash_command(self, command: commands.slash_commands.SlashCommand) -> None:
        if (name := command.name) in self.slash_commands.keys():
            raise exceptions.CommandAlreadyExists(f"A slash command named {name} already exists.")
        _LOGGER.debug(f"Adding slash command {name} to bot.")
        self.slash_commands[name] = command

    def add_slash_group(self, group: commands.slash_commands.SlashGroup) -> None:
        if (name := group.name) in self.slash_groups.keys():
            raise exceptions.CommandAlreadyExists(f"A slash command named {name} already exists.")
        _LOGGER.debug(f"Adding slash group {name} to bot.")
        self.slash_groups[name] = group

    @typing.overload
    def add_item(self, listener_or_command: events.EventListener) -> events.EventListener:
        ...

    @typing.overload
    def add_item(
        self, listener_or_command: commands.slash_commands.SlashCommand
    ) -> commands.slash_commands.SlashCommand:
        ...

    def add_item(
        self, listener_or_command: events.EventListener | commands.slash_commands.SlashCommand | typing.Any
    ) -> events.EventListener | commands.slash_commands.SlashCommand:
        def inner() -> None:
            nonlocal listener_or_command
            if isinstance(listener_or_command, events.EventListener):
                self.event_handler.add_listener(listener_or_command)
            elif isinstance(listener_or_command, commands.slash_commands.SlashCommand):
                self.add_slash_command(listener_or_command)

        inner()
        return listener_or_command

    def set_prefix(self, prefix_or_function: str | typing.Sequence[str] | builtins.function) -> "CommandsClient":
        """
        Set a prefix to parse message commands.
        Allowed prefix data
        -------------------
        * strings : [str][]
        * iterables : [list][] / [set][] / [tuple][]
        * callables : [builtins.function][] or a [asyncio.coroutine][].
        """
        if isinstance(prefix_or_function, str):
            self.prefix_type = str
        elif (
            isinstance(prefix_or_function, list)
            or isinstance(prefix_or_function, tuple)
            or isinstance(prefix_or_function, set)
        ):
            self.prefix_type = type(prefix_or_function)
        elif isinstance(prefix_or_function, builtins.function):
            self.prefix_type = builtins.function
        return self

    def with_slash_command(
        self,
        *,
        name: str,
        description: str,
    ) -> typing.Callable[[AppCommandCallbackT], commands.slash_commands.SlashCommand]:
        """Creates a slash command.

        Parameters
        ----------
        name : str
            Name of the command.
        description : str
            Description of the command.

        Returns
        -------
        typing.Callable[..., commands.slash_commands.SlashCommand]
            A [wyvern.commands.slash_commands.SlashCommand][] when called.
        """

        def inner(callback: AppCommandCallbackT) -> commands.slash_commands.SlashCommand:
            cmd = commands.as_slash_command(name=name, description=description)(callback)

            self.add_slash_command(cmd._set_client(self))
            return cmd

        return inner
