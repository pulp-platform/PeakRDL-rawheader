# Release Process

This document describes how to publish a new release of `peakrdl-rawheader` to PyPI.

## Steps

1. Bump the version number in `pyproject.toml`.

If you are using `uv`:

```bash
uv version --bump major|minor|patch
```

If you bump the version manually, run:

```bash
uv lock
```

2. Update `CHANGELOG.md` for the new version.

3. Commit and push the release preparation changes:

```bash
git add pyproject.toml uv.lock CHANGELOG.md
git commit -m "Release vX.Y.Z"
git push origin main
```

4. Optional: publish to TestPyPI first by running the `publish-test-pypi` CI job via manual `workflow_dispatch`.

5. Create a new GitHub release with the matching version tag (for example `vX.Y.Z`).

This triggers the GitHub [release workflow](.github/workflows/release.yml), which builds and publishes the package to PyPI using [Trusted Publishing](https://docs.pypi.org/trusted-publishers/).
