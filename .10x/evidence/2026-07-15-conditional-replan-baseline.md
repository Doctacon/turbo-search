Status: recorded
Created: 2026-07-15
Updated: 2026-07-15
Relates-To: .10x/tickets/cancelled/2026-07-14-conditional-website-replanning.md

# Conditional Website Replanning Measurement Gate

## What was observed

A fresh local-only Oscilar plan completed successfully into the new directory `artifacts/site-crawls/oscilar-com-conditional-baseline-20260715-a010c673` without replacing prior artifacts or contacting Turbopuffer.

Counts:

- 347 requests; zero failed, blocked, or robots-disallowed requests;
- 340 pages and 6,804 chunks;
- 289 unchanged current pages (85.0%), 3 added, 48 changed, and 1 removed relative to local applied state;
- 6,301 unchanged chunks (92.6%) and 503 chunks/rows to embed/upsert;
- no page/chunk limit reached.

Stage timing:

| Stage | Seconds | Share of elapsed |
|---|---:|---:|
| Sitemap/language policy | 1.978 | 1.7% |
| Crawl/acquisition | 111.248 | 96.3% |
| Corpus write | 0.078 | 0.1% |
| Chunking | 1.061 | 0.9% |
| Diff | 0.058 | 0.1% |
| Artifact construction | 0.626 | 0.5% |
| Publication | 0.326 | 0.3% |
| Total elapsed | 115.471 | 100% |

Policy plus crawl consumed 98.1% of elapsed time, so acquisition is materially dominant and avoiding unchanged bodies would have high leverage if authoritative conditional responses were available.

## Validator sample

A bounded sample used the homepage plus 11 deterministic evenly spaced canonical URLs from the published 340-page manifest. For each URL, normal HEAD and streamed GET headers were inspected. When a GET exposed a validator, an exact conditional GET was sent.

- HEAD 200: 12/12;
- GET 200: 12/12;
- ETag present: 0/12;
- Last-Modified present: 12/12;
- conditional GET sent with exact `If-Modified-Since`: 12/12;
- authoritative 304 Not Modified: 0/12;
- conditional response 200: 12/12.

The site advertises `Last-Modified` values but did not honor them for conditional GET on this sample. Header presence alone is not sufficient authority to reuse cached extracted content.

## Gate conclusion

**Do not implement the proposed authoritative-validator cache for Oscilar.** Acquisition is the correct hot path, but the second required gate failed: no sampled request produced a 304 response. A TTL, assumed freshness window, or reuse based only on an unchanged-looking header would violate the ticket's no-heuristic-freshness safety contract. A content-hash cache would still download the full body and therefore would not address the measured dominant acquisition cost.

## Procedure

From the repository root, with the API key explicitly removed from the command environment:

```bash
env -u TURBOPUFFER_API_KEY uv run buoy plan 'https://oscilar.com/' \
  --namespace site-oscilar-com-v1 \
  --state-root .turbo-search \
  --out-dir artifacts/site-crawls/oscilar-com-conditional-baseline-20260715-a010c673 \
  --json
```

No apply or apply preflight command ran. The JSON reported `dry_run: true`, `credentials_required: false`, `turbopuffer_api_calls: false`, and `api_calls_occurred: false`. Read-only DuckDB inspection afterward still showed the historical 2026-07-13 apply metadata, 6,763 applied rows, and one apply run.

Sanitized raw metrics and sampled URLs: `.10x/evidence/.storage/2026-07-15-conditional-replan-baseline.json`.

## Limits

This is one Oscilar run and a 12-page validator sample at one point in time. Server/CDN behavior can change, and other websites may support ETag or 304 correctly. The measurement does not justify a general conditional cache implementation without a representative workload that passes both the acquisition-materiality and authoritative-validator gates. No live Turbopuffer operation, namespace mutation, apply, deletion, or credential read occurred.
