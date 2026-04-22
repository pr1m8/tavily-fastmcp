"""Tests for the physical tools package layout."""

from __future__ import annotations

from importlib import import_module

EXPECTED_MODULES = [
    "catalog",
    "crawl",
    "extract",
    "get_research",
    "health",
    "map",
    "research",
    "search",
]


def test_tools_package_contains_expected_registration_modules() -> None:
    """The package should expose concrete tool registration modules."""
    package = import_module("tavily_fastmcp.tools")
    for module_name in EXPECTED_MODULES:
        module = import_module(f"tavily_fastmcp.tools.{module_name}")
        assert module is not None
    assert hasattr(package, "register_search_tool")
    assert hasattr(package, "register_research_tool")
