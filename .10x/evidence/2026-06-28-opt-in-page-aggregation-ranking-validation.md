Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/done/2026-06-28-opt-in-page-aggregation-ranking.md, .10x/evidence/2026-06-28-website-page-aggregation-experiments.md

# Opt-In Page Aggregation Ranking Validation

## What was observed

Implemented production-facing, opt-in page/file group aggregation for retrieval and evals.

New CLI option:

```bash
--ranking-aggregation max|capped-sum-3
```

Recommended experimental website invocation:

```bash
turbo-search evals \
  --live \
  --dataset src/turbo_search/data/turbopuffer_site_search_seed_evals.json \
  --namespace site-turbopuffer-com-v1 \
  --top-k 10 \
  --candidates 200 \
  --ranking-mode page \
  --ranking-profile none \
  --ranking-pool 20 \
  --ranking-aggregation capped-sum-3
```

Behavior:

- `ranking_aggregation=max` is the default and preserves previous ranking behavior.
- `ranking_aggregation=capped_sum_3` sums the top three reciprocal-rank contributions inside each page/file group.
- `ranking_mode=page` still groups repository rows by `repo_path`; website rows group by canonical URL.
- `ranking_mode=chunk` still returns raw fused chunk order.
- Defaults were not changed.

Changed files:

- `src/turbo_search/retriever.py`
- `src/turbo_search/cli.py`
- `src/turbo_search/evals.py`
- `src/turbo_search/autoresearch.py`
- `tests/test_retriever.py`
- `tests/test_cli.py`
- `README.md`
- `docs/generic-site-rag-plan-apply.md`
- `.10x/knowledge/repo-search-ranking-defaults.md`

## Validation commands

```bash
uv run python -m unittest tests.test_retriever tests.test_cli tests.test_autoresearch tests.test_evals
uv run python -m unittest discover tests
git diff --check
```

Observed:

```text
53 tests OK
130 tests OK
git diff --check: no whitespace errors
```

Unit coverage includes:

- default max aggregation preserving best-rank behavior;
- `capped_sum_3` rewarding multi-chunk page evidence;
- invalid aggregation names rejected by `RetrievalOptions`;
- repository rows continuing to group by `repo_path` under page mode and capped aggregation;
- CLI dry-run accepting `--ranking-aggregation capped-sum-3` without credentials or API calls.

## Live retrieval-only eval

Artifacts:

- `autoresearch/runs/opt-in-page-aggregation-ranking-20260628/default-file.json`
- `autoresearch/runs/opt-in-page-aggregation-ranking-20260628/page-max-pool20.json`
- `autoresearch/runs/opt-in-page-aggregation-ranking-20260628/page-capped-sum-3-pool20.json`
- `autoresearch/runs/opt-in-page-aggregation-ranking-20260628/summary.json`
- `autoresearch/runs/opt-in-page-aggregation-ranking-20260628/report.md`

Safety:

- live turbopuffer retrieval calls only;
- no live writes;
- no deletes or stale deletes;
- no namespace management;
- no state mutation.

Results on `site-turbopuffer-com-v1`:

| Variant | Mode | Profile | Pool | Aggregation | P@5 | Score | NDCG | Recall | MRR |
|---|---|---|---:|---|---:|---:|---:|---:|---:|
| default | file | repo_code | 100 | max | 0.200 | 59.734 | 0.681 | 0.483 | 0.708 |
| page max | page | none | 20 | max | 0.270 | 65.279 | 0.727 | 0.567 | 0.750 |
| page capped | page | none | 20 | capped_sum_3 | 0.290 | 71.220 | 0.804 | 0.567 | 0.850 |

The implemented opt-in option reproduced the experiment result:

```text
page-capped-sum-3-pool20
Precision@5: 0.290
repo_search_score: 71.220
```

## What this supports or challenges

Supports:

- The `capped-sum-3` aggregation can be safely exposed as an opt-in retrieval/eval option.
- The option improves the assistant-drafted turbopuffer.com website seed eval over both current default and simple page collapse.
- Repository grouping behavior is preserved by tests.

Challenges:

- This still should not become a default solely from one assistant-drafted website dataset.
- More websites or human-reviewed labels are needed before default promotion.

## Limits

The live eval is retrieval-only and uses small assistant-drafted labels. It is useful for directional ranking validation, not a production-grade quality guarantee.
