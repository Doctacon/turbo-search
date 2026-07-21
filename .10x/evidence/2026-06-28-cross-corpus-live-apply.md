Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/done/2026-06-28-cross-corpus-validation-basket.md, .10x/evidence/2026-06-28-cross-corpus-validation-local-plans.md, .10x/evidence/2026-06-28-cross-corpus-seed-eval-datasets.md

# Cross-Corpus Live Apply

## What was observed

After explicit user approval, the four expanded validation basket namespaces were live-applied from the previously generated local plans.

No stale deletion or namespace deletion was requested or run. All applies used the default local embedding model `BAAI/bge-small-en-v1.5` and updated local applied state after successful upsert.

## Procedure

Preflight, local-only, no credentials or turbopuffer API calls:

```bash
uv run turbo-search apply --plan artifacts/site-crawls/github-pytest-dev-pytest-plan-20260628/plan.json --namespace github-pytest-dev-pytest-v1 --json
uv run turbo-search apply --plan artifacts/site-crawls/github-fastapi-typer-plan-20260628/plan.json --namespace github-fastapi-typer-v1 --json
uv run turbo-search apply --plan artifacts/site-crawls/ruff-docs-plan-20260628/plan.json --namespace site-ruff-docs-v1 --json
uv run turbo-search apply --plan artifacts/site-crawls/typer-docs-plan-20260628/plan.json --namespace site-typer-docs-v1 --json
```

Approved live apply, without `--delete-stale`:

```bash
uv run turbo-search apply --plan artifacts/site-crawls/github-pytest-dev-pytest-plan-20260628/plan.json --namespace github-pytest-dev-pytest-v1 --approve --json
uv run turbo-search apply --plan artifacts/site-crawls/github-fastapi-typer-plan-20260628/plan.json --namespace github-fastapi-typer-v1 --approve --json
uv run turbo-search apply --plan artifacts/site-crawls/ruff-docs-plan-20260628/plan.json --namespace site-ruff-docs-v1 --approve --json
uv run turbo-search apply --plan artifacts/site-crawls/typer-docs-plan-20260628/plan.json --namespace site-typer-docs-v1 --approve --json
```

Artifacts:

- `autoresearch/runs/cross-corpus-validation-basket-20260628/live-apply/pytest-preflight.json`
- `autoresearch/runs/cross-corpus-validation-basket-20260628/live-apply/pytest-apply.json`
- `autoresearch/runs/cross-corpus-validation-basket-20260628/live-apply/typer-repo-preflight.json`
- `autoresearch/runs/cross-corpus-validation-basket-20260628/live-apply/typer-repo-apply.json`
- `autoresearch/runs/cross-corpus-validation-basket-20260628/live-apply/ruff-docs-preflight.json`
- `autoresearch/runs/cross-corpus-validation-basket-20260628/live-apply/ruff-docs-apply.json`
- `autoresearch/runs/cross-corpus-validation-basket-20260628/live-apply/typer-docs-preflight.json`
- `autoresearch/runs/cross-corpus-validation-basket-20260628/live-apply/typer-docs-apply.json`
- `autoresearch/runs/cross-corpus-validation-basket-20260628/live-apply/apply-summary.json`
- `autoresearch/runs/cross-corpus-validation-basket-20260628/live-apply/apply-report.md`

## Results

| Target | Namespace | Rows upserted | Embeddings | Rows deleted | State updated |
|---|---|---:|---:|---:|---|
| pytest repo | `github-pytest-dev-pytest-v1` | 3493 | 3493 | 0 | true |
| Typer repo | `github-fastapi-typer-v1` | 2512 | 2512 | 0 | true |
| Ruff docs | `site-ruff-docs-v1` | 1441 | 1441 | 0 | true |
| Typer docs | `site-typer-docs-v1` | 1271 | 1271 | 0 | true |
| **total** |  | 8717 | 8717 | 0 |  |

Preflight also showed `stale_rows = 0` for all four targets and `delete_stale = false`.

## What this supports or challenges

Supports:

- The expanded validation basket now has live namespaces available for retrieval-only evals.
- Apply behavior matched the local plans: all planned rows were embedded/upserted and no rows were deleted.
- Local applied state was updated for each namespace.

Limits:

- This evidence proves index application counts, not retrieval quality.
- Live retrieval-only evals still need explicit approval under the project guardrail before running.
- Seed labels remain assistant-drafted and not human-approved.
