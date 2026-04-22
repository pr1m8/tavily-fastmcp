# Development

Install all dependency groups before running checks:

```bash
pdm install -G:all
```

The Makefile wraps the standard validation path:

```bash
make lint
make type
make test
make docs
```

The equivalent PDM commands are:

```bash
pdm run ruff check .
pdm run mypy src
pdm run pytest
pdm run sphinx-build -b html docs/source docs/source/_build/html
```

Live Tavily tests are opt-in:

```bash
cp .env.example .env
# set TAVILY_API_KEY in .env
make test-live
```
