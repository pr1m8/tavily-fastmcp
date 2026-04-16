"""Unit tests for optional agent and client helpers."""

from __future__ import annotations

import sys
import types

import pytest

from tavily_fastmcp.agent import create_langchain_agent
from tavily_fastmcp.client import iter_component_names


class _FakeAsyncClient:
    """Tiny fake async client for component introspection tests."""

    async def __aenter__(self) -> "_FakeAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        return None

    async def list_tools(self):
        return [types.SimpleNamespace(name="tavily.search")]

    async def list_prompts(self):
        return [types.SimpleNamespace(name="tavily-router")]

    async def list_resources(self):
        return [types.SimpleNamespace(uri="resource://tavily-fastmcp/catalog/server")]


@pytest.mark.asyncio
async def test_iter_component_names_reads_tools_prompts_and_resources() -> None:
    """Client helper should gather names from the async client surface."""
    components = await iter_component_names(_FakeAsyncClient())
    assert components["tools"] == ["tavily.search"]
    assert components["prompts"] == ["tavily-router"]
    assert components["resources"] == ["resource://tavily-fastmcp/catalog/server"]


def test_create_langchain_agent_raises_without_dependency(monkeypatch) -> None:
    """Agent helper should raise a clear runtime error when LangChain is absent."""
    monkeypatch.setitem(sys.modules, "langchain", None)
    monkeypatch.setitem(sys.modules, "langchain.agents", None)
    with pytest.raises(RuntimeError):
        create_langchain_agent(model="openai:gpt-5", tools=[])


def test_create_langchain_agent_uses_router_prompt(monkeypatch) -> None:
    """Agent helper should pass the packaged router prompt into create_agent."""
    captured: dict[str, object] = {}

    def fake_create_agent(*, model: str, tools: list[object], system_prompt: str) -> dict[str, object]:
        captured["model"] = model
        captured["tools"] = tools
        captured["system_prompt"] = system_prompt
        return captured

    fake_agents_module = types.SimpleNamespace(create_agent=fake_create_agent)
    monkeypatch.setitem(sys.modules, "langchain", types.SimpleNamespace(agents=fake_agents_module))
    monkeypatch.setitem(sys.modules, "langchain.agents", fake_agents_module)

    result = create_langchain_agent(model="openai:gpt-5", tools=["tool"])
    assert result["model"] == "openai:gpt-5"
    assert result["tools"] == ["tool"]
    assert str(result["system_prompt"]).startswith("# Tavily Router")
