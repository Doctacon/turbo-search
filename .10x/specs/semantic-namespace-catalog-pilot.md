Status: active
Created: 2026-07-15
Updated: 2026-07-15

# Semantic Namespace Catalog Pilot

## Purpose and scope

Define the local, synthetic namespace catalog used to evaluate routing across many Buoy/Turbopuffer namespaces without contacting Turbopuffer or selecting production infrastructure.

The catalog is pilot authority only. It models stable namespace/source/revision identity, retrieval compatibility, controlled taxonomy assignments, lifecycle eligibility, and synthetic access boundaries. It MUST NOT be presented as a production catalog, Data Vault, ontology, graph, or remote namespace registry.

## Canonical fixture

The pilot MUST use a version-controlled JSON fixture as its canonical input. The fixture MUST include a non-empty `catalog_revision` and a non-empty list of namespace records.

Each namespace record MUST contain:

- `namespace_id`: unique Turbopuffer-style identifier;
- `revision_id`: immutable fixture revision identity for this indexed representation;
- `source_id`: stable source identity independent of namespace naming;
- `source_kind`: explicit source class such as site, repository, PDF, or local file;
- `title`: human-readable source title;
- `description`: concise card description used for semantic routing;
- `tag_ids`: unique controlled taxonomy term IDs;
- `embedding_model`, `embedding_dimensions`, and `embedding_precision`;
- `schema_version` and `ranking_profile`;
- `enabled`: whether the revision is eligible for routing;
- `is_public` and `allowed_groups`: synthetic pilot authorization fields.

IDs and descriptions MUST be explicit fixture data. The loader MUST NOT infer business meaning, compatibility, authorization, or source identity from namespace prefixes.

The fixture MUST reject duplicate namespace IDs, duplicate revision IDs, unknown taxonomy terms, empty required strings, non-positive vector dimensions, unsupported embedding precision, duplicate group IDs, and a private namespace with no allowed group.

## Synthetic access contract

The pilot uses synthetic groups only; it does not define production authorization.

A namespace is authorized when either:

- `is_public` is true; or
- the query principal has at least one group in `allowed_groups`.

A private namespace with no matching group MUST be excluded before any exact or semantic scoring. Unauthorized namespace IDs, titles, descriptions, tags, scores, and exclusion reasons MUST NOT appear in route results or user-facing diagnostics.

## Compatibility and lifecycle gates

A namespace MUST be excluded before scoring when:

- `enabled` is false; or
- its embedding model, dimensions, or precision differ from the query contract.

The pilot MUST treat those fields as an exact compatibility tuple. It MUST NOT infer compatibility from model-name similarity or namespace naming.

## Namespace cards

The pilot MUST derive one deterministic semantic card per eligible namespace revision from:

```text
Title: <title>
Description: <description>
Tags: <taxonomy labels in tag-id order>
Source kind: <source_kind>
```

Card generation MUST be deterministic for identical catalog and taxonomy revisions. Cards are disposable projections and MUST retain `catalog_revision`, `revision_id`, and `namespace_id` references.

## Local representation

Implementation MAY load the JSON fixture into Python structures or an in-memory DuckDB database. It MUST NOT persist a database outside test/pilot temporary directories and MUST NOT add a new runtime dependency.

## Acceptance scenarios

### Authorized compatible namespace

Given an enabled namespace with a matching embedding contract and either public access or an overlapping group, when candidates are prepared, then the namespace is eligible for routing.

### Unauthorized namespace

Given a private namespace without a matching group, when routing runs, then it is absent from candidates, results, scores, and diagnostics.

### Incompatible namespace

Given a namespace with a different embedding model, dimensions, or precision, when routing runs, then it is excluded before exact and semantic scoring.

### Disabled namespace

Given `enabled: false`, when routing runs, then the namespace is excluded before scoring.

### Invalid reference

Given a namespace referencing an unknown taxonomy term, when the fixture loads, then validation fails before evaluation.

### Deterministic card

Given the same catalog and taxonomy revisions, when cards are generated repeatedly, then their text and identity references are byte-for-byte stable.

## Acceptance criteria

- The canonical fixture and loader satisfy every field and validation rule above.
- Eligibility gates are deterministic and test-covered.
- Unauthorized namespace metadata cannot leak through results or diagnostics.
- No network, credential lookup, embedding-model download, Turbopuffer SDK construction, or persistent database occurs.

## Explicit exclusions

- Production catalog persistence or synchronization.
- Namespace creation, mutation, deletion, or discovery.
- Real user/group policy.
- Data Vault schemas or loading.
- Ontology, concept extraction, graph nodes, or graph traversal.
- Freshness/staleness policy beyond the explicit `enabled` fixture field.
