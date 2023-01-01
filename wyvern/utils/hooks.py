from __future__ import annotations

import importlib
import typing

import attrs


@attrs.define
class Hook:
    name: str
    callback: typing.Callable[..., typing.Any]

    def __call__(self, *args: typing.Any, **kwds: typing.Any) -> None:
        self.callback(*args, **kwds)


def hook(name: str | None = None) -> typing.Callable[[typing.Callable[..., typing.Any]], Hook]:
    def decorator(callback: typing.Callable[..., typing.Any]) -> Hook:
        return Hook(name or callback.__name__, callback)

    return decorator


def parse_hooks(import_path: str) -> dict[str, Hook]:
    module = importlib.import_module(import_path)
    return {_hook.name: _hook for _hook in module.__dict__.values() if isinstance(_hook, Hook)}
