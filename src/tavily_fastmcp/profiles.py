"""Prompt profile registry.

Purpose:
    Publish reusable packaged workflow profiles that pair metadata with
    large markdown system prompts and MCP-facing discovery metadata.

Design:
    - Profiles are defined in code so tests can validate their structure.
    - Prompt bodies stay in markdown files so they can be edited easily.
    - Each profile maps cleanly to prompt and profile resource URIs.
    - The registry includes both operational profiles and documentation-heavy
      semantic guides for the full Tavily FastMCP surface.

Examples:
    >>> router = load_profile("router")
    >>> router.slug
    'router'
    >>> "tavily.search" in router.recommended_tools
    True
"""

from __future__ import annotations

from typing import Any, TypedDict

from tavily_fastmcp.models import ProfileSummary, PromptProfile
from tavily_fastmcp.prompt_loader import load_prompt_text

RESOURCE_PREFIX = "resource://tavily-fastmcp"


class _ProfileData(TypedDict):
    """Static metadata for a packaged prompt profile."""

    title: str
    summary: str
    use_when: list[str]
    avoid_when: list[str]
    recommended_tools: list[str]
    tags: list[str]
    meta: dict[str, Any]
    prompt_name: str


_PROFILE_DATA: dict[str, _ProfileData] = {
    "router": {
        "title": "Tavily Router",
        "summary": (
            "General-purpose routing profile that chooses the smallest correct Tavily workflow."
        ),
        "use_when": [
            "The user request is general and you need to choose the right Tavily capability.",
            "You want a system prompt that strongly discourages wasteful or redundant tool use.",
        ],
        "avoid_when": [
            "You already know the task is a deep research report.",
            "You need a narrow specialized prompt for site-only work.",
        ],
        "recommended_tools": ["tavily.search", "tavily.extract", "tavily.map", "tavily.crawl"],
        "tags": ["router", "default", "planning"],
        "meta": {"complexity": "medium", "recommended_default": True},
        "prompt_name": "router",
    },
    "suite-overview": {
        "title": "Tavily Suite Overview",
        "summary": "Massive composite semantic overview of the full Tavily FastMCP tool family.",
        "use_when": [
            "You want one authoritative overview of how all Tavily tools relate to each other.",
            "You are teaching another agent, client, or system prompt how the full suite works.",
        ],
        "avoid_when": [
            "You need the shortest possible router prompt rather than a large semantic reference.",
        ],
        "recommended_tools": [
            "tavily.search",
            "tavily.extract",
            "tavily.map",
            "tavily.crawl",
            "tavily.research",
            "tavily.get_research",
        ],
        "tags": ["overview", "composite", "suite", "reference"],
        "meta": {"complexity": "high", "reference_profile": True},
        "prompt_name": "suite_overview",
    },
    "quick-search": {
        "title": "Quick Search",
        "summary": "Lean prompt for broad web discovery followed by minimal extraction.",
        "use_when": [
            "The user mainly needs a quick answer grounded in a small number of sources.",
            "Fresh web discovery matters but a full research job would be excessive.",
        ],
        "avoid_when": [
            "The task requires a site-wide crawl or a long-form research report.",
        ],
        "recommended_tools": ["tavily.search", "tavily.extract"],
        "tags": ["search", "lightweight", "web"],
        "meta": {"complexity": "low", "latency_profile": "fast"},
        "prompt_name": "quick_search",
    },
    "tool-search": {
        "title": "Search Tool Guide",
        "summary": (
            "Deep operational guide for Tavily web search as the suite's discovery primitive."
        ),
        "use_when": [
            "You want an in-depth explanation of what search does, when it should be first, "
            "and how it hands off to extract.",
            "You need a discovery-specific system prompt rather than the general router.",
        ],
        "avoid_when": [
            "The user already provided exact URLs.",
        ],
        "recommended_tools": ["tavily.search", "tavily.extract"],
        "tags": ["search", "discovery", "reference", "deep-guide"],
        "meta": {"complexity": "medium", "tool_focus": "tavily.search"},
        "prompt_name": "tool_search_master",
    },
    "extract-and-summarize": {
        "title": "Extract and Summarize",
        "summary": "URL-first profile for known pages and precise extraction work.",
        "use_when": [
            "The user has already supplied URLs.",
            "Search is unnecessary and extraction quality matters more than discovery breadth.",
        ],
        "avoid_when": [
            "The relevant URLs are still unknown.",
        ],
        "recommended_tools": ["tavily.extract"],
        "tags": ["extract", "url-first", "summarization"],
        "meta": {"complexity": "low"},
        "prompt_name": "extract_and_summarize",
    },
    "tool-extract": {
        "title": "Extract Tool Guide",
        "summary": "Deep operational guide for Tavily URL extraction and page-grounded synthesis.",
        "use_when": [
            "You want a richer extract-specific prompt than the shorter "
            "extract-and-summarize profile.",
            "You need guidance about page weighting, version conflicts, and URL-first discipline.",
        ],
        "avoid_when": [
            "The problem is still broad discovery rather than page reading.",
        ],
        "recommended_tools": ["tavily.extract"],
        "tags": ["extract", "reference", "deep-guide", "url-reading"],
        "meta": {"complexity": "medium", "tool_focus": "tavily.extract"},
        "prompt_name": "tool_extract_master",
    },
    "site-discovery": {
        "title": "Site Discovery",
        "summary": "Map-first profile for finding the right pages inside one site.",
        "use_when": [
            "The user asks for docs pages or site structure.",
            "You need candidate URLs before reading content.",
        ],
        "avoid_when": [
            "The user already gave exact URLs.",
            "The task is cross-site research, not site-local discovery.",
        ],
        "recommended_tools": ["tavily.map", "tavily.extract"],
        "tags": ["map", "docs", "navigation"],
        "meta": {"complexity": "medium"},
        "prompt_name": "site_discovery",
    },
    "tool-map": {
        "title": "Map Tool Guide",
        "summary": "Deep operational guide for Tavily site mapping and URL shortlisting.",
        "use_when": [
            "You want a site-discovery-specific reference prompt rather than only the "
            "shorter site-discovery profile.",
            "You need stronger guidance on how map differs from crawl and extract.",
        ],
        "avoid_when": [
            "You already know the exact pages to read.",
        ],
        "recommended_tools": ["tavily.map", "tavily.extract"],
        "tags": ["map", "reference", "deep-guide", "site-structure"],
        "meta": {"complexity": "medium", "tool_focus": "tavily.map"},
        "prompt_name": "tool_map_master",
    },
    "site-crawl": {
        "title": "Site Crawl",
        "summary": "Site-focused profile for multi-page extraction across one domain.",
        "use_when": [
            "The answer lives across many pages in a docs site or help center.",
            "A map-only pass is too shallow.",
        ],
        "avoid_when": [
            "A handful of exact URLs would answer the question.",
        ],
        "recommended_tools": ["tavily.crawl", "tavily.extract"],
        "tags": ["crawl", "docs", "knowledge-base"],
        "meta": {"complexity": "medium", "latency_profile": "moderate"},
        "prompt_name": "site_crawl",
    },
    "tool-crawl": {
        "title": "Crawl Tool Guide",
        "summary": "Deep operational guide for scoped multi-page site traversal and synthesis.",
        "use_when": [
            "You need a stronger crawl-specific reference prompt than the shorter "
            "site-crawl profile.",
            "You want guidance on scope, synthesis, and crawl anti-patterns.",
        ],
        "avoid_when": [
            "The answer is likely on one or two pages.",
        ],
        "recommended_tools": ["tavily.crawl", "tavily.extract"],
        "tags": ["crawl", "reference", "deep-guide", "site-reading"],
        "meta": {"complexity": "medium", "tool_focus": "tavily.crawl"},
        "prompt_name": "tool_crawl_master",
    },
    "deep-research": {
        "title": "Deep Research",
        "summary": "Long-form research profile for structured reports and comprehensive synthesis.",
        "use_when": [
            "The user explicitly asks for research, a report, or a deep comparison.",
            "You need structured output or multi-step evidence collection.",
        ],
        "avoid_when": [
            "A small search plus extraction would suffice.",
        ],
        "recommended_tools": ["tavily.research", "tavily.get_research"],
        "tags": ["research", "report", "structured-output"],
        "meta": {"complexity": "high", "latency_profile": "slow"},
        "prompt_name": "deep_research",
    },
    "tool-research": {
        "title": "Research Tool Guide",
        "summary": (
            "Deep operational guide for Tavily research jobs, objective framing, "
            "and report-shaped outputs."
        ),
        "use_when": [
            "You want a research-specific reference prompt with heavier emphasis on "
            "framing and deliverable shape.",
            "You need to teach another agent what makes research worth using at all.",
        ],
        "avoid_when": [
            "The task is still a narrow factual lookup.",
        ],
        "recommended_tools": ["tavily.research", "tavily.get_research"],
        "tags": ["research", "reference", "deep-guide", "reporting"],
        "meta": {"complexity": "high", "tool_focus": "tavily.research"},
        "prompt_name": "tool_research_master",
    },
    "tool-get-research": {
        "title": "Get Research Tool Guide",
        "summary": "Deep operational guide for retrieving and interpreting Tavily research jobs.",
        "use_when": [
            "You need a separate explanation of research retrieval semantics and "
            "asynchronous workflow handling.",
        ],
        "avoid_when": [
            "No research task has been created yet.",
        ],
        "recommended_tools": ["tavily.get_research"],
        "tags": ["research", "retrieval", "reference", "deep-guide"],
        "meta": {"complexity": "medium", "tool_focus": "tavily.get_research"},
        "prompt_name": "tool_get_research_master",
    },
    "routing-matrix": {
        "title": "Routing Matrix",
        "summary": "Compact but strict decision matrix for selecting Tavily tools and transitions.",
        "use_when": [
            "You want a terse decision framework instead of a narrative profile.",
            "You are implementing deterministic routing logic or policy checks.",
        ],
        "avoid_when": [
            "You need a more narrative pedagogical explanation.",
        ],
        "recommended_tools": [
            "tavily.search",
            "tavily.extract",
            "tavily.map",
            "tavily.crawl",
            "tavily.research",
            "tavily.get_research",
        ],
        "tags": ["routing", "matrix", "decision-table", "reference"],
        "meta": {"complexity": "medium"},
        "prompt_name": "routing_matrix",
    },
    "synthesis-policy": {
        "title": "Synthesis Policy",
        "summary": (
            "Answer-shaping and grounding policy for turning Tavily retrieval into "
            "user-facing responses."
        ),
        "use_when": [
            "You want a final-answer policy layer that sits above retrieval routing.",
            "You need stronger guardrails around inference, uncertainty, and conflicting sources.",
        ],
        "avoid_when": [
            "You only need the retrieval policy and not answer-writing policy.",
        ],
        "recommended_tools": [
            "tavily.search",
            "tavily.extract",
            "tavily.map",
            "tavily.crawl",
            "tavily.research",
            "tavily.get_research",
        ],
        "tags": ["synthesis", "policy", "grounding", "answering"],
        "meta": {"complexity": "medium"},
        "prompt_name": "synthesis_policy",
    },
    "mcp-usage-guide": {
        "title": "MCP Usage Guide",
        "summary": (
            "Explains the server as an MCP product with tools, prompts, resources, "
            "namespacing, and templates."
        ),
        "use_when": [
            "You want client-facing guidance about how to consume the server through MCP.",
            "You need a product-level prompt about namespacing, resources, and discoverability.",
        ],
        "avoid_when": [
            "You only care about Tavily semantics and not MCP surfacing.",
        ],
        "recommended_tools": ["tavily.catalog", "tavily.health"],
        "tags": ["mcp", "resources", "prompts", "templates", "reference"],
        "meta": {"complexity": "medium", "surface": "mcp"},
        "prompt_name": "mcp_usage_guide",
    },
}


def list_profiles() -> list[ProfileSummary]:
    """Return summary metadata for all packaged profiles.

    Returns:
        Sorted profile summaries.

    Raises:
        FileNotFoundError: If a packaged prompt file is missing.

    Examples:
        >>> any(profile.slug == "router" for profile in list_profiles())
        True
    """
    summaries: list[ProfileSummary] = []
    for slug, data in sorted(_PROFILE_DATA.items()):
        summaries.append(
            ProfileSummary(
                slug=slug,
                title=str(data["title"]),
                summary=str(data["summary"]),
                tags=list(data["tags"]),
                recommended_tools=list(data["recommended_tools"]),
                prompt_resource_uri=f"{RESOURCE_PREFIX}/prompt/{slug}",
                profile_resource_uri=f"{RESOURCE_PREFIX}/profile/{slug}",
            )
        )
    return summaries


def load_profile(slug: str) -> PromptProfile:
    """Load a full packaged prompt profile.

    Args:
        slug: Stable profile slug.

    Returns:
        The full prompt profile.

    Raises:
        KeyError: If the profile slug is unknown.
        FileNotFoundError: If the prompt markdown file is missing.

    Examples:
        >>> load_profile("deep-research").title
        'Deep Research'
    """
    if slug not in _PROFILE_DATA:
        raise KeyError(f"Unknown prompt profile: {slug}")
    data = _PROFILE_DATA[slug]
    prompt_name = str(data["prompt_name"])
    return PromptProfile(
        slug=slug,
        title=str(data["title"]),
        summary=str(data["summary"]),
        use_when=list(data["use_when"]),
        avoid_when=list(data["avoid_when"]),
        recommended_tools=list(data["recommended_tools"]),
        tags=list(data["tags"]),
        meta=dict(data["meta"]),
        prompt_markdown=load_prompt_text(prompt_name),
    )


def profile_to_markdown(profile: PromptProfile) -> str:
    """Render a profile to a human-readable markdown document.

    Args:
        profile: The profile to render.

    Returns:
        Markdown that combines metadata with prompt text.

    Raises:
        ValueError: If rendering fails.

    Examples:
        >>> md = profile_to_markdown(load_profile("router"))
        >>> md.startswith("# ")
        True
    """
    use_when = "\n".join(f"- {item}" for item in profile.use_when)
    avoid_when = "\n".join(f"- {item}" for item in profile.avoid_when)
    tools = "\n".join(f"- {tool}" for tool in profile.recommended_tools)
    tags = ", ".join(profile.tags)
    return (
        f"# {profile.title}\n\n"
        f"**Slug:** `{profile.slug}`\n\n"
        f"**Summary:** {profile.summary}\n\n"
        f"**Tags:** {tags}\n\n"
        f"## Use when\n\n{use_when}\n\n"
        f"## Avoid when\n\n{avoid_when}\n\n"
        f"## Recommended tools\n\n{tools}\n\n"
        f"## Prompt\n\n{profile.prompt_markdown}\n"
    )
