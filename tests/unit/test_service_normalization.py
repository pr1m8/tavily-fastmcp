"""Unit tests for Tavily response normalization helpers."""

from __future__ import annotations

from tavily_fastmcp.service import LangChainTavilyService


def test_normalize_search_response_keeps_key_fields() -> None:
    """Search normalization should preserve the main result fields."""
    response = LangChainTavilyService._normalize_search_response(
        {
            "query": "fastmcp prompts",
            "answer": "FastMCP exposes prompts and resources.",
            "results": [
                {
                    "url": "https://example.com/docs",
                    "title": "Docs",
                    "content": "Prompt docs.",
                    "score": 0.91,
                }
            ],
            "images": ["https://example.com/image.png"],
            "follow_up_questions": ["What about templates?"],
            "request_id": "req_123",
        }
    )
    assert response.query == "fastmcp prompts"
    assert response.answer is not None
    assert response.results[0].url == "https://example.com/docs"
    assert response.images == ["https://example.com/image.png"]
    assert response.follow_up_questions == ["What about templates?"]
    assert response.request_id == "req_123"


def test_normalize_extract_response_handles_empty_failures() -> None:
    """Extract normalization should coerce missing failure payloads to empty lists."""
    response = LangChainTavilyService._normalize_extract_response(
        {
            "results": [{"url": "https://example.com", "raw_content": "hello", "images": []}],
            "failed_results": None,
        }
    )
    assert response.results[0].url == "https://example.com"
    assert response.failed_results == []


def test_normalize_research_response_builds_sources() -> None:
    """Research normalization should convert source dictionaries into typed models."""
    response = LangChainTavilyService._normalize_research_response(
        {
            "request_id": "req_research",
            "status": "completed",
            "content": "A structured answer.",
            "sources": [{"title": "Official Docs", "url": "https://example.com"}],
        }
    )
    assert response.request_id == "req_research"
    assert response.status == "completed"
    assert response.sources[0].title == "Official Docs"
