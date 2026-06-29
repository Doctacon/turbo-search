"""Hybrid retrieval helpers for turbopuffer-backed site search.

Dry-run planning is local-only. Live retrieval is intentionally isolated behind
``HybridRetriever.from_config`` so credentials are read only when the caller has
explicitly opted into a live turbopuffer query.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import os
from typing import Any, Mapping, Protocol, Sequence

from turbo_search.config import RuntimeConfig
from turbo_search.chunker import SentenceTransformerEmbedder

DEFAULT_TOP_K = 5
DEFAULT_CANDIDATES = 200
DEFAULT_RANKING_POOL = 100
DEFAULT_RANKING_MODE = "file"
DEFAULT_RANKING_PROFILE = "repo_code"
DEFAULT_RANKING_AGGREGATION = "max"
DEFAULT_WEBSITE_RANKING_MODE = "page"
DEFAULT_WEBSITE_RANKING_PROFILE = "none"
DEFAULT_WEBSITE_RANKING_POOL = 20
DEFAULT_WEBSITE_RANKING_AGGREGATION = "max"
RANKING_MODES = {"chunk", "file", "page"}
RANKING_PROFILES = {"none", "repo_code"}
RANKING_AGGREGATIONS = {"max", "capped_sum_3"}
RRF_K = 60
RETRIEVAL_ATTRIBUTES = [
    "title",
    "url",
    "section_path",
    "content",
    "path",
    "repo_path",
    "doc_kind",
    "chunk_index",
]
SCHEMA_PORTABLE_RETRIEVAL_ATTRIBUTES = [attribute for attribute in RETRIEVAL_ATTRIBUTES if attribute != "repo_path"]


def namespace_uses_website_defaults(namespace: str) -> bool:
    """Return true when a namespace should use website ranking defaults."""

    return namespace.startswith("site-")


def ranking_defaults_for_namespace(namespace: str) -> dict[str, object]:
    """Return namespace-aware ranking defaults for CLI and experiment runners."""

    if namespace_uses_website_defaults(namespace):
        return {
            "ranking_mode": DEFAULT_WEBSITE_RANKING_MODE,
            "ranking_profile": DEFAULT_WEBSITE_RANKING_PROFILE,
            "ranking_pool": DEFAULT_WEBSITE_RANKING_POOL,
            "ranking_aggregation": DEFAULT_WEBSITE_RANKING_AGGREGATION,
        }
    return {
        "ranking_mode": DEFAULT_RANKING_MODE,
        "ranking_profile": DEFAULT_RANKING_PROFILE,
        "ranking_pool": DEFAULT_RANKING_POOL,
        "ranking_aggregation": DEFAULT_RANKING_AGGREGATION,
    }


class Embedder(Protocol):
    def encode(self, texts: Sequence[str]) -> list[list[float]]:
        """Return one embedding vector per input text."""


@dataclass(frozen=True)
class RetrievalOptions:
    """Validated knobs for hybrid retrieval."""

    top_k: int = DEFAULT_TOP_K
    candidates: int = DEFAULT_CANDIDATES
    doc_kind: str | None = None
    ranking_mode: str = DEFAULT_RANKING_MODE
    ranking_profile: str = DEFAULT_RANKING_PROFILE
    ranking_pool: int = DEFAULT_RANKING_POOL
    ranking_aggregation: str = DEFAULT_RANKING_AGGREGATION

    def __post_init__(self) -> None:
        if self.top_k <= 0:
            raise ValueError("top_k must be greater than zero.")
        if self.candidates <= 0:
            raise ValueError("candidates must be greater than zero.")
        if self.ranking_pool <= 0:
            raise ValueError("ranking_pool must be greater than zero.")
        if self.ranking_mode not in RANKING_MODES:
            raise ValueError(f"ranking_mode must be one of {sorted(RANKING_MODES)}.")
        if self.ranking_profile not in RANKING_PROFILES:
            raise ValueError(f"ranking_profile must be one of {sorted(RANKING_PROFILES)}.")
        if self.ranking_aggregation not in RANKING_AGGREGATIONS:
            raise ValueError(f"ranking_aggregation must be one of {sorted(RANKING_AGGREGATIONS)}.")

    @property
    def effective_ranking_pool(self) -> int:
        return max(self.top_k, self.ranking_pool if self.ranking_mode in {"file", "page"} else self.top_k)


@dataclass
class SearchHit:
    """One retrieved chunk plus citation and score metadata."""

    id: str
    title: str = ""
    url: str = ""
    section_path: str = ""
    content: str = ""
    path: str = ""
    repo_path: str = ""
    score_info: dict[str, object] = field(default_factory=dict)
    doc_kind: str = ""
    chunk_index: int | None = None

    def to_dict(self, *, include_content: bool = True) -> dict[str, object]:
        payload: dict[str, object] = {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "section_path": self.section_path,
            "path": self.path,
            "repo_path": self.repo_path,
            "score_info": self.score_info,
        }
        if include_content:
            payload["content"] = self.content
        if self.doc_kind:
            payload["doc_kind"] = self.doc_kind
        if self.chunk_index is not None:
            payload["chunk_index"] = self.chunk_index
        return payload


@dataclass
class RetrievalResult:
    """Structured retrieval response for CLI/library callers."""

    query: str
    hits: list[SearchHit]
    region: str
    namespace: str
    embedding_model: str
    top_k: int
    candidates: int
    doc_kind: str | None
    fusion: str
    ranking_mode: str
    ranking_profile: str
    ranking_pool: int
    ranking_aggregation: str
    dry_run: bool = False
    turbopuffer_api_calls: bool = True

    def to_dict(self) -> dict[str, object]:
        return {
            "command": "retrieve",
            "dry_run": self.dry_run,
            "credentials_required": not self.dry_run,
            "turbopuffer_api_calls": self.turbopuffer_api_calls,
            "api_calls_occurred": self.turbopuffer_api_calls,
            "query": self.query,
            "region": self.region,
            "namespace": self.namespace,
            "embedding_model": self.embedding_model,
            "top_k": self.top_k,
            "candidates": self.candidates,
            "doc_kind": self.doc_kind,
            "ranking_mode": self.ranking_mode,
            "ranking_profile": self.ranking_profile,
            "ranking_pool": self.ranking_pool,
            "ranking_aggregation": self.ranking_aggregation,
            "fusion": self.fusion,
            "hits": [hit.to_dict() for hit in self.hits],
        }


@dataclass(frozen=True)
class RetrievalPlan:
    """Safe no-credential plan for the retrieve command."""

    query: str
    config: RuntimeConfig
    options: RetrievalOptions

    def to_dict(self) -> dict[str, object]:
        ann_subquery: dict[str, object] = {
            "name": "ann",
            "rank_by": ["vector", "ANN", "<query embedding>"],
            "limit": self.options.candidates,
            "include_attributes": RETRIEVAL_ATTRIBUTES,
        }
        bm25_subquery: dict[str, object] = {
            "name": "bm25",
            "rank_by": bm25_rank_by(self.query),
            "limit": self.options.candidates,
            "include_attributes": RETRIEVAL_ATTRIBUTES,
        }
        if self.options.doc_kind:
            doc_filter = ("doc_kind", "Eq", self.options.doc_kind)
            ann_subquery["filters"] = doc_filter
            bm25_subquery["filters"] = doc_filter
        return {
            "command": "retrieve",
            "dry_run": True,
            "plan": True,
            "credentials_required": False,
            "turbopuffer_api_calls": False,
            "api_calls_occurred": False,
            "query": self.query,
            "region": self.config.region,
            "namespace": self.config.namespace,
            "embedding_model": self.config.embedding_model,
            "top_k": self.options.top_k,
            "candidates": self.options.candidates,
            "doc_kind": self.options.doc_kind,
            "ranking_mode": self.options.ranking_mode,
            "ranking_profile": self.options.ranking_profile,
            "ranking_pool": self.options.ranking_pool,
            "ranking_aggregation": self.options.ranking_aggregation,
            "live_execution": "pass --live to embed the query and call turbopuffer",
            "retrieval": {
                "request": "turbopuffer multi_query",
                "subqueries": [ann_subquery, bm25_subquery],
                "rerank_by": ["RRF"],
                "fallback": "client-side reciprocal-rank fusion if server RRF is unsupported or separate lists are returned",
            },
        }


class HybridRetriever:
    """Small wrapper around query embedding and turbopuffer multi-query."""

    def __init__(
        self,
        *,
        namespace: object,
        embedder: Embedder,
        config: RuntimeConfig,
    ) -> None:
        self._namespace = namespace
        self._embedder = embedder
        self._config = config

    @classmethod
    def from_config(cls, config: RuntimeConfig) -> "HybridRetriever":
        """Build a live retriever, reading the API key from the environment only."""

        api_key = os.environ.get("TURBOPUFFER_API_KEY")
        if not api_key:
            raise RuntimeError(
                "TURBOPUFFER_API_KEY must be set in the environment for live retrieval. "
                "Use `retrieve --dry-run` or omit `--live` to inspect the plan without credentials."
            )
        embedder = SentenceTransformerEmbedder(config.embedding_model)
        namespace = build_namespace(config=config, api_key=api_key)
        return cls(namespace=namespace, embedder=embedder, config=config)

    def retrieve(self, query: str, options: RetrievalOptions) -> RetrievalResult:
        cleaned_query = query.strip()
        if not cleaned_query:
            raise RuntimeError("A non-empty query is required for retrieval.")
        vectors = self._embedder.encode([cleaned_query])
        if not vectors or not vectors[0]:
            raise RuntimeError("The embedding model returned no vector for the query.")

        subqueries = build_multi_query_subqueries(
            query=cleaned_query,
            query_vector=vectors[0],
            candidates=options.candidates,
            doc_kind=options.doc_kind,
        )
        try:
            response, fusion = run_multi_query(self._namespace, subqueries)
        except Exception as exc:  # pragma: no cover - SDK/network/schema failure paths are integration-tested.
            if not is_missing_attribute_error(exc, "repo_path"):
                raise RuntimeError(user_friendly_query_error(exc)) from exc
            portable_subqueries = build_multi_query_subqueries(
                query=cleaned_query,
                query_vector=vectors[0],
                candidates=options.candidates,
                doc_kind=options.doc_kind,
                include_attributes=SCHEMA_PORTABLE_RETRIEVAL_ATTRIBUTES,
            )
            try:
                response, fusion = run_multi_query(self._namespace, portable_subqueries)
            except Exception as fallback_exc:  # pragma: no cover - requires SDK/network failure.
                raise RuntimeError(user_friendly_query_error(fallback_exc)) from fallback_exc

        result_lists = extract_result_lists(response)
        if not result_lists:
            return RetrievalResult(
                query=cleaned_query,
                hits=[],
                region=self._config.region,
                namespace=self._config.namespace,
                embedding_model=self._config.embedding_model,
                top_k=options.top_k,
                candidates=options.candidates,
                doc_kind=options.doc_kind,
                fusion=fusion,
                ranking_mode=options.ranking_mode,
                ranking_profile=options.ranking_profile,
                ranking_pool=options.ranking_pool,
                ranking_aggregation=options.ranking_aggregation,
            )
        ranking_pool = options.effective_ranking_pool
        if fusion == "client_rrf" or len(result_lists) > 1:
            hits = client_side_rrf(result_lists, top_k=ranking_pool)
            fusion = "client_rrf"
        else:
            hits = [
                row_to_hit(row, score_info={"fusion": "server_rrf", "source_rank": rank})
                for rank, row in enumerate(result_lists[0], start=1)
            ][:ranking_pool]
        hits = rank_hits(hits, options=options)[: options.top_k]
        return RetrievalResult(
            query=cleaned_query,
            hits=hits,
            region=self._config.region,
            namespace=self._config.namespace,
            embedding_model=self._config.embedding_model,
            top_k=options.top_k,
            candidates=options.candidates,
            doc_kind=options.doc_kind,
            fusion=fusion,
            ranking_mode=options.ranking_mode,
            ranking_profile=options.ranking_profile,
            ranking_pool=options.ranking_pool,
            ranking_aggregation=options.ranking_aggregation,
        )


def retrieval_plan(query: str, *, config: RuntimeConfig, options: RetrievalOptions) -> RetrievalPlan:
    return RetrievalPlan(query=query, config=config, options=options)


def build_multi_query_subqueries(
    *,
    query: str,
    query_vector: Sequence[float],
    candidates: int,
    doc_kind: str | None = None,
    include_attributes: Sequence[str] = RETRIEVAL_ATTRIBUTES,
) -> list[dict[str, object]]:
    """Build ANN and boosted BM25 subqueries for one turbopuffer multi-query."""

    common: dict[str, object] = {
        "limit": candidates,
        "include_attributes": list(include_attributes),
    }
    if doc_kind:
        common["filters"] = ("doc_kind", "Eq", doc_kind)
    return [
        {
            **common,
            "rank_by": ("vector", "ANN", list(query_vector)),
        },
        {
            **common,
            "rank_by": bm25_rank_by(query),
        },
    ]


def bm25_rank_by(query: str) -> tuple[object, ...]:
    """Return boosted BM25 expression over citation/content fields."""

    return (
        "Sum",
        [
            ("Product", 2.0, ("title", "BM25", query)),
            ("Product", 1.5, ("section_path", "BM25", query)),
            ("content", "BM25", query),
        ],
    )


def run_multi_query(namespace: object, subqueries: Sequence[dict[str, object]]) -> tuple[object, str]:
    fusion = "server_rrf"
    try:
        return namespace.multi_query(queries=subqueries, rerank_by=("RRF",)), fusion  # type: ignore[attr-defined]
    except TypeError as exc:
        if not is_unsupported_rerank_type_error(exc):
            raise
        fusion = "client_rrf"
        return namespace.multi_query(queries=subqueries), fusion  # type: ignore[attr-defined]


def build_namespace(*, config: RuntimeConfig, api_key: str) -> object:
    try:
        import turbopuffer as tpuf
    except ImportError as exc:  # pragma: no cover - depends on optional install.
        raise RuntimeError("turbopuffer is required for live retrieval. Run `uv sync` first.") from exc

    if hasattr(tpuf, "api_key"):
        setattr(tpuf, "api_key", api_key)
    if hasattr(tpuf, "api_base_url"):
        setattr(tpuf, "api_base_url", f"https://{config.region}.turbopuffer.com")
    if hasattr(tpuf, "Turbopuffer"):
        try:
            client = tpuf.Turbopuffer(api_key=api_key, region=config.region)  # type: ignore[attr-defined]
        except TypeError:
            client = tpuf.Turbopuffer(api_key=api_key)  # type: ignore[attr-defined]
        if hasattr(client, "namespace"):
            return client.namespace(config.namespace)
        if hasattr(client, "Namespace"):
            return client.Namespace(config.namespace)
    if hasattr(tpuf, "Namespace"):
        return tpuf.Namespace(config.namespace)  # type: ignore[attr-defined]
    raise RuntimeError("Unsupported turbopuffer SDK: no Namespace constructor found.")


def is_unsupported_rerank_type_error(exc: TypeError) -> bool:
    message = str(exc).lower()
    return "rerank_by" in message or "unexpected keyword" in message or "unexpected argument" in message


def is_missing_attribute_error(exc: BaseException, attribute: str) -> bool:
    message = str(exc).casefold()
    attribute_text = attribute.casefold()
    return attribute_text in message and "not found in schema" in message


def user_friendly_query_error(exc: BaseException) -> str:
    message = str(exc) or exc.__class__.__name__
    return (
        "Live retrieval failed. Likely fixes: confirm TURBOPUFFER_API_KEY is set, "
        "the namespace has been indexed, and TURBOPUFFER_REGION/TURBOPUFFER_NAMESPACE match the indexed corpus. "
        f"Underlying error: {message}"
    )


def extract_result_lists(response: object) -> list[list[object]]:
    """Normalize common SDK multi_query response shapes into row lists."""

    if response is None:
        return []

    direct_rows = get_field(response, "rows")
    if direct_rows is not None:
        return [list(direct_rows)]

    for field_name in ("results", "queries", "responses", "result_sets"):
        value = get_field(response, field_name)
        lists = extract_nested_lists(value)
        if lists:
            return lists

    if isinstance(response, Sequence) and not isinstance(response, (str, bytes, bytearray)):
        lists = extract_nested_lists(response)
        if lists:
            return lists
    return []


def extract_nested_lists(value: object) -> list[list[object]]:
    if value is None:
        return []
    if isinstance(value, Mapping):
        rows = get_field(value, "rows")
        return [list(rows)] if rows is not None else []
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        value_list = list(value)
        if not value_list:
            return []
        if all(is_row_like(item) for item in value_list):
            return [value_list]
        lists: list[list[object]] = []
        for item in value_list:
            rows = get_field(item, "rows")
            if rows is not None:
                lists.append(list(rows))
            elif isinstance(item, Sequence) and not isinstance(item, (str, bytes, bytearray)):
                lists.append(list(item))
        return [rows for rows in lists if rows]
    rows = get_field(value, "rows")
    return [list(rows)] if rows is not None else []


def is_row_like(item: object) -> bool:
    if isinstance(item, Mapping):
        return "id" in item or "attributes" in item or any(name in item for name in RETRIEVAL_ATTRIBUTES)
    return any(hasattr(item, name) for name in ("id", "attributes", "title", "content"))


def client_side_rrf(result_lists: Sequence[Sequence[object]], *, top_k: int, rrf_k: int = RRF_K) -> list[SearchHit]:
    scores: dict[str, float] = {}
    rows_by_key: dict[str, object] = {}
    ranks_by_key: dict[str, dict[str, int]] = {}
    names = ["ann", "bm25"]
    for list_index, rows in enumerate(result_lists):
        source_name = names[list_index] if list_index < len(names) else f"query_{list_index + 1}"
        for rank, row in enumerate(rows, start=1):
            key = row_key(row)
            if not key:
                continue
            scores[key] = scores.get(key, 0.0) + 1.0 / (rrf_k + rank)
            rows_by_key.setdefault(key, row)
            ranks_by_key.setdefault(key, {})[source_name] = rank
    ordered = sorted(scores, key=lambda key: (-scores[key], min(ranks_by_key[key].values()), key))[:top_k]
    hits: list[SearchHit] = []
    for key in ordered:
        hits.append(
            row_to_hit(
                rows_by_key[key],
                score_info={
                    "fusion": "client_rrf",
                    "rrf_score": scores[key],
                    "source_ranks": ranks_by_key[key],
                },
            )
        )
    return hits


def rank_hits(hits: Sequence[SearchHit], *, options: RetrievalOptions) -> list[SearchHit]:
    """Apply the configured final ranking layer to fused retrieval candidates."""

    if options.ranking_mode == "chunk":
        return list(hits)

    groups: dict[str, list[tuple[int, SearchHit]]] = {}
    for rank, hit in enumerate(hits, start=1):
        key = ranking_group_key(hit, options.ranking_mode)
        groups.setdefault(key, []).append((rank, hit))

    ranked_groups: list[tuple[float, int, str, SearchHit]] = []
    for key, group in groups.items():
        best_rank, representative = min(group, key=lambda item: item[0])
        base_score = ranking_group_score(group, options.ranking_aggregation)
        ranking_score = base_score * ranking_profile_multiplier(representative, options.ranking_profile)
        ranked_groups.append(
            (
                ranking_score,
                best_rank,
                key,
                hit_with_ranking_info(
                    representative,
                    ranking_score=ranking_score,
                    source_rank=best_rank,
                    file_hit_count=len(group),
                    source_ranks=[rank for rank, _hit in group],
                    options=options,
                ),
            )
        )
    ranked_groups.sort(key=lambda item: (-item[0], item[1], item[2]))
    return [item[3] for item in ranked_groups]


def ranking_group_score(group: Sequence[tuple[int, SearchHit]], aggregation: str) -> float:
    scores = sorted((1.0 / (RRF_K + rank) for rank, _hit in group), reverse=True)
    if aggregation == "max":
        return scores[0]
    if aggregation == "capped_sum_3":
        return sum(scores[:3])
    raise ValueError(f"Unsupported ranking aggregation: {aggregation}")


def ranking_group_key(hit: SearchHit, mode: str) -> str:
    """Group repository chunks by file and, when requested, website chunks by page."""

    if hit.repo_path:
        return f"repo:{normalize_path(hit.repo_path)}"
    if hit.path and hit.url.startswith("https://github.com/"):
        return f"repo:{normalize_path(hit.path)}"
    if mode == "page" and hit.url:
        return f"page:{normalize_page_url(hit.url)}"
    return f"chunk:{hit.id or hit.url or hit.path or hit.title}"


def hit_with_ranking_info(
    hit: SearchHit,
    *,
    ranking_score: float,
    source_rank: int,
    file_hit_count: int,
    source_ranks: Sequence[int],
    options: RetrievalOptions,
) -> SearchHit:
    score_info = dict(hit.score_info)
    score_info["ranking"] = {
        "mode": options.ranking_mode,
        "profile": options.ranking_profile,
        "ranking_pool": options.ranking_pool,
        "aggregation": options.ranking_aggregation,
        "file_score": ranking_score,
        "group_score": ranking_score,
        "file_hit_count": file_hit_count,
        "group_hit_count": file_hit_count,
        "source_rank": source_rank,
        "source_ranks": list(source_ranks),
    }
    return SearchHit(
        id=hit.id,
        title=hit.title,
        url=hit.url,
        section_path=hit.section_path,
        content=hit.content,
        path=hit.path,
        repo_path=hit.repo_path,
        score_info=score_info,
        doc_kind=hit.doc_kind,
        chunk_index=hit.chunk_index,
    )


def ranking_profile_multiplier(hit: SearchHit, profile: str) -> float:
    if profile == "none" or not hit.repo_path:
        return 1.0
    path = normalize_path(hit.repo_path)
    lower_path = path.casefold()
    if lower_path.startswith((".pi/", ".10x/", ".loom/", ".claude/", ".cursor/")):
        return 0.20
    if lower_path.startswith("docs/") or lower_path.endswith(".md") or lower_path in {"readme.md", "changelog.md"}:
        return 0.70
    return 1.0


def normalize_path(value: str) -> str:
    return value.replace("\\", "/").strip("/")


def normalize_page_url(value: str) -> str:
    return value.split("#", 1)[0].rstrip("/").casefold()


def row_to_hit(row: object, *, score_info: Mapping[str, object] | None = None) -> SearchHit:
    attrs = row_attributes(row)
    base_score_info: dict[str, object] = {}
    for score_field in ("score", "dist", "distance", "rank", "$dist"):
        value = get_field(row, score_field)
        if value is not None:
            clean_name = "distance" if score_field in {"dist", "$dist"} else score_field.strip("$")
            base_score_info[clean_name] = value
    if score_info:
        base_score_info.update(dict(score_info))
    chunk_index = attrs.get("chunk_index")
    return SearchHit(
        id=str(get_field(row, "id") or attrs.get("id") or row_key(row)),
        title=str(attrs.get("title") or ""),
        url=str(attrs.get("url") or ""),
        section_path=str(attrs.get("section_path") or ""),
        content=str(attrs.get("content") or ""),
        path=str(attrs.get("path") or ""),
        repo_path=str(attrs.get("repo_path") or ""),
        doc_kind=str(attrs.get("doc_kind") or ""),
        chunk_index=chunk_index if isinstance(chunk_index, int) else None,
        score_info=base_score_info,
    )


def row_attributes(row: object) -> dict[str, object]:
    attrs = get_field(row, "attributes")
    if isinstance(attrs, Mapping):
        result = {str(key): value for key, value in attrs.items() if key != "vector"}
    else:
        result = {}
    if isinstance(row, Mapping):
        source_items = row.items()
    else:
        source_items = ((name, getattr(row, name)) for name in RETRIEVAL_ATTRIBUTES if hasattr(row, name))
    for key, value in source_items:
        key_str = str(key)
        if key_str in {"vector", "attributes"}:
            continue
        if key_str in RETRIEVAL_ATTRIBUTES or key_str in {"id"}:
            result.setdefault(key_str, value)
    return result


def row_key(row: object) -> str:
    row_id = get_field(row, "id")
    if row_id is not None:
        return str(row_id)
    attrs = row_attributes(row)
    attr_id = attrs.get("id")
    if attr_id is not None:
        return str(attr_id)
    for fields in (("url", "section_path", "content"), ("path", "chunk_index"), ("title", "content")):
        parts = [str(attrs.get(field) or "") for field in fields]
        if any(parts):
            return "|".join(parts)
    return ""


def get_field(item: object, name: str) -> object | None:
    if isinstance(item, Mapping):
        return item.get(name)
    return getattr(item, name, None)
