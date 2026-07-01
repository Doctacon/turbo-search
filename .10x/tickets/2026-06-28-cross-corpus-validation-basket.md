Status: open
Created: 2026-06-28
Updated: 2026-06-28
Depends-On: .10x/decisions/namespace-ranking-defaults.md, .10x/tickets/2026-06-28-repo-search-heavy-ranking-experiments.md

# Cross-Corpus Validation Basket

## Scope

Expand validation before further ranking default changes so repo/site ranking does not overfit the existing corpora.

User-selected basket:

- Repos:
  - `https://github.com/pytest-dev/pytest`
  - `https://github.com/fastapi/typer`
- Sites:
  - Ruff docs
  - Typer docs

Policy selected by user:

```text
No regressions: promote future defaults only if no validation target regresses meaningfully.
```

## Acceptance criteria

- Add source-backed seed eval datasets for the selected repos/sites.
- Use local-only plan/dry-run first for any new namespace; no credentials or turbopuffer calls during planning.
- Use new namespaces only for repo/site apply if live apply is separately approved.
- Do not delete namespaces or stale rows.
- Run live retrieval-only evals only after the relevant namespace has been applied and live validation is explicitly approved.
- Compare current defaults against at least one baseline/alternate relevant to each corpus.
- Record evidence with commands, counts, metrics, limits, and promotion/no-promotion conclusion.
- Apply the no-regression policy before changing defaults.

## Explicit exclusions

- No private repositories.
- No GitHub HTML crawling for repo ingestion.
- No namespace deletion or stale deletion.
- No proprietary model APIs.
- No schema/index changes unless separately scoped and approved.

## Blockers

- Live apply/retrieval for new namespaces still requires explicit approval at execution time.
- Exact Ruff and Typer docs base URLs should be confirmed from current public docs before planning.

## References

- `.10x/decisions/namespace-ranking-defaults.md`
- `.10x/evidence/2026-06-28-repo-adaptive-aggregation-validation.md`
- `.10x/evidence/2026-06-28-cross-repo-click-validation.md`
- `.10x/knowledge/repo-search-ranking-defaults.md`

## Progress and notes

- 2026-06-28: Opened after user agreed to expand validation with 2 repos + 2 sites, selected `pytest + typer` repos, `Ruff + Typer docs` sites, and selected no-regressions promotion policy.
- 2026-06-28: Completed local-only plans for all four targets. No embeddings, credential reads, turbopuffer calls, deletes, or namespace mutation occurred. Planned rows/chunks: pytest repo 3493, Typer repo 2512, Ruff docs 1441, Typer docs 1271. Evidence: `.10x/evidence/2026-06-28-cross-corpus-validation-local-plans.md`.
