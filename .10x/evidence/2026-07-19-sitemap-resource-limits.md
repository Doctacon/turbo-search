Status: recorded
Created: 2026-07-19
Updated: 2026-07-20
Relates-To: .10x/tickets/done/2026-07-18-bound-sitemap-resource-usage.md, .10x/specs/sitemap-resource-limits.md, .10x/specs/website-exact-host-crawl-boundary.md

# Sitemap Resource-Limit Validation

## What was observed

- `fetch_url_bytes()` reads at most 64 KiB per call and accepts exactly 512 KiB robots bodies and 10 MiB sitemap transfers while rejecting one byte over either ceiling.
- Sitemap gzip expansion reads incrementally, accepts exactly 50 MiB decompressed output, and rejects a compressed expansion-bomb fixture at 50 MiB + 1 byte.
- URL-, content-type-, content-encoding-, and magic-byte-declared malformed gzip raises `SitemapResourceError` rather than becoming empty sitemap discovery. Corrupt DEFLATE that raises `zlib.error` is wrapped in the required URL-specific malformed-gzip error.
- The validated final response URL is retained after redirects and used for gzip declaration detection and relative sitemap parsing. A sitemap redirected from `.xml` to `.xml.gz` with malformed non-magic content fails closed before link fallback.
- Multiple queued sitemaps propagate a late resource-limit error; sitemap resource errors do not enter link fallback.
- Bounded discovery remains exact-host constrained. The existing exact-host fixture suite still proves blocked declarations/redirects receive zero requests and redirected robots rules remain effective.
- Sitemap crawling now uses page URLs returned by bounded discovery rather than asking Scrapling to download sitemap bodies independently. Robots are placed into Scrapling's parser cache only after the bounded exact-host reader succeeds.

## Procedure

All commands were non-live and made no remote-service writes:

```text
PYTHONDONTWRITEBYTECODE=1 uv run --python 3.11 python -m unittest tests.test_crawler tests.test_crawler_exact_host -q
# Ran 61 tests in 5.950s — OK

PYTHONDONTWRITEBYTECODE=1 uv run --python 3.11 python -m unittest discover -s tests -p 'test_*.py' -q
# Ran 431 tests in 21.992s — OK

PYTHONDONTWRITEBYTECODE=1 uv run --python 3.13 python -m unittest tests.test_crawler tests.test_crawler_exact_host -q
# Ran 61 tests in 5.973s — OK

PYTHONDONTWRITEBYTECODE=1 uv run --python 3.13 python -m unittest discover -s tests -p 'test_*.py' -q
# Ran 431 tests in 20.379s — OK

git diff --check
# passed with no output
```

The full suites emitted only existing best-effort temporary plan-artifact cleanup warnings. The exact-host focused suites emitted an upstream lxml `strip_cdata` deprecation warning.

## What this supports

The implementation and tests support the behavioral and acceptance scenarios in `.10x/specs/sitemap-resource-limits.md` without changing the exact hostname rule, 20-hop redirect boundary, sitemap/page count caps, include/exclude path filtering, robots enforcement, crawl strategies, or trusted-local SSRF exclusion.

## Refresh and combined validation

PR #54 was refreshed from reviewed sitemap head `7055771` onto exact `origin/develop` `b938233` in merge commit `fa9bfbb`. The second parent contains the independently reviewed MarkItDown normalization and Node 24 workflow updates. `git show --remerge-diff fa9bfbb` shows the only conflict and manual resolution: the crawler import block retains both `unicodedata` and `zlib`. Both pre-refresh and post-refresh branch deltas name the same five sitemap-owned files.

The following non-live checks passed after the refresh on both Python 3.11 and 3.13:

```text
# 13 explicit sitemap resource-limit and MarkItDown normalization tests
# Ran 13 tests — OK (3.11: 0.381s; 3.13: 0.310s)

PYTHONDONTWRITEBYTECODE=1 uv run --python <version> python -m unittest tests.test_crawler_exact_host -q
# Ran 11 tests — OK (3.11: 5.542s; 3.13: 6.035s)

PYTHONDONTWRITEBYTECODE=1 uv run --python <version> python -m unittest discover -s tests -p 'test_*.py' -q
# Ran 435 tests — OK (3.11: 23.269s; 3.13: 22.435s)

git diff --check origin/develop...HEAD
# passed with no output
```

The full suites emitted only the existing best-effort temporary plan-artifact cleanup warnings. The exact-host suites emitted the upstream lxml `strip_cdata` deprecation warning.

GitHub Actions run `29719492676` completed successfully at exact head `fa9bfbb241e4e64a74c6c4520bc094d364037fa7`: Python 3.11, Python 3.13, and Build distributions all passed. PR #54 reported the same exact head and a clean merge state after the run.

## Limits

- Transfer-boundary tests use mocked incremental response streams. Existing exact-host integration tests use loopback fixture servers; no live website was crawled.
- Page-body limits and service-grade DNS/IP/private-network SSRF controls remain explicitly excluded.
- Independent rereview passed at `7055771` and is recorded in `.10x/reviews/2026-07-20-sitemap-resource-limits-review.md`; refresh equivalence plus combined local and exact-head hosted validation support closure without a live crawl or merge.
