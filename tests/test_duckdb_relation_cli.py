from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import json
import os
from pathlib import Path
import tempfile
import unittest

import duckdb

from buoy_search.cli import build_parser, main
from buoy_search.plan_artifacts import PLAN_SCHEMA_VERSION


class DuckDBRelationCliTests(unittest.TestCase):
    def run_cli(self, args: list[str]) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            result = main(args)
        return result, stdout.getvalue(), stderr.getvalue()

    def test_plan_materializes_relation_without_path_leak_and_saved_dry_run_survives_source_deletion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            database = root / "sensitive" / "calls.duckdb"
            database.parent.mkdir()
            with duckdb.connect(str(database)) as connection:
                connection.execute("CREATE TABLE calls(call_id VARCHAR, transcript VARCHAR, subject VARCHAR)")
                connection.execute(
                    "INSERT INTO calls VALUES "
                    "('call/b', 'Second transcript body.', NULL), "
                    "('call/a', 'First transcript body.', 'First call'), "
                    "('empty', '  ', 'Empty')"
                )
            out_dir = root / "plan"
            state_root = root / "state"

            result, stdout, stderr = self.run_cli(
                [
                    "plan",
                    str(database),
                    "--relation",
                    "calls",
                    "--source-id",
                    "gong-calls",
                    "--id-column",
                    "call_id",
                    "--content-column",
                    "transcript",
                    "--title-column",
                    "subject",
                    "--out-dir",
                    str(out_dir),
                    "--state-root",
                    str(state_root),
                    "--max-pages",
                    "1",
                    "--max-chunks",
                    "10",
                    "--no-progress",
                    "--json",
                ]
            )

            self.assertEqual(result, 0, stderr)
            payload = json.loads(stdout)
            self.assertEqual(payload["source_kind"], "duckdb_relation")
            self.assertEqual(payload["base_url"], "duckdb://gong-calls")
            self.assertEqual(payload["site_id"], "duckdb-gong-calls")
            self.assertEqual(payload["namespace"], "duckdb-gong-calls-v1")
            self.assertEqual(payload["duckdb_relation"], "calls")
            self.assertEqual(payload["rows_scanned"], 3)
            self.assertEqual(payload["documents_selected"], 1)
            self.assertEqual(payload["documents_skipped_empty"], 1)
            self.assertEqual(payload["documents_skipped_limit"], 1)
            self.assertTrue(payload["document_limit_reached"])
            self.assertFalse(payload["credentials_required"])
            self.assertFalse(payload["turbopuffer_api_calls"])
            self.assertEqual(
                payload["catalog_registration"],
                {
                    "action": "unknown_until_approved",
                    "catalog_namespace": "buoy-routing-catalog-v1",
                    "manual_semantics_preservation": "unknown_until_approved",
                    "namespace": "duckdb-gong-calls-v1",
                    "ranking_aggregation": "max",
                    "ranking_mode": "page",
                    "ranking_pool": 20,
                    "ranking_profile": "none",
                    "region": "gcp-us-central1",
                    "remote_catalog_state": "unknown_until_approved",
                    "source_kind": "database",
                    "vector_dimensions": 384,
                },
            )
            plan = json.loads((out_dir / "plan.json").read_text(encoding="utf-8"))
            manifest = json.loads((out_dir / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(plan["schema_version"], PLAN_SCHEMA_VERSION)
            self.assertEqual(plan["crawl_options"]["source_kind"], "duckdb_relation")
            self.assertEqual(plan["crawl_options"]["duckdb_source_id"], "gong-calls")
            self.assertEqual(plan["crawl_options"]["duckdb_relation"], "calls")
            self.assertEqual(plan["crawl_options"]["id_column"], "call_id")
            self.assertEqual(plan["crawl_options"]["content_column"], "transcript")
            self.assertEqual(plan["crawl_options"]["title_column"], "subject")
            self.assertEqual(manifest["base_url"], "duckdb://gong-calls")
            self.assertEqual(manifest["pages"][0]["canonical_url"], "duckdb://gong-calls/call%2Fa")
            self.assertEqual(manifest["pages"][0]["source_metadata"]["duckdb_document_id"], "call/a")
            serialized = "\n".join(
                (out_dir / filename).read_text(encoding="utf-8")
                for filename in ("plan.json", "manifest.json", "chunks.jsonl", "summary.json")
            ) + "\n" + "\n".join(
                path.read_text(encoding="utf-8") for path in (out_dir / "pages").glob("*.md")
            )
            self.assertNotIn(str(database), serialized)

            database.unlink()
            apply_result, apply_stdout, apply_stderr = self.run_cli(
                [
                    "apply",
                    "--dry-run",
                    "--plan",
                    str(out_dir / "plan.json"),
                    "--state-root",
                    str(state_root),
                    "--no-progress",
                    "--json",
                ]
            )

            self.assertEqual(apply_result, 0, apply_stderr)
            apply_payload = json.loads(apply_stdout)
            self.assertTrue(apply_payload["artifact_verified"])
            self.assertEqual(apply_payload["base_url"], "duckdb://gong-calls")
            self.assertEqual(apply_payload["namespace"], "duckdb-gong-calls-v1")
            self.assertFalse(apply_payload["api_calls_occurred"])
            self.assertEqual(apply_payload["catalog_registration"]["source_kind"], "database")
            self.assertEqual(apply_payload["catalog_registration"]["ranking_mode"], "page")
            self.assertEqual(apply_payload["catalog_registration"]["ranking_profile"], "none")

    def test_crawl_accepts_database_base_url_and_table_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            database = root / "docs.duckdb"
            with duckdb.connect(str(database)) as connection:
                connection.execute("CREATE TABLE docs(document_id VARCHAR, content VARCHAR)")
                connection.execute("INSERT INTO docs VALUES ('one', 'One document body.')")
            out_dir = root / "crawl"

            result, stdout, stderr = self.run_cli(
                [
                    "crawl",
                    "--base-url",
                    str(database),
                    "--table",
                    "docs",
                    "--source-id",
                    "local-docs",
                    "--out-dir",
                    str(out_dir),
                    "--json",
                ]
            )

            self.assertEqual(result, 0, stderr)
            payload = json.loads(stdout)
            self.assertEqual(payload["base_url"], "duckdb://local-docs")
            self.assertEqual(payload["duckdb_relation"], "docs")
            self.assertEqual(payload["documents_generated"], 1)
            self.assertEqual(len(list((out_dir / "pages").glob("*.md"))), 1)

    def test_plan_external_backed_view_recommends_upstream_materialization(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            external_csv = root / "documents.csv"
            external_csv.write_text(
                "document_id,content\none,External document body.\n",
                encoding="utf-8",
            )
            database = root / "docs.duckdb"
            with duckdb.connect(str(database)) as connection:
                connection.execute(
                    f"CREATE VIEW docs AS SELECT * FROM read_csv_auto('{external_csv.as_posix()}')"
                )

            result, stdout, stderr = self.run_cli(
                [
                    "plan",
                    str(database),
                    "--relation",
                    "docs",
                    "--source-id",
                    "external-docs",
                    "--out-dir",
                    str(root / "out"),
                    "--no-progress",
                    "--json",
                ]
            )

            self.assertEqual(result, 2)
            self.assertEqual(stdout, "")
            self.assertEqual(
                stderr.strip(),
                "DuckDB relation 'docs' depends on external files, databases, or extensions, "
                "which Buoy disables for safe read-only indexing. Materialize the final relation "
                "as a table in this DuckDB database upstream, then plan again.",
            )
            self.assertNotIn(str(external_csv), stderr)

    def test_database_flags_require_relation_and_relation_requires_source_id(self) -> None:
        parser = build_parser()
        plan_help = parser._subparsers._group_actions[0].choices["plan"].format_help()
        crawl_help = parser._subparsers._group_actions[0].choices["crawl"].format_help()
        self.assertIn("pages/files/documents", plan_help)
        self.assertIn("pages/files/documents", crawl_help)
        self.assertIn("--relation", plan_help)
        self.assertIn("--table", crawl_help)

        result, stdout, stderr = self.run_cli(
            ["plan", "https://example.com", "--source-id", "not-database", "--json"]
        )
        self.assertEqual(result, 2)
        self.assertEqual(stdout, "")
        self.assertIn("--source-id require --relation", stderr)

        with tempfile.TemporaryDirectory() as tmp:
            database = Path(tmp) / "docs.duckdb"
            database.touch()
            result, stdout, stderr = self.run_cli(
                ["plan", str(database), "--relation", "docs", "--json"]
            )
        self.assertEqual(result, 2)
        self.assertEqual(stdout, "")
        self.assertIn("--source-id is required", stderr)

    def test_default_plan_output_uses_stable_source_identity_without_plan_suffix(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            database = root / "docs.duckdb"
            with duckdb.connect(str(database)) as connection:
                connection.execute("CREATE TABLE docs(document_id VARCHAR, content VARCHAR)")
                connection.execute("INSERT INTO docs VALUES ('one', 'One document body.')")
            old_cwd = Path.cwd()
            try:
                os.chdir(root)
                result, stdout, stderr = self.run_cli(
                    [
                        "plan",
                        str(database),
                        "--relation",
                        "docs",
                        "--source-id",
                        "stable-docs",
                        "--state-root",
                        str(root / "state"),
                        "--no-progress",
                        "--json",
                    ]
                )
            finally:
                os.chdir(old_cwd)

            self.assertEqual(result, 0, stderr)
            payload = json.loads(stdout)
            expected = Path("artifacts/site-crawls/duckdb-stable-docs")
            self.assertEqual(payload["out_dir"], str(expected))
            self.assertTrue((root / expected / "plan.json").is_file())
            self.assertFalse((root / "artifacts/site-crawls/duckdb-stable-docs-plan").exists())


if __name__ == "__main__":
    unittest.main()
