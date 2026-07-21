Status: recorded
Created: 2026-07-14
Updated: 2026-07-14
Relates-To: .10x/tickets/done/2026-07-14-single-pass-plan-and-stage-timing.md

# Single-Pass Planning and Stage Timing Validation

## What was observed

- Website, GitHub repository, and local-document crawl implementations now return an internal `CrawlExecution` containing the summary and the exact `IndexingPlan` they already generated. Public crawl commands retain their summary-only interfaces.
- `plan` consumes that retained plan and no longer calls `process_corpus` again.
- `build_plan_artifacts` runs once. After diffing, the immutable plan document's diff field is replaced while reusing the manifest and pre-serialized chunks JSONL; artifact identity excludes diff and remains unchanged.
- Plan JSON/text timing exposes elapsed, sitemap policy, crawl, corpus write, chunking, diff, artifact construction, and publication durations. Clock failures produce zero diagnostic duration and cannot fail work.

## Validation

```text
PYTHONDONTWRITEBYTECODE=1 uv run python -m unittest tests.test_cli tests.test_crawler tests.test_github_repo tests.test_plan_artifacts tests.test_apply_cli -q
Ran 145 tests; OK

PYTHONDONTWRITEBYTECODE=1 uv run python -m unittest discover -s tests -p 'test_*.py' -q
Ran 248 tests; OK

uv build --out-dir /tmp/buoy-single-pass-test-repair-build
built buoy_search-0.2.1 wheel and sdist

uv lock --check; git diff --check
OK
```

Focused CLI coverage now asserts exactly one corpus-processing call and one complete artifact build for website, GitHub repository, and local-PDF plan paths. A focused old-pattern full rebuild versus optimized diff-finalization regression removes only observational `created_at` before comparing the complete plan and also asserts exact artifact hash, plan ID, diff, manifest, and chunks JSONL equality. Crawler coverage proves diagnostic clock failures are best-effort.

## Retained-corpus benchmark

Raw results: `.10x/evidence/.storage/2026-07-14-single-pass-plan-benchmark.json`.

Using the retained 228-file / 8,749-chunk ADK corpus, three local no-network runs compared the previous two-process/two-artifact pattern with one process/one artifact build:

- previous-pattern median: 6.350 seconds
- single-pass median: 3.195 seconds
- measured reduction: 49.7%

This isolates post-fetch corpus/artifact work and is not a full live plan benchmark.

## Limits

Stage timings are diagnostic and host/workload specific. Publication timing covers machine plan artifacts; final summary write and superseded-plan cleanup remain outside that stage. No live crawl or remote operation ran.
