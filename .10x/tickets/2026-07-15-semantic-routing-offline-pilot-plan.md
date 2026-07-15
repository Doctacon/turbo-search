Status: open
Created: 2026-07-15
Updated: 2026-07-15
Parent: None
Depends-On: None

# Semantic Routing Offline Pilot Plan

## Plan outcome

Build and run the smallest local pilot that can test whether a semantic namespace catalog and controlled taxonomy improve namespace selection and downstream cached evidence retrieval over exact-only routing, without Turbopuffer calls, hosted APIs, production infrastructure, or a knowledge graph.

This is a parent plan, not an executable ticket.

## Governing records

- `.10x/decisions/data-vault-is-analogy-not-architecture.md`
- `.10x/specs/semantic-namespace-catalog-pilot.md`
- `.10x/specs/controlled-taxonomy-pilot.md`
- `.10x/specs/offline-semantic-routing-evaluation.md`
- `.10x/research/2026-07-15-data-vault-namespace-catalog-routing.md`
- `.10x/research/2026-07-15-data-vault-governed-tagging-filtering.md`
- `.10x/research/2026-07-15-data-vault-multi-hop-global-retrieval.md`
- `.10x/research/2026-07-15-data-vault-concept-graph.md`

## Ratified direction

The user approved the recommended next phase:

1. namespace cards with source, tags, compatibility, eligibility, and synthetic access metadata;
2. a small controlled taxonomy;
3. offline comparison of exact, semantic-card, and hybrid routing;
4. evaluation of namespace recall/precision, false exclusion, fan-out, downstream evidence, and ACL safety;
5. no graph work unless cheaper approaches leave a measured gap.

Data Vault remains analogy only. No Data Vault component is introduced.

## Child sequence

1. `.10x/tickets/2026-07-15-build-offline-namespace-catalog-fixture.md`
2. `.10x/tickets/2026-07-15-build-controlled-taxonomy-fixture.md`
3. `.10x/tickets/2026-07-15-build-offline-semantic-router-evaluator.md`
4. `.10x/tickets/2026-07-15-run-offline-semantic-routing-pilot.md`

Children 1 and 2 are independent and may run in parallel in separate worktrees. Child 3 depends on both. Child 4 depends on child 3 and owns the fixed pilot cases, execution, evidence, and results checkpoint.

## Aggregate acceptance criteria

- The catalog, taxonomy, and evaluator satisfy their focused active specifications.
- Every implementation child is independently reviewed and validated before integration.
- The pilot runs from deterministic committed fixtures with no network or credentials.
- Exact, semantic-card, and hybrid strategies run against identical eligible candidates and held-out cases.
- The report includes per-case and aggregate routing/evidence metrics plus exact safety-failure counts.
- No Turbopuffer SDK construction, live retrieval/write, hosted API, model download, Data Vault, graph database, concept extraction, or production persistence occurs.
- The result is an evidence checkpoint, not an automatic architecture promotion.

## Integration points

- Existing `RRF_K = 60` and namespace-qualified cross-namespace identity.
- Existing Python 3.11+ package and colocated test conventions.
- Existing DuckDB dependency MAY support temporary local relational checks but is not required as production authority.
- Current explicit multi-namespace retrieval remains unchanged.

## Blockers

None for the bounded offline pilot. Production catalog semantics, real ACLs, public tag behavior, live namespace routing, concept/ontology design, graphs, and promotion thresholds remain explicitly out of scope and blocked on pilot evidence plus later user ratification.

## Progress and notes

- 2026-07-15: User approved synthesis into focused specifications and an executable offline-pilot plan using local fixtures, exact/semantic/hybrid routing, current RRF baseline, and no graph or production infrastructure.
- 2026-07-15: Focused specification set and four bounded child tickets created. Implementation intentionally deferred under the specification-first execution gate.
