Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/2026-06-28-repo-search-heavy-ranking-experiments.md, .10x/decisions/namespace-ranking-defaults.md

# Cross-Repo Click Validation

Note: this evidence created the aggregation decision point. A follow-up adaptive aggregation experiment resolved it by promoting `adaptive_sum_3`; see `.10x/evidence/2026-06-28-repo-adaptive-aggregation-validation.md`.

## What was observed

Validated repo search on a third public repository selected by the user:

```text
https://github.com/pallets/click
```

New namespace:

```text
github-pallets-click-v1
```

Commit indexed:

```text
679a7a0eccbdded7a6e85680bdaaf08003765e01
```

Added eval dataset:

```text
src/turbo_search/data/click_repo_search_seed_evals.json
```

The dataset has 10 assistant-drafted, source-backed cases covering decorators, core command/context runtime, parser/options/arguments, parameter types, terminal UI, `CliRunner`, shell completion, exceptions, help formatting, and utility helpers.

Safety:

- new namespace only;
- approved live upsert to the new namespace;
- no namespace deletion;
- no stale deletion;
- no mutation of existing namespaces;
- no proprietary model APIs.

## Procedure

Plan:

```bash
uv run turbo-search plan https://github.com/pallets/click \
  --out-dir artifacts/site-crawls/github-pallets-click-plan-20260628 \
  --namespace github-pallets-click-v1 \
  --json
```

Observed plan summary:

```text
files_discovered = 150
files_selected = 140
files_skipped_filtered = 1
files_skipped_empty = 3
files_skipped_binary = 1
files_skipped_oversize = 5
chunks_generated = 1196
rows_to_upsert = 1196
first_apply = true
turbopuffer_api_calls = false
```

Apply preflight and approved apply:

```bash
uv run turbo-search apply \
  --plan artifacts/site-crawls/github-pallets-click-plan-20260628/plan.json \
  --namespace github-pallets-click-v1 \
  --json

uv run turbo-search apply \
  --plan artifacts/site-crawls/github-pallets-click-plan-20260628/plan.json \
  --namespace github-pallets-click-v1 \
  --approve \
  --json
```

Observed approved apply:

```text
rows_to_upsert = 1196
rows_upserted = 1196
embeddings_generated = 1196
stale_rows = 0
rows_deleted = 0
state_updated = true
```

Live evals:

```bash
uv run turbo-search evals \
  --live \
  --dataset src/turbo_search/data/click_repo_search_seed_evals.json \
  --namespace github-pallets-click-v1 \
  --top-k 10 \
  --candidates 200
```

Artifacts:

- `artifacts/site-crawls/github-pallets-click-plan-20260628/summary.json`
- `autoresearch/runs/cross-repo-click-20260628/apply-preflight.json`
- `autoresearch/runs/cross-repo-click-20260628/apply-approved.json`
- `autoresearch/runs/cross-repo-click-20260628/eval-default.json`
- `autoresearch/runs/cross-repo-click-20260628/eval-capped.json`
- `autoresearch/runs/cross-repo-click-20260628/eval-chunk-none.json`
- `autoresearch/runs/cross-repo-click-20260628/summary.json`
- `autoresearch/runs/cross-repo-click-20260628/report.md`
- `autoresearch/runs/cross-repo-three-repo-aggregation-20260628/summary.json`
- `autoresearch/runs/cross-repo-three-repo-aggregation-20260628/report.md`

Validation commands:

```bash
uv run python -m unittest discover tests
git diff --check
```

Observed:

```text
139 tests OK
git diff --check: no whitespace errors
```

## Results

### Click only

| Variant | P@5 | Score | NDCG | Recall | MRR | Passed |
|---|---:|---:|---:|---:|---:|---:|
| file / repo_code / pool100 / max | 0.380 | 67.150 | 0.676 | 0.633 | 0.900 | 10/10 |
| file / repo_code / pool100 / capped_sum_3 | 0.420 | 72.550 | 0.744 | 0.658 | 0.950 | 10/10 |
| chunk / none | 0.240 | 42.769 | 0.350 | 0.517 | 0.720 | 10/10 |

### Three-repo aggregation comparison with current scoring profile

| Aggregation | Corpus | P@5 | Score | NDCG | Recall | MRR |
|---|---|---:|---:|---:|---:|---:|
| max | turbo-search | 0.520 | 87.126 | 0.914 | 0.833 | 1.000 |
| max | psf/requests | 0.420 | 84.093 | 0.889 | 0.800 | 1.000 |
| max | pallets/click | 0.380 | 67.150 | 0.676 | 0.633 | 0.900 |
| max | average | 0.440 | 79.457 |  |  |  |
| capped_sum_3 | turbo-search | 0.540 | 90.061 | 0.939 | 0.900 | 1.000 |
| capped_sum_3 | psf/requests | 0.420 | 81.620 | 0.852 | 0.833 | 0.925 |
| capped_sum_3 | pallets/click | 0.420 | 72.550 | 0.744 | 0.658 | 0.950 |
| capped_sum_3 | average | 0.460 | 81.411 |  |  |  |

## What this supports or challenges

Supports:

- File-level `repo_code` ranking remains far better than raw chunk ranking on Click.
- Click is a harder validation corpus than `turbo-search` or `psf/requests`; both `max` and `capped_sum_3` scores are materially lower.
- With the current query-aware, path/symbol, and role-diversification profile, `capped_sum_3` is now stronger on two of three repos and stronger on the three-repo average.

Challenges:

- The active universal default remains `max`, but Click reopens the aggregation question. `capped_sum_3` still regresses `psf/requests` versus `max` (`84.093 -> 81.620`) even though it improves the three-repo average.
- The Click dataset is assistant-drafted and not human-reviewed; label noise may be higher because Click has many broad core/docs/test files.
- The next universal-default decision depends on policy: avoid any repo regression (`max`) versus optimize average composite across validation repos (`capped_sum_3` or adaptive aggregation).

## Conclusion

Do not silently change the universal aggregation default from `max` based on this evidence alone. Click materially challenges the current default and creates a decision point: either keep no-regression `max`, promote average-better `capped_sum_3`, or test an adaptive scoring-only aggregation rule. The follow-up adaptive rule was tested and promoted separately in `.10x/evidence/2026-06-28-repo-adaptive-aggregation-validation.md`.
