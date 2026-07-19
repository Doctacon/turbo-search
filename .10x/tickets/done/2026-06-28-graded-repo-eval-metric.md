Status: done
Created: 2026-06-28
Updated: 2026-06-28
Parent: .10x/tickets/done/2026-06-28-repo-search-eval-autoresearch-plan.md
Depends-On: None

# Graded Repo Eval Metric

## Scope

Implement deterministic graded repository search metrics governed by `.10x/specs/repo-search-eval-autoresearch.md`.

This ticket may extend `src/turbo_search/evals.py`, tests, and CLI/report plumbing needed to expose the composite metric. It must preserve backward compatibility for the existing smoke eval dataset.

## Acceptance criteria

- Eval cases can include graded judgments with `repo_path`, `url`, optional `section_path`, `grade`, and optional `reason`.
- Existing `expected_urls` / `expected_topics` datasets still load and score as before or through a compatibility adapter.
- Metric math is implemented for:
  - NDCG@10;
  - Recall@10;
  - MRR@10;
  - Precision@5;
  - `repo_search_score` using the spec weights.
- Matching is deterministic and covers URL and repo path cases.
- Tests cover perfect ranking, partial ranking, no match, duplicate hit handling, and invalid dataset validation.

## Explicit exclusions

- LLM judging.
- Reranker or query-rewriting implementation.
- Live turbopuffer calls beyond existing eval command behavior.

## Evidence expectations

- Focused `unittest` output for eval metric tests.
- Full relevant test suite output after integration.

## References

- `.10x/specs/repo-search-eval-autoresearch.md`
- `src/turbo_search/evals.py`
- `tests/test_evals.py`

## Progress and notes

- 2026-06-28: Implemented graded `EvalJudgment` loading and validation while preserving legacy `expected_urls`/`expected_topics` compatibility.
- 2026-06-28: Implemented deterministic matching for normalized URLs, repo paths in hit fields/source metadata/attributes/GitHub blob URLs, and optional section containment.
- 2026-06-28: Implemented NDCG@10, Recall@10, MRR@10, Precision@5, and weighted `repo_search_score`.
- 2026-06-28: Added tests for perfect ranking, partial ranking, no match, duplicate hit handling, section matching, graded dataset loading, and invalid judgment validation.
- 2026-06-28: Validation recorded in `.10x/evidence/2026-06-28-graded-repo-eval-metric-validation.md`.

## Current State

Done. Graded repository eval metrics are implemented and focused tests pass.

## Blockers

- None.
