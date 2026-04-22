"""Research retrieval tool registration.

Purpose:
    Register the namespaced Tavily get-research MCP tool.

Design:
    - Keep research retrieval explicit and separate from task creation.
    - Convert flat MCP arguments into the canonical request model.
"""

from __future__ import annotations

from typing import Annotated, Any, cast

from pydantic import Field

from tavily_fastmcp._typing import ToolRegistrar
from tavily_fastmcp.models import GetResearchRequest, ResearchResponse
from tavily_fastmcp.service import TavilyServiceProtocol


def register_get_research_tool(mcp: Any, *, backend: TavilyServiceProtocol) -> None:
    """Register the ``tavily.get_research`` MCP tool.

    Args:
        mcp: FastMCP server instance.
        backend: Tavily service backend.

    Returns:
        ``None``.
    """
    tool_server = cast(ToolRegistrar, mcp)

    @tool_server.tool(
        name="tavily.get_research",
        title="Tavily Get Research",
        description="Retrieve the status or result of an existing Tavily research task.",
        tags={"research", "status", "readonly"},
        annotations={
            "title": "Tavily Get Research",
            "readOnlyHint": True,
            "openWorldHint": True,
            "idempotentHint": True,
        },
        meta={"profile_hints": ["deep-research"]},
    )
    async def tavily_get_research(
        request_id: Annotated[str, Field(description="Tavily research request identifier.")],
        ctx: Any | None = None,
    ) -> ResearchResponse:
        """Retrieve a Tavily research task by request identifier.

        Args:
            request_id: Tavily research request identifier.
            ctx: Optional FastMCP context.

        Returns:
            A normalized Tavily research response.
        """
        request = GetResearchRequest(request_id=request_id)
        if ctx is not None:
            await ctx.info(f"Fetching research task: {request_id}")
        return backend.get_research_from_model(request)
