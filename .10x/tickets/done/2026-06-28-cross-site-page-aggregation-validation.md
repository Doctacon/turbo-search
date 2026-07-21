Status: done
Created: 2026-06-28
Updated: 2026-06-28
Depends-On: .10x/evidence/2026-06-28-opt-in-page-aggregation-ranking-validation.md

# Cross-Site Page Aggregation Validation

## Scope

Validate the opt-in `--ranking-mode page --ranking-aggregation capped-sum-3` website ranking on an existing indexed website namespace other than `site-turbopuffer-com-v1`.

Use existing applied namespaces only. Do not run new indexing, live writes, stale deletes, namespace deletion, or namespace replacement.

## Acceptance criteria

- Identify an existing indexed website namespace suitable for live retrieval-only validation.
- Add an assistant-drafted seed eval dataset for that site with clear page-level judgments.
- Run live retrieval-only evals comparing current default, page max, and page capped-sum-3.
- Record whether capped-sum-3 generalizes beyond `turbopuffer.com`.
- Preserve defaults; do not promote website defaults.

## Blockers

- None for live retrieval-only validation; user selected cross-site validation and instructed execution.
- Labels remain assistant-drafted unless separately reviewed by a human/domain owner.

## References

- `.10x/evidence/2026-06-28-opt-in-page-aggregation-ranking-validation.md`
- `.turbo-search/state/sqlmesh-readthedocs-io/site-sqlmesh-readthedocs-io-v1/last-applied.json`
- `artifacts/site-crawls/sqlmesh-readthedocs-io-plan/summary.json`

## Progress and notes

- 2026-06-28: Activated after user selected cross-site validation and instructed execution.
- 2026-06-28: Existing indexed candidate selected: `site-sqlmesh-readthedocs-io-v1` from `https://sqlmesh.readthedocs.io/en/stable/`.
- 2026-06-28: Added assistant-drafted SQLMesh seed eval dataset at `src/turbo_search/data/sqlmesh_site_search_seed_evals.json`.
- 2026-06-28: Ran live retrieval-only evals. Page mode pool 20 improved SQLMesh Precision@5 from `0.260` to `0.473` and score from `84.484` to `87.460`. Capped aggregation matched max at pool 20 and improved composite at larger pools. Evidence: `.10x/evidence/2026-06-28-cross-site-page-aggregation-sqlmesh-validation.md`.

## Current State

Done. Cross-site validation supports page-level website ranking; default promotion remains a separate decision tracked by `.10x/tickets/done/2026-06-28-website-ranking-default-promotion-decision.md`.
