Status: recorded
Created: 2026-07-21
Updated: 2026-07-21
Target: PR #82 at `ac1c51be2c251ff2f4d0ff2114094e6d1b455c72`
Verdict: fail

# Buoy v0.4.0 Release Candidate Review

## Findings

Independent review confirmed the changelog, exact 0.4.0 version metadata, artifact identities/inventory, removed and retained compatibility, digest-verified 0.3.0 upgrade behavior, locked-source tests/validators, exact-head hosted CI, and no-live boundaries.

The review found one release-blocking clean-install defect:

- `src/buoy_search/treatment_token_budget.py` requires exactly `transformers==5.12.1` before loading the bundled tokenizer;
- distributable metadata declared only unpinned `sentence-transformers`, so a normal clean CPython 3.13 artifact installation resolved `transformers==5.14.1`;
- the exact four tokenizer files and identity were present, but `load_pinned_tokenizer()` failed with `TreatmentTokenBudgetError: pinned tokenizer package mismatch: transformers==5.12.1 required`;
- locked-source CI did not expose this because `uv sync --locked` selected 5.12.1.

## Verdict

Fail. PR #82 is not integration-eligible at this reviewed head. Distributable metadata must encode the exact Transformers requirement, lock/artifacts/evidence must be refreshed, and a normal clean artifact installation must actually load and exercise the bundled tokenizer before re-review.

## Residual risk

No release mutation occurred. The candidate remains blocked until the repaired artifact-level behavior independently passes.
