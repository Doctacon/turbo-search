Status: cancelled
Created: 2026-07-21
Updated: 2026-07-22
Parent: .10x/tickets/cancelled/2026-07-21-label-driven-automatic-release-plan.md
Depends-On: .10x/tickets/cancelled/2026-07-21-implement-label-driven-release-readiness.md

# Implement Label-Driven Main-Push Release

## Scope

Implement `.10x/specs/main-push-automatic-github-release.md`: exact merged-PR/topology/immutable-trailer recovery, target recomputation, duplicate-stable-release-per-SHA rejection, dynamic exact-version validation/build, frozen-changelog policy, generated notes, and existing immutable create/no-op/permanent-fail publication state machine with current/legacy repository separation.

## Acceptance criteria

- Exact merge commit maps to one valid release PR and one exact trailer plan; mutable post-merge labels cannot change identity; every ambiguous/wrong topology/trailer or different stable release already on the SHA fails before mutation.
- Readiness and main-push compute identical base/target across patch/minor/major vectors.
- Build/install/CLI/assets use exact target override.
- Generated notes, annotated tag, assets, canonical provenance, 422 race, final downloads, no-op, and every mismatch are executable-test covered.
- Least permissions, serialization, deterministic build once, no environment/PyPI/Turbopuffer/destructive operations, full suites/CI/security/independent review pass.

## Explicit exclusions

Hosted label/auto-merge configuration; actual main merge/release; product behavior; legacy release mutation.

## References

- `.10x/specs/main-push-automatic-github-release.md`
- `.10x/specs/buoy-release-validation.md`
- `.10x/tickets/cancelled/2026-07-21-implement-label-driven-release-readiness.md`

## Evidence expectations

Merged-PR API fixtures; version vectors; state matrices; permissions; deterministic artifacts; complete suites; hosted CI; independent review; protected integration.

## Cancellation

- 2026-07-22: Cancelled at the user’s direction. For now, release-process work is abandoned; ordinary development continues on `work/*` branches in worktrees and integrates into `develop`. Existing release specifications, decisions, research, and evidence are preserved for possible later reuse.

## Blockers

Blocked on label-driven readiness integration.
