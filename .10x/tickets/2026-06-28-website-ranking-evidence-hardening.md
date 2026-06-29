Status: done
Created: 2026-06-28
Updated: 2026-06-28
Depends-On: .10x/evidence/2026-06-28-website-page-ranking-default-promotion-validation.md

# Website Ranking Evidence Hardening

## Scope

Harden evidence for the promoted website page-ranking default without changing defaults.

Work includes:

- Add one more existing indexed website namespace to the validation set if available.
- Draft a source-backed seed eval dataset for that site with page-level judgments and `human_approved_ground_truth=false`.
- Run live retrieval-only evals comparing the promoted default and capped aggregation where useful.
- Summarize whether the promoted default still holds across three websites.

No indexing, live writes, stale deletes, namespace deletion/replacement, or state mutation are in scope.

## Acceptance criteria

- Uses an existing applied `site-*` namespace only.
- New eval dataset loads through the eval harness.
- Live retrieval-only evidence compares default website ranking against at least one relevant opt-in variant.
- Cross-site evidence summary includes turbopuffer.com, SQLMesh, and the new site.
- Existing unit tests and `git diff --check` pass.
- Records clearly state labels are assistant-drafted, not human-approved.

## Blockers

- None. User instructed evidence hardening.

## References

- `.10x/evidence/2026-06-28-website-page-ranking-default-promotion-validation.md`
- `.turbo-search/state/pi-dev/site-pi-dev-v1/last-applied.json`
- `artifacts/site-crawls/pi-dev-plan/summary.json`

## Progress and notes

- 2026-06-28: Activated after user requested evidence hardening.
- 2026-06-28: Added `src/turbo_search/data/pi_site_search_seed_evals.json` with 10 source-backed, assistant-drafted page-level judgments for `site-pi-dev-v1`.
- 2026-06-28: Ran live retrieval-only evals on `site-pi-dev-v1`. Promoted website default improved Precision@5 from `0.220` to `0.333` and score from `82.624` to `88.398` versus legacy file default. Evidence: `.10x/evidence/2026-06-28-website-ranking-evidence-hardening.md`.

## Current State

Done. Website page-ranking default is now supported by three assistant-drafted website eval sets; labels remain not human-approved.
