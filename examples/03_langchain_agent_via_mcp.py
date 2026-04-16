"""LangChain agent example using the MCP server.

Examples:
    >>> callable(main)
    True
"""

from __future__ import annotations

import asyncio


async def main() -> None:
    """Connect to the MCP server and create a LangChain agent."""
    from langchain.agents import create_agent
    from langchain_mcp_adapters.client import MultiServerMCPClient

    client = MultiServerMCPClient(
        {
            "tavily": {
                "command": "python",
                "args": ["-m", "tavily_fastmcp.server", "--transport", "stdio"],
                "transport": "stdio",
            }
        }
    )
    tools = await client.get_tools()
    agent = create_agent(model="openai:gpt-5", tools=tools)
    result = await agent.ainvoke(
        {
            "messages": [
                {"role": "user", "content": "Find the best official FastMCP prompts docs."},
            ]
        }
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
