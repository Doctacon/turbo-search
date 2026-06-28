Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/2026-06-28-repo-search-heavy-ranking-experiments.md, .10x/knowledge/repo-search-ranking-defaults.md

# Local Reranker Repo and Website Validation

## What was observed

Tested local open-source cross-encoder reranking on both:

- GitHub repo namespace: `github-doctacon-turbo-search-v1`
- Website namespace: `site-turbopuffer-com-v1` for `https://turbopuffer.com/`

No live writes, deletes, stale deletes, namespace management, or proprietary model APIs were used for reranker experiments. Live turbopuffer calls were retrieval-only.

Added assistant-drafted website eval dataset:

- `src/turbo_search/data/turbopuffer_site_search_seed_evals.json`

The website labels are not human-approved ground truth.

## Required retrieval fix

Live website retrieval initially failed because the generic retrieval request asked turbopuffer for `repo_path`, but the `site-turbopuffer-com-v1` website schema does not contain that attribute:

```text
attribute "repo_path" not found in schema, cannot be part of include_attributes
```

Implemented schema fallback in `src/turbo_search/retriever.py`: when a live query fails because `repo_path` is missing from the schema, retry the same query without `repo_path` in `include_attributes`. Added unit coverage in `tests/test_retriever.py`.

## Validation commands

```bash
uv run python -m unittest tests.test_retriever tests.test_cli tests.test_autoresearch tests.test_evals
uv run python -m unittest discover tests
git diff --check
```

Observed:

```text
47 tests OK
124 tests OK
git diff --check: no whitespace errors
```

## Website baseline

Command shape:

```bash
uv run turbo-search evals \
  --live \
  --dataset src/turbo_search/data/turbopuffer_site_search_seed_evals.json \
  --namespace site-turbopuffer-com-v1 \
  --top-k 10 \
  --json > autoresearch/runs/turbopuffer-site-default-ranking-20260628/result.json
```

Key output:

```json
{
  "passed": 10,
  "total": 10,
  "precision_at_5": 0.2,
  "repo_search_score": 59.73415602338338,
  "ndcg_at_10": 0.6807725337584856,
  "recall_at_10": 0.4833333333333333,
  "mrr_at_10": 0.7083333333333333
}
```

## Reranker models tested

1. `cross-encoder/ms-marco-MiniLM-L-6-v2`
2. `BAAI/bge-reranker-base`

Both were loaded through `sentence_transformers.CrossEncoder` and run locally. No proprietary API calls were made.

Experiment variants for each corpus/model:

- baseline default retrieval;
- raw chunk baseline;
- collapse/dedupe preserving raw order;
- rerank raw top 50;
- rerank raw top 100;
- rerank then collapse;
- collapse then rerank.

## MiniLM cross-encoder results

Artifact:

- `autoresearch/runs/local-reranker-repo-and-site-20260628/results.json`
- `autoresearch/runs/local-reranker-repo-and-site-20260628/report.md`

### GitHub repo

Default baseline remains best:

```text
baseline-default: P@5 0.500, score 87.251
cross-encoder-rerank-raw100-collapse: P@5 0.500, score 81.884
collapse-first-raw100: P@5 0.460, score 71.083
```

MiniLM did not improve repo precision over the promoted default. It matched P@5 in one variant but reduced composite score.

### turbopuffer.com website

Best MiniLM variants:

```text
cross-encoder-rerank-raw100-collapse: P@5 0.240, score 63.234
cross-encoder-rerank-raw50-collapse: P@5 0.240, score 62.973
collapse-then-cross-encoder-rerank-50: P@5 0.240, score 59.820
baseline-default: P@5 0.200, score 59.734
```

MiniLM modestly improved website Precision@5 from 0.200 to 0.240 in collapse-combined variants.

## BGE reranker results

Artifact:

- `autoresearch/runs/local-bge-reranker-repo-and-site-20260628/results.json`
- `autoresearch/runs/local-bge-reranker-repo-and-site-20260628/report.md`

### GitHub repo

Default baseline remains best:

```text
baseline-default: P@5 0.500, score 87.251
bge-rerank-raw100-collapse: P@5 0.480, score 78.036
bge-rerank-raw50-collapse: P@5 0.460, score 74.800
```

BGE did not improve repo precision or composite score over the promoted default.

### turbopuffer.com website

Best BGE variants:

```text
collapse-then-bge-rerank-50: P@5 0.240, score 66.935
collapse-then-bge-rerank-100: P@5 0.240, score 64.661
bge-rerank-raw50-collapse: P@5 0.220, score 64.101
collapse-first-raw100: P@5 0.200, score 67.415
baseline-default: P@5 0.200, score 59.734
```

BGE modestly improved website Precision@5 to 0.240 when reranking page-collapsed candidates. Pure page collapse had the best website composite score but did not improve Precision@5.

## What this supports or challenges

Supports:

- The promoted repo default is strong enough that generic local rerankers should not be promoted for GitHub repo search yet.
- Website search needs its own page-level strategy; repository-only `repo_path` grouping does not help website duplicate URL/page chunks.
- Local reranking can modestly improve website Precision@5 when combined with URL/page collapse.
- Website retrieval must be schema-portable; repository metadata attributes cannot be required for every namespace.

Challenges:

- Generic open-source rerankers are not automatically better than the file-level/path-profile default for code repository search.
- Website composite and Precision@5 respond differently: URL/page collapse improved composite score more than reranking, while reranking improved Precision@5 slightly.
- The website seed dataset is assistant-drafted and small; results are directional, not production-grade.

## Recommended next action

Do not promote local reranking as a default. Next high-value experiment should be page-level website ranking/dedup as a first-class retrieval mode, then compare it across both `site-turbopuffer-com-v1` and repo namespaces.

## Limits

No source-code changes were made to implement production reranking. The only code change in this slice was the schema-portability fallback needed for website retrieval. No namespace writes/deletes were run. No secrets were recorded.
