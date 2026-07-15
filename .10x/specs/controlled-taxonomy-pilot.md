Status: active
Created: 2026-07-15
Updated: 2026-07-15

# Controlled Taxonomy Pilot

## Purpose and scope

Define a small, local, controlled taxonomy for testing namespace routing and tag-aware retrieval without ratifying production taxonomy content or public tag behavior.

This specification governs pilot fixtures and internal evaluator behavior only. The existing retrieval-tag output drift remains owned by `.10x/tickets/2026-07-15-reconcile-retrieval-tag-output.md`.

## Taxonomy fixture

The pilot MUST use a version-controlled JSON fixture with a non-empty `taxonomy_revision` and a non-empty list of terms.

Each term MUST contain:

- `term_id`: stable unique identifier;
- `label`: human-readable canonical label;
- `description`: what the term means in the synthetic fixture;
- `synonyms`: zero or more unique alternative phrases.

Term IDs are identity. Labels, descriptions, and synonyms are descriptors. The pilot MUST reject duplicate term IDs, case-insensitive duplicate labels, a synonym duplicated across terms, empty required values, and a synonym equal to its own label after normalization.

The first pilot taxonomy MUST remain flat. Parent/child hierarchies, ontology constraints, open-set terms, and automatic taxonomy growth are excluded until evidence shows they are required.

## Assignment classes

Namespace `tag_ids` in the catalog fixture are governed synthetic assignments. They MAY participate in exact filters and exact routing.

Semantic similarity between a query and a namespace card is a derived score. It MUST NOT create, persist, or silently promote a governed taxonomy assignment.

Probabilistic or LLM-generated tags are excluded from the first pilot. ACL groups MUST remain separate fields and MUST NOT be represented as taxonomy terms.

## Query-term matching

Exact matching MUST:

1. Unicode-normalize and case-fold the query and labels/synonyms;
2. match complete normalized phrases rather than arbitrary substrings;
3. map a matched label or synonym to exactly one term ID;
4. return each matched term once;
5. expose matched term IDs and matched phrases for authorized selected namespaces.

Exact matching MUST NOT infer related terms, expand hierarchy, or call an LLM.

## Tag-aware cached evidence

Pilot cached evidence rows MAY carry internal `tag_ids` solely to evaluate tag filtering or a bounded tag-match boost. Those tags use the same taxonomy revision and validation rules as namespace assignments.

Hard filtering MUST use governed fixture tags only. Semantic similarity MUST NOT act as a hard exclusion. An untagged relevant evidence row MUST remain measurable so false exclusion is visible.

No pilot tag field changes the public `SearchHit`, CLI, Turbopuffer schema, or live retrieval contract.

## Acceptance scenarios

### Canonical label

Given a query containing a term label as a complete phrase, when exact matching runs, then the corresponding term ID is returned once.

### Synonym

Given a query containing a unique synonym, when exact matching runs, then its canonical term ID is returned with the synonym as match evidence.

### Substring

Given a query containing characters that only form a substring of a label, when exact matching runs, then the term does not match.

### Ambiguous taxonomy

Given the same normalized synonym on two terms, when the taxonomy loads, then validation fails.

### ACL separation

Given a taxonomy label resembling a group name, when authorization runs, then the label grants no access.

### Derived score

Given semantic card similarity without an exact term match, when routing completes, then no governed tag assignment is created or persisted.

## Acceptance criteria

- Taxonomy and assignment validation are deterministic and test-covered.
- Exact matching produces explainable stable term IDs.
- ACL fields and topical taxonomy remain structurally separate.
- Derived semantic scores do not mutate governed assignments.
- No LLM, remote model, network, credential, or Turbopuffer operation is used.

## Explicit exclusions

- Production taxonomy governance or stewardship workflow.
- Hierarchies, ontology constraints, entity extraction, concepts, or relationships.
- Automatic tagging or open-set keyword generation.
- Public CLI/API tag filters or output.
- Live chunk updates or Turbopuffer writes.
