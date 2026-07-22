Status: cancelled
Created: 2026-07-21
Updated: 2026-07-22
Parent: .10x/tickets/cancelled/2026-07-21-label-driven-automatic-release-plan.md
Depends-On: .10x/tickets/cancelled/2026-07-21-implement-tag-derived-package-versioning.md

# Implement Label-Driven Release Readiness

## Scope

Implement `.10x/specs/develop-to-main-release-readiness.md`: exact release-label/version plan, authoritative base tag, dynamic metadata/frozen changelog policy, full unique job names, exact-version validation/build, per-PR label-event concurrency, and a no-checkout final merge controller using exact permissions/head matching and immutable trailers. Keep main protection contexts unchanged until hosted configuration child.

## Acceptance criteria

- Exactly one patch/minor/major label computes target; all ambiguity/mismatch states fail without mutation.
- PR source/parents/tag authority/absence are exact.
- Four check-run names exactly match protection.
- Distribution uses target override and complete active release validation.
- Final merge job never checks out code, runs only after all four checks, refetches exact current metadata, and can merge only the validated exact head/plan with deterministic authority trailers.
- Dry fixtures, full suites, hosted CI, permissions/action pins, security review, and independent review pass.

## Explicit exclusions

Main-push publication; hosted label/auto-merge/protection mutation; main merge/tag/Release/PyPI/Turbopuffer/product changes.

## References

- `.10x/specs/develop-to-main-release-readiness.md`
- `.10x/specs/protected-github-branches.md`
- `.10x/tickets/cancelled/2026-07-21-implement-tag-derived-package-versioning.md`

## Evidence expectations

Label/version vectors; labeled/unlabeled concurrency; workflow/job identities; exact no-checkout permissions/head/merge/trailer proof; exact prospective fixture; target build; tests/CI/review/integration.

## Cancellation

- 2026-07-22: Cancelled at the user’s direction. For now, release-process work is abandoned; ordinary development continues on `work/*` branches in worktrees and integrates into `develop`. Existing release specifications, decisions, research, and evidence are preserved for possible later reuse.

## Blockers

Blocked on tag-derived package versioning integration.
