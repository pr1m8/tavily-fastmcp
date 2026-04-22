"""Unit tests for prompt loading.

Purpose:
    Validate that the packaged prompt catalog is large, discoverable, and
    structurally rich enough to support both terse and deep prompt profiles.
"""

from __future__ import annotations

from tavily_fastmcp.prompt_loader import list_prompt_names, load_prompt_text

_EXPECTED_PROMPTS = {
    "router",
    "quick_search",
    "extract_and_summarize",
    "site_discovery",
    "site_crawl",
    "deep_research",
    "suite_overview",
    "tool_search_master",
    "tool_extract_master",
    "tool_map_master",
    "tool_crawl_master",
    "tool_research_master",
    "tool_get_research_master",
    "routing_matrix",
    "synthesis_policy",
    "mcp_usage_guide",
}


def test_prompt_catalog_contains_expected_guides() -> None:
    """The prompt catalog should expose the expected deep-guide prompt set."""
    names = set(list_prompt_names())
    assert _EXPECTED_PROMPTS <= names


def test_router_prompt_exists() -> None:
    """The router prompt should be packaged and recognizable."""
    assert load_prompt_text("router").startswith("# Tavily Router")


def test_deep_prompts_are_substantive() -> None:
    """Massive semantic guides should be materially larger than smoke prompts."""
    for name in {
        "suite_overview",
        "tool_search_master",
        "tool_extract_master",
        "tool_map_master",
        "tool_crawl_master",
        "tool_research_master",
        "tool_get_research_master",
    }:
        text = load_prompt_text(name)
        assert len(text) > 2500
        assert "## Core purpose" in text or "## What this server is for" in text


def test_all_prompts_have_markdown_headings() -> None:
    """Every packaged prompt should look like a real markdown reference document."""
    for name in list_prompt_names():
        text = load_prompt_text(name)
        assert text.startswith("# ")
        assert "## " in text
