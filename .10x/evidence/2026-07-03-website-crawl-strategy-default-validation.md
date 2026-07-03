Status: recorded
Created: 2026-07-03
Updated: 2026-07-03
Relates-To: .10x/tickets/done/2026-07-03-website-crawl-strategy-default-sitemap.md, .10x/specs/website-crawl-strategy-default.md

# Website Crawl Strategy Default Validation

## What was observed

`turbo-search crawl` and `turbo-search plan` now default to `--crawl-strategy sitemap` instead of `hybrid`.

The default sitemap strategy uses sitemap pages when available and does not run the link crawler after a non-empty sitemap crawl. Empty sitemap results still fall back to link crawling. `--crawl-strategy hybrid` remains available for explicit sitemap-plus-link discovery.

## Procedure

Targeted unit validation:

```bash
uv run python -m unittest tests.test_crawler tests.test_cli
```

Output:

```text
.......................................................
----------------------------------------------------------------------
Ran 55 tests in 0.689s

OK
```

Full test discovery:

```bash
uv run python -m unittest discover -s tests
```

Output:

```text
..................................................................................................................................................................
----------------------------------------------------------------------
Ran 162 tests in 2.962s

OK
```

CLI help validation:

```bash
uv run turbo-search plan --help | rg -n "crawl-strategy|Default: sitemap|hybrid merges|language-policy"
```

Output:

```text
10:                         [--crawl-strategy {sitemap,link,hybrid}]
12:                         [--language-policy {english,all}]
64:  --crawl-strategy {sitemap,link,hybrid}
65:                        Discovery mode. Default: sitemap, which uses sitemap
67:                        hybrid merges sitemap pages with same-site link
75:  --language-policy {english,all}
```

## What this supports or challenges

This supports that the user-facing default now matches the intended behavior: sitemap-only when sitemap pages are available, link crawl only when explicitly requested or when sitemap discovery has no pages.

## Limits

- Validation used unit tests and help output, not a full public-site crawl.
- No live turbopuffer writes, embeddings, namespace creation, namespace deletion, or live retrieval evals were run.
