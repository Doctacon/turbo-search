Status: done
Created: 2026-07-08
Updated: 2026-07-08
Parent: None
Depends-On: None

# Local MarkItDown Document Source Ingestion

## Scope

Implement `.10x/specs/local-markitdown-document-source-ingestion.md`.

In scope:

- Generalize the existing local PDF source path to a local MarkItDown document source path for the ratified extension allowlist.
- Preserve PDF identity and behavior: `pdf-<filename-slug>-<sha16>-v1` and `pdf://...` remain unchanged.
- Add non-PDF identity: `file-<ext>-<filename-slug>-<sha16>-v1` and synthetic `file://...` source/document URLs.
- Use MarkItDown local conversion for one file into one Markdown document.
- Store filename, extension, hash, source ID, and source kind in frontmatter/manifest/chunks/rows without storing absolute local paths.
- Update dependencies for selected local office formats: MarkItDown extras for PDF, DOCX, PPTX, XLSX, and XLS.
- Update CLI help/text summaries and README/workflow docs.
- Add tests for source detection, namespace/source ID generation, crawl/plan behavior, empty extraction, unsupported extensions, PDF backward compatibility, artifact privacy, row metadata, and website/GitHub non-regression.

Out of scope:

- Directories and multi-file batches.
- Archive traversal/ZIP ingestion.
- Images, OCR, image captions, audio/video transcription, YouTube, remote file URLs, Azure/cloud converters, MarkItDown plugins, and LLM vision/captioning.
- Page/slide/sheet/cell/line/cell-level citations.
- Live turbopuffer writes beyond existing `apply --approve` behavior.

## Acceptance criteria

- `turbo-search plan ./example.docx --json` works for a supported text-bearing file and reports `source_kind: local_file`, deterministic `file-docx-<filename-slug>-<sha16>-v1` namespace candidate, generated chunks, local plan paths, and no live API calls.
- `turbo-search crawl --base-url ./example.csv --json` produces the local document corpus shape without live calls.
- Existing PDF plans still use `pdf-<filename-slug>-<sha16>-v1` and `pdf://...`.
- Generated artifacts and row metadata include filename/extension/hash/source_kind but not the absolute local path.
- Empty MarkItDown extraction fails clearly.
- Unsupported extensions fail clearly.
- Existing website, GitHub, PDF, plan/apply, retrieval, and artifact tests continue to pass.
- Documentation states supported extensions and explicit v1 exclusions.

## Evidence expectations

- Unit test command output for new local document tests and existing source-routing tests.
- Full test suite output.
- At least one local-only smoke plan against a generated text/data fixture converted through MarkItDown without mocking, with summary showing no credentials/API calls.
- Artifact privacy check showing the source absolute filepath is absent from generated plan artifacts.
- `git diff --check`, `uv lock --check`, and `git diff --stat`.

## Progress and notes

- 2026-07-08: Opened after user selected local-docs-only MarkItDown support and `file-<ext>-<filename>-<sha16>-v1` identity for non-PDF files.
- 2026-07-08: Marked active and began implementation after explicit user request to execute the ticket.
- 2026-07-08: Implemented local MarkItDown document sources, updated dependencies/docs/tests, and verified with the full suite plus a real CSV smoke plan.
- 2026-07-08: Closed as done. Evidence: `.10x/evidence/2026-07-08-local-markitdown-document-source-ingestion.md`. Review: `.10x/reviews/2026-07-08-local-markitdown-document-source-ingestion-review.md`.

## Blockers

- None.

## References

- `.10x/specs/local-markitdown-document-source-ingestion.md`
- `.10x/decisions/local-document-ingestion-uses-markitdown.md`
- `.10x/research/2026-07-08-markitdown-local-document-types.md`
- `.10x/specs/local-pdf-source-ingestion.md`
- `.10x/decisions/local-pdf-ingestion-uses-markitdown.md`
- `.10x/evidence/2026-07-08-local-markitdown-document-source-ingestion.md`
- `.10x/reviews/2026-07-08-local-markitdown-document-source-ingestion-review.md`
