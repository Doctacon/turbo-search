Status: open
Created: 2026-07-15
Updated: 2026-07-15
Parent: .10x/tickets/2026-07-15-production-semantic-routing-plan.md
Depends-On: None

# Build Production Local Namespace Catalog

## Outcome

Implement the canonical local catalog model, persistence, pinned card-vector projection, and complete local catalog management CLI governed by `.10x/specs/production-local-namespace-catalog.md`.

## Branch and worktree

Execute on `work/build-production-local-namespace-catalog` in its own worktree from current integrated `develop`.

## Scope

- Add the smallest production catalog module and typed card/document/error models.
- Implement state-root/catalog path resolution and exact CLI/environment precedence, existing stable-JSON canonical hashes/golden fixtures, strict loaders, atomic lock-protected mutation, and vector validation.
- Implement deterministic card text, pinned local-only model construction, vector creation/reuse, and generated semantic helpers needed by later apply work.
- Add `catalog list`, `show`, `upsert`, `enable`, `disable`, and approved local-only `remove` commands with text/JSON output.
- Expose a narrow validated card merge/commit API for later apply reconciliation without implementing apply integration yet.
- Add focused unit/CLI tests for every catalog acceptance scenario, complete source-kind/URI mapping and contradictions, 384-dimension contract, golden passage/hash/vector fixtures, corruption/concurrency, model no-download behavior, mutation safety, and no credential/Turbopuffer access.
- Update user documentation for catalog creation and management.
- Record evidence and obtain independent review before closure.

## Acceptance criteria

- Catalog schema, revisions, semantic/retrieval/routing contracts, hashes, ordering, strict unknown-field rejection, and vectors match the active spec.
- Local state mutation is atomic and lock-protected; failed writes preserve prior bytes.
- Manual upsert creates or updates manual semantics and persisted vectors without contacting Turbopuffer or reading credentials.
- Enable/disable preserve semantic/vector fields; remove is preview-only without `--approve` and never deletes remote/applied state.
- Read commands do not load the model and hide vectors by default.
- Generated semantic helper behavior is deterministic and independently testable.
- Existing CLI commands and explicit retrieval remain compatible.
- No remote catalog, apply integration, automatic routing, ACL, graph, taxonomy, tag filter, telemetry, or new dependency is added.
- Focused tests, full suite, and `git diff --check` pass.
- Independent review has no unresolved significant finding.

## Explicit exclusions

- mutation during plan/apply;
- pending apply registration/reconciliation command wiring;
- `retrieve --auto-route`;
- Turbopuffer namespace listing/query/write;
- import from remote namespace IDs;
- multi-user permissions;
- model download or hosted embedding API.

## Evidence expectations

Evidence must cover schema/hash fixtures, atomic/lock failure behavior, vector model/revision/hash validation, no-download/no-credential/no-Turbopuffer sentinels, every catalog CLI operation, explicit retrieval regression, full validation, and diff boundaries.

## Blockers

None after shaping review/integration.

## Progress and notes

- 2026-07-15: Opened as the first executable child. No implementation occurred in the specification-authoring turn.
