Status: done
Created: 2026-06-28
Updated: 2026-06-28
Depends-On: .10x/decisions/superseded/website-ranking-defaults.md, .10x/evidence/2026-06-28-opt-in-page-aggregation-ranking-validation.md, .10x/evidence/2026-06-28-cross-site-page-aggregation-sqlmesh-validation.md

# Promote Website Page Ranking Default

## Scope

Promote namespace-aware ranking defaults so website namespaces use page-level ranking by default while repository namespaces preserve file-level repo-code defaults.

Implement:

```text
site-* namespaces:
  ranking_mode = page
  ranking_profile = none
  ranking_pool = 20
  ranking_aggregation = max

other namespaces:
  ranking_mode = file
  ranking_profile = repo_code
  ranking_pool = 100
  ranking_aggregation = max
```

Explicit CLI flags must override namespace-derived defaults.

## Acceptance criteria

- `retrieve` and `evals` dry-runs against `site-*` namespaces resolve to page/none/pool20/max when ranking flags are omitted.
- `retrieve` and `evals` dry-runs against `github-*` namespaces resolve to file/repo_code/pool100/max when ranking flags are omitted.
- Explicit ranking CLI flags still override namespace defaults.
- Existing repo retrieval/ranking unit tests continue to pass.
- Live retrieval-only eval validates the promoted default on `site-turbopuffer-com-v1`, `site-sqlmesh-readthedocs-io-v1`, and `github-doctacon-turbo-search-v1` without writes/deletes/namespace mutation.
- Documentation explains namespace-aware defaults and opt-in capped aggregation.

## Blockers

- None. User approved promotion with “yup, send it”.

## References

- `.10x/decisions/superseded/website-ranking-defaults.md`
- `.10x/evidence/2026-06-28-opt-in-page-aggregation-ranking-validation.md`
- `.10x/evidence/2026-06-28-cross-site-page-aggregation-sqlmesh-validation.md`

## Progress and notes

- 2026-06-28: Opened after user approved promotion of website page ranking defaults.
- 2026-06-28: Implemented namespace-aware CLI/autoresearch defaults: `site-*` uses page/none/pool20/max; other namespaces preserve file/repo_code/pool100/max.
- 2026-06-28: Added tests for website defaults, GitHub defaults, and explicit override preservation.
- 2026-06-28: Live retrieval-only validation passed on `site-turbopuffer-com-v1`, `site-sqlmesh-readthedocs-io-v1`, and `github-doctacon-turbo-search-v1`. Evidence: `.10x/evidence/2026-06-28-website-page-ranking-default-promotion-validation.md`.

## Current State

Done. Website page ranking default is promoted for `site-*` namespaces; repo defaults are preserved.
