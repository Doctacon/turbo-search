Status: recorded
Created: 2026-07-19
Updated: 2026-07-19
Relates-To: .10x/tickets/done/2026-07-18-normalize-terminal-ticket-placement.md

# Terminal Ticket Placement Normalization

## What was observed

- Before mutation, exactly 20 top-level ticket records had an existing terminal status: 19 `done` and one `cancelled`.
- All 20 destination paths were absent, so the move set was collision-free.
- The move repaired 57 exact affected references across `.10x` Markdown.
- After mutation, zero top-level `.10x/tickets/*.md` records have status `done` or `cancelled`.
- All moved statuses and non-path-reference content matched their pre-move `HEAD` content.
- Reference validation found no new broken reference. The same 27 unrelated broken references existed before and after the move.
- Only `.10x` Markdown records changed. No source, runtime, test, or external state changed.

## Exact move map and normalized hashes

Every source was directly under `.10x/tickets/`; the Source filename column plus that directory is the exact old path. Each destination is the exact new path. Splitting the now-absent source directory from its filename avoids creating new broken Markdown references in this evidence record.

Each SHA-256 is the source record hash at `HEAD`. Validation replaced every new terminal path with its old path before comparison; the resulting complete content matched the corresponding source record byte-for-byte.

| Status | Source filename | Destination | Source SHA-256 |
|---|---|---|---|
| done | `2026-06-28-config-autoresearch-runner.md` | `.10x/tickets/done/2026-06-28-config-autoresearch-runner.md` | `df7254cf363e0a4588e0bb7da5645f4182c9d3b3b66bd272675927e09fbd1967` |
| done | `2026-06-28-cross-repo-requests-validation.md` | `.10x/tickets/done/2026-06-28-cross-repo-requests-validation.md` | `c9d4ed7cda8e44696c5b5564854304010b9d811457ba5a5474118d2901b93329` |
| done | `2026-06-28-cross-site-page-aggregation-validation.md` | `.10x/tickets/done/2026-06-28-cross-site-page-aggregation-validation.md` | `97c90c0e46784833ed1790bdf73680f4d25fef20756647279073ad5c3f19d04e` |
| done | `2026-06-28-graded-repo-eval-metric.md` | `.10x/tickets/done/2026-06-28-graded-repo-eval-metric.md` | `bb03f8e16d1eab5b30601a17a4785abdf1da0ea15a519a790e30aaccc5ace576` |
| cancelled | `2026-06-28-human-review-website-ranking-labels.md` | `.10x/tickets/cancelled/2026-06-28-human-review-website-ranking-labels.md` | `a52d16fb89f8aa66a89ca4e065b04a5ccb5d7da7686d21b20661932fd3aa2bb5` |
| done | `2026-06-28-live-turbo-search-repo-index-and-eval.md` | `.10x/tickets/done/2026-06-28-live-turbo-search-repo-index-and-eval.md` | `1e627bae4bff6bb9efb434dd5871dba4ac69e83603a38f7a784d5165a764c339` |
| done | `2026-06-28-opt-in-page-aggregation-ranking.md` | `.10x/tickets/done/2026-06-28-opt-in-page-aggregation-ranking.md` | `50fa9b75693765f0a9d0488c67d5d55b540933e3de0faa0b8ad9006c11ca4a36` |
| done | `2026-06-28-promote-repo-search-file-level-ranking.md` | `.10x/tickets/done/2026-06-28-promote-repo-search-file-level-ranking.md` | `e04bafe16ad12bfaf4b1730e6fce43365cb4e89d3a4abf9560915b6b405d0120` |
| done | `2026-06-28-promote-website-page-ranking-default.md` | `.10x/tickets/done/2026-06-28-promote-website-page-ranking-default.md` | `dc268559d3ca0e57de8fb62c582fa1a1e1dbf86bd8c7b8ac329b334ba6e205ca` |
| done | `2026-06-28-repo-eval-autoresearch-docs-validation.md` | `.10x/tickets/done/2026-06-28-repo-eval-autoresearch-docs-validation.md` | `d1f09d52a0b8e66a4217b83a4b7afc994709cdd61703d7012a65ca27082f1cda` |
| done | `2026-06-28-repo-file-card-metadata-indexing.md` | `.10x/tickets/done/2026-06-28-repo-file-card-metadata-indexing.md` | `b78192d862732ca1f7471904fa32dfc21c3a316ef4c7c955def28dfb9f193a5b` |
| done | `2026-06-28-repo-search-eval-autoresearch-plan.md` | `.10x/tickets/done/2026-06-28-repo-search-eval-autoresearch-plan.md` | `7f235344d2a4ec9848ec14e15ab9a55d92ce5e913811bf71f347199d957869d7` |
| done | `2026-06-28-repo-search-metadata-cross-repo-validation.md` | `.10x/tickets/done/2026-06-28-repo-search-metadata-cross-repo-validation.md` | `425a3a444fffb1dd52984142b27289469304c5173a29e97016954bd5c30e696f` |
| done | `2026-06-28-repo-search-precision-hypothesis-experiments.md` | `.10x/tickets/done/2026-06-28-repo-search-precision-hypothesis-experiments.md` | `426523f837c167b08b4e20b38711a3c46ac1b12b2c2098bf030a5101bf3a0922` |
| done | `2026-06-28-turbo-search-seed-repo-eval-dataset.md` | `.10x/tickets/done/2026-06-28-turbo-search-seed-repo-eval-dataset.md` | `959fb195f61a95dec27290e6c2ce7c8a0f3eb39dab46191ca263a51c6628e9b0` |
| done | `2026-06-28-website-page-aggregation-experiments.md` | `.10x/tickets/done/2026-06-28-website-page-aggregation-experiments.md` | `08e3fd79302199a27013bdd782461df342825e252df48178e131421c99f4fe09` |
| done | `2026-06-28-website-page-level-ranking.md` | `.10x/tickets/done/2026-06-28-website-page-level-ranking.md` | `53af3cd430dde08f055f271c4f68a1a7d59a61ac378e9881abebd8aba9fe924c` |
| done | `2026-06-28-website-ranking-default-promotion-decision.md` | `.10x/tickets/done/2026-06-28-website-ranking-default-promotion-decision.md` | `b555378c645719ca834e38027ac560a6930e448da7ee439bf535f9accda33421` |
| done | `2026-06-28-website-ranking-evidence-hardening.md` | `.10x/tickets/done/2026-06-28-website-ranking-evidence-hardening.md` | `a0d96fcfee8235411bf36a252a2017ba4bc287efa29d4ddc52288784580632e5` |
| done | `2026-07-08-local-pdf-source-ingestion.md` | `.10x/tickets/done/2026-07-08-local-pdf-source-ingestion.md` | `9c07854a07de5aae2f695485e6f632f2be632e9389523173bfb1b2f8b2188f10` |

Counts: **20 total; 19 done; one cancelled; zero collisions; 57 repaired references.**

## Procedure

1. Ran the repository-required branch/worktree inspection and confirmed `work/normalize-terminal-ticket-placement` at `326d070` with a clean starting tree.
2. Parsed only top-level `.10x/tickets/*.md` records and selected only records whose first `Status:` value was exactly `done` or `cancelled`.
3. Refused mutation if any selected destination existed; zero destinations existed.
4. Renamed `done` records into `.10x/tickets/done/` and the `cancelled` record into `.10x/tickets/cancelled/`.
5. Replaced only the 20 exact old paths with their exact terminal-directory paths across `.10x/**/*.md`.
6. Compared every destination against `git show HEAD:<source>` after normalizing only the 20 path substitutions.
7. Parsed all `.10x` Markdown references and compared the missing-reference set to the captured pre-mutation set.
8. Ran `git diff --check` and a changed-path scope check.

## Validation results

- Terminal inventory: `TOP_LEVEL_TERMINAL=0`.
- Moved-record validation: `MOVED_VALIDATED=20`, `ERRORS=0`.
- Reference repair: `EXPECTED_REPAIRED_REFERENCES=57`; no affected old path remains outside the split historical move-map notation above.
- Markdown references: 27 broken, all pre-existing and unrelated; `NEW_BROKEN=0`, `RESOLVED_UNRELATED=0`.
- Content/status preservation: each destination retained its original `Status:` and matched its complete `HEAD` source after normalizing only affected path references.
- Diff hygiene: `git diff --check` passed.
- Scope: every changed path is under `.10x/` and ends in `.md`.

## Follow-up resolution of the 27 pre-existing candidates

A follow-up audit enumerated each candidate at its original source line, searched current active, done, cancelled, and superseded records plus all Git history, and classified it before mutation. The 20 live Markdown pointers were repaired to existing terminal records. Seven strings were preserved because they are not missing current-record references: four are immutable fenced historical quotations/log output, and three are commit-qualified paths proven present in the cited tree.

The Before column deliberately splits absent working-tree paths into directory and filename so this evidence does not introduce new dangling current-path syntax. “Preserved historical text” means the source bytes were left unchanged.

| # | Source line | Missing target before | Classification | After |
|---:|---|---|---|---|
| 1 | `.10x/evidence/2026-07-12-approved-apply-progress.md:4` | `.10x/tickets/` + `2026-07-12-approved-apply-progress.md` | wrong terminal path; Git history contains only the `done/` ticket | `.10x/tickets/done/2026-07-12-approved-apply-progress.md` |
| 2 | `.10x/evidence/2026-07-12-approved-apply-throughput-measurement.md:4` | `.10x/tickets/` + `2026-07-12-approved-apply-throughput-measurement.md` | wrong terminal path; Git history contains only the `done/` ticket | `.10x/tickets/done/2026-07-12-approved-apply-throughput-measurement.md` |
| 3 | `.10x/evidence/2026-07-13-live-dagster-throughput-benchmark.md:4` | `.10x/tickets/` + `2026-07-12-live-dagster-throughput-benchmark.md` | wrong terminal path; Git history contains only the `done/` ticket | `.10x/tickets/done/2026-07-12-live-dagster-throughput-benchmark.md` |
| 4 | `.10x/evidence/2026-07-13-readme-details-on-demand-rewrite.md:4` | `.10x/tickets/` + `2026-07-13-readme-details-on-demand-rewrite.md` | wrong terminal path; Git history contains only the `done/` ticket | `.10x/tickets/done/2026-07-13-readme-details-on-demand-rewrite.md` |
| 5 | `.10x/evidence/2026-07-14-buoy-v0-2-0-release-attempt.md:4` | `.10x/tickets/` + `2026-07-14-buoy-public-ci-release-plan.md` | rename/move; history records top-level to `done/` | `.10x/tickets/done/2026-07-14-buoy-public-ci-release-plan.md` |
| 6 | `.10x/evidence/2026-07-14-finalize-v0-2-1-release-docs.md:4` | `.10x/tickets/` + `2026-07-14-finalize-v0-2-1-release-docs.md` | rename/move; history records top-level to `done/` | `.10x/tickets/done/2026-07-14-finalize-v0-2-1-release-docs.md` |
| 7 | `.10x/evidence/2026-07-14-publish-buoy-rebrand-commit.md:4` | `.10x/tickets/` + `2026-07-14-buoy-public-ci-release-plan.md` | rename/move | `.10x/tickets/done/2026-07-14-buoy-public-ci-release-plan.md` |
| 8 | `.10x/evidence/2026-07-15-bootstrap-protected-develop-branch.md:89` | `.10x/tickets/` + `2026-07-15-add-pi-worktree-governance.md` | obsolete historical pointer in fenced SHA-256 output; history records later move to `done/` | preserved historical text; current owner `.10x/tickets/done/2026-07-15-add-pi-worktree-governance.md` |
| 9 | `.10x/evidence/2026-07-15-bootstrap-protected-develop-branch.md:90` | `.10x/tickets/` + `2026-07-15-establish-protected-development-workflow.md` | obsolete historical pointer in fenced SHA-256 output; history records later move to `done/` | preserved historical text; current owner `.10x/tickets/done/2026-07-15-establish-protected-development-workflow.md` |
| 10 | `.10x/evidence/2026-07-15-bootstrap-protected-develop-branch.md:91` | `.10x/tickets/` + `2026-07-15-integrate-pi-worktree-governance.md` | obsolete historical pointer in fenced SHA-256 output; history records later move to `done/` | preserved historical text; current owner `.10x/tickets/done/2026-07-15-integrate-pi-worktree-governance.md` |
| 11 | `.10x/reviews/2026-07-12-approved-apply-progress-review.md:4` | `.10x/tickets/` + `2026-07-12-approved-apply-progress.md` | wrong terminal path | `.10x/tickets/done/2026-07-12-approved-apply-progress.md` |
| 12 | `.10x/reviews/2026-07-12-approved-apply-throughput-measurement-review.md:4` | `.10x/tickets/` + `2026-07-12-approved-apply-throughput-measurement.md` | wrong terminal path | `.10x/tickets/done/2026-07-12-approved-apply-throughput-measurement.md` |
| 13 | `.10x/reviews/2026-07-13-live-dagster-throughput-benchmark-review.md:4` | `.10x/tickets/` + `2026-07-12-live-dagster-throughput-benchmark.md` | wrong terminal path | `.10x/tickets/done/2026-07-12-live-dagster-throughput-benchmark.md` |
| 14 | `.10x/reviews/2026-07-14-readme-details-on-demand-review.md:4` | `.10x/tickets/` + `2026-07-13-readme-details-on-demand-rewrite.md` | wrong terminal path | `.10x/tickets/done/2026-07-13-readme-details-on-demand-rewrite.md` |
| 15 | `.10x/reviews/2026-07-18-thistle-provenance-reference-repair-review.md:18` | `.10x/tickets/done/` + `2026-07-11-block-cross-host-crawl-redirects.md` | obsolete historical pointer quoted in a fenced finding; history confirms it was never committed, while the surrounding review already records the actual canonical disposition | preserved historical quotation; canonical owner `.10x/research/2026-07-18-thistle-qdrant-dead-end-disposition.md` |
| 16 | `.10x/specs/sitemap-resource-limits.md:41` | commit-qualified ticket path | obsolete working-tree pointer but valid historical citation | preserved; `git cat-file -e d7a37d7:.10x/tickets/done/2026-07-10-bound-sitemap-resource-usage.md` passed |
| 17 | `.10x/specs/sitemap-resource-limits.md:42` | commit-qualified evidence path | obsolete working-tree pointer but valid historical citation | preserved; `git cat-file -e d7a37d7:.10x/evidence/2026-07-10-sitemap-resource-limits.md` passed |
| 18 | `.10x/specs/sitemap-resource-limits.md:43` | commit-qualified review path | obsolete working-tree pointer but valid historical citation | preserved; `git cat-file -e d7a37d7:.10x/reviews/2026-07-10-sitemap-resource-limits-review.md` passed |
| 19 | `.10x/tickets/cancelled/2026-07-14-create-buoy-v0-2-0-github-release.md:4` | `.10x/tickets/` + `2026-07-14-buoy-public-ci-release-plan.md` | rename/move | `.10x/tickets/done/2026-07-14-buoy-public-ci-release-plan.md` |
| 20 | `.10x/tickets/done/2026-07-14-add-buoy-ci-release-and-public-files.md:4` | `.10x/tickets/` + `2026-07-14-buoy-public-ci-release-plan.md` | rename/move | `.10x/tickets/done/2026-07-14-buoy-public-ci-release-plan.md` |
| 21 | `.10x/tickets/done/2026-07-14-buoy-public-ci-release-plan.md:29` | `.10x/tickets/` + `2026-07-14-finalize-v0-2-1-release-docs.md` | rename/move | `.10x/tickets/done/2026-07-14-finalize-v0-2-1-release-docs.md` |
| 22 | `.10x/tickets/done/2026-07-14-buoy-public-ci-release-plan.md:50` | `.10x/tickets/` + `2026-07-14-finalize-v0-2-1-release-docs.md` | rename/move | `.10x/tickets/done/2026-07-14-finalize-v0-2-1-release-docs.md` |
| 23 | `.10x/tickets/done/2026-07-14-create-buoy-v0-2-1-github-release.md:4` | `.10x/tickets/` + `2026-07-14-buoy-public-ci-release-plan.md` | rename/move | `.10x/tickets/done/2026-07-14-buoy-public-ci-release-plan.md` |
| 24 | `.10x/tickets/done/2026-07-14-finalize-v0-2-1-release-docs.md:4` | `.10x/tickets/` + `2026-07-14-buoy-public-ci-release-plan.md` | rename/move | `.10x/tickets/done/2026-07-14-buoy-public-ci-release-plan.md` |
| 25 | `.10x/tickets/done/2026-07-14-publish-buoy-rebrand-commit.md:4` | `.10x/tickets/` + `2026-07-14-buoy-public-ci-release-plan.md` | rename/move | `.10x/tickets/done/2026-07-14-buoy-public-ci-release-plan.md` |
| 26 | `.10x/tickets/done/2026-07-14-repair-release-workflow-and-bump-v0-2-1.md:4` | `.10x/tickets/` + `2026-07-14-buoy-public-ci-release-plan.md` | rename/move | `.10x/tickets/done/2026-07-14-buoy-public-ci-release-plan.md` |
| 27 | `.10x/tickets/done/2026-07-14-validate-buoy-ci-release-automation.md:4` | `.10x/tickets/` + `2026-07-14-buoy-public-ci-release-plan.md` | rename/move | `.10x/tickets/done/2026-07-14-buoy-public-ci-release-plan.md` |

Counts: **27 candidates; 20 repaired current pointers; four preserved fenced historical strings; three preserved and verified commit-qualified citations; zero unresolved references.** No placeholder record or authority was created.

### Follow-up validation

- Semantic Markdown reference scan: `CURRENT_REFERENCES_MISSING=0`, `COMMIT_REFERENCES_MISSING=0`.
- Preserved fenced history: `FENCED_HISTORICAL_PATH_STRINGS=4`, exactly the three SHA-256 output paths and one reviewed false Thistle citation above.
- Terminal inventory: `TOP_LEVEL_TERMINAL=0`.
- Original move preservation, rechecked against parent `326d070`: `MOVED_VALIDATED=20`, `ERRORS=0`; each moved record retained status and complete content after normalizing only both rounds of path repairs.
- Scope: changed paths remain `.10x` Markdown only; source, runtime, and tests are unchanged.
- Diff hygiene: `git diff --check` passed.
- Repository state: no staged files.

## What this supports or challenges

This supports the claim that only already-terminal records were relocated, all 27 follow-up candidates were resolved without rewriting historical logs or inventing authority, current and commit-qualified Markdown references are resolvable, and historical record meaning was preserved.

## Limits

Independent record review is still required. This evidence does not close the owning ticket or merge PR #44.
