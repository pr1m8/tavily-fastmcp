"""Settings for the Tavily FastMCP package.

Purpose:
    Centralize environment-backed configuration for direct Python use,
    MCP server startup, and test execution.

Design:
    - Preserve Tavily's canonical ``TAVILY_API_KEY`` environment variable.
    - Namespace local runtime settings under ``TAVILY_FASTMCP_``.
    - Cache the validated settings object for ergonomic reuse.

Examples:
    >>> from tavily_fastmcp.settings import Settings
    >>> settings = Settings.model_construct(
    ...     tavily_api_key="dummy",
    ...     transport="stdio",
    ... )
    >>> settings.transport
    'stdio'
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for :mod:`tavily_fastmcp`.

    Args:
        tavily_api_key: Tavily API key read from ``TAVILY_API_KEY``.
        transport: MCP transport to run when using the CLI.
        host: Hostname for streamable HTTP or SSE style transports.
        port: TCP port for HTTP-based transports.
        log_level: Logging verbosity.
        default_search_topic: Default Tavily topic.
        default_search_depth: Default Tavily search depth.
        enable_live_tests: Whether live integration tests are enabled.

    Returns:
        A validated settings object.

    Raises:
        ValueError: If one or more settings values are invalid.

    Examples:
        >>> settings = Settings.model_construct(
        ...     tavily_api_key="dummy",
        ...     transport="stdio",
        ... )
        >>> settings.transport
        'stdio'
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="TAVILY_FASTMCP_",
        extra="ignore",
    )

    tavily_api_key: SecretStr = Field(..., alias="TAVILY_API_KEY")
    transport: Literal["stdio", "http", "sse"] = "stdio"
    host: str = "127.0.0.1"
    port: int = 8001
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    default_search_topic: Literal["general", "news", "finance"] = "general"
    default_search_depth: Literal["basic", "advanced"] = "basic"
    enable_live_tests: bool = False


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the cached package settings.

    Returns:
        The cached validated settings object.

    Raises:
        ValueError: If required environment variables are missing.

    Examples:
        >>> from tavily_fastmcp.settings import get_settings
        >>> callable(get_settings)
        True
    """
    return Settings()
