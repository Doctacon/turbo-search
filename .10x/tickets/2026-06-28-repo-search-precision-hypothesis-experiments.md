Status: done
Created: 2026-06-28
Updated: 2026-06-28
Parent: .10x/tickets/2026-06-28-repo-search-eval-autoresearch-plan.md
Depends-On: .10x/research/2026-06-28-repo-search-precision-state-of-art.md

# Repo Search Precision Hypothesis Experiments

## Scope

Execute the first three hypotheses from `.10x/research/2026-06-28-repo-search-precision-state-of-art.md` sequentially against the applied `github-doctacon-turbo-search-v1` namespace:

1. collapse/diversify results by `repo_path` before top-k;
2. file-level aggregation/max-pooling before top-k;
3. source-first retrieval/profile reranking using path/doc-type priors.

Run multiple variants per hypothesis to test consistency. This ticket is experiment-only unless explicitly promoted later.

## Acceptance criteria

- Baseline live repo-search metrics are restated.
- Each of the first three hypotheses has at least three measured variants where practical.
- Each variant reports `Precision@5`, composite score, NDCG@10, Recall@10, MRR@10, passed/total, and case-level effects.
- Results are compared against baseline and summarized as consistent, mixed, or negative.
- No live apply, delete, namespace-management, or source-code mutation occurs.
- Evidence is recorded with command shapes and no secrets.

## Explicit exclusions

- No turbopuffer writes, namespace creation, namespace deletion, or stale deletion.
- No production default retrieval behavior change.
- No source-code mutation for this experiment ticket.
- No private repository support.
- No claim that assistant-drafted seed labels are human-approved ground truth.

## References

- `.10x/research/2026-06-28-repo-search-precision-state-of-art.md`
- `.10x/evidence/2026-06-28-live-turbo-search-repo-index-and-eval.md`
- `autoresearch/runs/repo-search-live-baseline-20260628/result.json`
- `src/turbo_search/data/turbo_search_repo_search_seed_evals.json`

## Evidence expectations

- Experiment output artifact under `autoresearch/runs/`.
- Evidence record under `.10x/evidence/`.

## Progress and notes

- 2026-06-28: Opened for sequential live retrieval-only experiments after user requested execution of first three precision hypotheses.
- 2026-06-28: Ran live retrieval-only pools for top 10, 20, 50, and 100 with candidate counts 100 and 200.
- 2026-06-28: Evaluated 27 variants: 1 baseline rerun, 4 H1 repo-path collapse variants, 12 H2 file-level aggregation variants, and 10 H3 source-first path-profile variants.
- 2026-06-28: Evidence recorded in `.10x/evidence/2026-06-28-repo-search-precision-hypothesis-experiments.md`.
- 2026-06-28: Full artifacts written under `autoresearch/runs/precision-hypothesis-experiments-20260628/`.

## Current State

Done. All three hypotheses improved Precision@5 consistently over the baseline. Best observed variant was `h3-demote-process-docs-rrf-top100-c200` with `Precision@5 = 0.500` and `repo_search_score = 87.251` versus baseline `Precision@5 = 0.300` and score `59.967`.

## Blockers

- None.

## Follow-up signals

- Promote repo-path collapse/file-level aggregation as an experimental retrieval option before changing defaults.
- Keep source-first behavior configurable and gentle; strict source-only/source-heavy profiles can reduce recall.
- Expand and human-review the eval dataset before treating these results as production default evidence.
