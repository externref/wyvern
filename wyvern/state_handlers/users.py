from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from wyvern.clients import GatewayClient
    from wyvern.models.users import User

__all__: tuple[str, ...] = ("UserState",)


class UserState:
    """A handler for user cache and rest connection with the client.
    This interface can be used to get/fetch users with convinience.
    """

    _client: "GatewayClient"
    cached_users: dict[int, "User"] = {}
    """Mapping of cached users with their ID : Object"""

    def __init__(self, client: "GatewayClient") -> None:
        self._client = client


    def get(self, user_id: int) -> "User" | None:
        """Fetchs a user using the state cache..

        Parameters
        ----------

        user_id : int
            ID of the user that is to be to get.

        Returns
        -------

        wyvern.models.users.User | None
            The user object that was fetched.

        """
        return self.cached_users.get(user_id)

    async def fetch(self, user_id: int) -> "User":
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

        wyvern.exceptions.UserNotFound
            The targetted user was not found.
        """
        return await self._client.rest.fetch_user(user_id)

    def get_user_named(self, name: str) -> "User" | None:
        """Gets a member named the provided argument from cache

        Parameters
        ----------

        name : str
            Name to lookup for.

        Returns
        -------

        wyvern.models.users.User | None
            The user object that was fetched.

        """
        users = [user for user in self.cached_users.values() if user.username == name]
        return users[0] if users != [] else None

    def parse_from_string(self, string: str) -> "User" | None:
        """
        Parses a user object from a string

        The order for parsing:

        * Lookup for mentions.
        * Lookup for username#discriminator.
        * Lookup for username only.

        Parameters
        ----------

        string : str
            The string to parse from.

        Returns 
        -------

        wyvern.models.users.User | None
            The user object that was parsed, if any.

        """
        if string.startswith("<@") and string.endswith(">"):
            return self.get(int(string.strip("<@!>")))
        elif "#" in string:
            username, discriminator = string.split("#")
            users = [
                user
                for user in self.cached_users.values()
                if user.username == username and user.discriminator == int(discriminator)
            ]
            if users != []:
                return users[0]
            else:
                pass
        elif user := self.get_user_named(string):
            return user
        return None

    def _add_to_state(self, *users: "User") -> None:
        for user in users:
            self.cached_users[user.id] = user
