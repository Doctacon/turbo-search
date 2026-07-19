Status: done
Created: 2026-07-08
Updated: 2026-07-08
Parent: None
Depends-On: None

# Local PDF Source Ingestion

## Scope

Implement `.10x/specs/local-pdf-source-ingestion.md`.

In scope:

- Add a first-class local PDF source type to source detection and deterministic identity helpers.
- Add MarkItDown PDF conversion dependency and use MarkItDown to convert one local PDF file into one generated Markdown page.
- Reuse the existing Markdown chunking, local plan artifacts, local applied-state diffing, and apply preflight/approved-apply paths.
- Preserve privacy by storing filename and hash only; do not persist absolute local paths in generated artifacts, plan state, chunks JSONL, or rows.
- Update CLI help/text summaries so source arguments cover URLs and local PDF paths.
- Add unit tests for PDF source detection, namespace/source ID, crawl/plan behavior, missing/empty extraction failures, and non-regression of website/GitHub behavior.
- Update README and workflow documentation with local PDF usage.

Out of scope:

- PDF page-number citations.
- OCR/scanned PDF support.
- Directory or multi-PDF ingestion.
- Remote PDF URLs as a special source type.
- MarkItDown plugins, Azure, LLM vision, or cloud extraction.
- Live turbopuffer writes beyond existing `apply --approve` behavior.

## Acceptance criteria

- `turbo-search plan ./example.pdf --json` works for a text PDF and reports `source_kind: pdf`, deterministic `pdf-<filename-slug>-<sha16>-v1` namespace candidate, generated chunks, local plan paths, and no live API calls.
- Generated artifacts and row metadata include filename/hash/source_kind but not the absolute local path.
- `turbo-search crawl --base-url ./example.pdf --json` produces the local PDF corpus shape without live calls.
- Empty MarkItDown extraction fails clearly as unsupported scanned/empty PDF extraction.
- Existing website and GitHub source tests continue to pass.
- Documentation shows how to plan/apply/search a local PDF namespace and states that page citations/OCR are out of v1 scope.

## Evidence expectations

- Unit test command output for the PDF tests and existing source-routing tests.
- At least one local-only smoke plan against a generated text PDF fixture, with summary showing no credentials/API calls.
- `git diff --stat` and targeted diff inspection before closure.

## Progress and notes

- 2026-07-08: Opened after user ratified MarkItDown-based local PDF ingestion, single-file v1 scope, filename+hash identity, and no page-number citations.
- 2026-07-08: Implemented local PDF source detection, MarkItDown conversion, synthetic `pdf://` source identity, PDF frontmatter/manifest/row metadata, CLI routing/help, docs, and tests.
- 2026-07-08: Verified with compile check, targeted tests, full test suite, lockfile check, diff whitespace check, and local-only MarkItDown smoke plan. Evidence: `.10x/evidence/2026-07-08-local-pdf-source-ingestion.md`.
- 2026-07-08: Review passed with no blockers. Review: `.10x/reviews/2026-07-08-local-pdf-source-ingestion-review.md`.

## Blockers

- None.

## References

- `.10x/specs/local-pdf-source-ingestion.md`
- `.10x/decisions/local-pdf-ingestion-uses-markitdown.md`
- `.10x/research/2026-07-08-markitdown-pdf-ingestion.md`
- MarkItDown clone inspected at commit `e144e0a2be95b34df17433bac904e635f2c5e551`.
