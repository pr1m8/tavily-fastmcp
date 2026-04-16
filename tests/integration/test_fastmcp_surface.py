"""Integration tests for the FastMCP surface.

These tests are skipped automatically when FastMCP is unavailable.
"""

from __future__ import annotations

import pytest

fastmcp = pytest.importorskip("fastmcp")

from tavily_fastmcp.server import create_server


@pytest.mark.integration
@pytest.mark.asyncio
async def test_in_memory_server_exposes_profiles() -> None:
    """The server should expose profile resources and namespaced tools."""
    client = fastmcp.Client(create_server())
    async with client:
        tools = await client.list_tools()
        resources = await client.list_resources()
    tool_names = {tool.name for tool in tools}
    resource_uris = {resource.uri for resource in resources}
    assert "tavily.search" in tool_names
    assert "resource://tavily-fastmcp/catalog/server" in resource_uris


@pytest.mark.integration
@pytest.mark.asyncio
async def test_in_memory_server_exposes_prompt_catalog_resources() -> None:
    """The server should expose the expanded prompt and profile resource surfaces."""
    client = fastmcp.Client(create_server())
    async with client:
        resources = await client.list_resources()
    resource_uris = {resource.uri for resource in resources}
    assert "resource://tavily-fastmcp/catalog/profiles" in resource_uris
    assert any("resource://tavily-fastmcp/profile/" in uri for uri in resource_uris)
