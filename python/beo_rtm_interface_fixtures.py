"""Disabled BEO/RTM interface fixtures.

This module builds deterministic local interface dictionaries from draft BEO
fixtures. It preserves opaque trace metadata only; it does not generate RTM
ledgers, resolve requirements, publish BEOs, call MCP transports, execute
subprocesses, or contact network/model services.
"""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Any

_BEO_STATUSES = {"PASS", "FAIL"}
_BEO_PUBLICATION = "DRAFT_ONLY"
_RTM_STATUS = "NOT_GENERATED"
_RTM_AUTHORITY = "DISABLED_INTERFACE_ONLY"
_TRACE_HASH_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
_AUTHORITY_FIELDS = frozenset(
    {
        "rtm",
        "rtm_id",
        "requirements",
        "coverage_matrix",
        "published_at",
        "approved_by",
    }
)


def build_beo_rtm_interface_fixture(
    beo_fixture: dict[str, Any],
    *,
    interface_id: str,
) -> dict[str, Any]:
    """Build a disabled RTM-facing interface fixture from a draft BEO fixture.

    The return value is an interface contract only. It carries identifiers and
    canonical trace artifacts forward while keeping RTM generation, requirement
    resolution, drift authority, BEO publication, and live transports disabled.
    """
    normalized_interface_id = _required_string(interface_id, "interface_id")

    generated_fields = sorted(_AUTHORITY_FIELDS.intersection(beo_fixture))
    if generated_fields:
        raise ValueError(
            "BEO/RTM interface fixture rejects generated RTM authority field: "
            + generated_fields[0]
        )

    beo_id = _required_string(beo_fixture.get("beo_id"), "beo_id")
    beb_id = _required_string(beo_fixture.get("beb_id"), "beb_id")
    beo_status = _required_string(beo_fixture.get("status"), "status")
    _required_string(beo_fixture.get("pre_engine_hash"), "pre_engine_hash")

    if beo_status not in _BEO_STATUSES:
        raise ValueError("BEO/RTM interface status must be PASS/FAIL")

    beo_publication = str(beo_fixture.get("beo_publication", ""))
    if beo_publication != _BEO_PUBLICATION:
        raise ValueError("BEO/RTM interface requires beo_publication DRAFT_ONLY")

    rtm_status = str(beo_fixture.get("rtm_status", ""))
    if rtm_status != _RTM_STATUS:
        raise ValueError("BEO/RTM interface requires rtm_status NOT_GENERATED")

    return {
        "interface_id": normalized_interface_id,
        "source": "beo-rtm-interface-fixture",
        "beo_id": beo_id,
        "beb_id": beb_id,
        "beo_status": beo_status,
        "beo_publication": _BEO_PUBLICATION,
        "rtm_status": _RTM_STATUS,
        "rtm_authority": _RTM_AUTHORITY,
        "trace_artifacts": _trace_artifacts(beo_fixture),
        "active_vault_read": False,
        "requirements_resolved": False,
        "reason": "RTM generation remains disabled; fixture preserves opaque trace metadata only",
    }


def _required_string(value: Any, field: str) -> str:
    text = str(value or "")
    if not text.strip():
        raise ValueError(f"BEO/RTM interface fixture requires non-empty {field}")
    return text


def _trace_artifacts(beo_fixture: dict[str, Any]) -> list[dict[str, str]]:
    artifacts = beo_fixture.get("trace_artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise ValueError("BEO/RTM interface fixture requires non-empty trace_artifacts")

    normalized: list[dict[str, str]] = []
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            raise ValueError("BEO/RTM interface trace_artifacts must contain objects")
        kind = _required_string(artifact.get("kind"), "trace_artifacts.kind")
        artifact_id = _required_string(artifact.get("id"), "trace_artifacts.id")
        version_hash = _required_string(
            artifact.get("version_hash"), "trace_artifacts.version_hash"
        )
        if not _TRACE_HASH_PATTERN.match(version_hash):
            raise ValueError("trace_artifacts.version_hash must match sha256:<64-lowercase-hex>")
        normalized.append(
            {
                "kind": kind,
                "id": artifact_id,
                "version_hash": version_hash,
            }
        )
    return deepcopy(normalized)
