Status: open
Created: 2026-07-15
Updated: 2026-07-15
Parent: .10x/tickets/2026-07-15-data-vault-semantic-retrieval-research-plan.md
Depends-On: None

# Research Data Vault Multi-Hop and Global Retrieval

## Scope

Research retrieval and evaluation strategies for questions that need evidence across namespaces, multiple hops, entity relationships, or corpus-wide synthesis. Determine when metadata routing, iterative vector retrieval, concept indexes, or graph traversal are justified over current explicit multi-namespace RRF.

Execute in branch `work/research-data-vault-multihop` in its own worktree based on current `develop`. Produce `.10x/research/2026-07-15-data-vault-multi-hop-global-retrieval.md`. Research only; do not implement.

## Questions

- Which query classes are local factual, cross-namespace, multi-hop, entity-centric, temporal, or global/sensemaking?
- Which baselines should be compared: current RRF, metadata-filtered retrieval, query decomposition, iterative retrieval, RAPTOR-style summaries, GraphRAG local/global/DRIFT, and graph-path retrieval?
- Which public benchmarks transfer to Buoy, and which project-specific datasets must be authored?
- What evidence establishes that a graph improves retrieval rather than only answer fluency?
- How should citation completeness, hop coverage, retrieval recall, faithfulness, latency, index cost, query cost, and ACL correctness be measured?
- What cost/quality gate should stop graph construction when metadata or decomposition suffices?

## Acceptance criteria

- Inspect current Buoy retrieval/eval architecture, ranking defaults, multi-namespace RRF contract, and existing eval records.
- Review primary papers and official/open-source implementations for multi-hop metadata RAG, GraphRAG, RAPTOR or comparable hierarchical retrieval, and iterative/decomposed retrieval.
- Define a query taxonomy and candidate evaluation matrix with the current system as baseline.
- Separate retrieval metrics from generation metrics and include provenance/citation and ACL checks.
- Identify reusable public datasets and specify the smallest Buoy-specific seed dataset needed for cross-namespace/Data Vault scenarios.
- Estimate indexing/query cost categories and define promotion thresholds or decision gates without inventing numeric values unsupported by evidence.
- Recommend an experiment order that can reject unnecessary graph complexity early.

## Explicit exclusions

- Building a benchmark, running live evals, implementing retrievers, or constructing a graph.
- Treating paper-specific gains as universal.
- Comparing raw scores across namespaces without calibrated or rank-based fusion.

## Evidence expectations

Record paper/version links, task and dataset scope, reported metrics with limitations, local paths, baseline gaps, contradictory findings, and confidence. Distinguish peer-reviewed work, preprints, vendor claims, and project documentation.

## Blockers

None for research. Experiments and implementation remain blocked on completed research, synthesis, and user ratification.

## Progress and notes

- 2026-07-15: Ticket opened from the ratified four-track research plan. Execution intentionally deferred from the ticket-authoring turn.
