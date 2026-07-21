Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/done/2026-06-28-website-capped-aggregation-default-review.md, .10x/research/2026-06-28-expanded-validation-ranking-hypotheses.md, .10x/decisions/namespace-ranking-defaults.md

# Website Adaptive Aggregation Review

## What was observed

Tested expanded-validation hypothesis H6: website `adaptive_sum_3` might capture `capped_sum_3` gains while avoiding the previous Pi-site capped regression.

Live retrieval-only evals compared these page-ranking variants across all current website validation namespaces:

```text
page / none / pool20 / max
page / none / pool20 / adaptive_sum_3
page / none / pool20 / capped_sum_3
```

No writes, deletes, apply, stale cleanup, namespace deletion, or state mutation occurred.

## Procedure

For each site dataset/namespace pair:

```bash
uv run turbo-search evals --live --dataset <dataset> --namespace <namespace> \
  --top-k 10 --candidates 200 \
  --ranking-mode page --ranking-profile none --ranking-pool 20 \
  --ranking-aggregation max --json

uv run turbo-search evals --live --dataset <dataset> --namespace <namespace> \
  --top-k 10 --candidates 200 \
  --ranking-mode page --ranking-profile none --ranking-pool 20 \
  --ranking-aggregation adaptive-sum-3 --json

uv run turbo-search evals --live --dataset <dataset> --namespace <namespace> \
  --top-k 10 --candidates 200 \
  --ranking-mode page --ranking-profile none --ranking-pool 20 \
  --ranking-aggregation capped-sum-3 --json
```

Artifacts:

- `autoresearch/runs/website-adaptive-aggregation-20260628/summary.json`
- `autoresearch/runs/website-adaptive-aggregation-20260628/report.md`
- Per-site JSON result files under `autoresearch/runs/website-adaptive-aggregation-20260628/`.

## Results

| Site | Variant | P@5 | Score | Delta score vs max | Recall | NDCG | MRR |
|---|---|---:|---:|---:|---:|---:|---:|
| turbopuffer | max | 0.270 | 65.279 | +0.000 | 0.567 | 0.727 | 0.750 |
| turbopuffer | adaptive | 0.290 | 63.262 | -2.017 | 0.567 | 0.701 | 0.700 |
| turbopuffer | capped | 0.290 | 71.220 | +5.941 | 0.567 | 0.804 | 0.850 |
| SQLMesh | max | 0.473 | 87.460 | +0.000 | 0.750 | 0.959 | 1.000 |
| SQLMesh | adaptive | 0.473 | 87.460 | +0.000 | 0.750 | 0.959 | 1.000 |
| SQLMesh | capped | 0.473 | 87.460 | +0.000 | 0.750 | 0.959 | 1.000 |
| Pi | max | 0.333 | 88.398 | +0.000 | 0.850 | 0.965 | 1.000 |
| Pi | adaptive | 0.333 | 88.493 | +0.094 | 0.850 | 0.967 | 1.000 |
| Pi | capped | 0.333 | 88.204 | -0.194 | 0.850 | 0.961 | 1.000 |
| Ruff | max | 0.577 | 87.691 | +0.000 | 0.867 | 0.902 | 1.000 |
| Ruff | adaptive | 0.577 | 88.816 | +1.124 | 0.867 | 0.922 | 1.000 |
| Ruff | capped | 0.577 | 89.225 | +1.534 | 0.867 | 0.930 | 1.000 |
| Typer docs | max | 0.493 | 73.690 | +0.000 | 0.625 | 0.764 | 0.950 |
| Typer docs | adaptive | 0.513 | 74.043 | +0.353 | 0.625 | 0.767 | 0.950 |
| Typer docs | capped | 0.513 | 74.540 | +0.850 | 0.625 | 0.776 | 0.950 |

Averages:

| Variant | Avg P@5 | Avg score |
|---|---:|---:|
| max | 0.429 | 80.504 |
| adaptive | 0.437 | 80.415 |
| capped | 0.437 | 82.130 |

## What this supports or challenges

Supports:

- `capped_sum_3` remains the best website aggregation by average score across the five-site basket.
- `adaptive_sum_3` improves Pi, Ruff, and Typer docs and ties SQLMesh.

Challenges:

- `adaptive_sum_3` regresses turbopuffer composite score versus `max` (`65.279 -> 63.262`), even though P@5 improves.
- `capped_sum_3` still regresses Pi-site composite score slightly versus `max` (`88.398 -> 88.204`) while P@5 is unchanged.

## Conclusion

H6 fails under the selected no-regression policy. Keep website default unchanged:

```text
site-* = page / none / pool20 / max
```

`capped_sum_3` remains promising for average-score optimization, but cannot be promoted while the no-regression policy is active unless the Pi-site delta is accepted as non-meaningful or resolved by a different formula.
