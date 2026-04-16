# Tavily Get Research: Full Semantic Guide

You are using `tavily.get_research`, the suite's research-result retrieval primitive.

This document explains the role of research retrieval, why it exists separately from research creation, and how to use it safely in asynchronous workflows.

## Core purpose

`get_research` retrieves the result of a previously created research task.

It is ideal for:

- polling for completion
- retrieving final report content
- fetching sources attached to a completed research task
- continuing a workflow that was split into create-then-retrieve phases

## What Get Research is not

It is not:

- a search tool
- a page-reading tool
- a site discovery tool
- a way to “just do research again”

It is specifically about **retrieving an existing research job** by request ID.

## The research lifecycle

The standard lifecycle is:

1. call `tavily.research`
2. receive a request identifier
3. call `tavily.get_research`
4. inspect the returned status, content, and sources
5. synthesize for the user

## Why the separation matters

Keeping creation and retrieval separate helps the system:

- model asynchronous behavior accurately
- avoid pretending results are ready when they are not
- poll or revisit prior research jobs cleanly

## Retrieval strategy

When retrieving a research job, pay attention to:

- status
- completion timestamps if available
- returned content shape
- source list completeness

If the result is incomplete or pending, say so.
Do not invent a completed report.

## Get Research anti-patterns

### Anti-pattern: calling without a valid request ID

This tool is only meaningful when a prior research task exists.

### Anti-pattern: pretending retrieval succeeded when status is unclear

Always respect the returned status.

### Anti-pattern: treating retrieval content as final user output automatically

Even a returned report usually needs user-facing synthesis.

## Get Research quality checklist

Before finalizing, ask:

- Am I retrieving a real prior research job?
- Did I inspect status before answering?
- Did I distinguish retrieved content from my own synthesis?
- Did I avoid pretending a pending job is complete?

## Retrieval status handling

Whenever you retrieve a research job, classify the state immediately:

- **completed**: the content can be synthesized
- **pending / in_progress**: retrieval succeeded but the report is not ready yet
- **failed**: the job did not complete successfully and you must not fabricate a result
- **unknown / partial**: the result shape is unclear and should be treated cautiously

This matters because retrieval success is not the same as content readiness.

## How retrieval should change your answer

### Completed result

When the report is complete:

- inspect the content shape
- inspect the attached sources
- determine whether the user needs a narrative answer, bullets, or structured fields
- synthesize rather than blindly dump the raw report

### Pending result

When the report is pending:

- explicitly say the job is not complete yet
- explain that you only have partial or status-only information
- do not convert “pending” into a pretend conclusion

### Failed result

When the report failed:

- state that the retrieval succeeded but the research task did not complete successfully
- avoid filling in the missing report from memory or guesswork

## Source-awareness after retrieval

A research job may return a polished body of content plus source metadata.
Treat both as useful:

- the content tells you the report-level synthesis
- the sources tell you the evidentiary footprint behind that synthesis

If the user asks how confident the answer is, the source list is part of that judgment.

## Get Research quality checklist

Before finalizing, ask:

- Am I retrieving a real prior research job?
- Did I inspect status before answering?
- Did I distinguish retrieved content from my own synthesis?
- Did I avoid pretending a pending job is complete?
- Did I preserve the difference between report retrieval and final user communication?
