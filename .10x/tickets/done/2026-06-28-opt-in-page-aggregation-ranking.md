Status: done
Created: 2026-06-28
Updated: 2026-06-28
Depends-On: .10x/evidence/2026-06-28-website-page-aggregation-experiments.md

# Opt-In Page Aggregation Ranking

## Scope

Implement production-facing, opt-in website page aggregation ranking after experiments showed `capped-sum-3` outperformed simple URL/page collapse on `site-turbopuffer-com-v1`.

Candidate interface:

```bash
--ranking-mode page --ranking-aggregation capped-sum-3 --ranking-pool 20
```

Defaults must remain unchanged unless separately approved.

## Acceptance criteria

- Add a validated ranking aggregation option for page/file ranking without changing existing defaults.
- Preserve repository default behavior and raw chunk mode.
- Unit tests cover `capped-sum-3`, default max behavior, invalid aggregation names, and repository grouping preservation.
- Live retrieval-only eval compares the new option against default and current page mode on `site-turbopuffer-com-v1`.
- Documentation clearly marks aggregation as opt-in/experimental.

## Blockers

- None for opt-in implementation. Product decision remains pending before any default promotion.

## References

- `.10x/evidence/2026-06-28-website-page-aggregation-experiments.md`
- `.10x/tickets/done/2026-06-28-website-page-aggregation-experiments.md`

## Progress and notes

- 2026-06-28: Opened as follow-up after page aggregation hypothesis passed both Precision@5 and composite targets.
- 2026-06-28: Activated after user instructed execution of the recommendation.
- 2026-06-28: Implemented `--ranking-aggregation max|capped-sum-3` for retrieve/evals/autoresearch options. Defaults remain unchanged (`max`).
- 2026-06-28: Added unit coverage for capped aggregation, default max behavior, invalid aggregation names, repo grouping preservation, and CLI dry-run parsing.
- 2026-06-28: Live retrieval-only eval on `site-turbopuffer-com-v1` reproduced the target result: `Precision@5 = 0.290`, `repo_search_score = 71.220` for `--ranking-mode page --ranking-profile none --ranking-pool 20 --ranking-aggregation capped-sum-3`. Evidence: `.10x/evidence/2026-06-28-opt-in-page-aggregation-ranking-validation.md`.

## Current State

Done. The option is implemented and validated; no defaults were changed.
