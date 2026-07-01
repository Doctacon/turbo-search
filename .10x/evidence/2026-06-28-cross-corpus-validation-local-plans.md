Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/2026-06-28-cross-corpus-validation-basket.md

# Cross-Corpus Validation Local Plans

## What was observed

Local-only plan artifacts were generated for the expanded validation basket selected by the user:

- `https://github.com/pytest-dev/pytest`
- `https://github.com/fastapi/typer`
- `https://docs.astral.sh/ruff/`
- `https://typer.tiangolo.com/`

All runs reported:

```text
dry_run = true
turbopuffer_api_calls = false
credentials_required = false
errors = []
limit_reached = false
```

No embeddings, turbopuffer writes, namespace mutation, stale deletion, namespace deletion, or credential reads occurred.

## Procedure

Repository plans:

```bash
uv run turbo-search plan https://github.com/pytest-dev/pytest \
  --namespace github-pytest-dev-pytest-v1 \
  --out-dir artifacts/site-crawls/github-pytest-dev-pytest-plan-20260628 \
  --json | tee artifacts/site-crawls/github-pytest-dev-pytest-plan-20260628.plan-output.json

uv run turbo-search plan https://github.com/fastapi/typer \
  --namespace github-fastapi-typer-v1 \
  --out-dir artifacts/site-crawls/github-fastapi-typer-plan-20260628 \
  --json | tee artifacts/site-crawls/github-fastapi-typer-plan-20260628.plan-output.json
```

Website plans:

```bash
uv run turbo-search plan https://docs.astral.sh/ruff/ \
  --namespace site-ruff-docs-v1 \
  --out-dir artifacts/site-crawls/ruff-docs-plan-20260628 \
  --max-pages 250 \
  --max-chunks 10000 \
  --concurrent-requests 2 \
  --concurrent-requests-per-domain 1 \
  --download-delay 0.25 \
  --css-selector .md-content__inner \
  --include-path /ruff \
  --include-path '/ruff/**' \
  --exclude-path '/ruff/llms*.txt' \
  --json | tee artifacts/site-crawls/ruff-docs-plan-20260628.plan-output.json

uv run turbo-search plan https://typer.tiangolo.com/ \
  --namespace site-typer-docs-v1 \
  --out-dir artifacts/site-crawls/typer-docs-plan-20260628 \
  --max-pages 250 \
  --max-chunks 10000 \
  --concurrent-requests 2 \
  --concurrent-requests-per-domain 1 \
  --download-delay 0.25 \
  --css-selector .md-content__inner \
  --exclude-path '/llms*.txt' \
  --json | tee artifacts/site-crawls/typer-docs-plan-20260628.plan-output.json
```

Summary artifact:

- `autoresearch/runs/cross-corpus-validation-basket-20260628/plan-summary.json`
- `autoresearch/runs/cross-corpus-validation-basket-20260628/plan-report.md`

## Results

| Target | Namespace | Pages/files | Chunks/rows | Requests | Commit | Limit | Errors |
|---|---|---:|---:|---:|---|---|---|
| pytest repo | `github-pytest-dev-pytest-v1` | 573 | 3493 | 0 | `1aa747de62dd` | false | 0 |
| typer repo | `github-fastapi-typer-v1` | 644 | 2512 | 0 | `b210c0e2376d` | false | 0 |
| ruff docs | `site-ruff-docs-v1` | 249 | 1441 | 253 | n/a | false | 0 |
| typer docs | `site-typer-docs-v1` | 75 | 1271 | 156 | n/a | false | 0 |

Plan artifacts:

- `artifacts/site-crawls/github-pytest-dev-pytest-plan-20260628/plan.json`
- `artifacts/site-crawls/github-fastapi-typer-plan-20260628/plan.json`
- `artifacts/site-crawls/ruff-docs-plan-20260628/plan.json`
- `artifacts/site-crawls/typer-docs-plan-20260628/plan.json`

## What this supports or challenges

Supports:

- The four selected targets are viable validation-basket candidates.
- The planned live index size is moderate: 8,717 total rows/chunks.
- The repo sources are pinned by observed commit SHA for repeatability.
- The docs-site crawls completed within the 250-page cap without hitting the limit.

Limits:

- These are only local plan artifacts; no live namespace exists yet for these targets.
- No seed eval labels have been drafted yet.
- No retrieval quality conclusion is supported until live apply and retrieval-only evals are explicitly approved and run.
