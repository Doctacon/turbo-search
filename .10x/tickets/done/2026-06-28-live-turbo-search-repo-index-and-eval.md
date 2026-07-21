Status: done
Created: 2026-06-28
Updated: 2026-06-28
Parent: .10x/tickets/done/2026-06-28-repo-search-eval-autoresearch-plan.md
Depends-On: .10x/tickets/done/2026-06-28-repo-search-eval-autoresearch-plan.md

# Live turbo-search Repo Index and Eval

## Scope

With user approval that live writes and namespaces are now in scope, create/apply the `turbo-search` GitHub repository namespace and run live retrieval-only repo eval against the seed graded dataset.

Target repository URL: `https://github.com/Doctacon/turbo-search`
Target namespace: `github-doctacon-turbo-search-v1`
Region: default `gcp-us-central1` unless runtime config overrides.

## Acceptance criteria

- Plan the public GitHub repository through the existing local-only `plan` workflow.
- Run apply preflight against the generated plan.
- Run approved apply for the generated plan and namespace, without stale deletion unless explicitly requested.
- Run live repo eval/autoresearch against the applied namespace using `src/turbo_search/data/turbo_search_repo_search_seed_evals.json`.
- Record command shapes, counts, scores, and limits without secrets.

## Explicit exclusions

- Namespace deletion.
- Stale deletion.
- Private repository support.
- Persisting or printing API keys.
- Modifying source code as part of the live operation.

## Evidence expectations

- Plan summary with source kind, namespace, selected file/chunk counts, and no turbopuffer API calls.
- Apply preflight/approved apply summaries with row counts and success state.
- Live eval result with component metrics and composite score.

## References

- `.10x/specs/repo-search-eval-autoresearch.md`
- `autoresearch/experiments/repo-search-fixture-baseline.json`
- `src/turbo_search/data/turbo_search_repo_search_seed_evals.json`

## Progress and notes

- 2026-06-28: Activated after user explicitly authorized writes and namespaces.
- 2026-06-28: Planned `https://github.com/Doctacon/turbo-search` into `artifacts/site-crawls/github-doctacon-turbo-search-plan-live`; plan selected 30 files, generated 432 chunks, and made no turbopuffer calls.
- 2026-06-28: Ran apply preflight; artifact verified, 432 rows to upsert, 0 stale rows, no live calls.
- 2026-06-28: Ran approved apply; generated 432 embeddings, upserted 432 rows to `github-doctacon-turbo-search-v1`, updated local state, and did not delete stale rows.
- 2026-06-28: Ran post-apply preflight; 432 chunks unchanged, 0 rows to upsert, 0 stale rows.
- 2026-06-28: Added `autoresearch/experiments/repo-search-live-baseline.json` and ran live retrieval-only repo eval.
- 2026-06-28: Live eval passed 10/10 cases with composite `repo_search_score` 59.96699925637771; evidence recorded in `.10x/evidence/2026-06-28-live-turbo-search-repo-index-and-eval.md`.

## Current State

Done. The public `Doctacon/turbo-search` GitHub repository is applied to namespace `github-doctacon-turbo-search-v1`, local state is updated, and a live repo-search baseline score is recorded.

## Blockers

- None.

## Follow-up signals

- Score quality is moderate despite pass rate 10/10; low-scoring cases indicate ranking/precision issues.
- The indexed corpus is the public GitHub remote commit `2b401d9b7d67ea5ade0faaf41516c86708b3df1b`, not uncommitted local working-tree changes.
