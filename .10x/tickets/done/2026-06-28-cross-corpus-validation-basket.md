Status: done
Created: 2026-06-28
Updated: 2026-07-19
Depends-On: .10x/decisions/namespace-ranking-defaults.md

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

None. The recorded execution used the current public docs URLs and separately approved live apply/retrieval.

## References

- `.10x/decisions/namespace-ranking-defaults.md`
- `.10x/tickets/2026-06-28-repo-search-heavy-ranking-experiments.md` — active umbrella that receives context and evidence from this independently completed basket; it was not an execution dependency.
- `.10x/evidence/2026-06-28-repo-adaptive-aggregation-validation.md`
- `.10x/evidence/2026-06-28-cross-repo-click-validation.md`
- `.10x/knowledge/repo-search-ranking-defaults.md`

## Progress and notes

- 2026-06-28: Opened after user agreed to expand validation with 2 repos + 2 sites, selected `pytest + typer` repos, `Ruff + Typer docs` sites, and selected no-regressions promotion policy.
- 2026-06-28: Completed local-only plans for all four targets. No embeddings, credential reads, turbopuffer calls, deletes, or namespace mutation occurred. Planned rows/chunks: pytest repo 3493, Typer repo 2512, Ruff docs 1441, Typer docs 1271. Evidence: `.10x/evidence/2026-06-28-cross-corpus-validation-local-plans.md`.
- 2026-06-28: Added seed eval datasets for all four targets and dry-run/source-backed validation. Cases/judgments: pytest 10/52, Typer repo 10/53, Ruff docs 10/31, Typer docs 10/37. Added `tests.test_evals` coverage for loading these datasets. Evidence: `.10x/evidence/2026-06-28-cross-corpus-seed-eval-datasets.md`.
- 2026-06-28: Discovered current 50 KiB repo file cap skips some central source files in pytest and Typer plans; seed labels avoid skipped files for now. Follow-up owner: `.10x/tickets/cancelled/2026-06-28-repo-oversize-source-indexing.md`.
- 2026-06-28: After explicit user approval, live-applied all four new namespaces without `--delete-stale`. Rows/embeddings upserted: pytest repo 3493, Typer repo 2512, Ruff docs 1441, Typer docs 1271; rows deleted 0. Evidence: `.10x/evidence/2026-06-28-cross-corpus-live-apply.md`.
- 2026-06-28: After explicit user approval, ran live retrieval-only evals on the four new namespaces. Current repo default beat repo max on both new repos and raw chunk by a large margin; capped_sum_3 regressed Typer repo, so no repo default change. Current site default beat raw chunk on both new sites; capped_sum_3 improved both new sites, but prior Pi-site evidence blocks automatic promotion under no-regression policy. Evidence: `.10x/evidence/2026-06-28-cross-corpus-live-retrieval-evals.md`. Follow-up owner for website capped review: `.10x/tickets/done/2026-06-28-website-capped-aggregation-default-review.md`.
- 2026-07-19: Closure review mapped all eight criteria to the four existing evidence records and active namespace-ranking decision. Separate approvals, new-namespace-only writes, zero deletions, retrieval-only evals, baseline comparisons, metrics, and the no-regression no-promotion conclusion are recorded. Review: `.10x/reviews/2026-07-19-stale-ticket-status-closure-review.md`.

## Closure mapping

- Source-backed datasets: `.10x/evidence/2026-06-28-cross-corpus-seed-eval-datasets.md`.
- Local-only planning, resolved URLs, counts, and no credentials/remote calls: `.10x/evidence/2026-06-28-cross-corpus-validation-local-plans.md`.
- Separately approved new-namespace applies with zero deletions: `.10x/evidence/2026-06-28-cross-corpus-live-apply.md`.
- Separately approved retrieval-only baseline/alternate comparisons, metrics, limits, and no-regression conclusion: `.10x/evidence/2026-06-28-cross-corpus-live-retrieval-evals.md`.
- Ranking authority remains coherent with `.10x/decisions/namespace-ranking-defaults.md`; no default changed from this basket.

## Retrospective

The existing evidence identified an important validation limit rather than hiding it: assistant-drafted repo labels avoided central files skipped by the 50 KiB cap. That blind spot was preserved under a separate owner, while website capped aggregation received its own review owner instead of being promoted from average-only gains.
