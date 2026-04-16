"""FastMCP server factory for Tavily FastMCP.

Purpose:
    Build a discoverable FastMCP server exposing typed Tavily-backed tools,
    prompt catalogs, profile catalogs, static resources, and dynamic
    resource templates.

Design:
    - Accept a service dependency so tests can inject a fake backend.
    - Publish tool, prompt, and resource metadata with tags and custom meta.
    - Keep prompt markdown as package data and surface it through MCP.

Examples:
    >>> callable(create_server)
    True
"""

from __future__ import annotations

import argparse
import json
from typing import Annotated, Any

from pydantic import Field

from tavily_fastmcp.models import (
    CrawlRequest,
    CrawlResponse,
    ExtractRequest,
    ExtractResponse,
    GetResearchRequest,
    HealthResponse,
    MapRequest,
    MapResponse,
    ResearchRequest,
    ResearchResponse,
    SearchRequest,
    SearchResponse,
    ServerCatalog,
)
from tavily_fastmcp.prompt_loader import list_prompt_names, load_prompt_text
from tavily_fastmcp.profiles import RESOURCE_PREFIX, list_profiles, load_profile, profile_to_markdown
from tavily_fastmcp.service import LangChainTavilyService, TavilyServiceProtocol
from tavily_fastmcp.settings import Settings, get_settings

PACKAGE_NAME = "tavily-fastmcp"
PACKAGE_VERSION = "0.3.0"
SERVER_NAME = "Tavily FastMCP"
ROUTER_PROMPT_NAME = "router"


def _build_catalog() -> ServerCatalog:
    prompt_names = list_prompt_names()
    profiles = list_profiles()
    base_resources = [
        f"{RESOURCE_PREFIX}/catalog/server",
        f"{RESOURCE_PREFIX}/catalog/profiles",
        f"{RESOURCE_PREFIX}/prompt/{ROUTER_PROMPT_NAME}",
        f"{RESOURCE_PREFIX}/example/claude-desktop-config",
        f"{RESOURCE_PREFIX}/example/cursor-config",
    ]
    profile_resource_uris = [profile.profile_resource_uri for profile in profiles]
    prompt_resource_uris = [f"{RESOURCE_PREFIX}/prompt/{profile.slug}" for profile in profiles]
    return ServerCatalog(
        name=SERVER_NAME,
        version=PACKAGE_VERSION,
        package_name=PACKAGE_NAME,
        prompt_names=prompt_names,
        profile_slugs=[profile.slug for profile in profiles],
        tool_names=[
            "tavily.health",
            "tavily.catalog",
            "tavily.search",
            "tavily.extract",
            "tavily.map",
            "tavily.crawl",
            "tavily.research",
            "tavily.get_research",
        ],
        resource_uris=base_resources + profile_resource_uris + prompt_resource_uris,
        example_resource_uris=[
            f"{RESOURCE_PREFIX}/example/claude-desktop-config",
            f"{RESOURCE_PREFIX}/example/cursor-config",
        ],
        meta={
            "package": PACKAGE_NAME,
            "version": PACKAGE_VERSION,
            "namespacing": "tavily.* and resource://tavily-fastmcp/*",
            "includes_profiles": True,
        },
    )


def create_server(
    *,
    settings: Settings | None = None,
    service: TavilyServiceProtocol | None = None,
) -> Any:
    """Create a configured FastMCP server instance.

    Args:
        settings: Optional validated settings object.
        service: Optional Tavily service implementation for dependency
            injection in tests.

    Returns:
        A configured FastMCP server instance.

    Raises:
        RuntimeError: If FastMCP is not installed.

    Examples:
        >>> callable(create_server)
        True
    """
    try:
        from fastmcp import Context, FastMCP
    except ImportError as exc:  # pragma: no cover - dependency dependent
        raise RuntimeError(
            "FastMCP is required to create the server. Install package dependencies first."
        ) from exc

    app_settings = settings or get_settings()
    backend = service or LangChainTavilyService(app_settings)
    router_prompt = load_prompt_text(ROUTER_PROMPT_NAME)
    catalog = _build_catalog()

    mcp = FastMCP(
        name=SERVER_NAME,
        instructions=router_prompt,
        include_fastmcp_meta=True,
    )

    @mcp.resource(
        uri=f"{RESOURCE_PREFIX}/catalog/server",
        name="ServerCatalog",
        title="Server Catalog",
        description="Structured catalog of tools, prompts, profiles, and example resources.",
        mime_type="application/json",
        tags={"catalog", "server", "metadata"},
        meta={"component": "catalog", "version": PACKAGE_VERSION},
    )
    def server_catalog_resource() -> ServerCatalog:
        """Return the structured server catalog.

        Returns:
            A server catalog model.

        Raises:
            ValueError: If the catalog cannot be serialized.

        Examples:
            >>> _build_catalog().package_name
            'tavily-fastmcp'
        """
        return catalog

    @mcp.resource(
        uri=f"{RESOURCE_PREFIX}/catalog/profiles",
        name="ProfileCatalog",
        title="Profile Catalog",
        description="List of packaged workflow profiles exposed by the server.",
        mime_type="application/json",
        tags={"catalog", "profiles", "metadata"},
        meta={"component": "profile-catalog"},
    )
    def profile_catalog_resource() -> list[dict[str, Any]]:
        """Return summary metadata for all profiles."""
        return [profile.model_dump() for profile in list_profiles()]

    @mcp.resource(
        uri=f"{RESOURCE_PREFIX}/profile/{{slug}}",
        name="PromptProfile",
        title="Prompt Profile",
        description="Structured profile metadata plus packaged markdown prompt content.",
        mime_type="application/json",
        tags={"profile", "prompt", "template"},
        meta={"component": "profile-template"},
    )
    def profile_resource(slug: str) -> dict[str, Any]:
        """Return a specific packaged profile by slug.

        Args:
            slug: Stable profile slug.

        Returns:
            The serialized prompt profile.

        Raises:
            KeyError: If the slug is unknown.

        Examples:
            >>> load_profile('router').slug
            'router'
        """
        return load_profile(slug).model_dump()

    @mcp.resource(
        uri=f"{RESOURCE_PREFIX}/prompt/{{name}}",
        name="PromptMarkdown",
        title="Prompt Markdown",
        description="Packaged markdown prompt text addressed by prompt or profile name.",
        mime_type="text/markdown",
        tags={"prompt", "markdown", "template"},
        meta={"component": "prompt-template"},
    )
    def prompt_markdown_resource(name: str) -> str:
        """Return packaged prompt markdown by name or profile slug.

        Args:
            name: Prompt file stem or profile slug.

        Returns:
            Markdown prompt content.

        Raises:
            FileNotFoundError: If the prompt does not exist.
            KeyError: If a supplied profile slug is unknown.

        Examples:
            >>> load_prompt_text('router').startswith('#')
            True
        """
        prompt_names = set(list_prompt_names())
        if name in prompt_names:
            return load_prompt_text(name)
        return load_profile(name).prompt_markdown

    @mcp.resource(
        uri=f"{RESOURCE_PREFIX}/example/claude-desktop-config",
        name="ClaudeDesktopConfig",
        title="Claude Desktop Config",
        description="Example stdio configuration snippet for Claude Desktop.",
        mime_type="application/json",
        tags={"example", "config", "claude"},
        meta={"component": "example"},
    )
    def claude_desktop_config_resource() -> dict[str, Any]:
        """Return an example Claude Desktop MCP configuration."""
        return {
            "mcpServers": {
                "tavily-fastmcp": {
                    "command": "python",
                    "args": ["-m", "tavily_fastmcp.server", "--transport", "stdio"],
                    "env": {"TAVILY_API_KEY": "tvly-your-key-here"},
                }
            }
        }

    @mcp.resource(
        uri=f"{RESOURCE_PREFIX}/example/cursor-config",
        name="CursorConfig",
        title="Cursor Config",
        description="Example stdio configuration snippet for Cursor or similar MCP clients.",
        mime_type="application/json",
        tags={"example", "config", "cursor"},
        meta={"component": "example"},
    )
    def cursor_config_resource() -> dict[str, Any]:
        """Return an example generic stdio MCP client configuration."""
        return {
            "name": "tavily-fastmcp",
            "command": "python",
            "args": ["-m", "tavily_fastmcp.server", "--transport", "stdio"],
            "env": {"TAVILY_API_KEY": "tvly-your-key-here"},
        }

    @mcp.prompt(
        name="tavily-router",
        title="Tavily Router Prompt",
        description="General routing prompt that chooses the smallest correct Tavily workflow.",
        tags={"router", "default", "planning"},
        meta={"prompt_file": "router.md"},
    )
    def tavily_router_prompt(user_request: str) -> str:
        """Render the main router prompt for a user request.

        Args:
            user_request: User request appended after the router instructions.

        Returns:
            A rendered prompt string.

        Raises:
            ValueError: If prompt rendering fails.

        Examples:
            >>> "User request" in (load_prompt_text("router") + "\n\n## User request")
            True
        """
        return f"{router_prompt}\n\n## User request\n\n{user_request}\n"

    @mcp.prompt(
        name="tavily-profile",
        title="Tavily Profile Prompt",
        description="Render a packaged profile and bind it to a concrete user request.",
        tags={"profile", "prompt", "workflow"},
        meta={"dynamic": True},
    )
    def tavily_profile_prompt(profile_slug: str, user_request: str) -> str:
        """Render a specific profile prompt.

        Args:
            profile_slug: Profile slug to render.
            user_request: User request appended after the profile.

        Returns:
            A rendered profile prompt.

        Raises:
            KeyError: If the profile slug is unknown.

        Examples:
            >>> load_profile('quick-search').slug
            'quick-search'
        """
        profile = load_profile(profile_slug)
        return (
            f"{profile.prompt_markdown}\n\n"
            "## Bound request\n\n"
            f"{user_request}\n"
        )

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
        meta={"component": "server", "version": PACKAGE_VERSION},
    )
    async def tavily_health(ctx: Context | None = None) -> HealthResponse:
        """Return a simple health payload.

        Args:
            ctx: Optional FastMCP context.

        Returns:
            A health response.

        Raises:
            RuntimeError: Never raised intentionally.

        Examples:
            .. code-block:: python

                await client.call_tool("tavily.health")
        """
        if ctx is not None:
            await ctx.info("Health check requested.")
        return HealthResponse(status="ok", server_name=SERVER_NAME, version=PACKAGE_VERSION)

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
        meta={"component": "catalog", "version": PACKAGE_VERSION},
    )
    async def tavily_catalog(ctx: Context | None = None) -> ServerCatalog:
        """Return the structured server catalog."""
        if ctx is not None:
            await ctx.info("Server catalog requested.")
        return catalog

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
        topic: Annotated[str, Field(description="Search topic mode.")] = app_settings.default_search_topic,
        include_answer: Annotated[bool, Field(description="Include Tavily's answer field.")] = False,
        include_raw_content: Annotated[bool, Field(description="Include cleaned page content.")] = False,
        include_images: Annotated[bool, Field(description="Include image URLs.")] = False,
        include_image_descriptions: Annotated[bool, Field(description="Include image descriptions.")] = False,
        search_depth: Annotated[str, Field(description="Tavily search depth.")] = app_settings.default_search_depth,
        time_range: Annotated[str | None, Field(description="Relative publish-date filter.")] = None,
        start_date: Annotated[str | None, Field(description="Inclusive start date in YYYY-MM-DD format.")] = None,
        end_date: Annotated[str | None, Field(description="Inclusive end date in YYYY-MM-DD format.")] = None,
        include_domains: Annotated[list[str] | None, Field(description="Domains to include.")] = None,
        exclude_domains: Annotated[list[str] | None, Field(description="Domains to exclude.")] = None,
        include_usage: Annotated[bool, Field(description="Include usage metadata.")] = False,
        ctx: Context | None = None,
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

        Raises:
            RuntimeError: If the Tavily backend cannot execute the request.

        Examples:
            .. code-block:: python

                await client.call_tool(
                    "tavily.search",
                    {"query": "latest FastMCP docs", "max_results": 3},
                )
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
        ctx: Context | None = None,
    ) -> ExtractResponse:
        """Extract content from known URLs."""
        request = ExtractRequest(urls=urls, extract_depth=extract_depth, include_images=include_images)
        if ctx is not None:
            await ctx.info(f"Extracting content from {len(urls)} URL(s).")
        return backend.extract_from_model(request)

    @mcp.tool(
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
        url: Annotated[str, Field(description="Root URL to begin mapping.")],
        instructions: Annotated[str | None, Field(description="Optional mapping guidance.")] = None,
        ctx: Context | None = None,
    ) -> MapResponse:
        """Map a site to discover likely relevant URLs."""
        request = MapRequest(url=url, instructions=instructions)
        if ctx is not None:
            await ctx.info(f"Mapping site: {url}")
        return backend.map_from_model(request)

    @mcp.tool(
        name="tavily.crawl",
        title="Tavily Crawl",
        description="Crawl one site and retrieve content from multiple pages.",
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
        instructions: Annotated[str | None, Field(description="Optional crawling guidance.")] = None,
        ctx: Context | None = None,
    ) -> CrawlResponse:
        """Crawl a site and retrieve multi-page content."""
        request = CrawlRequest(url=url, instructions=instructions)
        if ctx is not None:
            await ctx.info(f"Crawling site: {url}")
        return backend.crawl_from_model(request)

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
        ctx: Context | None = None,
    ) -> ResearchResponse:
        """Create a Tavily research task."""
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

    @mcp.tool(
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
        ctx: Context | None = None,
    ) -> ResearchResponse:
        """Retrieve a Tavily research task by request ID."""
        request = GetResearchRequest(request_id=request_id)
        if ctx is not None:
            await ctx.info(f"Fetching research task: {request_id}")
        return backend.get_research_from_model(request)

    return mcp


def build_arg_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser.

    Returns:
        A configured ``ArgumentParser`` instance.

    Raises:
        RuntimeError: Never raised intentionally.

    Examples:
        >>> parser = build_arg_parser()
        >>> parser.prog
        'tavily-fastmcp'
    """
    parser = argparse.ArgumentParser(prog="tavily-fastmcp")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http", "sse"],
        default=None,
        help="Override the configured transport.",
    )
    return parser


def main() -> None:
    """Run the MCP server from the command line.

    Returns:
        ``None``.

    Raises:
        RuntimeError: If FastMCP is unavailable.

    Examples:
        >>> callable(main)
        True
    """
    args = build_arg_parser().parse_args()
    settings = get_settings()
    if args.transport is not None:
        settings = settings.model_copy(update={"transport": args.transport})
    server = create_server(settings=settings)
    server.run(transport=settings.transport)


if __name__ == "__main__":  # pragma: no cover
    main()
