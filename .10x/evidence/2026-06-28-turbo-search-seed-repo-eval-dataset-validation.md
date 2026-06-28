Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/2026-06-28-turbo-search-seed-repo-eval-dataset.md

# turbo-search Seed Repo Eval Dataset Validation

## What was observed

Implemented the draft graded repository-search eval dataset for the `turbo-search` repository.

Changed files:

- `src/turbo_search/data/turbo_search_repo_search_seed_evals.json`
  - Added seed/draft metadata with `human_approved_ground_truth: false`.
  - Added 10 graded eval cases covering GitHub repository ingestion, local-only plan/apply safety, retrieval behavior, chunking/artifact generation, and eval/autoresearch behavior.
  - Each case includes at least one grade-3 judgment plus additional grade-1/2 supporting judgments.
  - Judgments use repo-relative `repo_path` locators and include reviewer-calibration reasons.
- `tests/test_evals.py`
  - Added dataset loading and metadata assertions.
  - Added coverage-area assertions for the required representative areas.
  - Added judgment validation assertions for grade-3/supporting labels, reasons, repo paths, and local path existence.

Validation command:

```bash
uv run python -m unittest tests.test_evals
```

Output:

```text
..............
----------------------------------------------------------------------
Ran 14 tests in 0.003s

OK
```

## Procedure

1. Read the ticket, governing spec, eval harness, existing eval tests, and relevant source/docs for label drafting.
2. Drafted seed labels from inspected repository source paths only; no live GitHub or turbopuffer calls were run.
3. Added tests proving the dataset loads through `load_eval_cases`, remains explicitly draft/seed, has at least 8 cases, covers expected areas, and contains valid graded judgments.
4. Ran focused unittest validation.

## What this supports or challenges

Supports the ticket acceptance criteria:

- Dataset exists under `src/turbo_search/data/`.
- Dataset contains at least 8 graded cases; it currently contains 10.
- Each case has at least one grade-3 judgment and supporting grade-1/2 judgments.
- Judgments use `repo_path` and include reasons.
- Dataset loads through the graded eval loader and is covered by focused tests.
- Dataset metadata states it is seed/draft and not human-approved ground truth.

## Limits

The labels are assistant-drafted seed labels for calibration, not final human-approved ground truth. Validation is local/unit-only; no live retrieval quality was measured in this ticket.
