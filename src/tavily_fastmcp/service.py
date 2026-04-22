"""Direct Tavily service layer.

Purpose:
    Offer a typed Python API that wraps ``langchain-tavily`` while keeping
    optional third-party imports out of package import time.

Design:
    - Define a protocol so tests can swap in a fake service.
    - Normalize upstream payloads into stable local models.
    - Keep network calls explicit and easy to mock.

Examples:
    >>> from tavily_fastmcp.models import SearchRequest
    >>> callable(SearchRequest)
    True
"""

from __future__ import annotations

from typing import Any, Protocol

from tavily_fastmcp.models import (
    CrawlHit,
    CrawlRequest,
    CrawlResponse,
    ExtractHit,
    ExtractRequest,
    ExtractResponse,
    GetResearchRequest,
    MapRequest,
    MapResponse,
    ResearchRequest,
    ResearchResponse,
    ResearchSource,
    SearchHit,
    SearchRequest,
    SearchResponse,
)
from tavily_fastmcp.settings import Settings

_SEARCH_CONSTRUCTOR_FIELDS = frozenset(
    {
        "auto_parameters",
        "country",
        "exact_match",
        "include_answer",
        "include_favicon",
        "include_image_descriptions",
        "include_raw_content",
        "include_usage",
        "max_results",
    }
)


class TavilyServiceProtocol(Protocol):
    """Protocol for Tavily operations used by the MCP server.

    Examples:
        >>> hasattr(TavilyServiceProtocol, '__class__')
        True
    """

    def search_from_model(
        self, request: SearchRequest | None = None, **kwargs: Any
    ) -> SearchResponse:
        """Execute a Tavily search request."""

    def extract_from_model(
        self, request: ExtractRequest | None = None, **kwargs: Any
    ) -> ExtractResponse:
        """Execute a Tavily extract request."""

    def map_from_model(self, request: MapRequest | None = None, **kwargs: Any) -> MapResponse:
        """Execute a Tavily map request."""

    def crawl_from_model(self, request: CrawlRequest | None = None, **kwargs: Any) -> CrawlResponse:
        """Execute a Tavily crawl request."""

    def research_from_model(
        self, request: ResearchRequest | None = None, **kwargs: Any
    ) -> ResearchResponse:
        """Execute a Tavily research request."""

    def get_research_from_model(
        self,
        request: GetResearchRequest | None = None,
        **kwargs: Any,
    ) -> ResearchResponse:
        """Retrieve a Tavily research task."""


class LangChainTavilyService:
    """Production Tavily service backed by :mod:`langchain_tavily`.

    Args:
        settings: Package settings containing the Tavily API key and
            defaults for topic and depth.

    Returns:
        A service object able to execute Tavily operations.

    Raises:
        RuntimeError: If ``langchain_tavily`` is not installed.

    Examples:
        >>> service = LangChainTavilyService.__new__(LangChainTavilyService)
        >>> service is not None
        True
    """

    def __init__(self, settings: Settings) -> None:
        """Initialize LangChain Tavily tools from validated settings."""
        self.settings = settings
        try:
            from langchain_tavily import (
                TavilyCrawl,
                TavilyExtract,
                TavilyGetResearch,
                TavilyMap,
                TavilyResearch,
                TavilySearch,
            )
        except ImportError as exc:  # pragma: no cover - dependency dependent
            raise RuntimeError(
                "langchain-tavily is required for LangChainTavilyService. "
                "Install the runtime dependencies first."
            ) from exc

        self._search_tool_cls = TavilySearch
        self._search_tool = TavilySearch(
            max_results=5,
            topic=settings.default_search_topic,
            search_depth=settings.default_search_depth,
        )
        self._extract_tool = TavilyExtract()
        self._map_tool = TavilyMap()
        self._crawl_tool = TavilyCrawl()
        self._research_tool = TavilyResearch()
        self._get_research_tool = TavilyGetResearch()

    def search_from_model(
        self,
        request: SearchRequest | None = None,
        **kwargs: Any,
    ) -> SearchResponse:
        """Execute a search request.

        Args:
            request: Optional typed request.
            **kwargs: Alternative field values when no request is supplied.

        Returns:
            A normalized search response.

        Raises:
            RuntimeError: If the underlying tool call fails.

        Examples:
            >>> callable(LangChainTavilyService.search_from_model)
            True
        """
        model = request or SearchRequest(**kwargs)
        payload = model.model_dump(exclude_none=True)
        search_tool_factory = getattr(self, "_search_tool_cls", None)
        if search_tool_factory is not None:
            constructor_payload = {
                field: payload.pop(field)
                for field in _SEARCH_CONSTRUCTOR_FIELDS
                if field in payload
            }
            raw = search_tool_factory(**constructor_payload).invoke(payload)
        else:
            raw = self._search_tool.invoke(payload)
        self._raise_if_error(raw)
        return self._normalize_search_response(raw)

    def extract_from_model(
        self,
        request: ExtractRequest | None = None,
        **kwargs: Any,
    ) -> ExtractResponse:
        """Execute an extract request."""
        model = request or ExtractRequest(**kwargs)
        raw = self._extract_tool.invoke(model.model_dump(mode="json", exclude_none=True))
        self._raise_if_error(raw)
        return self._normalize_extract_response(raw)

    def map_from_model(self, request: MapRequest | None = None, **kwargs: Any) -> MapResponse:
        """Execute a map request."""
        model = request or MapRequest(**kwargs)
        raw = self._map_tool.invoke(model.model_dump(mode="json", exclude_none=True))
        self._raise_if_error(raw)
        return self._normalize_map_response(raw)

    def crawl_from_model(self, request: CrawlRequest | None = None, **kwargs: Any) -> CrawlResponse:
        """Execute a crawl request."""
        model = request or CrawlRequest(**kwargs)
        raw = self._crawl_tool.invoke(model.model_dump(mode="json", exclude_none=True))
        self._raise_if_error(raw)
        return self._normalize_crawl_response(raw)

    def research_from_model(
        self,
        request: ResearchRequest | None = None,
        **kwargs: Any,
    ) -> ResearchResponse:
        """Execute a research request."""
        model = request or ResearchRequest(**kwargs)
        raw = self._research_tool.invoke(model.model_dump(exclude_none=True))
        self._raise_if_error(raw)
        return self._normalize_research_response(raw)

    def get_research_from_model(
        self,
        request: GetResearchRequest | None = None,
        **kwargs: Any,
    ) -> ResearchResponse:
        """Retrieve a research task."""
        model = request or GetResearchRequest(**kwargs)
        raw = self._get_research_tool.invoke(model.model_dump(exclude_none=True))
        self._raise_if_error(raw)
        return self._normalize_research_response(raw)

    @staticmethod
    def _raise_if_error(raw: dict[str, Any]) -> None:
        error = raw.get("error")
        if error is not None:
            raise RuntimeError(f"Tavily tool call failed: {error}")

    @staticmethod
    def _normalize_search_response(raw: dict[str, Any]) -> SearchResponse:
        return SearchResponse(
            query=raw.get("query"),
            answer=raw.get("answer"),
            results=[SearchHit(**item) for item in raw.get("results", [])],
            images=list(raw.get("images", []) or []),
            response_time=raw.get("response_time"),
            request_id=raw.get("request_id"),
            follow_up_questions=list(raw.get("follow_up_questions", []) or []),
            usage=raw.get("usage"),
        )

    @staticmethod
    def _normalize_extract_response(raw: dict[str, Any]) -> ExtractResponse:
        return ExtractResponse(
            results=[ExtractHit(**item) for item in raw.get("results", [])],
            failed_results=list(raw.get("failed_results", []) or []),
            response_time=raw.get("response_time"),
        )

    @staticmethod
    def _normalize_map_response(raw: dict[str, Any]) -> MapResponse:
        return MapResponse(
            base_url=raw.get("base_url"),
            results=list(raw.get("results", []) or []),
            request_id=raw.get("request_id"),
            response_time=raw.get("response_time"),
        )

    @staticmethod
    def _normalize_crawl_response(raw: dict[str, Any]) -> CrawlResponse:
        return CrawlResponse(
            base_url=raw.get("base_url"),
            results=[CrawlHit(**item) for item in raw.get("results", [])],
            request_id=raw.get("request_id"),
            response_time=raw.get("response_time"),
        )

    @staticmethod
    def _normalize_research_response(raw: dict[str, Any]) -> ResearchResponse:
        return ResearchResponse(
            request_id=raw.get("request_id"),
            created_at=raw.get("created_at"),
            completed_at=raw.get("completed_at"),
            status=raw.get("status"),
            input=raw.get("input"),
            model=raw.get("model"),
            content=raw.get("content"),
            sources=[ResearchSource(**item) for item in raw.get("sources", [])],
            response_time=raw.get("response_time"),
        )
