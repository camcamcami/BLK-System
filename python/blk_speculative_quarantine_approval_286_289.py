"""BLK-SYSTEM-286..289 speculative quarantine HITL approval packages.

This module makes the acceleration boundary explicit: BLK-pipe/Codex may
compute before a human notices an approval prompt only inside a disposable
quarantine, while durable promotion remains gated by an exact Discord/button
interaction or explicit policy-bypass evidence.  The builders here emit local,
hash-bound evidence only; they do not start transports, dispatch BLK-pipe,
invoke Codex, mutate target/source/Git state, publish BEOs, generate RTM, touch
protected bodies, or claim production isolation.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import hashlib
import json
import re
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering
from blk_identity_relay_spine_283_285 import (
    _validate_identity_contract,
    _validate_relay_contract,
    build_identity_record_283,
    build_relay_envelope_284,
)


class SpeculativeQuarantineValidationError(ValueError):
    """Raised when speculative quarantine approval evidence fails closed."""


_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_ID_RE = re.compile(r"^[A-Z]+(?:-[A-Z0-9]+)+$")
_SNOWFLAKE_RE = re.compile(r"^[0-9]{17,20}$")

CANONICAL_BLK283_IDENTITY_CONTRACT_HASH = "sha256:b7bdbb14890a4ebadcf2e286ca7cf78a899b02cf55cf336bc0681d095662c251"
CANONICAL_BLK284_RELAY_CONTRACT_HASH = "sha256:d209df42c15863a373c7338bd249d24d5f6ae1cba1f1ddd873d2ef8acfdf54ca"
CANONICAL_BLK285_LOOP_EVIDENCE_HASH = "sha256:574b9bfcc919331a28b7919c5412362440f8447a3a0df4d2ad27dc751e16a373"

_EXECUTION_TIMING_MODES = (
    "pre_approval_blocked",
    "speculative_quarantine",
    "config_policy_bypass",
)
_STATE_MODEL = (
    "REQUESTED",
    "QUARANTINE_RUNNING",
    "QUARANTINE_COMPLETE_AWAITING_DECISION",
    "APPROVED_PROMOTED",
    "DRY_RUN_ONLY_PURGED",
    "REJECTED_PURGED",
    "EXPIRED_PURGED",
    "STALE_TARGET_HASH_BLOCKED",
)
_ALLOWED_INTERACTION_DECISIONS = (
    "APPROVE",
    "DENY",
    "APPROVE_DRY_RUN_ONLY",
    "NEEDS_CHANGES",
)
_ALLOWED_GATE_DECISIONS = _ALLOWED_INTERACTION_DECISIONS + (
    "EXPIRE",
    "CONFIG_POLICY_BYPASS",
)
_ALLOWED_POLICY_OPERATION_CLASSES = ("doc_only", "test_only", "format_only")
_REVIEW_OBVIOUS_FUNCTIONS = (
    "start_speculative_quarantine_run",
    "record_quarantine_result",
    "approve_and_promote_quarantined_result",
    "reject_and_purge_quarantined_result",
    "expire_and_purge_quarantined_result",
)

_CONTRACT_SIDE_EFFECTS = {
    "source_git_mutation_before_approval": False,
    "durable_target_mutation_before_approval": False,
    "relay_network_runtime_created": False,
    "message_dispatch_authorized": False,
    "approval_reuse": False,
    "blk_pipe_runtime_started": False,
    "live_codex_dispatch_started": False,
    "protected_body_access": False,
    "beo_publication": False,
    "rtm_generation": False,
    "production_blk_link": False,
    "production_blk_test_mcp": False,
    "network_model_browser_cyber_tooling": False,
    "package_manager_called": False,
    "production_isolation_claim": False,
}
_INTERACTION_SIDE_EFFECTS = {
    "message_dispatch_authorized": False,
    "approval_reuse": False,
    "relay_network_runtime_created": False,
    "blk_pipe_runtime_started": False,
    "live_codex_dispatch_started": False,
    "target_source_git_mutation": False,
    "protected_body_access": False,
    "beo_publication": False,
    "rtm_generation": False,
    "production_blk_link": False,
    "production_blk_test_mcp": False,
    "production_isolation_claim": False,
}
_QUARANTINE_SIDE_EFFECTS = {
    "target_source_git_mutation": False,
    "durable_target_mutation": False,
    "protected_body_access": False,
    "beo_publication": False,
    "rtm_generation": False,
    "production_blk_link": False,
    "production_blk_test_mcp": False,
    "relay_network_runtime_created": False,
    "message_dispatch_authorized": False,
    "production_isolation_claim": False,
}
_GATE_SIDE_EFFECTS = {
    "target_source_git_mutation": False,
    "durable_target_mutation": False,
    "protected_body_access": False,
    "beo_publication": False,
    "rtm_generation": False,
    "production_blk_link": False,
    "production_blk_test_mcp": False,
    "relay_network_runtime_created": False,
    "message_dispatch_authorized": False,
    "approval_reuse": False,
    "production_isolation_claim": False,
}
_DEFAULT_EXTERNAL_SIDE_EFFECTS = {
    "codex_model_api_called": False,
    "network_called": False,
    "package_manager_called": False,
}

_CONTRACT_KEYS = frozenset(
    {
        "status",
        "markers",
        "upstream_identity_contract_hash",
        "upstream_relay_contract_hash",
        "upstream_loop_evidence_hash",
        "execution_timing_modes",
        "state_model",
        "allowed_decisions",
        "primary_ux",
        "fallback_short_challenge",
        "invariant",
        "review_obvious_functions",
        "side_effects",
        "approval_timing_contract_hash",
    }
)
_FALLBACK_KEYS = frozenset(
    {
        "short_reply",
        "request_hash_required",
        "time_window_required",
        "single_use_required",
        "long_copy_paste_required",
    }
)
_LOOP_EVIDENCE_KEYS = frozenset(
    {
        "status",
        "markers",
        "identity_contract_hash",
        "relay_contract_hash",
        "loop_kernel_hash",
        "identity_record_sample_hash",
        "relay_envelope_sample_hash",
        "loop_binding",
        "side_effects",
        "loop_evidence_hash",
    }
)
_INTERACTION_KEYS = frozenset(
    {
        "status",
        "markers",
        "approval_timing_contract_hash",
        "identity_contract_hash",
        "relay_contract_hash",
        "approval_request_hash",
        "request_id",
        "decision",
        "discord_user_id",
        "discord_message_id",
        "discord_interaction_id",
        "component_custom_id",
        "decided_at",
        "expires_at",
        "discord_component_interaction",
        "long_copy_paste_required",
        "actor_identity_hash",
        "approval_identity_hash",
        "hitl_relay_hash",
        "side_effects",
        "hitl_interaction_hash",
    }
)
_QUARANTINE_KEYS = frozenset(
    {
        "status",
        "markers",
        "approval_timing_contract_hash",
        "hitl_interaction_hash",
        "hitl_decision",
        "hitl_decided_at",
        "approval_request_hash",
        "request_id",
        "run_id",
        "execution_timing_mode",
        "state",
        "target_hash_before_quarantine",
        "manifest_hash",
        "result_hash",
        "report_hash",
        "quarantine_workspace_id",
        "started_at",
        "completed_at",
        "approval_expires_at",
        "pre_approval_compute_performed",
        "promotion_performed",
        "target_repo_mutated",
        "external_side_effects",
        "side_effects",
        "quarantine_evidence_hash",
    }
)
_GATE_KEYS = frozenset(
    {
        "status",
        "markers",
        "approval_timing_contract_hash",
        "quarantine_evidence_hash",
        "run_id",
        "decision",
        "decided_at",
        "approval_expires_at",
        "target_hash_before_quarantine",
        "target_hash_at_decision",
        "selected_result_hash",
        "policy_hash",
        "policy_source_id",
        "policy_operation_class",
        "policy_scope_hash",
        "outcome_state",
        "promotion_gate_opened",
        "purge_performed",
        "purge_receipt_hash",
        "stale_target_blocked",
        "durable_target_mutation_performed",
        "side_effects",
        "promotion_or_purge_gate_hash",
    }
)


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def hash_package(package: dict[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json(package).encode("utf-8")).hexdigest()


def _without_hash(package: dict[str, Any], key: str) -> dict[str, Any]:
    return {name: deepcopy(value) for name, value in package.items() if name != key}


def _deepcopy(value: Any) -> Any:
    return deepcopy(value)


def _require_dict(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise SpeculativeQuarantineValidationError(f"{context} must be a dictionary")
    return value


def _require_allowed_keys(package: dict[str, Any], allowed: frozenset[str], context: str) -> None:
    _require_dict(package, context)
    extras = sorted(set(package) - allowed)
    if extras:
        raise SpeculativeQuarantineValidationError(f"{context} unsupported field(s): {', '.join(extras)}")
    missing = sorted(allowed - set(package))
    if missing:
        raise SpeculativeQuarantineValidationError(f"{context} missing field(s): {', '.join(missing)}")


def _require_hash(value: Any, context: str) -> None:
    if not isinstance(value, str) or not _HASH_RE.match(value):
        raise SpeculativeQuarantineValidationError(f"{context} must be sha256:<64 lowercase hex>")


def _require_hash_field(package: dict[str, Any], field: str, context: str) -> None:
    _require_hash(package.get(field), f"{context}.{field}")
    expected = hash_package(_without_hash(package, field))
    if package[field] != expected:
        raise SpeculativeQuarantineValidationError(f"{context} hash mismatch for {field}")


def _reject_laundering(value: Any, context: str) -> None:
    errors = scan_for_authority_laundering(value, path=context)
    if errors:
        raise SpeculativeQuarantineValidationError(
            f"{context} forbidden authority wording: {'; '.join(errors[:4])}"
        )


def _require_ascii(value: str, context: str) -> None:
    if not isinstance(value, str) or any(ord(ch) > 127 for ch in value):
        raise SpeculativeQuarantineValidationError(f"{context} must contain ASCII characters only")


def _require_exact_id(value: Any, prefix: str, context: str) -> None:
    if not isinstance(value, str):
        raise SpeculativeQuarantineValidationError(f"{context} must be a string")
    _require_ascii(value, context)
    if not value.startswith(prefix) or not _ID_RE.match(value):
        raise SpeculativeQuarantineValidationError(f"{context} must be an exact ID with prefix {prefix}")
    _reject_laundering(value, context)


def _require_snowflake(value: Any, context: str) -> None:
    if not isinstance(value, str) or not _SNOWFLAKE_RE.match(value):
        raise SpeculativeQuarantineValidationError(f"{context} must be an ASCII decimal Discord snowflake")


def _parse_timestamp(value: Any, context: str) -> datetime:
    if not isinstance(value, str):
        raise SpeculativeQuarantineValidationError(f"{context} must be a timestamp string")
    candidate = value.replace("Z", "+00:00") if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise SpeculativeQuarantineValidationError(f"{context} must be ISO-8601") from exc
    if parsed.tzinfo is None:
        raise SpeculativeQuarantineValidationError(f"{context} must be timezone-aware")
    return parsed


def _require_timestamp_order(start: Any, end: Any, context: str) -> None:
    parsed_start = _parse_timestamp(start, f"{context}.start")
    parsed_end = _parse_timestamp(end, f"{context}.end")
    if parsed_start >= parsed_end:
        raise SpeculativeQuarantineValidationError(f"{context} start must be before end")


def _require_exact_side_effects(package: dict[str, Any], expected: dict[str, bool], context: str) -> None:
    if package.get("side_effects") != expected:
        raise SpeculativeQuarantineValidationError(f"{context} side_effects mismatch")


def _require_default_external_side_effects(value: Any) -> dict[str, bool]:
    external = dict(_DEFAULT_EXTERNAL_SIDE_EFFECTS) if value is None else _deepcopy(value)
    if external != _DEFAULT_EXTERNAL_SIDE_EFFECTS:
        raise SpeculativeQuarantineValidationError("external_side_effects must remain default false unless policy grants them")
    return external


def _validate_policy_fields(
    decision: str,
    policy_hash: str | None,
    policy_source_id: str | None,
    policy_operation_class: str | None,
    policy_scope_hash: str | None,
) -> None:
    if decision == "CONFIG_POLICY_BYPASS":
        _require_hash(policy_hash, "policy_hash")
        _require_exact_id(policy_source_id, "POLICY-", "policy_source_id")
        if policy_operation_class not in _ALLOWED_POLICY_OPERATION_CLASSES:
            raise SpeculativeQuarantineValidationError("policy_operation_class unsupported for config bypass")
        _require_hash(policy_scope_hash, "policy_scope_hash")
        return
    if any(field is not None for field in (policy_hash, policy_source_id, policy_operation_class, policy_scope_hash)):
        raise SpeculativeQuarantineValidationError("policy fields are only allowed for config bypass")


def _require_gate_decision_matches_quarantine(decision: str, quarantine: dict[str, Any]) -> None:
    hitl_decision = quarantine.get("hitl_decision")
    if decision == "CONFIG_POLICY_BYPASS":
        if hitl_decision != "APPROVE":
            raise SpeculativeQuarantineValidationError("policy bypass cannot override HITL decision")
        return
    if decision == "EXPIRE":
        return
    if decision != hitl_decision:
        raise SpeculativeQuarantineValidationError("promotion/purge gate decision mismatch with HITL interaction")


def _resolve_gate_outcome(
    *,
    decision: str,
    decided_at: str,
    approval_expires_at: str,
    target_hash_before_quarantine: str,
    target_hash_at_decision: str,
) -> str:
    if _parse_timestamp(decided_at, "decided_at") >= _parse_timestamp(approval_expires_at, "approval_expires_at"):
        return "EXPIRED_PURGED"
    if decision in {"DENY", "NEEDS_CHANGES"}:
        return "REJECTED_PURGED"
    if decision == "APPROVE_DRY_RUN_ONLY":
        return "DRY_RUN_ONLY_PURGED"
    if decision == "EXPIRE":
        return "EXPIRED_PURGED"
    if target_hash_at_decision != target_hash_before_quarantine:
        return "STALE_TARGET_HASH_BLOCKED"
    if decision in {"APPROVE", "CONFIG_POLICY_BYPASS"}:
        return "APPROVED_PROMOTED"
    raise SpeculativeQuarantineValidationError("decision did not resolve to a gate outcome")


def _gate_purge_performed(outcome_state: str) -> bool:
    return outcome_state in {
        "DRY_RUN_ONLY_PURGED",
        "REJECTED_PURGED",
        "EXPIRED_PURGED",
        "STALE_TARGET_HASH_BLOCKED",
    }


def _gate_purge_receipt_hash(
    *,
    quarantine_evidence_hash: str,
    outcome_state: str,
    target_hash_at_decision: str,
) -> str:
    return hash_package(
        {
            "quarantine_evidence_hash": quarantine_evidence_hash,
            "outcome_state": outcome_state,
            "target_hash_at_decision": target_hash_at_decision,
        }
    )


def _require_quarantine_timing_claim(
    execution_timing_mode: Any,
    started_at: Any,
    hitl_decided_at: Any,
    context: str,
) -> None:
    started = _parse_timestamp(started_at, f"{context} started_at")
    hitl_decided = _parse_timestamp(hitl_decided_at, f"{context} hitl_decided_at")
    if execution_timing_mode == "speculative_quarantine" and started >= hitl_decided:
        raise SpeculativeQuarantineValidationError(f"{context} pre-approval compute must start before HITL decision")
    if execution_timing_mode == "pre_approval_blocked" and started < hitl_decided:
        raise SpeculativeQuarantineValidationError(f"{context} pre-approval blocked mode must wait for HITL decision")


def _require_gate_not_before_evidence(decided_at: Any, quarantine: dict[str, Any], context: str) -> None:
    gate_decided = _parse_timestamp(decided_at, f"{context} decided_at")
    hitl_decided = _parse_timestamp(quarantine.get("hitl_decided_at"), f"{context} hitl_decided_at")
    quarantine_completed = _parse_timestamp(quarantine.get("completed_at"), f"{context} completed_at")
    if gate_decided < hitl_decided:
        raise SpeculativeQuarantineValidationError(f"{context} decided_at must not precede HITL decision")
    if gate_decided < quarantine_completed:
        raise SpeculativeQuarantineValidationError(f"{context} decided_at must not precede quarantine completion")


def _validate_loop_evidence(loop_evidence: dict[str, Any]) -> dict[str, Any]:
    package = _require_dict(loop_evidence, "loop evidence")
    _require_allowed_keys(package, _LOOP_EVIDENCE_KEYS, "loop evidence")
    if package.get("status") != "IDENTITY_RELAY_LOOP_EVIDENCE_READY":
        raise SpeculativeQuarantineValidationError("loop evidence status mismatch")
    if package.get("identity_contract_hash") != CANONICAL_BLK283_IDENTITY_CONTRACT_HASH:
        raise SpeculativeQuarantineValidationError("loop evidence canonical BLK-283 hash mismatch")
    if package.get("relay_contract_hash") != CANONICAL_BLK284_RELAY_CONTRACT_HASH:
        raise SpeculativeQuarantineValidationError("loop evidence canonical BLK-284 hash mismatch")
    if package.get("loop_evidence_hash") != CANONICAL_BLK285_LOOP_EVIDENCE_HASH:
        raise SpeculativeQuarantineValidationError("loop evidence canonical BLK-285 hash mismatch")
    _require_hash_field(package, "loop_evidence_hash", "loop evidence")
    side_effects = package.get("side_effects")
    for key in (
        "loop_runtime_execution",
        "message_dispatch_authorized",
        "source_git_mutation",
        "protected_body_access",
        "beo_closeout_execution",
        "rtm_generation_authority",
        "production_blk_link_authority",
        "production_blk_test_mcp",
    ):
        if not isinstance(side_effects, dict) or side_effects.get(key) is not False:
            raise SpeculativeQuarantineValidationError(f"loop evidence side_effects.{key} must remain false")
    _reject_laundering(package, "loop evidence")
    return _deepcopy(package)


def _validate_canonical_upstreams(
    identity_contract: dict[str, Any],
    relay_contract: dict[str, Any],
    loop_evidence: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    try:
        identity = _validate_identity_contract(identity_contract)
    except Exception as exc:  # noqa: BLE001 - normalize upstream error type.
        raise SpeculativeQuarantineValidationError(f"identity contract invalid: {exc}") from exc
    try:
        relay = _validate_relay_contract(relay_contract, identity)
    except Exception as exc:  # noqa: BLE001 - normalize upstream error type.
        raise SpeculativeQuarantineValidationError(f"relay contract invalid: {exc}") from exc
    loop = _validate_loop_evidence(loop_evidence)
    if identity["identity_contract_hash"] != CANONICAL_BLK283_IDENTITY_CONTRACT_HASH:
        raise SpeculativeQuarantineValidationError("canonical BLK-283 identity contract hash required")
    if relay["relay_contract_hash"] != CANONICAL_BLK284_RELAY_CONTRACT_HASH:
        raise SpeculativeQuarantineValidationError("canonical BLK-284 relay contract hash required")
    return identity, relay, loop


def build_approval_timing_contract_286(
    identity_contract: dict[str, Any],
    relay_contract: dict[str, Any],
    loop_evidence: dict[str, Any],
) -> dict[str, Any]:
    identity, relay, loop = _validate_canonical_upstreams(identity_contract, relay_contract, loop_evidence)
    package = {
        "status": "SPECULATIVE_QUARANTINE_APPROVAL_CONTRACT_READY",
        "markers": [
            "BLK_SYSTEM_286_SPECULATIVE_QUARANTINE_APPROVAL_CONTRACT_READY",
            "DISCORD_BUTTON_SELECTOR_FIRST_HITL_READY",
            "PRE_APPROVAL_COMPUTE_SEPARATED_FROM_DURABLE_PROMOTION",
        ],
        "upstream_identity_contract_hash": identity["identity_contract_hash"],
        "upstream_relay_contract_hash": relay["relay_contract_hash"],
        "upstream_loop_evidence_hash": loop["loop_evidence_hash"],
        "execution_timing_modes": list(_EXECUTION_TIMING_MODES),
        "state_model": list(_STATE_MODEL),
        "allowed_decisions": list(_ALLOWED_GATE_DECISIONS),
        "primary_ux": "discord_component_button_selector_first",
        "fallback_short_challenge": {
            "short_reply": "Approve",
            "request_hash_required": True,
            "time_window_required": True,
            "single_use_required": True,
            "long_copy_paste_required": False,
        },
        "invariant": "pre_approval_compute_only_in_disposable_quarantine_promotion_requires_decision_or_policy",
        "review_obvious_functions": list(_REVIEW_OBVIOUS_FUNCTIONS),
        "side_effects": dict(_CONTRACT_SIDE_EFFECTS),
    }
    package["approval_timing_contract_hash"] = hash_package(package)
    return validate_approval_timing_contract_286(package)


def validate_approval_timing_contract_286(contract: dict[str, Any]) -> dict[str, Any]:
    package = _require_dict(contract, "approval timing contract")
    _require_allowed_keys(package, _CONTRACT_KEYS, "approval timing contract")
    if package.get("status") != "SPECULATIVE_QUARANTINE_APPROVAL_CONTRACT_READY":
        raise SpeculativeQuarantineValidationError("approval timing contract status mismatch")
    if "BLK_SYSTEM_286_SPECULATIVE_QUARANTINE_APPROVAL_CONTRACT_READY" not in package.get("markers", []):
        raise SpeculativeQuarantineValidationError("approval timing contract marker missing")
    if package.get("upstream_identity_contract_hash") != CANONICAL_BLK283_IDENTITY_CONTRACT_HASH:
        raise SpeculativeQuarantineValidationError("approval timing contract canonical BLK-283 hash mismatch")
    if package.get("upstream_relay_contract_hash") != CANONICAL_BLK284_RELAY_CONTRACT_HASH:
        raise SpeculativeQuarantineValidationError("approval timing contract canonical BLK-284 hash mismatch")
    if package.get("upstream_loop_evidence_hash") != CANONICAL_BLK285_LOOP_EVIDENCE_HASH:
        raise SpeculativeQuarantineValidationError("approval timing contract canonical BLK-285 hash mismatch")
    if tuple(package.get("execution_timing_modes", [])) != _EXECUTION_TIMING_MODES:
        raise SpeculativeQuarantineValidationError("approval timing contract execution_timing_modes mismatch")
    if tuple(package.get("state_model", [])) != _STATE_MODEL:
        raise SpeculativeQuarantineValidationError("approval timing contract state_model mismatch")
    if tuple(package.get("allowed_decisions", [])) != _ALLOWED_GATE_DECISIONS:
        raise SpeculativeQuarantineValidationError("approval timing contract allowed_decisions mismatch")
    if package.get("primary_ux") != "discord_component_button_selector_first":
        raise SpeculativeQuarantineValidationError("approval timing contract primary_ux mismatch")
    fallback = package.get("fallback_short_challenge")
    if not isinstance(fallback, dict) or set(fallback) != _FALLBACK_KEYS:
        raise SpeculativeQuarantineValidationError("approval timing contract fallback_short_challenge schema mismatch")
    if fallback != {
        "short_reply": "Approve",
        "request_hash_required": True,
        "time_window_required": True,
        "single_use_required": True,
        "long_copy_paste_required": False,
    }:
        raise SpeculativeQuarantineValidationError("approval timing contract fallback_short_challenge mismatch")
    if tuple(package.get("review_obvious_functions", [])) != _REVIEW_OBVIOUS_FUNCTIONS:
        raise SpeculativeQuarantineValidationError("approval timing contract review_obvious_functions mismatch")
    _require_exact_side_effects(package, _CONTRACT_SIDE_EFFECTS, "approval timing contract")
    _require_hash_field(package, "approval_timing_contract_hash", "approval timing contract")
    _reject_laundering(package, "approval timing contract")
    return _deepcopy(package)


def _subject_hash_for(value: dict[str, Any]) -> str:
    return hash_package(value)


def build_hitl_interaction_evidence_287(
    approval_timing_contract: dict[str, Any],
    identity_contract: dict[str, Any],
    relay_contract: dict[str, Any],
    *,
    approval_request_hash: str,
    request_id: str,
    discord_user_id: str,
    discord_message_id: str,
    discord_interaction_id: str,
    component_custom_id: str,
    decision: str,
    decided_at: str,
    expires_at: str,
) -> dict[str, Any]:
    contract = validate_approval_timing_contract_286(approval_timing_contract)
    try:
        identity = _validate_identity_contract(identity_contract)
        relay = _validate_relay_contract(relay_contract, identity)
    except Exception as exc:  # noqa: BLE001 - normalize upstream error type.
        raise SpeculativeQuarantineValidationError(f"identity/relay upstream invalid: {exc}") from exc
    if identity["identity_contract_hash"] != contract["upstream_identity_contract_hash"]:
        raise SpeculativeQuarantineValidationError("identity contract hash does not match approval timing contract")
    if relay["relay_contract_hash"] != contract["upstream_relay_contract_hash"]:
        raise SpeculativeQuarantineValidationError("relay contract hash does not match approval timing contract")
    _require_hash(approval_request_hash, "approval_request_hash")
    _require_exact_id(request_id, "REQUEST-", "request_id")
    _require_snowflake(discord_user_id, "discord_user_id")
    _require_snowflake(discord_message_id, "discord_message_id")
    _require_snowflake(discord_interaction_id, "discord_interaction_id")
    _require_exact_id(component_custom_id, "BLK-HITL-", "component_custom_id")
    if decision not in _ALLOWED_INTERACTION_DECISIONS:
        raise SpeculativeQuarantineValidationError("decision must be a Discord HITL interaction decision")
    _require_timestamp_order(decided_at, expires_at, "decision_window")
    actor = build_identity_record_283(
        identity,
        record_kind="actor",
        record_id=f"ACTOR-DISCORD-{discord_user_id}",
        source_system_id="SOURCE-DISCORD",
        subject_hash=_subject_hash_for({"discord_user_id": discord_user_id}),
        created_at=decided_at,
        metadata={"external_ref": f"discord-user-{discord_user_id}", "purpose": "HITL interaction actor"},
    )
    approval = build_identity_record_283(
        identity,
        record_kind="approval",
        record_id=request_id.replace("REQUEST-", "APPROVAL-", 1),
        source_system_id="SOURCE-DISCORD",
        subject_hash=approval_request_hash,
        created_at=decided_at,
        metadata={"external_ref": f"discord-interaction-{discord_interaction_id}", "purpose": "HITL decision evidence"},
    )
    envelope = build_relay_envelope_284(
        relay,
        source_identity_record=approval,
        envelope_id=request_id.replace("REQUEST-", "RELAY-", 1),
        message_type="HITL_APPROVAL_SIGNAL",
        target_component="blk-req",
        payload_hash=approval_request_hash,
        created_at=decided_at,
        trace_identity_hashes=[actor["identity_hash"], approval["identity_hash"]],
        metadata={"purpose": "HITL component decision signal"},
    )
    package = {
        "status": "HITL_INTERACTION_IDENTITY_RELAY_EVIDENCE_READY",
        "markers": [
            "BLK_SYSTEM_287_HITL_INTERACTION_IDENTITY_RELAY_EVIDENCE_READY",
            "DISCORD_COMPONENT_DECISION_BOUND_TO_BLK_ID_AND_BLK_RELAY",
            "NO_LONG_COPY_PASTE_APPROVAL_REQUIRED",
        ],
        "approval_timing_contract_hash": contract["approval_timing_contract_hash"],
        "identity_contract_hash": identity["identity_contract_hash"],
        "relay_contract_hash": relay["relay_contract_hash"],
        "approval_request_hash": approval_request_hash,
        "request_id": request_id,
        "decision": decision,
        "discord_user_id": discord_user_id,
        "discord_message_id": discord_message_id,
        "discord_interaction_id": discord_interaction_id,
        "component_custom_id": component_custom_id,
        "decided_at": decided_at,
        "expires_at": expires_at,
        "discord_component_interaction": True,
        "long_copy_paste_required": False,
        "actor_identity_hash": actor["identity_hash"],
        "approval_identity_hash": approval["identity_hash"],
        "hitl_relay_hash": envelope["relay_hash"],
        "side_effects": dict(_INTERACTION_SIDE_EFFECTS),
    }
    package["hitl_interaction_hash"] = hash_package(package)
    return validate_hitl_interaction_evidence_287(package, contract)


def validate_hitl_interaction_evidence_287(
    interaction: dict[str, Any],
    approval_timing_contract: dict[str, Any],
) -> dict[str, Any]:
    contract = validate_approval_timing_contract_286(approval_timing_contract)
    package = _require_dict(interaction, "HITL interaction evidence")
    _require_allowed_keys(package, _INTERACTION_KEYS, "HITL interaction evidence")
    if package.get("status") != "HITL_INTERACTION_IDENTITY_RELAY_EVIDENCE_READY":
        raise SpeculativeQuarantineValidationError("HITL interaction evidence status mismatch")
    if "BLK_SYSTEM_287_HITL_INTERACTION_IDENTITY_RELAY_EVIDENCE_READY" not in package.get("markers", []):
        raise SpeculativeQuarantineValidationError("HITL interaction evidence marker missing")
    if package.get("approval_timing_contract_hash") != contract["approval_timing_contract_hash"]:
        raise SpeculativeQuarantineValidationError("HITL interaction evidence contract hash mismatch")
    if package.get("identity_contract_hash") != contract["upstream_identity_contract_hash"]:
        raise SpeculativeQuarantineValidationError("HITL interaction evidence identity hash mismatch")
    if package.get("relay_contract_hash") != contract["upstream_relay_contract_hash"]:
        raise SpeculativeQuarantineValidationError("HITL interaction evidence relay hash mismatch")
    _require_hash(package.get("approval_request_hash"), "HITL interaction approval_request_hash")
    _require_exact_id(package.get("request_id"), "REQUEST-", "HITL interaction request_id")
    _require_snowflake(package.get("discord_user_id"), "HITL interaction discord_user_id")
    _require_snowflake(package.get("discord_message_id"), "HITL interaction discord_message_id")
    _require_snowflake(package.get("discord_interaction_id"), "HITL interaction discord_interaction_id")
    _require_exact_id(package.get("component_custom_id"), "BLK-HITL-", "HITL interaction component_custom_id")
    if package.get("decision") not in _ALLOWED_INTERACTION_DECISIONS:
        raise SpeculativeQuarantineValidationError("HITL interaction evidence decision mismatch")
    _require_timestamp_order(package.get("decided_at"), package.get("expires_at"), "HITL interaction decision_window")
    if package.get("discord_component_interaction") is not True:
        raise SpeculativeQuarantineValidationError("HITL interaction must be a Discord component interaction")
    if package.get("long_copy_paste_required") is not False:
        raise SpeculativeQuarantineValidationError("HITL interaction must not require long copy paste")
    _require_hash(package.get("actor_identity_hash"), "HITL interaction actor_identity_hash")
    _require_hash(package.get("approval_identity_hash"), "HITL interaction approval_identity_hash")
    _require_hash(package.get("hitl_relay_hash"), "HITL interaction hitl_relay_hash")
    _require_exact_side_effects(package, _INTERACTION_SIDE_EFFECTS, "HITL interaction evidence")
    _require_hash_field(package, "hitl_interaction_hash", "HITL interaction evidence")
    _reject_laundering(package, "HITL interaction evidence")
    return _deepcopy(package)


def build_speculative_quarantine_evidence_288(
    approval_timing_contract: dict[str, Any],
    hitl_interaction: dict[str, Any],
    *,
    run_id: str,
    execution_timing_mode: str,
    state: str,
    target_hash_before_quarantine: str,
    manifest_hash: str,
    result_hash: str,
    report_hash: str,
    quarantine_workspace_id: str,
    started_at: str,
    completed_at: str,
    external_side_effects: dict[str, bool] | None = None,
) -> dict[str, Any]:
    contract = validate_approval_timing_contract_286(approval_timing_contract)
    interaction = validate_hitl_interaction_evidence_287(hitl_interaction, contract)
    _require_exact_id(run_id, "RUN-", "run_id")
    if execution_timing_mode not in _EXECUTION_TIMING_MODES:
        raise SpeculativeQuarantineValidationError("execution_timing_mode unsupported")
    if state != "QUARANTINE_COMPLETE_AWAITING_DECISION":
        raise SpeculativeQuarantineValidationError("state must be completed quarantine evidence")
    _require_hash(target_hash_before_quarantine, "target_hash_before_quarantine")
    _require_hash(manifest_hash, "manifest_hash")
    _require_hash(result_hash, "result_hash")
    _require_hash(report_hash, "report_hash")
    _require_exact_id(quarantine_workspace_id, "QUARANTINE-", "quarantine_workspace_id")
    _require_timestamp_order(started_at, completed_at, "quarantine_window")
    external = _require_default_external_side_effects(external_side_effects)
    pre_compute = execution_timing_mode == "speculative_quarantine"
    _require_quarantine_timing_claim(
        execution_timing_mode,
        started_at,
        interaction["decided_at"],
        "pre-approval compute",
    )
    package = {
        "status": "SPECULATIVE_QUARANTINE_EVIDENCE_READY",
        "markers": [
            "BLK_SYSTEM_288_SPECULATIVE_QUARANTINE_EVIDENCE_READY",
            "PRE_APPROVAL_COMPUTE_QUARANTINED_NOT_PROMOTED",
            "TARGET_REPO_UNCHANGED_BEFORE_DECISION",
        ],
        "approval_timing_contract_hash": contract["approval_timing_contract_hash"],
        "hitl_interaction_hash": interaction["hitl_interaction_hash"],
        "hitl_decision": interaction["decision"],
        "hitl_decided_at": interaction["decided_at"],
        "approval_request_hash": interaction["approval_request_hash"],
        "request_id": interaction["request_id"],
        "run_id": run_id,
        "execution_timing_mode": execution_timing_mode,
        "state": state,
        "target_hash_before_quarantine": target_hash_before_quarantine,
        "manifest_hash": manifest_hash,
        "result_hash": result_hash,
        "report_hash": report_hash,
        "quarantine_workspace_id": quarantine_workspace_id,
        "started_at": started_at,
        "completed_at": completed_at,
        "approval_expires_at": interaction["expires_at"],
        "pre_approval_compute_performed": pre_compute,
        "promotion_performed": False,
        "target_repo_mutated": False,
        "external_side_effects": external,
        "side_effects": dict(_QUARANTINE_SIDE_EFFECTS),
    }
    package["quarantine_evidence_hash"] = hash_package(package)
    return validate_speculative_quarantine_evidence_288(package, contract, interaction)


def validate_speculative_quarantine_evidence_288(
    quarantine: dict[str, Any],
    approval_timing_contract: dict[str, Any],
    hitl_interaction: dict[str, Any],
) -> dict[str, Any]:
    contract = validate_approval_timing_contract_286(approval_timing_contract)
    interaction = validate_hitl_interaction_evidence_287(hitl_interaction, contract)
    package = _require_dict(quarantine, "quarantine evidence")
    _require_allowed_keys(package, _QUARANTINE_KEYS, "quarantine evidence")
    if package.get("status") != "SPECULATIVE_QUARANTINE_EVIDENCE_READY":
        raise SpeculativeQuarantineValidationError("quarantine evidence status mismatch")
    if "BLK_SYSTEM_288_SPECULATIVE_QUARANTINE_EVIDENCE_READY" not in package.get("markers", []):
        raise SpeculativeQuarantineValidationError("quarantine evidence marker missing")
    if package.get("approval_timing_contract_hash") != contract["approval_timing_contract_hash"]:
        raise SpeculativeQuarantineValidationError("quarantine evidence contract hash mismatch")
    if package.get("hitl_interaction_hash") != interaction["hitl_interaction_hash"]:
        raise SpeculativeQuarantineValidationError("quarantine evidence interaction hash mismatch")
    if package.get("hitl_decision") != interaction["decision"]:
        raise SpeculativeQuarantineValidationError("quarantine evidence HITL decision mismatch")
    if package.get("hitl_decided_at") != interaction["decided_at"]:
        raise SpeculativeQuarantineValidationError("quarantine evidence HITL decided_at mismatch")
    if package.get("approval_request_hash") != interaction["approval_request_hash"]:
        raise SpeculativeQuarantineValidationError("quarantine evidence approval_request_hash mismatch")
    if package.get("request_id") != interaction["request_id"]:
        raise SpeculativeQuarantineValidationError("quarantine evidence request_id mismatch")
    _require_exact_id(package.get("run_id"), "RUN-", "quarantine evidence run_id")
    if package.get("execution_timing_mode") not in _EXECUTION_TIMING_MODES:
        raise SpeculativeQuarantineValidationError("quarantine evidence execution_timing_mode mismatch")
    if package.get("state") != "QUARANTINE_COMPLETE_AWAITING_DECISION":
        raise SpeculativeQuarantineValidationError("quarantine evidence state must be complete")
    for field in ("target_hash_before_quarantine", "manifest_hash", "result_hash", "report_hash"):
        _require_hash(package.get(field), f"quarantine evidence {field}")
    _require_exact_id(package.get("quarantine_workspace_id"), "QUARANTINE-", "quarantine evidence quarantine_workspace_id")
    _require_timestamp_order(package.get("started_at"), package.get("completed_at"), "quarantine evidence window")
    if package.get("approval_expires_at") != interaction["expires_at"]:
        raise SpeculativeQuarantineValidationError("quarantine evidence approval_expires_at mismatch")
    if package.get("pre_approval_compute_performed") is not (package.get("execution_timing_mode") == "speculative_quarantine"):
        raise SpeculativeQuarantineValidationError("quarantine evidence pre_approval_compute_performed mismatch")
    _require_quarantine_timing_claim(
        package.get("execution_timing_mode"),
        package.get("started_at"),
        package.get("hitl_decided_at"),
        "quarantine evidence",
    )
    if package.get("promotion_performed") is not False:
        raise SpeculativeQuarantineValidationError("quarantine evidence promotion_performed must remain false")
    if package.get("target_repo_mutated") is not False:
        raise SpeculativeQuarantineValidationError("quarantine evidence target_repo_mutated must remain false")
    _require_default_external_side_effects(package.get("external_side_effects"))
    _require_exact_side_effects(package, _QUARANTINE_SIDE_EFFECTS, "quarantine evidence")
    _require_hash_field(package, "quarantine_evidence_hash", "quarantine evidence")
    _reject_laundering(package, "quarantine evidence")
    return _deepcopy(package)


def build_promotion_or_purge_gate_289(
    approval_timing_contract: dict[str, Any],
    quarantine: dict[str, Any],
    hitl_interaction: dict[str, Any],
    *,
    decision: str,
    decided_at: str,
    target_hash_at_decision: str,
    selected_result_hash: str,
    policy_hash: str | None = None,
    policy_source_id: str | None = None,
    policy_operation_class: str | None = None,
    policy_scope_hash: str | None = None,
) -> dict[str, Any]:
    contract = validate_approval_timing_contract_286(approval_timing_contract)
    quarantine_package = _validate_quarantine_for_gate(quarantine, contract, hitl_interaction)
    if decision not in _ALLOWED_GATE_DECISIONS:
        raise SpeculativeQuarantineValidationError("decision unsupported for promotion/purge gate")
    _parse_timestamp(decided_at, "decided_at")
    _require_gate_not_before_evidence(decided_at, quarantine_package, "promotion/purge gate")
    _require_hash(target_hash_at_decision, "target_hash_at_decision")
    _require_hash(selected_result_hash, "selected_result_hash")
    _validate_policy_fields(decision, policy_hash, policy_source_id, policy_operation_class, policy_scope_hash)
    _require_gate_decision_matches_quarantine(decision, quarantine_package)
    if selected_result_hash != quarantine_package["result_hash"]:
        raise SpeculativeQuarantineValidationError("selected_result_hash must match quarantined result_hash")
    expires_at = quarantine_package["approval_expires_at"]
    outcome_state = _resolve_gate_outcome(
        decision=decision,
        decided_at=decided_at,
        approval_expires_at=expires_at,
        target_hash_before_quarantine=quarantine_package["target_hash_before_quarantine"],
        target_hash_at_decision=target_hash_at_decision,
    )
    promotion_gate_opened = outcome_state == "APPROVED_PROMOTED"
    purge_performed = _gate_purge_performed(outcome_state)
    purge_receipt_hash = None
    if purge_performed:
        purge_receipt_hash = _gate_purge_receipt_hash(
            quarantine_evidence_hash=quarantine_package["quarantine_evidence_hash"],
            outcome_state=outcome_state,
            target_hash_at_decision=target_hash_at_decision,
        )
    package = {
        "status": "PROMOTION_PURGE_STALE_GATE_READY",
        "markers": [
            "BLK_SYSTEM_289_PROMOTION_PURGE_STALE_GATE_READY",
            "APPROVE_PROMOTES_ONLY_EXACT_QUARANTINED_RESULT",
            "REJECT_EXPIRE_OR_STALE_TARGET_PURGES_QUARANTINE",
        ],
        "approval_timing_contract_hash": contract["approval_timing_contract_hash"],
        "quarantine_evidence_hash": quarantine_package["quarantine_evidence_hash"],
        "run_id": quarantine_package["run_id"],
        "decision": decision,
        "decided_at": decided_at,
        "approval_expires_at": expires_at,
        "target_hash_before_quarantine": quarantine_package["target_hash_before_quarantine"],
        "target_hash_at_decision": target_hash_at_decision,
        "selected_result_hash": selected_result_hash,
        "policy_hash": policy_hash,
        "policy_source_id": policy_source_id,
        "policy_operation_class": policy_operation_class,
        "policy_scope_hash": policy_scope_hash,
        "outcome_state": outcome_state,
        "promotion_gate_opened": promotion_gate_opened,
        "purge_performed": purge_performed,
        "purge_receipt_hash": purge_receipt_hash,
        "stale_target_blocked": outcome_state == "STALE_TARGET_HASH_BLOCKED",
        "durable_target_mutation_performed": False,
        "side_effects": dict(_GATE_SIDE_EFFECTS),
    }
    package["promotion_or_purge_gate_hash"] = hash_package(package)
    return validate_promotion_or_purge_gate_289(package, contract, quarantine_package, hitl_interaction)


def _validate_quarantine_for_gate(
    quarantine: dict[str, Any],
    approval_timing_contract: dict[str, Any],
    hitl_interaction: dict[str, Any],
) -> dict[str, Any]:
    contract = validate_approval_timing_contract_286(approval_timing_contract)
    interaction = validate_hitl_interaction_evidence_287(hitl_interaction, contract)
    package = validate_speculative_quarantine_evidence_288(quarantine, contract, interaction)
    if package.get("state") != "QUARANTINE_COMPLETE_AWAITING_DECISION":
        raise SpeculativeQuarantineValidationError("quarantine evidence must be complete before promotion/purge gate")
    return package


def validate_promotion_or_purge_gate_289(
    gate: dict[str, Any],
    approval_timing_contract: dict[str, Any],
    quarantine: dict[str, Any],
    hitl_interaction: dict[str, Any],
) -> dict[str, Any]:
    contract = validate_approval_timing_contract_286(approval_timing_contract)
    quarantine_package = _validate_quarantine_for_gate(quarantine, contract, hitl_interaction)
    package = _require_dict(gate, "promotion/purge gate")
    _require_allowed_keys(package, _GATE_KEYS, "promotion/purge gate")
    if package.get("status") != "PROMOTION_PURGE_STALE_GATE_READY":
        raise SpeculativeQuarantineValidationError("promotion/purge gate status mismatch")
    if "BLK_SYSTEM_289_PROMOTION_PURGE_STALE_GATE_READY" not in package.get("markers", []):
        raise SpeculativeQuarantineValidationError("promotion/purge gate marker missing")
    if package.get("approval_timing_contract_hash") != contract["approval_timing_contract_hash"]:
        raise SpeculativeQuarantineValidationError("promotion/purge gate contract hash mismatch")
    if package.get("quarantine_evidence_hash") != quarantine_package["quarantine_evidence_hash"]:
        raise SpeculativeQuarantineValidationError("promotion/purge gate quarantine_evidence_hash mismatch")
    if package.get("run_id") != quarantine_package["run_id"]:
        raise SpeculativeQuarantineValidationError("promotion/purge gate run_id mismatch")
    if package.get("decision") not in _ALLOWED_GATE_DECISIONS:
        raise SpeculativeQuarantineValidationError("promotion/purge gate decision mismatch")
    decision = package["decision"]
    _parse_timestamp(package.get("decided_at"), "promotion/purge gate decided_at")
    _require_gate_not_before_evidence(package.get("decided_at"), quarantine_package, "promotion/purge gate")
    if package.get("approval_expires_at") != quarantine_package["approval_expires_at"]:
        raise SpeculativeQuarantineValidationError("promotion/purge gate approval_expires_at mismatch")
    if package.get("target_hash_before_quarantine") != quarantine_package["target_hash_before_quarantine"]:
        raise SpeculativeQuarantineValidationError("promotion/purge gate target_hash_before_quarantine mismatch")
    _require_hash(package.get("target_hash_at_decision"), "promotion/purge gate target_hash_at_decision")
    if package.get("selected_result_hash") != quarantine_package["result_hash"]:
        raise SpeculativeQuarantineValidationError("promotion/purge gate selected_result_hash mismatch")
    _validate_policy_fields(
        decision,
        package.get("policy_hash"),
        package.get("policy_source_id"),
        package.get("policy_operation_class"),
        package.get("policy_scope_hash"),
    )
    _require_gate_decision_matches_quarantine(decision, quarantine_package)
    outcome = package.get("outcome_state")
    if outcome not in {
        "APPROVED_PROMOTED",
        "DRY_RUN_ONLY_PURGED",
        "REJECTED_PURGED",
        "EXPIRED_PURGED",
        "STALE_TARGET_HASH_BLOCKED",
    }:
        raise SpeculativeQuarantineValidationError("promotion/purge gate outcome_state mismatch")
    expected_outcome = _resolve_gate_outcome(
        decision=decision,
        decided_at=package["decided_at"],
        approval_expires_at=package["approval_expires_at"],
        target_hash_before_quarantine=quarantine_package["target_hash_before_quarantine"],
        target_hash_at_decision=package["target_hash_at_decision"],
    )
    if outcome != expected_outcome:
        raise SpeculativeQuarantineValidationError("promotion/purge gate outcome_state mismatch")
    if package.get("promotion_gate_opened") is not (outcome == "APPROVED_PROMOTED"):
        raise SpeculativeQuarantineValidationError("promotion/purge gate promotion_gate_opened mismatch")
    purge_expected = _gate_purge_performed(outcome)
    if package.get("purge_performed") is not purge_expected:
        raise SpeculativeQuarantineValidationError("promotion/purge gate purge_performed mismatch")
    if purge_expected:
        expected_receipt = _gate_purge_receipt_hash(
            quarantine_evidence_hash=quarantine_package["quarantine_evidence_hash"],
            outcome_state=outcome,
            target_hash_at_decision=package["target_hash_at_decision"],
        )
        if package.get("purge_receipt_hash") != expected_receipt:
            raise SpeculativeQuarantineValidationError("promotion/purge gate purge_receipt_hash mismatch")
    elif package.get("purge_receipt_hash") is not None:
        raise SpeculativeQuarantineValidationError("promotion/purge gate purge_receipt_hash must be null")
    if package.get("stale_target_blocked") is not (outcome == "STALE_TARGET_HASH_BLOCKED"):
        raise SpeculativeQuarantineValidationError("promotion/purge gate stale_target_blocked mismatch")
    if package.get("durable_target_mutation_performed") is not False:
        raise SpeculativeQuarantineValidationError("promotion/purge gate durable_target_mutation_performed must remain false")
    _require_exact_side_effects(package, _GATE_SIDE_EFFECTS, "promotion/purge gate")
    _require_hash_field(package, "promotion_or_purge_gate_hash", "promotion/purge gate")
    _reject_laundering(package, "promotion/purge gate")
    return _deepcopy(package)
