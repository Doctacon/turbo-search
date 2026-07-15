Status: active
Created: 2026-07-15
Updated: 2026-07-15

# Offline Semantic Routing Evaluation

## Purpose and scope

Define an offline pilot that compares exact taxonomy routing, semantic namespace-card routing, and a hybrid strategy before any production catalog, live Turbopuffer integration, or knowledge graph is considered.

The current explicit multi-namespace retrieval and cross-namespace reciprocal-rank fusion behavior remains the downstream control. This pilot evaluates selection before retrieval and uses cached synthetic result lists to measure downstream effects.

## Inputs

The evaluator MUST consume:

- a valid semantic catalog fixture governed by `.10x/specs/semantic-namespace-catalog-pilot.md`;
- a valid taxonomy fixture governed by `.10x/specs/controlled-taxonomy-pilot.md`;
- deterministic card vectors and query vectors supplied by the fixture or an injected local scorer;
- evaluation cases with query text, synthetic principal groups, embedding contract, expected namespace IDs, forbidden namespace IDs, cached namespace-local ranked evidence, and a `development` or `held_out` split.

Tests and the committed pilot dataset MUST use deterministic fixture vectors. The evaluator MUST NOT download or initialize an embedding model. A later separately authorized experiment may inject a local open-source model without changing routing semantics.

## Eligibility first

Authorization, `enabled`, and embedding-contract compatibility MUST be evaluated before every routing strategy. Ineligible namespaces MUST not be scored.

Forbidden namespace selection is a safety failure, not a relevance tradeoff. The evaluator MUST report an exact count and case IDs while keeping forbidden namespace metadata out of ordinary route results.

## Routing strategies

All strategies receive the same eligible candidate set and route limit.

### Exact taxonomy

- Extract query term IDs using the controlled taxonomy matching contract.
- Select namespaces assigned at least one matched term.
- Rank by descending number of distinct matched terms, then `namespace_id` ascending.
- If no term matches, return no exact candidates rather than guessing.

### Semantic card

- Rank eligible namespace cards by cosine similarity between deterministic query and card vectors.
- Sort descending by similarity, then `namespace_id` ascending.
- Semantic scores MUST NOT be compared with namespace-local retrieval scores.

### Hybrid

- Fuse exact-taxonomy and semantic-card ranks using reciprocal-rank fusion with the project's existing `RRF_K = 60`.
- Each strategy has equal weight.
- A namespace present in only one list remains eligible for the fused list.
- Resolve ties by `namespace_id` ascending.

## Route output

For each selected authorized namespace, the route result MUST include:

- `namespace_id` and `revision_id`;
- route rank and strategy;
- matched taxonomy term IDs/phrases when applicable;
- semantic rank when applicable;
- fused score when applicable;
- compatibility contract used.

Output MUST include catalog/taxonomy revisions and deterministic strategy parameters. It MUST NOT expose unauthorized candidate metadata.

## Downstream cached retrieval

For each strategy, the evaluator MUST take the selected namespaces' cached namespace-local ranked evidence and merge them using the existing namespace-qualified RRF semantics. Raw namespace-local scores MUST NOT be compared directly.

Cached evidence identity MUST include namespace plus row identity. The evaluator MUST not collapse equivalent row IDs across namespaces.

## Metrics

The evaluator MUST report per case, per split, and aggregate:

- required namespace recall;
- selected namespace precision;
- over-selection count;
- selected namespace count/fan-out;
- forbidden namespace selection count;
- incompatible or disabled namespace selection count;
- downstream required-evidence recall at the configured cutoff;
- route strategy and deterministic parameters.

It MUST retain individual case results; aggregate averages MUST NOT hide safety failures.

The pilot is descriptive. No numeric promotion threshold is ratified. Results MUST be compared on identical held-out cases, route limits, cached evidence, and compatibility/ACL fixtures.

## Evaluation discipline

- Development cases MAY be used to correct fixtures and implementation defects.
- Held-out cases MUST NOT be used to tune card text, vectors, synonyms, route limits, or fusion.
- Any held-out-driven change creates a new fixture revision and requires a new untouched held-out set before promotion claims.
- The pilot MUST identify exact-only routing as the cheapest control and current explicit selection/RRF as the downstream baseline.

## Acceptance scenarios

### ACL before relevance

Given an unauthorized namespace with the best semantic similarity, when any strategy runs, then it is never selected or exposed.

### Compatibility before relevance

Given an incompatible namespace with exact tag and high semantic matches, when routing runs, then it is excluded before scoring.

### Exact miss

Given no label or synonym match, when exact routing runs, then it returns no route; semantic and hybrid results remain independently measurable.

### Hybrid union

Given one namespace ranked only by exact matching and another only by semantic matching, when hybrid routing runs, then both may appear subject to the route limit and deterministic RRF order.

### Downstream identity

Given equal row IDs in two namespaces, when cached results merge, then both remain distinct namespace-qualified evidence items.

### Reproducibility

Given identical fixture revisions and vectors, when the pilot runs repeatedly, then route results and metrics are byte-for-byte stable.

## Acceptance criteria

- All three strategies and eligibility gates satisfy the contracts above.
- The evaluator is deterministic and entirely local.
- The fixture covers public/private access, overlapping groups, disabled and incompatible namespaces, exact and synonym matches, semantic-only matches, false-exclusion cases, and duplicate cross-namespace row IDs.
- Tests prove no network, credential lookup, model download, Turbopuffer SDK construction, live retrieval, or write occurs.
- A recorded pilot report maps results to the metrics without selecting production architecture.

## Explicit exclusions

- Answer generation or LLM judging.
- Live Turbopuffer reads/writes or namespace discovery.
- Real ACL policy.
- Public CLI/API behavior.
- Learned routing, query decomposition, concepts, ontology, graph construction, or traversal.
- Production storage, synchronization, or promotion thresholds.
