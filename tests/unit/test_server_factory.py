"""Unit tests for the server factory using a fake FastMCP surface."""

from __future__ import annotations

import sys
import types

import pytest

from tavily_fastmcp.models import (
    CrawlResponse,
    ExtractResponse,
    HealthResponse,
    MapResponse,
    ResearchResponse,
    SearchHit,
    SearchResponse,
)
from tavily_fastmcp.server import build_arg_parser, create_server, main
from tavily_fastmcp.settings import Settings


class _FakeContext:
    """Minimal async context object."""

    def __init__(self) -> None:
        self.messages: list[str] = []

    async def info(self, message: str) -> None:
        self.messages.append(message)


class _FakeFastMCP:
    """Tiny decorator-based server shim for unit tests."""

    def __init__(self, name: str, instructions: str, include_fastmcp_meta: bool) -> None:
        self.name = name
        self.instructions = instructions
        self.include_fastmcp_meta = include_fastmcp_meta
        self.tools: list[types.SimpleNamespace] = []
        self.resources: list[types.SimpleNamespace] = []
        self.prompts: list[types.SimpleNamespace] = []
        self.last_run_transport: str | None = None

    def resource(self, **metadata):
        def decorator(func):
            self.resources.append(types.SimpleNamespace(func=func, **metadata))
            return func
        return decorator

    def prompt(self, **metadata):
        def decorator(func):
            self.prompts.append(types.SimpleNamespace(func=func, **metadata))
            return func
        return decorator

    def tool(self, **metadata):
        def decorator(func):
            self.tools.append(types.SimpleNamespace(func=func, **metadata))
            return func
        return decorator

    def run(self, transport: str) -> None:
        self.last_run_transport = transport


class _FakeService:
    """Fake backend used to exercise server tool handlers."""

    def search_from_model(self, request=None, **kwargs):
        return SearchResponse(query=request.query, results=[SearchHit(url="https://example.com")])

    def extract_from_model(self, request=None, **kwargs):
        return ExtractResponse(results=[])

    def map_from_model(self, request=None, **kwargs):
        return MapResponse(base_url=str(request.url), results=[str(request.url)])

    def crawl_from_model(self, request=None, **kwargs):
        return CrawlResponse(base_url=str(request.url), results=[])

    def research_from_model(self, request=None, **kwargs):
        return ResearchResponse(request_id="req_1", status="submitted")

    def get_research_from_model(self, request=None, **kwargs):
        return ResearchResponse(request_id=request.request_id, status="completed")


@pytest.fixture
def fake_fastmcp(monkeypatch):
    """Install a fake FastMCP module for server factory tests."""
    fake_module = types.SimpleNamespace(FastMCP=_FakeFastMCP, Context=_FakeContext)
    monkeypatch.setitem(sys.modules, "fastmcp", fake_module)
    return fake_module


@pytest.mark.asyncio
async def test_create_server_registers_resources_prompts_and_tools(fake_fastmcp) -> None:
    """Server factory should register the expected MCP surface components."""
    server = create_server(
        settings=Settings.model_construct(tavily_api_key="dummy", transport="stdio"),
        service=_FakeService(),
    )
    tool_names = {entry.name for entry in server.tools}
    prompt_names = {entry.name for entry in server.prompts}
    resource_uris = {entry.uri for entry in server.resources}

    assert "tavily.search" in tool_names
    assert "tavily.extract" in tool_names
    assert "tavily-router" in prompt_names
    assert "tavily-profile" in prompt_names
    assert "resource://tavily-fastmcp/catalog/server" in resource_uris
    assert server.instructions.startswith("# Tavily Router")

    health_tool = next(entry for entry in server.tools if entry.name == "tavily.health")
    catalog_tool = next(entry for entry in server.tools if entry.name == "tavily.catalog")
    search_tool = next(entry for entry in server.tools if entry.name == "tavily.search")
    profile_prompt = next(entry for entry in server.prompts if entry.name == "tavily-profile")
    profile_resource = next(entry for entry in server.resources if entry.uri.endswith("/profile/{slug}"))
    prompt_resource = next(entry for entry in server.resources if entry.uri.endswith("/prompt/{name}"))

    ctx = _FakeContext()
    health = await health_tool.func(ctx=ctx)
    catalog = await catalog_tool.func(ctx=ctx)
    search = await search_tool.func(query="fastmcp docs", ctx=ctx)

    assert isinstance(health, HealthResponse)
    assert health.status == "ok"
    assert "Health check requested." in ctx.messages
    assert "tavily.search" in catalog.tool_names
    assert search.results[0].url == "https://example.com"
    assert "Bound request" in profile_prompt.func("suite-overview", "Explain the suite")
    assert profile_resource.func("suite-overview")["title"] == "Tavily Suite Overview"
    assert prompt_resource.func("suite_overview").startswith("# Tavily FastMCP Suite Overview")


def test_create_server_raises_when_fastmcp_missing(monkeypatch) -> None:
    """Server factory should raise a friendly error when FastMCP is unavailable."""
    monkeypatch.setitem(sys.modules, "fastmcp", None)
    with pytest.raises(RuntimeError):
        create_server(settings=Settings.model_construct(tavily_api_key="dummy", transport="stdio"), service=_FakeService())


def test_build_arg_parser_and_main(fake_fastmcp, monkeypatch) -> None:
    """CLI entrypoint should respect transport overrides and call run on the server."""
    parser = build_arg_parser()
    assert parser.parse_args(["--transport", "stdio"]).transport == "stdio"

    fake_server = _FakeFastMCP(name="x", instructions="y", include_fastmcp_meta=True)
    monkeypatch.setattr("tavily_fastmcp.server.get_settings", lambda: Settings.model_construct(tavily_api_key="dummy", transport="stdio"))
    monkeypatch.setattr("tavily_fastmcp.server.create_server", lambda settings=None: fake_server)
    monkeypatch.setattr(sys, "argv", ["tavily-fastmcp", "--transport", "http"])
    main()
    assert fake_server.last_run_transport == "http"
