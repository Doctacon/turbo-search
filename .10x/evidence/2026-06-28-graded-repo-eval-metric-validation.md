Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/done/2026-06-28-graded-repo-eval-metric.md

# Graded Repo Eval Metric Validation

## What was observed

Implemented deterministic graded repository eval support while preserving existing smoke eval behavior.

Changed files:

- `src/turbo_search/evals.py`
  - Added `EvalJudgment` for graded `repo_path`/`url`/`section_path` judgments.
  - Added graded dataset loading while preserving legacy `expected_urls`/`expected_topics` datasets.
  - Added deterministic matching for normalized URLs, repo paths in hit fields/source metadata/attributes/GitHub blob URLs, and optional section containment.
  - Added NDCG@10, Recall@10, MRR@10, Precision@5, and weighted `repo_search_score`.
  - Added aggregate repo metric reporting for graded live eval runs without adding live write/delete behavior.
- `tests/test_evals.py`
  - Added coverage for graded dataset loading, perfect/partial/no-match metric math, duplicate hit handling, section matching, and invalid judgment validation.

Validation commands:

```bash
uv run python -m py_compile src/turbo_search/evals.py
uv run python -m unittest tests.test_evals
uv run python -m unittest tests.test_evals tests.test_cli tests.test_retriever
```

Final focused test output:

```text
............
----------------------------------------------------------------------
Ran 12 tests in 0.005s

OK
```

Relevant integration test output:

```text
.................................
----------------------------------------------------------------------
Ran 33 tests in 0.033s

OK
```

## Procedure

1. Read the executable ticket and governing spec.
2. Extended the existing eval harness rather than adding a separate live path.
3. Preserved legacy smoke eval APIs and dataset compatibility.
4. Added deterministic graded metric and matching tests.
5. Ran focused validation.

## What this supports or challenges

Supports acceptance criteria for `.10x/tickets/done/2026-06-28-graded-repo-eval-metric.md`:

- graded judgments are loadable and validated;
- legacy smoke eval datasets still load and score;
- all requested component metrics and composite score are implemented;
- deterministic URL/repo path/section matching is covered;
- tests cover perfect, partial, no-match, duplicate, and invalid dataset cases.

## Limits

No live turbopuffer retrieval was run for this ticket. No LLM judging, reranking, query rewriting, seed dataset, or autoresearch runner behavior was implemented; those are explicitly out of scope for this child ticket.
