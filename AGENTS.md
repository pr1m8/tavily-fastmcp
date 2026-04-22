# Repository Guidelines

## Project Structure & Module Organization

This is a Python 3.13+ package using a `src/` layout. Runtime code lives in
`src/tavily_fastmcp/`: server creation and CLI entry points are in `server.py`,
typed settings/models are in `settings.py` and `models.py`, service logic is in
`service.py`, and MCP tool registration is split under `tools/`. Packaged prompt
markdown files live in `src/tavily_fastmcp/prompts/`. Tests are organized by
scope in `tests/unit/`, `tests/integration/`, and `tests/e2e/`. Usage samples are
in `examples/`, and Sphinx documentation is in `docs/source/`.

## Build, Test, and Development Commands

- `pdm install -G :all`: install runtime and development dependencies.
- `pdm run pytest`: run the full test suite with coverage reporting.
- `pdm run pytest tests/unit`: run only unit tests while iterating.
- `pdm run ruff check .`: lint imports, style, docstrings, and common bugs.
- `pdm run mypy src`: run strict type checking for the package.
- `pdm build`: build distributable package artifacts.
- `pdm run sphinx-build -b html docs/source docs/source/_build/html`: build docs.
- `pdm run tavily-fastmcp` or `python -m tavily_fastmcp.server --transport stdio`:
  run the MCP server locally.

## Coding Style & Naming Conventions

Use 4-space indentation, type annotations, and explicit Pydantic models for
structured data. Ruff targets Python 3.13 with a 100-character line length and
Google-style docstrings. Keep module names lowercase with underscores, test files
named `test_*.py`, and MCP tool modules grouped by capability, such as
`tools/search.py` or `tools/crawl.py`. Preserve the typed package marker
`py.typed` when changing package metadata.

## Testing Guidelines

Pytest is configured in `pyproject.toml` with `pytest-asyncio`, coverage for
`src/tavily_fastmcp`, and an 85% minimum coverage threshold. Mark tests with
`unit`, `integration`, `e2e`, or `live` as appropriate. Live Tavily tests require
`TAVILY_API_KEY`; do not make them mandatory for routine local validation.

## Agent Integration Notes

Use the stdio MCP server for LangChain, LangGraph, Claude Code, Cursor, and
similar clients:

```bash
python -m tavily_fastmcp.server --transport stdio
```

For LangChain agents, install `pdm add "tavily-fastmcp[langchain]"`, load tools
with `MultiServerMCPClient`, then pass `await client.get_tools()` to
`langchain.agents.create_agent`. For custom LangGraph flows, also install
`langgraph` and pass the same MCP-loaded tools into `ToolNode` or bind them to a
chat model. Keep `TAVILY_API_KEY` in the environment or MCP client config; never
hard-code it in examples, tests, or checked-in agent configs.

Route agent tasks by intent: `tavily.search` for discovery, `tavily.extract` for
known URLs, `tavily.map` for site structure, `tavily.crawl` for multi-page site
inspection, and `tavily.research` for synthesized reports. Use
`tavily.catalog` plus resources such as
`resource://tavily-fastmcp/catalog/profiles` when an agent needs to inspect the
available profiles before choosing a workflow.

## Commit & Pull Request Guidelines

Recent history uses Conventional Commit-style subjects, for example
`feat(tools): Introduce modular tool registration` and `chore(tests): Add initial
test suite initialization file`. Keep commits focused and use a clear scope when
helpful. Pull requests should include a short behavior summary, linked issues
when available, test commands run, and notes for any docs, prompt, or live API
changes.

## Security & Configuration Tips

Never commit API keys or local `.env` files. Tavily authentication uses
`TAVILY_API_KEY`; package-specific settings use the `TAVILY_FASTMCP_` prefix.
When adding examples or docs, prefer placeholder keys such as `tvly-your-key-here`.
