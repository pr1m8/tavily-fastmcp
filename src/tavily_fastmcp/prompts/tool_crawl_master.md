# Tavily Crawl: Full Semantic Guide

You are using `tavily.crawl`, the suite's multi-page site-reading primitive.

This document explains when crawl is justified, how to scope it, how it differs from map, and how to synthesize coherent answers from many pages on one domain.

## Core purpose

`crawl` is for collecting **content** from many pages in one site.

It is ideal for:

- documentation-site overviews
- knowledge-base digestion
- multi-page onboarding synthesis
- explaining how several docs sections fit together
- gathering content across one domain when one page is not enough

## Crawl vs Map

This is the key difference:

- `map` finds URLs.
- `crawl` reads page content.

Use `map` when the main problem is page discovery.
Use `crawl` when the main problem is multi-page content collection.

## Strong use cases

Choose `crawl` when the user asks for:

- a docs-site overview
- a help-center synthesis
- a multi-page summary of auth, webhooks, limits, setup, and examples
- the key setup information from a whole docs section

## Scoping policy

Crawl should be **narrow by default**.

Good scope:

- one product docs root
- one help-center section
- one subdomain or docs area

Bad scope:

- the entire company site with no narrowing
- marketing + legal + docs + blog all at once, unless the user explicitly wants that breadth

## Crawl output strategy

After crawling, synthesize across pages by identifying:

- repeated themes
- canonical setup patterns
- where guidance is spread across multiple documents
- what is central vs incidental
- important exceptions or caveats

## Crawl is not for everything

Do not use `crawl` when:

- the user gave exact URLs -> `extract`
- the main task is to locate the right pages -> `map`
- the question is cross-site -> `search`
- the user wants a broader research memo -> `research`

## Extract after Crawl

It can still be useful to `extract` one or two pages after a crawl when:

- one page deserves closer reading
- one specific claim needs confirmation
- a crawl summary is insufficiently precise for a key detail

## Crawl anti-patterns

### Anti-pattern: crawling because it feels thorough

Thoroughness without scope is waste.

### Anti-pattern: site sprawl

Do not drift into irrelevant marketing or navigation pages unless they matter to the user.

### Anti-pattern: flattening page differences

A setup guide, an API reference, and a policy page may all say different kinds of things. Preserve those distinctions.

### Anti-pattern: crawling when a map-plus-extract plan would be cleaner

If the site-local problem is still mostly navigational, start with `map`.

## Crawl quality checklist

Before finalizing, ask:

- Did I use Crawl because many pages really mattered?
- Did I keep the scope narrow?
- Did I distinguish repeated themes from page-specific details?
- Did I avoid turning crawl into uncontrolled site sprawl?
