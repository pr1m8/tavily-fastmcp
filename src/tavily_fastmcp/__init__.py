"""Top-level package for :mod:`tavily_fastmcp`.

Purpose:
    Provide a typed, ergonomic FastMCP wrapper around Tavily search,
    extract, map, crawl, and research workflows.

Design:
    - Keep canonical request and response models in one place.
    - Expose a direct Python service API and a discoverable MCP server API.
    - Ship large packaged markdown prompts and reusable workflow profiles.

Attributes:
    __all__:
        Curated public API for settings, prompt loading, profile loading,
        server creation, and the direct Tavily service.

Examples:
    >>> from tavily_fastmcp import get_settings, load_profile
    >>> settings = get_settings
    >>> callable(settings)
    True
"""

from tavily_fastmcp.profiles import list_profiles, load_profile, profile_to_markdown
from tavily_fastmcp.prompt_loader import list_prompt_names, load_prompt_text
from tavily_fastmcp.server import create_server
from tavily_fastmcp.service import LangChainTavilyService
from tavily_fastmcp.settings import Settings, get_settings

__all__ = [
    "LangChainTavilyService",
    "Settings",
    "create_server",
    "get_settings",
    "list_profiles",
    "list_prompt_names",
    "load_profile",
    "load_prompt_text",
    "profile_to_markdown",
]
