# Tools

The MCP server exposes namespaced tools so clients can discover and route
Tavily work predictably.

| Tool | Use for |
| --- | --- |
| `tavily.health` | Local smoke checks and package/server metadata. |
| `tavily.catalog` | Discovering tools, prompts, resources, examples, and profiles. |
| `tavily.search` | Broad web discovery when relevant URLs are not known. |
| `tavily.extract` | Reading and summarizing specific known URLs. |
| `tavily.map` | Finding candidate pages inside one site or docs domain. |
| `tavily.crawl` | Multi-page traversal across a scoped site. |
| `tavily.research` | Creating longer Tavily research tasks. |
| `tavily.get_research` | Retrieving existing Tavily research task results. |

All tool handlers validate inputs through local Pydantic request models before
calling `langchain-tavily`, then normalize responses back into local typed
models.
