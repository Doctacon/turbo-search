Status: done
Created: 2026-06-28
Updated: 2026-07-19
Depends-On: .10x/evidence/2026-06-28-cross-corpus-live-retrieval-evals.md, .10x/evidence/2026-06-28-website-page-aggregation-experiments.md, .10x/evidence/2026-06-28-cross-site-page-aggregation-sqlmesh-validation.md, .10x/evidence/2026-06-28-repo-role-diversification-validation.md

# Website Capped Aggregation Default Review

## Scope

Review whether website namespaces should promote page-level `capped_sum_3` aggregation instead of the current `max` aggregation.

Expanded Ruff and Typer site evals improved with `page / none / pool20 / capped_sum_3`, but prior Pi-site evidence showed a tiny score regression at pool 20 while P@5 was unchanged. The user-selected promotion policy is no meaningful regressions, so default promotion requires resolving whether that prior regression is meaningful, stale, or acceptable.

## Acceptance criteria

- Compare `page/max/pool20` vs `page/capped_sum_3/pool20` across all current website validation namespaces: turbopuffer, SQLMesh, Pi, Ruff docs, and Typer docs.
- Use live retrieval-only evals; no writes, deletes, apply, stale cleanup, or namespace deletion.
- Record per-site P@5, composite score, recall, NDCG, MRR, and deltas.
- Apply the selected no-regression policy before any default change.
- If promotion is justified, update the namespace-ranking decision, docs, tests, and evidence in a separate implementation slice.

## Explicit exclusions

- No repo ranking changes.
- No website reindexing or live apply.
- No stale deletion or namespace deletion.

## Blockers

None. The recorded retrieval-only comparison was explicitly approved and completed.

## References

- `.10x/evidence/2026-06-28-cross-corpus-live-retrieval-evals.md`
- `.10x/decisions/namespace-ranking-defaults.md`

## Progress and notes

- 2026-06-28: Opened after expanded Ruff/Typer docs evals improved with capped aggregation while existing Pi-site evidence prevents automatic promotion under no-regression policy.
- 2026-06-28: Tested `adaptive_sum_3` against max and capped across turbopuffer, SQLMesh, Pi, Ruff docs, and Typer docs. Adaptive regressed turbopuffer composite score; capped still regressed Pi slightly. Website default remains `page/none/pool20/max` under no-regression policy. Evidence: `.10x/evidence/2026-06-28-website-adaptive-aggregation-review.md`.
- 2026-07-19: Closure review mapped the five criteria to the existing five-site evidence and active namespace-ranking decision. The no-regression gate correctly prevented a default change, so the conditional implementation criterion is not applicable. Review: `.10x/reviews/2026-07-19-stale-ticket-status-closure-review.md`.

## Closure mapping

- Five-site max/adaptive/capped comparison and retrieval-only safety: `.10x/evidence/2026-06-28-website-adaptive-aggregation-review.md`.
- Per-site P@5, composite score, recall, NDCG, MRR, and deltas: results table in that evidence.
- No-regression policy and unchanged website default: `.10x/decisions/namespace-ranking-defaults.md` plus the evidence conclusion.
- Separate promotion slice: not applicable because capped regressed Pi and adaptive regressed turbopuffer; no promotion was justified.

## Retrospective

Average-score leadership was insufficient for promotion. The existing five-site comparison shows why per-target no-regression matters: capped won on average but regressed Pi, while adaptive avoided the Pi regression yet regressed turbopuffer.
