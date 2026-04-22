# LangChain

Use the package with `langchain-mcp-adapters` to load the server tools into a LangChain agent.

## Install

```bash
pdm add "tavily-fastmcp[langchain]"
```

For LangGraph workflows:

```bash
pdm add "tavily-fastmcp[langchain]" langgraph
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

## LangGraph Tool Node

Use LangGraph when you want explicit state transitions around Tavily tools. This
pattern loads the MCP tools once and routes model tool calls through `ToolNode`.

```python
import asyncio

from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition


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
    model = ChatOpenAI(model="gpt-5").bind_tools(tools)

    async def call_model(state: MessagesState) -> dict:
        response = await model.ainvoke(state["messages"])
        return {"messages": [response]}

    graph_builder = StateGraph(MessagesState)
    graph_builder.add_node("agent", call_model)
    graph_builder.add_node("tools", ToolNode(tools))
    graph_builder.add_edge(START, "agent")
    graph_builder.add_conditional_edges("agent", tools_condition)
    graph_builder.add_edge("tools", "agent")
    graph = graph_builder.compile()

    result = await graph.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Map the FastMCP docs site and identify the pages about prompts.",
                }
            ]
        }
    )
    print(result["messages"][-1].content)


asyncio.run(main())
```

## Tool Routing

- Use `tavily.search` for broad discovery and current facts.
- Use `tavily.extract` when the agent already has URLs and needs page text.
- Use `tavily.map` before extraction when the agent needs a site's URL structure.
- Use `tavily.crawl` for multi-page inspection on one domain.
- Use `tavily.research` for synthesized reports across multiple sources.
