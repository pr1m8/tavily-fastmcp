# Automation

Use `make` for the common local workflows and GitHub Actions for release
automation.

## Local commands

```bash
make install
make lint
make type
make test
make test-e2e
make docs
make build
make publish-check
```

`make test-live` runs the opt-in Tavily smoke test. It requires `.env` with
`TAVILY_API_KEY` and sets `TAVILY_FASTMCP_ENABLE_LIVE_TESTS=true` for that
command only.

## GitHub workflows

- `CI`: installs all groups, then runs Ruff, mypy, and pytest.
- `Docs`: builds Sphinx HTML and uploads the rendered site artifact.
- `Build`: builds source and wheel distributions, then checks package metadata.
- `Release`: publishes distributions to PyPI from GitHub Releases using trusted
  publishing.

Run `make publish-check` before tagging a release.
