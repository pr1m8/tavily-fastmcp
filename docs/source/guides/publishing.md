# Publishing

Publishing is designed to happen through GitHub Releases and PyPI trusted
publishing, not from a developer laptop.

## Release checklist

1. Confirm repository URLs in `pyproject.toml`, `README.md`, and badge links.
2. Confirm the PyPI project exists and trusted publishing is configured for
   repository `pr1m8/tavily-fastmcp` and workflow file `release.yml`. Leave the
   PyPI environment field blank unless the workflow defines a GitHub
   environment.
3. If trusted publishing is not available yet, create a project-scoped PyPI API
   token and save it as the GitHub repository secret `PYPI_API_TOKEN`. The
   release workflow uses this token first when present, then falls back to
   trusted publishing.
4. Run the local publish gate:

   ```bash
   make publish-check
   ```

5. Update the package version in `pyproject.toml` and `src/tavily_fastmcp/server.py`.
6. Commit the release changes and create a tag such as `v0.3.1`.
7. Push the branch and tag.
8. Publish a GitHub Release for the tag. The `Release` workflow builds and
   uploads distributions to PyPI.

## Manual build

To inspect local distributions without uploading them:

```bash
make build
ls dist/
```

Use `pdm publish` only for an explicit manual recovery path.
