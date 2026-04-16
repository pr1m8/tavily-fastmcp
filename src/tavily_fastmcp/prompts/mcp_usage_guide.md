# Tavily FastMCP Usage Guide

This document explains the server as an MCP surface rather than only as a set of Tavily tool semantics.

## What the server exposes

The server exposes:

- namespaced Tavily tools under `tavily.*`
- packaged markdown prompts
- structured prompt profiles
- static resources
- dynamic resource templates addressed by URI

## Why this matters for MCP clients

Different MCP clients may want different surfaces:

- some primarily discover tools
- some also inspect prompts
- some read resources for configuration, guidance, or examples

This server is designed to support all three.

## Namespacing policy

Tool names should remain namespaced as `tavily.search`, `tavily.extract`, and so on.

This makes them:

- easier to discover in clients
- less likely to collide with unrelated tools
- easier to route to in prompt policies

## Prompt usage strategy

Use packaged prompts when you want a client or agent to adopt one of the suite's standard operating profiles.

Examples:

- use the router prompt as the default system prompt
- use the site-discovery prompt when the task is docs-navigation heavy
- use the deep-research prompt for long-form reports

## Resource usage strategy

Use resources when the client benefits from read-only documentation or machine-readable metadata.

Examples:

- server catalog
- profile catalog
- prompt markdown retrieval
- example client configs

## Template usage strategy

Dynamic resource templates are appropriate for:

- profile-by-slug retrieval
- prompt-by-name retrieval
- future additions such as examples, policies, or schemas keyed by identifier

## Recommended client behavior

A well-behaved MCP client should:

- inspect the tool catalog
- keep namespaced tool names intact
- optionally read the profile catalog
- load a prompt profile appropriate to the task
- avoid flattening all tools into one vague “web research” capability

## Overall intent

This server is not just a binding to Tavily.
It is a structured MCP product around Tavily, designed to make the tool family easier to discover, safer to route, and more reusable across clients.
