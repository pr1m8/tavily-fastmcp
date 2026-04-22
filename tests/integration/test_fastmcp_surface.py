"""Integration tests for the FastMCP surface.

These tests are skipped automatically when FastMCP is unavailable.
"""

from __future__ import annotations

import pytest

from tavily_fastmcp.models import (
    CrawlResponse,
    ExtractResponse,
    MapResponse,
    ResearchResponse,
    SearchResponse,
)
from tavily_fastmcp.server import create_server
from tavily_fastmcp.settings import Settings

fastmcp = pytest.importorskip("fastmcp")


class _FakeService:
    """Backend stub for metadata-only in-memory FastMCP integration tests."""

    def search_from_model(self, request=None, **kwargs):
        return SearchResponse(results=[])

    def extract_from_model(self, request=None, **kwargs):
        return ExtractResponse(results=[])

    def map_from_model(self, request=None, **kwargs):
        return MapResponse(results=[])

    def crawl_from_model(self, request=None, **kwargs):
        return CrawlResponse(results=[])

    def research_from_model(self, request=None, **kwargs):
        return ResearchResponse(status="submitted")

    def get_research_from_model(self, request=None, **kwargs):
        return ResearchResponse(status="completed")


def _create_test_server():
    return create_server(
        settings=Settings.model_construct(tavily_api_key="dummy", transport="stdio"),
        service=_FakeService(),
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_in_memory_server_exposes_profiles() -> None:
    """The server should expose profile resources and namespaced tools."""
    client = fastmcp.Client(_create_test_server())
    async with client:
        tools = await client.list_tools()
        resources = await client.list_resources()
    tool_names = {tool.name for tool in tools}
    resource_uris = {str(resource.uri) for resource in resources}
    assert "tavily.search" in tool_names
    assert "resource://tavily-fastmcp/catalog/server" in resource_uris


@pytest.mark.integration
@pytest.mark.asyncio
async def test_in_memory_server_exposes_prompt_catalog_resources() -> None:
    """The server should expose the expanded prompt and profile resource surfaces."""
    client = fastmcp.Client(_create_test_server())
    async with client:
        resources = await client.list_resources()
        resource_templates = await client.list_resource_templates()
    resource_uris = {str(resource.uri) for resource in resources}
    resource_template_uris = {template.uriTemplate for template in resource_templates}
    assert "resource://tavily-fastmcp/catalog/profiles" in resource_uris
    assert "resource://tavily-fastmcp/profile/{slug}" in resource_template_uris
