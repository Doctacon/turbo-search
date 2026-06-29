Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/2026-06-28-promote-website-page-ranking-default.md, .10x/decisions/website-ranking-defaults.md

# Website Page Ranking Default Promotion Validation

## What was observed

Implemented namespace-aware ranking defaults for CLI `retrieve` and `evals`.

Promoted website defaults for `site-*` namespaces:

```text
ranking_mode = page
ranking_profile = none
ranking_pool = 20
ranking_aggregation = max
```

Preserved repository/general defaults for non-`site-*` namespaces:

```text
ranking_mode = file
ranking_profile = repo_code
ranking_pool = 100
ranking_aggregation = max
```

Explicit CLI ranking flags still override namespace-derived defaults.

Changed files:

- `src/turbo_search/retriever.py`
- `src/turbo_search/cli.py`
- `src/turbo_search/autoresearch.py`
- `tests/test_cli.py`
- `tests/test_autoresearch.py`
- `README.md`
- `docs/generic-site-rag-plan-apply.md`
- `.10x/knowledge/repo-search-ranking-defaults.md`

Records added/updated:

- `.10x/decisions/website-ranking-defaults.md`
- `.10x/tickets/2026-06-28-promote-website-page-ranking-default.md`
- `.10x/tickets/2026-06-28-website-ranking-default-promotion-decision.md`

## Validation commands

```bash
uv run python -m unittest tests.test_cli tests.test_retriever tests.test_evals tests.test_autoresearch
uv run python -m unittest discover tests
git diff --check
```

Observed:

```text
56 tests OK
133 tests OK
git diff --check: no whitespace errors
```

Unit coverage includes:

- `retrieve` dry-run for default `site-*` namespace resolves to page/none/pool20/max.
- `evals` dry-run for default `site-*` namespace resolves to page/none/pool20/max.
- `retrieve` dry-run for `github-doctacon-turbo-search-v1` resolves to file/repo_code/pool100/max.
- `evals` dry-run for `github-doctacon-turbo-search-v1` resolves to file/repo_code/pool100/max.
- Explicit `--ranking-mode`, `--ranking-profile`, `--ranking-pool`, and `--ranking-aggregation` still override defaults.
- Config-only autoresearch experiments inherit website defaults for `site-*` namespaces when ranking options are omitted.

## Live retrieval-only validation

Artifacts:

- `autoresearch/runs/website-default-promotion-20260628/turbopuffer-default.json`
- `autoresearch/runs/website-default-promotion-20260628/sqlmesh-default.json`
- `autoresearch/runs/website-default-promotion-20260628/repo-default.json`
- `autoresearch/runs/website-default-promotion-20260628/summary.json`
- `autoresearch/runs/website-default-promotion-20260628/report.md`

Safety:

- live turbopuffer retrieval calls only;
- no live writes;
- no deletes or stale deletes;
- no namespace management;
- no state mutation.

Results with omitted ranking flags:

| Corpus | Namespace | Mode | Profile | Pool | Aggregation | P@5 | Score | NDCG | Recall | MRR |
|---|---|---|---|---:|---|---:|---:|---:|---:|---:|
| turbopuffer | `site-turbopuffer-com-v1` | page | none | 20 | max | 0.270 | 65.279 | 0.727 | 0.567 | 0.750 |
| SQLMesh | `site-sqlmesh-readthedocs-io-v1` | page | none | 20 | max | 0.473 | 87.460 | 0.959 | 0.750 | 1.000 |
| repo | `github-doctacon-turbo-search-v1` | file | repo_code | 100 | max | 0.500 | 87.251 | 0.920 | 0.833 | 1.000 |

## What this supports or challenges

Supports:

- Website defaults are now namespace-aware and use validated page ranking.
- Repository defaults are preserved for GitHub namespaces.
- The promoted defaults reproduce the intended precision-oriented website behavior without requiring users to pass ranking flags.

Challenges / limits:

- Website seed labels are still assistant-drafted, not human-approved.
- `capped_sum_3` remains opt-in because it was not uniformly better than max at pool 20.

## Conclusion

The promotion is implemented, tested, and live-retrieval validated. No namespace data was mutated.
