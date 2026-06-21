"""Command-line interface for the Jellyfish docs RAG prototype."""

from __future__ import annotations

import argparse
from dataclasses import replace
import json
from pathlib import Path
import sys
from typing import Sequence

from turbo_search import __version__
from turbo_search.applied_state import AppliedStateError, load_applied_state
from turbo_search.apply import ApplyPlanError, apply_preflight_summary, load_verified_apply_plan, run_approved_apply
from turbo_search.config import load_config
from turbo_search.crawler import (
    DEFAULT_CRAWL_CONCURRENT_REQUESTS,
    DEFAULT_CRAWL_CONCURRENT_REQUESTS_PER_DOMAIN,
    DEFAULT_CRAWL_DOWNLOAD_DELAY,
    DEFAULT_CRAWL_MAX_CHUNKS,
    DEFAULT_CRAWL_MAX_PAGES,
    CrawlOptions,
    crawl_site,
    default_out_dir,
    validate_base_url,
)
from turbo_search.evals import (
    build_dry_run_eval_report,
    load_eval_cases,
    run_live_evals,
)
from turbo_search.indexer import (
    DEFAULT_OVERLAP_SENTENCES,
    DEFAULT_TARGET_TOKENS,
    IndexingPlan,
    process_corpus,
    write_chunks,
)
from turbo_search.plan_artifacts import (
    DEFAULT_PLAN_EMBEDDING_MODEL,
    PlanArtifacts,
    build_plan_artifacts,
    write_plan_artifacts,
)
from turbo_search.plan_diff import IncrementalPlanDiff, PlanDiffError, diff_manifest_against_state
from turbo_search.retriever import (
    DEFAULT_CANDIDATES,
    DEFAULT_TOP_K,
    HybridRetriever,
    RetrievalOptions,
    RetrievalPlan,
    RetrievalResult,
    retrieval_plan,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="turbo-search",
        description="Local site RAG utilities. Crawl/index commands are dry-run by default unless explicitly documented otherwise.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command")

    index_parser = subparsers.add_parser(
        "index",
        help="parse and chunk Markdown docs; write only when --write is passed",
        description=(
            "Parse and chunk a Markdown corpus. Default mode is a safe dry-run: "
            "no credentials, embeddings, or turbopuffer API calls are used."
        ),
    )
    index_parser.add_argument(
        "--corpus-dir",
        default="jellyfish-site-docs",
        help="Markdown corpus directory to index.",
    )
    index_parser.add_argument(
        "--max-files",
        type=positive_int,
        default=None,
        help="Process at most this many Markdown files.",
    )
    index_parser.add_argument(
        "--limit-chunks",
        type=positive_int,
        default=None,
        help="Stop after generating this many chunks.",
    )
    index_parser.add_argument(
        "--batch-size",
        type=positive_int,
        default=64,
        help="Turbopuffer upsert batch size for --write mode.",
    )
    index_parser.add_argument(
        "--target-tokens",
        type=positive_int,
        default=DEFAULT_TARGET_TOKENS,
        help="Approximate target tokens per chunk.",
    )
    index_parser.add_argument(
        "--overlap-sentences",
        type=nonnegative_int,
        default=DEFAULT_OVERLAP_SENTENCES,
        help="Number of trailing sentences to overlap between adjacent chunks in a section.",
    )
    index_parser.add_argument(
        "--write",
        action="store_true",
        help="Explicitly embed chunks and write batched upserts to turbopuffer.",
    )
    index_parser.set_defaults(func=_run_index)

    crawl_parser = subparsers.add_parser(
        "crawl",
        help="crawl a website with Scrapling and chunk locally; always dry-run",
        description=(
            "Crawl a public website with Scrapling, generate a local Markdown corpus, "
            "and chunk it for namespace planning. This command is local-only: it does not "
            "read credentials, embed text, create namespaces, or call turbopuffer."
        ),
    )
    crawl_parser.add_argument(
        "--base-url",
        required=True,
        help="Absolute http(s) URL to crawl.",
    )
    crawl_parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Local output directory. Defaults to artifacts/site-crawls/<host>.",
    )
    crawl_parser.add_argument(
        "--max-pages",
        type=positive_int,
        default=DEFAULT_CRAWL_MAX_PAGES,
        help="Maximum pages to scrape.",
    )
    crawl_parser.add_argument(
        "--max-chunks",
        type=positive_int,
        default=DEFAULT_CRAWL_MAX_CHUNKS,
        help="Maximum chunks to generate from crawled pages.",
    )
    crawl_parser.add_argument(
        "--concurrent-requests",
        type=positive_int,
        default=DEFAULT_CRAWL_CONCURRENT_REQUESTS,
        help="Global Scrapling crawl concurrency.",
    )
    crawl_parser.add_argument(
        "--concurrent-requests-per-domain",
        type=positive_int,
        default=DEFAULT_CRAWL_CONCURRENT_REQUESTS_PER_DOMAIN,
        help="Per-domain Scrapling crawl concurrency.",
    )
    crawl_parser.add_argument(
        "--download-delay",
        type=nonnegative_float,
        default=DEFAULT_CRAWL_DOWNLOAD_DELAY,
        help="Polite delay between crawl requests in seconds.",
    )
    crawl_parser.add_argument(
        "--css-selector",
        default=None,
        help=(
            "Optional CSS selector passed to Scrapling extraction to scope content, "
            "e.g. article or .md-content__inner."
        ),
    )
    crawl_parser.add_argument(
        "--target-tokens",
        type=positive_int,
        default=DEFAULT_TARGET_TOKENS,
        help="Approximate target tokens per generated chunk.",
    )
    crawl_parser.add_argument(
        "--overlap-sentences",
        type=nonnegative_int,
        default=DEFAULT_OVERLAP_SENTENCES,
        help="Number of trailing sentences to overlap between adjacent chunks.",
    )
    crawl_parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON output. Text summary is used by default.",
    )
    crawl_parser.set_defaults(func=_run_crawl)

    plan_parser = subparsers.add_parser(
        "plan",
        help="crawl a website and write local review/apply plan artifacts; no live writes",
        description=(
            "Crawl a public website with Scrapling, generate a local Markdown corpus, "
            "chunk it, compare it to local applied state, and write reviewable plan artifacts. "
            "This command is local-only: it does not read credentials, embed text, create namespaces, "
            "or call turbopuffer."
        ),
    )
    plan_parser.add_argument(
        "--base-url",
        required=True,
        help="Absolute http(s) URL to crawl and plan.",
    )
    plan_parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Local output directory. Defaults to artifacts/site-crawls/<host>-plan.",
    )
    plan_parser.add_argument(
        "--namespace",
        default=None,
        help="Stable target namespace for diffing state. Defaults to the deterministic site namespace candidate.",
    )
    plan_parser.add_argument(
        "--state-root",
        type=Path,
        default=Path(".turbo-search"),
        help="Local applied-state root. Defaults to .turbo-search.",
    )
    plan_parser.add_argument(
        "--max-pages",
        type=positive_int,
        default=DEFAULT_CRAWL_MAX_PAGES,
        help="Maximum pages to scrape.",
    )
    plan_parser.add_argument(
        "--max-chunks",
        type=positive_int,
        default=DEFAULT_CRAWL_MAX_CHUNKS,
        help="Maximum chunks to generate from crawled pages.",
    )
    plan_parser.add_argument(
        "--concurrent-requests",
        type=positive_int,
        default=DEFAULT_CRAWL_CONCURRENT_REQUESTS,
        help="Global Scrapling crawl concurrency.",
    )
    plan_parser.add_argument(
        "--concurrent-requests-per-domain",
        type=positive_int,
        default=DEFAULT_CRAWL_CONCURRENT_REQUESTS_PER_DOMAIN,
        help="Per-domain Scrapling crawl concurrency.",
    )
    plan_parser.add_argument(
        "--download-delay",
        type=nonnegative_float,
        default=DEFAULT_CRAWL_DOWNLOAD_DELAY,
        help="Polite delay between crawl requests in seconds.",
    )
    plan_parser.add_argument(
        "--css-selector",
        default=None,
        help=(
            "Optional CSS selector passed to Scrapling extraction to scope content, "
            "e.g. article or .md-content__inner."
        ),
    )
    plan_parser.add_argument(
        "--target-tokens",
        type=positive_int,
        default=DEFAULT_TARGET_TOKENS,
        help="Approximate target tokens per generated chunk.",
    )
    plan_parser.add_argument(
        "--overlap-sentences",
        type=nonnegative_int,
        default=DEFAULT_OVERLAP_SENTENCES,
        help="Number of trailing sentences to overlap between adjacent chunks.",
    )
    plan_parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON output. Text summary is used by default.",
    )
    plan_parser.set_defaults(func=_run_plan)

    apply_parser = subparsers.add_parser(
        "apply",
        help="verify and optionally apply a saved generic site RAG plan",
        description=(
            "Verify a saved plan artifact and recompute its local state diff. Default mode is "
            "a safe preflight: no credentials, embeddings, or turbopuffer API calls are used. "
            "Pass --approve to embed and upsert only new/changed rows."
        ),
    )
    apply_parser.add_argument(
        "--plan",
        type=Path,
        required=True,
        help="Path to a saved plan.json artifact.",
    )
    apply_parser.add_argument(
        "--namespace",
        required=True,
        help="Expected stable target namespace. Must match the plan and manifest.",
    )
    apply_parser.add_argument(
        "--state-root",
        type=Path,
        default=Path(".turbo-search"),
        help="Local applied-state root. Defaults to .turbo-search.",
    )
    apply_parser.add_argument(
        "--batch-size",
        type=positive_int,
        default=64,
        help="Turbopuffer upsert batch size for approved apply mode.",
    )
    apply_parser.add_argument(
        "--approve",
        action="store_true",
        help="Explicitly embed and upsert rows selected by the recomputed diff.",
    )
    apply_parser.add_argument(
        "--delete-stale",
        action="store_true",
        help="With --approve, delete exact stale row IDs from the recomputed diff instead of retaining them.",
    )
    apply_parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON output. Text summary is used by default.",
    )
    apply_parser.set_defaults(func=_run_apply)

    retrieve_parser = subparsers.add_parser(
        "retrieve",
        help="retrieve relevant chunks; dry-run plan by default unless --live is passed",
        description=(
            "Plan or execute hybrid retrieval against the configured turbopuffer namespace. "
            "Default mode is safe: it prints the multi-query plan without loading embeddings, "
            "reading credentials, or contacting turbopuffer. Pass --live to embed the query "
            "and query turbopuffer."
        ),
    )
    retrieve_parser.add_argument(
        "query",
        help="Question to retrieve relevant Jellyfish docs chunks for.",
    )
    retrieve_parser.add_argument(
        "--live",
        action="store_true",
        help="Execute live retrieval. Reads TURBOPUFFER_API_KEY from the environment and calls turbopuffer.",
    )
    retrieve_parser.add_argument(
        "--dry-run",
        "--plan",
        dest="dry_run",
        action="store_true",
        help="Print the retrieval plan without credentials, embeddings, or turbopuffer API calls (default).",
    )
    retrieve_parser.add_argument(
        "--top-k",
        type=positive_int,
        default=DEFAULT_TOP_K,
        help="Number of fused chunks to return.",
    )
    retrieve_parser.add_argument(
        "--candidates",
        type=positive_int,
        default=DEFAULT_CANDIDATES,
        help="Candidate limit for each ANN/BM25 subquery before RRF fusion.",
    )
    retrieve_parser.add_argument(
        "--doc-kind",
        default=None,
        help="Optional doc_kind filter, e.g. blog, library, platform, integrations.",
    )
    add_runtime_config_arguments(retrieve_parser)
    retrieve_parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON output. Text output is used by default for live results.",
    )
    retrieve_parser.set_defaults(func=_run_retrieve)

    evals_parser = subparsers.add_parser(
        "evals",
        help="list or run Jellyfish retrieval smoke evals",
        description=(
            "List or execute hand-authored retrieval smoke evals for the configured namespace. "
            "Default mode is safe: it lists eval questions and expected source hints without "
            "credentials, embeddings, or turbopuffer calls. Pass --live to run retrieval "
            "against turbopuffer."
        ),
    )
    evals_parser.add_argument(
        "--live",
        action="store_true",
        help="Execute live evals. Reads TURBOPUFFER_API_KEY from the environment and calls turbopuffer.",
    )
    evals_parser.add_argument(
        "--dry-run",
        "--list",
        dest="dry_run",
        action="store_true",
        help="List eval questions and expected hints without credentials or turbopuffer API calls (default).",
    )
    evals_parser.add_argument(
        "--top-k",
        type=positive_int,
        default=DEFAULT_TOP_K,
        help="Number of fused chunks to score for each eval question.",
    )
    evals_parser.add_argument(
        "--candidates",
        type=positive_int,
        default=DEFAULT_CANDIDATES,
        help="Candidate limit for each ANN/BM25 subquery before RRF fusion.",
    )
    evals_parser.add_argument(
        "--dataset",
        type=Path,
        default=None,
        help="Optional path to a JSON eval dataset. Defaults to the built-in Jellyfish smoke set.",
    )
    add_runtime_config_arguments(evals_parser)
    evals_parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON output. Text output is used by default.",
    )
    evals_parser.set_defaults(func=_run_evals)

    return parser


def add_runtime_config_arguments(command_parser: argparse.ArgumentParser) -> None:
    """Add non-secret turbopuffer runtime overrides to a command."""

    command_parser.add_argument(
        "--region",
        default=None,
        help="Override TURBOPUFFER_REGION for this command without changing the environment.",
    )
    command_parser.add_argument(
        "--namespace",
        default=None,
        help="Override TURBOPUFFER_NAMESPACE for this command without changing the environment.",
    )
    command_parser.add_argument(
        "--embedding-model",
        default=None,
        help="Override TURBO_SEARCH_EMBEDDING_MODEL for this command.",
    )


def config_from_args(args: argparse.Namespace):
    """Load non-secret runtime config, applying CLI overrides when supplied."""

    config = load_config()
    return replace(
        config,
        region=args.region or config.region,
        namespace=args.namespace or config.namespace,
        embedding_model=args.embedding_model or config.embedding_model,
    )


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed


def nonnegative_int(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be zero or greater")
    return parsed


def nonnegative_float(value: str) -> float:
    parsed = float(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be zero or greater")
    return parsed


def _print_json(payload: dict[str, object]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def _run_index(args: argparse.Namespace) -> int:
    config = load_config()
    corpus_dir = Path(args.corpus_dir)
    try:
        plan = process_corpus(
            corpus_dir,
            max_files=args.max_files,
            limit_chunks=args.limit_chunks,
            target_tokens=args.target_tokens,
            overlap_sentences=args.overlap_sentences,
        )
    except FileNotFoundError as exc:
        print(f"Corpus directory not found: {exc}", file=sys.stderr)
        return 2
    except NotADirectoryError as exc:
        print(f"Corpus path is not a directory: {exc}", file=sys.stderr)
        return 2

    dry_run = not args.write
    rows_written = 0
    api_calls_occurred = False
    if args.write:
        try:
            rows_written = write_chunks(plan.chunks, config=config, batch_size=args.batch_size)
            plan.stats.rows_written = rows_written
            api_calls_occurred = rows_written > 0
        except RuntimeError as exc:
            print(str(exc), file=sys.stderr)
            return 2

    _print_json(index_summary(plan, args=args, config=config, dry_run=dry_run, api_calls_occurred=api_calls_occurred))
    return 0


def index_summary(
    plan: IndexingPlan,
    *,
    args: argparse.Namespace,
    config: object,
    dry_run: bool,
    api_calls_occurred: bool,
) -> dict[str, object]:
    return {
        "command": "index",
        "dry_run": dry_run,
        "credentials_required": not dry_run,
        "turbopuffer_api_calls": api_calls_occurred,
        "api_calls_occurred": api_calls_occurred,
        "corpus_dir": str(plan.corpus_dir),
        "corpus_dir_exists": plan.corpus_dir.exists(),
        "files_discovered": plan.files_discovered,
        "files_seen": plan.stats.files_seen,
        "files_skipped_empty": plan.stats.files_skipped_empty,
        "files_error": plan.stats.files_error,
        "chunks_generated": plan.stats.chunks_generated,
        "rows_written": plan.stats.rows_written,
        "limit_reached": plan.limit_reached,
        "max_files": args.max_files,
        "limit_chunks": args.limit_chunks,
        "batch_size": args.batch_size,
        "target_tokens": args.target_tokens,
        "overlap_sentences": args.overlap_sentences,
        "region": config.region,
        "namespace": config.namespace,
        "embedding_model": config.embedding_model,
        "errors": [error.__dict__ for error in plan.stats.errors[:10]],
    }


def _run_crawl(args: argparse.Namespace) -> int:
    try:
        base_url = validate_base_url(args.base_url)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    out_dir = args.out_dir if args.out_dir is not None else default_out_dir(base_url)
    options = CrawlOptions(
        base_url=base_url,
        out_dir=out_dir,
        max_pages=args.max_pages,
        max_chunks=args.max_chunks,
        concurrent_requests=args.concurrent_requests,
        concurrent_requests_per_domain=args.concurrent_requests_per_domain,
        download_delay=args.download_delay,
        css_selector=args.css_selector,
        target_tokens=args.target_tokens,
        overlap_sentences=args.overlap_sentences,
    )
    try:
        summary = crawl_site(options)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.json:
        _print_json(summary)
    else:
        print_crawl_text(summary)
    return 0


def _run_plan(args: argparse.Namespace) -> int:
    try:
        base_url = validate_base_url(args.base_url)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    out_dir = args.out_dir if args.out_dir is not None else default_out_dir(base_url).with_name(
        f"{default_out_dir(base_url).name}-plan"
    )
    options = CrawlOptions(
        base_url=base_url,
        out_dir=out_dir,
        max_pages=args.max_pages,
        max_chunks=args.max_chunks,
        concurrent_requests=args.concurrent_requests,
        concurrent_requests_per_domain=args.concurrent_requests_per_domain,
        download_delay=args.download_delay,
        css_selector=args.css_selector,
        target_tokens=args.target_tokens,
        overlap_sentences=args.overlap_sentences,
    )
    try:
        crawl_summary = crawl_site(options)
        pages_dir = out_dir / "pages"
        indexing_plan = process_corpus(
            pages_dir,
            limit_chunks=args.max_chunks,
            target_tokens=args.target_tokens,
            overlap_sentences=args.overlap_sentences,
        )
        namespace = args.namespace or str(crawl_summary["namespace_candidate"])
        initial_artifacts = build_plan_artifacts(
            indexing_plan=indexing_plan,
            base_url=base_url,
            out_dir=out_dir,
            namespace=namespace,
            crawl_options=plan_crawl_options(args),
            chunk_options=plan_chunk_options(args),
            embedding_model=DEFAULT_PLAN_EMBEDDING_MODEL,
            state_root=args.state_root,
        )
        state = load_applied_state(
            site_id=initial_artifacts.manifest.site_id,
            namespace=initial_artifacts.manifest.namespace,
            base_url=base_url,
            state_root=args.state_root,
        )
        diff = diff_manifest_against_state(initial_artifacts.manifest, state)
        artifacts = build_plan_artifacts(
            indexing_plan=indexing_plan,
            base_url=base_url,
            out_dir=out_dir,
            namespace=namespace,
            crawl_options=plan_crawl_options(args),
            chunk_options=plan_chunk_options(args),
            embedding_model=DEFAULT_PLAN_EMBEDDING_MODEL,
            diff=diff.to_dict(),
            state_root=args.state_root,
        )
        write_plan_artifacts(artifacts, out_dir)
    except (RuntimeError, OSError, ValueError, AppliedStateError, PlanDiffError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    summary = plan_summary(
        crawl_summary=crawl_summary,
        artifacts=artifacts,
        diff=diff,
        state_first_apply=state.first_apply,
    )
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    if args.json:
        _print_json(summary)
    else:
        print_plan_text(summary)
    return 0


def plan_crawl_options(args: argparse.Namespace) -> dict[str, object]:
    return {
        "max_pages": args.max_pages,
        "max_chunks": args.max_chunks,
        "concurrent_requests": args.concurrent_requests,
        "concurrent_requests_per_domain": args.concurrent_requests_per_domain,
        "download_delay": args.download_delay,
        "css_selector": args.css_selector,
    }


def plan_chunk_options(args: argparse.Namespace) -> dict[str, object]:
    return {
        "target_tokens": args.target_tokens,
        "overlap_sentences": args.overlap_sentences,
    }


def plan_summary(
    *,
    crawl_summary: dict[str, object],
    artifacts: PlanArtifacts,
    diff: IncrementalPlanDiff,
    state_first_apply: bool,
) -> dict[str, object]:
    plan_dict = artifacts.plan_dict()
    diff_summary = diff.summary_dict()
    summary = dict(crawl_summary)
    summary.update(
        {
            "command": "plan",
            "dry_run": True,
            "credentials_required": False,
            "turbopuffer_api_calls": False,
            "api_calls_occurred": False,
            "namespace": plan_dict["namespace"],
            "namespace_candidate": plan_dict["namespace_candidate"],
            "site_id": plan_dict["site_id"],
            "plan_id": plan_dict["plan_id"],
            "plan_path": str(Path(str(plan_dict["manifest_path"])).with_name("plan.json")),
            "manifest_path": plan_dict["manifest_path"],
            "chunks_path": plan_dict["chunks_path"],
            "pages_dir": plan_dict["pages_dir"],
            "state_backend": plan_dict["state_backend"],
            "state_path": plan_dict["state_path"],
            "state_first_apply": state_first_apply,
            "embedding_model": plan_dict["embedding_model"],
            "artifact_hash": plan_dict["artifact_hash"],
            "diff": diff_summary,
            **diff_summary,
        }
    )
    return summary


def _run_apply(args: argparse.Namespace) -> int:
    try:
        verified = load_verified_apply_plan(
            plan_path=args.plan,
            namespace=args.namespace,
            state_root=args.state_root,
        )
    except (ApplyPlanError, AppliedStateError, PlanDiffError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if not args.approve:
        summary = apply_preflight_summary(
            verified,
            namespace=args.namespace,
            approved=False,
            delete_stale=args.delete_stale,
        )
        if args.json:
            _print_json(summary)
        else:
            print_apply_text(summary)
        return 0

    config = replace(load_config(), namespace=args.namespace, embedding_model=str(verified.plan["embedding_model"]))
    try:
        summary = run_approved_apply(
            verified,
            config=config,
            namespace=args.namespace,
            batch_size=args.batch_size,
            delete_stale=args.delete_stale,
        )
    except (RuntimeError, AppliedStateError, OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.json:
        _print_json(summary)
    else:
        print_apply_text(summary)
    return 0


def _run_retrieve(args: argparse.Namespace) -> int:
    config = config_from_args(args)
    options = RetrievalOptions(top_k=args.top_k, candidates=args.candidates, doc_kind=args.doc_kind)
    if args.dry_run and args.live:
        print("Choose either --live or --dry-run/--plan, not both.", file=sys.stderr)
        return 2
    if not args.live:
        plan = retrieval_plan(args.query, config=config, options=options)
        if args.json:
            _print_json(plan.to_dict())
        else:
            print_retrieval_text(plan)
        return 0

    try:
        result = HybridRetriever.from_config(config).retrieve(args.query, options)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if args.json:
        _print_json(result.to_dict())
    else:
        print_retrieval_text(result)
    return 0


def _run_evals(args: argparse.Namespace) -> int:
    config = config_from_args(args)
    options = RetrievalOptions(top_k=args.top_k, candidates=args.candidates)
    if args.dry_run and args.live:
        print("Choose either --live or --dry-run/--list, not both.", file=sys.stderr)
        return 2
    try:
        cases = load_eval_cases(args.dataset)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Could not load retrieval eval dataset: {exc}", file=sys.stderr)
        return 2

    if args.live:
        try:
            report = run_live_evals(cases, config=config, options=options)
        except RuntimeError as exc:
            print(str(exc), file=sys.stderr)
            return 2
    else:
        report = build_dry_run_eval_report(cases, config=config, options=options)

    if args.json:
        _print_json(report.to_dict())
    else:
        print_eval_text(report.to_dict())
    return 0


def print_crawl_text(payload: dict[str, object]) -> None:
    print("Website crawl dry-run (no credentials, embeddings, or turbopuffer API calls):")
    print(f"  base_url: {payload['base_url']}")
    print(f"  namespace_candidate: {payload['namespace_candidate']}")
    print(f"  strategy: {payload['crawl_strategy']}")
    print(f"  pages_scraped: {payload['pages_scraped']}; chunks_generated: {payload['chunks_generated']}")
    print(f"  out_dir: {payload['out_dir']}")
    print("  live writes: not supported by this command")


def print_plan_text(payload: dict[str, object]) -> None:
    print("Website RAG plan (local-only; no credentials, embeddings, or turbopuffer API calls):")
    print(f"  base_url: {payload['base_url']}")
    print(f"  namespace: {payload['namespace']}")
    print(f"  plan_id: {payload['plan_id']}")
    print(f"  pages_scraped: {payload['pages_scraped']}; chunks_generated: {payload['chunks_generated']}")
    diff = payload.get("diff", {}) if isinstance(payload.get("diff"), dict) else {}
    print(
        "  diff: "
        f"first_apply={diff.get('first_apply')}, "
        f"upsert={diff.get('rows_to_upsert')}, "
        f"unchanged={diff.get('chunks_unchanged')}, "
        f"stale={diff.get('stale_rows')}, "
        f"retained_stale={diff.get('retained_stale_rows')}"
    )
    print(f"  plan_path: {payload['plan_path']}")
    print(f"  state_path: {payload['state_path']}")
    print("  live writes: not supported by this command; future apply must be explicit")


def print_apply_text(payload: dict[str, object]) -> None:
    if payload.get("approved"):
        print("Website RAG apply completed (explicitly approved live upsert path):")
    else:
        print("Website RAG apply preflight (no credentials, embeddings, or turbopuffer API calls):")
    print(f"  namespace: {payload['namespace']}")
    print(f"  plan_id: {payload['plan_id']}")
    print(f"  rows_to_upsert: {payload['rows_to_upsert']}; rows_upserted: {payload['rows_upserted']}")
    print(
        f"  stale_rows: {payload['stale_rows']}; "
        f"retained_stale_rows: {payload['retained_stale_rows']}; "
        f"stale_rows_to_delete: {payload['stale_rows_to_delete']}; "
        f"rows_deleted: {payload['rows_deleted']}"
    )
    print(f"  state_path: {payload['state_path']}")
    if not payload.get("approved"):
        print("  live: pass --approve to embed and upsert selected rows")


def print_retrieval_text(output: RetrievalPlan | RetrievalResult) -> None:
    payload = output.to_dict()
    if payload.get("dry_run"):
        print("Retrieval plan (dry-run; no credentials, embeddings, or turbopuffer API calls):")
        print(f"  query: {payload['query']}")
        print(f"  namespace: {payload['namespace']} ({payload['region']})")
        print(f"  embedding_model: {payload['embedding_model']}")
        print(f"  top_k: {payload['top_k']}; candidates per subquery: {payload['candidates']}")
        print("  hybrid: ANN over vector + boosted BM25 over title/section_path/content + RRF")
        print("  live: pass --live to execute; TURBOPUFFER_API_KEY is read from the environment only")
        return

    hits = payload.get("hits", [])
    print(f"Retrieved {len(hits)} chunks using {payload.get('fusion')}:")
    for index, hit in enumerate(hits, start=1):
        if not isinstance(hit, dict):
            continue
        title = hit.get("title") or "Untitled"
        url = hit.get("url") or "no URL"
        section_path = hit.get("section_path") or ""
        print(f"\n{index}. {title}")
        print(f"   URL: {url}")
        if section_path:
            print(f"   Section: {section_path}")
        if hit.get("path"):
            print(f"   Path: {hit['path']}")
        print(f"   Score: {hit.get('score_info', {})}")
        content = str(hit.get("content") or "").strip()
        if content:
            preview = content if len(content) <= 600 else content[:597].rstrip() + "..."
            print(f"   Content: {preview}")


def print_eval_text(payload: dict[str, object]) -> None:
    if payload.get("dry_run"):
        print("Retrieval smoke evals (dry-run; no credentials, embeddings, or turbopuffer API calls):")
        print(f"  namespace: {payload['namespace']} ({payload['region']})")
        print(f"  evals: {payload['total']}; top_k: {payload['top_k']}; candidates: {payload['candidates']}")
        print("  live: pass --live to execute; TURBOPUFFER_API_KEY is read from the environment only")
    else:
        print(
            f"Retrieval smoke evals: {payload['passed']}/{payload['total']} passed "
            f"({float(payload['pass_rate']) * 100:.1f}%)"
        )
        print(f"  namespace: {payload['namespace']} ({payload['region']})")
    cases = payload.get("cases", [])
    if not isinstance(cases, list):
        return
    for case in cases:
        if not isinstance(case, dict):
            continue
        print(f"\n- {case.get('id')}: {case.get('question')}")
        if payload.get("dry_run"):
            print(f"  expected_urls: {case.get('expected_urls', [])}")
            print(f"  expected_topics: {case.get('expected_topics', [])}")
            continue
        score = case.get("score") if isinstance(case.get("score"), dict) else {}
        print(f"  status: {case.get('status')} (matched_rank={score.get('matched_rank')})")
        top_hits = case.get("top_hits", [])
        if not isinstance(top_hits, list):
            continue
        for hit in top_hits:
            if not isinstance(hit, dict):
                continue
            print(f"  {hit.get('rank')}. {hit.get('title') or 'Untitled'}")
            print(f"     URL: {hit.get('url') or 'no URL'}")
            if hit.get("section_path"):
                print(f"     Section: {hit['section_path']}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
