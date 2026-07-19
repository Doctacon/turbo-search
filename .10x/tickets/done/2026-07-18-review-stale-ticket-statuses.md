Status: done
Created: 2026-07-18
Updated: 2026-07-19
Parent: .10x/tickets/2026-07-18-repository-cleanup-plan.md
Depends-On: .10x/tickets/done/2026-07-18-normalize-terminal-ticket-placement.md

# Review Stale Ticket Statuses

## Scope

Perform closure review—not implementation repair—of stale open/active/blocked tickets identified in `.10x/research/2026-07-18-repository-dead-end-inventory.md`:

- float16 embedding inference;
- single-pass plan and stage timing;
- cross-corpus validation basket;
- repo oversize source indexing;
- website capped aggregation default review;
- repo searchable path/symbol metadata;
- repo search heavy ranking experiments;
- conditional website replanning.

For each ticket, map existing acceptance criteria to existing evidence/reviews/source and choose only an evidence-supported disposition: close, cancel with durable no-action rationale, remain open/active, or block with a precise closure note. Do not create new verification evidence or repair implementation in this ticket.

## Acceptance criteria

- Read each ticket and every referenced governing/evidence/review record needed for closure.
- Check active spec coherence and material test/source assertions where semantic authority is relevant.
- Move only supported terminal tickets to terminal directories and repair references.
- Unsupported closure leaves the ticket open/blocked with exact missing evidence, review, retrospective, or spec-coherence requirements.
- Preserve unfinished work with a durable owner; do not conflate rejected hypotheses with failed implementation.
- Record one adversarial aggregate review with verdict and residual risk.

## Evidence expectations

Per-ticket acceptance mapping, disposition table, moved/reference map, unsupported-closure notes, and aggregate review.

## Blockers

None. Terminal placement normalization integrated at `9c78f09` before review execution.

## Explicit exclusions

Running new tests/benchmarks/live operations; fixing code; accepting residual risk; changing ranking or precision defaults; closing Node.js-action or retrieval-tag tickets.

## References

- `.10x/tickets/2026-07-18-repository-cleanup-plan.md`
- `.10x/research/2026-07-18-repository-dead-end-inventory.md`

## Progress and notes

- 2026-07-19: Read all eight named tickets and the governing specs, decisions, knowledge, evidence, and reviews needed for closure. Narrowly inspected material current float16 and single-pass source/tests for the spec-drift gate; ran no tests, benchmarks, or live operations.
- 2026-07-19: Disposed five tickets as `done`, cancelled two with explicit evidence-backed no-action rationales, and kept the heavy-ranking umbrella active with exact missing terminal support. Node.js-action and retrieval-tag tickets remained out of scope.
- 2026-07-19: Aggregate adversarial review passed: `.10x/reviews/2026-07-19-stale-ticket-status-closure-review.md`.
- 2026-07-19: Read-only graph validation found 1,809 existing current references, six valid commit-qualified historical references, zero missing current/commit references, zero top-level terminal statuses, zero terminal-directory status errors, and zero stale moved-path references. Changed paths are `.10x` Markdown only and `git diff --check` passes.
- 2026-07-19: Follow-up review corrected the cross-corpus graph edge: the active namespace-ranking decision remains its dependency, while the independently completed basket now references the active heavy-ranking umbrella as downstream context/evidence rather than treating that umbrella as a prerequisite. No disposition or historical result changed.

## Disposition table

| Ticket | Disposition |
|---|---|
| `.10x/tickets/done/2026-07-13-float16-embedding-inference.md` | done |
| `.10x/tickets/done/2026-07-14-single-pass-plan-and-stage-timing.md` | done |
| `.10x/tickets/done/2026-06-28-cross-corpus-validation-basket.md` | done |
| `.10x/tickets/cancelled/2026-06-28-repo-oversize-source-indexing.md` | cancelled/no action; `done` unsupported |
| `.10x/tickets/done/2026-06-28-website-capped-aggregation-default-review.md` | done |
| `.10x/tickets/done/2026-06-28-repo-searchable-path-symbol-metadata.md` | done |
| `.10x/tickets/2026-06-28-repo-search-heavy-ranking-experiments.md` | remains active |
| `.10x/tickets/cancelled/2026-07-14-conditional-website-replanning.md` | cancelled/no action |

## Moved/reference map

- Five supported `done` tickets moved from `.10x/tickets/` to `.10x/tickets/done/`.
- Two supported `cancelled` tickets moved from `.10x/tickets/` to `.10x/tickets/cancelled/`.
- This completed review ticket moved to `.10x/tickets/done/`.
- All affected `.10x` Markdown references were updated to their terminal paths.

## Unsupported closures

- Repo oversize source indexing cannot be marked `done`: existing evidence covers pytest/Typer rather than the full then-current basket and does not contain an explicit binary/vendor/generated-noise audit. Cancellation preserves the opt-in result and rejects global promotion.
- Repo search heavy ranking cannot be terminal: named code-aware embedding, syntax-aware chunking, learning-to-rank, and routed-selector/profile outcomes lack completion evidence or explicit no-action authority.

## Closure mapping

- Every target acceptance criterion is mapped in `.10x/reviews/2026-07-19-stale-ticket-status-closure-review.md` and summarized in each updated ticket.
- Terminal moves and reference repair are bounded to supported dispositions.
- Unsupported work retains a durable active owner or an explicit evidence-backed no-action rationale.
- No new verification evidence, implementation repair, default change, risk acceptance, test, benchmark, or live operation occurred.
- Graph/status/diff validation is recorded in this ticket's final progress entry before commit.

## Retrospective

Status staleness had two distinct causes: completed bounded experiments whose no-promotion conclusion was itself success, and broad umbrellas whose named remaining scope still lacked authority for terminal disposition. Future experiment tickets should state whether a failed promotion gate completes the ticket and should avoid mixing implemented defaults, rejected hypotheses, and unimplemented selector work under one indefinite owner.
