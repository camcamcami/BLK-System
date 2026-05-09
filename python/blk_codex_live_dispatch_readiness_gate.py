from __future__ import annotations

from datetime import datetime
from pathlib import PurePosixPath
from typing import Any

from blk_codex_dispatch_envelope import validate_codex_deterministic_dispatch_envelope

READINESS_GATE_ID = "codex_live_dispatch_readiness_gate"
READINESS_STATUS = "CODEX_LIVE_DISPATCH_READINESS_GATE_FIXTURE_ONLY"
READY_REVIEW = "READY_FOR_AUTHORITY_REVIEW_NOT_EXECUTION"
BLOCKED = "BLOCKED_NOT_AUTHORIZED"
EVIDENCE_STATUS = "PRESENT_FOR_REVIEW_ONLY"
EVIDENCE_AUTHORITY = "REVIEW_ONLY_NOT_EXECUTION"
ARTIFACT_ROOT = PurePosixPath("artifacts/codex-readiness")
MAX_PATH_LENGTH = 180

REQUIRED_RUNTIME_APPROVAL_FIELDS = frozenset(
    {
        "approval_id",
        "source_system",
        "operator_identity",
        "message_event_id",
        "timestamp",
        "expires_at",
        "exact_approved_scope",
        "explicit_excluded_authorities",
        "validated_for_review_only",
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
PREREQUISITE_FIELDS = (
    "blk_pipe_wiring_plan",
    "containment_evidence",
    "validation_execution_plan",
    "telemetry_persistence_plan",
    "rollback_plan",
    "monitoring_plan",
    "operator_controls",
)
REQUIRED_HOSTILE_AUDIT_CHECKS = frozenset(
    {
        "runtime_approval_check",
        "blk_pipe_wiring_check",
        "containment_evidence_check",
        "validation_execution_check",
        "telemetry_persistence_check",
        "rollback_plan_check",
        "monitoring_plan_check",
        "operator_controls_check",
        "authority_non_expansion_check",
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
        "runtime_approval",
        "approval_id",
        "approval_provenance",
        "exact_approved_scope",
        "explicit_excluded_authorities",
        "validated_for_review_only",
        "allowed_modified_files",
        "allowed_new_files",
        "telemetry_authority",
        "sandbox_authority",
        "jsonl_events_authority",
        "final_message_artifact_authority",
    }
)
FORBIDDEN_STRING_MARKERS = tuple(
    marker.casefold()
    for marker in (
        "READY_FOR_EXECUTION",
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
        "APPROVED_FOR_LIVE_EXECUTION",
        "AUTHORIZED_FOR_LIVE_EXECUTION",
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


def build_codex_live_dispatch_readiness_gate(
    *,
    dispatch_envelope: dict[str, Any],
    runtime_approval: dict[str, Any] | None,
    blk_pipe_wiring_plan: dict[str, Any] | None,
    containment_evidence: dict[str, Any] | None,
    validation_execution_plan: dict[str, Any] | None,
    telemetry_persistence_plan: dict[str, Any] | None,
    rollback_plan: dict[str, Any] | None,
    monitoring_plan: dict[str, Any] | None,
    operator_controls: dict[str, Any] | None,
    failure_ceiling: dict[str, Any] | None,
    hostile_audit: dict[str, Any] | None,
    run_id: str,
    used_runtime_approval_ids: set[str],
    used_readiness_run_ids: set[str],
    now: str,
) -> dict[str, Any]:
    """Build and evaluate a fail-closed Codex live-dispatch readiness fixture."""
    record = {
        "readiness_gate_id": READINESS_GATE_ID,
        "readiness_status": READINESS_STATUS,
        "dispatch_envelope": dispatch_envelope,
        "runtime_approval": runtime_approval,
        "blk_pipe_wiring_plan": blk_pipe_wiring_plan,
        "containment_evidence": containment_evidence,
        "validation_execution_plan": validation_execution_plan,
        "telemetry_persistence_plan": telemetry_persistence_plan,
        "rollback_plan": rollback_plan,
        "monitoring_plan": monitoring_plan,
        "operator_controls": operator_controls,
        "failure_ceiling": failure_ceiling,
        "hostile_audit": hostile_audit,
        "run_id": run_id,
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
    return evaluate_codex_live_dispatch_readiness(
        record,
        now=now,
        used_runtime_approval_ids=used_runtime_approval_ids,
        used_readiness_run_ids=used_readiness_run_ids,
    )


def evaluate_codex_live_dispatch_readiness(
    record: dict[str, Any],
    *,
    now: str,
    used_runtime_approval_ids: set[str],
    used_readiness_run_ids: set[str],
) -> dict[str, Any]:
    if used_runtime_approval_ids is None:
        raise ValueError("used_runtime_approval_ids must be supplied for replay protection")
    if used_readiness_run_ids is None:
        raise ValueError("used_readiness_run_ids must be supplied for replay protection")
    if not isinstance(record, dict):
        raise ValueError("readiness record must be a dictionary")

    reasons: list[str] = []
    if record.get("readiness_gate_id") != READINESS_GATE_ID:
        reasons.append("readiness_gate_id invalid")
    if record.get("readiness_status") != READINESS_STATUS:
        reasons.append("readiness_status invalid")

    try:
        validate_codex_deterministic_dispatch_envelope(
            record.get("dispatch_envelope"), now=now, used_approval_ids=set(), used_run_ids=set()
        )
    except ValueError as exc:
        reasons.append(f"dispatch_envelope invalid: {exc}")

    reasons.extend(_runtime_approval_reasons(record.get("runtime_approval"), now, used_runtime_approval_ids))

    run_id = record.get("run_id")
    if not isinstance(run_id, str) or not run_id.strip():
        reasons.append("readiness run_id missing")
    elif run_id in used_readiness_run_ids:
        reasons.append("readiness run replayed")

    for field in PREREQUISITE_FIELDS:
        reasons.extend(_evidence_reasons(field, record.get(field)))
    reasons.extend(_failure_ceiling_reasons(record.get("failure_ceiling")))
    reasons.extend(_hostile_audit_reasons(record.get("hostile_audit")))

    record["blocked_reasons"] = sorted(set(reasons))
    record["evaluation"] = READY_REVIEW if not record["blocked_reasons"] else BLOCKED
    _enforce_false_non_authority_flags(record)
    return record


def validate_codex_live_dispatch_readiness_gate(
    record: dict[str, Any],
    *,
    now: str,
    used_runtime_approval_ids: set[str],
    used_readiness_run_ids: set[str],
) -> dict[str, Any]:
    """Validate a readiness fixture and reject authority-laundering attempts."""
    evaluated = evaluate_codex_live_dispatch_readiness(
        record,
        now=now,
        used_runtime_approval_ids=used_runtime_approval_ids,
        used_readiness_run_ids=used_readiness_run_ids,
    )
    _scan_for_authority_laundering(evaluated)
    return evaluated


def _runtime_approval_reasons(approval: Any, now: str, used_ids: set[str]) -> list[str]:
    if approval is None:
        return ["runtime_approval missing"]
    if not isinstance(approval, dict):
        return ["runtime_approval malformed"]
    reasons: list[str] = []
    missing = sorted(REQUIRED_RUNTIME_APPROVAL_FIELDS - set(approval))
    if missing:
        reasons.append(f"runtime_approval missing fields: {missing}")
        return reasons
    for field in REQUIRED_RUNTIME_APPROVAL_FIELDS - {"explicit_excluded_authorities", "validated_for_review_only"}:
        value = approval.get(field)
        if not isinstance(value, str) or not value.strip():
            reasons.append(f"runtime_approval {field} empty")
    if approval.get("validated_for_review_only") is not True:
        reasons.append("runtime_approval validated_for_review_only must be true")
    excluded = approval.get("explicit_excluded_authorities")
    if not isinstance(excluded, list):
        reasons.append("runtime_approval explicit_excluded_authorities malformed")
    else:
        missing_exclusions = sorted(REQUIRED_EXCLUDED_AUTHORITIES - set(excluded))
        if missing_exclusions:
            reasons.append(f"runtime_approval excluded authorities incomplete: {missing_exclusions}")
    approval_id = approval.get("approval_id")
    if isinstance(approval_id, str) and approval_id in used_ids:
        reasons.append("runtime_approval replayed")
    try:
        if _parse_timestamp(approval.get("expires_at"), "runtime_approval.expires_at") <= _parse_timestamp(now, "now"):
            reasons.append("runtime_approval expired")
    except ValueError as exc:
        reasons.append(str(exc))
    return reasons


def _evidence_reasons(field: str, evidence: Any) -> list[str]:
    if evidence is None:
        return [f"{field} missing"]
    if not isinstance(evidence, dict):
        return [f"{field} malformed"]
    reasons: list[str] = []
    if evidence.get("status") != EVIDENCE_STATUS:
        reasons.append(f"{field} status must be {EVIDENCE_STATUS}")
    if evidence.get("authority") != EVIDENCE_AUTHORITY:
        reasons.append(f"{field} authority must be {EVIDENCE_AUTHORITY}")
    artifact_ref = evidence.get("artifact_ref")
    try:
        _validate_artifact_ref(artifact_ref, field)
    except ValueError as exc:
        reasons.append(str(exc))
    summary = evidence.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        reasons.append(f"{field} summary missing")
    return reasons


def _failure_ceiling_reasons(failure_ceiling: Any) -> list[str]:
    if failure_ceiling is None:
        return ["failure_ceiling missing"]
    if not isinstance(failure_ceiling, dict):
        return ["failure_ceiling malformed"]
    reasons: list[str] = []
    max_iterations = failure_ceiling.get("max_iterations")
    if not isinstance(max_iterations, int) or not 1 <= max_iterations <= 3:
        reasons.append("failure_ceiling max_iterations invalid")
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


def _validate_artifact_ref(path: Any, field: str) -> str:
    if not isinstance(path, str) or not path.strip():
        raise ValueError(f"{field} artifact_ref missing")
    if len(path) > MAX_PATH_LENGTH:
        raise ValueError(f"{field} artifact_ref too long")
    posix = PurePosixPath(path)
    if posix.is_absolute():
        raise ValueError(f"{field} artifact_ref must be relative")
    parts = posix.parts
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError(f"{field} artifact_ref must not contain traversal segments")
    if ".git" in parts:
        raise ValueError(f"{field} artifact_ref must not target .git")
    if parts[:2] != ARTIFACT_ROOT.parts or len(parts) <= len(ARTIFACT_ROOT.parts):
        raise ValueError(f"{field} artifact_ref must be under {ARTIFACT_ROOT}/")
    return posix.as_posix()


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
            raise ValueError(f"forbidden authority field at readiness.{field}")


def _scan_for_authority_laundering(value: Any, path: str = "readiness") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key)
            if key_text.casefold() == "authority":
                if child != EVIDENCE_AUTHORITY:
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
