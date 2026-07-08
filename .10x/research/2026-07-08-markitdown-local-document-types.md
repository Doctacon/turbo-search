Status: done
Created: 2026-07-08
Updated: 2026-07-08

# MarkItDown Local Document Type Support

## Question

Which MarkItDown-backed local file types should `turbo-search` support after PDF ingestion, and which dependencies or exclusions matter for a local-only v1?

## Sources and methods

- Inspected installed MarkItDown package metadata via `uv run python` after adding `markitdown[pdf]`.
- Inspected converter modules under `.venv/lib/python3.13/site-packages/markitdown/converters/`.
- Checked a minimal local XML conversion through `MarkItDown().convert(...)`.
- User ratified the recommended v1 scope in the current workstream: local docs only, with `file-<ext>-<filename>-<sha16>-v1` non-PDF namespace identity.

## Findings

- Installed MarkItDown version observed: `0.1.6`.
- MarkItDown package extras observed from metadata:
  - `pdf`: `pdfminer-six`, `pdfplumber`.
  - `docx`: `mammoth`, `lxml`.
  - `pptx`: `python-pptx`.
  - `xlsx`: `pandas`, `openpyxl`.
  - `xls`: `pandas`, `xlrd`.
  - `audio-transcription`: `pydub`, `SpeechRecognition`.
  - `youtube-transcription`: `youtube-transcript-api`.
  - Azure/content-understanding extras depend on Azure packages.
- Local converters observed in the package include PDF, DOCX, PPTX, XLSX/XLS, CSV, HTML, plain text/Markdown/JSON/JSONL, IPYNB, EPUB, ZIP, Outlook MSG, image, audio, YouTube, RSS/Wikipedia/Bing SERP, and Azure-backed converters.
- Converter module accepted-extension observations relevant to the ratified local-docs v1:
  - DOCX: `.docx`.
  - PPTX: `.pptx`.
  - XLSX/XLS: `.xlsx`, `.xls`.
  - CSV: `.csv`.
  - HTML: `.html`, `.htm`.
  - Plain text: `.txt`, `.text`, `.md`, `.markdown`, `.json`, `.jsonl`; XML also converted successfully in a minimal local test.
  - IPYNB: `.ipynb`.
  - EPUB: `.epub`.
- User-selected v1 excludes audio, images, YouTube, Azure/cloud conversion, remote URLs, and broader local converter behavior.

## Conclusions

- `turbo-search` should generalize the existing PDF path to a local MarkItDown document source for a fixed extension allowlist.
- PDF identity should remain backward-compatible with existing `pdf-...` namespaces and `pdf://...` source URIs.
- Non-PDF local file identity should use `file-<ext>-<filename-slug>-<sha16>` and synthetic `file://...` source/document URLs.
- Dependencies should be limited to MarkItDown extras needed for the selected local document types: existing `pdf`, plus `docx`, `pptx`, `xlsx`, and `xls`. Base MarkItDown covers the simpler text/data/html/notebook/epub paths observed.
- Whole-file conversion should remain v1 behavior. Slide/page/sheet/cell citations, directories, archives, OCR, audio transcription, image captions, remote URLs, plugins, and cloud conversion remain out of scope.
