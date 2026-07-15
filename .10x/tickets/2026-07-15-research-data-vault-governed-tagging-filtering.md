Status: active
Created: 2026-07-15
Updated: 2026-07-15
Parent: .10x/tickets/2026-07-15-data-vault-semantic-retrieval-research-plan.md
Depends-On: None

# Research Data Vault Governed Tagging and Filtering

## Scope

Research governed tagging for namespaces, sources, documents, and chunks, including exact metadata filtering and relevance boosts. Distinguish Data Vault 2.0 business metadata from structural tags and probabilistic inferred labels.

Execute in branch `work/research-data-vault-tagging` in its own worktree based on current `develop`. Produce `.10x/research/2026-07-15-data-vault-governed-tagging-filtering.md`. Research only; do not implement.

## Questions

- Which tags are authoritative, human-defined, rule-derived, closed-set similarity assignments, or open-set LLM extractions?
- How should tag identity, hierarchy/synonyms, taxonomy version, assignment source, confidence, reviewer state, and effective history be modeled?
- Which fields should be materialized onto Turbopuffer chunks for filtering/ranking, and which provenance belongs in an external authoritative store?
- How do Chief Labels/Collections, RAGFlow tag sets, Cognee NodeSets, and comparable open-source tools apply, update, remove, and query tags?
- What should AND/OR/exclusion, namespace-level versus chunk-level, and filter-versus-boost semantics be?
- How are ACL tags kept separate from topical relevance tags so retrieval cannot bypass authorization?

## Acceptance criteria

- Inspect Buoy's current deterministic tags, Turbopuffer schema, retrieval filters/output, plan artifacts, and the blocked tag-output drift ticket.
- Build a taxonomy of tagging modes and identify which are safe as authority versus derived hints.
- Define at least two candidate tagging architectures with update/deletion/reprocessing behavior.
- Provide a candidate assignment/provenance model and a minimal materialized Turbopuffer attribute model consistent with documented limits.
- Define query semantics and compatibility impacts for single- and multi-namespace retrieval without turning examples into requirements.
- Propose evals for tag precision/recall, routing/retrieval quality, false exclusion, ACL safety, taxonomy drift, and operating cost.
- Recommend the smallest controlled-tag experiment, not an implementation.

## Explicit exclusions

- Implementing retrieval tag output/filtering, resolving `.10x/tickets/2026-07-15-reconcile-retrieval-tag-output.md`, or changing public behavior.
- Treating LLM-inferred tags as Data Vault authority.
- Live Turbopuffer operations or proprietary-only taxonomy services.

## Evidence expectations

Record official documentation, open-source implementation evidence where available, inspected local paths, taxonomy/version tradeoffs, failure cases, and confidence. Separate product claims from measured evidence.

## Blockers

None for research. Tag semantics and implementation remain blocked on findings, synthesis, and user ratification.

## Progress and notes

- 2026-07-15: Ticket opened from the ratified four-track research plan. Execution intentionally deferred from the ticket-authoring turn.
- 2026-07-15: Inspected the parent plan, preliminary research, blocked tag-output drift ticket, referenced active records, and Buoy tagging/schema/retrieval/applied-state source. Reviewed official Chief, RAGFlow, Cognee, and Turbopuffer documentation plus Data Vault and open taxonomy/catalog comparisons. Drafted `.10x/research/2026-07-15-data-vault-governed-tagging-filtering.md`; ticket remains active pending independent review.
