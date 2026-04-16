"""Live Tavily integration tests.

These are intentionally opt-in and skipped unless both dependencies and
credentials are available.
"""

import os

import pytest

pytest.importorskip("langchain_tavily")

from tavily_fastmcp.service import LangChainTavilyService
from tavily_fastmcp.settings import Settings


@pytest.mark.integration
@pytest.mark.live
def test_live_search_smoke() -> None:
    """Perform a tiny real Tavily search when enabled."""
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key or os.environ.get("TAVILY_FASTMCP_ENABLE_LIVE_TESTS", "false").lower() != "true":
        pytest.skip("Live Tavily testing is disabled.")
    service = LangChainTavilyService(
        Settings.model_construct(
            tavily_api_key=api_key,
            transport="stdio",
            default_search_topic="general",
            default_search_depth="basic",
        )
    )
    response = service.search_from_model(query="FastMCP prompts docs", max_results=2)
    assert response.results
