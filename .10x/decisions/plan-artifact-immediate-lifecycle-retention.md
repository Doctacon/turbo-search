Status: active
Created: 2026-07-12
Updated: 2026-07-18

# Immediate Plan-Artifact Lifecycle Retention

## Context

`turbo-search plan` writes full reviewable local artifacts. They are required while a plan is pending review, preflight, retry, or approved apply, but accumulated completed/superseded plans caused multi-gigabyte local bloat.

The operator requires artifacts to be removed immediately after they are no longer needed.

## Decision

Automatically delete an entire plan artifact directory in either case:

1. its exact plan completes a successful confirmed apply (interactive `y`/`yes` or `--approve`), after remote work and local state commit both succeed; or
2. a successfully written newer plan for the same namespace supersedes it.

Pending and failed plans remain intact. `apply --dry-run`, interactive pre-prompt work, and cancellation do not delete artifacts.

This automatic lifecycle applies prospectively. Existing artifact directories are not deleted merely by upgrading; a separate explicit reconciliation/GC action is required before destructive cleanup of historical plans.

## Alternatives considered

- **Seven-day grace period:** rejected; it retains files after they are no longer needed.
- **Manual-only GC:** rejected; it requires recurring manual cleanup and permits bloat.
- **Delete pending/failed plans:** rejected; those artifacts are still needed for review, retry, and diagnosis.
- **Retroactively delete all existing plans:** rejected without a separately reviewed explicit reconciliation action.

## Consequences

- Successful applies no longer leave a reusable local plan directory.
- Users needing long-term source/audit copies must preserve them outside the automatic artifact location before confirmed apply.
- Cleanup failures must never turn a successful remote/local apply into a reported failure; they require durable local reporting and a later reconciliation path.
