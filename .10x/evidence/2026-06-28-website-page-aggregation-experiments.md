Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/done/2026-06-28-website-page-aggregation-experiments.md, .10x/evidence/2026-06-28-website-page-level-ranking-validation.md

# Website Page Aggregation Experiments

## What was observed

Tested whether website pages should be ranked by aggregated multi-chunk evidence instead of simple URL/page collapse.

Namespace:

- `site-turbopuffer-com-v1`

Dataset:

- `src/turbo_search/data/turbopuffer_site_search_seed_evals.json`

The dataset is assistant-drafted and not human-approved ground truth.

No production defaults were changed. The experiment used live retrieval-only calls and local post-processing of raw chunk results. No writes, deletes, stale deletes, namespace management, or state mutation were run.

## Procedure

For each eval case, retrieved raw chunk-fused results with:

```text
ranking_mode=chunk
ranking_profile=none
max_pool=150
candidates in {100, 200, 400}
```

Then grouped hits by canonical page URL and tested aggregation formulas across pools `{20, 50, 100, 150}`:

- `max`: best chunk score only;
- `sum`: sum all page chunk RRF scores;
- `capped-sum-2`, `capped-sum-3`, `capped-sum-5`: sum only the best N chunk scores per page;
- `sqrt-count`: best chunk score multiplied by square root of page hit count;
- `max-boost-*`: best chunk score with small capped hit-count boosts;
- `sum-damped-*`: damped sum where later chunks contribute less.

Artifacts:

- `autoresearch/runs/website-page-aggregation-20260628/results.json`
- `autoresearch/runs/website-page-aggregation-20260628/report.md`

Whitespace validation:

```bash
git diff --check
```

Observed no whitespace errors.

## Baselines and targets

Current default:

```text
Precision@5: 0.200
repo_search_score: 59.734
```

Prior best page Precision@5 target:

```text
page-mode-pool20
Precision@5: 0.270
repo_search_score: 65.279
```

Prior best page composite target:

```text
page-mode-c100-pool100
Precision@5: 0.200
repo_search_score: 68.646
```

Success criteria were to beat either `Precision@5 > 0.270` or `repo_search_score > 68.646`.

## Results

The hypothesis passed.

Best Precision@5 variant:

```text
agg-capped-sum-3-best-rank-c200-p20
Precision@5: 0.290
repo_search_score: 71.220
NDCG@10: 0.804
Recall@10: 0.567
MRR@10: 0.850
```

This beats both prior targets:

- Precision@5: `0.270 -> 0.290`
- Composite score: `68.646 -> 71.220`

Best composite variant:

```text
agg-capped-sum-3-best-rank-c400-p150
Precision@5: 0.240
repo_search_score: 77.957
NDCG@10: 0.856
Recall@10: 0.750
MRR@10: 0.900
```

This strongly beats the prior composite target, though with lower Precision@5 than the pool-20 variant.

## Interpretation

Capped aggregation, especially `capped-sum-3`, is the strongest signal tested so far for `turbopuffer.com` website search. It improves ranking by rewarding pages with multiple matching chunks while avoiding unlimited dominance by long pages.

Pool size controls the tradeoff:

- Pool 20 produced the best Precision@5.
- Larger pools improved recall and composite score.

The representative selection mode did not change the measured URL-level metrics in this dataset because judgments are page-level and do not require section matches.

## What this supports or challenges

Supports:

- Website ranking should likely become page-level aggregation, not simple page collapse, after more validation.
- `capped-sum-3` is a good candidate formula for an experimental production option.
- The next production-facing option should expose formula/pool separately from default behavior.

Challenges:

- The best Precision@5 and best composite settings differ.
- Only one website namespace was tested.
- Labels remain assistant-drafted, so default promotion would be premature without either more websites or human-reviewed labels.

## Recommended next action

Implement an opt-in page aggregation option, likely:

```bash
--ranking-mode page --ranking-aggregation capped-sum-3 --ranking-pool 20
```

Do not change defaults yet. Validate the option with unit tests and repeat the live eval before asking whether to promote website defaults.
