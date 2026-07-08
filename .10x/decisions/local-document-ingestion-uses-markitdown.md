Status: active
Created: 2026-07-08
Updated: 2026-07-08

# Local Document Ingestion Uses MarkItDown Local Converters

## Context

`turbo-search` has local PDF ingestion using Microsoft MarkItDown and synthetic, path-private source identity. The user asked to extend support to other MarkItDown file types. MarkItDown supports many converters, including local office/text/data/document formats as well as converters that may involve images, audio transcription, remote URLs, YouTube, or Azure/cloud services.

The project has an open-source-first/local-control preference. The user selected the recommended v1 scope: local document/data files only, with non-PDF namespaces shaped as `file-<ext>-<filename-slug>-<sha16>-v1`.

## Decision

Extend local source ingestion to a fixed allowlist of local MarkItDown document/data file extensions:

- `.pdf` via existing PDF behavior;
- `.docx`;
- `.pptx`;
- `.xlsx`;
- `.xls`;
- `.csv`;
- `.html` and `.htm`;
- `.txt` and `.text`;
- `.md` and `.markdown`;
- `.json` and `.jsonl`;
- `.xml`;
- `.ipynb`;
- `.epub`.

PDF behavior MUST remain backward-compatible with the existing `pdf-...` namespace prefix and `pdf://...` synthetic document URLs.

Non-PDF local files MUST use:

- `source_id`: `file-<extension-without-dot>-<filename-slug>-<sha16>`;
- `namespace_candidate`: `file-<extension-without-dot>-<filename-slug>-<sha16>-v1`;
- source/base identity: `file://<source_id>`;
- document citation URL: `file://<source_id>/<url-encoded-filename>`.

Conversion MUST use MarkItDown's normal local conversion path through the package-facing Python interface. The implementation MUST NOT enable MarkItDown plugins, OCR, image captions, audio transcription, YouTube transcription, Azure/content-understanding/document-intelligence, or remote URL ingestion for this v1.

## Alternatives considered

- Support every MarkItDown converter: rejected for v1 because it would pull in non-document, remote, cloud, image, audio, archive, and high-edge-case behaviors beyond the requested safe local-docs scope.
- Office-only expansion: rejected because the user selected broader local docs/data support.
- Per-type namespace prefixes such as `docx-...` and `pptx-...`: rejected because the user selected `file-<ext>-...` for non-PDF files.
- Replace PDF `pdf-...` naming with `file-pdf-...`: rejected to preserve backward compatibility with the just-added PDF behavior and namespaces already created.

## Consequences

- Local document ingestion can reuse the existing Markdown chunking, plan/apply, and retrieval paths.
- Non-PDF citations identify the file, not page/slide/sheet/cell/line positions.
- Generated artifacts and rows must store filename, extension, SHA-256 hash, and synthetic source ID, not the absolute local filepath.
- Runtime dependencies expand to MarkItDown extras for office file conversion.
