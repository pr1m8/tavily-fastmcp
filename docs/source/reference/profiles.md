# Profiles

Profiles pair prompt markdown with routing metadata. They are available as MCP
resources and can be used directly by clients that want reusable workflow
guidance.

| Profile | Best fit |
| --- | --- |
| `router` | General routing across Tavily capabilities. |
| `suite-overview` | Full semantic overview of the tool family. |
| `quick-search` | Fast web discovery plus minimal extraction. |
| `tool-search` | Deep guide for `tavily.search`. |
| `extract-and-summarize` | URL-first extraction and synthesis. |
| `tool-extract` | Deep guide for `tavily.extract`. |
| `site-discovery` | Map-first discovery inside one site. |
| `tool-map` | Deep guide for `tavily.map`. |
| `site-crawl` | Scoped multi-page site traversal. |
| `tool-crawl` | Deep guide for `tavily.crawl`. |
| `deep-research` | Report-shaped research workflows. |
| `tool-research` | Deep guide for `tavily.research`. |
| `tool-get-research` | Deep guide for retrieving research tasks. |
| `routing-matrix` | Compact decision policy for tool selection. |
| `synthesis-policy` | Answer-shaping and grounding policy. |
| `mcp-usage-guide` | Client-facing MCP usage guidance. |

Important resource URI patterns:

```text
resource://tavily-fastmcp/catalog/profiles
resource://tavily-fastmcp/profile/{slug}
resource://tavily-fastmcp/prompt/{name}
```
