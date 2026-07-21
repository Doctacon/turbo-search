Status: open
Created: 2026-07-21
Updated: 2026-07-21
Parent: .10x/tickets/2026-07-21-buoy-v0-4-0-release-plan.md
Depends-On: None

# Validate Buoy v0.4.0 Release Candidate

## Scope

- Reconcile the complete `v0.3.0..develop` release range into an accurate pending 0.4.0 changelog section without claiming blocked experiments or failed live baselines as shipped successes.
- Validate exact project/module/lock/distribution version 0.4.0 and all requirements in `.10x/specs/buoy-release-validation.md`.
- Build once in a clean temporary output, inspect wheel/sdist contents and entry points, test clean install, and test digest-verified same-environment upgrade from released 0.3.0.
- Run primary CLI checks, retained local-state/plan compatibility checks, fixture autoresearch and repository-search eval validation, local links, distribution inventory, diff hygiene, and complete Python 3.11/3.13 suites.
- Preserve all external-state boundaries and obtain independent review before closure.

## Acceptance criteria

- Pending changelog content is complete, truthful, and versioned 0.4.0 without release date/compare link.
- Every required validation in the active release-validation specification passes with reproducible evidence.
- Built artifacts contain no `.10x/**`, old console entry point, package-owned `turbo-search` launcher, or `legacy_main`; required package/data/CLI surfaces work.
- Upgrade validation verifies the immutable 0.3.0 digest and package-manager removal of only its obsolete package-owned launcher.
- No tag, Release, PyPI publication, branch merge, Turbopuffer operation, user-state mutation, or external cleanup occurs.
- Independent review passes and exact-head hosted checks pass before the child closes.

## Explicit exclusions

Main/develop ancestry changes; PR #80 merge; tag/Release creation; publication; new product behavior; live retrieval/apply/evals; user-owned launcher or state deletion.

## References

- `.10x/specs/buoy-release-validation.md`
- `.10x/specs/buoy-ci-and-github-releases.md`
- `docs/releasing.md`
- `CHANGELOG.md`

## Evidence expectations

Exact source commit; changelog range method; command matrix and exits; Python 3.11/3.13 results; artifact names/digests/inventory/metadata; clean-install and 0.3.0-upgrade observations; compatibility/eval/link results; side-effect limits; hosted checks; independent review.

## Blockers

None.

## Progress and notes

- 2026-07-21: Opened from the user's explicit v0.4.0 release request. Read-only preflight found version metadata already at 0.4.0 and the changelog still under Unreleased. No validation workflow, artifact build, source edit, tag, release, merge, or external product operation occurred.
