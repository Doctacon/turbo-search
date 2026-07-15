Status: open
Created: 2026-07-15
Updated: 2026-07-15
Parent: .10x/tickets/2026-07-15-data-vault-semantic-retrieval-research-plan.md
Depends-On: None

# Research Data Vault Namespace Catalog and Routing

## Scope

Research the smallest governed catalog and query-routing layer for many Buoy/Turbopuffer namespaces, informed by Data Vault 2.0 identity, lineage, and history without treating a namespace or vector index as a Data Vault hub.

Execute in branch `work/research-data-vault-namespace-routing` in its own worktree based on current `develop`. Produce `.10x/research/2026-07-15-data-vault-namespace-catalog-routing.md`. Research only; do not implement.

## Questions

- What is the authoritative identity for a namespace, source, Data Vault business concept, and indexed revision?
- Which catalog fields are required for semantic routing, embedding/schema compatibility, ACLs, freshness, source lineage, and retrieval profiles?
- Should the canonical catalog be relational/Data Vault-backed with a derived searchable namespace-card index, or can Turbopuffer safely be canonical?
- How should a query select a bounded compatible namespace set without all-namespace fan-out?
- Which routing approaches—exact filters, taxonomy classification, semantic namespace cards, learned routing, or hybrids—deserve evaluation?
- How are rename, reindex, stale source, deletion, model migration, and access-policy changes represented historically?

## Acceptance criteria

- Inspect current namespace discovery, multi-namespace retrieval, plan artifacts, applied state, and relevant decisions/specifications.
- Use official Turbopuffer documentation and primary/open-source routing/catalog examples.
- Define at least two viable architectures, their authority boundaries, failure modes, and migration paths.
- Provide a candidate catalog model with Data Vault 2.0 mapping, provenance, ACL, version, and embedding-contract fields.
- Define routing flow, compatibility checks, fallback behavior, and explicit non-goals.
- Propose offline eval cases and metrics for namespace-selection recall, over-selection, latency, cost, ACL safety, and final answer quality.
- State what can be tested without live Turbopuffer access.
- Recommend the smallest experiment, not an implementation.

## Explicit exclusions

- Product code, schemas, migrations, CLI/UI changes, live retrieval, live writes, or namespace mutation.
- Selecting a proprietary managed catalog or graph service when an open-source/self-hostable alternative is viable.
- Assuming catalog metadata ratifies Data Vault business meaning.

## Evidence expectations

Record source URLs, versions/dates where available, inspected local paths, competing options, null findings, cost/scale limits, and confidence. Distinguish documented facts from recommendations.

## Blockers

None for research. Architecture selection and implementation remain blocked on synthesis and user ratification.

## Progress and notes

- 2026-07-15: Ticket opened from the ratified four-track research plan. Execution intentionally deferred from the ticket-authoring turn.
