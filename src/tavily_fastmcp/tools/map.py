"""Map tool registration.

Purpose:
    Register the namespaced Tavily map MCP tool.

Design:
    - Keep mapping focused on structural URL discovery.
    - Convert flat MCP arguments into the canonical request model.
"""

from __future__ import annotations

from typing import Annotated, Any, cast

from pydantic import Field

from tavily_fastmcp._typing import ToolRegistrar
from tavily_fastmcp.models import MapRequest, MapResponse
from tavily_fastmcp.service import TavilyServiceProtocol


def register_map_tool(mcp: Any, *, backend: TavilyServiceProtocol) -> None:
    """Register the ``tavily.map`` MCP tool.

    Args:
        mcp: FastMCP server instance.
        backend: Tavily service backend.

    Returns:
        ``None``.
    """
    tool_server = cast(ToolRegistrar, mcp)

    @tool_server.tool(
        name="tavily.map",
        title="Tavily Map",
        description="Discover site structure and candidate URLs on a single domain.",
        tags={"map", "site", "readonly"},
        annotations={
            "title": "Tavily Map",
            "readOnlyHint": True,
            "openWorldHint": True,
            "idempotentHint": True,
        },
        meta={"profile_hints": ["site-discovery"]},
    )
    async def tavily_map(
        url: Annotated[str, Field(description="Root URL to map.")],
        instructions: Annotated[str | None, Field(description="Optional mapping guidance.")] = None,
        ctx: Any | None = None,
    ) -> MapResponse:
        """Discover candidate URLs on a site.

        Args:
            url: Root URL to map.
            instructions: Optional mapping guidance.
            ctx: Optional FastMCP context.

        Returns:
            A normalized Tavily map response.
        """
        request = MapRequest.model_validate({"url": url, "instructions": instructions})
        if ctx is not None:
            await ctx.info(f"Mapping site: {url}")
        return backend.map_from_model(request)
