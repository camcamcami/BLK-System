from __future__ import annotations

from copy import deepcopy
from typing import Any

SELECTION_STATUS = "BLK_SYSTEM_AUTHORITY_FRONTIER_SELECTION_GATE"
READY = "FRONTIER_SELECTION_READY_FOR_HUMAN_DECISION_NOT_RUNTIME"
BLOCKED = "FRONTIER_SELECTION_BLOCKED_NOT_AUTHORIZED"
DISABLED = "FRONTIER_ACTIVATION_DISABLED_NOT_AUTHORIZED"
MATURITY = "L0_L1_SELECTION_FIXTURE_ONLY"
ALLOWED_FRONTIERS = frozenset({"codex_live_dispatch_l3_smoke", "blk_test_fixed_tool_pilot_l3_l4"})

DENIED_FLAGS = (
    "runtime_authority_granted",
    "live_codex_execution_authorized",
    "codex_subprocess_started",
    "blk_pipe_dispatch_authorized",
    "production_blk_test_mcp_authorized",
    "live_blk_test_transport_authorized",
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
        "selection_id",
        "selection_status",
        "review_status",
        "maturity",
        "selected_frontier",
        "exactly_one_frontier_selected",
        "roadmap_source",
        "governing_docs",
        "decision_evidence",
        "required_future_approval_fields",
        "excluded_adjacent_authorities",
        "hostile_review_checklist",
        "disabled_activation_adapter_required",
        "validation_errors",
        *DENIED_FLAGS,
    }
)

REQUIRED_APPROVAL_FIELD_MARKERS = (
    "source system",
    "operator identity",
    "message/event id",
    "issued timestamp",
    "expires timestamp",
    "exact approved frontier",
    "exact approved scope",
    "explicit excluded authorities",
    "replay identifiers",
    "hostile review",
    "operator stop controls",
)

REQUIRED_HOSTILE_REVIEW_MARKERS = (
    "next sprint is not approval",
    "review ready is not runtime approval",
    "exactly one frontier",
    "adjacent authority inheritance",
    "protected body no read",
    "disabled adapter side effects",
    "generic authority laundering",
)

REQUIRED_EXCLUDED_AUTHORITIES = frozenset(
    {
        "live_codex_execution",
        "codex_subprocess",
        "blk_pipe_dispatch",
        "production_blk_test_mcp",
        "live_blk_test_transport",
        "fixed_tool_execution",
        "source_mutation",
        "git_mutation",
        "protected_body_read_copy_scan",
        "beo_publication",
        "rtm_generation",
        "drift_rejection",
        "package_manager_network_model_browser_cyber_tooling",
        "production_isolation_claim",
    }
)

SUSPICIOUS_KEY_TERMS = ("authority", "authorized", "authorization", "approval", "approved", "allowed", "claim")
ALLOWED_SUSPICIOUS_KEYS = frozenset({
    "excluded_adjacent_authorities",
    "required_future_approval_fields",
    "next_sprint_not_approval",
    "sprint_dispatch_not_runtime_approval",
    "review_ready_not_runtime_approval",
    "fixture_ready_not_runtime_approval",
    *DENIED_FLAGS,
})
FORBIDDEN_STRING_MARKERS = tuple(
    marker.casefold()
    for marker in (
        "APPROVED_FOR_LIVE_EXECUTION",
        "AUTHORIZED_FOR_LIVE_EXECUTION",
        "READY_FOR_RUNTIME",
        "CODEX_LIVE_APPROVAL",
        "BLK_PIPE_EXECUTION_APPROVAL",
        "BLK_TEST_PILOT_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME means pilot approved",
        "READY_FOR_AUTHORITY_REVIEW_NOT_EXECUTION means live Codex execution authorized",
        "BEO fixture readiness grants publication approval",
        "RTM fixture readiness grants runtime generation approval",
        "sprint-dispatch approval is runtime approval",
        "next sprint approves runtime pilot",
        "production sandbox is enforced",
        "PRODUCTION_SANDBOX_ENFORCED",
        "PROTECTED_BODY_READ_ALLOWED",
        "RTM_GENERATION_APPROVAL",
        "DRIFT_REJECTION_AUTHORITY",
        "BEO_PUBLICATION_APPROVAL",
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
ALLOWED_NEGATIVE_AUTHORITY_STRINGS = frozenset(
    phrase.casefold()
    for phrase in (
        "next sprint is not approval",
        "review ready is not runtime approval",
        "sprint dispatch is not runtime approval",
        "fixture ready is not runtime approval",
    )
)


def build_authority_frontier_selection_gate(
    *,
    selection_id: str,
    selected_frontier: str,
    used_selection_ids: set[str],
) -> dict[str, Any]:
    record = {
        "selection_id": selection_id,
        "selection_status": SELECTION_STATUS,
        "review_status": BLOCKED,
        "maturity": MATURITY,
        "selected_frontier": selected_frontier,
        "exactly_one_frontier_selected": True,
        "roadmap_source": "BLK-045",
        "governing_docs": _governing_docs_for(selected_frontier),
        "decision_evidence": {
            "next_sprint_not_approval": True,
            "sprint_dispatch_not_runtime_approval": True,
            "review_ready_not_runtime_approval": True,
            "fixture_ready_not_runtime_approval": True,
        },
        "required_future_approval_fields": list(REQUIRED_APPROVAL_FIELD_MARKERS),
        "excluded_adjacent_authorities": sorted(REQUIRED_EXCLUDED_AUTHORITIES),
        "hostile_review_checklist": list(REQUIRED_HOSTILE_REVIEW_MARKERS),
        "disabled_activation_adapter_required": True,
        "validation_errors": [],
        **{flag: False for flag in DENIED_FLAGS},
    }
    return validate_authority_frontier_selection_gate(record, used_selection_ids=used_selection_ids)


def validate_authority_frontier_selection_gate(record: dict[str, Any], *, used_selection_ids: set[str]) -> dict[str, Any]:
    if used_selection_ids is None:
        raise ValueError("used_selection_ids must be supplied for replay protection")
    if not isinstance(record, dict):
        raise ValueError("frontier selection record must be a dictionary")
    evaluated = deepcopy(record)
    errors: list[str] = []

    unknown = sorted(set(evaluated) - TOP_LEVEL_KEYS)
    errors.extend(f"unsupported top-level key {key!r}" for key in unknown)

    if evaluated.get("selection_status") != SELECTION_STATUS:
        errors.append("selection_status invalid")
    if evaluated.get("maturity") != MATURITY:
        errors.append("maturity invalid")
    if evaluated.get("roadmap_source") != "BLK-045":
        errors.append("roadmap_source must be BLK-045")
    if evaluated.get("disabled_activation_adapter_required") is not True:
        errors.append("disabled_activation_adapter_required must be true")

    selection_id = evaluated.get("selection_id")
    if not isinstance(selection_id, str) or not selection_id.strip():
        errors.append("selection_id missing")
    elif selection_id in used_selection_ids:
        errors.append("selection replayed")

    frontier = evaluated.get("selected_frontier")
    if not isinstance(frontier, str) or frontier not in ALLOWED_FRONTIERS:
        errors.append("selected_frontier must name exactly one allowed frontier")
    if not isinstance(frontier, str) or evaluated.get("exactly_one_frontier_selected") is not True:
        errors.append("exactly_one_frontier_selected must be true for one selected_frontier")

    docs = evaluated.get("governing_docs")
    if not isinstance(docs, list) or "BLK-048" not in docs:
        errors.append("governing_docs must include BLK-048")
    elif isinstance(frontier, str) and frontier in ALLOWED_FRONTIERS:
        required_docs = set(_governing_docs_for(frontier))
        missing_docs = sorted(required_docs - set(docs))
        errors.extend(f"governing_docs missing {doc}" for doc in missing_docs)

    errors.extend(_decision_evidence_errors(evaluated.get("decision_evidence")))
    errors.extend(_required_marker_errors("required_future_approval_fields", evaluated.get("required_future_approval_fields"), REQUIRED_APPROVAL_FIELD_MARKERS))
    errors.extend(_required_set_errors("excluded_adjacent_authorities", evaluated.get("excluded_adjacent_authorities"), REQUIRED_EXCLUDED_AUTHORITIES))
    errors.extend(_required_marker_errors("hostile_review_checklist", evaluated.get("hostile_review_checklist"), REQUIRED_HOSTILE_REVIEW_MARKERS))

    for flag in DENIED_FLAGS:
        if evaluated.get(flag) is not False:
            errors.append(f"{flag} must be false")
        evaluated[flag] = False

    errors.extend(_authority_laundering_errors(evaluated))
    evaluated["validation_errors"] = errors
    evaluated["review_status"] = BLOCKED if errors else READY
    return evaluated


def simulate_disabled_frontier_activation_adapter(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "adapter_result": DISABLED,
        "selection_id": record.get("selection_id") if isinstance(record, dict) else None,
        "blocked_reasons": ["frontier activation adapter disabled; future explicit runtime approval required"],
        "codex_subprocess_started": False,
        "blk_pipe_dispatched": False,
        "mcp_server_started": False,
        "mcp_client_started": False,
        "fixed_tool_executed": False,
        "source_mutation_attempted": False,
        "git_mutation_attempted": False,
        "protected_body_read_attempted": False,
        "protected_body_copy_attempted": False,
        "protected_body_scan_attempted": False,
        "beo_publication_attempted": False,
        "rtm_generation_attempted": False,
        "drift_rejection_attempted": False,
        "network_called": False,
        "model_service_called": False,
        "browser_tooling_called": False,
        "cyber_tooling_called": False,
        "package_manager_called": False,
        "arbitrary_shell_called": False,
        "production_isolation_claimed": False,
    }


def _governing_docs_for(frontier: str) -> list[str]:
    common = ["BLK-024", "BLK-045", "BLK-046", "BLK-048"]
    if frontier == "codex_live_dispatch_l3_smoke":
        return common + ["BLK-040", "BLK-041", "BLK-042", "BLK-043", "BLK-044"]
    if frontier == "blk_test_fixed_tool_pilot_l3_l4":
        return common + ["BLK-017", "BLK-018", "BLK-019", "BLK-020", "BLK-025", "BLK-047"]
    return common


def _decision_evidence_errors(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["decision_evidence must be a dictionary"]
    required = (
        "next_sprint_not_approval",
        "sprint_dispatch_not_runtime_approval",
        "review_ready_not_runtime_approval",
        "fixture_ready_not_runtime_approval",
    )
    return [f"decision_evidence.{key} must be true" for key in required if value.get(key) is not True]


def _required_marker_errors(path: str, value: Any, markers: tuple[str, ...]) -> list[str]:
    if not isinstance(value, list) or not value:
        return [f"{path} must be a non-empty list"]
    normalized_items = [str(item).casefold() for item in value]
    errors = []
    for marker in markers:
        if not any(marker.casefold() in item for item in normalized_items):
            errors.append(f"{path} missing required marker {marker!r}")
    return errors


def _required_set_errors(path: str, value: Any, required: frozenset[str]) -> list[str]:
    if not isinstance(value, list):
        return [f"{path} must be a list"]
    actual = set(value)
    missing = sorted(required - actual)
    extra = sorted(actual - required)
    errors = [f"{path} missing {item}" for item in missing]
    errors.extend(f"{path} extra {item}" for item in extra)
    return errors


def _authority_laundering_errors(value: Any, path: str = "record") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key)
            child_path = f"{path}.{key_text}"
            normalized_key = key_text.casefold()
            if path != "record" and ("frontier" in normalized_key or "selected" in normalized_key):
                errors.append(f"nested frontier selection at {child_path}: {key_text}")
            if key_text not in ALLOWED_SUSPICIOUS_KEYS and any(term in normalized_key for term in SUSPICIOUS_KEY_TERMS):
                errors.append(f"forbidden authority-like key at {child_path}: {key_text}")
            if path != "record" and key_text in DENIED_FLAGS:
                errors.append(f"forbidden nested denied authority key at {child_path}: {key_text}")
            if isinstance(child, str):
                errors.extend(_split_key_value_laundering_errors(key_text, child, child_path))
            if key_text not in ALLOWED_SUSPICIOUS_KEYS:
                errors.extend(_string_laundering_errors(key_text, child_path))
            errors.extend(_authority_laundering_errors(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            if isinstance(child, str) and child in ALLOWED_FRONTIERS and path != "record.selected_frontier":
                errors.append(f"nested frontier selection at {path}[{index}]: {child}")
            errors.extend(_authority_laundering_errors(child, f"{path}[{index}]"))
    elif isinstance(value, str):
        if value in ALLOWED_FRONTIERS and path != "record.selected_frontier":
            errors.append(f"nested frontier selection at {path}: {value}")
        if not path.startswith("record.excluded_adjacent_authorities[") and path != "record.review_status":
            errors.extend(_string_laundering_errors(value, path))
    return errors


def _split_key_value_laundering_errors(key: str, value: str, path: str) -> list[str]:
    normalized_key = key.casefold()
    normalized_value = value.casefold()
    authority_key_terms = (
        "runtime",
        "live",
        "execution",
        "transport",
        "pilot",
        "publication",
        "generation",
        "drift",
        "protected_body",
        "body_read",
        "package",
        "network",
        "model",
        "browser",
        "cyber",
        "sandbox",
        "isolation",
    )
    positive_value_terms = ("approved", "authorized", "allowed", "granted", "claimed")
    if any(term in normalized_key for term in authority_key_terms) and any(term in normalized_value for term in positive_value_terms):
        return [f"split key/value authority laundering at {path}: {key}={value}"]
    return []


def _string_laundering_errors(value: str, path: str) -> list[str]:
    normalized = value.casefold()
    findings = []
    for marker in FORBIDDEN_STRING_MARKERS:
        if marker in normalized:
            findings.append(f"forbidden authority wording at {path}: {value}")
    if normalized in ALLOWED_NEGATIVE_AUTHORITY_STRINGS:
        return findings
    positive_terms = ("approved", "authorized", "allowed", "granted", "approval")
    runtime_terms = ("runtime", "live", "execution", "execute", "transport", "pilot", "publication", "generation")
    if any(term in normalized for term in positive_terms) and any(term in normalized for term in runtime_terms):
        findings.append(f"forbidden authority wording at {path}: {value}")
    return findings
