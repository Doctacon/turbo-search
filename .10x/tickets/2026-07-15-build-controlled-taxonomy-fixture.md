Status: open
Created: 2026-07-15
Updated: 2026-07-15
Parent: .10x/tickets/2026-07-15-semantic-routing-offline-pilot-plan.md
Depends-On: None

# Build Controlled Taxonomy Fixture

## Scope

Implement the flat pilot taxonomy model, JSON loader/validation, deterministic exact label/synonym matching, and focused tests governed by `.10x/specs/controlled-taxonomy-pilot.md`.

Execute on branch `work/build-controlled-taxonomy-fixture` in its own worktree based on current `develop`.

## Acceptance criteria

- Add the minimum typed Python taxonomy/term model and loader.
- Reject duplicate IDs, labels, cross-term synonyms, empty values, and self-synonyms after normalization.
- Implement deterministic complete-phrase label/synonym matching with explainable term IDs and phrases.
- Keep ACL groups structurally separate and prove taxonomy terms grant no access.
- Ensure semantic scores cannot mutate governed assignments.
- Add focused tests for every acceptance scenario in the specification.
- Run focused tests, full suite, and `git diff --check`.

## Explicit exclusions

- Hierarchies, ontology, open-set/LLM tagging, production stewardship, public tag output/filter behavior, live writes, routing fusion, or graphs.

## References

- `.10x/specs/controlled-taxonomy-pilot.md`
- `.10x/tickets/2026-07-15-reconcile-retrieval-tag-output.md`
- `.10x/tickets/2026-07-15-semantic-routing-offline-pilot-plan.md`

## Evidence expectations

Record changed files, normalization/matching rules, focused/full test results, proof of no network/external mutation, and limits.

## Blockers

None.

## Progress and notes

- 2026-07-15: Ticket opened from the user-ratified offline pilot specification set. Execution deferred from the specification-authoring turn.
