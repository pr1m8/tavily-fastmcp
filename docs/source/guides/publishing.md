# Publishing

Publishing is designed to happen through GitHub Releases and PyPI trusted
publishing, not from a developer laptop.

## Release checklist

1. Confirm repository URLs in `pyproject.toml`, `README.md`, and badge links.
2. Confirm the PyPI project exists and trusted publishing is configured for the
   `Release` workflow and `pypi` environment.
3. Run the local publish gate:

   ```bash
   make publish-check
   ```

4. Update the package version in `pyproject.toml` and `src/tavily_fastmcp/server.py`.
5. Commit the release changes and create a tag such as `v0.3.1`.
6. Push the branch and tag.
7. Publish a GitHub Release for the tag. The `Release` workflow builds and
   uploads distributions to PyPI.

## Manual build

To inspect local distributions without uploading them:

```bash
make build
ls dist/
```

Use `pdm publish` only for an explicit manual recovery path.
