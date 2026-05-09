from __future__ import annotations

from copy import deepcopy
from typing import Any

REQUEST_STATUS = "BLK_TEST_FIXED_TOOL_PILOT_AUTHORITY_REQUEST_PACKAGE"
READY = "BLK_TEST_PILOT_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME"
BLOCKED = "BLK_TEST_PILOT_REQUEST_BLOCKED_NOT_AUTHORIZED"
DISABLED = "BLK_TEST_PILOT_DISABLED_NOT_AUTHORIZED"
MATURITY = "L0_L1_REQUEST_FIXTURE_ONLY"

DENIED_FLAGS = (
    "production_blk_test_mcp_authorized",
    "live_transport_authorized",
    "fixed_tool_execution_authorized",
    "source_mutation_authorized",
    "git_mutation_authorized",
    "protected_body_read_authorized",
    "protected_body_copy_authorized",
    "protected_body_scan_authorized",
    "beo_publication_authorized",
    "rtm_generation_authorized",
    "drift_rejection_authorized",
    "package_manager_authorized",
    "network_model_cyber_browser_tooling_authorized",
    "production_isolation_claimed",
)

TOP_LEVEL_KEYS = frozenset(
    {
        "request_id",
        "request_status",
        "review_status",
        "maturity",
        "roadmap_source",
        "governing_docs",
        "separate_human_approval_required",
        "future_approval_envelope",
        "proof_obligations",
        "fixed_tool_registry_constraints",
        "excluded_adjacent_authorities",
        "hostile_review_checklist",
        "operator_stop_controls",
        "timeout_output_profile",
        "disabled_transport_preserved",
        "validation_errors",
        *DENIED_FLAGS,
    }
)

REQUIRED_APPROVAL_ENVELOPE_FIELDS = frozenset(
    {
        "grant_id_required",
        "source_system_required",
        "operator_identity_required",
        "message_event_id_required_when_available",
        "issued_at_required",
        "expires_at_required",
        "exact_scope_required",
        "target_boundary_required",
        "fixed_tool_registry_required",
        "test_profile_required",
        "timeout_output_profile_required",
        "explicit_excluded_authorities_required",
        "replay_tracking_required",
        "hostile_review_required",
    }
)

REQUIRED_PROOF_OBLIGATION_SECTIONS = frozenset(
    {
        "fixed_tool_registry",
        "source_binding",
        "physical_isolation",
        "process_output_controls",
        "evidence_semantics",
    }
)

REQUIRED_EXCLUDED_AUTHORITIES = frozenset(
    {
        "codex_live_approval",
        "blk_pipe_execution_approval",
        "blk020_first_smoke_approval",
        "beo_publication_approval",
        "rtm_generation_approval",
        "rtm_drift_rejection_authority",
        "production_blk_test_mcp",
        "protected_body_read",
        "source_mutation",
        "package_manager_network_model_cyber_browser_tooling",
        "production_isolation_claim",
    }
)

REQUIRED_HOSTILE_REVIEW_CHECKS = frozenset(
    {
        "runtime_non_authority_check",
        "approval_separation_check",
        "fixed_tool_registry_check",
        "physical_isolation_check",
        "replay_expiry_check",
        "authority_laundering_check",
        "disabled_adapter_side_effect_check",
    }
)

SUSPICIOUS_KEY_TERMS = (
    "authority",
    "authorized",
    "authorization",
    "approval",
    "approved",
    "allowed",
    "claim",
)

ALLOWED_SUSPICIOUS_KEYS = frozenset(
    {
        "separate_human_approval_required",
        "future_approval_envelope",
        "excluded_adjacent_authorities",
        "explicit_excluded_authorities_required",
        "hostile_review_required",
        *DENIED_FLAGS,
    }
)

FORBIDDEN_STRING_MARKERS = tuple(
    marker.casefold()
    for marker in (
        "APPROVED_FOR_LIVE_BLK_TEST",
        "APPROVED_FOR_LIVE_EXECUTION",
        "AUTHORIZED_FOR_LIVE_EXECUTION",
        "READY_FOR_RUNTIME",
        "READY_FOR_EXECUTION",
        "CODEX_LIVE_APPROVAL",
        "BLK_PIPE_EXECUTION_APPROVAL",
        "BLK-SYSTEM-014 / BLK-020 approval reused",
        "BEO_PUBLICATION_APPROVAL",
        "RTM_GENERATION_APPROVAL",
        "DRIFT_REJECTION_AUTHORITY",
        "PROTECTED_BODY_READ_ALLOWED",
        "LIVE_TRANSPORT_AUTHORIZED",
        "FIXED_TOOL_EXECUTION_AUTHORIZED",
        "PRODUCTION_BLK_TEST_MCP_AUTHORIZED",
        "SOURCE_MUTATION_AUTHORIZED",
        "authority approved",
        "grants execution authority",
        "production sandbox is enforced",
        "production sandbox enforced",
        "host secret isolation enforced",
        "network firewall enforced",
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


def build_blk_test_fixed_tool_pilot_authority_request(
    *,
    request_id: str,
    used_request_ids: set[str],
) -> dict[str, Any]:
    record = {
        "request_id": request_id,
        "request_status": REQUEST_STATUS,
        "review_status": BLOCKED,
        "maturity": MATURITY,
        "roadmap_source": "BLK-045",
        "governing_docs": ["BLK-017", "BLK-018", "BLK-019", "BLK-020", "BLK-025", "BLK-045", "BLK-046", "BLK-047"],
        "separate_human_approval_required": True,
        "future_approval_envelope": {
            "grant_id_required": True,
            "source_system_required": True,
            "operator_identity_required": True,
            "message_event_id_required_when_available": True,
            "issued_at_required": True,
            "expires_at_required": True,
            "exact_scope_required": True,
            "target_boundary_required": True,
            "fixed_tool_registry_required": True,
            "test_profile_required": True,
            "timeout_output_profile_required": True,
            "explicit_excluded_authorities_required": True,
            "replay_tracking_required": True,
            "hostile_review_required": True,
        },
        "proof_obligations": {
            "fixed_tool_registry": [
                "no arbitrary shell",
                "no caller supplied commands",
                "no wildcard tools",
                "no package manager execution",
                "no network model browser or cyber capability",
            ],
            "source_binding": [
                "BLK-pipe report identity",
                "beb_id",
                "source commit hash",
                "pre_engine_hash",
                "post_engine_hash",
                "trace artifact sha256 hashes",
                "request hash and replay ids",
            ],
            "physical_isolation": [
                "no primary repo runtime input",
                "no git root ancestor or descendant",
                "no root home protected vault or host secret paths",
                "no symlink or traversal escape",
                "cleanup verified before success report",
            ],
            "process_output_controls": [
                "missing approval refuses before process start",
                "timeout and output flood return non success evidence",
                "descendant process and pipe holder controls required",
                "bounded redacted output evidence",
                "operator stop controls required",
            ],
            "evidence_semantics": [
                "PASS remains evidence only",
                "BLOCKED FATAL stale malformed unknown replayed and policy blocked evidence never becomes success",
                "no BEO RTM coverage drift or protected vault truth projection",
            ],
        },
        "fixed_tool_registry_constraints": [
            "deterministic repository owned descriptors only",
            "no dynamic tool expansion",
            "no arbitrary shell",
            "no package manager execution",
            "no network model browser or cyber capability",
        ],
        "excluded_adjacent_authorities": sorted(REQUIRED_EXCLUDED_AUTHORITIES),
        "hostile_review_checklist": sorted(REQUIRED_HOSTILE_REVIEW_CHECKS),
        "operator_stop_controls": {
            "kill_control_required": True,
            "timeout_control_required": True,
            "interruption_control_required": True,
            "cleanup_failure_blocks_success": True,
        },
        "timeout_output_profile": {
            "timeout_required": True,
            "output_cap_required": True,
            "secret_redaction_required": True,
        },
        "disabled_transport_preserved": True,
        "validation_errors": [],
        **{flag: False for flag in DENIED_FLAGS},
    }
    return validate_blk_test_fixed_tool_pilot_authority_request(record, used_request_ids=used_request_ids)


def validate_blk_test_fixed_tool_pilot_authority_request(
    record: dict[str, Any],
    *,
    used_request_ids: set[str],
) -> dict[str, Any]:
    if used_request_ids is None:
        raise ValueError("used_request_ids must be supplied for replay protection")
    if not isinstance(record, dict):
        raise ValueError("BLK-test pilot authority request record must be a dictionary")

    evaluated = deepcopy(record)
    errors: list[str] = []

    unknown_top_keys = sorted(set(evaluated) - TOP_LEVEL_KEYS)
    for key in unknown_top_keys:
        errors.append(f"unsupported top-level key {key!r}")

    if evaluated.get("request_status") != REQUEST_STATUS:
        errors.append("request_status must be BLK_TEST_FIXED_TOOL_PILOT_AUTHORITY_REQUEST_PACKAGE")
    if evaluated.get("maturity") != MATURITY:
        errors.append("maturity must be L0_L1_REQUEST_FIXTURE_ONLY")
    if evaluated.get("roadmap_source") != "BLK-045":
        errors.append("roadmap_source must be BLK-045")
    if evaluated.get("separate_human_approval_required") is not True:
        errors.append("separate_human_approval_required must remain true")
    if evaluated.get("disabled_transport_preserved") is not True:
        errors.append("disabled_transport_preserved must remain true")

    request_id = evaluated.get("request_id")
    if not isinstance(request_id, str) or not request_id.strip():
        errors.append("request_id missing")
    elif request_id in used_request_ids:
        errors.append("request replayed")

    governing_docs = evaluated.get("governing_docs")
    if not isinstance(governing_docs, list) or "BLK-047" not in governing_docs:
        errors.append("governing_docs must include BLK-047")

    errors.extend(_approval_envelope_errors(evaluated.get("future_approval_envelope")))
    errors.extend(_proof_obligation_errors(evaluated.get("proof_obligations")))
    errors.extend(_required_list_errors("fixed_tool_registry_constraints", evaluated.get("fixed_tool_registry_constraints")))
    errors.extend(_required_set_errors("excluded_adjacent_authorities", evaluated.get("excluded_adjacent_authorities"), REQUIRED_EXCLUDED_AUTHORITIES))
    errors.extend(_required_set_errors("hostile_review_checklist", evaluated.get("hostile_review_checklist"), REQUIRED_HOSTILE_REVIEW_CHECKS))
    errors.extend(_operator_stop_control_errors(evaluated.get("operator_stop_controls")))
    errors.extend(_timeout_output_profile_errors(evaluated.get("timeout_output_profile")))

    for flag in DENIED_FLAGS:
        if evaluated.get(flag) is not False:
            errors.append(f"{flag} must be false")
        evaluated[flag] = False

    errors.extend(_authority_laundering_errors(evaluated))
    evaluated["validation_errors"] = errors
    evaluated["review_status"] = BLOCKED if errors else READY
    return evaluated


def simulate_disabled_blk_test_pilot_adapter(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "adapter_result": DISABLED,
        "request_id": record.get("request_id") if isinstance(record, dict) else None,
        "blocked_reasons": ["BLK-test fixed-tool pilot adapter disabled; future human runtime approval required"],
        "mcp_server_started": False,
        "mcp_client_started": False,
        "fixed_tool_executed": False,
        "source_mutation_attempted": False,
        "protected_body_read_attempted": False,
        "beo_publication_attempted": False,
        "rtm_generation_attempted": False,
        "network_called": False,
        "package_manager_called": False,
    }


def _approval_envelope_errors(value: Any) -> list[str]:
    if not isinstance(value, dict) or not value:
        return ["future_approval_envelope must be a dictionary with required proof fields"]
    missing = sorted(field for field in REQUIRED_APPROVAL_ENVELOPE_FIELDS if value.get(field) is not True)
    return [f"future_approval_envelope missing {field}" for field in missing]


def _proof_obligation_errors(value: Any) -> list[str]:
    if not isinstance(value, dict) or not value:
        return ["proof_obligations must be a dictionary"]
    errors: list[str] = []
    for section in sorted(REQUIRED_PROOF_OBLIGATION_SECTIONS):
        errors.extend(_required_list_errors(f"proof_obligations.{section}", value.get(section)))
    return errors


def _operator_stop_control_errors(value: Any) -> list[str]:
    if not isinstance(value, dict) or not value:
        return ["operator_stop_controls must be a dictionary"]
    required = (
        "kill_control_required",
        "timeout_control_required",
        "interruption_control_required",
        "cleanup_failure_blocks_success",
    )
    return [f"operator_stop_controls.{field} must be true" for field in required if value.get(field) is not True]


def _timeout_output_profile_errors(value: Any) -> list[str]:
    if not isinstance(value, dict) or not value:
        return ["timeout_output_profile must be a dictionary"]
    required = ("timeout_required", "output_cap_required", "secret_redaction_required")
    return [f"timeout_output_profile.{field} must be true" for field in required if value.get(field) is not True]


def _required_list_errors(path: str, value: Any) -> list[str]:
    if not isinstance(value, list) or not value:
        return [f"{path} must be a non-empty list"]
    return []


def _required_set_errors(path: str, value: Any, required: frozenset[str]) -> list[str]:
    if not isinstance(value, list):
        return [f"{path} must be a list"]
    missing = sorted(required - set(value))
    return [f"{path} missing {item}" for item in missing]


def _authority_laundering_errors(value: Any, path: str = "record") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key)
            child_path = f"{path}.{key_text}"
            normalized_key = key_text.casefold()
            if key_text not in ALLOWED_SUSPICIOUS_KEYS and any(term in normalized_key for term in SUSPICIOUS_KEY_TERMS):
                errors.append(f"forbidden authority-like key at {child_path}: {key_text}")
            if path != "record" and key_text in DENIED_FLAGS:
                errors.append(f"forbidden nested denied authority key at {child_path}: {key_text}")
            if key_text not in ALLOWED_SUSPICIOUS_KEYS:
                errors.extend(_string_laundering_errors(key_text, child_path))
            errors.extend(_authority_laundering_errors(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(_authority_laundering_errors(child, f"{path}[{index}]"))
    elif isinstance(value, str):
        if not path.startswith("record.excluded_adjacent_authorities["):
            errors.extend(_string_laundering_errors(value, path))
    return errors


def _string_laundering_errors(value: str, path: str) -> list[str]:
    normalized = value.casefold()
    findings = []
    for marker in FORBIDDEN_STRING_MARKERS:
        if marker in normalized:
            findings.append(f"forbidden authority wording at {path}: {value}")
    return findings
