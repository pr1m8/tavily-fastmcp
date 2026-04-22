# Claude Code

Claude Code can run `tavily-fastmcp` as a local stdio MCP server. Keep
`TAVILY_API_KEY` outside Git and pass it at runtime.

## Add the Server

```bash
export TAVILY_API_KEY="tvly-your-key-here"
claude mcp add tavily-fastmcp --scope project \
  --env TAVILY_API_KEY="$TAVILY_API_KEY" \
  -- python -m tavily_fastmcp.server --transport stdio
```

Verify the server:

```bash
claude mcp list
claude mcp get tavily-fastmcp
```

## Shared Project Config

For teams, commit `.mcp.json` and rely on environment variable expansion for
the real key:

```json
{
  "mcpServers": {
    "tavily-fastmcp": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "tavily_fastmcp.server", "--transport", "stdio"],
      "env": {
        "TAVILY_API_KEY": "${TAVILY_API_KEY}"
      }
    }
  }
}
```

Claude Code prompts before using project-scoped MCP servers from `.mcp.json`.
After connecting, ask for current-source research such as:

```text
Use tavily-fastmcp to research the current FastMCP resource-template guidance.
Compare the top sources and return links with a short recommendation.
```
