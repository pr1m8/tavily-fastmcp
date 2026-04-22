# LangChain

Use the package with `langchain-mcp-adapters` to load the server tools into a LangChain agent.

## Install

```bash
pdm add "tavily-fastmcp[langchain]"
```

For local development from this repository:

```bash
pdm install -G :all
```

## Agent over MCP

This pattern lets the model decide when to search, extract source pages, crawl a
site, or request a Tavily research report.

```python
import asyncio

from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient


async def main() -> None:
    client = MultiServerMCPClient(
        {
            "tavily": {
                "transport": "stdio",
                "command": "python",
                "args": ["-m", "tavily_fastmcp.server", "--transport", "stdio"],
                "env": {"TAVILY_API_KEY": "tvly-your-key-here"},
            }
        }
    )

    tools = await client.get_tools()
    agent = create_agent(
        model="openai:gpt-5",
        tools=tools,
        system_prompt=(
            "Use Tavily for current web research. Use tavily.search for broad "
            "discovery, tavily.extract for source reading, and tavily.research "
            "for synthesized reports."
        ),
    )

    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Find current MCP client setup guidance and cite the best sources.",
                }
            ]
        }
    )
    print(result)


asyncio.run(main())
```

## Direct Service Agent Tooling

For scripts that do not need MCP transport, call the typed service directly and
wrap only the operations your agent should use.

```python
from tavily_fastmcp.service import LangChainTavilyService
from tavily_fastmcp.settings import get_settings

service = LangChainTavilyService(get_settings())


def web_research(query: str) -> str:
    response = service.search_from_model(
        query=query,
        search_depth="advanced",
        max_results=5,
        include_answer=True,
    )
    urls = "\n".join(hit.url for hit in response.results)
    return f"{response.answer or 'No direct answer returned.'}\n\nSources:\n{urls}"
```
