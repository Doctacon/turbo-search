Status: active
Created: 2026-07-15
Updated: 2026-07-15
Parent: .10x/tickets/2026-07-15-data-vault-semantic-retrieval-research-plan.md
Depends-On: None

# Research Data Vault Cross-Namespace Concept Graph

## Scope

Research a provenance-preserving concept/entity graph derived from chunks across many namespaces while keeping Data Vault 2.0 hubs, links, satellites, business keys, and history authoritative.

Execute in branch `work/research-data-vault-concept-graph` in its own worktree based on current `develop`. Produce `.10x/research/2026-07-15-data-vault-concept-graph.md`. Research only; do not implement.

## Questions

- Which nodes and edges are needed for source, namespace, chunk, business entity, concept, relationship, assertion, taxonomy term, and time?
- How should stable Data Vault identities map to derived entities without merging unratified LLM guesses into hubs or links?
- How should every concept, relationship, and summary retain chunk/source provenance, extraction version, confidence, validity, and retraction state?
- How do Chief Concepts, Cognee NodeSets, Graphiti, Microsoft GraphRAG, LlamaIndex PropertyGraphIndex, and RAGFlow handle graph construction, retrieval, updates, and deletion?
- Which open-source/self-hostable storage choices are viable, and when is a relational edge model sufficient before a graph database?
- How are cross-namespace ACLs enforced during graph traversal and concept aggregation?

## Acceptance criteria

- Inspect current Buoy identity/hash/provenance fields and active Data Vault/tagging preliminary research.
- Compare at least three open-source graph/concept approaches using source-backed behavior, licensing, operational cost, update semantics, and retrieval integration.
- Define candidate node/edge schemas with explicit authority and provenance classification.
- Analyze entity resolution, aliases, contradictory facts, temporal validity, deletion, model/taxonomy migration, and ACL leakage.
- Compare a full graph with smaller alternatives: concept cards, inverted entity assignments, or relational adjacency tables.
- Propose evals for entity resolution, edge precision, provenance completeness, deletion correctness, traversal usefulness, latency, and cost.
- Recommend a bounded concept-layer experiment, not an implementation or graph-store selection.

## Explicit exclusions

- Creating Data Vault hubs/links from LLM output.
- Choosing or deploying a graph database, changing schemas, extracting live entities, or mutating Turbopuffer.
- Assuming graph visualization improves retrieval.

## Evidence expectations

Record official docs and source links, licenses, local paths, model/graph lifecycle behavior, contradictions, null findings, and confidence. Name where product internals are undocumented.

## Blockers

None for research. Concept/edge semantics, storage, and implementation remain blocked on synthesis and user ratification.

## Progress and notes

- 2026-07-15: Ticket opened from the ratified four-track research plan. Execution intentionally deferred from the ticket-authoring turn.
- 2026-07-15: Activated the ticket and completed the bounded research record at `.10x/research/2026-07-15-data-vault-concept-graph.md`. Inspected current Buoy identity/provenance source and compared Chief Concepts, Cognee, Graphiti, Microsoft GraphRAG, LlamaIndex property graphs, RAGFlow, Data Vault authority boundaries, and open-source relational/graph storage. The record proposes a reified assertion/evidence model, ACL/temporal/deletion controls, smaller alternatives, and a synthetic offline eval; it makes no store selection or live/source/spec/decision change. Ticket intentionally remains active for independent review.
