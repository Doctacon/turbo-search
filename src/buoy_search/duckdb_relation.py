"""Read-only DuckDB relation acquisition for local corpus planning."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import time
from typing import TYPE_CHECKING, Literal
from urllib.parse import quote, urlparse

import duckdb

from buoy_search.chunker import IndexingPlan, process_corpus, sha256_text

if TYPE_CHECKING:
    from buoy_search.crawler import CrawlOptions

SOURCE_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
DEFAULT_SCAN_BATCH_SIZE = 500
SAFE_DUCKDB_CONFIG = {
    "enable_external_access": "false",
    "autoinstall_known_extensions": "false",
    "autoload_known_extensions": "false",
    "allow_community_extensions": "false",
}
BLOCKED_EXTERNAL_DEPENDENCY_ERRORS = (
    "file system operations are disabled by configuration",
    "loading external extensions is disabled through configuration",
)


class DuckDBRelationError(RuntimeError):
    """Raised when a DuckDB relation cannot be acquired safely."""


@dataclass(frozen=True)
class DuckDBRelationSource:
    """One DuckDB table or view with stable, path-private logical identity."""

    kind: Literal["duckdb_relation"]
    database_path: Path = field(repr=False)
    relation: str
    source_id: str
    id_column: str
    content_column: str
    title_column: str | None

    @property
    def base_url(self) -> str:
        return f"duckdb://{self.source_id}"

    @property
    def site_id(self) -> str:
        return f"duckdb-{self.source_id}"

    @property
    def namespace_candidate(self) -> str:
        return f"{self.site_id}-v1"

    @property
    def default_out_dir(self) -> Path:
        return Path("artifacts/site-crawls") / self.site_id

    def document_url(self, document_id: str) -> str:
        return f"{self.base_url}/{quote(document_id, safe='')}"


@dataclass(frozen=True)
class DuckDBDocument:
    document_id: str
    content: str
    title: str


@dataclass(frozen=True)
class DuckDBScanResult:
    documents: list[DuckDBDocument]
    rows_scanned: int
    documents_skipped_empty: int
    documents_skipped_limit: int
    title_column: str | None


@dataclass(frozen=True)
class DuckDBRelationExecution:
    summary: dict[str, object]
    indexing_plan: IndexingPlan


def validate_source_id(value: str) -> str:
    if not SOURCE_ID_PATTERN.fullmatch(value):
        raise ValueError(
            "--source-id must match ^[a-z0-9]+(?:-[a-z0-9]+)*$ "
            "(lowercase letters, digits, and single hyphens only)."
        )
    return value


def validate_identifier(value: str, *, label: str) -> str:
    if not IDENTIFIER_PATTERN.fullmatch(value):
        raise ValueError(
            f"{label} must match ^[A-Za-z_][A-Za-z0-9_]*$ (an ordinary SQL identifier)."
        )
    return value


def validate_relation(value: str) -> str:
    components = value.split(".")
    if not 1 <= len(components) <= 3:
        raise ValueError("--relation must contain one to three dot-separated identifiers.")
    for component in components:
        validate_identifier(component, label="each --relation component")
    return value


def quote_identifier(value: str) -> str:
    """Quote one already-validated ordinary DuckDB identifier."""

    validate_identifier(value, label="identifier")
    return f'"{value.replace(chr(34), chr(34) * 2)}"'


def quote_relation(value: str) -> str:
    validate_relation(value)
    return ".".join(quote_identifier(component) for component in value.split("."))


def validate_duckdb_base_url(value: str) -> str:
    parsed = urlparse(value)
    if (
        parsed.scheme != "duckdb"
        or not parsed.netloc
        or parsed.username is not None
        or parsed.password is not None
        or parsed.port is not None
        or parsed.path not in {"", "/"}
        or parsed.params
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError(
            "DuckDB base URL must be duckdb://<source-id> with no path, "
            "credentials, port, query, or fragment."
        )
    validate_source_id(parsed.netloc)
    return f"duckdb://{parsed.netloc}"


def is_duckdb_base_url(value: str) -> bool:
    return urlparse(value).scheme == "duckdb"


def source_id_from_base_url(value: str) -> str:
    return urlparse(validate_duckdb_base_url(value)).netloc


def duckdb_relation_source(
    database_path: str | Path,
    *,
    relation: str,
    source_id: str,
    id_column: str = "document_id",
    content_column: str = "content",
    title_column: str | None = None,
) -> DuckDBRelationSource:
    path = Path(database_path).expanduser()
    if not path.exists():
        raise ValueError(f"DuckDB database path does not exist: {database_path}")
    if not path.is_file():
        raise ValueError(f"DuckDB database path must be an existing regular file: {database_path}")
    return DuckDBRelationSource(
        kind="duckdb_relation",
        database_path=path,
        relation=validate_relation(relation),
        source_id=validate_source_id(source_id),
        id_column=validate_identifier(id_column, label="--id-column"),
        content_column=validate_identifier(content_column, label="--content-column"),
        title_column=(
            validate_identifier(title_column, label="--title-column")
            if title_column is not None
            else None
        ),
    )


def scan_duckdb_relation(
    source: DuckDBRelationSource,
    *,
    max_documents: int,
    batch_size: int = DEFAULT_SCAN_BATCH_SIZE,
) -> DuckDBScanResult:
    """Validate and deterministically scan one relation through one read-only connection."""

    if max_documents <= 0:
        raise ValueError("max_documents must be greater than zero")
    if batch_size <= 0:
        raise ValueError("batch_size must be greater than zero")

    relation_sql = quote_relation(source.relation)
    try:
        with duckdb.connect(
            str(source.database_path),
            read_only=True,
            config=SAFE_DUCKDB_CONFIG,
        ) as connection:
            # Text conversion of TIMESTAMPTZ values otherwise inherits the host/session zone.
            connection.execute("SET TimeZone='UTC'")
            connection.execute("BEGIN TRANSACTION")
            try:
                description = connection.execute(f"SELECT * FROM {relation_sql} LIMIT 0").description
                available = {str(column[0]).casefold(): str(column[0]) for column in description}
                id_column = require_column(available, source.id_column, label="ID")
                content_column = require_column(available, source.content_column, label="content")
                if source.title_column is not None:
                    title_column = require_column(available, source.title_column, label="title")
                else:
                    title_column = available.get("title")

                title_expression = (
                    f"CAST({quote_identifier(title_column)} AS VARCHAR)"
                    if title_column is not None
                    else "NULL"
                )
                id_expression = f"CAST({quote_identifier(id_column)} AS VARCHAR)"
                cursor = connection.execute(
                    f"SELECT {id_expression}, "
                    f"CAST({quote_identifier(content_column)} AS VARCHAR), "
                    f"{title_expression} "
                    f"FROM {relation_sql} "
                    f"ORDER BY {id_expression} COLLATE \"binary\" NULLS FIRST"
                )
                documents: list[DuckDBDocument] = []
                seen_ids: set[str] = set()
                rows_scanned = 0
                skipped_empty = 0
                skipped_limit = 0
                while True:
                    rows = cursor.fetchmany(batch_size)
                    if not rows:
                        break
                    for raw_id, raw_content, raw_title in rows:
                        rows_scanned += 1
                        if raw_id is None or not str(raw_id).strip():
                            raise DuckDBRelationError(
                                f"DuckDB relation {source.relation!r} contains a null or blank document ID "
                                f"in column {source.id_column!r}."
                            )
                        document_id = str(raw_id)
                        if document_id in seen_ids:
                            raise DuckDBRelationError(
                                f"DuckDB relation {source.relation!r} contains duplicate document ID "
                                f"{document_id!r} after text conversion."
                            )
                        seen_ids.add(document_id)
                        if raw_content is None or not str(raw_content).strip():
                            skipped_empty += 1
                            continue
                        if len(documents) >= max_documents:
                            skipped_limit += 1
                            continue
                        title = str(raw_title) if raw_title is not None else ""
                        documents.append(
                            DuckDBDocument(
                                document_id=document_id,
                                content=str(raw_content),
                                title=title if title.strip() else document_id,
                            )
                        )
            finally:
                connection.execute("ROLLBACK")
    except DuckDBRelationError:
        raise
    except duckdb.Error as exc:
        if isinstance(exc, duckdb.PermissionException) and any(
            marker in str(exc).casefold() for marker in BLOCKED_EXTERNAL_DEPENDENCY_ERRORS
        ):
            raise DuckDBRelationError(
                f"DuckDB relation {source.relation!r} depends on external files, databases, "
                "or extensions, which Buoy disables for safe read-only indexing. Materialize "
                "the final relation as a table in this DuckDB database upstream, then plan again."
            ) from exc
        raise DuckDBRelationError(
            f"Could not read DuckDB relation {source.relation!r} in read-only mode: {exc}"
        ) from exc

    if not documents:
        raise DuckDBRelationError(
            f"DuckDB relation {source.relation!r} contains no nonblank documents in "
            f"content column {source.content_column!r}."
        )
    return DuckDBScanResult(
        documents=documents,
        rows_scanned=rows_scanned,
        documents_skipped_empty=skipped_empty,
        documents_skipped_limit=skipped_limit,
        title_column=title_column,
    )


def require_column(available: dict[str, str], requested: str, *, label: str) -> str:
    actual = available.get(requested.casefold())
    if actual is None:
        names = ", ".join(sorted(available.values())) or "<none>"
        raise DuckDBRelationError(
            f"DuckDB relation is missing {label} column {requested!r}; available columns: {names}."
        )
    return actual


def stable_page_filename(source: DuckDBRelationSource, document_id: str) -> str:
    digest = hashlib.sha256(source.document_url(document_id).encode("utf-8")).hexdigest()
    return f"document-{digest[:24]}.md"


def write_duckdb_corpus(
    source: DuckDBRelationSource,
    documents: list[DuckDBDocument],
    pages_dir: Path,
    *,
    crawl_timestamp: str,
) -> None:
    pages_dir.mkdir(parents=True, exist_ok=True)
    for stale_page in pages_dir.glob("*.md"):
        stale_page.unlink()
    for document in documents:
        frontmatter = {
            "url": source.document_url(document.document_id),
            "title": document.title,
            "status": 200,
            "content_type": "text/markdown; charset=utf-8",
            "source_kind": "duckdb_relation",
            "duckdb_source_id": source.source_id,
            "duckdb_relation": source.relation,
            "duckdb_document_id": document.document_id,
            "source_hash": sha256_text(document.content),
            "crawl_timestamp": crawl_timestamp,
            "fetcher": "duckdb-read-only",
        }
        lines = ["---"]
        lines.extend(f"{key}: {json.dumps(value, ensure_ascii=False)}" for key, value in frontmatter.items())
        lines.extend(["---", ""])
        (pages_dir / stable_page_filename(source, document.document_id)).write_text(
            "\n".join(lines) + document.content, encoding="utf-8"
        )


def crawl_duckdb_relation_with_plan(
    source: DuckDBRelationSource, options: CrawlOptions
) -> DuckDBRelationExecution:
    """Materialize one relation and hand it to the shared corpus processor."""

    started_at = time.monotonic()
    scan_started_at = time.monotonic()
    scan = scan_duckdb_relation(source, max_documents=options.max_pages)
    scan_seconds = max(0.0, time.monotonic() - scan_started_at)
    pages_dir = options.out_dir / "pages"
    write_started_at = time.monotonic()
    write_duckdb_corpus(
        source,
        scan.documents,
        pages_dir,
        crawl_timestamp=datetime.now(timezone.utc).isoformat(),
    )
    corpus_write_seconds = max(0.0, time.monotonic() - write_started_at)
    chunk_started_at = time.monotonic()
    plan = process_corpus(
        pages_dir,
        limit_chunks=options.max_chunks,
        target_tokens=options.target_tokens,
        overlap_sentences=options.overlap_sentences,
    )
    chunking_seconds = max(0.0, time.monotonic() - chunk_started_at)
    summary: dict[str, object] = {
        "command": "crawl",
        "dry_run": True,
        "credentials_required": False,
        "turbopuffer_api_calls": False,
        "api_calls_occurred": False,
        "source_kind": "duckdb_relation",
        "base_url": source.base_url,
        "duckdb_source_id": source.source_id,
        "duckdb_relation": source.relation,
        "id_column": source.id_column,
        "content_column": source.content_column,
        "title_column": scan.title_column,
        "title_column_detected": scan.title_column is not None,
        "allowed_host": "",
        "namespace_candidate": source.namespace_candidate,
        "crawl_strategy": "duckdb-read-only",
        "requested_crawl_strategy": options.crawl_strategy,
        "docs_version_policy": options.docs_version_policy,
        "docs_version_report": {"detected": False, "policy": options.docs_version_policy},
        "language_policy": options.language_policy,
        "language_report": {"detected": False, "policy": options.language_policy},
        "sitemap_seed_urls": [],
        "out_dir": str(options.out_dir),
        "pages_dir": str(pages_dir),
        "max_pages": options.max_pages,
        "max_chunks": options.max_chunks,
        "include_paths": [],
        "exclude_paths": [],
        "strip_trailing_slash": options.strip_trailing_slash,
        "css_selector": None,
        "target_tokens": options.target_tokens,
        "overlap_sentences": options.overlap_sentences,
        "rows_scanned": scan.rows_scanned,
        "documents_selected": len(scan.documents),
        "documents_generated": len(scan.documents),
        "documents_skipped_empty": scan.documents_skipped_empty,
        "documents_skipped_limit": scan.documents_skipped_limit,
        "pages_scraped": len(scan.documents),
        "requests_count": 0,
        "robots_disallowed_count": 0,
        "blocked_requests_count": 0,
        "failed_requests_count": 0,
        "files_discovered": plan.files_discovered,
        "files_seen": plan.stats.files_seen,
        "files_error": plan.stats.files_error,
        "chunks_generated": plan.stats.chunks_generated,
        "document_limit_reached": bool(scan.documents_skipped_limit),
        "chunk_limit_reached": plan.limit_reached,
        "limit_reached": bool(scan.documents_skipped_limit) or plan.limit_reached,
        "sample_chunks": [
            {
                "id": chunk.id,
                "title": chunk.title,
                "url": chunk.url,
                "section_path": chunk.section_path,
                "content_preview": chunk.content[:240].replace("\n", " "),
            }
            for chunk in plan.chunks[:3]
        ],
        "errors": [error.__dict__ for error in plan.stats.errors[:10]],
        "timing": {
            "elapsed_seconds": max(0.0, time.monotonic() - started_at),
            "sitemap_policy_seconds": 0.0,
            "crawl_seconds": scan_seconds,
            "corpus_write_seconds": corpus_write_seconds,
            "chunking_seconds": chunking_seconds,
        },
    }
    options.out_dir.mkdir(parents=True, exist_ok=True)
    (options.out_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8"
    )
    return DuckDBRelationExecution(summary=summary, indexing_plan=plan)


def crawl_duckdb_relation(
    source: DuckDBRelationSource, options: CrawlOptions
) -> dict[str, object]:
    return crawl_duckdb_relation_with_plan(source, options).summary
