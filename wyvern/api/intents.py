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

from wyvern.internals.enum_flags import Flag

__all__: tuple[str, ...] = ("Intents",)


@typing.final
class Intents(Flag):
    """
    Intents constructor to provide to the GatewayBot class.

    Attributes
    ----------
    value: int
        The final value of intents generated by the constructor.
    """

    NONE = 0
    """
    No intents.
    """
    GUILDS = 1 << 0
    """Required for these gateway events:

    * ``GUILD_CREATE``
    * ``GUILD_UPDATE``
    * ``GUILD_DELETE``
    * ``GUILD_ROLE_CREATE``
    * ``GUILD_ROLE_UPDATE``
    * ``GUILD_ROLE_DELETE``
    * ``CHANNEL_CREATE``
    * ``CHANNEL_UPDATE``
    * ``CHANNEL_DELETE``
    * ``CHANNEL_PINS_UPDATE``
    * ``THREAD_CREATE``
    * ``THREAD_UPDATE``
    * ``THREAD_DELETE``
    * ``THREAD_LIST_SYNC``
    * ``THREAD_MEMBER_UPDATE``
    * ``THREAD_MEMBERS_UPDATE``
    * ``STAGE_INSTANCE_CREATE``
    * ``STAGE_INSTANCE_UPDATE``
    * ``STAGE_INSTANCE_DELETE``
    """
    GUILD_MEMBERS = 1 << 1
    """Required for these gateway events:

    * ``GUILD_MEMBER_ADD``
    * ``GUILD_MEMBER_UPDATE``
    * ``GUILD_MEMBER_REMOVE``
    * ``THREAD_MEMBERS_UPDATE``
    .. warning::
        This is a privileged intent.
    """
    GUILD_BANS = 1 << 2
    """Required for these gateway events:

    * ``GUILD_BAN_ADD``
    * ``GUILD_BAN_REMOVE``
    """
    GUILD_EMOJIS = 1 << 3
    """Required for these gateway events:

    * ``GUILD_EMOJIS_UPDATE``
    * ``GUILD_STICKERS_UPDATE``
    """
    GUILD_INTEGRATIONS = 1 << 4
    """Required for these gateway events:

    * ``GUILD_INTEGRATIONS_UPDATE``
    * ``INTEGRATION_CREATE``
    * ``INTEGRATION_UPDATE``
    * ``INTEGRATION_DELETE``
    """
    GUILD_WEBHOOKS = 1 << 5
    """Required for these gateway events:

    * ``WEBHOOKS_UPDATE``
    """
    GUILD_INVITES = 1 << 6
    """Required for these gateway events:

    * ``INVITE_CREATE``
    * ``INVITE_DELETE``
    """
    GUILD_VOICE_STATES = 1 << 7
    """Required for these gateway events:

    * ``VOICE_STATE_UPDATE``
    """
    GUILD_PRESENCES = 1 << 8
    """Required for these gateway events:

    * ``PRESENCE_UPDATE``
    .. warning::
        This is a privileged intent.
    """
    GUILD_MESSAGES = 1 << 9
    """Required for these gateway events:

    * ``MESSAGE_CREATE``
    * ``MESSAGE_UPDATE``
    * ``MESSAGE_DELETE``
    * ``MESSAGE_DELETE_BULK``
    """
    GUILD_MESSAGE_REACTIONS = 1 << 10
    """Required for these gateway events:

    * ``MESSAGE_REACTION_ADD``
    * ``MESSAGE_REACTION_REMOVE``
    * ``MESSAGE_REACTION_REMOVE_ALL``
    * ``MESSAGE_REACTION_REMOVE_EMOJI``
    """
    GUILD_MESSAGE_TYPING = 1 << 11
    """Required for these gateway events:

    * ``TYPING_START``
    """
    DIRECT_MESSAGES = 1 << 12
    """Required for these gateway events:

    * ``MESSAGE_CREATE``
    * ``MESSAGE_UPDATE``
    * ``MESSAGE_DELETE``
    * ``CHANNEL_PINS_UPDATE``
    """
    DIRECT_MESSAGE_REACTIONS = 1 << 13
    """Required for these gateway events:

    * ``MESSAGE_REACTION_ADD``
    * ``MESSAGE_REACTION_REMOVE``
    * ``MESSAGE_REACTION_REMOVE_ALL``
    * ``MESSAGE_REACTION_REMOVE_EMOJI``
    """
    DIRECT_MESSAGE_TYPING = 1 << 14
    """Required for these gateway events:

    * ``TYPING_START``
    """
    MESSAGE_CONTENT = 1 << 15
    """Required for guild message's content.

    .. warning::
        This is a privileged intent.
    """
    GUILD_SCHEDULED_EVENTS = 1 << 16
    """Required for these gateway events:

    * ``GUILD_SCHEDULED_EVENT_CREATE``
    * ``GUILD_SCHEDULED_EVENT_UPDATE``
    * ``GUILD_SCHEDULED_EVENT_DELETE``
    * ``GUILD_SCHEDULED_EVENT_USER_ADD``
    * ``GUILD_SCHEDULED_EVENT_USER_REMOVE``
    """
    AUTO_MODERATION_CONFIGURATION = 1 << 20
    """Required for these gateway events:

    * ``AUTO_MODERATION_RULE_CREATE``
    * ``AUTO_MODERATION_RULE_UPDATE``
    * ``AUTO_MODERATION_RULE_DELETE``
    """

    AUTO_MODERATION_EXECUTION = 1 << 21
    """Required for these gateway events:

    * ``AUTO_MODERATION_ACTION_EXECUTION``
    """

    UNPRIVILEGED = (
        GUILDS
        | GUILD_EMOJIS
        | GUILD_INTEGRATIONS
        | GUILD_WEBHOOKS
        | GUILD_INVITES
        | GUILD_VOICE_STATES
        | GUILD_MESSAGE_REACTIONS
        | GUILD_MESSAGE_TYPING
        | GUILD_MESSAGES
        | DIRECT_MESSAGES
        | DIRECT_MESSAGE_TYPING
        | DIRECT_MESSAGE_REACTIONS
        | AUTO_MODERATION_CONFIGURATION
        | AUTO_MODERATION_EXECUTION
    )
    """All unprivileged intents."""
    PRIVILEGED = MESSAGE_CONTENT | GUILD_MEMBERS | GUILD_PRESENCES
    """All privileged intents."""
    ALL = PRIVILEGED | UNPRIVILEGED
    """All intents."""
