Status: blocked
Created: 2026-07-21
Updated: 2026-07-21
Parent: .10x/tickets/2026-07-21-label-driven-automatic-release-plan.md
Depends-On: .10x/tickets/2026-07-21-implement-tag-derived-package-versioning.md

# Implement Label-Driven Release Readiness

## Scope

Implement `.10x/specs/develop-to-main-release-readiness.md`: exact release-label/version plan, authoritative base tag, dynamic metadata/frozen changelog policy, full unique job names, exact-version validation/build, and a no-checkout same-repository auto-merge adapter requesting method MERGE. Keep main protection contexts unchanged until hosted configuration child.

## Acceptance criteria

- Exactly one patch/minor/major label computes target; all ambiguity/mismatch states fail without mutation.
- PR source/parents/tag authority/absence are exact.
- Four check-run names exactly match protection.
- Distribution uses target override and complete active release validation.
- Auto-merge adapter never checks out PR code and can only enable MERGE for exact release PR metadata.
- Dry fixtures, full suites, hosted CI, permissions/action pins, security review, and independent review pass.

## Explicit exclusions

Main-push publication; hosted label/auto-merge/protection mutation; main merge/tag/Release/PyPI/Turbopuffer/product changes.

## References

- `.10x/specs/develop-to-main-release-readiness.md`
- `.10x/specs/protected-github-branches.md`
- `.10x/tickets/2026-07-21-implement-tag-derived-package-versioning.md`

## Evidence expectations

Label/version vectors; workflow/job identities; no-checkout/permissions proof; exact prospective fixture; target build; tests/CI/review/integration.

## Blockers

Blocked on tag-derived package versioning integration.
