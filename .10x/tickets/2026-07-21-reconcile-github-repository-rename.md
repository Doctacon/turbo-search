Status: blocked
Created: 2026-07-21
Updated: 2026-07-21
Parent: .10x/tickets/2026-07-21-release-buoy-v0-4-1-through-main-automation.md
Depends-On: None

# Reconcile GitHub Repository Rename

## Outcome

Reconcile active repository/release authority from `Doctacon/buoy-search` to the user-ratified canonical `Doctacon/buoy` before the v0.4.1 topology bridge and promotion, while preserving immutable v0.4.0 provenance and historical source/evidence identities.

## Scope

- Introduce explicit current repository identity `Doctacon/buoy` in release automation and readiness policy.
- Preserve a separate exact legacy v0.4.0 provenance repository pin `Doctacon/buoy-search`; do not overload one constant for current and legacy identity.
- Update active release tests, fake-host fixtures, package project URLs, current changelog links, and active release documentation to canonical `https://github.com/Doctacon/buoy`.
- Inspect every old-identity occurrence and classify it as active-current (update), immutable legacy v0.4 provenance (preserve), historical record/source pin (preserve), or generic fixture (update only when it represents current repository identity).
- Update the local `origin` URL to the canonical repository after protected integration; do not rewrite historical commits or hosted release objects.
- Run focused release-policy/state-machine tests, complete locked Python 3.11/3.13 suites, deterministic build/artifact/clean-wheel checks, exact v0.4 legacy no-op inspection, and hosted CI.
- Obtain independent review and integrate through an ordinary protected squash PR to develop.

## Acceptance criteria

- Readiness accepts only exact `Doctacon/buoy:develop` for future release PRs.
- v0.4.1/future release inspection and provenance require repository `Doctacon/buoy`.
- Exact published v0.4.0 legacy no-op still accepts only immutable historical repository `Doctacon/buoy-search` plus every existing pin; no other version can use the old identity.
- Active project/changelog/docs links use canonical `Doctacon/buoy`; distribution/package/import/CLI identities remain unchanged.
- Historical evidence/source pins are not semantically rewritten.
- Tests prove current-vs-legacy repository separation and fail closed on cross-use.
- Full local/hosted validation passes with deterministic artifacts and clean install.
- No main/tag/Release/asset/provenance/PyPI/Turbopuffer/protection/product behavior mutation occurs.

## Explicit exclusions

Distribution/package/CLI rename; mutation of historical releases/provenance; rewriting historical observations or immutable experiment sources; main merge; topology bridge; tag/Release creation; PyPI; Turbopuffer; protection changes; redirect-dependent acceptance.

## References

- `.10x/decisions/buoy-product-and-repository-identity.md`
- `.10x/specs/develop-to-main-release-readiness.md`
- `.10x/specs/main-push-automatic-github-release.md`
- `.10x/specs/protected-github-branches.md`
- `.10x/tickets/2026-07-21-release-buoy-v0-4-1-through-main-automation.md`
- `.10x/tickets/2026-07-21-bridge-v0-4-squash-topology-once.md`

## Evidence expectations

Canonical hosted repository identity; classified occurrence inventory; exact diff; current/legacy state tests; local and hosted validation; artifact hashes; independent review; integrated develop identity; origin URL readback; no-live-mutation attestation.

## Blockers

Blocked until PR #94 integrates the governing rename decision/spec changes.

## Progress and notes

- 2026-07-21: During a governance push, GitHub reported the canonical repository had moved to `Doctacon/buoy`. The user confirmed the rename was intentional and authorized reconciliation. No release, branch, protection, provider, or product state changed during shaping.
