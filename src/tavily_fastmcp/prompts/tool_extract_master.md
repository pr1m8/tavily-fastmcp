# Tavily Extract: Full Semantic Guide

You are using `tavily.extract`, the suite's page-reading primitive.

This document explains how to use extraction correctly, how it differs from search, and how to synthesize answers from a known set of URLs without drifting or hallucinating.

## Core purpose

`extract` is for reading **specific known URLs**.

It is ideal for:

- summarizing supplied pages
- comparing known docs pages
- reading policy pages
- extracting clean content from official references
- grounding a final answer in the actual content of selected pages

## What Extract is not for

`extract` is not the best first move when:

- you do not yet know which pages matter
- the user is asking a broad web question
- the main problem is site navigation

Those are discovery problems, which generally belong to `search` or `map`.

## Canonical use cases

Use `extract` when the user says things like:

- “summarize these URLs”
- “compare these two policy pages”
- “read the authentication docs page and tell me the flow”
- “pull the refund terms from this page”
- “extract the setup steps from these release notes / docs pages”

## Why Extract matters

Search results are often enough to find the right pages, but not enough to safely quote or characterize them. Extraction converts that candidate set into readable content.

## URL-first discipline

When URLs are already known:

- do not start with `search`
- do not broaden the scope unless the user requests it
- stay anchored to the supplied pages first

## Reading strategy

For each extracted page, classify it as:

- primary / canonical
- supporting / secondary
- stale / historical
- irrelevant or low-value

Then weight the synthesis accordingly.

## Extract across multiple URLs

When multiple URLs are provided:

1. identify which pages are central vs supplementary
2. extract all supplied pages if the set is small and deliberate
3. compare claims, scope, dates, and version context
4. preserve disagreements if the pages conflict

## Extract and version awareness

When pages appear to reflect different versions, releases, or time periods:

- call that out directly
- do not collapse them into one invented “current” answer
- prefer the more authoritative or current page if the user wants the present state

## Extract anti-patterns

### Anti-pattern: broadening scope too early

If the user gave URLs, the first responsibility is to read those URLs well.

### Anti-pattern: treating every URL equally

An official docs page and a third-party blog post should not be weighted the same.

### Anti-pattern: silent conflict resolution

If two pages disagree, do not silently pick one without explanation.

### Anti-pattern: quoting unseen details

Only summarize what the extracted page content supports.

## Extract-to-answer pattern

A strong extract-driven answer usually does this:

- answers the user's question first
- cites or references the most authoritative extracted pages implicitly
- separates confirmed details from inference
- names uncertainty if the pages are incomplete

## When Extract should lead to something else

Sometimes extraction reveals a broader need:

- if the supplied page is only a hub page and more pages are needed, `map` or `crawl` may follow
- if the supplied URLs are insufficient and broader discovery is needed, `search` may follow
- if the user actually wants a large report rather than a page summary, `research` may be appropriate

## Extract quality checklist

Before finalizing, ask:

- Did I stay URL-first?
- Did I distinguish primary from secondary pages?
- Did I preserve version or policy differences?
- Did I avoid claiming more than the extracted pages support?
