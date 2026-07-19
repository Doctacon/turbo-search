Status: recorded
Created: 2026-07-19
Updated: 2026-07-19
Target: .10x/tickets/done/2026-07-18-enforce-website-exact-host-crawl-boundary.md
Verdict: pass

# Website Exact-Host Crawl Boundary Review

## Target

PR #42 at final reviewed head `dcf775d`, governed by `.10x/tickets/done/2026-07-18-enforce-website-exact-host-crawl-boundary.md` and `.10x/specs/website-exact-host-crawl-boundary.md`.

## Findings

Review iteratively challenged destination-side request safety, Scrapling integration drift, output scope, and untrusted summary leakage. Before final pass, review found and required correction of:

- Markdown destination parsing that could leak query suffixes;
- fail-open private Scrapling robots integration across an unconstrained dependency range;
- website-only fields/sanitization leaking into local PDF/file output;
- autolink, visible-label, IPv6, encoded-label, title, and heading/section representations that escaped field-level sanitizers.

The final design avoids representation parsing: if either blocked-discovery or blocked-redirect count is nonzero, website `sample_chunks` is empty, so no sampled title, heading, section path, content, URL, query, fragment, credential-like, or encoded representation is emitted. Zero-block website samples preserve prior structure; local PDF/file summaries remain unchanged.

Final independent review confirmed:

- prohibited discovered and redirected destinations receive zero requests in local two-server fixtures;
- page, sitemap, and robots declarations/redirects plus unexpected final responses are exact-host checked;
- redirect chains are capped at 20;
- Scrapling is pinned exactly to 0.4.9 and private lifecycle/session/robots shape drift fails closed;
- count-only output and sample omission prevent untrusted blocked-destination leakage;
- focused/full Python 3.11/3.13 suites and hosted distribution checks pass;
- exclusions remain intact: no dedup, general SSRF, live crawl, or remote mutation.

## Verdict

Pass.

## Residual risk

The robots integration relies on private Scrapling 0.4.9 APIs, mitigated by exact pinning and fail-closed runtime-shape guards. This contract is intentionally exact-host crawl containment, not DNS/IP/private-network SSRF defense.
