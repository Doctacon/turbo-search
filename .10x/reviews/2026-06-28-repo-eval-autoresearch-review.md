Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Target: .10x/specs/repo-search-eval-autoresearch.md, .10x/tickets/done/2026-06-28-repo-search-eval-autoresearch-plan.md
Verdict: pass

# Repo Eval Autoresearch Review

## Target

Reviewed the composite repository search eval and config-only autoresearch implementation:

- `src/turbo_search/evals.py`
- `src/turbo_search/autoresearch.py`
- `src/turbo_search/data/turbo_search_repo_search_seed_evals.json`
- `tests/test_evals.py`
- `tests/test_autoresearch.py`
- `autoresearch/program.md`
- `autoresearch/experiments/repo-search-fixture-baseline.json`
- related README/docs and 10x records

## Findings

- Pass: Core spec alignment is good. Graded judgments validate grades 0-3 and require `repo_path` or `url`; object-with-`cases` datasets remain loadable.
- Pass: Metric formula matches the specified weights for NDCG@10, Recall@10, MRR@10, and Precision@5, with aggregate component means.
- Pass: Safety boundary is preserved for fixture mode and live mode. Autoresearch dispatches fixture locally or delegates live mode only to retrieval/eval code. No apply/upsert/delete/state mutation path was found.
- Pass: Tests cover metric math, matching, dataset validation, unsafe experiment fields, fixture artifact generation, and the checked-in sample runner. Relevant and full tests passed.
- Minor fixed: `repo_search_score` could slightly exceed 100 due floating-point accumulation. Fixed by clamping per-case and aggregate composite scores to the documented 0-100 range.
- Minor fixed: Top-hit summaries omitted `path`/`repo_path`, causing path-only fixture hits to render as `no locator`. Fixed by including path locators in summaries and reports.
- Blocker fixed: Follow-up review found live `SearchHit` normalization still dropped `repo_path` because retrieval did not request/preserve it. Fixed by adding `repo_path` to retrieval attributes, `SearchHit`, serialization, and row normalization. Evidence: `.10x/evidence/2026-06-28-live-retrieval-repo-path-normalization-validation.md`.
- Follow-up review: previous blocker resolved; no blocker remains.

## Verdict

Pass. No blocker remains after minor fixes recorded in `.10x/evidence/2026-06-28-repo-eval-autoresearch-review-minor-fixes.md` and live repo-path normalization recorded in `.10x/evidence/2026-06-28-live-retrieval-repo-path-normalization-validation.md`.

## Residual risk

- Seed labels are assistant-drafted and not human-approved ground truth.
- Fixture experiment validates metric/runner wiring, not live retrieval quality.
- Live `turbo-search` repo eval is pending an already-applied repository namespace; live writes/namespaces were intentionally out of scope.
