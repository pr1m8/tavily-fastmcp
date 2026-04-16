# tavily-fastmcp

[![CI](https://github.com/YOUR_GITHUB_USER/tavily-fastmcp/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_GITHUB_USER/tavily-fastmcp/actions/workflows/ci.yml)
[![Docs](https://readthedocs.org/projects/tavily-fastmcp/badge/?version=latest)](https://tavily-fastmcp.readthedocs.io/en/latest/)
[![PyPI](https://img.shields.io/pypi/v/tavily-fastmcp.svg)](https://pypi.org/project/tavily-fastmcp/)
[![Python](https://img.shields.io/pypi/pyversions/tavily-fastmcp.svg)](https://pypi.org/project/tavily-fastmcp/)
[![License](https://img.shields.io/pypi/l/tavily-fastmcp.svg)](LICENSE)
[![Typing](https://img.shields.io/badge/typing-typed-brightgreen.svg)](https://peps.python.org/pep-0561/)

Typed, ergonomic FastMCP server for Tavily search, extract, map, crawl, and research workflows.

It ships with:

- namespaced MCP tools like `tavily.search` and `tavily.research`
- packaged prompt profiles and large markdown system prompts
- static resources and dynamic resource templates for profiles, prompts, examples, and server catalogs
- a small direct Python API for local use without MCP
- docs, examples, CI, publishing workflow, coverage, Ruff, and mypy

## Why this package

`langchain-tavily` already gives you the raw Tavily tools. `tavily-fastmcp` adds a cleaner MCP boundary around them:

- richer metadata for MCP clients
- reusable profiles for common workflows
- discoverable prompt and resource surfaces
- stable typed request/response models you can test directly
- easier LangChain + MCP composition

Tavily's official LangChain package provides the raw Tavily tools, and this package wraps them in a typed FastMCP server surface with prompts, resources, profiles, and example client configuration.

## Installation

```bash
pdm add tavily-fastmcp
```

For LangChain helpers:

```bash
pdm add tavily-fastmcp[langchain]
```

For docs and development:

```bash
pdm install -G:all
```

## Environment

Tavily uses the `TAVILY_API_KEY` environment variable. This package preserves that variable directly and layers package-specific settings under the `TAVILY_FASTMCP_` prefix.

```bash
cp .env.example .env
```

## Quick start

### Run the MCP server

```bash
tavily-fastmcp
```

Or:

```bash
python -m tavily_fastmcp.server --transport stdio
```

### Direct Python usage

```python
from tavily_fastmcp.service import LangChainTavilyService
from tavily_fastmcp.settings import get_settings

service = LangChainTavilyService(get_settings())
response = service.search_from_model(query="latest FastMCP prompts docs")
print(response.results[0].url)
```

### Create a FastMCP server in code

```python
from tavily_fastmcp.server import create_server

server = create_server()
```

### Use through LangChain over MCP

```python
import asyncio

from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient


async def main() -> None:
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
                {
                    "role": "user",
                    "content": "Research the best docs pages for FastMCP resource templates.",
                }
            ]
        }
    )
    print(result)


asyncio.run(main())
```

## Included profiles and prompts

The package ships with large markdown prompts and reusable profiles for:

- `router`
- `suite-overview`
- `quick-search`
- `tool-search`
- `extract-and-summarize`
- `tool-extract`
- `site-discovery`
- `tool-map`
- `site-crawl`
- `tool-crawl`
- `deep-research`
- `tool-research`
- `tool-get-research`
- `routing-matrix`
- `synthesis-policy`
- `mcp-usage-guide`

They are exposed both as packaged markdown files and as MCP resources / prompts. The richer catalog now also includes a composite suite overview, per-tool deep guides, a routing matrix, a synthesis policy, and an MCP usage guide.

Example URIs:

- `resource://tavily-fastmcp/catalog/server`
- `resource://tavily-fastmcp/catalog/profiles`
- `resource://tavily-fastmcp/profile/deep-research`
- `resource://tavily-fastmcp/prompt/router`
- `resource://tavily-fastmcp/prompt/deep-research`
- `resource://tavily-fastmcp/example/claude-desktop-config`

The server is organized so MCP clients can discover tools, prompts, resources, examples, and workflow profiles through namespaced metadata and resource URIs.

## Tools exposed

- `tavily.health`
- `tavily.catalog`
- `tavily.search`
- `tavily.extract`
- `tavily.map`
- `tavily.crawl`
- `tavily.research`
- `tavily.get_research`

All tools use typed arguments, tags, annotations, titles, and custom metadata.

## MCP client examples

### Claude Desktop config snippet

```json
{
  "mcpServers": {
    "tavily-fastmcp": {
      "command": "python",
      "args": ["-m", "tavily_fastmcp.server", "--transport", "stdio"],
      "env": {
        "TAVILY_API_KEY": "tvly-your-key-here"
      }
    }
  }
}
```

### Cursor / Codex style stdio config

```json
{
  "name": "tavily-fastmcp",
  "command": "python",
  "args": ["-m", "tavily_fastmcp.server", "--transport", "stdio"],
  "env": {
    "TAVILY_API_KEY": "tvly-your-key-here"
  }
}
```

## Development

```bash
pdm install -G:all
pdm run ruff check .
pdm run mypy src
pdm run pytest
```

## Documentation

```bash
pdm run sphinx-build -b html docs/source docs/source/_build/html
```

## Project status

This scaffold is designed to be publishable and easy to extend, but you should still replace placeholder GitHub and Read the Docs URLs before release.


## Automation

This project now includes GitHub automation for the full package lifecycle:

- `CI` runs linting, typing, and tests on pushes and pull requests.
- `Docs` builds the Sphinx site and uploads the rendered HTML as an artifact.
- `Build` creates source and wheel distributions and validates them with `twine check`.
- `Release` rebuilds the distributions on GitHub Releases and publishes them to PyPI using trusted publishing.
- `.readthedocs.yaml` configures Read the Docs to build the Sphinx documentation with Python 3.13.
