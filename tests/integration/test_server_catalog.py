"""Integration tests for server catalog and packaging."""

from __future__ import annotations

from tavily_fastmcp.server import _build_catalog



def test_catalog_contains_namespaced_tools() -> None:
    """The catalog should expose namespaced tools."""
    catalog = _build_catalog()
    assert "tavily.search" in catalog.tool_names
    assert "tavily.research" in catalog.tool_names


def test_catalog_exposes_prompt_and_profile_resources() -> None:
    """The catalog should advertise prompt and profile resources for discovery."""
    catalog = _build_catalog()
    assert any(uri.endswith("/prompt/router") for uri in catalog.resource_uris)
    assert any("/profile/" in uri for uri in catalog.resource_uris)
    assert any("/prompt/suite-overview" in uri for uri in catalog.resource_uris)
