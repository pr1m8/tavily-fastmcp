"""Research tool registration.

Purpose:
    Register the namespaced Tavily research MCP tool.

Design:
    - Keep long-form research creation separate from retrieval.
    - Convert flat MCP arguments into the canonical request model.
"""

from __future__ import annotations

from typing import Annotated, Any

from pydantic import Field

from tavily_fastmcp.models import ResearchRequest, ResearchResponse
from tavily_fastmcp.service import TavilyServiceProtocol


def register_research_tool(mcp: Any, *, backend: TavilyServiceProtocol) -> None:
    """Register the ``tavily.research`` MCP tool.

    Args:
        mcp: FastMCP server instance.
        backend: Tavily service backend.

    Returns:
        ``None``.
    """

    @mcp.tool(
        name="tavily.research",
        title="Tavily Research",
        description="Create a deep multi-source Tavily research task.",
        tags={"research", "report", "readonly"},
        annotations={
            "title": "Tavily Research",
            "readOnlyHint": True,
            "openWorldHint": True,
            "idempotentHint": False,
        },
        meta={"profile_hints": ["deep-research"]},
    )
    async def tavily_research(
        input: Annotated[str, Field(description="Research task or question.")],
        model: Annotated[str, Field(description="Research model.")] = "auto",
        citation_format: Annotated[str, Field(description="Citation format.")] = "numbered",
        stream: Annotated[bool, Field(description="Whether Tavily should stream results.")] = False,
        output_schema: Annotated[dict[str, Any] | None, Field(description="Optional JSON schema for structured output.")] = None,
        ctx: Any | None = None,
    ) -> ResearchResponse:
        """Create a Tavily research task.

        Args:
            input: Research task or question.
            model: Tavily research model.
            citation_format: Citation format.
            stream: Whether Tavily should stream.
            output_schema: Optional JSON schema for structured output.
            ctx: Optional FastMCP context.

        Returns:
            A normalized Tavily research response.
        """
        request = ResearchRequest(
            input=input,
            model=model,
            citation_format=citation_format,
            stream=stream,
            output_schema=output_schema,
        )
        if ctx is not None:
            await ctx.info(f"Starting research task with model={model}.")
        return backend.research_from_model(request)
