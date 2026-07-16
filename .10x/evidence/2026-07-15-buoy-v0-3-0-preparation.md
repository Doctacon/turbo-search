Status: recorded
Created: 2026-07-15
Updated: 2026-07-15
Relates-To: .10x/tickets/2026-07-15-prepare-buoy-v0-3-0.md, .10x/tickets/2026-07-15-buoy-v0-3-0-release-plan.md

# Buoy v0.3.0 Preparation

## What was observed

Release preparation aligns the authoritative project, module, and lock metadata on `0.3.0`. The changelog contains a pending 0.3.0 section with no release link/date claim. It covers the canonical local catalog, apply registration/recovery, opt-in auto-routing, explicit-retrieval preservation, and state-root posture. Active identity/compatibility specifications, migration/release docs, runtime warnings, and regression tests retain deprecated command/environment aliases through 0.3 and consistently target removal in 0.4.

Both CI runtime suites passed 364 tests. Exact v0.3.0 tag and asset dry checks passed. The build produced exactly one wheel and one sdist (excluding uv's output-directory `.gitignore`) under `/tmp`, outside the repository. Machine-readable artifact observations are stored at `.10x/evidence/.storage/2026-07-15-buoy-v0-3-0-preparation-artifacts.json`.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `buoy_search-0.3.0-py3-none-any.whl` | 158105 | `7e065496344539cc650ee1c0b4a768b7bf2d6a6e743762b87cd58400de7c6b56` |
| `buoy_search-0.3.0.tar.gz` | 962860 | `8ad6493539b01d11ad65dd79c74a18da1bb81071aea0e3e3b2c24d0193a79fb2` |

Wheel `METADATA` and sdist `PKG-INFO` report `Name: buoy-search` and `Version: 0.3.0`. The wheel has 44 entries and sdist 432; both contain catalog/routing implementation, bundled package content, and no `turbo_search` import package. An isolated Python 3.13 wheel installation reported `buoy 0.3.0` from both console scripts; `turbo-search --version` emitted only the expected stderr deprecation warning ending `It will be removed in 0.4.` The `buoy_search` import reported 0.3.0 and `turbo_search` remained absent.

## Procedure

All commands ran from the bounded release-preparation worktree. Credential variables were unset for validation; full tests and repository checks set `HF_HUB_OFFLINE=1` and `TRANSFORMERS_OFFLINE=1` so no model lookup/download could occur.

```text
uv sync --locked --python 3.11
PYTHONDONTWRITEBYTECODE=1 uv run --python 3.11 python -m unittest discover -s tests -p 'test_*.py' -q
# Ran 364 tests: OK

uv sync --locked --python 3.13
PYTHONDONTWRITEBYTECODE=1 uv run --python 3.13 python -m unittest discover -s tests -p 'test_*.py' -q
# Ran 364 tests: OK

uv run --python 3.13 python -m unittest tests.test_release_automation tests.test_cli -q
# Ran 48 tests: OK

rm -rf /tmp/buoy-v0.3.0-dist
uv build --out-dir /tmp/buoy-v0.3.0-dist
uv run --no-project python scripts/release_checks.py tag --tag v0.3.0
uv run --no-project python scripts/release_checks.py assets --dist /tmp/buoy-v0.3.0-dist

uv venv /tmp/buoy-v0.3.0-venv --python 3.13
uv pip install --python /tmp/buoy-v0.3.0-venv/bin/python /tmp/buoy-v0.3.0-dist/buoy_search-0.3.0-py3-none-any.whl
/tmp/buoy-v0.3.0-venv/bin/buoy --version
/tmp/buoy-v0.3.0-venv/bin/turbo-search --version

uv lock --check
PYTHONPYCACHEPREFIX=/tmp/buoy-v0.3.0-pyc uv run --python 3.13 python -m compileall -q src tests scripts
rg <bounded current-authority version/deprecation consistency patterns>
git diff --check
```

A first isolated `--no-deps` wheel invocation correctly failed because CLI module import requires declared runtime dependencies (`duckdb` was first absent). The final isolated check installed declared wheel dependencies and then passed; this did not change the repository or release assets.

## What this supports or challenges

This supports the preparation ticket's local acceptance criteria: exact current version metadata/assets, accurate pending changelog, retained compatibility with a 0.4 removal target, CI-equivalent runtime coverage, artifact contents, and side-effect-free release dry checks. Tests added/updated assert 0.3.0 tag/assets, pending changelog behavior, and consistent 0.4 warnings across CLI, environment configuration, migration guide, and changelog.

## External-side-effect attestation

No GitHub mutation, tag creation/push, main/develop mutation, package publication, credential read, model construction/inference, Hugging Face model download, or Turbopuffer operation occurred. The isolated wheel dependency installation accessed ordinary Python package distribution infrastructure; it did not publish anything or access model weights.

## Limits

- Local macOS Python 3.11/3.13 validation does not replace hosted Linux CI; the ticket remains active for independent review and PR checks.
- Artifact digests apply to this local build. The hosted release workflow rebuilds once from the eventual reviewed tag and is authoritative for published asset digests.
- The changelog intentionally remains pending and omits the v0.3.0 release link/date until the separately owned post-release finalization child.
