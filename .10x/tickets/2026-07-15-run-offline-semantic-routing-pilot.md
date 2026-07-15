Status: open
Created: 2026-07-15
Updated: 2026-07-15
Parent: .10x/tickets/2026-07-15-semantic-routing-offline-pilot-plan.md
Depends-On: .10x/tickets/2026-07-15-build-offline-semantic-router-evaluator.md

# Run Offline Semantic Routing Pilot

## Scope

Create the fixed synthetic catalog, taxonomy, deterministic vectors, development/held-out routing cases, and cached namespace-local evidence required by the active specifications; run all routing strategies; record reproducible evidence and a bounded research synthesis.

Execute on branch `work/run-offline-semantic-routing-pilot` in its own worktree based on current `develop` after the evaluator dependency is integrated.

## Acceptance criteria

- Fixtures cover every scenario required by all three active pilot specifications without encoding real users, secrets, or proprietary data.
- Held-out cases are identified before execution and are not used to tune card text, vectors, taxonomy, route limits, or fusion.
- Exact, semantic-card, and hybrid strategies run with identical eligibility gates, route limits, cached evidence, and compatibility contracts.
- Record per-case and aggregate required-namespace recall, selected precision, over-selection, fan-out, forbidden/incompatible selection counts, and downstream evidence recall.
- Safety failures are reported exactly and never hidden by averages.
- Repeat execution proves byte-for-byte deterministic results.
- Create durable evidence and a research synthesis that states findings, contradictions, limits, and the smallest justified next action.
- Do not activate architecture, create implementation specs, or close the parent without user review.
- Run focused tests, full suite, diff checks, and independent review.

## Explicit exclusions

- Real namespaces or ACLs, network, credentials, Turbopuffer SDK/API calls, model downloads, hosted APIs, live evals/writes, answer generation, production infrastructure, Data Vault, graph database, concept extraction, ontology, or graph traversal.

## References

- `.10x/specs/offline-semantic-routing-evaluation.md`
- `.10x/specs/semantic-namespace-catalog-pilot.md`
- `.10x/specs/controlled-taxonomy-pilot.md`
- `.10x/tickets/2026-07-15-semantic-routing-offline-pilot-plan.md`

## Evidence expectations

Record fixture revisions, immutable case inventory/splits, command outputs, per-case and aggregate metrics, deterministic rerun digest, validation commands, independent review, no-network/external-side-effect confirmation, and limits.

## Blockers

Depends on the evaluator child being closed and integrated into current `develop`.

## Progress and notes

- 2026-07-15: Ticket opened from the user-ratified offline pilot specification set. Execution deferred until dependency closure.
