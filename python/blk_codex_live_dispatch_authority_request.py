from __future__ import annotations

from datetime import datetime
from typing import Any

from blk_codex_live_dispatch_readiness_gate import validate_codex_live_dispatch_readiness_gate

AUTHORITY_REQUEST_ID = "codex_live_dispatch_authority_request"
AUTHORITY_REQUEST_STATUS = "CODEX_LIVE_DISPATCH_AUTHORITY_REQUEST_FIXTURE_ONLY"
ADAPTER_STATUS = "CODEX_LIVE_DISPATCH_DISABLED_ADAPTER_FIXTURE_ONLY"
READY_HUMAN_REVIEW = "AUTHORITY_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_EXECUTION"
BLOCKED = "DISABLED_ADAPTER_BLOCKED_NOT_AUTHORIZED"
REQUIRED_HUMAN_GRANT_FIELDS = frozenset(
    {
        "grant_id",
        "source_system",
        "operator_identity",
        "message_event_id",
        "timestamp",
        "expires_at",
        "exact_approved_scope",
        "explicit_excluded_authorities",
        "review_only",
    }
)
REQUIRED_EXCLUDED_AUTHORITIES = frozenset(
    {
        "live_codex_execution",
        "blk_pipe_dispatch",
        "production_blk_test_mcp",
        "source_mutation",
        "git_mutation",
        "protected_body_read",
        "beo_publication",
        "rtm_generation",
        "drift_rejection",
        "production_sandbox_claim",
        "package_manager",
        "network_model_cyber_tooling",
    }
)
REQUIRED_HOSTILE_AUDIT_CHECKS = frozenset(
    {
        "ready_review_check",
        "separate_human_grant_check",
        "disabled_adapter_check",
        "authority_non_expansion_check",
    }
)
REQUIRED_OPERATOR_CASES = frozenset(
    {
        "missing_ready_review",
        "missing_human_grant",
        "disabled_adapter_attempt",
        "denied_authority",
    }
)
FORBIDDEN_AUTHORITY_TERMS = (
    "live_codex_execution",
    "blk_pipe_dispatch",
    "production_blk_test_mcp",
    "protected_body",
    "active_vault",
    "beo_publication",
    "rtm_generation",
    "drift_rejection",
    "production_sandbox",
    "network_firewall",
    "host_secret_isolation",
    "source_mutation",
    "git_mutation",
    "package_manager",
    "network_model_cyber",
    "execution_authorized",
    "codex_subprocess_started",
    "blk_pipe_dispatched",
    "source_mutation_authorized",
)
SUSPICIOUS_AUTHORITY_KEY_TERMS = (
    "authority",
    "authorized",
    "authorization",
    "approval",
    "approved",
    "allowed",
    "claim",
)
ALLOWED_AUTHORITY_KEY_EXCEPTIONS = frozenset(
    {
        "authority_request_id",
        "authority_request_status",
        "separate_human_grant",
        "separate_human_grant_required",
        "explicit_excluded_authorities",
    }
)
FORBIDDEN_STRING_MARKERS = tuple(
    marker.casefold()
    for marker in (
        "READY_FOR_EXECUTION",
        "APPROVED_FOR_LIVE_EXECUTION",
        "AUTHORIZED_FOR_LIVE_EXECUTION",
        "CODEX_LIVE_APPROVAL",
        "BLK_PIPE_EXECUTION_APPROVAL",
        "PRODUCTION_SANDBOX_ENFORCED",
        "PRODUCTION_SANDBOX_AUTHORITY",
        "NETWORK_FIREWALL_ENFORCED",
        "HOST_SECRET_ISOLATION_ENFORCED",
        "BEO_PUBLICATION_APPROVAL",
        "RTM_GENERATION_APPROVAL",
        "DRIFT_REJECTION_AUTHORITY",
        "PROTECTED_BODY_READ_ALLOWED",
        "authority approved",
        "grants execution authority",
        "pip install",
        "npm install",
        "uv pip install",
        "go get",
        "curl ",
        "wget ",
        "ssh ",
        "https://",
        "http://",
    )
)


def build_codex_live_dispatch_authority_request(
    *,
    readiness_record: dict[str, Any],
    separate_human_grant: dict[str, Any] | None,
    request_scope: str,
    failure_ceiling: dict[str, Any] | None,
    hostile_audit: dict[str, Any] | None,
    operator_escalation: dict[str, Any] | None,
    request_id: str,
    used_request_ids: set[str],
    used_human_grant_ids: set[str],
    now: str,
) -> dict[str, Any]:
    """Build a review-only Codex live-dispatch authority request package."""
    record = {
        "authority_request_id": AUTHORITY_REQUEST_ID,
        "authority_request_status": AUTHORITY_REQUEST_STATUS,
        "adapter_status": ADAPTER_STATUS,
        "readiness_record": readiness_record,
        "separate_human_grant": separate_human_grant,
        "separate_human_grant_required": True,
        "request_scope": request_scope,
        "failure_ceiling": failure_ceiling,
        "hostile_audit": hostile_audit,
        "operator_escalation": operator_escalation,
        "request_id": request_id,
        "evaluation": BLOCKED,
        "blocked_reasons": [],
        "execution_authorized": False,
        "codex_subprocess_started": False,
        "blk_pipe_dispatched": False,
        "source_mutation_authorized": False,
        "git_mutation_authorized": False,
        "protected_body_read_authorized": False,
        "protected_body_copy_authorized": False,
        "active_vault_scan_authorized": False,
        "beo_publication_authorized": False,
        "rtm_generation_authorized": False,
        "drift_rejection_authorized": False,
        "network_model_cyber_tooling_authorized": False,
        "package_manager_authorized": False,
        "production_sandbox_claimed": False,
    }
    return _evaluate_authority_request(
        record,
        now=now,
        used_request_ids=used_request_ids,
        used_human_grant_ids=used_human_grant_ids,
    )


def validate_codex_live_dispatch_authority_request(
    record: dict[str, Any],
    *,
    now: str,
    used_request_ids: set[str],
    used_human_grant_ids: set[str],
) -> dict[str, Any]:
    evaluated = _evaluate_authority_request(
        record,
        now=now,
        used_request_ids=used_request_ids,
        used_human_grant_ids=used_human_grant_ids,
    )
    _scan_for_authority_laundering(evaluated)
    return evaluated


def simulate_disabled_codex_live_dispatch_adapter(record: dict[str, Any]) -> dict[str, Any]:
    """Return the only allowed disabled adapter result; never dispatch."""
    return {
        "adapter_status": ADAPTER_STATUS,
        "adapter_result": BLOCKED,
        "blocked_reasons": ["disabled adapter blocks live Codex dispatch; separate future authority sprint required"],
        "execution_authorized": False,
        "codex_subprocess_started": False,
        "blk_pipe_dispatched": False,
        "source_mutation_authorized": False,
        "git_mutation_authorized": False,
        "protected_body_read_authorized": False,
        "beo_publication_authorized": False,
        "rtm_generation_authorized": False,
        "drift_rejection_authorized": False,
        "production_sandbox_claimed": False,
        "request_id": record.get("request_id") if isinstance(record, dict) else None,
    }


def _evaluate_authority_request(
    record: dict[str, Any],
    *,
    now: str,
    used_request_ids: set[str],
    used_human_grant_ids: set[str],
) -> dict[str, Any]:
    if used_request_ids is None:
        raise ValueError("used_request_ids must be supplied for replay protection")
    if used_human_grant_ids is None:
        raise ValueError("used_human_grant_ids must be supplied for replay protection")
    if not isinstance(record, dict):
        raise ValueError("authority request record must be a dictionary")

    reasons: list[str] = []
    if record.get("authority_request_id") != AUTHORITY_REQUEST_ID:
        reasons.append("authority_request_id invalid")
    if record.get("authority_request_status") != AUTHORITY_REQUEST_STATUS:
        reasons.append("authority_request_status invalid")
    if record.get("adapter_status") != ADAPTER_STATUS:
        reasons.append("adapter_status invalid")

    readiness = record.get("readiness_record")
    try:
        validated_readiness = validate_codex_live_dispatch_readiness_gate(
            readiness, now=now, used_runtime_approval_ids=set(), used_readiness_run_ids=set()
        )
        if validated_readiness.get("evaluation") != "READY_FOR_AUTHORITY_REVIEW_NOT_EXECUTION":
            reasons.append("readiness record is not ready for authority review")
    except ValueError as exc:
        reasons.append(f"readiness record invalid: {exc}")

    reasons.extend(_human_grant_reasons(record.get("separate_human_grant"), now, used_human_grant_ids))
    request_id = record.get("request_id")
    if not isinstance(request_id, str) or not request_id.strip():
        reasons.append("authority request_id missing")
    elif request_id in used_request_ids:
        reasons.append("authority request replayed")

    request_scope = record.get("request_scope")
    if not isinstance(request_scope, str) or not request_scope.strip():
        reasons.append("request_scope missing")
    else:
        reasons.extend(_forbidden_wording_reasons("request_scope", request_scope))
    reasons.extend(_failure_ceiling_reasons(record.get("failure_ceiling")))
    reasons.extend(_hostile_audit_reasons(record.get("hostile_audit")))
    reasons.extend(_operator_escalation_reasons(record.get("operator_escalation")))

    if record.get("separate_human_grant_required") is not True:
        reasons.append("separate_human_grant_required must be true")

    record["blocked_reasons"] = sorted(set(reasons))
    record["evaluation"] = READY_HUMAN_REVIEW if not record["blocked_reasons"] else BLOCKED
    _enforce_false_non_authority_flags(record)
    return record


def _human_grant_reasons(grant: Any, now: str, used_ids: set[str]) -> list[str]:
    if grant is None:
        return ["separate_human_grant missing"]
    if not isinstance(grant, dict):
        return ["separate_human_grant malformed"]
    reasons: list[str] = []
    missing = sorted(REQUIRED_HUMAN_GRANT_FIELDS - set(grant))
    if missing:
        reasons.append(f"separate_human_grant missing fields: {missing}")
        return reasons
    for field in REQUIRED_HUMAN_GRANT_FIELDS - {"explicit_excluded_authorities", "review_only"}:
        value = grant.get(field)
        if not isinstance(value, str) or not value.strip():
            reasons.append(f"separate_human_grant {field} empty")
    if grant.get("review_only") is not True:
        reasons.append("separate_human_grant review_only must be true")
    excluded = grant.get("explicit_excluded_authorities")
    if not isinstance(excluded, list):
        reasons.append("separate_human_grant explicit_excluded_authorities malformed")
    else:
        missing_exclusions = sorted(REQUIRED_EXCLUDED_AUTHORITIES - set(excluded))
        if missing_exclusions:
            reasons.append(f"separate_human_grant excluded authorities incomplete: {missing_exclusions}")
    grant_id = grant.get("grant_id")
    if isinstance(grant_id, str) and grant_id in used_ids:
        reasons.append("separate_human_grant replayed")
    try:
        if _parse_timestamp(grant.get("expires_at"), "separate_human_grant.expires_at") <= _parse_timestamp(now, "now"):
            reasons.append("separate_human_grant expired")
    except ValueError as exc:
        reasons.append(str(exc))
    reasons.extend(_forbidden_wording_reasons("separate_human_grant", grant))
    return reasons


def _failure_ceiling_reasons(failure_ceiling: Any) -> list[str]:
    if failure_ceiling is None:
        return ["failure_ceiling missing"]
    if not isinstance(failure_ceiling, dict):
        return ["failure_ceiling malformed"]
    reasons: list[str] = []
    max_iterations = failure_ceiling.get("max_iterations")
    if not isinstance(max_iterations, int) or max_iterations != 1:
        reasons.append("failure_ceiling max_iterations must be 1 for disabled adapter")
    if failure_ceiling.get("on_exhaustion") != "OPERATOR_ESCALATION_REQUIRED":
        reasons.append("failure_ceiling on_exhaustion must require operator escalation")
    return reasons


def _hostile_audit_reasons(hostile_audit: Any) -> list[str]:
    if hostile_audit is None:
        return ["hostile_audit missing"]
    if not isinstance(hostile_audit, dict):
        return ["hostile_audit malformed"]
    checks = hostile_audit.get("required_checks")
    if not isinstance(checks, list):
        return ["hostile_audit required_checks malformed"]
    missing = sorted(REQUIRED_HOSTILE_AUDIT_CHECKS - set(checks))
    return [f"hostile_audit missing checks: {missing}"] if missing else []


def _operator_escalation_reasons(operator_escalation: Any) -> list[str]:
    if operator_escalation is None:
        return ["operator_escalation missing"]
    if not isinstance(operator_escalation, dict):
        return ["operator_escalation malformed"]
    cases = operator_escalation.get("required_cases")
    if not isinstance(cases, list):
        return ["operator_escalation required_cases malformed"]
    missing = sorted(REQUIRED_OPERATOR_CASES - set(cases))
    return [f"operator_escalation missing cases: {missing}"] if missing else []


def _forbidden_wording_reasons(path: str, value: Any) -> list[str]:
    reasons: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            reasons.extend(_forbidden_wording_reasons(f"{path}.{key}", child))
    elif isinstance(value, (list, tuple, set)):
        for index, child in enumerate(value):
            reasons.extend(_forbidden_wording_reasons(f"{path}[{index}]", child))
    elif isinstance(value, str):
        lowered = value.casefold()
        for marker in FORBIDDEN_STRING_MARKERS:
            if marker in lowered:
                reasons.append(f"forbidden authority wording at {path}")
                break
    return reasons


def _enforce_false_non_authority_flags(record: dict[str, Any]) -> None:
    false_fields = (
        "execution_authorized",
        "codex_subprocess_started",
        "blk_pipe_dispatched",
        "source_mutation_authorized",
        "git_mutation_authorized",
        "protected_body_read_authorized",
        "protected_body_copy_authorized",
        "active_vault_scan_authorized",
        "beo_publication_authorized",
        "rtm_generation_authorized",
        "drift_rejection_authorized",
        "network_model_cyber_tooling_authorized",
        "package_manager_authorized",
        "production_sandbox_claimed",
    )
    for field in false_fields:
        record.setdefault(field, False)
        if record[field] is not False:
            raise ValueError(f"forbidden authority field at authority_request.{field}")


def _scan_for_authority_laundering(value: Any, path: str = "authority_request") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key)
            if key_text == "readiness_record":
                continue
            if key_text.casefold() == "authority":
                if child != "REVIEW_ONLY_NOT_EXECUTION":
                    raise ValueError(f"forbidden authority field at {path}.{key_text}")
                _scan_for_authority_laundering(child, f"{path}.{key_text}")
                continue
            if _looks_like_forbidden_authority_key(key_text) and child is not False:
                raise ValueError(f"forbidden authority field at {path}.{key_text}")
            _scan_for_authority_laundering(child, f"{path}.{key_text}")
    elif isinstance(value, (list, tuple, set)):
        for index, child in enumerate(value):
            _scan_for_authority_laundering(child, f"{path}[{index}]")
    elif isinstance(value, str):
        lowered = value.casefold()
        for marker in FORBIDDEN_STRING_MARKERS:
            if marker in lowered:
                raise ValueError(f"forbidden authority wording at {path}")


def _looks_like_forbidden_authority_key(key: str) -> bool:
    lowered = key.casefold()
    if lowered in ALLOWED_AUTHORITY_KEY_EXCEPTIONS:
        return False
    if any(term in lowered for term in FORBIDDEN_AUTHORITY_TERMS):
        return True
    return any(term in lowered for term in SUSPICIOUS_AUTHORITY_KEY_TERMS)


def _parse_timestamp(value: Any, field: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a timestamp string")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field} must be ISO-8601 parseable") from exc
