Status: recorded
Created: 2026-07-08
Updated: 2026-07-08
Target: .10x/tickets/done/2026-07-08-local-markitdown-document-source-ingestion.md
Verdict: pass

# Local MarkItDown Document Source Ingestion Review

## Target

Implementation for `.10x/tickets/done/2026-07-08-local-markitdown-document-source-ingestion.md`, governed by `.10x/specs/local-markitdown-document-source-ingestion.md`.

## Assumptions tested

- PDF identity remains backward-compatible and does not switch to `file-pdf-...`.
- Non-PDF local files use `file-<ext>-<filename-slug>-<sha16>-v1` and synthetic `file://...` URLs.
- Artifact and row metadata carry source identity without storing the absolute source filepath.
- MarkItDown is used through its package-facing `MarkItDown(...).convert(path)` path with plugins disabled.
- Plan/crawl remain local-only and live writes still require the existing explicit apply path.
- Unsupported local extensions do not silently fall through to MarkItDown's broader converter set.

## Findings

### Pass: source identity and routing match the spec

`src/turbo_search/crawler.py` now distinguishes website, GitHub repo, PDF, and non-PDF local document sources. PDFs preserve `PdfSource`, `pdf://...`, and `pdf-...-v1`; non-PDF files use `LocalFileSource`, `file://...`, and `file-<ext>-...-v1`.

### Pass: converter scope is bounded

The implementation uses a fixed extension allowlist and calls `MarkItDown(enable_plugins=False).convert(path)`. It does not enable MarkItDown plugins, remote URL ingestion, Azure/cloud conversion, audio transcription, image captions, OCR, or archive traversal.

### Pass: metadata privacy is preserved

Generated frontmatter, summary, manifest/chunk source metadata, and row construction use filename, extension, hash, source kind, and source ID. Tests and smoke evidence check that the absolute source filepath is not serialized into plan artifacts.

### Pass: plan/apply guardrails remain intact

The local document path plugs into existing crawl/plan artifact generation. Live mutation remains under `apply --approve`; no new live write path was added.

### Minor residual risk: real office fixture coverage is not exhaustive

The evidence includes a real CSV MarkItDown smoke plan plus full unit coverage. It does not include real DOCX/PPTX/XLS/XLSX/EPUB smoke fixtures. This is acceptable for v1 because the implementation delegates those formats to MarkItDown's packaged converters and the ticket required at least one text/data smoke fixture, not exhaustive converter validation. No follow-up ticket is opened unless these formats show runtime converter-specific failures.

## Verdict

Pass. The implementation satisfies the ticket acceptance criteria with the evidence in `.10x/evidence/2026-07-08-local-markitdown-document-source-ingestion.md`.

## Residual risk

No unresolved blocker. The only residual risk is converter-specific behavior for non-smoked office/EPUB files, explicitly accepted as a v1 dependency-delegation limit above.
