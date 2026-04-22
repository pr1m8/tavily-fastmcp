SHELL := /bin/bash

DOCS_OUTPUT ?= docs/source/_build/html

.PHONY: install lint format type test test-unit test-integration test-e2e test-live docs build clean-dist publish-check publish

install:
	pdm install -G:all

lint:
	pdm run ruff check .

format:
	pdm run ruff format .

type:
	pdm run mypy src

test:
	pdm run pytest

test-unit:
	pdm run pytest tests/unit --no-cov

test-integration:
	pdm run pytest tests/integration --no-cov

test-e2e:
	pdm run pytest tests/e2e --no-cov

test-live:
	@if [ ! -f .env ]; then \
		echo "Create .env from .env.example and set TAVILY_API_KEY first."; \
		exit 1; \
	fi
	set -a; . ./.env; set +a; TAVILY_FASTMCP_ENABLE_LIVE_TESTS=true pdm run pytest tests/integration/test_live_tavily.py --no-cov

docs:
	LC_ALL=C LANG=C pdm run sphinx-build -b html docs/source $(DOCS_OUTPUT)

clean-dist:
	rm -rf dist build

build: clean-dist
	pdm build

publish-check: lint type test docs build

publish:
	@echo "Publishing is handled by the GitHub Release workflow with PyPI trusted publishing."
	@echo "Run 'make publish-check', tag the release, push the tag, then publish a GitHub Release."
