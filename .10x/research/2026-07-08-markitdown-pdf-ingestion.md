Status: done
Created: 2026-07-08
Updated: 2026-07-08

# MarkItDown PDF Ingestion Research

## Question

Can `turbo-search` use Microsoft MarkItDown to ingest a local PDF file path into the existing local plan/apply/retrieval workflow, and can MarkItDown preserve PDF page numbers for retrieval citations?

## Sources and methods

- Cloned `https://github.com/microsoft/markitdown` to `/tmp/pi-github-repos/microsoft/markitdown` and inspected commit `e144e0a2be95b34df17433bac904e635f2c5e551`.
- Inspected MarkItDown package README, package metadata, core conversion API, result object, and PDF converter implementation.
- Ran web search for MarkItDown PDF usage and PDF extraction options.

## Findings

- MarkItDown is an MIT-licensed open-source Python package and CLI for converting files to Markdown for indexing/text-analysis workflows. Its package README shows `markitdown path-to-file.pdf > document.md` and Python usage via `MarkItDown().convert(...)`.
  - README permalink: https://github.com/microsoft/markitdown/blob/e144e0a2be95b34df17433bac904e635f2c5e551/packages/markitdown/README.md#L1-L42
  - License permalink: https://github.com/microsoft/markitdown/blob/e144e0a2be95b34df17433bac904e635f2c5e551/LICENSE
- MarkItDown declares PDF support through the `pdf` extra, which depends on `pdfminer.six` and `pdfplumber`.
  - Package metadata permalink: https://github.com/microsoft/markitdown/blob/e144e0a2be95b34df17433bac904e635f2c5e551/packages/markitdown/pyproject.toml#L35-L58
- The core `MarkItDown.convert(...)` method accepts a local path (`str` or `Path`) and routes it through `convert_local(...)`.
  - API permalink: https://github.com/microsoft/markitdown/blob/e144e0a2be95b34df17433bac904e635f2c5e551/packages/markitdown/src/markitdown/_markitdown.py#L275-L360
- `DocumentConverterResult` contains a single Markdown string and optional title. It has no page-number or per-page collection field.
  - Result object permalink: https://github.com/microsoft/markitdown/blob/e144e0a2be95b34df17433bac904e635f2c5e551/packages/markitdown/src/markitdown/_base_converter.py#L5-L40
- MarkItDown's PDF converter internally loops through `pdf.pages`, but returns one joined Markdown string. For prose PDFs with no form-style pages, it falls back to `pdfminer.high_level.extract_text(pdf_bytes)` for the whole document. It does not expose page numbers in the result.
  - PDF converter permalink: https://github.com/microsoft/markitdown/blob/e144e0a2be95b34df17433bac904e635f2c5e551/packages/markitdown/src/markitdown/converters/_pdf_converter.py#L497-L589
- User ratification in the current workstream:
  - Use MarkItDown for local PDF ingestion.
  - Keep MarkItDown as-is and do not add page-level citation support in v1.
  - Use filename plus a short file hash for default namespace identity.
  - Support a single PDF file path first; directory ingestion and OCR are out of scope.

## Conclusions

- MarkItDown is a good fit for v1 local PDF ingestion because it is open source, local/offline for the built-in PDF path, produces Markdown, and targets indexing/text-analysis use cases.
- Page-preserving citations should not be implemented in v1. MarkItDown does not expose page metadata through its current core result object, and the user chose to keep it as-is.
- `turbo-search` should convert one local `.pdf` file into one generated Markdown document, then reuse the existing chunk/plan/apply workflow.
- The implementation should not store absolute local file paths in artifacts or turbopuffer rows; use filename, content hash, and a synthetic `pdf://...` source identity instead.
