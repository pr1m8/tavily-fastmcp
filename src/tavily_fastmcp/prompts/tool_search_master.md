# Tavily Search: Full Semantic Guide

You are using `tavily.search`, the suite's broad web-discovery primitive.

This document explains what `tavily.search` is for, what it is not for, how it should be sequenced with other tools, and how to get high-value results with minimal waste.

## Core purpose

`search` is the suite's web-wide discovery tool. It helps you find candidate sources when the relevant pages are not already known.

It is ideal for:

- current information
- cross-site discovery
- finding official documentation
- finding release notes or announcements
- finding vendor help pages
- discovering candidate URLs for later extraction

## The kind of question Search answers best

Use `search` when the question starts as:

- “What is the latest…?”
- “Find the docs for…”
- “What changed in…?”
- “Which official page explains…?”
- “Compare these vendors / packages / tools…”
- “What sources should I read for…?”

The search tool is optimized for **finding** the right sources, not necessarily for fully reading them.

## What Search returns conceptually

A search call typically gives you a ranked candidate set of sources, potentially with:

- result URLs
- titles
- snippets or short content
- answer fields
- image lists
- metadata such as response time or usage

That means `search` is usually a **candidate generator**.

## Search is not Extract

This distinction matters:

- `search` tells you which pages are probably relevant.
- `extract` tells you what those pages actually say.

Do not over-read search snippets as if they were the underlying pages.

## When Search should be the first tool

Choose `search` first when:

- the relevant URLs are unknown
- the user wants up-to-date facts
- the question spans multiple sites or sources
- you need to find official docs or releases
- the task is still in a broad discovery phase

## When Search should not be the first tool

Do **not** start with `search` when:

- the user already gave exact URLs -> use `extract`
- the question is about one site's structure -> use `map`
- the task is clearly a single-site multi-page investigation -> use `crawl`
- the user explicitly wants a research report -> use `research`

## Query construction strategy

### 1. Prefer entity-rich queries

A good query usually includes:

- the exact package, product, company, standard, or feature name
- a disambiguator if the term is overloaded
- the action, policy, or question of interest

Examples:

- `FastMCP resource templates auth docs`
- `langchain tavily research tool official docs`
- `OpenAI structured outputs announcement`

### 2. Use official-source bias when appropriate

If the user wants product behavior, policy, or SDK details, bias toward official domains.

### 3. Use time filters when freshness matters

If the question is about the latest changes, current state, or recent announcements, time constraints and freshness-sensitive settings matter.

### 4. Use domain filters sparingly

Only narrow to included or excluded domains when you have a clear reason.

## Search result interpretation strategy

After searching, classify the result set:

- **strong**: official sources found quickly and align with the question
- **mixed**: relevant but partly secondary or ambiguous
- **weak**: low-quality, tangential, or conflicting

A strong result set often means you should `extract` the top 1–3 pages.
A weak result set may mean you should refine the query.

## Search-to-Extract handoff

The most common workflow is:

1. search
2. identify the best few URLs
3. extract those URLs
4. answer

This handoff is the default pattern for most web research that is not site-local.

## Search anti-patterns

### Anti-pattern: query spam

Do not issue many nearly identical queries with no new hypothesis.

### Anti-pattern: trusting titles too much

A promising title is not the same as a confirmed answer.

### Anti-pattern: over-extracting

Do not extract ten pages when two high-confidence pages will do.

### Anti-pattern: treating Search as a research job

Search is quick discovery, not deep synthesis.

## Search answer policy

If you can answer from high-confidence search + a small amount of extraction, do so.

If the result set is mixed:

- be explicit about source quality
- extract primary sources
- avoid overstating certainty

## Search escalation policy

Escalate beyond Search when:

- exact URLs are now known -> `extract`
- the answer is spread across one site -> `crawl`
- the task is site-page discovery -> `map`
- the task deserves a full report -> `research`

## Search quality checklist

Before finalizing, ask:

- Did I search with the right entities?
- Did I bias toward primary sources when needed?
- Did I extract the best pages instead of over-reading snippets?
- Did I stop once the answer was grounded?
