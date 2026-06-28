Status: done
Created: 2026-06-28
Updated: 2026-06-28

# Repo Search Precision State-of-the-Art and Hypotheses

## Question

What are 10 evidence-backed hypotheses for improving `turbo-search` repository-search `Precision@5` after the live baseline scored `precision_at_5 = 0.300` and `repo_search_score = 59.967` on the assistant-drafted seed eval dataset?

## Sources and methods

Local evidence inspected:

- `autoresearch/runs/repo-search-live-baseline-20260628/result.json`
- `.10x/evidence/2026-06-28-live-turbo-search-repo-index-and-eval.md`
- `.10x/specs/repo-search-eval-autoresearch.md`
- `src/turbo_search/data/turbo_search_repo_search_seed_evals.json`

Observed baseline patterns:

- Aggregate live metrics: `Precision@5 = 0.300`, `NDCG@10 = 0.612`, `Recall@10 = 0.633`, `MRR@10 = 0.708`, `repo_search_score = 59.967`.
- All 10 cases passed because at least one judged file appeared in top 10.
- Duplicate chunks from the same `repo_path` frequently consumed top-5 slots.
- `docs/generic-site-rag-plan-apply.md`, `src/turbo_search/github_repo.py`, `.pi/skills/...`, and README/docs appeared often in top-5 results.
- Lowest-scoring cases were `apply-preflight-approved-safety`, `evals-composite-metrics`, and `plan-command-local-only`.

External research inspected with web search/content extraction:

- Azure AI Search hybrid RRF docs: https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking
- Azure RAG information retrieval guidance: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-information-retrieval
- Azure RAG chunk enrichment guidance: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-enrichment-phase
- Cohere reranking best practices: https://docs.cohere.com/docs/reranking-best-practices
- Vespa RAG Blueprint: https://blog.vespa.ai/the-rag-blueprint/
- Repository-level Code Search with Neural Retrieval Methods: https://arxiv.org/html/2502.07067
- flupkede/codesearch README and repository structure: https://github.com/flupkede/codesearch
- Vera README and repository structure: https://github.com/lemon07r/Vera

## State-of-the-art summary

The strongest current pattern for precision-oriented RAG/code search is multi-stage retrieval:

1. broad sparse + dense retrieval;
2. fusion, commonly Reciprocal Rank Fusion;
3. metadata/path filtering and field weighting;
4. second-stage reranking with a cross-encoder, ColBERT/late-interaction model, or learned ranker;
5. deduplication/diversification before returning the top-k user-visible results.

For repository/code search specifically, recent systems emphasize file-level retrieval, code-aware reranking, repository structure, symbol/path metadata, AST or line-aware chunks, and max-pooling over file chunks. The CMU repository-level code search paper reports up to 80% improvements over BM25 in MAP/MRR/P@1 with a BM25 plus neural reranking pipeline, and found CodeReranker at depth ~100 especially strong. Practical open-source code-search systems such as `codesearch` combine vector search, BM25, RRF, AST-aware chunking, symbol navigation, and compact metadata-first results.

## Ten hypotheses

1. **Collapse top-k results by `repo_path` before scoring/returning.**
   - Rationale: The live baseline repeatedly returned multiple chunks from the same file in top 5. Since eval judgments are path-level, duplicate chunks lower effective `Precision@5`.
   - Experiment: Group candidate hits by `repo_path`, keep the best scoring chunk per file, then return top 5 files/chunks.
   - Expected effect: High immediate precision gain; low implementation risk.

2. **Add file-level max-pooling/parent-child ranking.**
   - Rationale: Repository-level search papers rank files, not arbitrary chunks, and use max-pooling over file passages/patches because one relevant section can make a whole file relevant.
   - Experiment: Retrieve top N chunks, aggregate per file by max or softmax of fused score, then choose the best representative chunk from top files.
   - Expected effect: Improves path-level precision and NDCG, especially for long implementation files.

3. **Use a code/source-first query profile with path/doc_kind priors.**
   - Rationale: Docs and `.pi/skills` often outranked implementation files even when the judged answer was source code. Azure guidance recommends filters/field weighting; code-search tools expose mode/profile choices.
   - Experiment: Add a retrieval profile that boosts `src/`, `tests/`, and `doc_kind=code`; demotes operational docs and skills unless the query/document labels indicate docs are likely relevant.
   - Expected effect: Improves precision on implementation questions; risk is hurting doc-oriented cases unless profile selection is query-aware.

4. **Improve index hygiene with configurable repository exclusions.**
   - Rationale: `.pi/skills/...` and broad workflow docs are legitimate files but can be distractors for code-search evals. Separate corpora or source profiles are common production practice.
   - Experiment: Re-index with configurable excludes for `.pi/`, `.10x/`, `.loom/`, generated artifacts, and optionally process docs; compare against baseline.
   - Expected effect: Likely precision gain for code-search workloads; must preserve a docs-inclusive profile for documentation queries.

5. **Add an open-source cross-encoder/code reranker over top 50-100 candidates.**
   - Rationale: Cohere and Azure guidance both recommend reranking after broader retrieval. The repository-level code-search paper found neural CodeReranker materially improved P@1/MRR over BM25 and commit-message matching.
   - Experiment: Locally rerank top 50 or 100 candidates with an open-source reranker such as a BGE reranker or CodeBERT-style cross-encoder, then return top 5.
   - Expected effect: Strong precision gain; cost is latency and dependency/model management.

6. **Evaluate a code-aware embedding model instead of only `BAAI/bge-small-en-v1.5`.**
   - Rationale: Current embeddings are general-purpose. Code-search literature uses CodeBERT/GraphCodeBERT/CodeT5-style models because code identifiers, syntax, and comments differ from prose.
   - Experiment: Build a second namespace using an open-source code embedding candidate after license review, then run the same eval.
   - Expected effect: May improve semantic matching on code-specific queries; risk is worse documentation matching.

7. **Index symbol/path/identifier metadata as first-class searchable text.**
   - Rationale: Azure chunk enrichment guidance emphasizes titles, keywords, entities, tags, and metadata. Code search particularly benefits from paths, basenames, function/class names, and split identifiers.
   - Experiment: Add normalized searchable fields/text for `repo_path`, basename, module path, symbol names, heading names, and split snake_case/CamelCase tokens.
   - Expected effect: Improves exact-match and intent-match precision for queries naming concepts like `apply`, `evals`, `plan`, `GitHub`, and `retriever`.

8. **Use syntax-aware or line-window code chunking with symbol breadcrumbs.**
   - Rationale: Practical tools use tree-sitter/AST chunks; the CMU paper found line-wise code windows worked best for its CodeReranker, while function parsing remained useful context. Current chunks can produce repeated broad file matches.
   - Experiment: Compare current line chunks with tree-sitter function/class chunks and fixed line windows carrying function/class breadcrumbs.
   - Expected effect: Better candidate specificity; may reduce false positives if combined with dedup/file aggregation.

9. **Tune hybrid fusion, candidate depth, and BM25/vector weights by eval.**
   - Rationale: Azure RRF docs note weighting vector queries changes contribution to fused ranking; RAG guidance recommends experimenting with fields/search types. Current config is one fixed hybrid plan.
   - Experiment: Run config-only grids over BM25 boost, vector candidate count, text candidate count, RRF depth, and exact-vs-ANN retrieval where practical.
   - Expected effect: Moderate precision gain with no source mutation; risk is overfitting 10 draft eval cases.

10. **Train or hand-tune a lightweight learning-to-rank layer from better labels.**
    - Rationale: Vespa’s RAG Blueprint argues production-quality ranking often requires learned weighting of retrieval features. Current labels are assistant-drafted and too small for robust training, but enough to define features.
    - Experiment: After human-calibrating 30-50 representative queries, learn or hand-tune a ranker over features such as vector rank, BM25 rank, path prior, doc_kind, duplicate count, file basename match, section heading match, and reranker score.
    - Expected effect: Strongest long-term precision path; requires better ground truth.

## Recommended first three experiments

1. Collapse/diversify by `repo_path` before top-k return.
2. Run config-only hybrid/fusion grid, including source-first profile if available.
3. Add a local open-source reranker over top 50-100 candidates and measure latency plus precision.

These three match the observed failure mode, require minimal product semantics, and align with state-of-the-art multi-stage retrieval practice.

## Limits

The seed eval labels are assistant-drafted and path-level, not human-approved ground truth. Any optimization can overfit the 10 current cases. Precision improvements should be validated on a larger, reviewed dataset before becoming the default retrieval behavior.
