Status: done
Created: 2026-07-18
Updated: 2026-07-20
Parent: None
Depends-On: None

# Restore MarkItDown Control-Character Normalization

## Scope

Restore the narrow product-neutral behavior from unique historical commit `b48f13c6286af65781e82327eea4deffd471c8a7` in current `src/buoy_search/crawler.py`: before local MarkItDown output is written or chunked, remove Unicode `Cc` control characters except ordinary Markdown whitespace (`\n`, `\r`, `\t`).

## Acceptance criteria

- PDF and non-PDF local document ingestion strip embedded NUL and other `Cc` controls before generated page artifacts and chunks.
- Newlines, carriage returns, tabs, valid Unicode, and Markdown structure remain.
- Empty-output handling remains after normalization.
- Focused current-package tests cover PDF and non-PDF paths; full non-live validation passes.

## Evidence expectations

Focused control-character fixtures, full checks, diff check, and independent review.

## Blockers

None. The exact behavior was user-requested, implemented, evidenced, and independently reviewed on the historical branch. The old records are indexed as non-authoritative provenance in `.10x/research/2026-07-18-thistle-qdrant-dead-end-disposition.md`.

## Explicit exclusions

OCR, semantic cleanup, table/page repair, heading rewriting, converter changes, citation/namespace changes, or live apply.

## References

- `.10x/specs/local-markitdown-document-source-ingestion.md`
- `.10x/specs/local-pdf-source-ingestion.md`
- `.10x/research/2026-07-18-thistle-qdrant-dead-end-disposition.md`

## Progress and notes

- 2026-07-18: Current source inspection confirmed `crawl_local_document()` directly calls `.strip()` on converted output and has no control-character normalization.
- 2026-07-18: Implemented shared Unicode `Cc` removal before the existing `.strip()`, artifact write, and chunking path, while preserving newline, carriage return, and tab.
- 2026-07-18: Added focused PDF, non-PDF, preservation, and normalization-produced-empty-output coverage. Focused and full non-live suites pass on Python 3.11 and 3.13.
- 2026-07-18: Pushed implementation commit `403d4f9` and opened PR #52. GitHub Actions run `29713256945` passed Python 3.11, Python 3.13, and distribution build jobs. Ticket remains active pending independent review.
- 2026-07-20: Independent review passed PR #52 at implementation/evidence head `2520170`; current hosted checks remained green, and reviewer reruns passed 4 focused plus 426 full non-live tests on Python 3.11 and 3.13. Review: `.10x/reviews/2026-07-20-markitdown-control-character-normalization-review.md`.

## Closure mapping

- PDF and non-PDF control removal: both source kinds converge on `crawl_local_document_with_plan()`, which normalizes converter output before the empty check, generated page write, and chunking; focused artifact/chunk tests cover each path.
- Preserved Markdown content: the sanitizer test preserves newline, carriage return, tab, valid Unicode, emoji, headings, and ordinary text while removing representative C0/C1 controls.
- Empty-output order: focused PDF and non-PDF cases prove control-only output reaches the existing clear extraction failure before output creation.
- Validation and compatibility: 4 focused and 426 full non-live tests passed on both supported Python versions; PR #52 hosted Python 3.11, Python 3.13, and distribution checks passed; independent review found no scope widening or blocker.

## Retrospective

Placing normalization once at the shared post-conversion boundary kept PDF and non-PDF behavior aligned and made the ordering before empty handling, artifact writing, and chunking directly inspectable. The focused ingestion tests intentionally mock converter output, so they prove handling of converter-returned strings rather than real converter generation of controls; direct sanitizer coverage, shared-boundary integration, and full-suite/hosted validation make that a documented non-blocking limit rather than a reason to add converter-specific fixtures without evidence of such a regression.
