Status: recorded
Created: 2026-07-22
Updated: 2026-07-22
Relates-To: .10x/tickets/done/2026-07-22-validate-public-fineweb-duckdb-indexing.md, .10x/specs/duckdb-document-relation-indexing.md

# Public FineWeb DuckDB indexing validation

## What was observed

A current public FineWeb Parquet shard was queried through upstream DuckDB 1.5.4 and three rows were materialized into an external temporary DuckDB `documents` table. Buoy planned all three documents into four chunks. Generated pages and chunks contained recognizable public content, and an exact recursive grep found no occurrence of the local source database path. After the source database was deleted, saved-plan apply dry-run integrity verification passed without credentials, embeddings, state mutation, or turbopuffer API calls.

Key results:

```text
source URL: https://huggingface.co/datasets/HuggingFaceFW/fineweb/resolve/main/sample/10BT/000_00000.parquet
reported public shard size: 2,147,292,183 bytes
DuckDB version: 1.5.4
materialized documents: 3
total materialized content: 4,620 characters
Buoy documents generated: 3
Buoy chunks generated: 4
Buoy rows to upsert: 4
artifact hash: b07b5e20dec5cef533fcc9d4af66a769233014af2258e2fe43246b7d133aa562
apply artifact_verified: true
apply dry_run: true
apply api_calls_occurred: false
apply embeddings_generated: 0
apply rows_upserted: 0
apply state_updated: false
```

The three selected source records were:

```text
<urn:uuid:0000138d-9831-41c1-99e3-93409287c322> | 2,051 chars | newsok.com article
<urn:uuid:00001606-adf3-4779-8006-9d9d324b64b8> |   972 chars | businessinsider.com.au market update
<urn:uuid:00001659-41b8-457e-bef7-3d1410bd26b0> | 1,597 chars | ridgelineapps.com page
```

## Procedure

All data, generated artifacts, command captures, and state paths were outside the repository under:

```text
/tmp/buoy-fineweb-validation-20260722
```

### Discover and inspect the public Parquet source

The initially guessed API path with an extra `data/` component returned HTTP 404:

```bash
curl -fsSL 'https://huggingface.co/api/datasets/HuggingFaceFW/fineweb/tree/main/data/sample/10BT?recursive=false&expand=false'
```

The current public FineWeb sample path was found with:

```bash
curl -fsSL 'https://huggingface.co/api/datasets/HuggingFaceFW/fineweb/tree/main/sample/10BT?recursive=false&expand=false' \
  | python3 -c 'import json,sys; data=json.load(sys.stdin); [print(x.get("path"), x.get("size"), (x.get("lfs") or {}).get("size")) for x in data[:12]]'
```

Relevant output:

```text
sample/10BT/000_00000.parquet 2147292183 2147292183
```

A first Python standard-library API request also hit the local Python installation's CA verification error. `curl` and DuckDB's `httpfs` extension successfully verified and accessed Hugging Face, so no TLS verification was disabled. Schema inspection used upstream DuckDB/Python:

```bash
uv run python - <<'PY'
import duckdb
url = 'https://huggingface.co/datasets/HuggingFaceFW/fineweb/resolve/main/sample/10BT/000_00000.parquet'
con = duckdb.connect()
con.execute('INSTALL httpfs')
con.execute('LOAD httpfs')
print('duckdb_version', duckdb.__version__)
for row in con.execute('SELECT name, type FROM parquet_schema(?) WHERE name IS NOT NULL', [url]).fetchall():
    print(row)
PY
```

This passed and reported the expected `text`, `id`, and `url` columns, among other FineWeb fields.

### Materialize the bounded source relation

The complete materialization command was:

```bash
TMP_ROOT=/tmp/buoy-fineweb-validation-20260722
SOURCE_URL='https://huggingface.co/datasets/HuggingFaceFW/fineweb/resolve/main/sample/10BT/000_00000.parquet'
DB="$TMP_ROOT/fineweb-sample.duckdb"
uv run python - "$DB" "$SOURCE_URL" <<'PY' | tee "$TMP_ROOT/materialize.log"
import sys, duckdb
path, url = sys.argv[1:]
con = duckdb.connect(path)
con.execute('INSTALL httpfs')
con.execute('LOAD httpfs')
con.execute("""
CREATE TABLE documents AS
SELECT
    id::VARCHAR AS document_id,
    COALESCE(NULLIF(url::VARCHAR, ''), 'FineWeb document ' || id::VARCHAR) AS title,
    text::VARCHAR AS content
FROM read_parquet(?)
WHERE text IS NOT NULL AND trim(text::VARCHAR) <> ''
ORDER BY id::VARCHAR
LIMIT 3
""", [url])
print('source_url:', url)
print('duckdb_version:', duckdb.__version__)
print('document_count:', con.execute('SELECT count(*) FROM documents').fetchone()[0])
print('total_content_chars:', con.execute('SELECT sum(length(content)) FROM documents').fetchone()[0])
for row in con.execute("SELECT document_id, title, length(content), substr(replace(content, chr(10), ' '), 1, 120) FROM documents ORDER BY document_id").fetchall():
    print('sample:', repr(row))
con.close()
PY
```

This passed. The resulting source database was 524 KiB and contained exactly three nonblank public documents. Buoy did not perform ingestion; it only read the already-shaped `documents` relation.

### Create the saved plan

The feature worktree CLI was run with explicit temporary output and state roots:

```bash
TMP_ROOT=/tmp/buoy-fineweb-validation-20260722
DB="$TMP_ROOT/fineweb-sample.duckdb"
OUT="$TMP_ROOT/output"
STATE="$TMP_ROOT/state"
uv run buoy plan "$DB" \
  --relation documents \
  --source-id public-fineweb-sample \
  --out-dir "$OUT" \
  --state-root "$STATE" \
  --max-pages 3 \
  --max-chunks 50 \
  --json \
  --no-progress | tee "$TMP_ROOT/plan-command.json"
```

This passed and wrote the explicit saved plan path:

```text
/tmp/buoy-fineweb-validation-20260722/output/plan.json
```

Generated artifact paths were:

```text
/tmp/buoy-fineweb-validation-20260722/output/plan.json
/tmp/buoy-fineweb-validation-20260722/output/summary.json
/tmp/buoy-fineweb-validation-20260722/output/manifest.json
/tmp/buoy-fineweb-validation-20260722/output/chunks.jsonl
/tmp/buoy-fineweb-validation-20260722/output/pages/document-6e4540490465a6165c78729a.md
/tmp/buoy-fineweb-validation-20260722/output/pages/document-b173d8026462e32e35fdf427.md
/tmp/buoy-fineweb-validation-20260722/output/pages/document-e0d2b44ed9b954c4c4ff9322.md
```

Inspection counted three manifest pages, four manifest chunks, four `chunks.jsonl` records, and three Markdown page files. Samples included actual FineWeb text beginning `Stocks are higher, but nearly unchanged...`, `In mid-2008, Michael asked...`, and `Ridgeline isn’t just another solution...` under logical `duckdb://public-fineweb-sample/...` URIs.

The exact source-path leakage check was:

```bash
DB=/tmp/buoy-fineweb-validation-20260722/fineweb-sample.duckdb
OUT=/tmp/buoy-fineweb-validation-20260722/output
if grep -R -n -F -- "$DB" "$OUT"; then
  echo 'FAIL: source database path found in generated artifacts' >&2
  exit 1
else
  rc=$?
  if [ "$rc" -eq 1 ]; then
    echo "PASS: no generated artifact contains $DB"
  else
    exit "$rc"
  fi
fi
```

It passed with no matches. The first inspection helper attempted the nonexistent `plan['source']` key and failed with `KeyError: 'source'`; it did not mutate artifacts. The corrected inspection read `plan['base_url']` and passed.

### Delete the source and verify the saved plan

The source database was deleted and absence was asserted before apply dry-run:

```bash
TMP_ROOT=/tmp/buoy-fineweb-validation-20260722
DB="$TMP_ROOT/fineweb-sample.duckdb"
PLAN="$TMP_ROOT/output/plan.json"
STATE="$TMP_ROOT/state"
rm -- "$DB"
test ! -e "$DB"
uv run buoy apply \
  --dry-run \
  --plan "$PLAN" \
  --state-root "$STATE" \
  --json \
  --no-progress | tee "$TMP_ROOT/apply-dry-run.json"
```

This passed with `artifact_verified=true`, `dry_run=true`, `rows_to_upsert=4`, `api_calls_occurred=false`, `turbopuffer_api_calls=false`, `credentials_required=false`, `embeddings_generated=0`, `rows_upserted=0`, and `state_updated=false`.

## What this supports

This directly supports every acceptance criterion in `.10x/tickets/done/2026-07-22-validate-public-fineweb-duckdb-indexing.md` and acceptance scenario 4 plus the valid-source portion of scenario 1 in `.10x/specs/duckdb-document-relation-indexing.md`:

- public FineWeb data was shaped upstream into DuckDB without Buoy ingestion;
- Buoy planned real documents and chunks;
- review artifacts contained real public text and excluded the local database filepath; and
- saved-plan dry-run verification remained independent of the deleted source database.

## Limits

Only three documents and four chunks were materialized and planned; this was intentionally not a throughput or scale benchmark. The public source shard is about 2.15 GB, but DuckDB queried it remotely and only the three selected rows were persisted locally; no full shard file was stored in the temporary directory. The selected web text may contain source-dataset quality or sensitivity issues typical of Common Crawl-derived corpora and was inspected only enough to prove real content. No live apply, embeddings, credentials, remote catalog read/write, turbopuffer API call, or repository implementation/documentation/test change occurred. Temporary command captures and saved plan artifacts remain under `/tmp/buoy-fineweb-validation-20260722`; the source DuckDB file does not.
