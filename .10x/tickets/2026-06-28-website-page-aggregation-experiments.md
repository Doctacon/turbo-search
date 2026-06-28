Status: active
Created: 2026-06-28
Updated: 2026-06-28
Depends-On: .10x/evidence/2026-06-28-website-page-level-ranking-validation.md

# Website Page Aggregation Experiments

## Scope

Test whether website pages should be ranked by aggregated multi-chunk evidence instead of simple URL/page collapse.

Hypothesis: for website search, ranking pages by aggregated evidence from multiple matching chunks improves Precision@5 and/or composite score over simple page collapse.

## Acceptance criteria

- Run retrieval-only experiments on `site-turbopuffer-com-v1` without writes, deletes, namespace management, or state mutation.
- Compare aggregation variants against current default and prior page-ranking baselines.
- Record whether any variant beats `Precision@5 > 0.270` or `repo_search_score > 68.646` on the assistant-drafted turbopuffer.com seed eval.
- Do not change production defaults.
- If a production option is implemented later, add tests before promotion.

## Blockers

- None for experiment execution.
- Website labels remain assistant-drafted and not human-approved ground truth.

## References

- `.10x/evidence/2026-06-28-website-page-level-ranking-validation.md`
- `src/turbo_search/data/turbopuffer_site_search_seed_evals.json`

## Progress and notes

- 2026-06-28: Activated after user instructed execution of the page-level aggregation hypothesis.
