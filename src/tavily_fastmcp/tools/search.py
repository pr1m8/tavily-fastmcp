"""Search tool registration.

Purpose:
    Register the namespaced Tavily search MCP tool.

Design:
    - Convert flat MCP arguments into the canonical :class:`SearchRequest`.
    - Keep request validation inside the shared model layer.
"""

from __future__ import annotations

from typing import Annotated, Any

from pydantic import Field

from tavily_fastmcp.models import SearchRequest, SearchResponse
from tavily_fastmcp.service import TavilyServiceProtocol
from tavily_fastmcp.settings import Settings


def register_search_tool(
    mcp: Any,
    *,
    backend: TavilyServiceProtocol,
    settings: Settings,
) -> None:
    """Register the ``tavily.search`` MCP tool.

    Args:
        mcp: FastMCP server instance.
        backend: Tavily service backend.
        settings: Package settings.

    Returns:
        ``None``.
    """

    @mcp.tool(
        name="tavily.search",
        title="Tavily Search",
        description="Search the web when relevant URLs are not yet known.",
        tags={"search", "web", "readonly"},
        annotations={
            "title": "Tavily Search",
            "readOnlyHint": True,
            "openWorldHint": True,
            "idempotentHint": True,
        },
        meta={"profile_hints": ["router", "quick-search"]},
    )
    async def tavily_search(
        query: Annotated[str, Field(description="Natural-language web search query.")],
        max_results: Annotated[int, Field(ge=1, le=20, description="Maximum number of results.")] = 5,
        topic: Annotated[str, Field(description="Search topic mode.")] = settings.default_search_topic,
        include_answer: Annotated[bool, Field(description="Include Tavily's answer field.")] = False,
        include_raw_content: Annotated[bool, Field(description="Include cleaned page content.")] = False,
        include_images: Annotated[bool, Field(description="Include image URLs.")] = False,
        include_image_descriptions: Annotated[bool, Field(description="Include image descriptions.")] = False,
        search_depth: Annotated[str, Field(description="Tavily search depth.")] = settings.default_search_depth,
        time_range: Annotated[str | None, Field(description="Relative publish-date filter.")] = None,
        start_date: Annotated[str | None, Field(description="Inclusive start date in YYYY-MM-DD format.")] = None,
        end_date: Annotated[str | None, Field(description="Inclusive end date in YYYY-MM-DD format.")] = None,
        include_domains: Annotated[list[str] | None, Field(description="Domains to include.")] = None,
        exclude_domains: Annotated[list[str] | None, Field(description="Domains to exclude.")] = None,
        include_usage: Annotated[bool, Field(description="Include usage metadata.")] = False,
        ctx: Any | None = None,
    ) -> SearchResponse:
        """Search the public web using Tavily.

        Args:
            query: Natural-language search query.
            max_results: Maximum number of results.
            topic: Tavily topic mode.
            include_answer: Whether to include Tavily's answer summary.
            include_raw_content: Whether to include raw page content.
            include_images: Whether to include image URLs.
            include_image_descriptions: Whether to include image descriptions.
            search_depth: Tavily search depth.
            time_range: Relative time filter.
            start_date: Inclusive start date.
            end_date: Inclusive end date.
            include_domains: Domains to include.
            exclude_domains: Domains to exclude.
            include_usage: Whether to include usage metadata.
            ctx: Optional FastMCP context.

        Returns:
            A normalized Tavily search response.
        """
        request = SearchRequest(
            query=query,
            max_results=max_results,
            topic=topic,
            include_answer=include_answer,
            include_raw_content=include_raw_content,
            include_images=include_images,
            include_image_descriptions=include_image_descriptions,
            search_depth=search_depth,
            time_range=time_range,
            start_date=start_date,
            end_date=end_date,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            include_usage=include_usage,
        )
        if ctx is not None:
            await ctx.info(f"Executing Tavily search for query: {query}")
        return backend.search_from_model(request)
