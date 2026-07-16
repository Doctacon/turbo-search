Status: active
Created: 2026-07-15
Updated: 2026-07-15
Parent: .10x/tickets/2026-07-15-buoy-v0-3-0-release-plan.md
Depends-On: None

# Prepare Buoy v0.3.0

## Scope

- Bump `pyproject.toml`, `src/buoy_search/__init__.py`, and lock metadata to 0.3.0.
- Move current release changes from Unreleased into a pending 0.3.0 changelog section covering production catalog, apply registration/recovery, opt-in auto-routing, and migration to the `.buoy` default.
- Update release documentation/examples to v0.3.0 where they describe the next release procedure.
- Retain deprecated `turbo-search` and `TURBO_SEARCH_*` aliases through 0.3 and update their announced removal target to 0.4; do not alter compatibility implementation.
- Run full CI-equivalent tests, build, tag/version dry checks, artifact inspection, docs/reference checks, and independent review.
- Land through a passing `work/* -> develop` pull request using squash merge.

## Acceptance criteria

- All authoritative version fields and built artifact names/metadata are exactly 0.3.0.
- Changelog is accurate, pending until hosted release verification, and retains valid compare links.
- Deprecated aliases still work and documentation consistently targets removal in 0.4.
- Python 3.11, Python 3.13, Build distributions, full local tests, and release dry checks pass.
- No tag, GitHub Release, main mutation, PyPI, or Turbopuffer operation occurs.

## Explicit exclusions

Alias removal, state-root compatibility removal, release tag creation, main promotion, unrelated cleanup.

## References

- `.10x/decisions/buoy-product-identity-and-compatibility-v0-3.md`
- `.10x/specs/buoy-package-and-cli-identity.md`
- `.10x/specs/buoy-local-compatibility.md`
- `.10x/specs/buoy-ci-and-github-releases.md`
- `.10x/specs/protected-github-branches.md`
- `docs/releasing.md`

## Evidence expectations

Exact version diffs, validation/build commands, artifact inventory, CI run/check URLs, compatibility checks, and independent review.

## Blockers

None.

## Progress and notes

- 2026-07-15: Marked active. Bumped project/module/lock metadata to 0.3.0; prepared the pending changelog; aligned release/migration docs, active identity/compatibility specs, warnings, and tests with retained aliases through 0.3 and removal target 0.4.
- 2026-07-15: Local preparation validation passed: 364 tests on Python 3.11 and 364 on Python 3.13, 48 focused release/CLI tests, exact tag/assets dry checks, lock/compile/reference/diff checks, two-artifact build and metadata/content inspection, and isolated wheel/legacy-alias checks. Evidence: `.10x/evidence/2026-07-15-buoy-v0-3-0-preparation.md`; artifact inventory: `.10x/evidence/.storage/2026-07-15-buoy-v0-3-0-preparation-artifacts.json`. Ticket remains active for independent review and hosted PR checks.
