# Tavily Research: Full Semantic Guide

You are using `tavily.research`, the suite's asynchronous deep-research primitive.

This document explains when research is worth using, how to frame strong research jobs, how it differs from search, and how to avoid wasting a heavy-weight tool on light-weight questions.

## Core purpose

`research` is for launching a **deeper, report-shaped investigation**.

It is ideal for:

- comparative reports
- research briefs
- multi-angle technical investigations
- vendor evaluations
- recommendation memos
- structured-output research jobs

## Research is about deliverable shape

The key criterion is not merely “this topic sounds important.”
The real criterion is: **does the user want a deliverable that feels like a thorough report?**

If yes, research is often the right tool.

## When Research is justified

Use `research` when the user asks for:

- a comprehensive report
- a deep comparison
- a market or technical brief
- a structured synthesis
- recommendation criteria across multiple dimensions
- reusable structured output such as JSON or table-ready fields

## When Research is not justified

Do not use `research` when:

- a quick answer would do
- the question is a narrow fact lookup
- the relevant pages are already known and few
- the main problem is finding or reading one or two pages

## Research vs Search

This distinction matters:

- `search` is discovery-first and generally lightweight.
- `research` is synthesis-first and generally heavyweight.

Use `search` when you need to **find** relevant sources.
Use `research` when you need to **produce a report-like output** across a topic.

## Research objective framing

A good research objective should specify:

- the exact question or decision
- the entities, products, tools, or vendors involved
- the comparison dimensions or criteria
- the desired output shape
- any constraints or exclusions

Weak objective:

- “research FastMCP”

Stronger objective:

- “Research FastMCP's approach to tools, prompts, and resources, focusing on typed schemas, client discoverability, and server ergonomics. Return a concise comparison-ready brief with strengths, limitations, and likely best-fit use cases.”

## Structured output strategy

Structured output is useful when the user needs:

- repeated comparisons
- machine-readable downstream use
- scoring dimensions
- table population
- reusable report objects

## Research anti-patterns

### Anti-pattern: vague objectives

Research jobs should not begin with underspecified goals.

### Anti-pattern: overuse

Do not reach for research every time a question is complex.
Sometimes `search` plus `extract` is enough.

### Anti-pattern: reprinting the report without synthesis

A good final answer interprets and organizes the result for the user.

### Anti-pattern: ignoring uncertainty

Research results can still be partial or mixed. Preserve that reality.

## Research quality checklist

Before launching, ask:

- Does this task truly deserve a report?
- Is the objective precise?
- Are the key criteria explicit?
- Would structured output help?
- Am I using research because of the deliverable shape rather than vague importance?
