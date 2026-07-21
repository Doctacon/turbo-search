Status: blocked
Created: 2026-07-21
Updated: 2026-07-21
Parent: .10x/tickets/2026-07-21-label-driven-automatic-release-plan.md
Depends-On: .10x/tickets/2026-07-21-implement-label-driven-main-push-release.md

# Configure Label-Driven Release Hosting

## Scope

After reviewed repository integration, configure GitHub `Doctacon/buoy`: enable repository auto-merge; create exact labels `release:patch`, `release:minor`, `release:major` with documented descriptions/colors; verify main protection requires the four exact app-bound readiness job names and develop protection is unchanged. Record before/after API state.

## Acceptance criteria

- Integrated workflows emit exact configured contexts.
- Auto-merge is enabled; merge commits remain enabled.
- Exact three labels exist with no ambiguous alias.
- Main/develop protection matches active spec; no weakening, force push, environment, tag/Release/provider/product mutation.
- Independent read-only review passes.

## Explicit exclusions

PR #93 labeling/merge; release publication; source edits; PyPI; Turbopuffer; protection weakening.

## References

- `.10x/specs/develop-to-main-release-readiness.md`
- `.10x/specs/protected-github-branches.md`
- `.10x/tickets/2026-07-21-implement-label-driven-main-push-release.md`

## Evidence expectations

Exact hosted before/after/readback, label IDs/descriptions, workflow contexts, protection, independent review.

## Blockers

Blocked on reviewed repository implementation integration.
