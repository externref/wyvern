from __future__ import annotations

import typing

__all__: tuple[str] = ("Flag",)


class Flag:
    value: int

    def __init__(self, value: int) -> None:
        self.value = value

    _ignored_flags = ("ALL", "PRIVILEGED", "UNPRIVILEGED")

    def __iter__(self) -> typing.Generator[tuple[str, bool], None, None]:
        for flag in [attr for attr in dir(self) if attr.isupper() and attr not in self._ignored_flags]:
            if self.value & getattr(self, flag) != 0:
                yield flag, True
            else:
                yield flag, False

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(value={self.value})>"

    def __int__(self) -> int:
        return self.value

    def get_enabled(self, *, as_str: bool = False) -> tuple[int | str, ...]:
        return tuple((getattr(self, flag[0]) if as_str is False else flag[0]) for flag in list(self) if flag[1] is True)

    def get_disabled(self, *, as_str: bool = False) -> tuple[int | str, ...]:
        return tuple(
            (getattr(self, flag[0]) if as_str is False else flag[0]) for flag in list(self) if flag[1] is False
        )
