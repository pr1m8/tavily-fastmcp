# Configuration

`tavily-fastmcp` reads Tavily credentials from `TAVILY_API_KEY` and package
settings from the `TAVILY_FASTMCP_` prefix.

## Environment variables

- `TAVILY_API_KEY`: required for live Tavily calls.
- `TAVILY_FASTMCP_TRANSPORT`: `stdio`, `http`, or `sse`; defaults to `stdio`.
- `TAVILY_FASTMCP_HOST`: host for HTTP transports; defaults to `127.0.0.1`.
- `TAVILY_FASTMCP_PORT`: port for HTTP transports; defaults to `8001`.
- `TAVILY_FASTMCP_LOG_LEVEL`: `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`.
- `TAVILY_FASTMCP_DEFAULT_SEARCH_TOPIC`: `general`, `news`, or `finance`.
- `TAVILY_FASTMCP_DEFAULT_SEARCH_DEPTH`: `basic` or `advanced`.
- `TAVILY_FASTMCP_ENABLE_LIVE_TESTS`: set to `true` to run live tests.

## Local secrets

Copy the template and put real credentials only in `.env`:

```bash
cp .env.example .env
```

`.env` is ignored by Git. Keep `.env.example` as placeholders only.
