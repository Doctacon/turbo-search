Status: recorded
Created: 2026-07-12
Updated: 2026-07-12
Target: .10x/tickets/done/2026-07-12-approved-apply-throughput-measurement.md
Verdict: pass

# Approved Apply Throughput Measurement Review

## Findings

The first review found two blockers: timing observation could interrupt an apply after a remote operation, and stale deletes were missing from write timing. Both were repaired and independently re-reviewed.

The final review verified that:

- embedding and write batch controls remain independent and backward compatible;
- timing observations are best-effort and cannot prevent state commit or mask apply errors;
- successful stale deletes contribute to cumulative write duration and post-success progress;
- approved summaries add timing diagnostics while preflight remains local-only and omits them;
- no concurrency, retry, model, write/delete order, or state-commit behavior changed.

## Evidence

- `.10x/evidence/2026-07-12-approved-apply-throughput-measurement.md`
- Final review: `.pi-subagents/artifacts/outputs/deed12ea-0b4c-43b8-86f5-9e5752f06d1e/review/approved-apply-throughput-measurement-rereview.md`
- Parent-observed full suite: `PYTHONDONTWRITEBYTECODE=1 uv run python -m unittest discover -s tests -p 'test_*.py' -q` — 206 passed.

## Residual risk

Timing values have deterministic test coverage but have not yet been measured against a live embedding workload or Turbopuffer service.
