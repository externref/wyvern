from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from wyvern.clients import GatewayClient
    from wyvern.models.members import Member

__all__: tuple[str, ...] = ("MembersState",)


class MembersState:
    _client: "GatewayClient"
    cached_members: dict[int, dict[int, Member]] = {}

    def __init__(self, client: GatewayClient) -> None:
        self._client = client

    def _guild_check(self, gid: int) -> None:
        if gid not in self.cached_members.keys():
            self.cached_members[gid] = {}

    def get(self, guild_id: int, member_id: int) -> "Member" | None:
        self._guild_check(guild_id)
        return self.cached_members[guild_id].get(member_id)

    async def fetch(self, guild_id: int, member_id: int) -> "Member":
        return await self._client.rest.fetch_member(guild_id, member_id)

    def get_member_named(self, guild_id: int, name: str) -> "Member" | None:
        self._guild_check(guild_id)
        return (
            members[0]
            if (members := [member for member in self.cached_members[guild_id].values() if member.username == name])
            else None
        )

    def add_member(self, mem: Member) -> None:
        self._guild_check(mem.guild_id)
        self.cached_members[mem.guild_id][mem.id] = mem

    def update_user_state(self) -> None:
        [
            self._client.users._add_to_state(*list(map(lambda mem: mem.user, members.values())))
            for members in self.cached_members.values()
        ]
