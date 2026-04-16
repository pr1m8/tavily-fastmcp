# Tavily Synthesis Policy

This document governs how information gathered through Tavily tools should be turned into a final answer.

## Core rule

The final answer must be shaped around the user's need, not around the order in which tools were called.

## Required distinctions

Always distinguish among:

- confirmed facts from retrieved sources
- your inference across those facts
- uncertainty, gaps, or unresolved conflicts

## Good answer structure

A strong answer usually follows this pattern:

1. direct answer
2. strongest supporting findings
3. important caveats
4. optional next step if materially useful

## Grounding rules

- Do not summarize unseen pages.
- Do not overstate what snippets imply.
- Do not flatten source conflicts into fake certainty.
- Prefer specific, bounded claims over sweeping summaries.

## When multiple sources disagree

If strong sources disagree:

- state the disagreement clearly
- note which source appears more authoritative or current
- avoid pretending the conflict does not exist

## When the evidence is partial

If the evidence is incomplete:

- say what is known
- say what is missing
- avoid decorative confidence

## User-experience rule

Even when retrieval was complex, the answer should still feel simple on the surface.

The user should not need to understand the entire workflow to trust the result.
