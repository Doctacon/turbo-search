Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/2026-06-28-website-ranking-evidence-hardening.md, .10x/evidence/2026-06-28-website-page-ranking-default-promotion-validation.md

# Website Ranking Evidence Hardening

## What was observed

Added a third existing indexed website namespace to validate the promoted website ranking default:

- `site-pi-dev-v1`

Existing applied state:

- `.turbo-search/state/pi-dev/site-pi-dev-v1/last-applied.json`

Added assistant-drafted seed eval dataset:

- `src/turbo_search/data/pi_site_search_seed_evals.json`

The new dataset is source-backed from existing `artifacts/site-crawls/pi-dev-plan/pages/*.md` pages, but it is **not human-approved ground truth**.

Safety:

- live turbopuffer retrieval calls only;
- no live writes;
- no stale deletes;
- no namespace deletion/replacement/management;
- no state mutation;
- no new indexing.

## Procedure

Validated the new dataset loads:

```bash
uv run python - <<'PY'
from pathlib import Path
from turbo_search.evals import load_eval_cases
load_eval_cases(Path('src/turbo_search/data/pi_site_search_seed_evals.json'))
PY
```

Ran live retrieval-only evals on `site-pi-dev-v1`:

```bash
uv run turbo-search evals \
  --live \
  --dataset src/turbo_search/data/pi_site_search_seed_evals.json \
  --namespace site-pi-dev-v1 \
  --top-k 10 \
  --candidates 200

uv run turbo-search evals \
  --live \
  --dataset src/turbo_search/data/pi_site_search_seed_evals.json \
  --namespace site-pi-dev-v1 \
  --top-k 10 \
  --candidates 200 \
  --ranking-mode file \
  --ranking-profile repo-code \
  --ranking-pool 100 \
  --ranking-aggregation max

uv run turbo-search evals \
  --live \
  --dataset src/turbo_search/data/pi_site_search_seed_evals.json \
  --namespace site-pi-dev-v1 \
  --top-k 10 \
  --candidates 200 \
  --ranking-mode page \
  --ranking-profile none \
  --ranking-pool 20 \
  --ranking-aggregation capped-sum-3
```

Also checked a larger capped aggregation variant:

```bash
uv run turbo-search evals \
  --live \
  --dataset src/turbo_search/data/pi_site_search_seed_evals.json \
  --namespace site-pi-dev-v1 \
  --top-k 10 \
  --candidates 400 \
  --ranking-mode page \
  --ranking-profile none \
  --ranking-pool 150 \
  --ranking-aggregation capped-sum-3
```

Artifacts:

- `autoresearch/runs/evidence-hardening-pi-site-20260628/summary.json`
- `autoresearch/runs/evidence-hardening-pi-site-20260628/report.md`
- per-variant JSON files in the same directory.

Validation commands:

```bash
uv run python -m unittest tests.test_evals tests.test_cli tests.test_retriever tests.test_autoresearch
uv run python -m unittest discover tests
git diff --check
```

Observed:

```text
56 tests OK
133 tests OK
git diff --check: no whitespace errors
```

## pi.dev results

| Variant | Candidates | Mode | Pool | Aggregation | P@5 | ΔP@5 | Score | ΔScore | NDCG | Recall | MRR |
|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| legacy-file-default | 200 | file | 100 | max | 0.220 | +0.000 | 82.624 | +0.000 | 0.935 | 0.700 | 1.000 |
| default-page-max-pool20 | 200 | page | 20 | max | 0.333 | +0.113 | 88.398 | +5.774 | 0.965 | 0.850 | 1.000 |
| page-capped-sum-3-pool20 | 200 | page | 20 | capped_sum_3 | 0.333 | +0.113 | 88.204 | +5.580 | 0.961 | 0.850 | 1.000 |
| page-capped-sum-3-c400-pool150 | 400 | page | 150 | capped_sum_3 | 0.340 | +0.120 | 90.787 | +8.163 | 0.971 | 0.950 | 1.000 |

## Cross-site summary

Validated website default: `page / none / pool20 / max`.

| Site | Legacy file P@5 | Default page P@5 | ΔP@5 | Legacy score | Default score | ΔScore |
|---|---:|---:|---:|---:|---:|---:|
| turbopuffer.com | 0.200 | 0.270 | +0.070 | 59.734 | 65.279 | +5.545 |
| SQLMesh | 0.260 | 0.473 | +0.213 | 84.484 | 87.460 | +2.975 |
| pi.dev | 0.220 | 0.333 | +0.113 | 82.624 | 88.398 | +5.774 |

## Interpretation

The evidence hardening result strengthens the promoted website default:

- The page/max/pool20 default improved Precision@5 and composite score on a third site.
- Capped aggregation remains useful but still does not clearly replace max as the precision-oriented default:
  - on pi.dev, capped-sum-3 at pool 20 matched Precision@5 but slightly reduced composite vs max;
  - larger capped-sum-3 improved recall/composite but changes the precision-vs-recall tradeoff.

The current default remains justified:

```text
site-* default = page / none / pool20 / max
```

## Limits

All website eval datasets remain assistant-drafted. They are source-backed and human-reviewable, but not human-approved ground truth. The next hardening step should be human review or adversarial label review rather than more automatic tuning.
