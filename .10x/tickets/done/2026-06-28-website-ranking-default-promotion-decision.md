Status: done
Created: 2026-06-28
Updated: 2026-06-28
Depends-On: .10x/evidence/2026-06-28-opt-in-page-aggregation-ranking-validation.md, .10x/evidence/2026-06-28-cross-site-page-aggregation-sqlmesh-validation.md

# Website Ranking Default Promotion Decision

## Scope

Decide whether to promote a website-specific page ranking default after validation on `site-turbopuffer-com-v1` and `site-sqlmesh-readthedocs-io-v1`.

Candidate defaults:

1. Precision-oriented:
   ```text
   ranking_mode = page
   ranking_profile = none
   ranking_pool = 20
   ranking_aggregation = max or capped_sum_3
   ```
2. Composite/recall-oriented:
   ```text
   ranking_mode = page
   ranking_profile = none
   ranking_pool = 100 or 150
   ranking_aggregation = capped_sum_3
   ```

Defaults must not change until the optimization target and evidence threshold are ratified.

## Acceptance criteria

- Clarify whether website defaults optimize primarily for Precision@5 or composite/recall.
- Compare validated results from turbopuffer.com and SQLMesh side by side.
- Decide whether assistant-drafted labels are sufficient for promotion or whether human-reviewed labels / one more website are required.
- If promotion is approved, open a bounded implementation ticket for default selection/source-kind routing and tests.

## Blockers

- None. User ratified precision-oriented website default promotion with `page/none/pool20/max` despite assistant-drafted labels.

## References

- `.10x/evidence/2026-06-28-opt-in-page-aggregation-ranking-validation.md`
- `.10x/evidence/2026-06-28-cross-site-page-aggregation-sqlmesh-validation.md`

## Progress and notes

- 2026-06-28: Opened after cross-site validation showed page ranking generalizes, while capped aggregation benefits vary by pool/site.
- 2026-06-28: User approved promotion with “yup, send it”. Decision recorded in `.10x/decisions/superseded/website-ranking-defaults.md`.
- 2026-06-28: Implementation owner opened: `.10x/tickets/done/2026-06-28-promote-website-page-ranking-default.md`.

## Current State

Done. Promotion decision completed; implementation tracked separately.
