"""Unit tests for profile registry."""

from __future__ import annotations

from tavily_fastmcp.profiles import list_profiles, load_profile, profile_to_markdown

EXPECTED_PROFILE_SLUGS = {
    "router",
    "suite-overview",
    "quick-search",
    "tool-search",
    "extract-and-summarize",
    "tool-extract",
    "site-discovery",
    "tool-map",
    "site-crawl",
    "tool-crawl",
    "deep-research",
    "tool-research",
    "tool-get-research",
    "routing-matrix",
    "synthesis-policy",
    "mcp-usage-guide",
}


def test_profile_catalog_contains_expected_profiles() -> None:
    """The profile catalog should expose both operational and reference profiles."""
    slugs = {profile.slug for profile in list_profiles()}
    assert EXPECTED_PROFILE_SLUGS <= slugs


def test_profile_markdown_render_contains_prompt() -> None:
    """Rendered profile markdown should include prompt content."""
    profile = load_profile("quick-search")
    markdown = profile_to_markdown(profile)
    assert profile.title in markdown
    assert "## Prompt" in markdown


def test_suite_overview_profile_is_massive() -> None:
    """The suite overview profile should expose a large composite prompt body."""
    profile = load_profile("suite-overview")
    assert len(profile.prompt_markdown) > 3000
    assert "composite semantic overview" in profile.prompt_markdown.lower()


def test_profile_resource_uris_are_namespaced() -> None:
    """Every profile summary should point at namespaced MCP resource URIs."""
    for profile in list_profiles():
        assert profile.prompt_resource_uri.startswith("resource://tavily-fastmcp/")
        assert profile.profile_resource_uri.startswith("resource://tavily-fastmcp/")
