"""Inspect an in-memory Tavily FastMCP server.

Examples:
    >>> callable(main)
    True
"""

from __future__ import annotations

import asyncio

from tavily_fastmcp.server import create_server


async def main() -> None:
    """Create an in-memory server and print its components."""
    from fastmcp import Client

    client = Client(create_server())
    async with client:
        tools = await client.list_tools()
        prompts = await client.list_prompts()
        resources = await client.list_resources()
    print([tool.name for tool in tools])
    print([prompt.name for prompt in prompts])
    print([resource.uri for resource in resources])


if __name__ == "__main__":
    asyncio.run(main())
