Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/2026-06-28-repo-search-heavy-ranking-experiments.md, .10x/decisions/namespace-ranking-defaults.md

# Repo Adaptive Aggregation Validation

## What was observed

Implemented `adaptive_sum_3` aggregation for file/page ranking and promoted it as the repository namespace default.

Formula:

```text
score = best_chunk_score * (1 + 0.05 * close_extra_chunk_count)
close_extra_chunk_count = count of chunks 2..3 where chunk_score >= 0.80 * best_chunk_score
```

This is intentionally much more conservative than `capped_sum_3`:

- `max` uses only the best chunk score;
- `capped_sum_3` fully sums up to three chunk scores;
- `adaptive_sum_3` starts from `max` and adds only a small 5%-per-close-extra-chunk bonus, capped at 10%.

No writes, deletes, reindexing, namespace cleanup, or state mutation were performed for the evals. The only code change is scoring behavior over existing retrieved candidates.

## Procedure

Regression tests:

```bash
uv run python -m unittest tests.test_retriever tests.test_cli tests.test_autoresearch
uv run python -m unittest discover tests
git diff --check
```

Observed:

```text
47 tests OK
140 tests OK
git diff --check: no whitespace errors
```

Live retrieval-only evals across the three current repo validation corpora:

```bash
uv run turbo-search evals --live \
  --dataset <repo dataset> \
  --namespace <repo namespace> \
  --top-k 10 \
  --candidates 200

uv run turbo-search evals --live \
  --dataset <repo dataset> \
  --namespace <repo namespace> \
  --top-k 10 \
  --candidates 200 \
  --ranking-mode file \
  --ranking-profile repo-code \
  --ranking-pool 100 \
  --ranking-aggregation max

uv run turbo-search evals --live \
  --dataset <repo dataset> \
  --namespace <repo namespace> \
  --top-k 10 \
  --candidates 200 \
  --ranking-mode file \
  --ranking-profile repo-code \
  --ranking-pool 100 \
  --ranking-aggregation capped-sum-3
```

Artifacts:

- `autoresearch/runs/repo-adaptive-aggregation-20260628/turbo-adaptive-default.json`
- `autoresearch/runs/repo-adaptive-aggregation-20260628/requests-adaptive-default.json`
- `autoresearch/runs/repo-adaptive-aggregation-20260628/click-adaptive-default.json`
- `autoresearch/runs/repo-adaptive-aggregation-20260628/turbo-max.json`
- `autoresearch/runs/repo-adaptive-aggregation-20260628/requests-max.json`
- `autoresearch/runs/repo-adaptive-aggregation-20260628/click-max.json`
- `autoresearch/runs/repo-adaptive-aggregation-20260628/turbo-capped.json`
- `autoresearch/runs/repo-adaptive-aggregation-20260628/requests-capped.json`
- `autoresearch/runs/repo-adaptive-aggregation-20260628/click-capped.json`
- `autoresearch/runs/repo-adaptive-aggregation-20260628/summary.json`
- `autoresearch/runs/repo-adaptive-aggregation-20260628/report.md`

## Results

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
| adaptive_sum_3 | turbo-search | 0.540 | 87.760 | 0.922 | 0.833 | 1.000 |
| adaptive_sum_3 | psf/requests | 0.420 | 84.426 | 0.895 | 0.800 | 1.000 |
| adaptive_sum_3 | pallets/click | 0.400 | 72.474 | 0.733 | 0.658 | 1.000 |
| adaptive_sum_3 | average | 0.453 | 81.553 |  |  |  |

## What this supports or challenges

Supports:

- `adaptive_sum_3` improves all three validation repos versus strict `max`.
- `adaptive_sum_3` beats `capped_sum_3` on the three-repo average while avoiding the Requests regression caused by full capped aggregation.
- `adaptive_sum_3` is a safe universal repository default candidate under the current no-regression standard.

Challenges / limits:

- The validation set is still only three repositories and all labels are assistant-drafted.
- The adaptive parameters (`0.80` closeness threshold, `0.05` bonus) are empirically chosen from current evals, not learned.
- Website defaults remain `page/max`; this evidence only supports repository/general namespace defaults.

## Conclusion

Promote `adaptive_sum_3` as the repository/default namespace aggregation while keeping website namespaces on `max`:

```text
site-* = page / none / pool20 / max
repo/general = file / repo_code / pool100 / adaptive_sum_3
```
