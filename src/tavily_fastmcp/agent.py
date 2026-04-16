"""Optional LangChain agent helpers.

Purpose:
    Offer a tiny convenience layer for wiring this package's packaged router
    prompt into a LangChain agent.

Design:
    - Keep imports optional so the package remains usable without LangChain.
    - Accept explicit tools for flexibility.

Examples:
    >>> callable(create_langchain_agent)
    True
"""

from __future__ import annotations

from typing import Any

from tavily_fastmcp.prompt_loader import load_prompt_text


def create_langchain_agent(*, model: str, tools: list[Any]) -> Any:
    """Create a LangChain agent with the packaged router prompt.

    Args:
        model: LangChain model identifier.
        tools: Tools to pass into ``create_agent``.

    Returns:
        A LangChain agent instance.

    Raises:
        RuntimeError: If LangChain is not installed.

    Examples:
        >>> callable(create_langchain_agent)
        True
    """
    try:
        from langchain.agents import create_agent
    except ImportError as exc:  # pragma: no cover - dependency dependent
        raise RuntimeError(
            "LangChain is required for create_langchain_agent(). Install the langchain extra."
        ) from exc
    return create_agent(model=model, tools=tools, system_prompt=load_prompt_text("router"))
