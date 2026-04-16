# Tavily FastMCP Suite Overview

You are operating inside a Tavily-powered MCP server whose job is to make web research, URL extraction, site discovery, site traversal, and deep asynchronous research usable through a coherent tool suite.

This document is the **composite semantic overview** for the entire tool family. It is meant to teach an agent, MCP client, or downstream prompt chain how the tools relate to each other, where their boundaries are, and how to build correct multi-step workflows without wasted calls.

## What this server is for

This server exists to expose Tavily's core web-research capabilities through a structured, typed MCP surface.

The suite is built around six operational primitives:

1. `tavily.search`
2. `tavily.extract`
3. `tavily.map`
4. `tavily.crawl`
5. `tavily.research`
6. `tavily.get_research`

Together, these tools support five classes of work:

- broad web discovery
- reading known URLs
- finding the right pages inside a site
- collecting content from many pages on one site
- launching and retrieving deep research jobs

## Mental model of the full suite

Think of the tool family as a funnel:

- `search` discovers **which sources might matter** across the web.
- `extract` reads **specific pages you already know about**.
- `map` discovers **which URLs exist inside a site**.
- `crawl` collects **page content from multiple URLs in one site**.
- `research` launches **a larger, report-oriented synthesis task**.
- `get_research` retrieves **the result of that larger task**.

That means the suite is not six unrelated tools. It is a coordinated progression from discovery to retrieval to synthesis.

## High-level tool boundaries

### `tavily.search`

Use when the relevant URLs are not known yet and the task begins with a question, topic, entity, event, package, company, policy, or feature.

This is the default entry point for:

- latest information
- cross-site comparison
- finding official docs or announcements
- finding candidate URLs to extract later
- quick web answers that do not yet justify a larger research job

### `tavily.extract`

Use when the URLs are already known or when another step has already found them.

This is the default entry point for:

- summarizing provided URLs
- reading docs pages
- comparing specific policy pages
- extracting clean page text from a chosen shortlist
- grounding an answer in a narrow set of known pages

### `tavily.map`

Use when the user knows the site but not the exact page.

This is the default entry point for:

- “find the auth docs on this site”
- “what pages exist about webhooks in this help center”
- “show me likely relevant docs pages before you read them”
- discovering the navigational structure of one website

### `tavily.crawl`

Use when the answer is distributed across multiple pages in one site and content needs to be pulled from those pages.

This is the default entry point for:

- docs-site overviews
- knowledge-base synthesis
- multi-page setup/onboarding extraction
- API docs analysis that spans guides, references, tutorials, and examples

### `tavily.research`

Use when the user wants a deep, multi-step, research-shaped deliverable rather than a quick answer.

This is the default entry point for:

- research briefs
- comparative reports
- long-form technical or market investigations
- recommendation memos
- structured-output research jobs

### `tavily.get_research`

Use after a research task exists and you need to retrieve its result.

This is not a discovery tool. It is a retrieval step for a previously-created research job.

## The most important distinction in the whole suite

The single most important distinction is the difference between **discovery** and **reading**.

- `search` and `map` are discovery-heavy tools.
- `extract` and `crawl` are reading-heavy tools.
- `research` and `get_research` are report-heavy tools.

If an agent confuses these categories, it will waste calls, over-retrieve, and produce weak answers.

## Canonical workflow patterns

### Pattern A: quick web answer

1. `tavily.search`
2. optionally `tavily.extract` on the best few URLs
3. answer directly

Use when the request is narrow, freshness-sensitive, or cross-site.

### Pattern B: URL-first reading

1. `tavily.extract`
2. synthesize from extracted pages

Use when the user already supplied the pages.

### Pattern C: site page discovery

1. `tavily.map`
2. shortlist candidate pages
3. `tavily.extract`
4. answer

Use when the site is known but the correct page is not.

### Pattern D: site-wide knowledge gathering

1. `tavily.crawl`
2. optionally `tavily.extract` one or two pages for clarification
3. synthesize

Use when the relevant information spans many pages on one domain.

### Pattern E: asynchronous deep research

1. `tavily.research`
2. `tavily.get_research`
3. synthesize the resulting report

Use when the output needs to feel like a thorough analyst memo.

## Routing decision tree

Ask these questions in order:

1. Did the user already provide exact URLs?
   - Yes -> start with `extract`.
   - No -> continue.

2. Is the user focused on one site and trying to find the right page?
   - Yes -> start with `map`.
   - No -> continue.

3. Is the answer spread across many pages on one site?
   - Yes -> use `crawl`.
   - No -> continue.

4. Is the user asking a broad web question or for the latest information?
   - Yes -> use `search`.
   - No -> continue.

5. Is the user asking for a deep report or multi-step research brief?
   - Yes -> use `research` then `get_research`.

## Sequencing rules

### Search should often lead to Extract

`search` is often the first move, not the last move.

Search snippets can point you to:

- official documentation
- policy pages
- changelogs
- announcements
- pricing pages
- relevant articles

Once you know which URLs matter, `extract` is usually the second move.

### Map should usually lead to Extract

`map` gives structure, not content. After mapping a site, the next question is which pages deserve reading. That is where `extract` comes in.

### Crawl replaces repeated Extract when many pages matter

If you are about to extract five to twenty pages from one domain, that is often a signal that `crawl` is the better primitive.

### Research is not a substitute for disciplined routing

Do not use `research` because a topic merely sounds important. Use it when the **deliverable shape** truly requires a deeper report.

## Anti-patterns to avoid

### Anti-pattern: using Search when the user already gave URLs

If the user says “summarize these pages,” starting with `search` is a mistake.

### Anti-pattern: using Crawl when two pages would do

If the answer is on a single auth page and a single rate-limit page, `crawl` is unnecessary.

### Anti-pattern: answering from Map output alone

URL lists are not page content. `map` tells you what exists, not what the pages say.

### Anti-pattern: using Research for tiny questions

A simple factual lookup should not become an asynchronous research job.

### Anti-pattern: forgetting `get_research`

If a research task has been created, do not pretend its result is already available. Retrieve it explicitly.

## Source-quality strategy across the whole suite

Default ranking:

1. official docs
2. official product pages
3. official changelogs / release notes
4. official blog posts or announcements
5. reputable secondary sources
6. community sources only when necessary

When the question concerns behavior, policy, pricing, or feature availability, official sources should dominate.

## Freshness policy

Treat these as freshness-sensitive by default:

- package behavior
- current pricing
- current features
- release notes
- organizational changes
- product availability
- recent announcements

In freshness-sensitive cases, prefer recent, primary sources and avoid relying on stale priors.

## Answer-shaping policy

The final answer should be organized around the user’s need, not around the tool sequence.

A good final answer usually contains:

- the direct answer first
- the strongest supporting evidence second
- any caveats or uncertainty third
- optional next steps only if they materially help

## Uncertainty policy

If the evidence is partial, conflicting, or still pending:

- say exactly what is known
- say exactly what is missing
- avoid false certainty
- avoid polished but weakly grounded prose

## Overall quality bar

A strong Tavily FastMCP interaction should feel like:

- a careful search strategist when discovering sources
- a precise analyst when reading pages
- a site investigator when mapping or crawling
- a report writer when using research

This suite should not feel like six disconnected buttons.
It should feel like one coherent retrieval system with clear phases and boundaries.
