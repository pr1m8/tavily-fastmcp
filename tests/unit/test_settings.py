"""Unit tests for settings."""

from __future__ import annotations

from tavily_fastmcp.settings import Settings



def test_settings_alias_model_construct() -> None:
    """Settings should support model construction for tests."""
    settings = Settings.model_construct(tavily_api_key="dummy", transport="stdio")
    assert settings.transport == "stdio"


def test_settings_reads_canonical_tavily_env_var(monkeypatch) -> None:
    """The settings model should read Tavily's canonical API key environment variable."""
    monkeypatch.setenv("TAVILY_API_KEY", "dummy-key")
    settings = Settings()
    assert settings.tavily_api_key.get_secret_value() == "dummy-key"
