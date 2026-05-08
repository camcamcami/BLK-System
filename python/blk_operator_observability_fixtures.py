"""Deterministic local operator observability fixtures for BLK-System.

The helpers in this module normalize already-supplied evidence dictionaries into
bounded operator status and escalation package fixtures. They do not run live
health checks, inspect files, contact services, mutate source, capture approval,
publish BEOs, generate RTM, or make drift decisions.
"""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Any

_STATUS_FIXTURE = "OPERATOR_OBSERVABILITY_FIXTURE_ONLY"
_PACKAGE_FIXTURE = "OPERATOR_ESCALATION_PACKAGE_FIXTURE_ONLY"
_AUTHORITY = "OBSERVABILITY_ONLY_NOT_EXECUTION"
_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")

FAILURE_CLASS_ORDER = [
    "INVALID_PAYLOAD",
    "UNAUTHORIZED_MUTATION",
    "VALIDATION_FAILED",
    "OUTPUT_FLOOD",
    "INVALID_REVERT_ANCHOR",
    "DIRTY_WORKSPACE",
    "MISSING_APPROVAL",
    "STALE_OR_REPLAYED_APPROVAL",
    "PROTECTED_VAULT_REQUEST",
    "DISABLED_BLK_TEST",
    "DRAFT_ONLY_BEO",
    "RTM_NOT_GENERATED",
    "UNKNOWN_OR_MALFORMED_REPORT",
]

_CATALOG = {
    "INVALID_PAYLOAD": {
        "domain": "BLK-pipe",
        "phrase": "Blocked before execution: invalid payload",
        "action": "fix payload or brief before redispatch",
    },
    "UNAUTHORIZED_MUTATION": {
        "domain": "BLK-pipe",
        "phrase": "Blocked and reverted: unauthorized mutation",
        "action": "inspect workspace before retry",
    },
    "VALIDATION_FAILED": {
        "domain": "BLK-pipe",
        "phrase": "Blocked after mutation: validation failed",
        "action": "inspect validation evidence before retry",
    },
    "OUTPUT_FLOOD": {
        "domain": "BLK-pipe",
        "phrase": "Blocked: output limit exceeded",
        "action": "inspect bounded evidence and narrow the task",
    },
    "INVALID_REVERT_ANCHOR": {
        "domain": "BLK-pipe",
        "phrase": "Blocked: revert anchor mismatch",
        "action": "inspect workspace before retry",
    },
    "DIRTY_WORKSPACE": {
        "domain": "BLK-pipe",
        "phrase": "Blocked: workspace is dirty",
        "action": "inspect workspace before retry",
    },
    "MISSING_APPROVAL": {
        "domain": "Human gate",
        "phrase": "Blocked: missing approval",
        "action": "obtain separate current human approval",
    },
    "STALE_OR_REPLAYED_APPROVAL": {
        "domain": "Human gate",
        "phrase": "Blocked: approval stale or replayed",
        "action": "obtain fresh source-bound approval",
    },
    "PROTECTED_VAULT_REQUEST": {
        "domain": "BLK-req",
        "phrase": "Blocked: protected BLK-req vault access denied",
        "action": "use approved metadata or context channel",
    },
    "DISABLED_BLK_TEST": {
        "domain": "BLK-test",
        "phrase": "Blocked: BLK-test transport disabled",
        "action": "request a separate BLK-test authority sprint if needed",
    },
    "DRAFT_ONLY_BEO": {
        "domain": "BEO",
        "phrase": "Advisory only: BEO remains draft-only",
        "action": "request separate publication authority if needed",
    },
    "RTM_NOT_GENERATED": {
        "domain": "blk-link",
        "phrase": "Advisory only: RTM not generated",
        "action": "request separate runtime RTM authority if needed",
    },
    "UNKNOWN_OR_MALFORMED_REPORT": {
        "domain": "Observability",
        "phrase": "Blocked: report is unknown or malformed",
        "action": "inspect source evidence and add supported fixture handling",
    },
}

_REPORT_ALLOWED_KEYS = {
    "failure_class",
    "source_report_id",
    "beb_id",
    "trace_artifacts",
    "raw_evidence_ref",
    "raw_evidence_hash",
    "evidence_excerpt",
    "retry_count",
    "failure_ceiling",
    "reverted",
    "dirty",
    "approval_id",
    "actor_identity",
    "command_executed",
    "file_read",
    "network_called",
    "source_mutated",
    "approval_captured",
    "beo_published",
    "rtm_generated",
    "drift_decision_made",
    "protected_body_read",
    "active_vault_scanned",
}
_TRACE_ALLOWED_KEYS = {"kind", "id", "version_hash", "meta"}
_SIDE_EFFECT_FLAGS = [
    "command_executed",
    "file_read",
    "network_called",
    "source_mutated",
    "approval_captured",
    "beo_published",
    "rtm_generated",
    "drift_decision_made",
    "protected_body_read",
    "active_vault_scanned",
]
_FORBIDDEN_KEYS = {
    "active_vault_path",
    "approval_capture",
    "artifact_text",
    "body",
    "body_excerpt",
    "body_hash_input",
    "command",
    "command_line",
    "content",
    "coverage_matrix",
    "coverage_status",
    "drift",
    "drift_decision",
    "drift_rejection",
    "file_path",
    "key_material",
    "ledger",
    "markdown",
    "path",
    "private_key",
    "protected_path",
    "publication",
    "raw_artifact",
    "requirement_body",
    "rtm",
    "rtm_authority",
    "rtm_id",
    "secret",
    "shell",
    "signer",
    "text",
    "token",
    "use_case_body",
}


def build_operator_status_fixture(
    report: dict[str, Any], *, fixture_id: str, excerpt_max_chars: int = 320
) -> dict[str, Any]:
    """Build a bounded local operator status fixture from caller-supplied evidence."""

    fixture_id = _required_string(fixture_id, "fixture_id")
    if not isinstance(report, dict):
        raise ValueError("report must be a dictionary")
    _reject_forbidden_fields_recursive(report, "report")
    _reject_unsupported_fields(report, _REPORT_ALLOWED_KEYS, "report")
    _validate_excerpt_limit(excerpt_max_chars)

    failure_class = _required_string(report.get("failure_class"), "failure_class")
    if failure_class not in _CATALOG:
        raise ValueError(f"unsupported failure_class: {failure_class}")
    catalog = _CATALOG[failure_class]

    for flag in _SIDE_EFFECT_FLAGS:
        _required_false(report.get(flag, False), flag)

    retry_count = _required_int(report.get("retry_count"), "retry_count", minimum=0)
    failure_ceiling = _required_int(report.get("failure_ceiling"), "failure_ceiling", minimum=1)
    if retry_count > failure_ceiling:
        raise ValueError("retry_count cannot exceed failure_ceiling")

    reverted = _required_bool(report.get("reverted"), "reverted")
    dirty = _required_bool(report.get("dirty"), "dirty")
    trace_artifacts = _trace_artifacts(report.get("trace_artifacts"))
    excerpt = _bounded_excerpt(
        _required_string(report.get("evidence_excerpt"), "evidence_excerpt"), excerpt_max_chars
    )

    output = {
        "fixture_id": fixture_id,
        "status_fixture": _STATUS_FIXTURE,
        "authority": _AUTHORITY,
        "failure_class": failure_class,
        "owning_domain": catalog["domain"],
        "concise_status": catalog["phrase"],
        "source_report_id": _required_string(report.get("source_report_id"), "source_report_id"),
        "beb_id": _required_string(report.get("beb_id"), "beb_id"),
        "trace_artifacts": trace_artifacts,
        "raw_evidence_ref": _required_string(report.get("raw_evidence_ref"), "raw_evidence_ref"),
        "raw_evidence_hash": _required_hash(report.get("raw_evidence_hash"), "raw_evidence_hash"),
        "bounded_evidence_excerpt": excerpt,
        "evidence_inline_bounded": True,
        "raw_evidence_embedded": False,
        "retry_count": retry_count,
        "failure_ceiling": failure_ceiling,
        "failure_ceiling_remaining": failure_ceiling - retry_count,
        "reverted": reverted,
        "dirty": dirty,
        "human_decision_required": True,
        "next_operator_action": "inspect workspace before retry" if dirty else catalog["action"],
        "approval_id": _optional_string(report.get("approval_id"), "approval_id"),
        "actor_identity": _optional_string(report.get("actor_identity"), "actor_identity"),
    }
    for flag in _SIDE_EFFECT_FLAGS:
        output[flag] = False
    return output


def build_operator_escalation_package(
    statuses: list[dict[str, Any]], *, package_id: str
) -> dict[str, Any]:
    """Build a token-bounded local escalation package from status fixtures."""

    package_id = _required_string(package_id, "package_id")
    if not isinstance(statuses, list) or not statuses:
        raise ValueError("statuses must be a non-empty list")
    normalized = [_validate_status_fixture(status) for status in statuses]
    output = {
        "package_id": package_id,
        "package_status": _PACKAGE_FIXTURE,
        "authority": _AUTHORITY,
        "status_count": len(normalized),
        "status_ids": [status["fixture_id"] for status in normalized],
        "failure_classes": [status["failure_class"] for status in normalized],
        "owning_domains": [status["owning_domain"] for status in normalized],
        "concise_statuses": [status["concise_status"] for status in normalized],
        "human_decision_required": any(status["human_decision_required"] for status in normalized),
        "next_operator_actions": [status["next_operator_action"] for status in normalized],
        "raw_evidence_refs": [status["raw_evidence_ref"] for status in normalized],
        "raw_evidence_hashes": [status["raw_evidence_hash"] for status in normalized],
        "bounded_evidence_excerpts": [status["bounded_evidence_excerpt"] for status in normalized],
        "raw_evidence_embedded": False,
    }
    for flag in _SIDE_EFFECT_FLAGS:
        output[flag] = False
    return output


def _validate_status_fixture(status: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(status, dict):
        raise ValueError("status must be a dictionary")
    if status.get("status_fixture") != _STATUS_FIXTURE:
        raise ValueError("status_fixture must be OPERATOR_OBSERVABILITY_FIXTURE_ONLY")
    if status.get("authority") != _AUTHORITY:
        raise ValueError("status authority must be OBSERVABILITY_ONLY_NOT_EXECUTION")
    for key in [
        "fixture_id",
        "failure_class",
        "owning_domain",
        "concise_status",
        "next_operator_action",
        "raw_evidence_ref",
    ]:
        _required_string(status.get(key), key)
    _required_hash(status.get("raw_evidence_hash"), "raw_evidence_hash")
    if status.get("failure_class") not in _CATALOG:
        raise ValueError("status failure_class is unsupported")
    if status.get("raw_evidence_embedded") is not False:
        raise ValueError("raw_evidence_embedded must be false")
    if not isinstance(status.get("human_decision_required"), bool):
        raise ValueError("human_decision_required must be bool")
    for flag in _SIDE_EFFECT_FLAGS:
        _required_false(status.get(flag), flag)
    return deepcopy(status)


def _trace_artifacts(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list) or not value:
        raise ValueError("trace_artifacts must be a non-empty list")
    out: list[dict[str, str]] = []
    identities: set[tuple[str, str]] = set()
    for item in value:
        if not isinstance(item, dict):
            raise ValueError("trace_artifacts entries must be dictionaries")
        _reject_forbidden_fields_recursive(item, "trace_artifacts")
        _reject_unsupported_fields(item, _TRACE_ALLOWED_KEYS, "trace_artifacts")
        kind = _required_string(item.get("kind"), "kind")
        artifact_id = _required_string(item.get("id"), "id")
        identity = (kind, artifact_id)
        if identity in identities:
            raise ValueError(f"duplicate trace identity: {kind}:{artifact_id}")
        identities.add(identity)
        out.append(
            {
                "kind": kind,
                "id": artifact_id,
                "version_hash": _required_hash(item.get("version_hash"), "version_hash"),
            }
        )
    return out


def _reject_forbidden_fields_recursive(value: Any, context: str) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            normalized = str(key).lower()
            if normalized in _FORBIDDEN_KEYS:
                raise ValueError(f"{context} rejects forbidden field: {key}")
            _reject_forbidden_fields_recursive(nested, context)
    elif isinstance(value, list):
        for item in value:
            _reject_forbidden_fields_recursive(item, context)


def _reject_unsupported_fields(value: dict[str, Any], allowed: set[str], context: str) -> None:
    for key in value:
        if key not in allowed:
            raise ValueError(f"{context} unsupported field: {key}")


def _bounded_excerpt(value: str, max_chars: int) -> str:
    if len(value) <= max_chars:
        return value
    return value[: max_chars - 3] + "..."


def _validate_excerpt_limit(value: int) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or not 24 <= value <= 1000:
        raise ValueError("excerpt_max_chars must be between 24 and 1000")


def _required_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value


def _optional_string(value: Any, field: str) -> str | None:
    if value is None:
        return None
    return _required_string(value, field)


def _required_hash(value: Any, field: str) -> str:
    value = _required_string(value, field)
    if not _HASH_RE.match(value):
        raise ValueError(f"{field} must be sha256:<64 lowercase hex>")
    return value


def _required_int(value: Any, field: str, *, minimum: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise ValueError(f"{field} must be an integer >= {minimum}")
    return value


def _required_bool(value: Any, field: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field} must be bool")
    return value


def _required_false(value: Any, field: str) -> None:
    if value is not False:
        raise ValueError(f"{field} must be false")
