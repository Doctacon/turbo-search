"""Runtime configuration helpers for the turbo-search CLI.

This module intentionally does not read secrets. Live commands read turbopuffer
credentials at the call site only after explicit user approval.
"""

from __future__ import annotations

from dataclasses import dataclass
import os

DEFAULT_REGION = "gcp-us-central1"
DEFAULT_NAMESPACE = "site-scrapling-readthedocs-io-v1"
DEFAULT_EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


@dataclass(frozen=True)
class RuntimeConfig:
    """Non-secret runtime defaults for local and live commands."""

    region: str = DEFAULT_REGION
    namespace: str = DEFAULT_NAMESPACE
    embedding_model: str = DEFAULT_EMBEDDING_MODEL


def load_config() -> RuntimeConfig:
    """Load non-secret runtime configuration from environment defaults.

    Deliberately excludes TURBOPUFFER_API_KEY so help and dry-run commands can be
    used safely without credentials.
    """

    return RuntimeConfig(
        region=os.environ.get("TURBOPUFFER_REGION", DEFAULT_REGION),
        namespace=os.environ.get("TURBOPUFFER_NAMESPACE", DEFAULT_NAMESPACE),
        embedding_model=os.environ.get("TURBO_SEARCH_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL),
    )
