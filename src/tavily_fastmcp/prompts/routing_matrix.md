# Tavily Routing Matrix

Use this document when you need a stricter decision matrix rather than a narrative profile.

## One-line rule for each tool

- `tavily.search`: find candidate sources across the web
- `tavily.extract`: read known URLs
- `tavily.map`: discover likely pages inside one site
- `tavily.crawl`: read many pages inside one site
- `tavily.research`: create a deeper report-oriented research job
- `tavily.get_research`: retrieve that research job later

## Best first tool by user situation

### The user already pasted links

First tool: `tavily.extract`

### The user says “find the docs page on this site”

First tool: `tavily.map`

### The user says “analyze this docs site / knowledge base”

First tool: `tavily.crawl`

### The user says “what is the latest on X”

First tool: `tavily.search`

### The user says “research this deeply”

First tool: `tavily.research`

## Common transitions

- search -> extract
- map -> extract
- crawl -> extract (only if one page needs close reading)
- research -> get_research

## Escalation rules

Escalate from `search` to `research` only when the deliverable shifts from a quick answer to a real report.

Escalate from `map` to `crawl` only when many pages actually need to be read.

Escalate from `extract` to `search` only when the provided URLs are insufficient and broader discovery is required.

## Hard boundaries

- Never use `search` when the user already gave exact URLs as the primary task input.
- Never use `crawl` as a lazy substitute for thinking about scope.
- Never use `map` output as page-content evidence.
- Never use `research` for trivial lookups.
- Never skip `get_research` if the workflow depends on retrieving a research task result.
