Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/done/2026-06-28-cross-corpus-validation-basket.md

# Cross-Corpus Seed Eval Datasets

## What was observed

Assistant-drafted seed eval datasets were added for the expanded validation basket:

| Target | Dataset | Cases | Judgments |
|---|---|---:|---:|
| pytest repo | `src/turbo_search/data/pytest_repo_search_seed_evals.json` | 10 | 52 |
| Typer repo | `src/turbo_search/data/typer_repo_search_seed_evals.json` | 10 | 53 |
| Ruff docs | `src/turbo_search/data/ruff_site_search_seed_evals.json` | 10 | 31 |
| Typer docs | `src/turbo_search/data/typer_site_search_seed_evals.json` | 10 | 37 |

All labels are seed-draft and are not human-approved ground truth.

No live retrieval, embeddings, credential reads, turbopuffer calls, namespace writes, stale deletion, or namespace deletion occurred.

## Procedure

Datasets were drafted against local plan artifacts from `.10x/evidence/2026-06-28-cross-corpus-validation-local-plans.md`.

Validation commands:

```bash
uv run turbo-search evals --dry-run --dataset src/turbo_search/data/pytest_repo_search_seed_evals.json --namespace dummy --json
uv run turbo-search evals --dry-run --dataset src/turbo_search/data/typer_repo_search_seed_evals.json --namespace dummy --json
uv run turbo-search evals --dry-run --dataset src/turbo_search/data/ruff_site_search_seed_evals.json --namespace dummy --json
uv run turbo-search evals --dry-run --dataset src/turbo_search/data/typer_site_search_seed_evals.json --namespace dummy --json
uv run python -m unittest tests.test_evals
```

Additional source-backing check compared every `repo_path` judgment to the corresponding repo plan manifest and every site `url` judgment to the corresponding site plan manifest.

Observed source-backing results:

```text
pytest cases 10 judgments 52 missing 0
typer cases 10 judgments 53 missing 0
ruff cases 10 judgments 31 missing 0
typerdocs cases 10 judgments 37 missing 0
```

Observed unit test result:

```text
Ran 17 tests in 0.006s
OK
```

Summary artifacts:

- `autoresearch/runs/cross-corpus-validation-basket-20260628/seed-dataset-summary.json`
- `autoresearch/runs/cross-corpus-validation-basket-20260628/seed-dataset-report.md`

## What this supports or challenges

Supports:

- The four new validation targets now have parseable, source-backed seed eval datasets.
- The datasets can be listed in dry-run mode without credentials or turbopuffer calls.
- A new `tests.test_evals` coverage check loads the expanded basket datasets.

Challenges / limits:

- Labels are assistant-drafted and should be treated as calibration labels, not human-approved product ground truth.
- Repository plan defaults skip files above 50 KiB. For `pytest-dev/pytest` and `fastapi/typer`, some central implementation files were not in the planned corpus, so repo labels intentionally target selected source/docs/tests that can actually be retrieved from the current plan. This limits what the expanded repo evals can measure until oversized source handling is improved.
- No live namespace exists yet for these four targets; retrieval quality remains unmeasured until live apply and live evals are explicitly approved.

## Conclusion

Step 2 of the validation basket is complete: seed datasets exist and are structurally/source-backed against the local plans. The next step is live apply approval for the four new namespaces, followed by live retrieval-only evals under the no-regression policy.
