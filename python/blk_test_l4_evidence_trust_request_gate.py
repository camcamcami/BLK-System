"""BLK-SYSTEM-049 evidence-trust request gate.

This module evaluates whether BLK-SYSTEM-048 disposable L4 runtime evidence is
trustworthy enough to request human review for a later non-disposable exact-target
L4 pilot. It never approves or executes that later pilot.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

SPRINT = "BLK-SYSTEM-049"
REQUEST_READY = "NON_DISPOSABLE_L4_PILOT_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME"
BLOCKED = "NON_DISPOSABLE_L4_PILOT_REQUEST_BLOCKED_NOT_RUNTIME"
REQUIRED_PROPOSAL_KEYS = frozenset(
    {
        "target_repo_path",
        "source_subtree_path",
        "branch_or_worktree",
        "workspace_clone_path",
        "workspace_marker_nonce",
        "fixed_tool",
        "timeout_output_profile",
        "replay_policy",
        "approval_window",
        "operator_identity",
        "source_system",
        "cleanup_rollback_obligations",
        "operator_stop_control",
        "hostile_review_criteria",
        "excluded_authorities",
    }
)
REQUIRED_EVIDENCE_FALSE = (
    "source_mutation_detected",
    "git_mutation_detected",
    "source_write_allowed",
    "staging_allowed",
    "commit_allowed",
    "push_allowed",
    "active_vault_read",
    "production_isolation_claimed",
    "network_called",
    "model_service_called",
    "browser_tooling_called",
    "cyber_tooling_called",
    "package_manager_called",
    "arbitrary_shell_called",
)
FORBIDDEN_MARKERS = (
    "authorizes",
    "approved for runtime",
    "runtime approval",
    "beo publication",
    "publish beo",
    "rtm generation",
    "drift rejection",
    "coverage truth",
    "protected body",
    "protected blk req",
    "production blk test mcp",
    "generic blk test mcp",
    "source mutation",
    "git mutation",
    "arbitrary shell",
    "package manager",
    "network",
    "model service",
    "browser",
    "cyber",
    "production isolation",
)


def evaluate_l4_evidence_trust_request_gate(
    *,
    disposable_runtime_evidence: dict[str, Any],
    hostile_review: dict[str, Any],
    final_verification: dict[str, Any],
    future_target_proposal: dict[str, Any],
) -> dict[str, Any]:
    _reject_laundering(disposable_runtime_evidence)
    _reject_laundering(hostile_review)
    _reject_laundering(final_verification)
    _reject_laundering(future_target_proposal)
    proposal_errors = _validate_future_target_proposal(future_target_proposal)
    evidence_errors = _validate_disposable_evidence(disposable_runtime_evidence)
    review_errors = _validate_hostile_review(hostile_review)
    verification_errors = _validate_final_verification(final_verification)
    errors = evidence_errors + review_errors + verification_errors + proposal_errors
    decision = BLOCKED if errors else REQUEST_READY
    return {
        "sprint": SPRINT,
        "decision": decision,
        "errors": errors,
        "runtime_approved": False,
        "non_disposable_runtime_executed": False,
        "requested_future_tool": future_target_proposal.get("fixed_tool") if isinstance(future_target_proposal, dict) else None,
        "beo_publication": "DRAFT_ONLY",
        "rtm_status": "NOT_GENERATED",
        "source_write_allowed": False,
        "protected_body_read_allowed": False,
        "production_mcp_authorized": False,
        "future_target_proposal": deepcopy(future_target_proposal) if isinstance(future_target_proposal, dict) else {},
    }


def _validate_disposable_evidence(evidence: dict[str, Any]) -> list[str]:
    if not isinstance(evidence, dict):
        return ["disposable_runtime_evidence must be a dict"]
    errors: list[str] = []
    expected = {
        "sprint": "BLK-SYSTEM-048",
        "pilot_status": "BLK_TEST_L4_DISPOSABLE_REPO_PASS_EVIDENCE_ONLY",
        "status": "PASS",
        "requested_tool": "run_ast_validation",
        "runtime_target_class": "disposable_real_git_repository",
        "beo_publication": "DRAFT_ONLY",
        "rtm_status": "NOT_GENERATED",
    }
    for key, value in expected.items():
        if evidence.get(key) != value:
            errors.append(f"evidence.{key} must be {value}")
    if evidence.get("replay_consumed") is not True or evidence.get("fixed_tool_executed") is not True:
        errors.append("evidence must show replay consumed and fixed tool executed")
    for key in REQUIRED_EVIDENCE_FALSE:
        if evidence.get(key) is not False:
            errors.append(f"evidence.{key} must be false")
    if not isinstance(evidence.get("output_byte_limit"), int) or not isinstance(evidence.get("evidence_json_bytes"), int):
        errors.append("evidence output bounds must be numeric")
    elif evidence["evidence_json_bytes"] > evidence["output_byte_limit"]:
        errors.append("evidence_json_bytes must not exceed output_byte_limit")
    return errors


def _validate_hostile_review(review: dict[str, Any]) -> list[str]:
    if not isinstance(review, dict):
        return ["hostile_review must be a dict"]
    errors: list[str] = []
    if review.get("verdict") != "PASS after remediation":
        errors.append("hostile_review.verdict must be PASS after remediation")
    if review.get("blockers_remediated") is not True:
        errors.append("hostile_review.blockers_remediated must be true")
    scope = review.get("review_scope")
    required = {"replay ordering", "fake Git identity", "output cap enforcement", "authority laundering", "protected-body leakage"}
    if not isinstance(scope, list) or not required.issubset(set(scope)):
        errors.append("hostile_review.review_scope missing required blocker classes")
    return errors


def _validate_final_verification(verification: dict[str, Any]) -> list[str]:
    if not isinstance(verification, dict):
        return ["final_verification must be a dict"]
    errors: list[str] = []
    for key in ("python_unittest_discovery", "focused_runtime_tests"):
        if "OK" not in str(verification.get(key, "")):
            errors.append(f"final_verification.{key} must be OK")
    for key in ("go_test", "go_vet", "git_diff_check"):
        if verification.get(key) != "PASS":
            errors.append(f"final_verification.{key} must be PASS")
    return errors


def _validate_future_target_proposal(proposal: dict[str, Any]) -> list[str]:
    if not isinstance(proposal, dict):
        return ["future_target_proposal must be a dict"]
    if proposal.get("runtime_approval") is True or proposal.get("runtime_approved") is True:
        raise ValueError("future target proposal must not contain runtime approval")
    keys = set(proposal)
    missing = sorted(REQUIRED_PROPOSAL_KEYS - keys)
    extra = sorted(keys - REQUIRED_PROPOSAL_KEYS - {"notes"})
    errors = [f"future_target_proposal missing {key}" for key in missing]
    if extra:
        errors.append(f"future_target_proposal unsupported keys: {extra}")
    if proposal.get("fixed_tool") not in (None, "run_ast_validation"):
        raise ValueError("fixed_tool must remain run_ast_validation")
    for key in REQUIRED_PROPOSAL_KEYS:
        if key in proposal and proposal[key] in ("", None, [], {}):
            errors.append(f"future_target_proposal.{key} must be non-empty")
    profile = proposal.get("timeout_output_profile", {})
    if isinstance(profile, dict):
        if not isinstance(profile.get("timeout_seconds"), int) or profile.get("timeout_seconds", 0) <= 0:
            errors.append("timeout_seconds must be positive")
        if not isinstance(profile.get("output_byte_limit"), int) or profile.get("output_byte_limit", 0) < 512:
            errors.append("output_byte_limit must be at least 512")
    return errors


def _reject_laundering(value: Any) -> None:
    if isinstance(value, dict):
        for item in value.values():
            _reject_laundering(item)
    elif isinstance(value, (list, tuple, set)):
        for item in value:
            _reject_laundering(item)
    elif isinstance(value, str):
        normalized = value.casefold().replace("_", " ").replace("-", " ")
        allowed_exact = {
            "blk system 048",
            "blk test l4 disposable repo pass evidence only".replace("_", " "),
            "pass",
            "run ast validation",
            "disposable real git repository",
            "draft only",
            "not generated",
            "pass after remediation",
            "ran 603 tests — ok",
            "ran 10 tests — ok",
            "operator:camcamcami",
            "discord dm",
            "replay ordering",
            "fake git identity",
            "output cap enforcement",
            "authority laundering",
            "protected body leakage",
            "protected-body leakage",
            "remove workspace clone",
            "preserve source repo read only",
            "discord stop command before runtime starts",
            "protected blk req body reads",
            "production blk test mcp",
            "generic blk test mcp",
            "source mutation",
            "beo publication",
            "rtm generation",
            "drift rejection",
        }
        if normalized in allowed_exact:
            return
        for marker in FORBIDDEN_MARKERS:
            if marker in normalized:
                raise ValueError(f"forbidden authority marker: {marker}")
