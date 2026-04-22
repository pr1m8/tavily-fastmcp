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
from typing import Any

from tavily_fastmcp.models import ServerCatalog
from tavily_fastmcp.profiles import RESOURCE_PREFIX, list_profiles, load_profile
from tavily_fastmcp.prompt_loader import list_prompt_names, load_prompt_text
from tavily_fastmcp.service import LangChainTavilyService, TavilyServiceProtocol
from tavily_fastmcp.settings import Settings, get_settings
from tavily_fastmcp.tools import (
    register_catalog_tool,
    register_crawl_tool,
    register_extract_tool,
    register_get_research_tool,
    register_health_tool,
    register_map_tool,
    register_research_tool,
    register_search_tool,
)

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
        from fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover - dependency dependent
        raise RuntimeError(
            "FastMCP is required to create the server. Install package dependencies first."
        ) from exc

    app_settings = settings or get_settings()
    backend = service or LangChainTavilyService(app_settings)
    router_prompt = load_prompt_text(ROUTER_PROMPT_NAME)
    catalog = _build_catalog()

    mcp_kwargs: dict[str, Any] = {
        "name": SERVER_NAME,
        "instructions": router_prompt,
        "include_fastmcp_meta": True,
    }
    try:
        mcp = FastMCP(**mcp_kwargs)
    except TypeError as exc:
        if "include_fastmcp_meta" not in str(exc):
            raise
        mcp_kwargs.pop("include_fastmcp_meta")
        mcp = FastMCP(**mcp_kwargs)

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
        r"""Render the main router prompt for a user request.

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
        return f"{profile.prompt_markdown}\n\n## Bound request\n\n{user_request}\n"

    register_health_tool(mcp, server_name=SERVER_NAME, package_version=PACKAGE_VERSION)
    register_catalog_tool(mcp, catalog=catalog, package_version=PACKAGE_VERSION)
    register_search_tool(mcp, backend=backend, settings=app_settings)
    register_extract_tool(mcp, backend=backend)
    register_map_tool(mcp, backend=backend)
    register_crawl_tool(mcp, backend=backend)
    register_research_tool(mcp, backend=backend)
    register_get_research_tool(mcp, backend=backend)

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
