Status: active
Created: 2026-06-28
Updated: 2026-06-28
Depends-On: .10x/evidence/2026-06-28-repo-search-file-ranking-promotion-validation.md, .10x/research/2026-06-28-repo-search-precision-state-of-art.md

# Repo Search Heavy Ranking Experiments

## Scope

Evaluate the heavier remaining precision hypotheses after the default file-level ranking promotion:

- open-source/local rerankers over top candidates;
- code-aware embedding model candidates;
- symbol/path/identifier metadata enrichment;
- syntax-aware or symbol-breadcrumb chunking;
- lightweight learning-to-rank after labels are expanded/reviewed.

## Acceptance criteria

- Each experiment is isolated from production defaults until evidence supports promotion.
- Proprietary model APIs are not used.
- New namespaces are used for re-indexing experiments; existing baseline namespaces are not deleted or mutated without a separate approval.
- Results compare against the post-promotion default baseline from `.10x/evidence/2026-06-28-repo-search-file-ranking-promotion-validation.md`.
- Any source changes have tests and live retrieval-only eval evidence.

## Blockers

- None for the completed local reranker slice.
- The next specific heavy experiment is not yet selected. Evidence points toward page-level website ranking/dedup before more reranker work.
- Larger/human-reviewed labels remain recommended before learning-to-rank or model-default promotion.

## References

- `.10x/research/2026-06-28-repo-search-precision-state-of-art.md`
- `.10x/evidence/2026-06-28-repo-search-file-ranking-promotion-validation.md`

## Progress and notes

- 2026-06-28: Opened as follow-up owner for heavier hypotheses not included in the file-ranking/H9/H4 execution slice.
- 2026-06-28: Activated local reranker slice for existing GitHub repo namespace `github-doctacon-turbo-search-v1` and website namespace `site-turbopuffer-com-v1`.
- 2026-06-28: Added assistant-drafted website eval dataset `src/turbo_search/data/turbopuffer_site_search_seed_evals.json` for `site-turbopuffer-com-v1`.
- 2026-06-28: Fixed schema portability for website retrieval: retry live queries without `repo_path` when a namespace schema does not contain it.
- 2026-06-28: Tested `cross-encoder/ms-marco-MiniLM-L-6-v2` and `BAAI/bge-reranker-base` reranker variants across repo and website corpora. Evidence: `.10x/evidence/2026-06-28-local-reranker-repo-and-site-validation.md`.
- 2026-06-28: Result: local rerankers should not be promoted as default for repo search; website search improved slightly on Precision@5 when reranking was combined with URL/page collapse.
