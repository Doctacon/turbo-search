Status: blocked
Created: 2026-07-21
Updated: 2026-07-21
Parent: .10x/tickets/2026-07-21-label-driven-automatic-release-plan.md
Depends-On: .10x/tickets/2026-07-21-implement-label-driven-release-readiness.md

# Implement Label-Driven Main-Push Release

## Scope

Implement `.10x/specs/main-push-automatic-github-release.md`: exact merged-PR/topology/label recovery, target recomputation, dynamic exact-version validation/build, frozen-changelog policy, generated notes, and existing immutable create/no-op/permanent-fail publication state machine with current/legacy repository separation.

## Acceptance criteria

- Exact merge commit maps to exactly one valid labeled release PR; every ambiguous/wrong topology or label fails before mutation.
- Readiness and main-push compute identical base/target across patch/minor/major vectors.
- Build/install/CLI/assets use exact target override.
- Generated notes, annotated tag, assets, canonical provenance, 422 race, final downloads, no-op, and every mismatch are executable-test covered.
- Least permissions, serialization, deterministic build once, no environment/PyPI/Turbopuffer/destructive operations, full suites/CI/security/independent review pass.

## Explicit exclusions

Hosted label/auto-merge configuration; actual main merge/release; product behavior; legacy release mutation.

## References

- `.10x/specs/main-push-automatic-github-release.md`
- `.10x/specs/buoy-release-validation.md`
- `.10x/tickets/2026-07-21-implement-label-driven-release-readiness.md`

## Evidence expectations

Merged-PR API fixtures; version vectors; state matrices; permissions; deterministic artifacts; complete suites; hosted CI; independent review; protected integration.

## Blockers

Blocked on label-driven readiness integration.
