"""Lightweight retrieval smoke/eval harness for configured site namespaces."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Mapping, Sequence

from turbo_search.config import RuntimeConfig
from turbo_search.retriever import HybridRetriever, RetrievalOptions, SearchHit

DEFAULT_EVAL_DATASET = Path(__file__).with_name("data") / "retrieval_smoke_evals.json"


@dataclass(frozen=True)
class EvalCase:
    """One hand-authored retrieval smoke question and expected source hints."""

    id: str
    question: str
    expected_urls: tuple[str, ...]
    expected_topics: tuple[str, ...]

    @classmethod
    def from_mapping(cls, payload: Mapping[str, object]) -> "EvalCase":
        expected_urls = payload.get("expected_urls") or []
        expected_topics = payload.get("expected_topics") or []
        if not isinstance(payload.get("id"), str) or not isinstance(payload.get("question"), str):
            raise ValueError("Eval cases must include string id and question fields.")
        if not isinstance(expected_urls, list) or not all(isinstance(value, str) for value in expected_urls):
            raise ValueError(f"Eval case {payload.get('id')!r} has invalid expected_urls.")
        if not isinstance(expected_topics, list) or not all(isinstance(value, str) for value in expected_topics):
            raise ValueError(f"Eval case {payload.get('id')!r} has invalid expected_topics.")
        if not expected_urls and not expected_topics:
            raise ValueError(f"Eval case {payload['id']!r} must include at least one expected URL or topic hint.")
        return cls(
            id=payload["id"],
            question=payload["question"],
            expected_urls=tuple(expected_urls),
            expected_topics=tuple(expected_topics),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "question": self.question,
            "expected_urls": list(self.expected_urls),
            "expected_topics": list(self.expected_topics),
        }


@dataclass(frozen=True)
class EvalScore:
    """Scoring result for one eval case."""

    passed: bool
    matched_url: str | None = None
    matched_topic: str | None = None
    matched_rank: int | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "passed": self.passed,
            "matched_url": self.matched_url,
            "matched_topic": self.matched_topic,
            "matched_rank": self.matched_rank,
        }


@dataclass(frozen=True)
class EvalRunResult:
    """Structured report for a retrieval smoke/eval run."""

    cases: list[dict[str, object]]
    passed: int
    total: int
    dry_run: bool
    region: str
    namespace: str
    top_k: int
    candidates: int
    embedding_model: str

    def to_dict(self) -> dict[str, object]:
        pass_rate = self.passed / self.total if self.total and not self.dry_run else 0.0
        return {
            "command": "evals",
            "dry_run": self.dry_run,
            "credentials_required": not self.dry_run,
            "turbopuffer_api_calls": not self.dry_run,
            "api_calls_occurred": not self.dry_run,
            "region": self.region,
            "namespace": self.namespace,
            "embedding_model": self.embedding_model,
            "top_k": self.top_k,
            "candidates": self.candidates,
            "total": self.total,
            "passed": self.passed,
            "failed": 0 if self.dry_run else self.total - self.passed,
            "not_run": self.total if self.dry_run else 0,
            "pass_rate": pass_rate,
            "cases": self.cases,
        }


def load_eval_cases(dataset_path: Path | None = None) -> list[EvalCase]:
    """Load and validate retrieval smoke eval cases from JSON."""

    path = dataset_path or DEFAULT_EVAL_DATASET
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("Retrieval eval dataset must be a JSON list.")
    cases = [EvalCase.from_mapping(item) for item in payload if isinstance(item, Mapping)]
    if len(cases) != len(payload):
        raise ValueError("Every retrieval eval dataset entry must be an object.")
    if not cases:
        raise ValueError("Retrieval eval dataset must contain at least one case.")
    ids = [case.id for case in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("Retrieval eval case ids must be unique.")
    return cases


def score_hits(case: EvalCase, hits: Sequence[SearchHit | Mapping[str, object]]) -> EvalScore:
    """Pass when an expected URL or topic hint appears in top-k hits."""

    expected_urls = [value.casefold() for value in case.expected_urls if value]
    expected_topics = [value.casefold() for value in case.expected_topics if value]
    for rank, hit in enumerate(hits, start=1):
        url = hit_field(hit, "url").casefold()
        for expected_url in expected_urls:
            if expected_url in url:
                return EvalScore(passed=True, matched_url=expected_url, matched_rank=rank)

        searchable = " ".join(
            hit_field(hit, field)
            for field in ("title", "url", "section_path", "content", "path")
        ).casefold()
        for expected_topic in expected_topics:
            if expected_topic in searchable:
                return EvalScore(passed=True, matched_topic=expected_topic, matched_rank=rank)
    return EvalScore(passed=False)


def hit_field(hit: SearchHit | Mapping[str, object], field_name: str) -> str:
    if isinstance(hit, Mapping):
        return str(hit.get(field_name) or "")
    return str(getattr(hit, field_name) or "")


def hit_summary(hit: SearchHit | Mapping[str, object], rank: int) -> dict[str, object]:
    return {
        "rank": rank,
        "title": hit_field(hit, "title"),
        "url": hit_field(hit, "url"),
        "section_path": hit_field(hit, "section_path"),
    }


def build_dry_run_eval_report(
    cases: Sequence[EvalCase],
    *,
    config: RuntimeConfig,
    options: RetrievalOptions,
) -> EvalRunResult:
    """Return a no-credential listing of eval cases and expected hints."""

    listed_cases = [
        {
            **case.to_dict(),
            "status": "not_run",
            "top_hits": [],
            "score": EvalScore(passed=False).to_dict(),
        }
        for case in cases
    ]
    return EvalRunResult(
        cases=listed_cases,
        passed=0,
        total=len(cases),
        dry_run=True,
        region=config.region,
        namespace=config.namespace,
        top_k=options.top_k,
        candidates=options.candidates,
        embedding_model=config.embedding_model,
    )


def run_live_evals(
    cases: Sequence[EvalCase],
    *,
    config: RuntimeConfig,
    options: RetrievalOptions,
) -> EvalRunResult:
    """Run live retrieval for every eval case and score top-k source hints."""

    retriever = HybridRetriever.from_config(config)
    reports: list[dict[str, object]] = []
    passed = 0
    for case in cases:
        result = retriever.retrieve(case.question, options)
        score = score_hits(case, result.hits[: options.top_k])
        if score.passed:
            passed += 1
        reports.append(
            {
                **case.to_dict(),
                "status": "passed" if score.passed else "failed",
                "fusion": result.fusion,
                "top_hits": [hit_summary(hit, rank) for rank, hit in enumerate(result.hits[: options.top_k], start=1)],
                "score": score.to_dict(),
            }
        )
    return EvalRunResult(
        cases=reports,
        passed=passed,
        total=len(cases),
        dry_run=False,
        region=config.region,
        namespace=config.namespace,
        top_k=options.top_k,
        candidates=options.candidates,
        embedding_model=config.embedding_model,
    )
