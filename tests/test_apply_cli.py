from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import json
import os
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

from turbo_search.applied_state import ROW_STATUS_ACTIVE, ROW_STATUS_RETAINED_STALE, AppliedStateRow, build_applied_state, load_applied_state, save_applied_state
from turbo_search.cli import main
from turbo_search.chunker import process_corpus
from turbo_search.plan_artifacts import build_plan_artifacts, write_plan_artifacts


class FakeEmbedder:
    texts: list[str] = []

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    def encode(self, texts):
        FakeEmbedder.texts.extend(list(texts))
        return [[float(index), 0.0, 1.0] for index, _ in enumerate(texts, start=1)]


class FakeWriter:
    rows: list[dict[str, object]] = []
    deletes: list[str] = []
    should_fail = False
    should_delete_fail = False

    def __init__(self, *, config, api_key: str, schema=None) -> None:
        self.config = config
        self.api_key = api_key
        self.schema = schema

    def upsert_rows(self, rows):
        if FakeWriter.should_fail:
            raise RuntimeError("fake upsert failure")
        FakeWriter.rows.extend(list(rows))

    def delete_rows(self, row_ids):
        if FakeWriter.should_delete_fail:
            raise RuntimeError("fake delete failure")
        FakeWriter.deletes.extend(list(row_ids))


def reset_fakes() -> None:
    FakeEmbedder.texts = []
    FakeWriter.rows = []
    FakeWriter.deletes = []
    FakeWriter.should_fail = False
    FakeWriter.should_delete_fail = False


def write_page(corpus: Path, name: str, url: str, title: str, body: str) -> None:
    corpus.mkdir(parents=True, exist_ok=True)
    (corpus / name).write_text(
        "\n".join(
            [
                "---",
                f'url: "{url}"',
                f'title: "{title}"',
                'status: "200"',
                'content_type: "text/html"',
                'source_hash: "source-hash"',
                'crawl_timestamp: "2026-06-20T00:00:00+00:00"',
                'fetcher: "test"',
                "---",
                "",
                body,
                "",
            ]
        ),
        encoding="utf-8",
    )


def build_saved_plan(root: Path, *, state_root: Path | None = None, page_b_body: str = "# Intro\n\nBeta useful docs."):
    corpus = root / "pages"
    write_page(corpus, "a.md", "https://example.com/docs/a", "Page A", "# Intro\n\nAlpha useful docs.")
    write_page(corpus, "b.md", "https://example.com/docs/b", "Page B", page_b_body)
    out_dir = root / "plan"
    artifacts = build_plan_artifacts(
        indexing_plan=process_corpus(corpus),
        base_url="https://example.com/docs/",
        out_dir=out_dir,
        state_root=state_root or root / "state",
    )
    write_plan_artifacts(artifacts, out_dir)
    return artifacts, out_dir / "plan.json"


def build_one_page_plan_with_stale_state(root: Path, state_root: Path):
    previous_artifacts, _ = build_saved_plan(root / "previous", state_root=state_root)
    desired = previous_artifacts.manifest.chunks[0]
    stale = previous_artifacts.manifest.chunks[1]

    one_page_root = root / "one-page"
    corpus = one_page_root / "pages"
    write_page(corpus, "a.md", "https://example.com/docs/a", "Page A", "# Intro\n\nAlpha useful docs.")
    one_page_artifacts = build_plan_artifacts(
        indexing_plan=process_corpus(corpus),
        base_url="https://example.com/docs/",
        out_dir=one_page_root / "plan",
        state_root=state_root,
    )
    write_plan_artifacts(one_page_artifacts, one_page_root / "plan")
    save_applied_state(
        build_applied_state(
            site_id=previous_artifacts.manifest.site_id,
            namespace=previous_artifacts.manifest.namespace,
            base_url=previous_artifacts.manifest.base_url,
            last_plan_id="plan_previous",
            last_apply_id="apply_previous",
            rows=[
                AppliedStateRow(
                    row_id=desired.row_id,
                    canonical_url=desired.canonical_url,
                    page_hash=desired.page_hash,
                    chunk_hash=desired.chunk_hash,
                    embedding_text_hash=desired.embedding_text_hash,
                    plan_id="plan_previous",
                    applied_at="2026-06-20T12:00:00+00:00",
                ),
                AppliedStateRow(
                    row_id=stale.row_id,
                    canonical_url=stale.canonical_url,
                    page_hash=stale.page_hash,
                    chunk_hash=stale.chunk_hash,
                    embedding_text_hash=stale.embedding_text_hash,
                    plan_id="plan_previous",
                    applied_at="2026-06-20T12:00:00+00:00",
                ),
            ],
            updated_at="2026-06-20T12:00:00+00:00",
        ),
        state_root=state_root,
    )
    return previous_artifacts, one_page_artifacts, one_page_root / "plan" / "plan.json", stale


class ApplyCliTests(unittest.TestCase):
    def setUp(self) -> None:
        reset_fakes()

    def run_main(self, args: list[str], *, env: dict[str, str] | None = None):
        stdout = StringIO()
        stderr = StringIO()
        env_patch = {} if env is None else env
        with patch.dict("os.environ", env_patch, clear=True):
            with redirect_stdout(stdout), redirect_stderr(stderr):
                result = main(args)
        return result, stdout.getvalue(), stderr.getvalue()

    def test_apply_preflight_verifies_plan_without_credentials_or_live_calls(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_root = root / "state"
            _, plan_path = build_saved_plan(root, state_root=state_root)

            with patch("turbo_search.apply.SentenceTransformerEmbedder", side_effect=AssertionError("embedder called")), patch(
                "turbo_search.apply.TurbopufferWriter", side_effect=AssertionError("writer called")
            ):
                result, stdout, stderr = self.run_main(
                    [
                        "apply",
                        "--plan",
                        str(plan_path),
                        "--namespace",
                        "site-example-com-v1",
                        "--state-root",
                        str(state_root),
                        "--json",
                    ]
                )

        payload = json.loads(stdout)
        self.assertEqual(result, 0, stderr)
        self.assertEqual(payload["command"], "apply")
        self.assertFalse(payload["approved"])
        self.assertTrue(payload["dry_run"])
        self.assertFalse(payload["credentials_required"])
        self.assertFalse(payload["turbopuffer_api_calls"])
        self.assertFalse(payload["api_calls_occurred"])
        self.assertTrue(payload["artifact_verified"])
        self.assertEqual(payload["rows_to_upsert"], 2)
        self.assertEqual(payload["rows_upserted"], 0)
        self.assertEqual(stderr, "")

    def test_apply_defaults_to_latest_plan_and_plan_namespace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old_cwd = Path.cwd()
            try:
                os.chdir(root)
                _, old_plan_path = build_saved_plan(
                    root / "artifacts/site-crawls/old-site-plan",
                    state_root=Path(".turbo-search"),
                )
                _, latest_plan_path = build_saved_plan(
                    root / "artifacts/site-crawls/latest-site-plan",
                    state_root=Path(".turbo-search"),
                )
                os.utime(old_plan_path, (1, 1))
                os.utime(latest_plan_path, (2, 2))

                result, stdout, stderr = self.run_main(["apply", "--json"])
            finally:
                os.chdir(old_cwd)

        payload = json.loads(stdout)
        self.assertEqual(result, 0, stderr)
        self.assertEqual(payload["plan_path"], str(latest_plan_path.relative_to(root)))
        self.assertEqual(payload["namespace"], "site-example-com-v1")
        self.assertFalse(payload["approved"])
        self.assertFalse(payload["turbopuffer_api_calls"])

    def test_apply_without_plan_fails_clearly_when_no_local_plan_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old_cwd = Path.cwd()
            try:
                os.chdir(root)
                result, stdout, stderr = self.run_main(["apply", "--json"])
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result, 2)
        self.assertEqual(stdout, "")
        self.assertIn("No plan search root found", stderr)
        self.assertIn("pass --plan explicitly", stderr)

    def test_approved_apply_requires_api_key_before_embedding_or_writing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_root = root / "state"
            _, plan_path = build_saved_plan(root, state_root=state_root)

            with patch("turbo_search.apply.SentenceTransformerEmbedder", side_effect=AssertionError("embedder called")), patch(
                "turbo_search.apply.TurbopufferWriter", side_effect=AssertionError("writer called")
            ):
                result, stdout, stderr = self.run_main(
                    [
                        "apply",
                        "--plan",
                        str(plan_path),
                        "--namespace",
                        "site-example-com-v1",
                        "--state-root",
                        str(state_root),
                        "--approve",
                        "--json",
                    ]
                )

        self.assertEqual(result, 2)
        self.assertEqual(stdout, "")
        self.assertIn("TURBOPUFFER_API_KEY must be set", stderr)

    def test_approved_apply_upserts_only_diff_rows_and_updates_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_root = root / "state"
            artifacts, plan_path = build_saved_plan(root, state_root=state_root)
            unchanged, needs_upsert = artifacts.manifest.chunks
            save_applied_state(
                build_applied_state(
                    site_id=artifacts.manifest.site_id,
                    namespace=artifacts.manifest.namespace,
                    base_url=artifacts.manifest.base_url,
                    last_plan_id="plan_previous",
                    last_apply_id="apply_previous",
                    rows=[
                        AppliedStateRow(
                            row_id=unchanged.row_id,
                            canonical_url=unchanged.canonical_url,
                            page_hash=unchanged.page_hash,
                            chunk_hash=unchanged.chunk_hash,
                            embedding_text_hash=unchanged.embedding_text_hash,
                            plan_id="plan_previous",
                            applied_at="2026-06-20T12:00:00+00:00",
                        )
                    ],
                    updated_at="2026-06-20T12:00:00+00:00",
                ),
                state_root=state_root,
            )

            with patch("turbo_search.apply.SentenceTransformerEmbedder", FakeEmbedder), patch(
                "turbo_search.apply.TurbopufferWriter", FakeWriter
            ):
                result, stdout, stderr = self.run_main(
                    [
                        "apply",
                        "--plan",
                        str(plan_path),
                        "--namespace",
                        artifacts.manifest.namespace,
                        "--state-root",
                        str(state_root),
                        "--approve",
                        "--json",
                    ],
                    env={"TURBOPUFFER_API_KEY": "test-key"},
                )

            payload = json.loads(stdout)
            loaded_state = load_applied_state(
                site_id=artifacts.manifest.site_id,
                namespace=artifacts.manifest.namespace,
                base_url=artifacts.manifest.base_url,
                state_root=state_root,
            )

        self.assertEqual(result, 0, stderr)
        self.assertTrue(payload["approved"])
        self.assertEqual(payload["rows_to_upsert"], 1)
        self.assertEqual(payload["rows_upserted"], 1)
        self.assertEqual(payload["embeddings_generated"], 1)
        self.assertEqual(len(FakeEmbedder.texts), 1)
        self.assertIn("Beta useful docs", FakeEmbedder.texts[0])
        self.assertEqual([row["id"] for row in FakeWriter.rows], [needs_upsert.row_id])
        self.assertTrue(payload["state_updated"])
        self.assertFalse(loaded_state.first_apply)
        self.assertEqual({row.row_id for row in loaded_state.rows if row.status == ROW_STATUS_ACTIVE}, {unchanged.row_id, needs_upsert.row_id})

    def test_approved_apply_does_not_update_state_when_upsert_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_root = root / "state"
            artifacts, plan_path = build_saved_plan(root, state_root=state_root)
            FakeWriter.should_fail = True

            with patch("turbo_search.apply.SentenceTransformerEmbedder", FakeEmbedder), patch(
                "turbo_search.apply.TurbopufferWriter", FakeWriter
            ):
                result, stdout, stderr = self.run_main(
                    [
                        "apply",
                        "--plan",
                        str(plan_path),
                        "--namespace",
                        artifacts.manifest.namespace,
                        "--state-root",
                        str(state_root),
                        "--approve",
                        "--json",
                    ],
                    env={"TURBOPUFFER_API_KEY": "test-key"},
                )
            loaded_state = load_applied_state(
                site_id=artifacts.manifest.site_id,
                namespace=artifacts.manifest.namespace,
                base_url=artifacts.manifest.base_url,
                state_root=state_root,
            )

        self.assertEqual(result, 2)
        self.assertEqual(stdout, "")
        self.assertIn("fake upsert failure", stderr)
        self.assertTrue(loaded_state.first_apply)

    def test_approved_apply_with_delete_stale_fails_when_no_stale_rows_before_credentials(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_root = root / "state"
            artifacts, plan_path = build_saved_plan(root, state_root=state_root)

            with patch("turbo_search.apply.SentenceTransformerEmbedder", side_effect=AssertionError("embedder called")), patch(
                "turbo_search.apply.TurbopufferWriter", side_effect=AssertionError("writer called")
            ):
                result, stdout, stderr = self.run_main(
                    [
                        "apply",
                        "--plan",
                        str(plan_path),
                        "--namespace",
                        artifacts.manifest.namespace,
                        "--state-root",
                        str(state_root),
                        "--approve",
                        "--delete-stale",
                        "--json",
                    ]
                )

        self.assertEqual(result, 2)
        self.assertEqual(stdout, "")
        self.assertIn("no stale rows", stderr)
        self.assertEqual(FakeEmbedder.texts, [])
        self.assertEqual(FakeWriter.rows, [])
        self.assertEqual(FakeWriter.deletes, [])

    def test_apply_fails_on_artifact_hash_mismatch_before_credentials(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_root = root / "state"
            _, plan_path = build_saved_plan(root, state_root=state_root)
            manifest_path = plan_path.parent / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["chunks"][0]["content"] = "tampered content"
            manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

            with patch("turbo_search.apply.SentenceTransformerEmbedder", side_effect=AssertionError("embedder called")), patch(
                "turbo_search.apply.TurbopufferWriter", side_effect=AssertionError("writer called")
            ):
                result, stdout, stderr = self.run_main(
                    [
                        "apply",
                        "--plan",
                        str(plan_path),
                        "--namespace",
                        "site-example-com-v1",
                        "--state-root",
                        str(state_root),
                        "--approve",
                        "--json",
                    ],
                    env={"TURBOPUFFER_API_KEY": "test-key"},
                )

        self.assertEqual(result, 2)
        self.assertEqual(stdout, "")
        self.assertTrue("chunks.jsonl does not match" in stderr or "artifact hash mismatch" in stderr)

    def test_apply_fails_on_namespace_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_root = root / "state"
            _, plan_path = build_saved_plan(root, state_root=state_root)

            result, stdout, stderr = self.run_main(
                [
                    "apply",
                    "--plan",
                    str(plan_path),
                    "--namespace",
                    "site-other-v1",
                    "--state-root",
                    str(state_root),
                    "--json",
                ]
            )

        self.assertEqual(result, 2)
        self.assertEqual(stdout, "")
        self.assertIn("namespace mismatch", stderr)

    def test_apply_fails_on_incompatible_local_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_root = root / "state"
            artifacts, plan_path = build_saved_plan(root, state_root=state_root)
            save_applied_state(
                build_applied_state(
                    site_id=artifacts.manifest.site_id,
                    namespace=artifacts.manifest.namespace,
                    base_url="https://example.com/other/",
                    last_plan_id="plan_previous",
                    last_apply_id="apply_previous",
                    rows=[],
                    updated_at="2026-06-20T12:00:00+00:00",
                ),
                state_root=state_root,
            )

            result, stdout, stderr = self.run_main(
                [
                    "apply",
                    "--plan",
                    str(plan_path),
                    "--namespace",
                    artifacts.manifest.namespace,
                    "--state-root",
                    str(state_root),
                    "--json",
                ]
            )

        self.assertEqual(result, 2)
        self.assertEqual(stdout, "")
        self.assertIn("base_url mismatch", stderr)

    def test_successful_apply_marks_stale_rows_as_retained_without_delete(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_root = root / "state"
            artifacts, plan_path = build_saved_plan(root, state_root=state_root)
            desired = artifacts.manifest.chunks[0]
            stale = artifacts.manifest.chunks[1]
            # Rebuild a one-page desired plan so the saved state's second row is stale.
            one_page_root = root / "one-page"
            corpus = one_page_root / "pages"
            write_page(corpus, "a.md", "https://example.com/docs/a", "Page A", "# Intro\n\nAlpha useful docs.")
            one_page_artifacts = build_plan_artifacts(
                indexing_plan=process_corpus(corpus),
                base_url="https://example.com/docs/",
                out_dir=one_page_root / "plan",
                state_root=state_root,
            )
            write_plan_artifacts(one_page_artifacts, one_page_root / "plan")
            plan_path = one_page_root / "plan" / "plan.json"
            save_applied_state(
                build_applied_state(
                    site_id=artifacts.manifest.site_id,
                    namespace=artifacts.manifest.namespace,
                    base_url=artifacts.manifest.base_url,
                    last_plan_id="plan_previous",
                    last_apply_id="apply_previous",
                    rows=[
                        AppliedStateRow(
                            row_id=desired.row_id,
                            canonical_url=desired.canonical_url,
                            page_hash=desired.page_hash,
                            chunk_hash=desired.chunk_hash,
                            embedding_text_hash=desired.embedding_text_hash,
                            plan_id="plan_previous",
                            applied_at="2026-06-20T12:00:00+00:00",
                        ),
                        AppliedStateRow(
                            row_id=stale.row_id,
                            canonical_url=stale.canonical_url,
                            page_hash=stale.page_hash,
                            chunk_hash=stale.chunk_hash,
                            embedding_text_hash=stale.embedding_text_hash,
                            plan_id="plan_previous",
                            applied_at="2026-06-20T12:00:00+00:00",
                        ),
                    ],
                    updated_at="2026-06-20T12:00:00+00:00",
                ),
                state_root=state_root,
            )

            with patch("turbo_search.apply.SentenceTransformerEmbedder", FakeEmbedder), patch(
                "turbo_search.apply.TurbopufferWriter", FakeWriter
            ):
                result, stdout, stderr = self.run_main(
                    [
                        "apply",
                        "--plan",
                        str(plan_path),
                        "--namespace",
                        artifacts.manifest.namespace,
                        "--state-root",
                        str(state_root),
                        "--approve",
                        "--json",
                    ],
                    env={"TURBOPUFFER_API_KEY": "test-key"},
                )
            loaded_state = load_applied_state(
                site_id=artifacts.manifest.site_id,
                namespace=artifacts.manifest.namespace,
                base_url=artifacts.manifest.base_url,
                state_root=state_root,
            )

        payload = json.loads(stdout)
        self.assertEqual(result, 0, stderr)
        self.assertEqual(payload["rows_to_upsert"], 0)
        self.assertEqual(payload["stale_rows"], 1)
        self.assertFalse(payload["delete_stale"])
        self.assertEqual(payload["stale_rows_to_delete"], 0)
        self.assertEqual(payload["rows_deleted"], 0)
        self.assertEqual(FakeWriter.deletes, [])
        retained = [row for row in loaded_state.rows if row.status == ROW_STATUS_RETAINED_STALE]
        self.assertEqual([row.row_id for row in retained], [stale.row_id])

    def test_apply_preflight_reports_stale_retention_without_delete_flag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_root = root / "state"
            artifacts, _, plan_path, _stale = build_one_page_plan_with_stale_state(root, state_root)

            with patch("turbo_search.apply.SentenceTransformerEmbedder", side_effect=AssertionError("embedder called")), patch(
                "turbo_search.apply.TurbopufferWriter", side_effect=AssertionError("writer called")
            ):
                result, stdout, stderr = self.run_main(
                    [
                        "apply",
                        "--plan",
                        str(plan_path),
                        "--namespace",
                        artifacts.manifest.namespace,
                        "--state-root",
                        str(state_root),
                        "--json",
                    ]
                )

        payload = json.loads(stdout)
        self.assertEqual(result, 0, stderr)
        self.assertFalse(payload["approved"])
        self.assertFalse(payload["delete_stale"])
        self.assertFalse(payload["delete_would_run"])
        self.assertEqual(payload["stale_rows"], 1)
        self.assertEqual(payload["stale_rows_to_delete"], 0)
        self.assertEqual(payload["stale_row_ids_to_delete"], [])
        self.assertEqual(payload["stale_rows_retained"], 1)
        self.assertEqual(payload["rows_deleted"], 0)
        self.assertEqual(stderr, "")

    def test_apply_preflight_reports_delete_stale_without_deleting(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_root = root / "state"
            artifacts, _, plan_path, stale = build_one_page_plan_with_stale_state(root, state_root)

            with patch("turbo_search.apply.SentenceTransformerEmbedder", side_effect=AssertionError("embedder called")), patch(
                "turbo_search.apply.TurbopufferWriter", side_effect=AssertionError("writer called")
            ):
                result, stdout, stderr = self.run_main(
                    [
                        "apply",
                        "--plan",
                        str(plan_path),
                        "--namespace",
                        artifacts.manifest.namespace,
                        "--state-root",
                        str(state_root),
                        "--delete-stale",
                        "--json",
                    ]
                )
            loaded_state = load_applied_state(
                site_id=artifacts.manifest.site_id,
                namespace=artifacts.manifest.namespace,
                base_url=artifacts.manifest.base_url,
                state_root=state_root,
            )

        payload = json.loads(stdout)
        self.assertEqual(result, 0, stderr)
        self.assertFalse(payload["approved"])
        self.assertTrue(payload["delete_stale"])
        self.assertTrue(payload["delete_would_run"])
        self.assertEqual(payload["stale_rows"], 1)
        self.assertEqual(payload["stale_rows_to_delete"], 1)
        self.assertEqual(payload["stale_row_ids_to_delete"], [stale.row_id])
        self.assertEqual(payload["rows_deleted"], 0)
        self.assertEqual(stderr, "")
        self.assertEqual([row.row_id for row in loaded_state.rows], [artifacts.manifest.chunks[0].row_id, stale.row_id])

    def test_approved_apply_with_delete_stale_deletes_exact_stale_ids_and_updates_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_root = root / "state"
            artifacts, _, plan_path, stale = build_one_page_plan_with_stale_state(root, state_root)

            with patch("turbo_search.apply.SentenceTransformerEmbedder", FakeEmbedder), patch(
                "turbo_search.apply.TurbopufferWriter", FakeWriter
            ):
                result, stdout, stderr = self.run_main(
                    [
                        "apply",
                        "--plan",
                        str(plan_path),
                        "--namespace",
                        artifacts.manifest.namespace,
                        "--state-root",
                        str(state_root),
                        "--approve",
                        "--delete-stale",
                        "--json",
                    ],
                    env={"TURBOPUFFER_API_KEY": "test-key"},
                )
            loaded_state = load_applied_state(
                site_id=artifacts.manifest.site_id,
                namespace=artifacts.manifest.namespace,
                base_url=artifacts.manifest.base_url,
                state_root=state_root,
            )

        payload = json.loads(stdout)
        self.assertEqual(result, 0, stderr)
        self.assertTrue(payload["approved"])
        self.assertTrue(payload["delete_stale"])
        self.assertEqual(payload["stale_rows_to_delete"], 1)
        self.assertEqual(payload["rows_deleted"], 1)
        self.assertEqual(payload["stale_rows_retained"], 0)
        self.assertEqual(FakeWriter.deletes, [stale.row_id])
        self.assertEqual([row.row_id for row in loaded_state.rows], [artifacts.manifest.chunks[0].row_id])
        self.assertFalse([row for row in loaded_state.rows if row.status == ROW_STATUS_RETAINED_STALE])

    def test_approved_apply_does_not_update_state_when_delete_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_root = root / "state"
            artifacts, _, plan_path, stale = build_one_page_plan_with_stale_state(root, state_root)
            FakeWriter.should_delete_fail = True

            with patch("turbo_search.apply.SentenceTransformerEmbedder", FakeEmbedder), patch(
                "turbo_search.apply.TurbopufferWriter", FakeWriter
            ):
                result, stdout, stderr = self.run_main(
                    [
                        "apply",
                        "--plan",
                        str(plan_path),
                        "--namespace",
                        artifacts.manifest.namespace,
                        "--state-root",
                        str(state_root),
                        "--approve",
                        "--delete-stale",
                        "--json",
                    ],
                    env={"TURBOPUFFER_API_KEY": "test-key"},
                )
            loaded_state = load_applied_state(
                site_id=artifacts.manifest.site_id,
                namespace=artifacts.manifest.namespace,
                base_url=artifacts.manifest.base_url,
                state_root=state_root,
            )

        self.assertEqual(result, 2)
        self.assertEqual(stdout, "")
        self.assertIn("fake delete failure", stderr)
        self.assertEqual(FakeWriter.deletes, [])
        self.assertEqual([row.row_id for row in loaded_state.rows], [artifacts.manifest.chunks[0].row_id, stale.row_id])
        self.assertTrue(all(row.status == ROW_STATUS_ACTIVE for row in loaded_state.rows))


if __name__ == "__main__":
    unittest.main()
