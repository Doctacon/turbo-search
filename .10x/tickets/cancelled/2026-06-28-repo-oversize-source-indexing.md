Status: cancelled
Created: 2026-06-28
Updated: 2026-07-19
Depends-On: .10x/tickets/done/2026-06-28-cross-corpus-validation-basket.md

# Repo Oversize Source Indexing

## Scope

Investigate and improve GitHub repository planning for important source files above the current 50 KiB file-size cap.

The expanded validation basket exposed that central implementation files can be skipped as oversized:

- `pytest-dev/pytest`: examples include `src/_pytest/fixtures.py`, `src/_pytest/python.py`, and `src/_pytest/config/__init__.py`.
- `fastapi/typer`: examples include `typer/main.py` and `typer/params.py`.

This limits repository-search validation because seed labels must avoid skipped source files even when those files are the primary authority for a user query.

## Acceptance criteria

- Characterize how many files and chunks would be added by increasing or replacing the current oversize-file policy across current validation repos.
- Preserve local-only `plan` behavior: no credentials, embeddings, turbopuffer calls, or namespace mutation during investigation.
- Propose the smallest safe change, such as a higher cap, line-range chunking for oversized text files, or per-language limits.
- Validate that generated artifacts remain reviewable and do not admit binary/vendor/generated noise.
- Do not change live namespaces or defaults without separate approval.

## Explicit exclusions

- No Tree-sitter or syntax-aware chunking unless separately selected.
- No live apply or reindex.
- No stale deletion or namespace deletion.

## Blockers

None. This ticket is cancelled with the evidence-backed no-action rationale below.

## References

- `.10x/evidence/2026-06-28-cross-corpus-validation-local-plans.md`
- `.10x/evidence/2026-06-28-cross-corpus-seed-eval-datasets.md`
- `src/buoy_search/github_repo.py`

## Progress and notes

- 2026-06-28: Opened after seed dataset drafting found central pytest and Typer implementation files skipped by the 50 KiB repo file cap.
- 2026-06-28: Added explicit opt-in `--repo-max-file-bytes` and locally planned pytest/Typer with a 200 KiB cap plus search metadata. Central authority files are included (`src/_pytest/fixtures.py`, `src/_pytest/python.py`, `src/_pytest/config/__init__.py`, `typer/main.py`, `typer/params.py`). Planned rows: pytest 6893, Typer 3221. No live apply in this local slice. Evidence: `.10x/evidence/2026-06-28-repo-oversize-metadata-local-validation.md`.
- 2026-06-28: After explicit user approval for writes/evals to new namespaces, live-applied oversize-only, metadata-only, and oversize+metadata ablations for pytest/Typer. Oversize recovered authority-file query score (`pytest 23.136 -> 78.622`, `Typer 27.002 -> 69.619`) but regressed existing seed score (`pytest 84.742 -> 81.354`, `Typer 59.423 -> 52.042`). Keep oversize opt-in/query-routed; do not promote as a global default. Evidence: `.10x/evidence/2026-06-28-repo-oversize-metadata-live-eval.md`.
- 2026-07-19: Closure review found the completed pytest/Typer ablation supports the opt-in/no-promotion conclusion but does not prove the acceptance criterion's full current-basket characterization or an explicit binary/vendor/generated-noise audit. A `done` disposition is therefore unsupported. The ticket is cancelled rather than kept indefinitely open because the existing live evidence rejects global promotion and preserves the experimental opt-in; any future query-routed oversize policy requires a newly scoped owner and fresh evidence. Review: `.10x/reviews/2026-07-19-stale-ticket-status-closure-review.md`.

## Existing acceptance mapping

- Added-file/chunk characterization: supported for pytest and Typer only by `.10x/evidence/2026-06-28-repo-oversize-metadata-local-validation.md`; not proven across the full then-current repo basket.
- Local-only planning safety: supported by the local validation evidence.
- Smallest safe direction: the existing records support an explicit 200 KiB opt-in and the conclusion to keep oversize opt-in or future query-routed, not a global default.
- Reviewability/noise control: row growth and recovered authority files are recorded, but an explicit binary/vendor/generated-noise audit is absent.
- Live safety: `.10x/evidence/2026-06-28-repo-oversize-metadata-live-eval.md` records separate approval, new namespaces, and zero deletions.

## No-action rationale

Do not complete or promote a global oversize default from this ticket. The tested opt-in recovered missing authority-file queries but materially regressed both existing seed datasets. Preserve the opt-in as experimental behavior; revisit only under a new query-routed contract that defines the broader basket and noise audit.
