from __future__ import annotations

import unittest

from turbo_search.config import RuntimeConfig
from turbo_search.evals import hit_summary
from turbo_search.retriever import (
    RETRIEVAL_ATTRIBUTES,
    HybridRetriever,
    RetrievalOptions,
    bm25_rank_by,
    build_multi_query_subqueries,
)


class FakeEmbedder:
    def __init__(self) -> None:
        self.texts: list[list[str]] = []

    def encode(self, texts: list[str]) -> list[list[float]]:
        self.texts.append(texts)
        return [[0.1, 0.2, 0.3]]


class CapturingNamespace:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def multi_query(self, **kwargs: object) -> dict[str, object]:
        self.calls.append(kwargs)
        return {
            "rows": [
                {
                    "id": "chunk-1",
                    "score": 0.42,
                    "attributes": {
                        "title": "Fetchers basics",
                        "url": "https://scrapling.readthedocs.io/en/latest/fetching/choosing.html",
                        "section_path": "Fetcher choices",
                        "content": "Choose Fetcher, DynamicFetcher, or StealthyFetcher based on the target site.",
                        "path": "fetching/choosing.md",
                        "repo_path": "src/turbo_search/retriever.py",
                        "doc_kind": "docs",
                        "chunk_index": 3,
                        "vector": [9.0, 9.0],
                    },
                }
            ]
        }


class RerankUnsupportedNamespace:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def multi_query(self, **kwargs: object) -> dict[str, object]:
        self.calls.append(kwargs)
        if "rerank_by" in kwargs:
            raise TypeError("multi_query() got an unexpected keyword argument 'rerank_by'")
        return {
            "results": [
                {
                    "rows": [
                        {"id": "ann-only", "attributes": {"title": "ANN", "content": "semantic match"}},
                        {"id": "both", "attributes": {"title": "Both", "content": "hybrid match"}},
                    ]
                },
                {
                    "rows": [
                        {"id": "both", "attributes": {"title": "Both", "content": "hybrid match"}},
                        {"id": "bm25-only", "attributes": {"title": "BM25", "content": "lexical match"}},
                    ]
                },
            ]
        }


class DuplicateRepoPathNamespace:
    def multi_query(self, **kwargs: object) -> dict[str, object]:
        return {
            "rows": [
                {"id": "docs-1", "attributes": {"title": "Docs", "repo_path": "docs/guide.md", "path": "docs/guide.md"}},
                {"id": "src-1", "attributes": {"title": "Code A", "repo_path": "src/module.py", "path": "src/module.py"}},
                {"id": "src-2", "attributes": {"title": "Code B", "repo_path": "src/module.py", "path": "src/module.py"}},
                {"id": "skill-1", "attributes": {"title": "Skill", "repo_path": ".pi/skills/tool/SKILL.md", "path": ".pi/skills/tool/SKILL.md"}},
                {"id": "test-1", "attributes": {"title": "Tests", "repo_path": "tests/test_module.py", "path": "tests/test_module.py"}},
            ]
        }


class MissingRepoPathSchemaNamespace:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def multi_query(self, **kwargs: object) -> dict[str, object]:
        self.calls.append(kwargs)
        include_attributes = kwargs["queries"][0]["include_attributes"]
        if "repo_path" in include_attributes:
            raise RuntimeError('attribute "repo_path" not found in schema')
        return {"rows": [{"id": "page-1", "attributes": {"title": "Page", "url": "https://example.com/docs", "content": "Docs"}}]}


class DuplicateUrlNamespace:
    def multi_query(self, **kwargs: object) -> dict[str, object]:
        return {
            "rows": [
                {"id": "docs-a", "attributes": {"title": "Docs A", "url": "https://example.com/docs#intro", "content": "first docs chunk"}},
                {"id": "docs-b", "attributes": {"title": "Docs B", "url": "https://example.com/docs", "content": "second docs chunk"}},
                {"id": "api-a", "attributes": {"title": "API", "url": "https://example.com/api", "content": "api chunk"}},
            ]
        }


class PageAggregationNamespace:
    def multi_query(self, **kwargs: object) -> dict[str, object]:
        return {
            "rows": [
                {"id": "api-a", "attributes": {"title": "API", "url": "https://example.com/api", "content": "api chunk"}},
                {"id": "docs-a", "attributes": {"title": "Docs A", "url": "https://example.com/docs#one", "content": "first docs chunk"}},
                {"id": "docs-b", "attributes": {"title": "Docs B", "url": "https://example.com/docs#two", "content": "second docs chunk"}},
                {"id": "docs-c", "attributes": {"title": "Docs C", "url": "https://example.com/docs#three", "content": "third docs chunk"}},
            ]
        }


class RetrieverTests(unittest.TestCase):
    def test_builds_ann_and_boosted_bm25_subqueries_without_vectors_in_attributes(self) -> None:
        queries = build_multi_query_subqueries(
            query="link extraction",
            query_vector=[0.1, 0.2],
            candidates=25,
            doc_kind="docs",
        )

        self.assertEqual(len(queries), 2)
        self.assertEqual(queries[0]["rank_by"], ("vector", "ANN", [0.1, 0.2]))
        self.assertEqual(queries[1]["rank_by"], bm25_rank_by("link extraction"))
        self.assertEqual(
            bm25_rank_by("link extraction"),
            (
                "Sum",
                [
                    ("Product", 2.0, ("title", "BM25", "link extraction")),
                    ("Product", 1.5, ("section_path", "BM25", "link extraction")),
                    ("content", "BM25", "link extraction"),
                ],
            ),
        )
        for query in queries:
            self.assertEqual(query["limit"], 25)
            self.assertEqual(query["filters"], ("doc_kind", "Eq", "docs"))
            self.assertEqual(query["include_attributes"], RETRIEVAL_ATTRIBUTES)
            self.assertNotIn("vector", query["include_attributes"])

    def test_live_retriever_uses_single_multi_query_with_server_rrf(self) -> None:
        namespace = CapturingNamespace()
        embedder = FakeEmbedder()
        retriever = HybridRetriever(
            namespace=namespace,
            embedder=embedder,
            config=RuntimeConfig(),
        )

        result = retriever.retrieve(
            "How should I choose a Scrapling fetcher?",
            RetrievalOptions(top_k=5, candidates=10),
        )

        self.assertEqual(embedder.texts, [["How should I choose a Scrapling fetcher?"]])
        self.assertEqual(len(namespace.calls), 1)
        self.assertEqual(namespace.calls[0]["rerank_by"], ("RRF",))
        self.assertEqual(len(namespace.calls[0]["queries"]), 2)
        self.assertEqual(result.fusion, "server_rrf")
        self.assertEqual(result.hits[0].title, "Fetchers basics")
        payload = result.to_dict()
        self.assertNotIn("vector", str(payload))
        self.assertEqual(payload["hits"][0]["url"], "https://scrapling.readthedocs.io/en/latest/fetching/choosing.html")
        self.assertEqual(payload["hits"][0]["section_path"], "Fetcher choices")
        self.assertEqual(payload["hits"][0]["repo_path"], "src/turbo_search/retriever.py")
        self.assertEqual(result.hits[0].repo_path, "src/turbo_search/retriever.py")
        self.assertEqual(hit_summary(result.hits[0], 1)["repo_path"], "src/turbo_search/retriever.py")
        self.assertIn("score_info", payload["hits"][0])

    def test_client_side_rrf_fallback_when_server_rerank_unsupported(self) -> None:
        namespace = RerankUnsupportedNamespace()
        retriever = HybridRetriever(
            namespace=namespace,
            embedder=FakeEmbedder(),
            config=RuntimeConfig(),
        )

        result = retriever.retrieve("hybrid search", RetrievalOptions(top_k=3, candidates=10))

        self.assertEqual(len(namespace.calls), 2)
        self.assertIn("rerank_by", namespace.calls[0])
        self.assertNotIn("rerank_by", namespace.calls[1])
        self.assertEqual(result.fusion, "client_rrf")
        self.assertEqual(result.hits[0].id, "both")
        self.assertEqual(result.hits[0].score_info["fusion"], "client_rrf")
        self.assertIn("ann", result.hits[0].score_info["source_ranks"])
        self.assertIn("bm25", result.hits[0].score_info["source_ranks"])

    def test_default_file_ranking_deduplicates_repo_paths_and_demotes_process_docs(self) -> None:
        retriever = HybridRetriever(
            namespace=DuplicateRepoPathNamespace(),
            embedder=FakeEmbedder(),
            config=RuntimeConfig(),
        )

        result = retriever.retrieve("repo code", RetrievalOptions(top_k=3, candidates=10, ranking_pool=10))

        self.assertEqual([hit.repo_path for hit in result.hits], ["src/module.py", "tests/test_module.py", "docs/guide.md"])
        self.assertEqual(len({hit.repo_path for hit in result.hits}), 3)
        self.assertEqual(result.ranking_mode, "file")
        self.assertEqual(result.ranking_profile, "repo_code")
        self.assertEqual(result.hits[0].score_info["ranking"]["file_hit_count"], 2)

    def test_chunk_ranking_preserves_raw_fused_order(self) -> None:
        retriever = HybridRetriever(
            namespace=DuplicateRepoPathNamespace(),
            embedder=FakeEmbedder(),
            config=RuntimeConfig(),
        )

        result = retriever.retrieve(
            "repo code",
            RetrievalOptions(top_k=3, candidates=10, ranking_mode="chunk", ranking_profile="none"),
        )

        self.assertEqual([hit.id for hit in result.hits], ["docs-1", "src-1", "src-2"])
        self.assertEqual(result.ranking_mode, "chunk")

    def test_page_ranking_deduplicates_website_urls_only_when_requested(self) -> None:
        retriever = HybridRetriever(
            namespace=DuplicateUrlNamespace(),
            embedder=FakeEmbedder(),
            config=RuntimeConfig(),
        )

        default_result = retriever.retrieve("website docs", RetrievalOptions(top_k=3, candidates=10, ranking_pool=10))
        page_result = retriever.retrieve(
            "website docs",
            RetrievalOptions(top_k=3, candidates=10, ranking_mode="page", ranking_profile="none", ranking_pool=10),
        )

        self.assertEqual([hit.id for hit in default_result.hits], ["docs-a", "docs-b", "api-a"])
        self.assertEqual([hit.id for hit in page_result.hits], ["docs-a", "api-a"])
        self.assertEqual(page_result.ranking_mode, "page")

    def test_page_ranking_still_groups_repo_rows_by_repo_path(self) -> None:
        retriever = HybridRetriever(
            namespace=DuplicateRepoPathNamespace(),
            embedder=FakeEmbedder(),
            config=RuntimeConfig(),
        )

        result = retriever.retrieve(
            "repo code",
            RetrievalOptions(top_k=3, candidates=10, ranking_mode="page", ranking_profile="none", ranking_pool=10),
        )

        self.assertEqual([hit.repo_path for hit in result.hits], ["docs/guide.md", "src/module.py", ".pi/skills/tool/SKILL.md"])
        self.assertEqual(len({hit.repo_path for hit in result.hits}), 3)

    def test_page_ranking_capped_sum_3_rewards_multi_chunk_page_evidence(self) -> None:
        retriever = HybridRetriever(
            namespace=PageAggregationNamespace(),
            embedder=FakeEmbedder(),
            config=RuntimeConfig(),
        )

        default_result = retriever.retrieve(
            "website docs",
            RetrievalOptions(top_k=2, candidates=10, ranking_mode="page", ranking_profile="none", ranking_pool=4),
        )
        aggregated_result = retriever.retrieve(
            "website docs",
            RetrievalOptions(
                top_k=2,
                candidates=10,
                ranking_mode="page",
                ranking_profile="none",
                ranking_pool=4,
                ranking_aggregation="capped_sum_3",
            ),
        )

        self.assertEqual([hit.id for hit in default_result.hits], ["api-a", "docs-a"])
        self.assertEqual([hit.id for hit in aggregated_result.hits], ["docs-a", "api-a"])
        ranking_info = aggregated_result.hits[0].score_info["ranking"]
        self.assertEqual(ranking_info["aggregation"], "capped_sum_3")
        self.assertEqual(ranking_info["group_hit_count"], 3)
        self.assertEqual(ranking_info["source_ranks"], [2, 3, 4])

    def test_invalid_ranking_aggregation_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "ranking_aggregation"):
            RetrievalOptions(ranking_aggregation="sum")

    def test_capped_sum_3_preserves_repo_path_grouping(self) -> None:
        retriever = HybridRetriever(
            namespace=DuplicateRepoPathNamespace(),
            embedder=FakeEmbedder(),
            config=RuntimeConfig(),
        )

        result = retriever.retrieve(
            "repo code",
            RetrievalOptions(
                top_k=3,
                candidates=10,
                ranking_mode="page",
                ranking_profile="none",
                ranking_pool=10,
                ranking_aggregation="capped_sum_3",
            ),
        )

        self.assertEqual(result.hits[0].repo_path, "src/module.py")
        self.assertEqual(len({hit.repo_path for hit in result.hits}), 3)

    def test_live_retriever_retries_without_repo_path_for_website_schema(self) -> None:
        namespace = MissingRepoPathSchemaNamespace()
        retriever = HybridRetriever(
            namespace=namespace,
            embedder=FakeEmbedder(),
            config=RuntimeConfig(),
        )

        result = retriever.retrieve("website docs", RetrievalOptions(top_k=1, candidates=10))

        self.assertEqual(result.hits[0].url, "https://example.com/docs")
        self.assertEqual(len(namespace.calls), 2)
        self.assertIn("repo_path", namespace.calls[0]["queries"][0]["include_attributes"])
        self.assertNotIn("repo_path", namespace.calls[1]["queries"][0]["include_attributes"])


if __name__ == "__main__":
    unittest.main()
