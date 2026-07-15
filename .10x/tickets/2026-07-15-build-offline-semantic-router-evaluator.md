Status: open
Created: 2026-07-15
Updated: 2026-07-15
Parent: .10x/tickets/2026-07-15-semantic-routing-offline-pilot-plan.md
Depends-On: .10x/tickets/2026-07-15-build-offline-namespace-catalog-fixture.md, .10x/tickets/2026-07-15-build-controlled-taxonomy-fixture.md

# Build Offline Semantic Router Evaluator

## Scope

Implement deterministic exact-taxonomy, semantic-card, and equal-weight RRF hybrid routing; eligibility-first candidate handling; cached namespace-local evidence fusion; metric calculation; and focused tests governed by `.10x/specs/offline-semantic-routing-evaluation.md`.

Execute on branch `work/build-offline-semantic-router-evaluator` in its own worktree based on current `develop` after both dependencies are integrated.

## Acceptance criteria

- Reuse the integrated catalog and taxonomy models rather than duplicating them.
- Apply authorization, enabled state, and exact embedding compatibility before every strategy.
- Implement exact, semantic cosine, and hybrid `RRF_K = 60` strategies with deterministic tie-breaking.
- Accept injected/precomputed vectors; never initialize/download a model in tests.
- Preserve namespace-qualified evidence identity and fuse cached rankings without comparing raw scores.
- Produce per-case/split/aggregate routing, fan-out, safety, and downstream evidence metrics.
- Keep unauthorized namespace metadata out of route output/diagnostics.
- Add focused tests for every acceptance scenario, including repeatability.
- Run focused tests, full suite, and `git diff --check`.

## Explicit exclusions

- Pilot dataset conclusions, architecture promotion, CLI/API changes, live Turbopuffer, answer generation, learned routing, decomposition, concepts, ontology, or graphs.

## References

- `.10x/specs/offline-semantic-routing-evaluation.md`
- `.10x/specs/semantic-namespace-catalog-pilot.md`
- `.10x/specs/controlled-taxonomy-pilot.md`
- `.10x/tickets/2026-07-15-semantic-routing-offline-pilot-plan.md`

## Evidence expectations

Record changed files, deterministic strategy behavior, metric examples, focused/full tests, safety assertions, no-network proof, diff hygiene, and limits.

## Blockers

Depends on both fixture/model children being integrated into current `develop`.

## Progress and notes

- 2026-07-15: Ticket opened from the user-ratified offline pilot specification set. Execution deferred until dependencies close and integrate.
