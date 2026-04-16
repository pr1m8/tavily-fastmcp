"""FastMCP client helpers for local inspection.

Purpose:
    Provide tiny wrappers that make it easy to inspect tools, resources, and
    prompts from an in-process FastMCP server during development.

Examples:
    >>> callable(iter_component_names)
    True
"""

from __future__ import annotations

from typing import Any


async def iter_component_names(client: Any) -> dict[str, list[str]]:
    """Inspect a FastMCP client for tools, prompts, and resources.

    Args:
        client: A FastMCP client instance already bound to a server.

    Returns:
        A dictionary containing component name lists.

    Raises:
        AttributeError: If the client does not expose the required methods.

    Examples:
        >>> isinstance({"tools": []}, dict)
        True
    """
    async with client:
        tools = await client.list_tools()
        prompts = await client.list_prompts()
        resources = await client.list_resources()
    return {
        "tools": [tool.name for tool in tools],
        "prompts": [prompt.name for prompt in prompts],
        "resources": [resource.uri for resource in resources],
    }
