"""Local typing helpers for third-party MCP objects."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Protocol, TypeVar

_F = TypeVar("_F", bound=Callable[..., Any])


class ToolRegistrar(Protocol):
    """Minimal typed surface for FastMCP-compatible tool registration."""

    def tool(self, **metadata: Any) -> Callable[[_F], _F]:
        """Return a decorator that registers a tool handler."""
        ...
