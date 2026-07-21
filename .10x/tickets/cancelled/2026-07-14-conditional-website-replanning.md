Status: cancelled
Created: 2026-07-14
Updated: 2026-07-19
Parent: None
Depends-On: None

# Add Safe Conditional Website Replanning

## Scope

Measure a repeated website plan with current stage timing, then—only if acquisition is material—reuse prior extracted pages exclusively when authoritative HTTP validators produce not-modified responses. Preserve full sitemap membership/removal detection and fall back to normal fetch on absent validators, option changes, cache mismatch, or corruption.

## Candidate acceptance

- Capture an authorized repeat-plan baseline with sitemap, crawl, corpus, chunk, diff, artifact, and publication timing.
- Cache keys include canonical URL and every extraction/chunk option that can change output.
- `ETag`/`Last-Modified` validators may produce reuse only after an authoritative not-modified response; no heuristic freshness.
- Sitemap membership still detects additions/removals and suspicious partial crawls cannot produce deletion-capable plans silently.
- Cold/full and warm/conditional plans for equivalent content produce identical manifests, chunks, hashes, and diffs.
- Corruption and missing-validator cases safely refetch.
- No Turbopuffer write or namespace mutation.

## References

- `.10x/reviews/2026-07-14-post-optimization-performance-ux-review.md`
- `.10x/evidence/2026-07-14-single-pass-plan-and-stage-timing.md`

## Progress and notes

- 2026-07-14: User authorized execution. Use the previously validated public Oscilar workload (`https://oscilar.com/`) for a no-Turbopuffer-write repeated-plan timing baseline; preserve existing state and prior artifacts.
- 2026-07-15: Measurement gate completed. Crawl consumed 111.248s of 115.471s (96.3%), with 289/340 current pages and 6,301/6,804 chunks unchanged. Acquisition is material. However, a homepage plus 11-page manifest sample had 0/12 ETags and all 12 exact `If-Modified-Since` conditional GETs returned 200, not 304. The authoritative-validator gate failed, so no cache/spec/implementation was created. Evidence: `.10x/evidence/2026-07-15-conditional-replan-baseline.md`.
- 2026-07-15: Independent measurement-gate review passed with no blockers: `.10x/reviews/2026-07-15-conditional-replan-measurement-gate-review.md`. Ticket remains blocked rather than implementing heuristic freshness.
- 2026-07-19: Closure review cancelled the Oscilar slice with no action. The required measurement gate was completed and independently reviewed: acquisition was material, but 0/12 conditional requests returned authoritative 304 responses. The ticket's own safety contract therefore forbids cache/spec/implementation work for this workload. Review: `.10x/reviews/2026-07-19-stale-ticket-status-closure-review.md`.

## Blockers

None. This ticket is cancelled with the evidence-backed no-action rationale below.

## Existing acceptance mapping

- Authorized repeated-plan baseline and full stage timing: `.10x/evidence/2026-07-15-conditional-replan-baseline.md`.
- No remote write/mutation: the evidence records local-only planning, removed API-key environment, dry-run flags, and unchanged historical applied state.
- Validator safety gate: the same evidence records 0 ETags and 0 authoritative 304 responses across the 12-page sample.
- Independent gate review: `.10x/reviews/2026-07-15-conditional-replan-measurement-gate-review.md` passed the decision to stop.
- Cache-key, equivalent-output, corruption, and fallback implementation criteria: intentionally not executed because the prerequisite authoritative-validator gate failed.

## No-action rationale

Do not create an Oscilar conditional cache, cache specification, or heuristic reuse path. Header presence without an authoritative 304 is insufficient, and a content-hash cache would still download the body without addressing the measured acquisition cost. If a different representative workload later passes both materiality and trustworthy-304 gates, it requires a newly authorized ticket rather than reopening this failed workload gate.
