Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/cancelled/2026-06-28-repo-oversize-source-indexing.md, .10x/tickets/done/2026-06-28-repo-searchable-path-symbol-metadata.md, .10x/research/2026-06-28-expanded-validation-ranking-hypotheses.md

# Repo Oversize + Searchable Metadata Local Validation

## What was observed

Implemented local-only support for two expanded-validation hypothesis families:

- H1/H2: allow larger text/code files to be included and chunked instead of skipped by the 50 KiB cap.
- H4/H5: optionally add searchable path, file-stem, Python symbol metadata, and per-window symbol breadcrumbs to generated repository Markdown.

The new options are explicit opt-ins:

```text
--repo-max-file-bytes <bytes>
--repo-search-metadata
```

Existing defaults remain unchanged:

```text
repo_max_file_bytes = 51200
repo_search_metadata = false
```

Local plans and apply preflights were generated for pytest and Typer using:

```text
repo_max_file_bytes = 200000
repo_search_metadata = true
```

No credentials, embeddings, turbopuffer calls, writes, deletes, live apply, stale cleanup, namespace deletion, or state mutation occurred.

## Procedure

Implementation validation:

```bash
uv run python -m unittest tests.test_github_repo tests.test_cli
uv run python -m unittest discover tests
git diff --check
```

Local experiment plans:

```bash
uv run turbo-search plan https://github.com/pytest-dev/pytest \
  --namespace github-pytest-dev-pytest-v2-oversize-metadata \
  --out-dir artifacts/site-crawls/github-pytest-dev-pytest-oversize-metadata-plan-20260628 \
  --repo-max-file-bytes 200000 \
  --repo-search-metadata \
  --json

uv run turbo-search plan https://github.com/fastapi/typer \
  --namespace github-fastapi-typer-v2-oversize-metadata \
  --out-dir artifacts/site-crawls/github-fastapi-typer-oversize-metadata-plan-20260628 \
  --repo-max-file-bytes 200000 \
  --repo-search-metadata \
  --json
```

Local apply preflight only:

```bash
uv run turbo-search apply --plan artifacts/site-crawls/github-pytest-dev-pytest-oversize-metadata-plan-20260628/plan.json \
  --namespace github-pytest-dev-pytest-v2-oversize-metadata \
  --json

uv run turbo-search apply --plan artifacts/site-crawls/github-fastapi-typer-oversize-metadata-plan-20260628/plan.json \
  --namespace github-fastapi-typer-v2-oversize-metadata \
  --json
```

Artifacts:

- `artifacts/site-crawls/github-pytest-dev-pytest-oversize-metadata-plan-20260628/plan.json`
- `artifacts/site-crawls/github-fastapi-typer-oversize-metadata-plan-20260628/plan.json`
- `autoresearch/runs/repo-oversize-metadata-local-20260628/summary.json`
- `autoresearch/runs/repo-oversize-metadata-local-20260628/report.md`

## Results

| Target | Files selected | Oversize skipped | Chunks/rows | Authority files included |
|---|---:|---:|---:|---|
| pytest | 573 -> 601 | 31 -> 2 | 3493 -> 6893 | `src/_pytest/fixtures.py`, `src/_pytest/python.py`, `src/_pytest/config/__init__.py` |
| Typer | 644 -> 647 | 3 -> 0 | 2512 -> 3221 | `typer/main.py`, `typer/params.py` |

Preflight rows to upsert:

```text
github-pytest-dev-pytest-v2-oversize-metadata: 6893 rows/embeddings, turbopuffer_api_calls=false
github-fastapi-typer-v2-oversize-metadata: 3221 rows/embeddings, turbopuffer_api_calls=false
```

Generated metadata was present in planned pages, for example:

```text
Search metadata:
Path tokens: typer main
File stem: main
Symbols: except_hook, get_install_completion_arguments, Typer, __init__, callback, main, ...
Symbol tokens: except hook get install completion arguments typer init callback main ...
```

Observed validation:

```text
uv run python -m unittest tests.test_github_repo tests.test_cli
34 tests OK

uv run python -m unittest discover tests
142 tests OK

git diff --check
OK
```

## What this supports or challenges

Supports:

- H1/H2 are locally viable: a 200 KiB repo file cap includes central pytest/Typer source files without exploding row counts beyond local reviewability.
- H4/H5 are locally viable: generated code pages can include searchable path and Python symbol metadata without changing existing defaults.
- The opt-in design preserves existing plan behavior unless the new flags are used.

Challenges / limits:

- Retrieval quality is not measured yet; these namespaces were not live-applied.
- Current seed datasets avoid some previously skipped central files. To fairly measure oversize-source gains, either live evals need updated experimental labels or new cases that expect those authority files.
- Metadata is currently Python-symbol focused and does not use Tree-sitter or language-specific parsers for non-Python languages.

## Conclusion

Local implementation and plan/preflight validation passed. The next step, if approved, is live-applying the two new experimental namespaces without `--delete-stale`, then running live retrieval-only evals with updated/experimental labels that include the newly indexed authority files.
