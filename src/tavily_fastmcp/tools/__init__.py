"""Tool registration helpers for :mod:`tavily_fastmcp`.

Purpose:
    Provide one module per MCP tool registration so the server surface is
    physically organized the same way it is described in the package docs.

Design:
    - Each module exposes one ``register_*_tool`` function.
    - Registration is side-effect free until the helper is called by the
      server factory.
    - The server keeps prompts and resources local while delegating tool
      wiring to this package.

Examples:
    >>> from tavily_fastmcp.tools import register_search_tool
    >>> callable(register_search_tool)
    True
"""

from tavily_fastmcp.tools.catalog import register_catalog_tool
from tavily_fastmcp.tools.crawl import register_crawl_tool
from tavily_fastmcp.tools.extract import register_extract_tool
from tavily_fastmcp.tools.get_research import register_get_research_tool
from tavily_fastmcp.tools.health import register_health_tool
from tavily_fastmcp.tools.map import register_map_tool
from tavily_fastmcp.tools.research import register_research_tool
from tavily_fastmcp.tools.search import register_search_tool

__all__ = [
    "register_catalog_tool",
    "register_crawl_tool",
    "register_extract_tool",
    "register_get_research_tool",
    "register_health_tool",
    "register_map_tool",
    "register_research_tool",
    "register_search_tool",
]
