from __future__ import annotations

from typing import Any

DESIGN_GATE_ID = "codex_live_dispatch_execution_authority_design_gate"
DESIGN_GATE_STATUS = "CODEX_LIVE_DISPATCH_EXECUTION_AUTHORITY_DESIGN_GATE_FIXTURE_ONLY"
READY_FOR_REVIEW = "EXECUTION_AUTHORITY_DESIGN_READY_FOR_REVIEW_NOT_EXECUTION"
BLOCKED = "EXECUTION_AUTHORITY_DESIGN_BLOCKED"

REQUIRED_CONTRACT_FIELDS = (
    "approval_envelope_contract",
    "blk_pipe_integration_contract",
    "containment_contract",
    "telemetry_contract",
    "rollback_contract",
    "monitoring_operator_control_contract",
    "failure_ceiling_contract",
    "replay_protection_contract",
    "hostile_audit_contract",
)
REQUIRED_HOSTILE_AUDIT_CHECKS = frozenset(
    {
        "authority_request_package_check",
        "approval_envelope_check",
        "blk_pipe_integration_check",
        "containment_claim_check",
        "telemetry_contract_check",
        "rollback_contract_check",
        "monitoring_operator_control_check",
        "failure_ceiling_check",
        "replay_protection_check",
        "authority_non_expansion_check",
    }
)
SIDE_EFFECT_FLAG_KEYS = frozenset(
    {
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
        "side_effects_authorized",
    }
)
FORBIDDEN_STRING_MARKERS = tuple(
    marker.casefold()
    for marker in (
        "READY_FOR_EXECUTION",
        "APPROVED_FOR_LIVE_EXECUTION",
        "AUTHORIZED_FOR_LIVE_EXECUTION",
        "EXECUTION_AUTHORIZED",
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
        "execute codex now",
        "start codex subprocess",
        "dispatch through blk-pipe",
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
ALLOWED_AUTHORITY_VALUES = frozenset(
    {
        "REVIEW_ONLY_NOT_EXECUTION",
        READY_FOR_REVIEW,
        BLOCKED,
        DESIGN_GATE_STATUS,
        DESIGN_GATE_ID,
        "AUTHORITY_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_EXECUTION",
        "CODEX_LIVE_DISPATCH_AUTHORITY_REQUEST_FIXTURE_ONLY",
        "CODEX_LIVE_DISPATCH_DISABLED_ADAPTER_FIXTURE_ONLY",
        "DISABLED_ADAPTER_BLOCKED_NOT_AUTHORIZED",
    }
)


def build_codex_live_dispatch_execution_authority_design_gate(
    *,
    authority_request_package: dict[str, Any],
    approval_envelope_contract: dict[str, Any] | None,
    blk_pipe_integration_contract: dict[str, Any] | None,
    containment_contract: dict[str, Any] | None,
    telemetry_contract: dict[str, Any] | None,
    rollback_contract: dict[str, Any] | None,
    monitoring_operator_control_contract: dict[str, Any] | None,
    failure_ceiling_contract: dict[str, Any] | None,
    replay_protection_contract: dict[str, Any] | None,
    hostile_audit_contract: dict[str, Any] | None,
    design_id: str,
    used_design_ids: set[str],
    now: str,
) -> dict[str, Any]:
    """Build a review-only execution-authority design gate package."""
    record = {
        "design_gate_id": DESIGN_GATE_ID,
        "design_gate_status": DESIGN_GATE_STATUS,
        "authority_request_package": authority_request_package,
        "approval_envelope_contract": approval_envelope_contract,
        "blk_pipe_integration_contract": blk_pipe_integration_contract,
        "containment_contract": containment_contract,
        "telemetry_contract": telemetry_contract,
        "rollback_contract": rollback_contract,
        "monitoring_operator_control_contract": monitoring_operator_control_contract,
        "failure_ceiling_contract": failure_ceiling_contract,
        "replay_protection_contract": replay_protection_contract,
        "hostile_audit_contract": hostile_audit_contract,
        "design_id": design_id,
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
    return _evaluate_design_gate(record, now=now, used_design_ids=used_design_ids)


def validate_codex_live_dispatch_execution_authority_design_gate(
    record: dict[str, Any],
    *,
    now: str,
    used_design_ids: set[str],
) -> dict[str, Any]:
    _raise_if_forbidden(record)
    evaluated = _evaluate_design_gate(record, now=now, used_design_ids=used_design_ids)
    _raise_if_forbidden(evaluated)
    return evaluated


def _evaluate_design_gate(
    record: dict[str, Any],
    *,
    now: str,
    used_design_ids: set[str],
) -> dict[str, Any]:
    if used_design_ids is None:
        raise ValueError("used_design_ids must be supplied for replay protection")
    if not isinstance(record, dict):
        raise ValueError("design gate record must be a dictionary")

    evaluated = dict(record)
    reasons: list[str] = []

    if evaluated.get("design_gate_id") != DESIGN_GATE_ID:
        reasons.append("design_gate_id invalid")
    if evaluated.get("design_gate_status") != DESIGN_GATE_STATUS:
        reasons.append("design_gate_status invalid")

    request_package = evaluated.get("authority_request_package")
    reasons.extend(_authority_request_package_reasons(request_package))

    design_id = evaluated.get("design_id")
    if not isinstance(design_id, str) or not design_id.strip():
        reasons.append("design_id missing")
    elif design_id in used_design_ids:
        reasons.append("design_id replayed")

    for field in REQUIRED_CONTRACT_FIELDS:
        if field == "hostile_audit_contract":
            reasons.extend(_hostile_audit_reasons(evaluated.get(field), field))
        else:
            reasons.extend(_contract_reasons(evaluated.get(field), field))

    reasons.extend(_side_effect_reasons(evaluated))
    reasons.extend(_forbidden_wording_reasons("record", evaluated))

    evaluated["blocked_reasons"] = reasons
    evaluated["evaluation"] = BLOCKED if reasons else READY_FOR_REVIEW
    _force_false_flags(evaluated)
    return evaluated


def _authority_request_package_reasons(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["authority_request_package missing or malformed"]
    required = {
        "authority_request_id": "codex_live_dispatch_authority_request",
        "authority_request_status": "CODEX_LIVE_DISPATCH_AUTHORITY_REQUEST_FIXTURE_ONLY",
        "adapter_status": "CODEX_LIVE_DISPATCH_DISABLED_ADAPTER_FIXTURE_ONLY",
        "evaluation": "AUTHORITY_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_EXECUTION",
    }
    reasons: list[str] = []
    for key, expected in required.items():
        if value.get(key) != expected:
            reasons.append(f"authority_request_package {key} invalid")
    if value.get("separate_human_grant_required") is not True:
        reasons.append("authority_request_package separate_human_grant_required must be true")
    for key in SIDE_EFFECT_FLAG_KEYS:
        if key in value and value.get(key) is not False:
            reasons.append(f"authority_request_package {key} must be false")
    if value.get("blocked_reasons") not in ([], None):
        reasons.append("authority_request_package must have no blocked_reasons")
    return reasons


def _contract_reasons(value: Any, field: str) -> list[str]:
    reasons: list[str] = []
    if not isinstance(value, dict):
        return [f"{field} missing or malformed"]
    if value.get("status") != "PRESENT_FOR_REVIEW_ONLY":
        reasons.append(f"{field} status must be PRESENT_FOR_REVIEW_ONLY")
    if value.get("authority") != "REVIEW_ONLY_NOT_EXECUTION":
        reasons.append(f"{field} authority must be REVIEW_ONLY_NOT_EXECUTION")
    if value.get("side_effects_authorized") is not False:
        reasons.append(f"{field} side_effects_authorized must be false")
    for key in ("contract_ref", "summary"):
        if not isinstance(value.get(key), str) or not value.get(key, "").strip():
            reasons.append(f"{field} {key} missing")
    return reasons


def _hostile_audit_reasons(value: Any, field: str) -> list[str]:
    if not isinstance(value, dict):
        return [f"{field} missing or malformed"]
    checks = value.get("required_checks")
    if not isinstance(checks, list):
        return [f"{field} required_checks missing"]
    missing = sorted(REQUIRED_HOSTILE_AUDIT_CHECKS - set(checks))
    reasons = [f"{field} required_checks missing {missing}"] if missing else []
    if value.get("authority") != "REVIEW_ONLY_NOT_EXECUTION":
        reasons.append(f"{field} authority must be REVIEW_ONLY_NOT_EXECUTION")
    return reasons


def _side_effect_reasons(value: Any, path: str = "record") -> list[str]:
    reasons: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            nested_path = f"{path}.{key}"
            if key in SIDE_EFFECT_FLAG_KEYS and nested is not False:
                reasons.append(f"{nested_path} must be false")
            reasons.extend(_side_effect_reasons(nested, nested_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            reasons.extend(_side_effect_reasons(nested, f"{path}[{index}]"))
    return reasons


def _forbidden_wording_reasons(path: str, value: Any) -> list[str]:
    reasons: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            reasons.extend(_forbidden_wording_reasons(f"{path}.{key}", nested))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            reasons.extend(_forbidden_wording_reasons(f"{path}[{index}]", nested))
    elif isinstance(value, str):
        folded = value.casefold()
        if value not in ALLOWED_AUTHORITY_VALUES:
            for marker in FORBIDDEN_STRING_MARKERS:
                if marker in folded:
                    reasons.append(f"{path} contains forbidden authority wording {value}")
                    break
    return reasons


def _raise_if_forbidden(value: dict[str, Any]) -> None:
    bad_reasons = _side_effect_reasons(value) + _forbidden_wording_reasons("record", value)
    if bad_reasons:
        raise ValueError("; ".join(bad_reasons))


def _force_false_flags(value: dict[str, Any]) -> None:
    for key in SIDE_EFFECT_FLAG_KEYS:
        if key in value:
            value[key] = False
