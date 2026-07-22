Status: recorded
Created: 2026-07-22
Updated: 2026-07-22
Target: .10x/tickets/done/2026-07-22-clarify-external-backed-duckdb-views.md
Verdict: pass

# External-backed DuckDB view guidance review

## Findings

Initial review found that substring-only classification could mask an unrelated self-contained view error. The repair now requires both `duckdb.PermissionException` and a known security-boundary marker. Regression coverage proves unrelated errors remain unchanged, both markers are recognized, missing relations retain their diagnostic, and all four DuckDB security settings remain disabled.

Documentation accurately says views must be self-contained and recommends upstream materialization for external-backed or extension-dependent views.

## Verdict

Pass. No critical, blocker, or significant findings remain.

## Residual risk

A future DuckDB version could change exception classes or diagnostics; fail-closed behavior would then expose the original DuckDB error rather than weakening security.
