"""Unit tests for service request execution methods."""

from __future__ import annotations

from typing import Any

from tavily_fastmcp.service import LangChainTavilyService


class _StubTool:
    """Simple stub tool that records payloads and returns canned data."""

    def __init__(self, result: dict[str, Any]) -> None:
        self.result = result
        self.calls: list[dict[str, Any]] = []

    def invoke(self, payload: dict[str, Any]) -> dict[str, Any]:
        self.calls.append(payload)
        return self.result



def _make_service() -> LangChainTavilyService:
    service = LangChainTavilyService.__new__(LangChainTavilyService)
    service._search_tool = _StubTool({"results": [{"url": "https://example.com"}]})
    service._extract_tool = _StubTool({"results": [{"url": "https://example.com", "raw_content": "x"}]})
    service._map_tool = _StubTool({"base_url": "https://example.com", "results": ["https://example.com/docs"]})
    service._crawl_tool = _StubTool({"base_url": "https://example.com", "results": [{"url": "https://example.com/docs", "raw_content": "docs"}]})
    service._research_tool = _StubTool({"request_id": "req_1", "status": "submitted"})
    service._get_research_tool = _StubTool({"request_id": "req_1", "status": "completed"})
    return service



def test_search_from_model_invokes_underlying_tool() -> None:
    """Search method should forward validated payloads to the tool."""
    service = _make_service()
    response = service.search_from_model(query="fastmcp", max_results=2)
    assert service._search_tool.calls[0]["query"] == "fastmcp"
    assert service._search_tool.calls[0]["max_results"] == 2
    assert response.results[0].url == "https://example.com"



def test_extract_from_model_invokes_underlying_tool() -> None:
    """Extract method should serialize URLs and return normalized results."""
    service = _make_service()
    response = service.extract_from_model(urls=["https://example.com"])
    assert service._extract_tool.calls[0]["urls"] == ["https://example.com/"]
    assert response.results[0].raw_content == "x"



def test_map_crawl_and_research_methods_invoke_tools() -> None:
    """Map, crawl, research, and get_research should all call their backends."""
    service = _make_service()
    map_response = service.map_from_model(url="https://example.com", instructions="find docs")
    crawl_response = service.crawl_from_model(url="https://example.com", instructions="read docs")
    research_response = service.research_from_model(input="research fastmcp")
    get_research_response = service.get_research_from_model(request_id="req_1")

    assert service._map_tool.calls[0]["instructions"] == "find docs"
    assert service._crawl_tool.calls[0]["instructions"] == "read docs"
    assert service._research_tool.calls[0]["input"] == "research fastmcp"
    assert service._get_research_tool.calls[0]["request_id"] == "req_1"
    assert map_response.results == ["https://example.com/docs"]
    assert crawl_response.results[0].url == "https://example.com/docs"
    assert research_response.request_id == "req_1"
    assert get_research_response.status == "completed"
