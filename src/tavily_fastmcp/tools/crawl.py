"""Crawl tool registration.

Purpose:
    Register the namespaced Tavily crawl MCP tool.

Design:
    - Reserve crawling for multi-page site reading.
    - Convert flat MCP arguments into the canonical request model.
"""

from __future__ import annotations

from typing import Annotated, Any, cast

from pydantic import Field

from tavily_fastmcp._typing import ToolRegistrar
from tavily_fastmcp.models import CrawlRequest, CrawlResponse
from tavily_fastmcp.service import TavilyServiceProtocol


def register_crawl_tool(mcp: Any, *, backend: TavilyServiceProtocol) -> None:
    """Register the ``tavily.crawl`` MCP tool.

    Args:
        mcp: FastMCP server instance.
        backend: Tavily service backend.

    Returns:
        ``None``.
    """
    tool_server = cast(ToolRegistrar, mcp)

    @tool_server.tool(
        name="tavily.crawl",
        title="Tavily Crawl",
        description="Traverse a site and retrieve multi-page content.",
        tags={"crawl", "site", "readonly"},
        annotations={
            "title": "Tavily Crawl",
            "readOnlyHint": True,
            "openWorldHint": True,
            "idempotentHint": True,
        },
        meta={"profile_hints": ["site-crawl"]},
    )
    async def tavily_crawl(
        url: Annotated[str, Field(description="Root URL to begin crawling.")],
        instructions: Annotated[
            str | None, Field(description="Optional crawling guidance.")
        ] = None,
        ctx: Any | None = None,
    ) -> CrawlResponse:
        """Crawl a site and retrieve multi-page content.

        Args:
            url: Root URL to begin crawling.
            instructions: Optional crawling guidance.
            ctx: Optional FastMCP context.

        Returns:
            A normalized Tavily crawl response.
        """
        request = CrawlRequest.model_validate({"url": url, "instructions": instructions})
        if ctx is not None:
            await ctx.info(f"Crawling site: {url}")
        return backend.crawl_from_model(request)
