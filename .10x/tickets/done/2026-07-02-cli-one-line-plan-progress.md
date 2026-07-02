Status: done
Created: 2026-07-02
Updated: 2026-07-02
Depends-On: None

# CLI One-Line Plan Progress

## Scope

Add default interactive one-line progress feedback for long local `turbo-search plan` website crawls, and share the same mechanism with `turbo-search crawl` where practical.

In scope:

- Show progress by default for interactive text-mode `plan` and `crawl` runs.
- Keep progress on one terminal line using carriage-return updates so terminal output remains compact.
- Send progress to stderr so final text/JSON stdout remains separate.
- Suppress progress automatically for `--json`, non-TTY stderr, and explicit `--no-progress`.
- Include crawl-stage signals such as sitemap/link crawl start, pages fetched, queued/discovered URLs, and later plan phases such as chunking/diffing/writing.
- Add unit tests for progress suppression/rendering and crawl progress events.

Out of scope:

- Rich/full-screen UI.
- Persistent partial crawl artifacts beyond existing outputs.
- Live turbopuffer apply progress.
- Exact ETA calculation.

## Acceptance criteria

- An interactive `uv run turbo-search plan "https://example.com"` can show a single updating progress line during long local work.
- `--json` output remains clean JSON on stdout with no default progress noise.
- Redirected/non-interactive command output does not get carriage-return progress spam.
- Users can disable interactive progress with `--no-progress`.
- Existing tests pass.

## Progress and notes

- 2026-07-02: Opened after user reported `plan "https://iceberg.apache.org/"` felt like sitting in limbo and requested default one-line updating progress.
- 2026-07-02: Implemented interactive stderr one-line progress for `crawl`/`plan`, automatic suppression for `--json` and non-TTY stderr, and `--no-progress`. Added tests and validation evidence.
- 2026-07-02: User reported progress still appeared on new lines for long Iceberg URLs. Root cause: long progress messages soft-wrapped at terminal width, and carriage return only returned to the current wrapped physical line. Added terminal-width truncation in the renderer so progress lines stay below wrap width.

## Blockers

- None.

## Evidence

- `.10x/evidence/2026-07-02-cli-one-line-plan-progress-validation.md`
