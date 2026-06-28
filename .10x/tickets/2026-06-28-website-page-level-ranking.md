Status: done
Created: 2026-06-28
Updated: 2026-06-28
Depends-On: .10x/evidence/2026-06-28-local-reranker-repo-and-site-validation.md

# Website Page-Level Ranking

## Scope

Evaluate and possibly promote page-level ranking/deduplication for website namespaces, analogous to repository file-level ranking by `repo_path`.

The `site-turbopuffer-com-v1` experiment showed that URL/page collapse improved website composite score from `59.734` to `67.415` even without improving `Precision@5`, while local reranking plus URL/page collapse improved `Precision@5` modestly to `0.240`.

## Acceptance criteria

- Website rows can be grouped by canonical `url` (or a stable page identity) without collapsing unrelated chunks incorrectly.
- Repo rows continue to group by `repo_path`.
- Generic site behavior is validated against `site-turbopuffer-com-v1` and at least one repo namespace to avoid regressions.
- Tests cover website schema without `repo_path` and URL/page grouping behavior.
- Live eval evidence compares page-level ranking against current defaults.

## Blockers

- None for experiment-first execution. User selected website page ranking and instructed not to change defaults automatically.

## References

- `.10x/evidence/2026-06-28-local-reranker-repo-and-site-validation.md`
- `src/turbo_search/data/turbopuffer_site_search_seed_evals.json`

## Progress and notes

- 2026-06-28: Opened after local reranker experiments indicated URL/page collapse is a stronger website direction than generic reranking alone.
- 2026-06-28: Activated after user selected `Website page rank` and `Experiment first` via question tool.
- 2026-06-28: Implemented opt-in `--ranking-mode page` while preserving defaults.
- 2026-06-28: Added tests for URL/page grouping and confirmed repo rows still group by `repo_path` under page mode.
- 2026-06-28: Ran live retrieval-only grid on `site-turbopuffer-com-v1` and `github-doctacon-turbo-search-v1`. Best website page variant improved Precision@5 from `0.200` to `0.270`; best composite variant improved score from `59.734` to `68.646`. Repo default was preserved. Evidence: `.10x/evidence/2026-06-28-website-page-level-ranking-validation.md`.

## Current State

Done. Page-level website ranking is available as an experimental option and is not the default.
