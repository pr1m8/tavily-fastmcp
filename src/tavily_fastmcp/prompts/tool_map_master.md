# Tavily Map: Full Semantic Guide

You are using `tavily.map`, the suite's site-structure discovery primitive.

This document explains how to use mapping to find the right pages inside a website, how it differs from crawl, and how to turn mapped URLs into a focused reading plan.

## Core purpose

`map` is for **discovering URLs inside one site**.

It is ideal for:

- finding docs sections
- discovering help-center page structure
- locating likely pages before extraction
- building a shortlist of candidate URLs on one domain

## Map is about structure, not page reading

This is the central rule:

- `map` helps you understand what exists.
- `extract` helps you read what exists.

Do not answer detailed factual questions from URL paths or titles alone unless the task is only about site structure.

## Best-fit use cases

Use `map` when the user says:

- “find the auth docs on this site”
- “show me which pages exist about billing”
- “map this docs site”
- “find likely relevant pages in this help center”

## The Map -> Extract workflow

The standard pattern is:

1. map the site
2. shortlist likely pages
3. extract the strongest pages
4. answer from extracted content

This is often more efficient than crawling a whole site.

## URL-shortlisting heuristics

After mapping, prefer pages whose:

- paths clearly match the requested concept
- titles imply canonical docs or guides
- paths indicate API references, tutorials, or setup guides
- paths look current rather than archived

Deprioritize:

- vague marketing pages
- legal pages unless specifically requested
- blog pages unless they appear to be the only relevant source

## When Map is better than Search

Choose `map` over `search` when:

- the relevant site is already known
- the user's question is site-local rather than web-wide
- you want the site's own URL structure, not external search results

## When Map is better than Crawl

Choose `map` over `crawl` when:

- the main uncertainty is “which page matters?”
- only a few pages are likely needed
- you want a narrow shortlist before reading content

## When Map is not enough

Map alone is insufficient when:

- the user wants actual policy or product details
- the answer depends on content distributed across many pages
- URL discovery must be followed by reading

## Map anti-patterns

### Anti-pattern: answering from path names alone

Paths are hints, not evidence.

### Anti-pattern: extracting every mapped URL
n
Shortlist first. Read selectively.

### Anti-pattern: mapping when exact URLs already exist

If the user has already supplied the pages, use `extract` instead.

### Anti-pattern: crawling too soon

If two or three mapped pages likely answer the question, do not escalate to `crawl` prematurely.

## Map quality checklist

Before finalizing, ask:

- Did I use Map because the site was known but the page was not?
- Did I separate URL discovery from actual reading?
- Did I shortlist intelligently before extraction?
- Did I avoid unnecessary crawl escalation?
