Status: done
Created: 2026-06-28
Updated: 2026-06-28
Depends-On: .10x/evidence/2026-06-28-repo-search-precision-hypothesis-experiments.md

# Promote Repo Search File-Level Ranking

## Scope

Decide and implement, if approved, a production or experimental retrieval mode based on the strongest precision experiments:

- collapse/diversify results by `repo_path`;
- aggregate chunk evidence at file level;
- optionally apply a gentle source-first path profile that demotes process/docs noise without strict source-only filtering.

## Acceptance criteria

- Product/API choice is explicit: default behavior change, CLI/config flag, autoresearch-only option, or no promotion.
- If implemented, behavior is covered by unit tests and at least one live retrieval-only eval comparison.
- Existing retrieval defaults are preserved unless explicitly superseded.
- Documentation states whether ranking is chunk-level, file-level, or profiled.
- No namespace writes/deletes occur unless separately authorized.

## Blockers

- None. User ratified changing defaults, creating new experiment namespaces for index hygiene, and using open-source/local models only.

## References

- `.10x/evidence/2026-06-28-repo-search-precision-hypothesis-experiments.md`
- `.10x/research/2026-06-28-repo-search-precision-state-of-art.md`
- `.10x/specs/repo-search-eval-autoresearch.md`

## Progress and notes

- 2026-06-28: Opened as durable owner for the promotion follow-up after experiments improved Precision@5 from 0.300 to 0.500 in the best variants.
- 2026-06-28: User selected `Change defaults`, `New namespaces`, and `Open local only` through the question tool. Default retrieval may be changed; current baseline namespace must not be mutated/deleted; new experiment namespaces are allowed.
- 2026-06-28: Implemented default file-level repository ranking with `repo_code` profile, `candidates=200`, and `ranking_pool=100`; added CLI/autoresearch options and tests.
- 2026-06-28: Live eval on `github-doctacon-turbo-search-v1` improved from baseline `Precision@5=0.300`, `repo_search_score=59.967` to `Precision@5=0.500`, `repo_search_score=87.251`.
- 2026-06-28: Ran H9 config grid with 21 variants; `candidates=200`, `ranking_pool=100` matched best observed score and larger values did not improve the seed eval.
- 2026-06-28: Ran H4 index hygiene experiments in new namespaces only: `github-doctacon-turbo-search-v1-no-process` and `github-doctacon-turbo-search-v1-src-tests`; both kept `Precision@5=0.500` but scored below the default baseline namespace.
- 2026-06-28: Validation passed: targeted unit tests, full unittest discovery, dry-run retrieval plan, live eval, and `git diff --check`. Evidence: `.10x/evidence/2026-06-28-repo-search-file-ranking-promotion-validation.md`.

## Current State

Done. Default retrieval/eval behavior now uses file-level repo ranking with the gentle `repo_code` path profile. The previous raw chunk order remains available through `--ranking-mode chunk --ranking-profile none`.
