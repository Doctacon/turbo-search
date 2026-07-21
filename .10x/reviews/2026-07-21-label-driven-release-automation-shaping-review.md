Status: recorded
Created: 2026-07-21
Updated: 2026-07-21
Target: PR #98 label-driven automatic release shaping
Verdict: concerns

# Label-Driven Release Automation Shaping Review

## Findings

Independent review confirmed label/SemVer calculations, hatch-vcs feasibility, v0.4 authority, bridge closure, hosted protection, and child sequencing. It identified four blockers:

1. Mutable post-merge PR labels could change target on workflow rerun and create another release for the same SHA.
2. A queued `pull_request_target` auto-merge adapter lacked race/revocation/concurrency and exact-permission semantics.
3. Historical records pointed to replacement active contracts instead of the static contracts under which they executed.
4. Active package/main-push specs inherited omitted normative guarantees from superseded records instead of being regeneration-grade.

## Response

- Replaced post-merge label authority with deterministic merge-commit trailers and required main-push recomputation/equality. Added rejection of any different stable tag/Release already associated with the same main SHA.
- Replaced mutable queued auto-merge/`pull_request_target` with a final job in the readiness workflow after all four checks. It uses per-PR canceling concurrency, no checkout, exact `contents: write`/`pull-requests: write`, current metadata/plan reinspection, `--match-head-commit`, method MERGE, and immutable trailers. Later PR metadata cannot change release identity.
- Repaired historical references to exact superseded static-version/package/release contracts and relabeled historical authority accurately.
- Restated retained package identity/compatibility, exact v0.4 legacy pins/digests, state machine, permissions, triggers, tests, protection, and portability in active specs.
- Added raw disposable hatch-vcs experiment configuration, commands, lock diff, versions, and artifact hashes to research.

## Verdict

Concerns are addressed on the PR branch; final independent rereview remains before integration.

## Residual risk

The first implementation must prove the same-repository pull-request workflow token can merge through exact protection only after required jobs, and must fail closed if hosted permissions differ.
