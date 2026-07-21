Status: done
Created: 2026-07-18
Updated: 2026-07-20
Parent: None
Depends-On: .10x/tickets/done/2026-07-18-direct-command-defaults-plan.md

# Repository Cleanup Plan

## Outcome

After the direct-command-defaults plan integrates, remove source-proven dead code and record debris, preserve valuable work from the abandoned Qdrant branch before retiring it, and shape the separately governed 0.4 compatibility removal without deleting active evidence or intentional compatibility.

The already authorized clean merged-worktree cleanup is complete and recorded at `.10x/evidence/2026-07-18-merged-worktree-cleanup.md`.

## Child sequence

1. `.10x/tickets/done/2026-07-18-triage-thistle-qdrant-dead-end.md`
2. `.10x/tickets/done/2026-07-18-enforce-website-exact-host-crawl-boundary.md`
3. `.10x/tickets/done/2026-07-18-remove-unreachable-local-catalog-persistence.md`
4. `.10x/tickets/done/2026-07-18-normalize-terminal-ticket-placement.md`
5. `.10x/tickets/done/2026-07-18-review-stale-ticket-statuses.md`
6. `.10x/tickets/done/2026-07-18-shape-v0-4-compatibility-removal.md`

Thistle triage and manifest-authorized deletion complete before the one explicitly salvaged behavior, exact-host crawler safety, is implemented. Dead local-catalog removal follows that safety repair. Record placement precedes status review so closure checks use the canonical graph. Compatibility shaping is last so it builds on the cleaned current state. Sitemap resource limits and MarkItDown normalization remain separate follow-up tickets rather than children of this user-authorized cleanup sequence. The parent is not executable.

## Aggregate acceptance criteria

- Dirty/unmerged work is never deleted before durable classification and salvage/disposition.
- Product-neutral Thistle exact-host crawler safety is implemented and verified; exact-chunk dedup is retired/no-action with only historical non-authoritative provenance preserved; Qdrant-specific work is retired only with preserved inventory evidence and coherent ticket statuses.
- Only production-unreachable local-catalog persistence code/tests are removed; active card/schema/remote/migrate-local behavior remains.
- All already-terminal tickets live in terminal directories with repaired references.
- Stale open/active/blocked tickets receive evidence-backed closure, cancellation/no-action rationale, or explicit remaining blockers; no closure evidence is invented.
- 0.4 compatibility removal is shaped as an explicit contract and bounded tickets, not implemented opportunistically.
- Ignored artifacts, active local state, remote namespaces, release branches/tags, and the two current dirty worktrees remain untouched unless a child explicitly governs them.

## Explicit exclusions

Deleting ignored `artifacts/`, `.buoy/`, credentials, remote namespaces, local/remote branches, release tags, the current direct-command worktree, or the Thistle worktree before triage; changing retrieval tags; implementing Node.js action upgrades; broad refactoring.

## References

- `.10x/research/2026-07-18-repository-dead-end-inventory.md`
- `.10x/evidence/2026-07-18-merged-worktree-cleanup.md`
- `.10x/tickets/done/2026-07-18-direct-command-defaults-plan.md`

## Progress and notes

- 2026-07-18: User authorized the recommended cleanup sequence. Removed 28 clean worktrees tied to merged PRs, preserved both dirty/unmerged worktrees, and recovered approximately 13.4 GB.
- 2026-07-18: Independent shaping review passed with no blockers. Review: `.10x/reviews/2026-07-18-repository-cleanup-shaping-review.md`.
- 2026-07-18: Thistle/Qdrant triage integrated at `f9fd5b3` with preservation/disposition review pass. After exact HEAD/status-manifest revalidation, removed the retired dirty worktree and local `thistle-site-test` branch under the merged deletion manifest. No external provider/container or unrelated repository state was touched. Evidence: `.10x/evidence/2026-07-18-thistle-worktree-deletion.md`.
- 2026-07-18: Post-merge audit found the exact-host spec cited an original untracked ticket as if it were addressable at commit `d7a37d7`. Repaired the provenance paragraph to cite the merged disposition research and exact path/hash inventories while stating that the retired untracked files are historical provenance, not current authority. Review: `.10x/reviews/2026-07-18-thistle-provenance-reference-repair-review.md`.
- 2026-07-18: User superseded the earlier dedup-reconciliation direction: retire exact-chunk dedup, preserve it only as historical non-authority, and salvage only the exact-host behavior from the dirty implementation.
- 2026-07-19: Stale-ticket closure review completed: five target tickets closed `done`, two were cancelled with explicit no-action rationales, and the broad repo-ranking owner remains active with exact missing closure support. No tests, benchmarks, live operations, implementation repair, default changes, or residual-risk acceptance occurred. Review: `.10x/reviews/2026-07-19-stale-ticket-status-closure-review.md`.
- 2026-07-19: Final compatibility-shaping child completed after user ratification. Two focused active specs, a non-executable implementation plan, two bounded executable children, and a separate stale-guidance owner captured the 0.4.0 contract. Review response: `.10x/reviews/2026-07-19-v0-4-compatibility-removal-shaping-review-response.md`. The subsequently authorized implementation completed separately under `.10x/tickets/done/2026-07-19-buoy-v0-4-compatibility-removal-plan.md`.
- 2026-07-20: Independent aggregate closure review passed at develop `474526051821425a9cba649711f793dd8e89ac9d`; all six sequenced children are terminal and every residual has a separate durable owner. Review: `.10x/reviews/2026-07-20-repository-cleanup-plan-closure-review.md`.

## Closure mapping

- Dirty-work classification and safe retirement: Thistle research, disposition review, deletion manifest, and deletion evidence.
- Exact-host safety and Qdrant/dedup retirement: focused spec, implementation evidence, independent review, and explicit no-action authority.
- Local-catalog dead-code boundary: reachability evidence and independent review preserving active behavior.
- Record normalization: terminal move/reference evidence and review.
- Stale-status reconciliation: aggregate plus independent closure reviews with unsupported work retained or cancelled truthfully.
- Compatibility shaping: user-ratified focused specs, bounded plan/tickets, and independent shaping review.
- Protected resources: child evidence confirms no unauthorized ignored-artifact, state, remote, branch/tag, or unrelated-worktree mutation.

## Retrospective

The cleanup succeeded by separating salvageable product-neutral safety from abandoned provider-specific experiments, then sequencing source cleanup before record/status cleanup. Closure reviews caught several record-graph errors that normal CI could not: missing references, incorrect dependency direction, stale blocker text, and artifact evidence self-reference. Future broad cleanups should inventory dirty work first, define terminal placement/reference checks up front, and keep release artifacts free of internal project records before final hashing.
