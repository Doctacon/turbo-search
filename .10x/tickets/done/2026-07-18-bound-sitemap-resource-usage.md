Status: done
Created: 2026-07-18
Updated: 2026-07-20
Parent: None
Depends-On: None

# Restore Bounded Sitemap Resource Usage

## Scope

Implement `.10x/specs/sitemap-resource-limits.md` in current `src/buoy_search/crawler.py`. Replace unbounded robots/sitemap reads and gzip expansion with incremental bounded processing and fail-closed errors.

## Acceptance criteria

- Meets `.10x/specs/sitemap-resource-limits.md`.
- The current `fetch_url_bytes()` and gzip handling no longer perform unbounded whole-body work.
- Oversize or malformed declared/detected gzip cannot silently appear empty and trigger broader link fallback.
- Focused boundary/bomb fixtures and full non-live validation pass.

## Evidence expectations

Exact-boundary and over-limit fixtures, gzip-bomb/malformed-gzip proof, focused/full checks, and independent review.

## Blockers

None. Exact limits and failure behavior were user-ratified on historical commit `d7a37d7` and are preserved in the active current spec.

## Explicit exclusions

Live crawling, page-body limits, service-grade SSRF, and changes to exact-host semantics beyond compatible integration.

## References

- `.10x/specs/sitemap-resource-limits.md`
- `.10x/research/2026-07-18-thistle-qdrant-dead-end-disposition.md`

## Progress and notes

- 2026-07-18: Current source inspection found `fetch_url_bytes()` calls `response.read()` and `maybe_decompress_sitemap()` expands gzip without byte ceilings; opened the smallest current repair owner.
- 2026-07-19: Bounded incremental readers and declared/detected gzip fail-closed handling are integrated with exact-host discovery. Focused crawler/exact-host and full 428-test suites pass on Python 3.11 and 3.13; evidence is recorded at `.10x/evidence/2026-07-19-sitemap-resource-limits.md`. Independent review remains, so this ticket stays active.
- 2026-07-19: PR #54 review blockers repaired: corrupt-DEFLATE `zlib.error` is wrapped as URL-specific malformed gzip, and validated final redirect URLs now drive declared-gzip detection and relative parsing. Focused 61-test and full 431-test suites pass on Python 3.11 and 3.13. The ticket remains active for independent rereview; no closure or merge was performed.
- 2026-07-20: Independent rereview passed PR #54 at implementation/evidence head `7055771`; review: `.10x/reviews/2026-07-20-sitemap-resource-limits-review.md`.
- 2026-07-20: Refreshed onto exact `origin/develop` `b938233` in merge commit `fa9bfbb`. The only merge conflict was the crawler import line; retaining both `unicodedata` and `zlib` preserves the independently reviewed MarkItDown and sitemap behavior. `git show --remerge-diff fa9bfbb` confirms that import resolution was the merge's only manual semantic choice, while the branch diff against `origin/develop` remains the same five sitemap-owned files as at `7055771`.
- 2026-07-20: Post-refresh validation passed 13 combined sitemap/MarkItDown focused tests, 11 exact-host tests, and 435 full non-live tests on both Python 3.11 and 3.13. Exact-head GitHub Actions run `29719492676` passed Python 3.11, Python 3.13, and distribution build jobs at `fa9bfbb`. No live crawl or merge was performed.

## Closure mapping

- Incremental bounded reads: focused exact-boundary and one-byte-over fixtures prove robots and sitemap bodies are read in chunks and enforced at their configured ceilings.
- Bounded gzip expansion: focused exact-boundary and expansion-bomb fixtures prove incremental decompressed-byte enforcement; declared or detected malformed gzip, including corrupt DEFLATE, fails closed with the sitemap URL.
- Queue and fallback behavior: focused fixtures prove late sitemap errors propagate and never broaden into link fallback.
- Redirect and exact-host compatibility: final validated redirect URLs drive gzip declaration and relative parsing; the exact-host fixture suite passes on both supported Python versions.
- Integration and compatibility: the refreshed branch retains both reviewed feature sets, complete supported-version suites pass locally, and exact-head hosted Python/distribution checks pass.
- Independent review: `.10x/reviews/2026-07-20-sitemap-resource-limits-review.md` records a pass with no blockers.

## Retrospective

Keeping network transfer limits in the bounded reader and decompression limits in the gzip reader makes each memory boundary directly testable. During refresh, `git show --remerge-diff` provided a precise way to distinguish the single intentional conflict resolution from clean automatic integration; retaining both standard-library imports and rerunning the combined focused/full suites prevented one independently reviewed behavior from displacing the other.
