Status: active
Created: 2026-06-28
Updated: 2026-06-28

# Repo and Website Ranking Defaults

`turbo-search` retrieval defaults to hybrid ANN + BM25 + RRF followed by namespace-aware final ranking. GitHub repo planning also excludes generated/vendor directories plus local agent memory/run artifacts (`.10x/`, `.loom/`, `.pi/`, `.turbo-search/`, `artifacts/`, `autoresearch/`) and eval fixture JSON under `/data/` by default so repository search stays focused on source, tests, and user-facing docs.

Website namespaces (`site-*`) default to:

```text
candidates = 200
ranking_mode = page
ranking_profile = none
ranking_pool = 20
ranking_aggregation = max
```

Repository namespaces default to repository-aware final ranking:

```text
candidates = 200
ranking_mode = file
ranking_profile = repo_code
ranking_pool = 100
ranking_aggregation = adaptive_sum_3
```

`ranking_mode=file` groups GitHub repository hits by `repo_path` so duplicate chunks from the same file do not consume the top-k result slots. The representative chunk is the earliest fused hit for that file. `ranking_aggregation=adaptive_sum_3` uses the best chunk per file plus a small close-evidence bonus: up to two additional same-file chunks add 5% each only when their rank-derived score is at least 80% of the best chunk score. Strict `max` and full `capped_sum_3` remain opt-in.

`ranking_profile=repo_code` is a gentle post-fusion path prior for repository rows only:

- process/project-agent and run-artifact paths such as `.pi/`, `.10x/`, `.loom/`, `.claude/`, `.cursor/`, `.turbo-search/`, `artifacts/`, and `autoresearch/` are demoted strongly;
- eval/fixture/dataset JSON under `/data/` is demoted strongly so answer-key-like files do not dominate implementation queries;
- `docs/`, README/CHANGELOG, and other Markdown files are demoted gently, with a partial recovery for exact documentation filename matches such as `docs/api.rst` on API queries;
- `tests/` files get a light boost because repository evals often ask where behavior is validated;
- source/config files are mostly neutral, with conservative query-aware boosts for exact source filename matches and Python `def`/`class` declarations already present in retrieved chunks;
- when top five lacks docs/tests and rank 1 is an implementation file, one strong docs/tests companion may be promoted into slot five without replacing the top implementation hit.

Generic website rows without `repo_path` remain chunk-keyed and are not collapsed by file ranking.

Use capped URL/page-level aggregation for website experiments with:

```bash
turbo-search retrieve "..." --ranking-aggregation capped-sum-3
```

`ranking_mode=page` groups website chunks by canonical URL while repository rows still group by `repo_path`. Page ranking improved assistant-drafted website evals on `site-turbopuffer-com-v1`, `site-sqlmesh-readthedocs-io-v1`, and `site-pi-dev-v1`, so page/max/pool20 was promoted as the `site-*` default on 2026-06-28. Website capped aggregation remains opt-in because it was not uniformly better than max at the precision-oriented pool. Use raw chunk order for debugging with:

```bash
turbo-search retrieve "..." --ranking-mode chunk --ranking-profile none
```

The repo default was first promoted after live retrieval-only experiments improved the `turbo-search` seed repo eval from `Precision@5 = 0.300` and `repo_search_score = 59.967` to `Precision@5 = 0.500` and `repo_search_score = 87.251` on namespace `github-doctacon-turbo-search-v1`. A follow-up capped aggregation experiment improved `turbo-search` further, but cross-repo validation on `psf/requests` showed full capped aggregation was not a safe universal default. After current `main` shipped project-memory/eval artifacts, a clean current-main namespace plus query-intent, path/symbol, role-diversification, and adaptive aggregation profile validates `turbo-search` at `Precision@5 = 0.540`, `Recall@10 = 0.833`, `NDCG@10 = 0.922`, and `repo_search_score = 87.760`. Cross-repo validation on `psf/requests` improved from the pre-profile `repo_search_score = 81.809` to `84.426` and `Precision@5 = 0.360` to `0.420`. Third-repo validation on `pallets/click` challenged the strict max aggregation default; adaptive aggregation improved Click max from `67.150` to `72.474` without regressing turbo-search or Requests. Across three repos, adaptive aggregation scored `81.553` average versus `79.457` for max and `81.411` for capped_sum_3.

Evidence:

- `.10x/evidence/2026-06-28-repo-search-file-ranking-promotion-validation.md`
- `.10x/evidence/2026-06-28-repo-capped-aggregation-default-promotion.md`
- `.10x/evidence/2026-06-28-repo-index-hygiene-and-profile-validation.md`
- `.10x/evidence/2026-06-28-repo-path-symbol-ranking-validation.md`
- `.10x/evidence/2026-06-28-repo-role-diversification-validation.md`
- `.10x/evidence/2026-06-28-cross-repo-click-validation.md`
- `.10x/evidence/2026-06-28-repo-adaptive-aggregation-validation.md`
