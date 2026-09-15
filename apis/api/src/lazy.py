"""Lazy init helpers so API modules can import without Storage/SPAIVars at boot."""

from __future__ import annotations

from typing import Any, Callable


class LazyObject:
    """Proxy that creates the real object on first attribute/item access."""

    __slots__ = ("_factory", "_value", "_ready")

    def __init__(self, factory: Callable[[], Any]) -> None:
        object.__setattr__(self, "_factory", factory)
        object.__setattr__(self, "_value", None)
        object.__setattr__(self, "_ready", False)

    def _resolve(self) -> Any:
        if not object.__getattribute__(self, "_ready"):
            value = object.__getattribute__(self, "_factory")()
            object.__setattr__(self, "_value", value)
            object.__setattr__(self, "_ready", True)
        return object.__getattribute__(self, "_value")

    def __getattr__(self, name: str) -> Any:
        return getattr(self._resolve(), name)

    def __getitem__(self, key: Any) -> Any:
        return self._resolve()[key]

    def __bool__(self) -> bool:
        return bool(self._resolve())

    def __repr__(self) -> str:
        if object.__getattribute__(self, "_ready"):
            return repr(self._resolve())
        return f"<LazyObject pending factory={object.__getattribute__(self, '_factory')!r}>"
