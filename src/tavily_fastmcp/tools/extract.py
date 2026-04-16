"""Extract tool registration.

Purpose:
    Register the namespaced Tavily extract MCP tool.

Design:
    - Convert flat MCP arguments into :class:`ExtractRequest`.
    - Keep tool behavior stable and URL-first.
"""

from __future__ import annotations

from typing import Annotated, Any

from pydantic import Field

from tavily_fastmcp.models import ExtractRequest, ExtractResponse
from tavily_fastmcp.service import TavilyServiceProtocol


def register_extract_tool(mcp: Any, *, backend: TavilyServiceProtocol) -> None:
    """Register the ``tavily.extract`` MCP tool.

    Args:
        mcp: FastMCP server instance.
        backend: Tavily service backend.

    Returns:
        ``None``.
    """

    @mcp.tool(
        name="tavily.extract",
        title="Tavily Extract",
        description="Extract content from specific known URLs.",
        tags={"extract", "url-first", "readonly"},
        annotations={
            "title": "Tavily Extract",
            "readOnlyHint": True,
            "openWorldHint": True,
            "idempotentHint": True,
        },
        meta={"profile_hints": ["extract-and-summarize", "quick-search"]},
    )
    async def tavily_extract(
        urls: Annotated[list[str], Field(description="URLs to extract.", min_length=1)],
        extract_depth: Annotated[str, Field(description="Extraction depth.")] = "basic",
        include_images: Annotated[bool, Field(description="Include image metadata.")] = False,
        ctx: Any | None = None,
    ) -> ExtractResponse:
        """Extract content from known URLs.

        Args:
            urls: URLs to extract.
            extract_depth: Extraction depth.
            include_images: Whether image metadata should be returned.
            ctx: Optional FastMCP context.

        Returns:
            A normalized Tavily extract response.
        """
        request = ExtractRequest(urls=urls, extract_depth=extract_depth, include_images=include_images)
        if ctx is not None:
            await ctx.info(f"Extracting content from {len(urls)} URL(s).")
        return backend.extract_from_model(request)
