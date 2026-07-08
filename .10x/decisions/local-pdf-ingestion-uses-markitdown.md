Status: active
Created: 2026-07-08
Updated: 2026-07-08

# Local PDF Ingestion Uses MarkItDown

## Context

`turbo-search` currently has first-class source acquisition for public websites and public GitHub repositories. The user wants to pass a local PDF filepath and index the PDF through the same plan/apply workflow.

The project has a standing open-source-first architecture rule. Microsoft MarkItDown is an MIT-licensed open-source Python package that converts PDFs and other files to Markdown for indexing/text-analysis workflows. Inspection in `.10x/research/2026-07-08-markitdown-pdf-ingestion.md` found that MarkItDown supports local path conversion and PDF conversion through the `pdf` extra, but it returns a single Markdown result without page metadata.

The user explicitly selected:

- single PDF filepath support for v1;
- no OCR/scanned-PDF handling in v1;
- filename-plus-hash namespace identity;
- keep MarkItDown as-is and do not add page-number citations.

## Decision

Use Microsoft MarkItDown as the local PDF-to-Markdown converter for v1 PDF ingestion.

The v1 implementation MUST use MarkItDown's normal local conversion path and MUST NOT fork, vendor, patch, monkeypatch, or depend on MarkItDown internals for page-number preservation.

Default PDF identity MUST be based on the PDF filename plus a short SHA-256 hash of the file bytes, not on the absolute local path.

## Alternatives considered

- `pypdf` directly: rejected for v1 because the user asked to use MarkItDown and MarkItDown already wraps PDF extraction for Markdown-oriented indexing.
- Split PDFs into one-page streams and call MarkItDown per page: rejected by the user for v1; page citations are not required.
- Fork or extend MarkItDown internals to emit page metadata: rejected for v1 because it increases maintenance surface and contradicts the user's request to keep MarkItDown as-is.
- OCR plugin or Azure/cloud document understanding: rejected for v1 because the selected scope is text PDFs only and the project defaults to local/open-source components.

## Consequences

- PDF ingestion can reuse the existing Markdown chunking, local plan, apply preflight, approved live apply, and retrieval paths.
- Retrieval citations for PDF content identify the document, not the PDF page number.
- Scanned/image-only PDFs may produce no useful text; v1 should fail clearly or report zero extractable content rather than silently implying OCR support.
- `markitdown[pdf]` becomes a runtime dependency of the CLI.

## Evidence

- `.10x/research/2026-07-08-markitdown-pdf-ingestion.md`
