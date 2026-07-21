Status: done
Created: 2026-07-14
Updated: 2026-07-19
Parent: None
Depends-On: None

# Make Planning Single-Pass and Stage-Timed

## Scope

Measure sitemap-policy, crawl, corpus write, chunking, diff, artifact construction, and publication durations; reuse each source's existing `IndexingPlan`; construct/serialize complete artifacts once while preserving outputs, hashes, progress, and source behavior.

## Acceptance criteria

- Website, repository, and local-document plan paths call corpus processing once.
- Complete chunk serialization/artifact construction occurs once per plan.
- Diagnostic timing is best-effort and cannot fail planning.
- Existing manifests/chunks/diffs/hash compatibility remain stable.
- Focused call-count/equivalence tests, full suite, retained-corpus benchmark, and review pass.

## Exclusions

Live crawl benchmarking without approval, chunk semantic changes, crawler rewrite, and concurrency changes.

## References

- `.10x/reviews/2026-07-14-buoy-performance-ux-codebase-review.md`

## Progress and notes

- 2026-07-14: Reused source-built `IndexingPlan` across website/repository/local-document plans, reduced complete artifact construction to one call, added best-effort stage timing, and added focused coverage. Full 247-test suite/build/lock/diff checks pass. Retained 8,749-chunk corpus benchmark reduced duplicate post-fetch work from median 6.350s to 3.195s (49.7%). Evidence: `.10x/evidence/2026-07-14-single-pass-plan-and-stage-timing.md`.
- 2026-07-14: Repaired closure-test gap with exact one-process/one-artifact assertions for website, repository, and local-document plan paths plus old-pattern/full-rebuild equivalence coverage (only `created_at` treated as volatile). Focused 145 and full 248 tests, build, lock, and diff checks pass.
- 2026-07-19: Closure review reconciled every criterion to the existing validation record and materially inspected the current single-pass implementation and exact call-count/equivalence tests. Commit `aa6110d` remains an ancestor of the reviewed head. Review: `.10x/reviews/2026-07-19-stale-ticket-status-closure-review.md`.

## Blockers

None.

## Closure mapping

- One corpus-processing pass and one artifact build for website, repository, and local-document plan paths: exact call-count assertions documented in `.10x/evidence/2026-07-14-single-pass-plan-and-stage-timing.md` and present in the inspected current tests.
- Best-effort timing: crawler clock-failure coverage and the current `observe_monotonic`/`elapsed_since` planning path.
- Manifest, chunk, diff, hash, and output compatibility: old-pattern/full-rebuild equivalence coverage documented in the evidence.
- Focused/full validation and retained-corpus benchmark: existing command output and stored benchmark in the evidence.
- Review: `.10x/reviews/2026-07-19-stale-ticket-status-closure-review.md`.

## Retrospective

The first validation pass was too indirect for a call-count optimization. The existing repair established the durable closure technique: assert exact processing/build counts for every source path and compare complete old/new artifacts while excluding only observational `created_at`.
