Status: open
Created: 2026-07-15
Updated: 2026-07-15
Parent: .10x/tickets/2026-07-15-semantic-routing-offline-pilot-plan.md
Depends-On: None

# Build Offline Namespace Catalog Fixture

## Scope

Implement the pilot-only catalog model, JSON loader/validation, eligibility gates, deterministic namespace-card generation, and focused tests governed by `.10x/specs/semantic-namespace-catalog-pilot.md`.

Execute on branch `work/build-offline-namespace-catalog-fixture` in its own worktree based on current `develop`.

## Acceptance criteria

- Add the minimum typed Python model and loader needed for the active catalog specification.
- Validate every required field, identity/reference constraint, synthetic ACL rule, compatibility tuple, and enabled state.
- Generate deterministic cards with catalog/revision provenance.
- Ensure unauthorized metadata never enters returned candidate/result diagnostics.
- Use temporary/in-memory storage only; add no dependency.
- Add colocated focused tests for every acceptance scenario in the specification.
- Run focused tests, full test suite, and `git diff --check`.

## Explicit exclusions

- Taxonomy matching beyond validating supplied tag IDs.
- Routing/scoring/evaluation strategy.
- CLI/API changes, live Turbopuffer, model loading, production persistence, Data Vault, concepts, or graph behavior.

## References

- `.10x/specs/semantic-namespace-catalog-pilot.md`
- `.10x/decisions/data-vault-is-analogy-not-architecture.md`
- `.10x/tickets/2026-07-15-semantic-routing-offline-pilot-plan.md`

## Evidence expectations

Record changed files, exact fixture/model contract, focused/full test commands and results, network/credential absence, diff hygiene, and limits.

## Blockers

None.

## Progress and notes

- 2026-07-15: Ticket opened from the user-ratified offline pilot specification set. Execution deferred from the specification-authoring turn.
