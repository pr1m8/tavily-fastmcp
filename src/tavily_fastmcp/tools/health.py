"""Health tool registration.

Purpose:
    Register the simple server health endpoint for MCP clients.

Design:
    - Keep the tool small and deterministic.
    - Return only package/server metadata so the tool is safe for smoke
      tests and client bootstrapping.
"""

from __future__ import annotations

from typing import Any

from tavily_fastmcp.models import HealthResponse


def register_health_tool(mcp: Any, *, server_name: str, package_version: str) -> None:
    """Register the ``tavily.health`` MCP tool.

    Args:
        mcp: FastMCP server instance.
        server_name: Human-readable server name.
        package_version: Package version string.

    Returns:
        ``None``.

    Examples:
        >>> callable(register_health_tool)
        True
    """

    @mcp.tool(
        name="tavily.health",
        title="Tavily Health",
        description="Return package and server health metadata.",
        tags={"health", "server", "readonly"},
        annotations={
            "title": "Tavily Health",
            "readOnlyHint": True,
            "openWorldHint": False,
            "idempotentHint": True,
        },
        meta={"component": "server", "version": package_version},
    )
    async def tavily_health(ctx: Any | None = None) -> HealthResponse:
        """Return a simple server health payload.

        Args:
            ctx: Optional FastMCP context.

        Returns:
            A health response model.
        """
        if ctx is not None:
            await ctx.info("Health check requested.")
        return HealthResponse(status="ok", server_name=server_name, version=package_version)
