Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/cancelled/2026-06-28-repo-oversize-source-indexing.md, .10x/tickets/done/2026-06-28-repo-searchable-path-symbol-metadata.md, .10x/evidence/2026-06-28-repo-oversize-metadata-local-validation.md

# Repo Oversize and Search Metadata Live Eval

## What was observed

After explicit user approval for writes and evals against new namespaces, live-applied and evaluated repository indexing variants for pytest and Typer:

- current namespace: existing baseline namespace;
- metadata only: default file-size cap plus `--repo-search-metadata`;
- oversize only: `--repo-max-file-bytes 200000` without metadata;
- oversize + metadata: both options enabled.

No stale deletion or namespace deletion was run. All live applies targeted new namespaces only.

## Procedure

Live apply examples:

```bash
uv run turbo-search apply --plan artifacts/site-crawls/github-pytest-dev-pytest-metadata-plan-20260628/plan.json \
  --namespace github-pytest-dev-pytest-v2-metadata \
  --approve --json

uv run turbo-search apply --plan artifacts/site-crawls/github-pytest-dev-pytest-oversize-plan-20260628/plan.json \
  --namespace github-pytest-dev-pytest-v2-oversize \
  --approve --json

uv run turbo-search apply --plan artifacts/site-crawls/github-pytest-dev-pytest-oversize-metadata-plan-20260628/plan.json \
  --namespace github-pytest-dev-pytest-v2-oversize-metadata \
  --approve --json
```

The same pattern was run for `github-fastapi-typer-*` namespaces.

Live retrieval-only evals used:

```bash
uv run turbo-search evals --live --dataset <dataset> --namespace <namespace> \
  --top-k 10 --candidates 200 --json
```

Datasets:

- Existing seed datasets:
  - `src/turbo_search/data/pytest_repo_search_seed_evals.json`
  - `src/turbo_search/data/typer_repo_search_seed_evals.json`
- Experimental authority datasets targeting files skipped by the old 50 KiB plan:
  - `autoresearch/runs/repo-oversize-metadata-live-20260628/pytest-authority-evals.json`
  - `autoresearch/runs/repo-oversize-metadata-live-20260628/typer-authority-evals.json`

Artifacts:

- `autoresearch/runs/repo-oversize-metadata-live-20260628/live-eval-summary.json`
- `autoresearch/runs/repo-oversize-metadata-live-20260628/live-eval-report.md`
- apply/eval JSON files under `autoresearch/runs/repo-oversize-metadata-live-20260628/` and `autoresearch/runs/repo-oversize-metadata-live-20260628/ablations/`.

## Apply counts

| Namespace | Rows | Embeddings | Deleted |
|---|---:|---:|---:|
| `github-pytest-dev-pytest-v2-metadata` | 4084 | 4084 | 0 |
| `github-pytest-dev-pytest-v2-oversize` | 5676 | 5676 | 0 |
| `github-pytest-dev-pytest-v2-oversize-metadata` | 6893 | 6893 | 0 |
| `github-fastapi-typer-v2-metadata` | 2793 | 2793 | 0 |
| `github-fastapi-typer-v2-oversize` | 2922 | 2922 | 0 |
| `github-fastapi-typer-v2-oversize-metadata` | 3221 | 3221 | 0 |

## Eval results

Seed = existing expanded repo seed datasets. Authority = experimental labels targeting files skipped by the old 50 KiB plan.

| Repo | Variant | Seed score | Seed P@5 | Authority score | Authority P@5 | Namespace |
|---|---|---:|---:|---:|---:|---|
| pytest | current namespace | 84.742 | 0.640 | 23.136 | 0.120 | `github-pytest-dev-pytest-v1` |
| pytest | metadata only | 85.971 | 0.700 | 23.425 | 0.160 | `github-pytest-dev-pytest-v2-metadata` |
| pytest | oversize only | 81.354 | 0.580 | 78.622 | 0.320 | `github-pytest-dev-pytest-v2-oversize` |
| pytest | oversize + metadata | 83.784 | 0.620 | 78.636 | 0.320 | `github-pytest-dev-pytest-v2-oversize-metadata` |
| Typer | current namespace | 59.423 | 0.380 | 27.002 | 0.240 | `github-fastapi-typer-v1` |
| Typer | metadata only | 62.062 | 0.440 | 26.739 | 0.240 | `github-fastapi-typer-v2-metadata` |
| Typer | oversize only | 52.042 | 0.320 | 69.619 | 0.400 | `github-fastapi-typer-v2-oversize` |
| Typer | oversize + metadata | 55.279 | 0.400 | 67.177 | 0.400 | `github-fastapi-typer-v2-oversize-metadata` |

## What this supports or challenges

Supports:

- Search metadata alone is useful on the existing seed datasets:
  - pytest seed `84.742 -> 85.971`;
  - Typer seed `59.423 -> 62.062`.
- Oversize indexing solves authority-file recall for queries whose correct answers are central files skipped by the old 50 KiB plan:
  - pytest authority `23.136 -> 78.622` with oversize only;
  - Typer authority `27.002 -> 69.619` with oversize only.
- Metadata partially offsets oversize seed regressions, but not enough to make oversize default-safe.

Challenges:

- Oversize indexing regresses the existing seed datasets:
  - pytest seed `84.742 -> 81.354` with oversize only;
  - Typer seed `59.423 -> 52.042` with oversize only.
- Oversize + metadata still regresses existing seed score versus current namespaces:
  - pytest `84.742 -> 83.784`;
  - Typer `59.423 -> 55.279`.
- Experimental authority labels are assistant-drafted and intentionally target newly included files; they are useful for measuring the blind spot but not enough to promote oversize indexing globally.

## Conclusion

Useful outcomes:

1. `--repo-search-metadata` is the strongest promotion candidate from this slice because metadata-only improved both pytest and Typer seed datasets without changing the file-size cap.
2. `--repo-max-file-bytes 200000` should remain opt-in or become query/role-routed, not a default, because it fixes authority-file recall while regressing existing seed retrieval.
3. The next safe step is to validate metadata-only indexing on the older repo basket (`turbo-search`, `psf/requests`, `pallets/click`) before considering a default planner change.
