Status: superseded
Created: 2026-06-28
Updated: 2026-06-28

# Namespace Ranking Defaults

Superseded-By: `.10x/decisions/namespace-ranking-defaults.md`

## Context

`turbo-search` uses namespace-aware final ranking after hybrid ANN + BM25 + RRF. Website and repository indexes have different duplicate patterns:

- website rows need page-level deduplication by canonical URL;
- GitHub repository rows need file-level grouping by `repo_path`;
- repository files may have multiple matching chunks, but repeated evidence can also over-rank broad core files.

The prior repository default briefly promoted `capped_sum_3` aggregation after it improved the `turbo-search` seed eval. Cross-repo validation on `psf/requests` showed that result does not generalize as a universal default:

```text
turbo-search clean namespace, max:          Score = 86.697
turbo-search clean namespace, capped_sum_3: Score = 89.197
psf/requests, max:                          Score = 81.809
psf/requests, capped_sum_3:                 Score = 78.229
```

The generalized repository default should therefore stay with `max`, while `capped_sum_3` remains an opt-in knob for repositories where repeated same-file evidence is known to help.

This decision supersedes `.10x/decisions/superseded/namespace-ranking-defaults-capped-sum-3.md` and preserves the website defaults from `.10x/decisions/superseded/website-ranking-defaults.md`.

## Decision

Use namespace-aware defaults:

Website namespaces (`site-*`):

```text
candidates = 200
ranking_mode = page
ranking_profile = none
ranking_pool = 20
ranking_aggregation = max
```

Repository/general namespaces, including GitHub namespaces:

```text
candidates = 200
ranking_mode = file
ranking_profile = repo_code
ranking_pool = 100
ranking_aggregation = max
```

User-supplied CLI/config ranking options continue to override namespace defaults. `--ranking-aggregation capped-sum-3` remains available for opt-in repo or website experiments.

## Alternatives considered

- Promote `capped_sum_3` for all repo namespaces: rejected after `psf/requests` cross-repo validation regressed composite score and Precision@5 versus `max`.
- Use larger ranking pools: deferred because current evidence does not show a universal default win.
- Use source-specific or learned aggregation defaults: deferred until there are more cross-repo labels.

## Consequences

- Repository retrieval/evals without explicit ranking flags use the safer single-best-file evidence default.
- `turbo-search` can still use `--ranking-aggregation capped-sum-3` when optimizing that specific namespace.
- Further repo score improvements should target index hygiene, path/symbol metadata, or an adaptive aggregation strategy validated across more repositories; scoring-only query intent, path/symbol boosts, and one-companion role diversification are now part of the `repo_code` profile.

## Evidence

- `.10x/evidence/2026-06-28-repo-capped-aggregation-default-promotion.md`
- `.10x/evidence/2026-06-28-repo-index-hygiene-and-profile-validation.md`
- `.10x/evidence/2026-06-28-cross-repo-requests-validation.md`
- `.10x/evidence/2026-06-28-repo-query-intent-profile-validation.md`
- `.10x/evidence/2026-06-28-repo-path-symbol-ranking-validation.md`
- `.10x/evidence/2026-06-28-repo-role-diversification-validation.md`
- `.10x/evidence/2026-06-28-website-ranking-evidence-hardening.md`
