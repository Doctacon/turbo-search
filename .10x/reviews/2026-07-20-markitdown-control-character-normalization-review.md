Status: recorded
Created: 2026-07-20
Updated: 2026-07-20
Target: .10x/tickets/done/2026-07-18-restore-markitdown-control-character-normalization.md
Verdict: pass

# MarkItDown Control-Character Normalization Review

## Target

PR #52 at implementation/evidence head `2520170181ed7d977531c007c25d3b381775e057`, governed by `.10x/tickets/done/2026-07-18-restore-markitdown-control-character-normalization.md` and the local PDF/document ingestion specifications.

## Criteria mapping

- **PDF and non-PDF output strips embedded Unicode `Cc` controls before artifacts and chunks:** pass. Both source kinds converge on `crawl_local_document_with_plan()`. It applies `normalize_markitdown_markdown()` immediately after conversion and before the empty-output check, page-directory creation, corpus write, and `process_corpus()`. Separate PDF and non-PDF tests assert representative controls are absent from both generated Markdown and processed chunk content.
- **Markdown whitespace, structure, and valid Unicode remain:** pass. The sanitizer removes only characters whose Unicode category is `Cc`, with explicit exceptions for newline, carriage return, and tab. Focused assertions preserve CRLF/tab, a Markdown heading, accented text, emoji, and ordinary content while removing NUL, unit separator, DEL, and a C1 control.
- **Empty-output handling remains after normalization:** pass. Source order is explicit, and a table-driven focused test covers PDF and non-PDF converter output containing only removable controls, expects the existing clear `No text was extracted` error, and confirms the output directory is not created.
- **Focused current-package and full non-live validation passes:** pass. Reviewer reruns passed 4 focused and 426 full tests on both Python 3.11 and 3.13. PR #52 checks at reviewed head also passed Python 3.11, Python 3.13, and distribution build jobs.
- **Scope remains narrow:** pass. The implementation diff adds one standard-library import, one sanitizer, and one call at the shared boundary. It does not change converters, OCR, semantic cleanup, document structure, citations, namespaces, remote services, or apply behavior.

## Findings

No blockers. The change matches the ticket's exact normalization contract, retains the existing empty-output behavior in the correct order, covers both shared ingestion routes, and introduces no new dependency or external side effect.

## Verdict

Pass. The ticket may close.

## Residual risk

The PDF and non-PDF ingestion tests mock their MarkItDown converter functions, so they prove normalization of converter-returned text but do not demonstrate a real MarkItDown converter emitting embedded controls. This is a non-blocking limit: the sanitizer itself is directly tested, the shared post-conversion placement is source-verified, and the full supported-version and hosted suites pass. No converter-specific fixture is warranted without evidence of converter-dependent behavior.
