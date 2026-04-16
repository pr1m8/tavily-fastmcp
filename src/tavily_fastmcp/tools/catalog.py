"""Catalog tool registration.

Purpose:
    Register the structured catalog tool that exposes server metadata.

Design:
    - Return the same structured catalog model used by resource endpoints.
    - Keep client discovery deterministic and idempotent.
"""

from __future__ import annotations

from typing import Any

from tavily_fastmcp.models import ServerCatalog


def register_catalog_tool(mcp: Any, *, catalog: ServerCatalog, package_version: str) -> None:
    """Register the ``tavily.catalog`` MCP tool.

    Args:
        mcp: FastMCP server instance.
        catalog: Structured server catalog.
        package_version: Package version string.

    Returns:
        ``None``.
    """

    @mcp.tool(
        name="tavily.catalog",
        title="Tavily Catalog",
        description="Return the structured server catalog that describes tools, resources, and prompts.",
        tags={"catalog", "server", "readonly"},
        annotations={
            "title": "Tavily Catalog",
            "readOnlyHint": True,
            "openWorldHint": False,
            "idempotentHint": True,
        },
        meta={"component": "catalog", "version": package_version},
    )
    async def tavily_catalog(ctx: Any | None = None) -> ServerCatalog:
        """Return the structured server catalog.

        Args:
            ctx: Optional FastMCP context.

        Returns:
            The server catalog.
        """
        if ctx is not None:
            await ctx.info("Server catalog requested.")
        return catalog
