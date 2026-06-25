from __future__ import annotations

import json
import tempfile
from pathlib import Path
import unittest

from turbo_search.evals import EvalCase, load_eval_cases, score_hits
from turbo_search.retriever import SearchHit


class EvalHarnessTests(unittest.TestCase):
    def test_loads_builtin_smoke_eval_dataset(self) -> None:
        cases = load_eval_cases()

        self.assertGreaterEqual(len(cases), 4)
        questions = {case.question for case in cases}
        self.assertIn("How should I choose between Scrapling fetchers?", questions)
        self.assertIn("How does Scrapling LinkExtractor filter links by allow and deny patterns?", questions)
        for case in cases:
            self.assertTrue(case.expected_urls or case.expected_topics)

    def test_loads_scrapling_smoke_eval_dataset(self) -> None:
        cases = load_eval_cases(Path("src/turbo_search/data/scrapling_retrieval_smoke_evals.json"))

        self.assertGreaterEqual(len(cases), 4)
        questions = {case.question for case in cases}
        self.assertIn("How does Scrapling LinkExtractor filter links by allow and deny patterns?", questions)
        self.assertTrue(any("scrapling.readthedocs.io" in url for case in cases for url in case.expected_urls))
        for case in cases:
            self.assertTrue(case.expected_urls or case.expected_topics)

    def test_score_hits_passes_on_expected_url_in_top_k(self) -> None:
        case = EvalCase(
            id="fetchers",
            question="How should I choose a fetcher?",
            expected_urls=("https://scrapling.readthedocs.io/en/latest/fetching/choosing.html",),
            expected_topics=("Fetchers basics",),
        )

        score = score_hits(
            case,
            [
                SearchHit(
                    id="1",
                    title="Fetchers basics",
                    url="https://scrapling.readthedocs.io/en/latest/fetching/choosing.html",
                    section_path="Fetchers basics",
                )
            ],
        )

        self.assertTrue(score.passed)
        self.assertEqual(score.matched_rank, 1)
        self.assertEqual(score.matched_url, "https://scrapling.readthedocs.io/en/latest/fetching/choosing.html")

    def test_score_hits_passes_on_expected_topic_in_title_or_content(self) -> None:
        case = EvalCase(
            id="link-extractor",
            question="How does LinkExtractor filter links?",
            expected_urls=(),
            expected_topics=("allow_domains",),
        )

        score = score_hits(
            case,
            [
                {
                    "title": "Generic templates",
                    "url": "https://scrapling.readthedocs.io/en/latest/spiders/generic-templates.html",
                    "content": "LinkExtractor supports allow, deny, and allow_domains filters.",
                }
            ],
        )

        self.assertTrue(score.passed)
        self.assertEqual(score.matched_rank, 1)
        self.assertEqual(score.matched_topic, "allow_domains")

    def test_load_eval_cases_rejects_missing_expected_hints(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dataset = Path(tmp) / "evals.json"
            dataset.write_text(json.dumps([{"id": "bad", "question": "Missing hints?"}]), encoding="utf-8")

            with self.assertRaises(ValueError):
                load_eval_cases(dataset)


if __name__ == "__main__":
    unittest.main()
