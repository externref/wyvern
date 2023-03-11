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

__all__: tuple[str, ...] = ("Endpoints",)


class Endpoints:
    @classmethod
    def guild_audit_logs(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/audit-logs"

    @classmethod
    def list_auto_moderation_rules(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/auto-moderation/rules"

    @classmethod
    def get_auto_moderation_rule(cls, guild_id: int, rule_id: int) -> str:
        return f"guilds/{guild_id}/auto-moderation/rules/{rule_id}"

    @classmethod
    def create_auto_moderation_rule(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/auto-moderation/rules"

    @classmethod
    def modify_auto_moderation_rule(cls, guild_id: int, rule_id: int) -> str:
        return f"guilds/{guild_id}/auto-moderation/rules/{rule_id}"

    @classmethod
    def delete_auto_moderation_rule(cls, guild_id: int, rule_id: int) -> str:
        return f"guilds/{guild_id}/auto-moderation/rules/{rule_id}"

    @classmethod
    def get_channel(cls, channel_id: int) -> str:
        return f"channels/{channel_id}"

    @classmethod
    def modify_channel(cls, channel_id: int) -> str:
        return f"channels/{channel_id}"

    @classmethod
    def delete_channel(cls, channel_id: int) -> str:
        return f"channels/{channel_id}"

    @classmethod
    def get_channel_messages(cls, channel_id: int) -> str:
        return f"channels/{channel_id}/messages"

    @classmethod
    def get_channel_message(cls, channel_id: int, message_id: int) -> str:
        return f"channels/{channel_id}/messages/{message_id}"

    @classmethod
    def create_message(cls, channel_id: int) -> str:
        return f"channels/{channel_id}/messages"

    @classmethod
    def crosspost_message(cls, channel_id: int, message_id: int) -> str:
        return f"channels/{channel_id}/messages/{message_id}/crosspost"

    @classmethod
    def create_reaction(cls, channel_id: int, message_id: int, emoji: str) -> str:
        return f"channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"

    @classmethod
    def delete_own_reaction(cls, channel_id: int, message_id: int, emoji: str) -> str:
        return f"channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"

    @classmethod
    def delete_user_reaction(cls, channel_id: int, message_id: int, emoji: str, user_id: int) -> str:
        return f"channels/{channel_id}/messages/{message_id}/reactions/{emoji}/{user_id}"

    @classmethod
    def get_user_reactions(cls, channel_id: int, message_id: int, emoji: str) -> str:
        return f"channels/{channel_id}/messages/{message_id}/reactions/{emoji}"

    @classmethod
    def delete_all_reactions(cls, channel_id: int, message_id: int) -> str:
        return f"channels/{channel_id}/messages/{message_id}/reactions"

    @classmethod
    def delete_all_reactions_for_emoji(cls, channel_id: int, message_id: int, emoji: str) -> str:
        return f"channels/{channel_id}/messages/{message_id}/reactions/{emoji}"

    @classmethod
    def edit_message(cls, channel_id: int, message_id: int) -> str:
        return f"channels/{channel_id}/messages/{message_id}"

    @classmethod
    def delete_message(cls, channel_id: int, message_id: int) -> str:
        return f"channels/{channel_id}/messages/{message_id}"

    @classmethod
    def bulk_delete_messages(cls, channel_id: int) -> str:
        return f"channels/{channel_id}/messages/bulk-delete"

    @classmethod
    def edit_channel_permissions(cls, channel_id: int, overwrite_id: int) -> str:
        return f"channels/{channel_id}/permissions/{overwrite_id}"

    @classmethod
    def get_channel_invites(cls, channel_id: int) -> str:
        return f"channels/{channel_id}/invites"

    @classmethod
    def create_channel_invite(cls, channel_id: int) -> str:
        return f"channels/{channel_id}/invites"

    @classmethod
    def delete_channel_permission(cls, channel_id: int, overwrite_id: int) -> str:
        return f"channels/{channel_id}/permissions/{overwrite_id}"

    @classmethod
    def follow_news_channel(cls, channel_id: int) -> str:
        return f"channels/{channel_id}/followers"

    @classmethod
    def trigger_typing_indicator(cls, channel_id: int) -> str:
        return f"channels/{channel_id}/typing"

    @classmethod
    def get_pinned_messages(cls, channel_id: int) -> str:
        return f"channels/{channel_id}/pins"

    @classmethod
    def add_pinned_channel_message(cls, channel_id: int, message_id: int) -> str:
        return f"channels/{channel_id}/pins/{message_id}"

    @classmethod
    def delete_pinned_channel_message(cls, channel_id: int, message_id: int) -> str:
        return f"channels/{channel_id}/pins/{message_id}"

    @classmethod
    def group_dm_add_recipient(cls, channel_id: int, user_id: int) -> str:
        return f"channels/{channel_id}/recipients/{user_id}"

    @classmethod
    def group_dm_remove_recipient(cls, channel_id: int, user_id: int) -> str:
        return f"channels/{channel_id}/recipients/{user_id}"

    @classmethod
    def start_thread_with_message(cls, channel_id: int, message_id: int) -> str:
        return f"channels/{channel_id}/messages/{message_id}/threads"

    @classmethod
    def start_thread_without_message(cls, channel_id: int) -> str:
        return f"channels/{channel_id}/threads"

    @classmethod
    def start_thread_in_forum(cls, channel_id: int) -> str:
        return f"channels/{channel_id}/threads"

    @classmethod
    def join_thread(cls, channel_id: int, thread_id: int) -> str:
        return f"channels/{channel_id}/threads/{thread_id}/members/@me"

    @classmethod
    def add_thread_member(cls, channel_id: int, thread_id: int, user_id: int) -> str:
        return f"channels/{channel_id}/threads/{thread_id}/members/{user_id}"

    @classmethod
    def leave_thread(cls, channel_id: int, thread_id: int) -> str:
        return f"channels/{channel_id}/threads/{thread_id}/members/@me"

    @classmethod
    def remove_thread_member(cls, channel_id: int, thread_id: int, user_id: int) -> str:
        return f"channels/{channel_id}/threads/{thread_id}/members/{user_id}"

    @classmethod
    def get_thread_member(cls, channel_id: int, thread_id: int, user_id: int) -> str:
        return f"channels/{channel_id}/threads/{thread_id}/members/{user_id}"

    @classmethod
    def list_thread_members(cls, channel_id: int) -> str:
        return f"channels/{channel_id}/threads-members"

    @classmethod
    def list_public_archived_threads(cls, channel_id: int) -> str:
        return f"channels/{channel_id}/threads/archived/public"

    @classmethod
    def list_private_archived_threads(cls, channel_id: int) -> str:
        return f"channels/{channel_id}/threads/archived/private"

    @classmethod
    def list_joined_private_archived_threads(cls, channel_id: int) -> str:
        return f"channels/{channel_id}/users/@me/threads/archived/private"

    @classmethod
    def list_guild_emojis(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/emojis"

    @classmethod
    def get_guild_emoji(cls, guild_id: int, emoji_id: int) -> str:
        return f"guilds/{guild_id}/emojis/{emoji_id}"

    @classmethod
    def create_guild_emoji(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/emojis"

    @classmethod
    def modify_guild_emoji(cls, guild_id: int, emoji_id: int) -> str:
        return f"guilds/{guild_id}/emojis/{emoji_id}"

    @classmethod
    def delete_guild_emoji(cls, guild_id: int, emoji_id: int) -> str:
        return f"guilds/{guild_id}/emojis/{emoji_id}"

    @classmethod
    def create_guild(cls) -> str:
        return "guilds"

    @classmethod
    def get_guild(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}"

    @classmethod
    def get_guild_preview(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/preview"

    @classmethod
    def edit_guild(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}"

    @classmethod
    def delete_guild(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}"

    @classmethod
    def get_guild_channels(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/channels"

    @classmethod
    def create_guild_channel(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/channels"

    @classmethod
    def modify_guild_channel_positions(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/channels"

    @classmethod
    def active_guild_threads(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/threads/active"

    @classmethod
    def get_guild_member(cls, guild_id: int, user_id: int) -> str:
        return f"guilds/{guild_id}/members/{user_id}"

    @classmethod
    def list_guild_members(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/members"

    @classmethod
    def search_guild_members(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/members/search"

    @classmethod
    def add_guild_member(cls, guild_id: int, user_id: int) -> str:
        return f"guilds/{guild_id}/members/{user_id}"

    @classmethod
    def modify_guild_member(cls, guild_id: int, user_id: int) -> str:
        return f"guilds/{guild_id}/members/{user_id}"

    @classmethod
    def modify_current_member(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/members/@me"

    @classmethod
    def guild_member_addrole(cls, guild_id: int, user_id: int, role_id: int) -> str:
        return f"guilds/{guild_id}/members/{user_id}/roles/{role_id}"

    @classmethod
    def guild_member_removerole(cls, guild_id: int, user_id: int, role_id: int) -> str:
        return f"guilds/{guild_id}/members/{user_id}/roles/{role_id}"

    @classmethod
    def remove_guild_member(cls, guild_id: int, user_id: int) -> str:
        return f"guilds/{guild_id}/members/{user_id}"

    @classmethod
    def get_guild_bans(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/bans"

    @classmethod
    def get_guild_ban(cls, guild_id: int, user_id: int) -> str:
        return f"guilds/{guild_id}/bans/{user_id}"

    @classmethod
    def create_guild_ban(cls, guild_id: int, user_id: int) -> str:
        return f"guilds/{guild_id}/bans/{user_id}"

    @classmethod
    def remove_guild_ban(cls, guild_id: int, user_id: int) -> str:
        return f"guilds/{guild_id}/bans/{user_id}"

    @classmethod
    def get_guild_roles(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/roles"

    @classmethod
    def create_guild_role(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/roles"

    @classmethod
    def modify_guild_role_positions(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/roles"

    @classmethod
    def modify_guild_role(cls, guild_id: int, role_id: int) -> str:
        return f"guilds/{guild_id}/roles/{role_id}"

    @classmethod
    def modify_guild_mfa(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/mfa"

    @classmethod
    def delete_guild_role(cls, guild_id: int, role_id: int) -> str:
        return f"guilds/{guild_id}/roles/{role_id}"

    @classmethod
    def get_guild_prune_count(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/prune"

    @classmethod
    def begin_guild_prune(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/prune"

    @classmethod
    def guild_voice_regions(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/regions"

    @classmethod
    def get_guild_invites(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/invites"

    @classmethod
    def get_guild_integrations(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/integrations"

    @classmethod
    def delete_guild_integration(cls, guild_id: int, integration_id: int) -> str:
        return f"guilds/{guild_id}/integrations/{integration_id}"

    @classmethod
    def get_guild_widget_settings(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/widget"

    @classmethod
    def modify_guild_widget(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/widget"

    @classmethod
    def get_guild_widget(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/widget.json"

    @classmethod
    def guild_vanity_url(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/vanity-url"

    @classmethod
    def get_guild_widget_image(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/widget.png"

    @classmethod
    def get_guild_welcome_screen(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/welcome-screen"

    @classmethod
    def modify_guild_welcome_screen(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/welcome-screen"

    @classmethod
    def modify_current_user_voice_state(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/voice-states/@me"

    @classmethod
    def modify_user_voice_state(cls, guild_id: int, user_id: int) -> str:
        return f"guilds/{guild_id}/voice-states/{user_id}"

    @classmethod
    def list_scheduled_guild_events(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/scheduled-events"

    @classmethod
    def create_scheduled_guild_event(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/scheduled-events"

    @classmethod
    def get_scheduled_guild_event(cls, guild_id: int, event_id: int) -> str:
        return f"guilds/{guild_id}/scheduled-events/{event_id}"

    @classmethod
    def modify_scheduled_guild_event(cls, guild_id: int, event_id: int) -> str:
        return f"guilds/{guild_id}/scheduled-events/{event_id}"

    @classmethod
    def delete_scheduled_guild_event(cls, guild_id: int, event_id: int) -> str:
        return f"guilds/{guild_id}/scheduled-events/{event_id}"

    @classmethod
    def get_scheduled_guild_event_users(cls, guild_id: int, event_id: int) -> str:
        return f"guilds/{guild_id}/scheduled-events/{event_id}/users"

    @classmethod
    def get_guild_template(cls, guild_id: int, template_code: str) -> str:
        return f"guilds/{guild_id}/templates/{template_code}"

    @classmethod
    def create_guild_from_template(cls, guild_id: int, template_code: str) -> str:
        return f"guilds/{guild_id}/templates/{template_code}"

    @classmethod
    def get_guild_templates(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/templates"

    @classmethod
    def create_guild_template(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/templates"

    @classmethod
    def sync_guild_template(cls, guild_id: int, template_code: str) -> str:
        return f"guilds/{guild_id}/templates/{template_code}"

    @classmethod
    def modify_guild_template(cls, guild_id: int, template_code: str) -> str:
        return f"guilds/{guild_id}/templates/{template_code}"

    @classmethod
    def delete_guild_template(cls, guild_id: int, template_code: str) -> str:
        return f"guilds/{guild_id}/templates/{template_code}"

    @classmethod
    def get_invite(cls, invite_code: str) -> str:
        return f"invites/{invite_code}"

    @classmethod
    def delete_invite(cls, invite_code: str) -> str:
        return f"invites/{invite_code}"

    @classmethod
    def create_stage_instance(cls) -> str:
        return "stage-instances"

    @classmethod
    def get_stage_instance(cls, channel_id: int) -> str:
        return f"stage-instances/{channel_id}"

    @classmethod
    def modify_stage_instance(cls, channel_id: int) -> str:
        return f"stage-instances/{channel_id}"

    @classmethod
    def delete_stage_instance(cls, channel_id: int) -> str:
        return f"stage-instances/{channel_id}"

    @classmethod
    def get_sticker(cls, sticker_id: int) -> str:
        return f"stickers/{sticker_id}"

    @classmethod
    def list_nitro_sticker_packs(cls) -> str:
        return "sticker-packs"

    @classmethod
    def list_guild_stickers(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/stickers"

    @classmethod
    def create_guild_sticker(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/stickers"

    @classmethod
    def get_guild_sticker(cls, guild_id: int, sticker_id: int) -> str:
        return f"guilds/{guild_id}/stickers/{sticker_id}"

    @classmethod
    def modify_guild_sticker(cls, guild_id: int, sticker_id: int) -> str:
        return f"guilds/{guild_id}/stickers/{sticker_id}"

    @classmethod
    def delete_guild_sticker(cls, guild_id: int, sticker_id: int) -> str:
        return f"guilds/{guild_id}/stickers/{sticker_id}"

    @classmethod
    def get_current_user(cls) -> str:
        return "users/@me"

    @classmethod
    def get_user(cls, user_id: int) -> str:
        return f"users/{user_id}"

    @classmethod
    def modify_current_user(cls) -> str:
        return "users/@me"

    @classmethod
    def get_current_user_guilds(cls) -> str:
        return "users/@me/guilds"

    @classmethod
    def get_current_user_guilds_membership(cls, guild_id: int) -> str:
        return f"users/@me/guilds/{guild_id}/member"

    @classmethod
    def leave_guild(cls, guild_id: int) -> str:
        return f"users/@me/guilds/{guild_id}"

    @classmethod
    def create_dm(cls) -> str:
        return "users/@me/channels"

    @classmethod
    def create_group_dm(cls) -> str:
        return "users/@me/channels"

    @classmethod
    def get_user_connections(cls) -> str:
        return "users/@me/connections"

    @classmethod
    def list_voice_regions(cls) -> str:
        return "voice/regions"

    @classmethod
    def create_webhook(cls, channel_id: int) -> str:
        return f"channels/{channel_id}/webhooks"

    @classmethod
    def get_channel_webhooks(cls, channel_id: int) -> str:
        return f"channels/{channel_id}/webhooks"

    @classmethod
    def get_webhook(cls, webhook_id: int) -> str:
        return f"webhooks/{webhook_id}"

    @classmethod
    def get_webhook_with_token(cls, webhook_id: int, webhook_token: str) -> str:
        return f"webhooks/{webhook_id}/{webhook_token}"

    @classmethod
    def modify_webhook(cls, webhook_id: int) -> str:
        return f"webhooks/{webhook_id}"

    @classmethod
    def modify_webhook_with_token(cls, webhook_id: int, webhook_token: str) -> str:
        return f"webhooks/{webhook_id}/{webhook_token}"

    @classmethod
    def delete_webhook(cls, webhook_id: int) -> str:
        return f"webhooks/{webhook_id}"

    @classmethod
    def delete_webhook_with_token(cls, webhook_id: int, webhook_token: str) -> str:
        return f"webhooks/{webhook_id}/{webhook_token}"

    @classmethod
    def execute_webhook(cls, webhook_id: int, webhook_token: str) -> str:
        return f"webhooks/{webhook_id}/{webhook_token}"

    @classmethod
    def execute_slack_compatible_webhook(cls, webhook_id: int, webhook_token: str) -> str:
        return f"webhooks/{webhook_id}/{webhook_token}/slack"

    @classmethod
    def execute_github_compatible_webhook(cls, webhook_id: int, webhook_token: str) -> str:
        return f"webhooks/{webhook_id}/{webhook_token}/github"

    @classmethod
    def get_webhook_message(cls, webhook_id: int, webhook_token: str, message_id: int) -> str:
        return f"webhooks/{webhook_id}/{webhook_token}/messages/{message_id}"

    @classmethod
    def edit_webhook_message(cls, webhook_id: int, webhook_token: str, message_id: int) -> str:
        return f"webhooks/{webhook_id}/{webhook_token}/messages/{message_id}"

    @classmethod
    def delete_webhook_message(cls, webhook_id: int, webhook_token: str, message_id: int) -> str:
        return f"webhooks/{webhook_id}/{webhook_token}/messages/{message_id}"

    @classmethod
    def get_guild_webhooks(cls, guild_id: int) -> str:
        return f"guilds/{guild_id}/webhooks"

    @classmethod
    def interaction_command(cls, app_id: int) -> str:
        return f"applications/{app_id}/commands"

    @classmethod
    def interaction_callback(cls, interaction_id: int, interaction_token: str) -> str:
        return f"interactions/{interaction_id}/{interaction_token}/callback"

    @classmethod
    def get_original_interaction(cls, interaction_id: int, interaction_token: str) -> str:
        return f"/webhooks/{interaction_id}/{interaction_token}/messages/@original"

    @classmethod
    def edit_original_interaction(cls, interaction_id: int, interaction_token: str) -> str:
        return f"/webhooks/{interaction_id}/{interaction_token}/messages/@original"

    @classmethod
    def delete_original_interaction(cls, interaction_id: int, interaction_token: str) -> str:
        return f"/webhooks/{interaction_id}/{interaction_token}/messages/@original"

    @classmethod
    def create_followup_message(cls, interaction_id: int, interaction_token: str) -> str:
        return f"/webhooks/{interaction_id}/{interaction_token}"

    @classmethod
    def get_followup_message(cls, interaction_id: int, interaction_token: str, message_id: int) -> str:
        return f"/webhooks/{interaction_id}/{interaction_token}/messages/{message_id}"

    @classmethod
    def edit_followup_message(cls, interaction_id: int, interaction_token: str, message_id: int) -> str:
        return f"/webhooks/{interaction_id}/{interaction_token}/messages/{message_id}"

    @classmethod
    def delete_followup_message(cls, interaction_id: int, interaction_token: str, message_id: int) -> str:
        return f"/webhooks/{interaction_id}/{interaction_token}/messages/{message_id}"
