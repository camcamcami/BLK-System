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
from urllib.parse import unquote

_BEO_STATUSES = {"PASS", "FAIL"}
_BEO_PUBLICATION = "DRAFT_ONLY"
_RTM_STATUS = "NOT_GENERATED"
_RTM_AUTHORITY = "DISABLED_INTERFACE_ONLY"
_ALLOWED_BEO_FIXTURE_KEYS = frozenset(
    {
        "beo_id",
        "beb_id",
        "status",
        "source",
        "commit_hash",
        "pre_engine_hash",
        "trace_artifacts",
        "test_summary",
        "rtm_status",
        "beo_publication",
    }
)
_TRACE_HASH_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
_INTERFACE_ID_PATTERN = re.compile(r"^BEO_RTM_IFACE_[0-9]{3}$")
_BEO_ID_PATTERN = re.compile(r"^BEO_[0-9]{3}$")
_BEB_ID_PATTERN = re.compile(r"^BEB_[0-9]{3}$")
_TRACE_ID_PATTERN = re.compile(r"^(REQ|UC)-[0-9]{3}$")
_TRACE_KEYS = frozenset({"kind", "id", "version_hash"})
_TRACE_KINDS = frozenset({"REQ", "UC"})
_AUTHORITY_FIELDS = frozenset(
    {
        "rtm",
        "rtm_id",
        "requirements",
        "coverage_matrix",
        "published_at",
        "approved_by",
        "active_vault_read",
        "requirements_resolved",
        "protected_body_copied",
        "beb_dispatch_executed",
        "beo_closeout_executed",
        "beo_publication_attempted",
        "rtm_generation_executed",
        "drift_decision_executed",
        "signer_storage_ledger_touched",
        "publication_authority_granted",
        "signature",
        "signer",
        "signer_identity",
        "storage_uri",
        "storage_location",
        "ledger_id",
        "public_ledger_mutation",
        "rollback_plan",
        "rollback_authority",
        "publication_authority",
    }
)
_PROTECTED_TRACE_MARKERS = (
    "docsactive",
    "docsrequirements",
    "docsusecases",
    "requirementsactive",
    "usecasesactive",
    "protectedblkreqbody",
    "protectedbody",
    "bodyexcerpt",
    "systemshall",
)
_AUTHORITY_TRACE_MARKERS = (
    "publishbeo",
    "beopublicationauthorized",
    "beopublicationauthorised",
    "authoritativebeopublication",
    "beopubapproved",
    "abpapproved",
    "rtmbeo",
    "rtmgeneration",
    "rtmgenerated",
    "rtmid",
    "activevaulthashcomparison",
    "signergenerated",
    "cryptographicsigning",
    "publicationauthoritygranted",
    "publicationauthority",
    "approvedforpublication",
    "allowedforpublication",
    "permittedforpublication",
    "greenlit",
    "approvalinherited",
    "codexapproval",
    "blkpipesuccess",
    "blktestpassapproval",
)
_SIDE_EFFECT_KEY_MARKERS = (
    "activevault",
    "activevaultread",
    "activevaulthashcomparison",
    "activevaultpath",
    "requirementsresolved",
    "protectedbodycopied",
    "protectedbodypath",
    "bebdispatch",
    "beocloseout",
    "beopublicationattempted",
    "rtmgeneration",
    "rtmgenerated",
    "generatertm",
    "rtmid",
    "driftdecision",
    "driftrejection",
    "signer",
    "signature",
    "storage",
    "ledger",
    "rollback",
    "publicationauthority",
    "publicledgermutation",
    "approvedby",
    "publishedat",
    "publicationstatus",
    "driftstatus",
    "bodytext",
    "reqbody",
    "coveragematrix",
    "coverageclaim",
    "coveragestatus",
    "blkreqbody",
    "requirementbody",
)
_EXACT_AUTHORITY_KEY_MARKERS = frozenset(
    {"rtm", "drift", "requirements", "body", "beopublication", "rtmstatus"}
)
_CONTROLLED_TOP_LEVEL_KEYS = frozenset({"beopublication", "rtmstatus"})
_SCAN_KEY_MARKERS = (
    _PROTECTED_TRACE_MARKERS + _AUTHORITY_TRACE_MARKERS + _SIDE_EFFECT_KEY_MARKERS
)
_SCAN_VALUE_MARKERS = _SCAN_KEY_MARKERS


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
    _reject_laundered_string(normalized_interface_id, "interface_id")
    if not _INTERFACE_ID_PATTERN.match(normalized_interface_id):
        raise ValueError("interface_id must be exact BEO_RTM_IFACE_###")

    generated_fields = sorted(_AUTHORITY_FIELDS.intersection(beo_fixture))
    if generated_fields:
        raise ValueError(
            "BEO/RTM interface fixture rejects generated RTM authority field or side-effect field: "
            + generated_fields[0]
        )
    _reject_laundering_markers(beo_fixture)
    unsupported_fields = sorted(set(beo_fixture) - _ALLOWED_BEO_FIXTURE_KEYS)
    if unsupported_fields:
        raise ValueError(
            "BEO/RTM interface fixture rejects unsupported source field: "
            + unsupported_fields[0]
        )

    beo_id = _required_string(beo_fixture.get("beo_id"), "beo_id")
    beb_id = _required_string(beo_fixture.get("beb_id"), "beb_id")
    if not _BEO_ID_PATTERN.match(beo_id):
        raise ValueError("beo_id must be exact BEO_###")
    if not _BEB_ID_PATTERN.match(beb_id):
        raise ValueError("beb_id must be exact BEB_###")
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
        "metadata_handoff_status": "BLK_REQ_TRACE_METADATA_ONLY",
        "active_vault_read": False,
        "requirements_resolved": False,
        "protected_body_copied": False,
        "beb_dispatch_executed": False,
        "beo_closeout_executed": False,
        "beo_publication_attempted": False,
        "rtm_generation_executed": False,
        "drift_decision_executed": False,
        "signer_storage_ledger_touched": False,
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
    seen_identities: set[tuple[str, str]] = set()
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            raise ValueError("BEO/RTM interface trace_artifacts must contain objects")
        unsupported = sorted(set(artifact) - _TRACE_KEYS)
        if unsupported:
            raise ValueError(f"trace_artifacts rejects unsupported key: {unsupported[0]}")
        kind = _required_string(artifact.get("kind"), "trace_artifacts.kind")
        if kind not in _TRACE_KINDS:
            raise ValueError("trace_artifacts.kind must be REQ or UC")
        artifact_id = _required_string(artifact.get("id"), "trace_artifacts.id")
        _reject_trace_identity_markers(artifact_id)
        if not _TRACE_ID_PATTERN.match(artifact_id):
            raise ValueError("trace_artifacts.id must be exact REQ-### or UC-###")
        if not artifact_id.startswith(f"{kind}-"):
            raise ValueError("trace_artifacts.kind must match id prefix")
        identity = (kind, artifact_id)
        if identity in seen_identities:
            raise ValueError("duplicate trace_artifacts identity")
        seen_identities.add(identity)
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


def _reject_trace_identity_markers(value: str) -> None:
    normalized = _normalize_for_marker_scan(value)
    if any(marker in normalized for marker in _PROTECTED_TRACE_MARKERS):
        raise ValueError("trace_artifacts.id rejects protected path or body marker")
    if any(marker in normalized for marker in _AUTHORITY_TRACE_MARKERS):
        raise ValueError("trace_artifacts.id rejects authority marker")


def _reject_laundering_markers(value: Any) -> None:
    def walk(node: Any, path: str) -> None:
        if isinstance(node, dict):
            for key, child in node.items():
                if path == "beo_fixture" and key == "trace_artifacts":
                    continue
                normalized_key = _normalize_for_marker_scan(key)
                if path == "beo_fixture" and normalized_key in _CONTROLLED_TOP_LEVEL_KEYS:
                    walk(child, f"{path}.{key}")
                    continue
                if (
                    normalized_key in _EXACT_AUTHORITY_KEY_MARKERS
                    or any(marker in normalized_key for marker in _SCAN_KEY_MARKERS)
                ):
                    raise ValueError(
                        "BEO/RTM interface fixture rejects generated RTM authority field or side-effect field: "
                        + str(key)
                    )
                walk(child, f"{path}.{key}")
        elif isinstance(node, list):
            for index, child in enumerate(node):
                walk(child, f"{path}[{index}]")
        elif isinstance(node, str):
            _reject_laundered_string(node, path)

    walk(value, "beo_fixture")


def _reject_laundered_string(value: str, path: str) -> None:
    normalized_value = _normalize_for_marker_scan(value)
    if any(marker in normalized_value for marker in _SCAN_VALUE_MARKERS):
        raise ValueError(
            "BEO/RTM interface fixture rejects authority or protected marker: "
            + path
        )


def _normalize_for_marker_scan(value: Any) -> str:
    decoded = str(value)
    for _ in range(8):
        next_decoded = unquote(decoded)
        if next_decoded == decoded:
            break
        decoded = next_decoded
    return re.sub(r"[^a-z0-9]+", "", decoded.lower())
