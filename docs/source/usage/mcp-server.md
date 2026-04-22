# MCP Server

```bash
tavily-fastmcp
```

Equivalent module invocation:

```bash
python -m tavily_fastmcp.server --transport stdio
```

For local clients, pass credentials through the client environment rather than
hard-coding them into repository files:

```json
{
  "mcpServers": {
    "tavily-fastmcp": {
      "command": "python",
      "args": ["-m", "tavily_fastmcp.server", "--transport", "stdio"],
      "env": {
        "TAVILY_API_KEY": "${TAVILY_API_KEY}"
      }
    }
  }
}
```

The server exposes:

- `tavily.health`
- `tavily.catalog`
- `tavily.search`
- `tavily.extract`
- `tavily.map`
- `tavily.crawl`
- `tavily.research`
- `tavily.get_research`
