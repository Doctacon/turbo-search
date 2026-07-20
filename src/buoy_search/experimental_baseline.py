"""Fail-closed executor for the one ratified experimental Buoy baseline.

This module is intentionally not connected to the ordinary CLI or apply path.
Its public executor accepts local/model/state hooks so dry validation can use
credential-free fakes. The default provider factory is inert until explicitly
called and constructs the locked SDK with retries disabled.
"""

from __future__ import annotations

from contextlib import AbstractContextManager
from dataclasses import asdict, dataclass, field
import hashlib
from importlib.metadata import version as package_version
import math
import os
from pathlib import Path
import re
from typing import Any, Callable, Mapping, Protocol, Sequence

from buoy_search.applied_state import AppliedState, AppliedStateRow
from buoy_search.apply import VerifiedApplyPlan
from buoy_search.catalog import (
    NamespaceCard,
    ROUTING_DIMENSIONS,
    ROUTING_MODEL,
    ROUTING_MODEL_REVISION,
    card_to_dict,
    parse_card,
)
from buoy_search.plan_artifacts import (
    GENERIC_SITE_TURBOPUFFER_SCHEMA,
    build_generic_site_row,
    stable_hash,
)
from buoy_search.remote_catalog import (
    DISTANCE_METRIC,
    REMOTE_CARD_ATTRIBUTES,
    REMOTE_CATALOG_NAMESPACE,
    REMOTE_CATALOG_SCHEMA,
    STRONG_CONSISTENCY,
    card_from_remote_row,
    card_to_remote_row,
    remote_card_id,
    validate_remote_schema,
)

JsonObject = dict[str, Any]
REGION = "gcp-us-central1"
PLAN_ID = "plan_b6c5d128295f442f"
ARTIFACT_HASH = "b6c5d128295f442fcae21472c9bcb037ecb44101ca648115e8f666ba59a6f0ce"
SOURCE_REPOSITORY = "Doctacon/buoy-search"
SOURCE_COMMIT = "fcb7abbe1652d2eab4ee23816b6d992d893603ac"
SOURCE_URI = "https://github.com/Doctacon/buoy-search"
SITE_ID = "github-doctacon-buoy-search"
TARGET_NAMESPACE = "github-doctacon-buoy-search-v1"
MODEL = "BAAI/bge-small-en-v1.5"
MODEL_REVISION = "5c38ec7c405ec4b44b94cc5a9bb96e735b38267a"
MODEL_PRECISION = "float32"
CACHE_MANIFEST_HASH = "5f783ebce23b6ac957d2741399b46e19502b1751acfd3c744b8c41103b138f35"
README_HASH = "ddb964361a55c6e5dfca6361615854b260c9c960205d04c7520151aaa1d75837"
CONTENT_ROWS = 903
CONTENT_BATCH_SIZES = (64,) * 14 + (7,)
MAX_ATTEMPTS = 26
MAX_WRITE_ROW_POSITIONS = 904
MAX_RETURNED_ROW_POSITIONS = 1817
SDK_VERSION = "2.4.0"

CONTENT_SCHEMA: JsonObject = {
    **GENERIC_SITE_TURBOPUFFER_SCHEMA,
    "vector": {
        **GENERIC_SITE_TURBOPUFFER_SCHEMA["vector"],
        "ann": {"distance_metric": DISTANCE_METRIC},
    },
}
CONTENT_ATTRIBUTES = tuple(name for name in CONTENT_SCHEMA if name != "vector")


class ExperimentalBaselineError(RuntimeError):
    """Raised on any mismatch while preserving secret-free attempt evidence."""

    def __init__(self, message: str, evidence: JsonObject | None = None) -> None:
        super().__init__(message)
        self.evidence = evidence


class DefinitiveProviderError(RuntimeError):
    """Injected provider failure whose remote outcome is known to be failed."""


class NamespaceResource(Protocol):
    def metadata(self, **kwargs: object) -> object: ...
    def query(self, **kwargs: object) -> object: ...
    def write(self, **kwargs: object) -> object: ...


@dataclass(frozen=True)
class CacheAttestation:
    revision: str
    manifest_sha256: str
    readme_sha256: str
    license: str
    license_statement_present: bool
    file_count: int


@dataclass(frozen=True)
class PreparedBaseline:
    """All model-derived values validated before credential access."""

    rows: tuple[JsonObject, ...]
    card: NamespaceCard
    next_state: AppliedState
    model: str
    model_revision: str
    precision: str
    dimensions: int
    normalized: bool
    pooling: str


@dataclass(frozen=True)
class ProviderResources:
    target: NamespaceResource
    catalog: NamespaceResource
    sdk_version: str
    max_retries: int
    wrapper_retries_disabled: bool = True
    fallbacks_disabled: bool = True
    pagination_disabled: bool = True
    simulated: bool = False


@dataclass(frozen=True)
class LocalEffects:
    """Plan-bound local effects; production callers bind existing primitives."""

    lock: Callable[[], AbstractContextManager[None]]
    validate_preconditions: Callable[[VerifiedApplyPlan], None]
    create_pending: Callable[[PreparedBaseline], None]
    commit_state: Callable[[PreparedBaseline], None]
    remove_pending: Callable[[], None]
    simulated: bool = False


@dataclass(frozen=True)
class Slot:
    number: int
    phase: str
    resource: str
    operation_number: int
    kind: str
    requested_rows: int | None = None
    top_k: int | None = None


@dataclass
class Attempt:
    slot: Slot
    status: str = "attempted"
    rows_affected: int | None = None
    rows_affected_present: bool = False
    returned_rows: int = 0
    billing: JsonObject | None = None
    billing_present: bool = False
    request_identity: str | None = None
    request_identity_present: bool = False
    affected_ids: list[str] | None = None
    affected_ids_present: bool = False
    error: str | None = None
    cumulative_physical_attempts: int = 0
    cumulative_write_row_positions: int = 0
    cumulative_returned_row_positions: int = 0


SLOTS: tuple[Slot, ...] = (
    Slot(1, "target_preflight_metadata", TARGET_NAMESPACE, 1, "read"),
    Slot(2, "target_empty_check", TARGET_NAMESPACE, 1, "read", top_k=1),
    Slot(3, "catalog_preflight_metadata", REMOTE_CATALOG_NAMESPACE, 1, "read"),
    Slot(4, "catalog_card_preflight", REMOTE_CATALOG_NAMESPACE, 1, "read", top_k=2),
    Slot(5, "catalog_card_preflight", REMOTE_CATALOG_NAMESPACE, 2, "read", top_k=2),
    *(Slot(6 + index, "content_write", TARGET_NAMESPACE, index + 1, "write", requested_rows=size)
      for index, size in enumerate(CONTENT_BATCH_SIZES)),
    Slot(21, "target_postwrite_metadata", TARGET_NAMESPACE, 1, "read"),
    Slot(22, "target_postwrite_verification", TARGET_NAMESPACE, 1, "read", top_k=904),
    Slot(23, "target_postwrite_verification", TARGET_NAMESPACE, 2, "read", top_k=904),
    Slot(24, "catalog_conditional_write", REMOTE_CATALOG_NAMESPACE, 1, "write", requested_rows=1),
    Slot(25, "catalog_postwrite_verification", REMOTE_CATALOG_NAMESPACE, 1, "read", top_k=2),
    Slot(26, "catalog_postwrite_verification", REMOTE_CATALOG_NAMESPACE, 2, "read", top_k=2),
)


@dataclass
class _Ledger:
    attempts: dict[int, Attempt] = field(default_factory=dict)
    physical_attempts: int = 0
    write_row_positions: int = 0
    returned_row_positions: int = 0
    delete_attempts: int = 0

    def invoke(self, slot_number: int, call: Callable[[], object]) -> JsonObject:
        slot = SLOTS[slot_number - 1]
        if slot.number != slot_number or slot_number in self.attempts:
            raise ExperimentalBaselineError("attempt slot reuse or reassignment is forbidden", self.evidence())
        self.physical_attempts += 1
        self.write_row_positions += slot.requested_rows or 0
        attempt = Attempt(
            slot=slot,
            cumulative_physical_attempts=self.physical_attempts,
            cumulative_write_row_positions=self.write_row_positions,
            cumulative_returned_row_positions=self.returned_row_positions,
        )
        # Accounting exists before the physical call.
        self.attempts[slot_number] = attempt
        self._check_budgets()
        try:
            response = call()
        except BaseException as exc:
            attempt.status = "failed" if isinstance(exc, DefinitiveProviderError) else "indeterminate"
            attempt.error = _safe_error(exc)
            raise ExperimentalBaselineError(
                f"provider attempt {slot_number} did not complete ({attempt.error})", self.evidence()
            ) from None
        try:
            payload = _plain_response(response)
            response_errors = _capture_response(
                attempt, payload, require_rows_affected=slot.kind == "write"
            )
            self.returned_row_positions += attempt.returned_rows
            attempt.cumulative_returned_row_positions = self.returned_row_positions
            self._check_budgets()
            if response_errors:
                raise ExperimentalBaselineError("; ".join(response_errors))
            attempt.status = "succeeded"
            return payload
        except ExperimentalBaselineError as exc:
            attempt.status = "failed"
            attempt.error = str(exc)
            raise ExperimentalBaselineError(
                f"provider attempt {slot_number} returned a malformed response: {exc}", self.evidence()
            ) from None

    def mark_unused(self, slot_number: int) -> None:
        if slot_number in self.attempts:
            raise ExperimentalBaselineError("an attempted slot cannot become unused", self.evidence())

    def _check_budgets(self) -> None:
        if self.physical_attempts > MAX_ATTEMPTS:
            raise ExperimentalBaselineError("physical-attempt ceiling exceeded", self.evidence())
        if self.write_row_positions > MAX_WRITE_ROW_POSITIONS:
            raise ExperimentalBaselineError("write-row-position ceiling exceeded", self.evidence())
        if self.returned_row_positions > MAX_RETURNED_ROW_POSITIONS:
            raise ExperimentalBaselineError("returned-row-position ceiling exceeded", self.evidence())
        if self.delete_attempts:
            raise ExperimentalBaselineError("delete attempts are forbidden", self.evidence())

    def evidence(self, *, success: bool = False) -> JsonObject:
        mapped: list[JsonObject] = []
        for slot in SLOTS:
            attempt = self.attempts.get(slot.number)
            if attempt is None:
                mapped.append({**asdict(slot), "status": "unused"})
            else:
                value = asdict(attempt)
                value["slot"] = asdict(slot)
                mapped.append(value)
        return {
            "executor": "experimental_buoy_baseline",
            "success": success,
            "approval_a_granted_by_executor": False,
            "approval_b_granted_by_executor": False,
            "dollar_cost": "unknown",
            "required_sdk_version": SDK_VERSION,
            "required_max_retries": 0,
            "limits": {
                "physical_attempts": MAX_ATTEMPTS,
                "write_row_positions": MAX_WRITE_ROW_POSITIONS,
                "returned_row_positions": MAX_RETURNED_ROW_POSITIONS,
                "delete_attempts": 0,
            },
            "read_attempts": sum(
                attempt.slot.kind == "read" for attempt in self.attempts.values()
            ),
            "write_attempts": sum(
                attempt.slot.kind == "write" for attempt in self.attempts.values()
            ),
            "physical_attempts": self.physical_attempts,
            "write_row_positions": self.write_row_positions,
            "returned_row_positions": self.returned_row_positions,
            "delete_attempts": self.delete_attempts,
            "slots": mapped,
        }


def validate_model_cache(cache_root: Path) -> CacheAttestation:
    """Hash the exact immutable snapshot without importing/loading a model."""

    root = cache_root.expanduser().resolve(strict=True)
    ref = root / "refs" / "main"
    if ref.read_text(encoding="utf-8").strip() != MODEL_REVISION:
        raise ExperimentalBaselineError("model cache refs/main revision mismatch")
    snapshot = root / "snapshots" / MODEL_REVISION
    if not snapshot.is_dir():
        raise ExperimentalBaselineError("immutable model snapshot is missing")
    entries: list[JsonObject] = []
    for path in sorted((item for item in snapshot.rglob("*") if item.is_file()), key=lambda item: str(item.relative_to(snapshot))):
        data = path.read_bytes()
        entries.append({
            "path": str(path.relative_to(snapshot)),
            "size": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        })
    manifest_hash = stable_hash(entries)
    readme = snapshot / "README.md"
    readme_bytes = readme.read_bytes()
    readme_text = readme_bytes.decode("utf-8")
    attestation = CacheAttestation(
        revision=MODEL_REVISION,
        manifest_sha256=manifest_hash,
        readme_sha256=hashlib.sha256(readme_bytes).hexdigest(),
        license="mit" if re.search(r"(?m)^license:\s*mit\s*$", readme_text) else "unknown",
        license_statement_present="FlagEmbedding is licensed under the MIT License" in readme_text,
        file_count=len(entries),
    )
    validate_cache_attestation(attestation)
    return attestation


def validate_cache_attestation(value: CacheAttestation) -> None:
    if value.revision != MODEL_REVISION:
        raise ExperimentalBaselineError("model revision mismatch")
    if value.manifest_sha256 != CACHE_MANIFEST_HASH:
        raise ExperimentalBaselineError("full model cache manifest hash mismatch")
    if value.readme_sha256 != README_HASH:
        raise ExperimentalBaselineError("model README hash mismatch")
    if value.license != "mit" or not value.license_statement_present:
        raise ExperimentalBaselineError("immutable model README does not prove the MIT license")
    if value.file_count != 12:
        raise ExperimentalBaselineError("immutable model cache must contain exactly 12 resolved files")


def validate_immutable_plan(verified: VerifiedApplyPlan) -> None:
    """Validate every local plan/state identity before model or credential work."""

    plan = verified.plan
    manifest = verified.manifest
    exact = {
        "plan_id": PLAN_ID,
        "artifact_hash": ARTIFACT_HASH,
        "namespace": TARGET_NAMESPACE,
        "embedding_model": MODEL,
        "embedding_precision": MODEL_PRECISION,
    }
    for field_name, expected in exact.items():
        if plan.get(field_name) != expected:
            raise ExperimentalBaselineError(f"immutable plan {field_name} mismatch")
    if (
        manifest.namespace != TARGET_NAMESPACE
        or manifest.site_id != SITE_ID
        or manifest.base_url != SOURCE_URI
        or len(manifest.chunks) != CONTENT_ROWS
    ):
        raise ExperimentalBaselineError("immutable manifest source/namespace/row count mismatch")
    row_ids = [chunk.row_id for chunk in manifest.chunks]
    if len(set(row_ids)) != CONTENT_ROWS or any(not value for value in row_ids):
        raise ExperimentalBaselineError("immutable manifest must contain 903 unique non-empty row IDs")
    for record in [*manifest.pages, *manifest.chunks]:
        metadata = record.source_metadata
        if metadata.get("repo_full_name") != SOURCE_REPOSITORY:
            raise ExperimentalBaselineError("immutable source repository mismatch")
        if metadata.get("commit_sha") != SOURCE_COMMIT:
            raise ExperimentalBaselineError("immutable source commit mismatch")
    if (
        verified.state.rows
        or not verified.state.first_apply
        or verified.state.site_id != manifest.site_id
        or verified.state.namespace != TARGET_NAMESPACE
        or verified.state.base_url != manifest.base_url
    ):
        raise ExperimentalBaselineError("local applied-state ledger is not exactly empty and compatible")
    diff = verified.diff
    if (
        not diff.first_apply
        or diff.rows_to_upsert != CONTENT_ROWS
        or diff.chunks_to_embed != CONTENT_ROWS
        or diff.chunks_unchanged != 0
        or diff.stale_rows != 0
        or diff.retained_stale_rows != 0
        or diff.stale_row_records
        or diff.retained_stale_row_records
        or len(diff.rows_to_upsert_records) != CONTENT_ROWS
    ):
        raise ExperimentalBaselineError("immutable first-apply diff contains incompatible or stale intent")


def validate_prepared(verified: VerifiedApplyPlan, prepared: PreparedBaseline) -> None:
    if (
        prepared.model != MODEL
        or prepared.model_revision != MODEL_REVISION
        or prepared.precision != MODEL_PRECISION
        or prepared.dimensions != ROUTING_DIMENSIONS
        or not prepared.normalized
        or prepared.pooling != "cls"
    ):
        raise ExperimentalBaselineError("prepared model contract mismatch")
    if len(prepared.rows) != CONTENT_ROWS:
        raise ExperimentalBaselineError("prepared content row count mismatch")
    chunks = list(verified.manifest.chunks)
    expected_ids = [chunk.row_id for chunk in chunks]
    actual_ids: list[str] = []
    for index, (chunk, row) in enumerate(zip(chunks, prepared.rows, strict=True)):
        if not isinstance(row, dict):
            raise ExperimentalBaselineError(f"prepared row {index} is not an object")
        vector = _validate_vector(row.get("vector"), label=f"content row {index}")
        expected = build_generic_site_row(
            chunk, vector, plan_id=PLAN_ID, applied_at=prepared.next_state.updated_at
        )
        if row != expected:
            raise ExperimentalBaselineError(f"prepared row {index} attributes mismatch")
        actual_ids.append(str(row.get("id")))
    if actual_ids != expected_ids or len(set(actual_ids)) != CONTENT_ROWS:
        raise ExperimentalBaselineError("prepared content IDs/order mismatch")
    card = parse_card(card_to_dict(prepared.card, include_vector=True))
    exact_card_values = {
        "namespace": TARGET_NAMESPACE,
        "enabled": True,
        "source_kind": "github_repo",
        "source_uri": SOURCE_URI,
        "site_id": SITE_ID,
        "title": SOURCE_REPOSITORY,
        "summary": f"Public GitHub repository {SOURCE_REPOSITORY} indexed from {SOURCE_URI}.",
        "aliases": ["buoy-search"],
        "tags": ["github", "repository"],
        "semantic_origin": "generated",
        "region": REGION,
        "embedding_model": MODEL,
        "embedding_precision": MODEL_PRECISION,
        "vector_dimensions": ROUTING_DIMENSIONS,
        "routing_model": ROUTING_MODEL,
        "routing_model_revision": ROUTING_MODEL_REVISION,
        "last_plan_id": PLAN_ID,
        "ranking_mode": "file",
        "ranking_profile": "repo_code",
        "ranking_pool": 100,
        "ranking_aggregation": "adaptive_sum_3",
    }
    if any(getattr(card, name) != value for name, value in exact_card_values.items()):
        raise ExperimentalBaselineError("prepared catalog card compatibility mismatch")
    if not card.last_apply_id:
        raise ExperimentalBaselineError("prepared catalog card is missing apply lineage")
    state = prepared.next_state
    expected_state_rows = [
        AppliedStateRow(
            row_id=chunk.row_id,
            canonical_url=chunk.canonical_url,
            page_hash=chunk.page_hash,
            chunk_hash=chunk.chunk_hash,
            embedding_text_hash=chunk.embedding_text_hash,
            plan_id=PLAN_ID,
            applied_at=state.updated_at,
            status="active",
        )
        for chunk in sorted(chunks, key=lambda item: item.row_id)
    ]
    if (
        state.schema_version != verified.state.schema_version
        or state.site_id != SITE_ID
        or state.namespace != TARGET_NAMESPACE
        or state.base_url != SOURCE_URI
        or not state.updated_at
        or state.last_plan_id != PLAN_ID
        or state.last_apply_id != card.last_apply_id
        or state.rows != expected_state_rows
    ):
        raise ExperimentalBaselineError("prepared local applied-state mismatch")


def create_provider_resources(*, api_key: str, region: str, max_retries: int) -> ProviderResources:
    """Construct exactly one locked Turbopuffer 2.4.0 client with no retries."""

    if region != REGION or max_retries != 0:
        raise ExperimentalBaselineError("provider construction requires exact region and max_retries=0")
    if package_version("turbopuffer") != SDK_VERSION:
        raise ExperimentalBaselineError("locked turbopuffer SDK version mismatch")
    try:
        import turbopuffer
        client = turbopuffer.Turbopuffer(api_key=api_key, region=region, max_retries=0)
    except Exception as exc:
        raise ExperimentalBaselineError(f"provider client construction failed ({_safe_error(exc)})") from None
    class DirectResource:
        def __init__(self, resource: object) -> None:
            self._resource = resource

        def metadata(self, **kwargs: object) -> object:
            try:
                return self._resource.metadata(**kwargs)  # type: ignore[attr-defined]
            except turbopuffer.NotFoundError:
                # A locked SDK 404 is the one unambiguous namespace-absent result.
                return {"namespace_absent": True}

        def query(self, **kwargs: object) -> object:
            return self._resource.query(**kwargs)  # type: ignore[attr-defined]

        def write(self, **kwargs: object) -> object:
            return self._resource.write(**kwargs)  # type: ignore[attr-defined]

    return ProviderResources(
        target=DirectResource(client.namespace(TARGET_NAMESPACE)),
        catalog=DirectResource(client.namespace(REMOTE_CATALOG_NAMESPACE)),
        sdk_version=SDK_VERSION,
        max_retries=0,
    )


def execute_experimental_baseline(
    verified: VerifiedApplyPlan,
    *,
    cache_attestation: CacheAttestation,
    prepare: Callable[[VerifiedApplyPlan], PreparedBaseline],
    credential_reader: Callable[[], str],
    provider_factory: Callable[..., ProviderResources],
    local_effects: LocalEffects,
    approval_a_granted: bool = False,
    simulation: bool = False,
) -> JsonObject:
    """Execute the bounded operation; callers must separately possess Approval A.

    No CLI routes here. Tests inject every external/model/local side effect.
    """

    if not approval_a_granted and not simulation:
        raise ExperimentalBaselineError("a separately granted Approval A is required for non-simulated execution")
    if approval_a_granted and simulation:
        raise ExperimentalBaselineError("simulation cannot claim live Approval A")
    if local_effects.simulated != simulation:
        raise ExperimentalBaselineError("local-effect simulation attestation mismatch")
    with local_effects.lock():
        return _execute_locked(
            verified,
            cache_attestation=cache_attestation,
            prepare=prepare,
            credential_reader=credential_reader,
            provider_factory=provider_factory,
            local_effects=local_effects,
            simulation=simulation,
        )


def _execute_locked(
    verified: VerifiedApplyPlan,
    *,
    cache_attestation: CacheAttestation,
    prepare: Callable[[VerifiedApplyPlan], PreparedBaseline],
    credential_reader: Callable[[], str],
    provider_factory: Callable[..., ProviderResources],
    local_effects: LocalEffects,
    simulation: bool,
) -> JsonObject:
    ledger = _Ledger()
    pending_created = False
    state_committed = False
    card_verified = False
    provider_attested = False
    try:
        validate_immutable_plan(verified)
        local_effects.validate_preconditions(verified)
        validate_cache_attestation(cache_attestation)
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"
        prepared = prepare(verified)
        validate_prepared(verified, prepared)
        credential = credential_reader()
        if not isinstance(credential, str) or not credential:
            raise ExperimentalBaselineError("TURBOPUFFER_API_KEY is required for an approved operation")
        provider = provider_factory(api_key=credential, region=REGION, max_retries=0)
        _validate_provider(provider, simulation=simulation)
        provider_attested = True

        target_absent = _target_preflight(ledger, provider.target)
        if target_absent:
            ledger.mark_unused(2)
        existing_card = _catalog_preflight(ledger, provider.catalog, prepared.card)

        local_effects.create_pending(prepared)
        pending_created = True
        for batch_number, size in enumerate(CONTENT_BATCH_SIZES, start=1):
            start = sum(CONTENT_BATCH_SIZES[: batch_number - 1])
            rows = list(prepared.rows[start : start + size])
            response = ledger.invoke(
                5 + batch_number,
                lambda rows=rows: provider.target.write(
                    distance_metric=DISTANCE_METRIC,
                    schema=CONTENT_SCHEMA,
                    upsert_rows=rows,
                    return_affected_ids=True,
                ),
            )
            _require_write_response(response, expected_rows=size)

        metadata = ledger.invoke(21, lambda: provider.target.metadata())
        _validate_content_metadata(metadata, allow_absent=False)
        first_rows = _target_verification_read(ledger, provider.target, 22)
        second_rows = _target_verification_read(ledger, provider.target, 23)
        _validate_target_rows(first_rows, prepared.rows)
        _validate_target_rows(second_rows, prepared.rows)
        if first_rows != second_rows:
            raise ExperimentalBaselineError("target verification order/content changed between strong reads")

        card_row = card_to_remote_row(prepared.card)
        condition = (
            ("id", "Eq", None)
            if existing_card is None
            else ("card_revision", "Eq", existing_card.card_revision)
        )
        response = ledger.invoke(
            24,
            lambda: provider.catalog.write(
                distance_metric=DISTANCE_METRIC,
                schema=REMOTE_CATALOG_SCHEMA,
                upsert_rows=[card_row],
                upsert_condition=condition,
                return_affected_ids=True,
            ),
        )
        _require_write_response(response, expected_rows=1, expected_ids=[str(card_row["id"])])
        first_card = _card_read(ledger, provider.catalog, 25, allow_missing=False)
        second_card = _card_read(ledger, provider.catalog, 26, allow_missing=False)
        expected_card = card_to_dict(prepared.card, include_vector=True)
        if first_card is None or second_card is None:
            raise ExperimentalBaselineError("catalog verification did not return the intended card")
        if card_to_dict(first_card, include_vector=True) != expected_card:
            raise ExperimentalBaselineError("first catalog verification card mismatch")
        if card_to_dict(second_card, include_vector=True) != expected_card:
            raise ExperimentalBaselineError("second catalog verification card mismatch")
        if first_card.card_revision != second_card.card_revision:
            raise ExperimentalBaselineError("catalog card revision changed between strong reads")
        card_verified = True
        if ledger.physical_attempts not in {25, 26}:
            raise ExperimentalBaselineError("successful request count is outside the fixed ledger")

        local_effects.commit_state(prepared)
        state_committed = True
        local_effects.remove_pending()
        pending_created = False
        evidence = ledger.evidence(success=True)
        evidence.update({
            "provider_attested": True,
            "sdk_version": provider.sdk_version,
            "max_retries": provider.max_retries,
            "target_namespace": TARGET_NAMESPACE,
            "catalog_namespace": REMOTE_CATALOG_NAMESPACE,
            "content_rows_verified": CONTENT_ROWS,
            "card_revision": prepared.card.card_revision,
            "local_state_committed": True,
            "remote_card_verified": True,
            "pending_retained": False,
            "simulation": simulation,
        })
        return evidence
    except ExperimentalBaselineError as exc:
        evidence = exc.evidence or ledger.evidence()
        evidence["provider_attested"] = provider_attested
        evidence["pending_retained"] = pending_created
        evidence["local_state_committed"] = state_committed
        evidence["remote_card_verified"] = card_verified
        evidence["card_success"] = card_verified
        evidence["simulation"] = simulation
        exc.evidence = evidence
        raise
    except BaseException as exc:
        evidence = ledger.evidence()
        evidence.update({
            "provider_attested": provider_attested,
            "pending_retained": pending_created,
            "local_state_committed": state_committed,
            "remote_card_verified": card_verified,
            "card_success": card_verified,
            "simulation": simulation,
        })
        raise ExperimentalBaselineError(f"experimental baseline aborted ({_safe_error(exc)})", evidence) from None


def _validate_provider(provider: ProviderResources, *, simulation: bool) -> None:
    if (
        provider.sdk_version != SDK_VERSION
        or provider.max_retries != 0
        or not provider.wrapper_retries_disabled
        or not provider.fallbacks_disabled
        or not provider.pagination_disabled
        or provider.simulated != simulation
    ):
        raise ExperimentalBaselineError("provider resources cannot attest zero retry/fallback/pagination")


def _target_preflight(ledger: _Ledger, resource: NamespaceResource) -> bool:
    metadata = ledger.invoke(1, lambda: resource.metadata())
    if metadata.get("namespace_absent") is True:
        if "schema" in metadata or "distance_metric" in metadata:
            raise ExperimentalBaselineError("target namespace absence result is ambiguous")
        return True
    _validate_content_metadata(metadata, allow_absent=False)
    response = ledger.invoke(
        2,
        lambda: resource.query(
            rank_by=("id", "asc"), top_k=1, include_attributes=["id"],
            consistency=dict(STRONG_CONSISTENCY),
        ),
    )
    if response["rows"]:
        raise ExperimentalBaselineError("target namespace is not empty")
    return False


def _catalog_preflight(
    ledger: _Ledger, resource: NamespaceResource, intended: NamespaceCard
) -> NamespaceCard | None:
    metadata = ledger.invoke(3, lambda: resource.metadata())
    validate_remote_schema(metadata)
    first = _card_read(ledger, resource, 4, allow_missing=True)
    second = _card_read(ledger, resource, 5, allow_missing=True)
    if (first is None) != (second is None):
        raise ExperimentalBaselineError("catalog card presence changed between strong reads")
    if first is None:
        return None
    assert second is not None
    if card_to_dict(first, include_vector=True) != card_to_dict(second, include_vector=True):
        raise ExperimentalBaselineError("catalog card changed between strong reads")
    _validate_existing_card_compatibility(first, intended)
    return first


def _validate_existing_card_compatibility(existing: NamespaceCard, intended: NamespaceCard) -> None:
    compatible_fields = (
        "namespace", "enabled", "source_kind", "source_uri", "site_id", "title", "summary",
        "aliases", "tags", "semantic_origin", "region", "embedding_model",
        "embedding_precision", "vector_dimensions", "plan_schema_version", "ranking_mode",
        "ranking_profile", "ranking_pool", "ranking_aggregation", "routing_model",
        "routing_model_revision", "semantic_hash", "vector", "vector_hash",
    )
    if any(getattr(existing, name) != getattr(intended, name) for name in compatible_fields):
        raise ExperimentalBaselineError("existing catalog card is incompatible with the intended card")


def _target_verification_read(
    ledger: _Ledger, resource: NamespaceResource, slot: int
) -> list[JsonObject]:
    response = ledger.invoke(
        slot,
        lambda: resource.query(
            rank_by=("id", "asc"), top_k=904,
            include_attributes=[*CONTENT_ATTRIBUTES, "vector"],
            vector_encoding="float", consistency=dict(STRONG_CONSISTENCY),
        ),
    )
    return response["rows"]


def _validate_target_rows(actual: Sequence[JsonObject], expected: Sequence[JsonObject]) -> None:
    if len(actual) != CONTENT_ROWS:
        raise ExperimentalBaselineError("target verification must return exactly 903 rows and no 904th row")
    ids = [row.get("id") for row in actual]
    if len(set(ids)) != CONTENT_ROWS:
        raise ExperimentalBaselineError("target verification contains duplicate IDs")
    for index, (actual_row, expected_row) in enumerate(zip(actual, expected, strict=True)):
        if set(actual_row) != set(expected_row):
            raise ExperimentalBaselineError(f"target verification row {index} fields mismatch")
        actual_attributes = {key: value for key, value in actual_row.items() if key != "vector"}
        expected_attributes = {key: value for key, value in expected_row.items() if key != "vector"}
        if actual_attributes != expected_attributes:
            raise ExperimentalBaselineError(f"target verification row {index} attributes mismatch")
        # The exact f16 namespace schema may quantize float32 inference values.
        # Compatibility therefore requires stable normalized vector shape, not
        # byte equality with the pre-write float32 values.
        _validate_vector(actual_row.get("vector"), label=f"verified content row {index}")


def _card_read(
    ledger: _Ledger,
    resource: NamespaceResource,
    slot: int,
    *,
    allow_missing: bool,
) -> NamespaceCard | None:
    row_id = remote_card_id(TARGET_NAMESPACE)
    response = ledger.invoke(
        slot,
        lambda: resource.query(
            rank_by=("id", "asc"), top_k=2, filters=("id", "Eq", row_id),
            include_attributes=list(REMOTE_CARD_ATTRIBUTES), vector_encoding="float",
            consistency=dict(STRONG_CONSISTENCY),
        ),
    )
    rows = response["rows"]
    if len(rows) > 1:
        raise ExperimentalBaselineError("exact card read returned duplicate rows")
    if not rows:
        if allow_missing:
            return None
        raise ExperimentalBaselineError("exact card read returned no row")
    return card_from_remote_row(rows[0], region=REGION)


def _validate_content_metadata(payload: Mapping[str, Any], *, allow_absent: bool) -> None:
    if payload.get("namespace_absent") is True:
        if allow_absent:
            return
        raise ExperimentalBaselineError("target namespace unexpectedly absent")
    schema = payload.get("schema")
    if _normalize_content_schema(schema) != _normalize_content_schema({
        "id": {"type": "string", "filterable": True}, **CONTENT_SCHEMA,
    }):
        raise ExperimentalBaselineError("target namespace schema mismatch")
    distance = payload.get("distance_metric")
    if distance is not None and distance != DISTANCE_METRIC:
        raise ExperimentalBaselineError("target namespace distance mismatch")


def _normalize_content_schema(value: object) -> JsonObject:
    if not isinstance(value, Mapping):
        raise ExperimentalBaselineError("target namespace metadata is missing schema")
    normalized: JsonObject = {}
    for raw_name, raw_config in value.items():
        name = str(raw_name)
        config = {"type": raw_config} if isinstance(raw_config, str) else raw_config
        if not isinstance(config, Mapping) or not isinstance(config.get("type"), str):
            raise ExperimentalBaselineError("target namespace schema contains an invalid attribute")
        type_name = str(config["type"])
        result: JsonObject = {
            "type": type_name,
            "filterable": config.get("filterable", name != "vector"),
        }
        for flag in ("full_text_search", "regex", "glob", "fuzzy", "sparse_knn"):
            if config.get(flag) not in (None, False):
                result[flag] = config[flag]
        ann = config.get("ann")
        if ann is True:
            result["ann"] = {"distance_metric": DISTANCE_METRIC}
        elif ann not in (None, False):
            if not isinstance(ann, Mapping):
                raise ExperimentalBaselineError("target namespace schema has invalid ANN config")
            result["ann"] = dict(ann)
        if config.get("embed") is not None:
            result["embed"] = config["embed"]
        normalized[name] = result
    implicit_id = normalized.pop("id", None)
    if implicit_id != {"type": "string", "filterable": True}:
        raise ExperimentalBaselineError("target namespace implicit id schema mismatch")
    return normalized


def _require_write_response(
    response: Mapping[str, Any], *, expected_rows: int, expected_ids: Sequence[str] | None = None
) -> None:
    if response.get("rows_affected") != expected_rows:
        raise ExperimentalBaselineError("successful write rows_affected mismatch")
    if expected_ids is not None:
        raw_ids = response.get("upserted_ids")
        if not isinstance(raw_ids, list) or raw_ids != list(expected_ids):
            raise ExperimentalBaselineError("successful write affected IDs mismatch")


def _capture_response(
    attempt: Attempt, payload: JsonObject, *, require_rows_affected: bool
) -> list[str]:
    errors: list[str] = []
    attempt.rows_affected_present = "rows_affected" in payload
    rows_affected = payload.get("rows_affected")
    if attempt.rows_affected_present and (type(rows_affected) is not int or rows_affected < 0):
        errors.append("rows_affected must be an exact non-negative integer")
    else:
        attempt.rows_affected = rows_affected if attempt.rows_affected_present else None
    if require_rows_affected and not attempt.rows_affected_present:
        errors.append("successful write omitted rows_affected")

    rows = payload.get("rows", [])
    if not isinstance(rows, list):
        errors.append("response rows must be an array")
    else:
        attempt.returned_rows = len(rows)
        if attempt.slot.top_k is not None and len(rows) > attempt.slot.top_k:
            errors.append("read returned more rows than top_k")

    attempt.billing_present = "billing" in payload
    billing = payload.get("billing")
    if attempt.billing_present:
        if not isinstance(billing, Mapping):
            errors.append("billing must be an object when present")
        else:
            attempt.billing = _redact_mapping(billing)

    identity = payload.get("request_id", payload.get("request_identity"))
    attempt.request_identity_present = identity is not None
    if identity is not None:
        if not isinstance(identity, str) or not identity:
            errors.append("request identity must be a non-empty string")
        else:
            attempt.request_identity = "sha256:" + hashlib.sha256(identity.encode("utf-8")).hexdigest()

    attempt.affected_ids_present = "upserted_ids" in payload
    affected_ids = payload.get("upserted_ids")
    if attempt.affected_ids_present:
        if not isinstance(affected_ids, list) or any(not isinstance(item, str) for item in affected_ids):
            errors.append("upserted_ids must be an array of strings")
        else:
            attempt.affected_ids = list(affected_ids)
    return errors


def _plain_response(value: object) -> JsonObject:
    if isinstance(value, Mapping):
        return {str(key): _plain_value(item) for key, item in value.items()}
    for method_name in ("to_dict", "model_dump"):
        method = getattr(value, method_name, None)
        if callable(method):
            result = method()
            if isinstance(result, Mapping):
                return {str(key): _plain_value(item) for key, item in result.items()}
    raise ExperimentalBaselineError("provider response must be an object")


def _plain_value(value: object) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _plain_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain_value(item) for item in value]
    for method_name in ("to_dict", "model_dump"):
        method = getattr(value, method_name, None)
        if callable(method):
            return _plain_value(method())
    if hasattr(value, "__dict__"):
        return {
            key: _plain_value(item)
            for key, item in vars(value).items()
            if not key.startswith("_")
        }
    return value


def _redact_mapping(value: Mapping[object, object]) -> JsonObject:
    safe: JsonObject = {}
    for raw_key, item in value.items():
        key = str(raw_key)[:80]
        if re.search(r"secret|token|credential|api.?key|header|account", key, re.IGNORECASE):
            safe[key] = "<redacted>"
        elif item is None or isinstance(item, (bool, int)):
            safe[key] = item
        elif isinstance(item, float):
            safe[key] = item if math.isfinite(item) else "<redacted>"
        elif isinstance(item, Mapping):
            safe[key] = _redact_mapping(item)
        elif isinstance(item, (list, tuple)):
            safe[key] = [
                child if child is None or isinstance(child, (bool, int, float)) else "<redacted>"
                for child in item[:100]
            ]
        else:
            safe[key] = "<redacted>"
    return safe


def _validate_vector(value: object, *, label: str) -> list[float]:
    if not isinstance(value, list) or len(value) != ROUTING_DIMENSIONS:
        raise ExperimentalBaselineError(f"{label} vector must have exactly 384 dimensions")
    vector: list[float] = []
    for item in value:
        if isinstance(item, bool) or not isinstance(item, (int, float)):
            raise ExperimentalBaselineError(f"{label} vector must contain finite numbers")
        number = float(item)
        if not math.isfinite(number):
            raise ExperimentalBaselineError(f"{label} vector must contain finite numbers")
        vector.append(number)
    norm = math.sqrt(sum(item * item for item in vector))
    if norm == 0.0 or abs(norm - 1.0) > 1e-4:
        raise ExperimentalBaselineError(f"{label} vector must be normalized")
    return vector


def _safe_error(exc: BaseException) -> str:
    name = re.sub(r"[^A-Za-z0-9_.-]", "_", exc.__class__.__name__)[:80]
    status = getattr(exc, "status_code", None)
    suffix = f",status={status}" if type(status) is int else ""
    if isinstance(exc, TimeoutError) or "timeout" in name.casefold():
        suffix += ",timeout"
    return name + suffix
