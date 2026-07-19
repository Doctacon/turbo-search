Status: done
Created: 2026-06-28
Updated: 2026-06-28
Depends-On: .10x/evidence/2026-06-28-repo-oversize-metadata-live-eval.md, .10x/tickets/2026-06-28-repo-searchable-path-symbol-metadata.md

# Repo Search Metadata Cross-Repo Validation

## Scope

Validate metadata-only repository indexing (`--repo-search-metadata` with the default 51200-byte file cap) across the older repo validation basket before considering any default planner change.

Targets:

- `turbo-search` clean namespace equivalent;
- `psf/requests`;
- `pallets/click`.

## Acceptance criteria

- Use new namespaces only.
- Preserve default file-size cap; test metadata-only, not oversize indexing.
- No stale deletion or namespace deletion.
- Compare current baseline namespaces against metadata-only namespaces using existing seed datasets.
- Apply no-regression policy before any default change.
- Record live apply counts and retrieval-only metrics in evidence.

## Explicit exclusions

- No oversize source indexing in this ticket.
- No code changes unless the metadata implementation has a bug.
- No default promotion in the same step as validation.

## Blockers

- Live apply/eval requires explicit approval at execution time.

## References

- `.10x/evidence/2026-06-28-repo-oversize-metadata-live-eval.md`
- `.10x/research/2026-06-28-expanded-validation-ranking-hypotheses.md`

## Progress and notes

- 2026-06-28: Opened after metadata-only improved pytest and Typer seed datasets while oversize indexing was not default-safe.
- 2026-06-28: After explicit user approval, live-applied metadata-only indexes to new older-basket namespaces and evaluated against current baselines. Metadata-only improved Click but regressed turbo-search and Requests by composite score, failing no-regression promotion despite better five-repo average score and P@5. No default promotion. Evidence: `.10x/evidence/2026-06-28-repo-search-metadata-cross-repo-validation.md`.
