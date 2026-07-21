Status: cancelled
Created: 2026-06-28
Updated: 2026-06-28
Depends-On: .10x/evidence/2026-06-28-website-ranking-evidence-hardening.md

# Human Review Website Ranking Labels

## Scope

Human-review the assistant-drafted website ranking eval labels before future default changes or heavier tuning.

Datasets needing review:

- `src/turbo_search/data/turbopuffer_site_search_seed_evals.json`
- `src/turbo_search/data/sqlmesh_site_search_seed_evals.json`
- `src/turbo_search/data/pi_site_search_seed_evals.json`

## Acceptance criteria

- Each eval question and judgment is reviewed against the source page.
- Incorrect, ambiguous, or overly broad judgments are corrected or removed.
- `human_approved_ground_truth` is set only after actual human approval.
- A review/evidence record documents reviewer, date, changed labels, and remaining limitations.
- No ranking defaults are changed in this ticket.

## Blockers

- Cancelled by user direction. On 2026-06-28, the user stated they trust assistant judgment, do not need human review, and prefer more hypotheses, tests, and repo search score improvements.

## References

- `.10x/evidence/2026-06-28-website-ranking-evidence-hardening.md`

## Progress and notes

- 2026-06-28: Opened after evidence hardening established three assistant-drafted website eval sets but left human approval unresolved.
- 2026-06-28: Cancelled after explicit user direction to skip human review and focus on more hypotheses/tests and repo search score improvements.
