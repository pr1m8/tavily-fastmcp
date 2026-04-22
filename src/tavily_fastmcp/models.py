"""Typed models for Tavily FastMCP.

Purpose:
    Define canonical request, response, catalog, and profile models.

Design:
    - Request models are strict and reject unknown fields.
    - Response models allow extra fields because upstream Tavily payloads
      may evolve.
    - Profile and catalog models are shared between direct Python helpers,
      packaged resources, and MCP prompts.

Examples:
    >>> SearchRequest(query="FastMCP docs").max_results
    5
    >>> ProfileSummary(slug="router", title="Router", summary="x").slug
    'router'
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import AnyUrl, BaseModel, ConfigDict, Field

type JsonObject = dict[str, Any]


class SearchRequest(BaseModel):
    """Canonical request model for Tavily search.

    Args:
        query: Natural-language search query.
        max_results: Maximum number of results.
        topic: Tavily topic mode.
        include_answer: Whether to include Tavily's answer field.
        include_raw_content: Whether to return cleaned page content.
        include_images: Whether to include image URLs.
        include_image_descriptions: Whether to include image descriptions.
        search_depth: Tavily search depth.
        time_range: Relative time filter.
        start_date: Inclusive start bound in ``YYYY-MM-DD`` format.
        end_date: Inclusive end bound in ``YYYY-MM-DD`` format.
        include_domains: Domains to include.
        exclude_domains: Domains to exclude.
        include_usage: Whether to return usage metadata.

    Returns:
        A validated request object.

    Raises:
        ValueError: If a field is invalid.

    Examples:
        >>> SearchRequest(query="FastMCP resources", max_results=3).max_results
        3
    """

    model_config = ConfigDict(extra="forbid")

    query: str
    max_results: int = Field(default=5, ge=1, le=20)
    topic: Literal["general", "news", "finance"] = "general"
    include_answer: bool = False
    include_raw_content: bool = False
    include_images: bool = False
    include_image_descriptions: bool = False
    search_depth: Literal["basic", "advanced"] = "basic"
    time_range: Literal["day", "week", "month", "year"] | None = None
    start_date: str | None = None
    end_date: str | None = None
    include_domains: list[str] | None = None
    exclude_domains: list[str] | None = None
    include_usage: bool = False


class ExtractRequest(BaseModel):
    """Canonical request model for Tavily extract.

    Args:
        urls: URLs to extract.
        extract_depth: Extraction depth.
        include_images: Whether to include images.

    Returns:
        A validated request object.

    Raises:
        ValueError: If a field is invalid.

    Examples:
        >>> ExtractRequest(urls=["https://example.com"]).extract_depth
        'basic'
    """

    model_config = ConfigDict(extra="forbid")

    urls: list[AnyUrl] = Field(min_length=1)
    extract_depth: Literal["basic", "advanced"] = "basic"
    include_images: bool = False


class MapRequest(BaseModel):
    """Canonical request model for Tavily map."""

    model_config = ConfigDict(extra="forbid")

    url: AnyUrl
    instructions: str | None = None


class CrawlRequest(BaseModel):
    """Canonical request model for Tavily crawl."""

    model_config = ConfigDict(extra="forbid")

    url: AnyUrl
    instructions: str | None = None


class ResearchRequest(BaseModel):
    """Canonical request model for Tavily research."""

    model_config = ConfigDict(extra="forbid")

    input: str
    model: Literal["mini", "pro", "auto"] = "auto"
    output_schema: JsonObject | None = None
    stream: bool = False
    citation_format: Literal["numbered", "mla", "apa", "chicago"] = "numbered"


class GetResearchRequest(BaseModel):
    """Canonical request model for retrieving a Tavily research task."""

    model_config = ConfigDict(extra="forbid")

    request_id: str


class SearchHit(BaseModel):
    """Normalized Tavily search hit."""

    model_config = ConfigDict(extra="allow")

    url: str
    title: str | None = None
    content: str | None = None
    raw_content: str | None = None
    score: float | None = None
    published_date: str | None = None


class SearchResponse(BaseModel):
    """Normalized Tavily search response."""

    model_config = ConfigDict(extra="allow")

    query: str | None = None
    answer: str | None = None
    results: list[SearchHit] = Field(default_factory=list)
    images: list[str] = Field(default_factory=list)
    response_time: float | None = None
    request_id: str | None = None
    follow_up_questions: list[str] = Field(default_factory=list)
    usage: JsonObject | None = None


class ExtractHit(BaseModel):
    """Normalized Tavily extract result item."""

    model_config = ConfigDict(extra="allow")

    url: str
    raw_content: str | None = None
    images: list[str] = Field(default_factory=list)


class ExtractResponse(BaseModel):
    """Normalized Tavily extract response."""

    model_config = ConfigDict(extra="allow")

    results: list[ExtractHit] = Field(default_factory=list)
    failed_results: list[JsonObject] = Field(default_factory=list)
    response_time: float | None = None


class MapResponse(BaseModel):
    """Normalized Tavily map response."""

    model_config = ConfigDict(extra="allow")

    base_url: str | None = None
    results: list[str] = Field(default_factory=list)
    request_id: str | None = None
    response_time: float | None = None


class CrawlHit(BaseModel):
    """Normalized Tavily crawl result item."""

    model_config = ConfigDict(extra="allow")

    url: str
    raw_content: str | None = None


class CrawlResponse(BaseModel):
    """Normalized Tavily crawl response."""

    model_config = ConfigDict(extra="allow")

    base_url: str | None = None
    results: list[CrawlHit] = Field(default_factory=list)
    request_id: str | None = None
    response_time: float | None = None


class ResearchSource(BaseModel):
    """Source used by a Tavily research task."""

    model_config = ConfigDict(extra="allow")

    title: str | None = None
    url: str | None = None
    favicon: str | None = None


class ResearchResponse(BaseModel):
    """Normalized Tavily research response."""

    model_config = ConfigDict(extra="allow")

    request_id: str | None = None
    created_at: str | None = None
    completed_at: str | None = None
    status: str | None = None
    input: str | None = None
    model: str | None = None
    content: str | JsonObject | None = None
    sources: list[ResearchSource] = Field(default_factory=list)
    response_time: float | None = None


class ProfileSummary(BaseModel):
    """Summary metadata for a packaged prompt profile.

    Args:
        slug: Stable profile slug.
        title: Human-readable title.
        summary: One-sentence profile summary.
        tags: Tags for filtering and discovery.
        recommended_tools: Ordered preferred tool names.
        prompt_resource_uri: Resource URI for the prompt text.
        profile_resource_uri: Resource URI for structured profile metadata.

    Returns:
        A reusable profile summary object.

    Raises:
        ValueError: If a field is invalid.

    Examples:
        >>> ProfileSummary(
        ...     slug="router",
        ...     title="Router",
        ...     summary="Route tasks",
        ...     prompt_resource_uri="resource://x",
        ...     profile_resource_uri="resource://y",
        ... ).slug
        'router'
    """

    slug: str
    title: str
    summary: str
    tags: list[str] = Field(default_factory=list)
    recommended_tools: list[str] = Field(default_factory=list)
    prompt_resource_uri: str
    profile_resource_uri: str


class PromptProfile(BaseModel):
    """Structured packaged profile with markdown prompt content.

    Args:
        slug: Stable profile slug.
        title: Human-readable title.
        summary: Short description.
        use_when: List of ideal use cases.
        avoid_when: List of anti-patterns.
        recommended_tools: Preferred tool sequence.
        tags: Discovery tags.
        meta: Arbitrary profile metadata.
        prompt_markdown: Full markdown prompt body.

    Returns:
        A rich profile object.

    Raises:
        ValueError: If a field is invalid.

    Examples:
        >>> profile = PromptProfile(
        ...     slug="router",
        ...     title="Router",
        ...     summary="Route tasks",
        ...     prompt_markdown="# Router",
        ... )
        >>> profile.title
        'Router'
    """

    slug: str
    title: str
    summary: str
    use_when: list[str] = Field(default_factory=list)
    avoid_when: list[str] = Field(default_factory=list)
    recommended_tools: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    meta: JsonObject = Field(default_factory=dict)
    prompt_markdown: str


class ServerCatalog(BaseModel):
    """Catalog of server metadata exposed through resources and tools."""

    name: str
    version: str
    package_name: str
    prompt_names: list[str] = Field(default_factory=list)
    profile_slugs: list[str] = Field(default_factory=list)
    tool_names: list[str] = Field(default_factory=list)
    resource_uris: list[str] = Field(default_factory=list)
    example_resource_uris: list[str] = Field(default_factory=list)
    meta: JsonObject = Field(default_factory=dict)


class HealthResponse(BaseModel):
    """Simple health payload."""

    status: Literal["ok"]
    server_name: str
    version: str
