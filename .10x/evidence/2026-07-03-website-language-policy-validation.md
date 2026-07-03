Status: recorded
Created: 2026-07-03
Updated: 2026-07-03
Relates-To: .10x/tickets/done/2026-07-03-website-language-policy.md, .10x/specs/website-language-policy.md

# Website Language Policy Validation

## What was observed

Implemented website language policy support for `turbo-search crawl` and `turbo-search plan`:

- default `--language-policy english` detects sitemap locale-prefix families and adds effective excludes for non-English prefixes;
- `--language-policy all` keeps all languages;
- summaries include `language_policy` and `language_report`;
- help, README, generic workflow docs, and site-planning knowledge mention the new default and opt-out.

## Procedure

Unit validation:

```bash
uv run python -m unittest tests.test_crawler tests.test_cli
```

Output:

```text
.....................................................
----------------------------------------------------------------------
Ran 53 tests in 0.621s

OK
```

Full test discovery:

```bash
uv run python -m unittest discover -s tests
```

Output:

```text
................................................................................................................................................................
----------------------------------------------------------------------
Ran 160 tests in 3.010s

OK
```

CLI help validation:

```bash
uv run turbo-search plan --help | rg -n "language-policy|docs-version"
```

Output:

```text
11:                         [--docs-version-policy {warn,all,latest,stable-latest,latest-nightly}]
12:                         [--language-policy {english,all}]
69:  --docs-version-policy {warn,all,latest,stable-latest,latest-nightly}
70:                        Website sitemap docs-version handling. Default: warn
75:  --language-policy {english,all}
```

Blowfish sitemap analysis:

```bash
uv run python - <<'PY'
from pathlib import Path
from turbo_search.crawler import CrawlOptions, discover_sitemap_page_urls, analyze_language_urls, apply_language_policy
options = CrawlOptions(base_url='https://blowfish.page/', out_dir=Path('/tmp/unused'))
urls = discover_sitemap_page_urls(options)
report = analyze_language_urls(urls, policy=options.language_policy)
effective, applied = apply_language_policy(options, sitemap_page_urls=urls)
print(len(urls))
print(report['detected'], report['applied'], report['non_english_url_count'])
print(report['tail_overlap_count_by_language'])
print(report['added_exclude_paths'])
print(effective.exclude_paths)
PY
```

Output:

```text
1349
True True 1199
{'de': 130, 'es': 124, 'fr': 126, 'it': 146, 'ja': 150, 'pt-br': 124, 'pt-pt': 124, 'zh-cn': 116}
['/de/**', '/es/**', '/fr/**', '/it/**', '/ja/**', '/pt-br/**', '/pt-pt/**', '/zh-cn/**']
('/de/**', '/es/**', '/fr/**', '/it/**', '/ja/**', '/pt-br/**', '/pt-pt/**', '/zh-cn/**')
```

Bounded Blowfish plan smoke test, writing only temporary local artifacts outside the repository:

```bash
rm -rf /tmp/turbo-search-blowfish-language-smoke /tmp/turbo-search-blowfish-state-smoke && \
uv run turbo-search plan https://blowfish.page/ \
  --crawl-strategy sitemap \
  --max-pages 1 \
  --max-chunks 20 \
  --out-dir /tmp/turbo-search-blowfish-language-smoke \
  --state-root /tmp/turbo-search-blowfish-state-smoke \
  --no-progress \
  --json > /tmp/turbo-search-blowfish-language-smoke.json
```

Inspected summary subset:

```json
{
  "chunks_generated": 14,
  "exclude_paths": [
    "/de/**",
    "/es/**",
    "/fr/**",
    "/it/**",
    "/ja/**",
    "/pt-br/**",
    "/pt-pt/**",
    "/zh-cn/**"
  ],
  "excluded_languages": [
    "de",
    "es",
    "fr",
    "it",
    "ja",
    "pt-br",
    "pt-pt",
    "zh-cn"
  ],
  "language_policy": "english",
  "pages_scraped": 1,
  "tail_overlap_count_by_language": {
    "de": 130,
    "es": 124,
    "fr": 126,
    "it": 146,
    "ja": 150,
    "pt-br": 124,
    "pt-pt": 124,
    "zh-cn": 116
  }
}
```

## What this supports or challenges

This supports that the default planning path now detects the Blowfish multilingual duplication pattern and prunes non-English localized paths before page crawling, while retaining an explicit `all` opt-out and passing existing crawler/CLI coverage.

## Limits

- The Blowfish smoke test crawled only one page by cap; it validates policy application and artifact reporting, not a full-site crawl count.
- No live turbopuffer writes, embeddings, namespace creation, namespace deletion, or live retrieval evals were run.
- Link-only crawls intentionally skip sitemap language pre-analysis and therefore do not auto-detect language families.
