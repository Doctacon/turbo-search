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


if __name__ == "__main__":
    unittest.main()
