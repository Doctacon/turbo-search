Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/2026-06-28-cross-site-page-aggregation-validation.md, .10x/evidence/2026-06-28-opt-in-page-aggregation-ranking-validation.md

# Cross-Site Page Aggregation Validation: SQLMesh

## What was observed

Validated the opt-in website page ranking/aggregation path on an existing indexed website namespace other than `turbopuffer.com`.

Namespace:

- `site-sqlmesh-readthedocs-io-v1`

Existing applied state:

- `.turbo-search/state/sqlmesh-readthedocs-io/site-sqlmesh-readthedocs-io-v1/last-applied.json`

Dataset added:

- `src/turbo_search/data/sqlmesh_site_search_seed_evals.json`

The SQLMesh dataset is assistant-drafted and not human-approved ground truth.

Safety:

- live turbopuffer retrieval calls only;
- no live writes;
- no stale deletes;
- no namespace deletion/replacement/management;
- no state mutation;
- no new indexing.

## Procedure

Compared current default, simple page ranking, and capped page aggregation:

```bash
uv run turbo-search evals \
  --live \
  --dataset src/turbo_search/data/sqlmesh_site_search_seed_evals.json \
  --namespace site-sqlmesh-readthedocs-io-v1 \
  --top-k 10 \
  --candidates 200

uv run turbo-search evals \
  --live \
  --dataset src/turbo_search/data/sqlmesh_site_search_seed_evals.json \
  --namespace site-sqlmesh-readthedocs-io-v1 \
  --top-k 10 \
  --candidates 200 \
  --ranking-mode page \
  --ranking-profile none \
  --ranking-pool 20

uv run turbo-search evals \
  --live \
  --dataset src/turbo_search/data/sqlmesh_site_search_seed_evals.json \
  --namespace site-sqlmesh-readthedocs-io-v1 \
  --top-k 10 \
  --candidates 200 \
  --ranking-mode page \
  --ranking-profile none \
  --ranking-pool 20 \
  --ranking-aggregation capped-sum-3
```

Additional pool/candidate checks compared max vs capped aggregation at pool 100 and candidate 400/pool 150.

Artifacts:

- `autoresearch/runs/cross-site-page-aggregation-sqlmesh-20260628/summary.json`
- `autoresearch/runs/cross-site-page-aggregation-sqlmesh-20260628/report.md`
- per-variant JSON files in the same directory.

Validation commands:

```bash
uv run python -m unittest tests.test_evals tests.test_cli tests.test_retriever tests.test_autoresearch
uv run python -m unittest discover tests
git diff --check
```

Observed:

```text
53 tests OK
130 tests OK
git diff --check: no whitespace errors
```

## Results

| Variant | Candidates | Pool | Aggregation | P@5 | ΔP@5 | Score | ΔScore | NDCG | Recall | MRR |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
| default-file | 200 | 100 | max | 0.260 | +0.000 | 84.484 | +0.000 | 0.943 | 0.750 | 1.000 |
| page-max-pool20 | 200 | 20 | max | 0.473 | +0.213 | 87.460 | +2.975 | 0.959 | 0.750 | 1.000 |
| page-capped-sum-3-pool20 | 200 | 20 | capped_sum_3 | 0.473 | +0.213 | 87.460 | +2.975 | 0.959 | 0.750 | 1.000 |
| page-max-pool100 | 200 | 100 | max | 0.280 | +0.020 | 85.526 | +1.042 | 0.959 | 0.750 | 1.000 |
| page-capped-sum-3-pool100 | 200 | 100 | capped_sum_3 | 0.280 | +0.020 | 86.735 | +2.250 | 0.962 | 0.800 | 1.000 |
| page-max-c400-pool150 | 400 | 150 | max | 0.280 | +0.020 | 85.526 | +1.042 | 0.959 | 0.750 | 1.000 |
| page-capped-sum-3-c400-pool150 | 400 | 150 | capped_sum_3 | 0.280 | +0.020 | 86.754 | +2.269 | 0.963 | 0.800 | 1.000 |

## Interpretation

The cross-site result supports page-level ranking beyond `turbopuffer.com`:

- SQLMesh page mode with pool 20 improved Precision@5 substantially over the current default: `0.260 -> 0.473`.
- SQLMesh page mode improved composite score: `84.484 -> 87.460`.
- `capped_sum_3` did not improve over `max` at pool 20 on SQLMesh, but it also did not regress.
- At larger pools, `capped_sum_3` improved recall/composite relative to max with the same pool/candidate settings: pool 100 score `85.526 -> 86.735`; candidate 400/pool 150 score `85.526 -> 86.754`.

This means the strongest cross-site signal is now **page-level grouping/ranking**. Capped aggregation remains useful for larger pools and was the best turbopuffer.com option, but the SQLMesh win at the recommended pool 20 comes from URL/page deduplication rather than extra capped aggregation.

## What this supports or challenges

Supports:

- Website search should likely use a website-specific page ranking path rather than repository-style file ranking or raw chunks.
- `--ranking-mode page --ranking-profile none` is validated on a second website namespace.
- `--ranking-aggregation capped-sum-3` is safe as an opt-in option and can improve composite metrics at larger pools.

Challenges:

- Default promotion still rests on assistant-drafted labels.
- `capped_sum_3` is not uniformly better than `max` at the same pool; the best setting depends on whether Precision@5 or recall/composite is prioritized.
- Only two website domains have been evaluated so far.

## Recommended next action

Before changing defaults, decide whether website default ranking should optimize for:

1. `Precision@5` using page mode with a smaller pool; or
2. composite/recall using page mode with capped aggregation and a larger pool.

A separate follow-up owner tracks that promotion decision.
