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
MAX_STATUS_COUNT = 20
MAX_TRACE_ARTIFACTS = 20
MAX_ID_CHARS = 128
MAX_RAW_REF_CHARS = 512
MAX_EXCERPT_CHARS = 1000
MAX_TOTAL_PACKAGE_EXCERPT_CHARS = 4000

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
        "action": "fix payload or brief; separate human decision required before any retry",
    },
    "UNAUTHORIZED_MUTATION": {
        "domain": "BLK-pipe",
        "phrase": "Blocked and reverted: unauthorized mutation",
        "action": "inspect workspace; separate human decision required before any retry",
    },
    "VALIDATION_FAILED": {
        "domain": "BLK-pipe",
        "phrase": "Blocked after mutation: validation failed",
        "action": "inspect validation evidence; separate human decision required before any retry",
    },
    "OUTPUT_FLOOD": {
        "domain": "BLK-pipe",
        "phrase": "Blocked: output limit exceeded",
        "action": "inspect bounded evidence and narrow the task; separate human decision required before any retry",
    },
    "INVALID_REVERT_ANCHOR": {
        "domain": "BLK-pipe",
        "phrase": "Blocked: revert anchor mismatch",
        "action": "stop and escalate; revert anchor mismatch requires human workspace inspection",
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
_STATUS_ALLOWED_KEYS = {
    "fixture_id",
    "status_fixture",
    "authority",
    "failure_class",
    "owning_domain",
    "concise_status",
    "source_report_id",
    "beb_id",
    "trace_artifacts",
    "raw_evidence_ref",
    "raw_evidence_hash",
    "bounded_evidence_excerpt",
    "evidence_inline_bounded",
    "raw_evidence_embedded",
    "retry_count",
    "failure_ceiling",
    "failure_ceiling_remaining",
    "retry_approved_by_fixture",
    "reverted",
    "dirty",
    "human_decision_required",
    "next_operator_action",
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
_FORBIDDEN_EXACT_KEYS = {
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
_FORBIDDEN_TOKENS = {
    "active",
    "body",
    "command",
    "content",
    "drift",
    "ledger",
    "markdown",
    "path",
    "private",
    "protected",
    "publication",
    "published",
    "rtm",
    "secret",
    "shell",
    "signer",
    "text",
    "token",
    "vault",
}


def build_operator_status_fixture(
    report: dict[str, Any], *, fixture_id: str, excerpt_max_chars: int = 320
) -> dict[str, Any]:
    """Build a bounded local operator status fixture from caller-supplied evidence."""

    fixture_id = _bounded_required_string(fixture_id, "fixture_id", MAX_ID_CHARS)
    if not isinstance(report, dict):
        raise ValueError("report must be a dictionary")
    _reject_forbidden_fields_recursive(report, "report", allowed_top_level=_REPORT_ALLOWED_KEYS)
    _reject_unsupported_fields(report, _REPORT_ALLOWED_KEYS, "report")
    _validate_excerpt_limit(excerpt_max_chars)

    failure_class = _bounded_required_string(report.get("failure_class"), "failure_class", MAX_ID_CHARS)
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
    _validate_class_indicators(failure_class, reverted=reverted, dirty=dirty)
    trace_artifacts = _trace_artifacts(report.get("trace_artifacts"))
    excerpt = _bounded_excerpt(
        _bounded_required_string(report.get("evidence_excerpt"), "evidence_excerpt", MAX_EXCERPT_CHARS),
        excerpt_max_chars,
    )
    remaining = failure_ceiling - retry_count

    output = {
        "fixture_id": fixture_id,
        "status_fixture": _STATUS_FIXTURE,
        "authority": _AUTHORITY,
        "failure_class": failure_class,
        "owning_domain": catalog["domain"],
        "concise_status": catalog["phrase"],
        "source_report_id": _bounded_required_string(
            report.get("source_report_id"), "source_report_id", MAX_ID_CHARS
        ),
        "beb_id": _bounded_required_string(report.get("beb_id"), "beb_id", MAX_ID_CHARS),
        "trace_artifacts": trace_artifacts,
        "raw_evidence_ref": _bounded_required_string(
            report.get("raw_evidence_ref"), "raw_evidence_ref", MAX_RAW_REF_CHARS
        ),
        "raw_evidence_hash": _required_hash(report.get("raw_evidence_hash"), "raw_evidence_hash"),
        "bounded_evidence_excerpt": excerpt,
        "evidence_inline_bounded": True,
        "raw_evidence_embedded": False,
        "retry_count": retry_count,
        "failure_ceiling": failure_ceiling,
        "failure_ceiling_remaining": remaining,
        "retry_approved_by_fixture": False,
        "reverted": reverted,
        "dirty": dirty,
        "human_decision_required": True,
        "next_operator_action": _operator_action(catalog["action"], remaining=remaining, dirty=dirty),
        "approval_id": _optional_bounded_string(report.get("approval_id"), "approval_id", MAX_ID_CHARS),
        "actor_identity": _optional_bounded_string(
            report.get("actor_identity"), "actor_identity", MAX_ID_CHARS
        ),
    }
    for flag in _SIDE_EFFECT_FLAGS:
        output[flag] = False
    return output


def build_operator_escalation_package(
    statuses: list[dict[str, Any]], *, package_id: str
) -> dict[str, Any]:
    """Build a token-bounded local escalation package from status fixtures."""

    package_id = _bounded_required_string(package_id, "package_id", MAX_ID_CHARS)
    if not isinstance(statuses, list) or not statuses:
        raise ValueError("statuses must be a non-empty list")
    if len(statuses) > MAX_STATUS_COUNT:
        raise ValueError(f"too many statuses: maximum is {MAX_STATUS_COUNT}")
    normalized = [_validate_status_fixture(status) for status in statuses]
    total_excerpt_chars = sum(len(status["bounded_evidence_excerpt"]) for status in normalized)
    if total_excerpt_chars > MAX_TOTAL_PACKAGE_EXCERPT_CHARS:
        raise ValueError("package bounded excerpts exceed total size limit")
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
    _reject_forbidden_fields_recursive(status, "status", allowed_top_level=_STATUS_ALLOWED_KEYS)
    _reject_unsupported_fields(status, _STATUS_ALLOWED_KEYS, "status")
    if status.get("status_fixture") != _STATUS_FIXTURE:
        raise ValueError("status_fixture must be OPERATOR_OBSERVABILITY_FIXTURE_ONLY")
    if status.get("authority") != _AUTHORITY:
        raise ValueError("status authority must be OBSERVABILITY_ONLY_NOT_EXECUTION")
    failure_class = _bounded_required_string(status.get("failure_class"), "failure_class", MAX_ID_CHARS)
    if failure_class not in _CATALOG:
        raise ValueError("status failure_class is unsupported")
    catalog = _CATALOG[failure_class]
    if status.get("owning_domain") != catalog["domain"]:
        raise ValueError("owning_domain does not match failure_class")
    if status.get("concise_status") != catalog["phrase"]:
        raise ValueError("concise_status does not match failure_class")
    _bounded_required_string(status.get("fixture_id"), "fixture_id", MAX_ID_CHARS)
    _bounded_required_string(status.get("source_report_id"), "source_report_id", MAX_ID_CHARS)
    _bounded_required_string(status.get("beb_id"), "beb_id", MAX_ID_CHARS)
    _bounded_required_string(status.get("raw_evidence_ref"), "raw_evidence_ref", MAX_RAW_REF_CHARS)
    _required_hash(status.get("raw_evidence_hash"), "raw_evidence_hash")
    excerpt = _bounded_required_string(
        status.get("bounded_evidence_excerpt"), "bounded_evidence_excerpt", MAX_EXCERPT_CHARS
    )
    if len(excerpt) > MAX_EXCERPT_CHARS:
        raise ValueError(f"bounded_evidence_excerpt must be at most {MAX_EXCERPT_CHARS} characters")
    if status.get("evidence_inline_bounded") is not True:
        raise ValueError("evidence_inline_bounded must be true")
    if status.get("raw_evidence_embedded") is not False:
        raise ValueError("raw_evidence_embedded must be false")
    retry_count = _required_int(status.get("retry_count"), "retry_count", minimum=0)
    failure_ceiling = _required_int(status.get("failure_ceiling"), "failure_ceiling", minimum=1)
    remaining = _required_int(status.get("failure_ceiling_remaining"), "failure_ceiling_remaining", minimum=0)
    if retry_count > failure_ceiling or remaining != failure_ceiling - retry_count:
        raise ValueError("failure ceiling fields are inconsistent")
    if status.get("retry_approved_by_fixture") is not False:
        raise ValueError("retry_approved_by_fixture must be false")
    reverted = _required_bool(status.get("reverted"), "reverted")
    dirty = _required_bool(status.get("dirty"), "dirty")
    _validate_class_indicators(failure_class, reverted=reverted, dirty=dirty)
    if status.get("human_decision_required") is not True:
        raise ValueError("human_decision_required must be true")
    expected_action = _operator_action(catalog["action"], remaining=remaining, dirty=dirty)
    if status.get("next_operator_action") != expected_action:
        raise ValueError("next_operator_action does not match failure_class and indicators")
    _trace_artifacts(status.get("trace_artifacts"))
    _optional_bounded_string(status.get("approval_id"), "approval_id", MAX_ID_CHARS)
    _optional_bounded_string(status.get("actor_identity"), "actor_identity", MAX_ID_CHARS)
    for flag in _SIDE_EFFECT_FLAGS:
        _required_false(status.get(flag), flag)
    return deepcopy(status)


def _trace_artifacts(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list) or not value:
        raise ValueError("trace_artifacts must be a non-empty list")
    if len(value) > MAX_TRACE_ARTIFACTS:
        raise ValueError(f"trace_artifacts must contain at most {MAX_TRACE_ARTIFACTS} entries")
    out: list[dict[str, str]] = []
    identities: set[tuple[str, str]] = set()
    for item in value:
        if not isinstance(item, dict):
            raise ValueError("trace_artifacts entries must be dictionaries")
        _reject_forbidden_fields_recursive(item, "trace_artifacts", allowed_top_level=_TRACE_ALLOWED_KEYS)
        _reject_unsupported_fields(item, _TRACE_ALLOWED_KEYS, "trace_artifacts")
        kind = _bounded_required_string(item.get("kind"), "kind", MAX_ID_CHARS)
        artifact_id = _bounded_required_string(item.get("id"), "id", MAX_ID_CHARS)
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


def _validate_class_indicators(failure_class: str, *, reverted: bool, dirty: bool) -> None:
    if failure_class == "DIRTY_WORKSPACE" and dirty is not True:
        raise ValueError("DIRTY_WORKSPACE requires dirty true")
    if failure_class == "UNAUTHORIZED_MUTATION" and reverted is not True:
        raise ValueError("UNAUTHORIZED_MUTATION requires reverted true")


def _operator_action(base_action: str, *, remaining: int, dirty: bool) -> str:
    if remaining == 0:
        return "stop and escalate; failure ceiling reached; no retry is approved by this fixture"
    if dirty:
        return "inspect workspace before retry"
    return base_action


def _reject_forbidden_fields_recursive(
    value: Any, context: str, *, allowed_top_level: set[str] | None = None
) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key)
            if allowed_top_level is None or key_text not in allowed_top_level:
                if _is_forbidden_key(key_text):
                    raise ValueError(f"{context} rejects forbidden field: {key}")
                _reject_forbidden_fields_recursive(nested, context)
            else:
                _reject_forbidden_fields_recursive(nested, context)
    elif isinstance(value, list):
        for item in value:
            _reject_forbidden_fields_recursive(item, context)


def _is_forbidden_key(key: str) -> bool:
    normalized = re.sub(r"[^a-z0-9]+", "_", key.lower()).strip("_")
    if normalized in _FORBIDDEN_EXACT_KEYS:
        return True
    tokens = {part for part in normalized.split("_") if part}
    if tokens & _FORBIDDEN_TOKENS:
        return True
    composites = {
        "active_vault",
        "protected_vault",
        "private_key",
        "key_material",
        "beo_publication",
        "rtm_status",
    }
    return any(composite in normalized for composite in composites)


def _reject_unsupported_fields(value: dict[str, Any], allowed: set[str], context: str) -> None:
    for key in value:
        if key not in allowed:
            raise ValueError(f"{context} unsupported field: {key}")


def _bounded_excerpt(value: str, max_chars: int) -> str:
    if len(value) <= max_chars:
        return value
    return value[: max_chars - 3] + "..."


def _validate_excerpt_limit(value: int) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or not 24 <= value <= MAX_EXCERPT_CHARS:
        raise ValueError(f"excerpt_max_chars must be between 24 and {MAX_EXCERPT_CHARS}")


def _required_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value


def _bounded_required_string(value: Any, field: str, max_chars: int) -> str:
    value = _required_string(value, field)
    if len(value) > max_chars:
        raise ValueError(f"{field} must be at most {max_chars} characters")
    return value


def _optional_bounded_string(value: Any, field: str, max_chars: int) -> str | None:
    if value is None:
        return None
    return _bounded_required_string(value, field, max_chars)


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
