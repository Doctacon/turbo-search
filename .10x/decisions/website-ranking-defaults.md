Status: active
Created: 2026-06-28
Updated: 2026-06-28

# Website Ranking Defaults

## Context

Repository search already defaults to file-level ranking with the `repo_code` path profile. Website namespaces previously inherited the same default even though website rows do not have `repo_path`, so generic file ranking behaved like chunk ranking for sites.

Validated website experiments showed page-level grouping improves website retrieval quality:

- `site-turbopuffer-com-v1`: default `Precision@5 = 0.200`, score `59.734`; page/capped pool 20 `Precision@5 = 0.290`, score `71.220`.
- `site-sqlmesh-readthedocs-io-v1`: default `Precision@5 = 0.260`, score `84.484`; page max pool 20 `Precision@5 = 0.473`, score `87.460`.

Capped aggregation helped strongly on turbopuffer.com and helped SQLMesh composite at larger pools, but did not beat simple max at SQLMesh pool 20. The generalized signal is page-level grouping, not a universal capped aggregation win.

The user ratified promoting the precision-oriented website default after reviewing this evidence.

## Decision

For website namespaces, use precision-oriented page ranking defaults:

```text
ranking_mode = page
ranking_profile = none
ranking_pool = 20
ranking_aggregation = max
```

For GitHub repository namespaces, preserve the existing repository defaults:

```text
ranking_mode = file
ranking_profile = repo_code
ranking_pool = 100
ranking_aggregation = max
```

Source-kind routing is determined from namespace identity for CLI/evals/autoresearch defaults:

- `site-*` namespaces use website defaults.
- non-`site-*` namespaces use repository/general defaults unless the user passes explicit ranking options.

User-supplied ranking CLI flags override namespace defaults.

## Alternatives considered

- Keep all website ranking opt-in: rejected because two website namespaces showed page ranking improvements and the user approved promotion.
- Promote `capped_sum_3` as the website default: rejected for now because it was not uniformly better than `max` at the precision-oriented pool 20.
- Use larger pool with capped aggregation for composite/recall: rejected for default because current promotion optimizes Precision@5 and avoids lower top-5 precision.

## Consequences

- Website retrieval/evals without explicit ranking flags will return page-deduplicated results by default.
- Repository retrieval/evals remain unchanged when using `github-*` namespaces.
- `--ranking-aggregation capped-sum-3` remains available as an opt-in website tuning option.
- Future default changes should require stronger labels or additional cross-site validation.

## Evidence

- `.10x/evidence/2026-06-28-opt-in-page-aggregation-ranking-validation.md`
- `.10x/evidence/2026-06-28-cross-site-page-aggregation-sqlmesh-validation.md`
- `.10x/evidence/2026-06-28-website-ranking-evidence-hardening.md`
