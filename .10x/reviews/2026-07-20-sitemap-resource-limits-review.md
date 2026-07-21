Status: recorded
Created: 2026-07-20
Updated: 2026-07-20
Target: .10x/tickets/done/2026-07-18-bound-sitemap-resource-usage.md
Verdict: pass

# Sitemap Resource-Limit Review

## Target

PR #54 at implementation/evidence head `70557710e419abad988f9724d57bebb522c3c7a3`, governed by `.10x/specs/sitemap-resource-limits.md` and integrated with `.10x/specs/website-exact-host-crawl-boundary.md`.

## Criteria mapping

- **Incremental robots and sitemap transfer limits:** pass. The bounded reader requests at most a fixed chunk and stops at the configured robots or sitemap ceiling; exact-boundary and one-byte-over fixtures cover both limits.
- **Incremental decompressed sitemap limit:** pass. Gzip output is read incrementally with a 50 MiB ceiling; exact-boundary and expansion-bomb fixtures cover acceptance and rejection.
- **Declared or detected malformed gzip fails closed:** pass. URL, response content type, response content encoding, and magic bytes declare gzip. Decompression failures, including `zlib.error`, become URL-specific `SitemapResourceError` failures instead of empty discovery or link fallback.
- **Redirect and queue behavior:** pass. Validated final response URLs drive gzip declaration and relative sitemap parsing, while late errors in a multi-sitemap queue propagate rather than broadening discovery.
- **Existing discovery boundaries remain:** pass. Exact-host fixtures retain blocked-declaration and redirect behavior, and the implementation preserves sitemap/page caps, robots enforcement, path filtering, and crawl strategy semantics.
- **Validation and scope:** pass. Focused and full non-live suites passed on Python 3.11 and 3.13 at the reviewed head. The diff does not add page-body limits, service-grade SSRF controls, live crawling, or unrelated behavior.

## Findings

No blockers. The repaired implementation at `7055771` satisfies the active sitemap resource-limit contract and preserves the exact-host boundary.

## Refresh assessment

The subsequent refresh merge `fa9bfbb` incorporates exact `origin/develop` `b938233`. Its only manual conflict resolution retains both the reviewed sitemap `zlib` import and the reviewed MarkItDown `unicodedata` import. `git show --remerge-diff fa9bfbb` isolates that resolution, the branch delta against `origin/develop` remains the same five sitemap-owned files, combined focused/exact-host/full supported-version checks pass, and exact-head GitHub Actions run `29719492676` passes all jobs. The refresh does not invalidate this pass.

## Verdict

Pass. The ticket may close.

## Residual risk

Boundary tests mock incremental network response streams, while exact-host integration uses loopback fixture servers. No live website was crawled. Page-body limits and service-grade DNS/IP/private-network SSRF controls remain explicitly excluded from this trusted-local CLI contract.
