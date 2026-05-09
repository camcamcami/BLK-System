"""BLK-SYSTEM-049 evidence-trust request gate.

This module evaluates whether BLK-SYSTEM-048 disposable L4 runtime evidence is
trustworthy enough to request human review for a later non-disposable exact-target
L4 pilot. It never approves or executes that later pilot.
"""

from __future__ import annotations

import hashlib
import posixpath
import re
from copy import deepcopy
from pathlib import Path
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
EXPECTED_ARTIFACT_PATHS = {
    "runtime_module": "python/blk_test_fixed_tool_l4_disposable_repo_runtime.py",
    "runtime_tests": "python/test_blk_test_fixed_tool_l4_disposable_repo_runtime.py",
    "review_document": "docs/reviews/BLK-SYSTEM-048_blk-test-fixed-tool-l4-disposable-real-repo-runtime-hostile-review.md",
    "closeout_document": "docs/outcomes/BLK-SYSTEM-048_sprint-closeout.md",
    "boundary_document": "docs/BLK-051_blk-test-fixed-tool-l4-disposable-real-repo-runtime-boundary.md",
}
REQUIRED_REPLAY_POLICY_KEYS = {"approval_id_required", "run_id_required"}
REQUIRED_APPROVAL_WINDOW_KEYS = {"issued_at_required", "expires_at_required"}
ALLOWED_HOSTILE_REVIEW_CRITERIA = {"authority laundering", "protected-body leakage", "source mutation"}
ALLOWED_EXCLUDED_AUTHORITIES = {
    "production BLK-test MCP",
    "generic BLK-test MCP",
    "source mutation",
    "protected BLK-req body reads",
    "BEO publication",
    "RTM generation",
    "drift rejection",
}

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
    evidence_artifacts: dict[str, Any] | None = None,
) -> dict[str, Any]:
    for value in (disposable_runtime_evidence, hostile_review, final_verification, future_target_proposal):
        _reject_runtime_approval_keys(value)
        _reject_laundering(value)
    proposal_errors = _validate_future_target_proposal(future_target_proposal)
    evidence_errors = _validate_disposable_evidence(disposable_runtime_evidence)
    review_errors = _validate_hostile_review(hostile_review)
    verification_errors = _validate_final_verification(final_verification)
    artifact_errors = _validate_evidence_artifacts(evidence_artifacts)
    errors = evidence_errors + review_errors + verification_errors + proposal_errors + artifact_errors
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
    if not isinstance(scope, list) or set(scope) != required:
        errors.append("hostile_review.review_scope must match exact blocker classes")
    return errors


def _validate_final_verification(verification: dict[str, Any]) -> list[str]:
    if not isinstance(verification, dict):
        return ["final_verification must be a dict"]
    errors: list[str] = []
    for key in ("python_unittest_discovery", "focused_runtime_tests"):
        value = str(verification.get(key, ""))
        if not re.fullmatch(r"Ran [1-9][0-9]* tests( in [0-9.]+s)? — OK", value):
            errors.append(f"final_verification.{key} must be an exact nonzero OK test summary")
        if any(marker in value.upper().replace("-", " ").replace("_", " ") for marker in ("NOT OK", "FAILED", "ERROR", "SKIPPED", "GARBAGE")):
            errors.append(f"final_verification.{key} contains failure marker")
    for key in ("go_test", "go_vet", "git_diff_check"):
        if verification.get(key) != "PASS":
            errors.append(f"final_verification.{key} must be PASS")
    return errors


def _validate_future_target_proposal(proposal: dict[str, Any]) -> list[str]:
    if not isinstance(proposal, dict):
        return ["future_target_proposal must be a dict"]
    _reject_runtime_approval_keys(proposal)
    keys = set(proposal)
    missing = sorted(REQUIRED_PROPOSAL_KEYS - keys)
    extra = sorted(keys - REQUIRED_PROPOSAL_KEYS)
    errors = [f"future_target_proposal missing {key}" for key in missing]
    if extra:
        errors.append(f"future_target_proposal unsupported keys: {extra}")
    if proposal.get("fixed_tool") not in (None, "run_ast_validation"):
        raise ValueError("fixed_tool must remain run_ast_validation")
    for key in REQUIRED_PROPOSAL_KEYS:
        if key in proposal and proposal[key] in ("", None, [], {}):
            errors.append(f"future_target_proposal.{key} must be non-empty")
    for text_key in (
        "target_repo_path",
        "source_subtree_path",
        "branch_or_worktree",
        "workspace_clone_path",
        "workspace_marker_nonce",
        "operator_identity",
        "source_system",
        "operator_stop_control",
    ):
        if text_key in proposal and not isinstance(proposal[text_key], str):
            errors.append(f"future_target_proposal.{text_key} must be a string")
    normalized_paths: dict[str, str] = {}
    for path_key in ("target_repo_path", "source_subtree_path", "workspace_clone_path"):
        value = str(proposal.get(path_key, ""))
        raw_parts = Path(value).parts
        normalized = posixpath.normpath(value)
        normalized_paths[path_key] = normalized
        if ".." in raw_parts:
            errors.append(f"future_target_proposal.{path_key} must not contain traversal")
        if not value.startswith("/"):
            errors.append(f"future_target_proposal.{path_key} must be an absolute path")
        if normalized == "/home/dad/BLK-System" or normalized.startswith("/home/dad/BLK-System/"):
            errors.append(f"future_target_proposal.{path_key} must not target the BLK-System repo")
        parts = Path(normalized).parts
        if any(part in {"active", "requirements", "use_cases", ".ssh", ".env"} for part in parts):
            errors.append(f"future_target_proposal.{path_key} must not name protected or secret paths")
    target = normalized_paths.get("target_repo_path", "")
    source = normalized_paths.get("source_subtree_path", "")
    workspace = normalized_paths.get("workspace_clone_path", "")
    if workspace in {target, source} or workspace.startswith(target.rstrip("/") + "/") or workspace.startswith(source.rstrip("/") + "/"):
        errors.append("workspace_clone_path must be separate from target/source paths")
    profile = proposal.get("timeout_output_profile")
    if not isinstance(profile, dict):
        errors.append("timeout_output_profile must be a dict")
    else:
        if set(profile) != {"timeout_seconds", "output_byte_limit"}:
            errors.append("timeout_output_profile keys must be exact")
        if not isinstance(profile.get("timeout_seconds"), int) or profile.get("timeout_seconds", 0) <= 0:
            errors.append("timeout_seconds must be positive")
        if not isinstance(profile.get("output_byte_limit"), int) or profile.get("output_byte_limit", 0) < 512:
            errors.append("output_byte_limit must be at least 512")
    replay_policy = proposal.get("replay_policy")
    if not isinstance(replay_policy, dict):
        errors.append("replay_policy must be a dict")
    elif set(replay_policy) != REQUIRED_REPLAY_POLICY_KEYS or any(value is not True for value in replay_policy.values()):
        errors.append("replay_policy keys must be exact approval_id_required/run_id_required true values")
    approval_window = proposal.get("approval_window")
    if not isinstance(approval_window, dict):
        errors.append("approval_window must be a dict")
    elif set(approval_window) != REQUIRED_APPROVAL_WINDOW_KEYS or any(value is not True for value in approval_window.values()):
        errors.append("approval_window keys must be exact issued_at_required/expires_at_required true values")
    criteria = proposal.get("hostile_review_criteria")
    if not isinstance(criteria, list) or any(not isinstance(item, str) for item in criteria) or set(criteria) != ALLOWED_HOSTILE_REVIEW_CRITERIA:
        errors.append("hostile_review_criteria must match exact non-authority review criteria")
    excluded = proposal.get("excluded_authorities")
    if not isinstance(excluded, list) or any(not isinstance(item, str) for item in excluded) or set(excluded) != ALLOWED_EXCLUDED_AUTHORITIES:
        errors.append("excluded_authorities must match exact denied-authority set")
    if proposal.get("cleanup_rollback_obligations") != ["remove workspace clone", "preserve source repo read-only"]:
        errors.append("cleanup_rollback_obligations must match exact non-runtime cleanup obligations")
    return errors



def _normalize_authority_token(text: str) -> str:
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    return re.sub(r"[^a-z0-9]+", " ", text.casefold()).strip()


def _reject_runtime_approval_keys(value: Any) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            normalized = _normalize_authority_token(str(key))
            if (
                "runtime" in normalized
                and (
                    "approval" in normalized
                    or "approved" in normalized
                    or "authorization" in normalized
                    or "authorized" in normalized
                )
            ) or normalized in {"approved", "authorized", "authorization"}:
                raise ValueError("future target proposal must not contain runtime approval")
            _reject_runtime_approval_keys(item)
    elif isinstance(value, (list, tuple, set)):
        for item in value:
            _reject_runtime_approval_keys(item)


def _validate_evidence_artifacts(artifacts: dict[str, Any] | None) -> list[str]:
    if not isinstance(artifacts, dict):
        return ["evidence_artifacts must be provided"]
    errors: list[str] = []
    required = {"runtime_module", "runtime_tests", "review_document", "closeout_document", "boundary_document"}
    if set(artifacts) != required:
        errors.append("evidence_artifacts keys must be exact")
        return errors
    for name, descriptor in artifacts.items():
        if not isinstance(descriptor, dict) or set(descriptor) != {"path", "sha256"}:
            errors.append(f"artifact {name} descriptor must contain path and sha256")
            continue
        rel = str(descriptor["path"])
        if rel != EXPECTED_ARTIFACT_PATHS[name]:
            errors.append(f"artifact {name} path must be {EXPECTED_ARTIFACT_PATHS[name]}")
            continue
        if rel.startswith("/") or ".." in Path(rel).parts:
            errors.append(f"artifact {name} path must be repo-relative")
            continue
        path = Path(rel)
        if not path.is_file():
            errors.append(f"artifact {name} path missing")
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if descriptor["sha256"] != digest:
            errors.append(f"artifact {name} sha256 mismatch")
    return errors


def _reject_laundering(value: Any) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "notes":
                _reject_laundering(item)
            elif key in {"excluded_authorities", "hostile_review_criteria", "review_scope", "cleanup_rollback_obligations"}:
                continue
            else:
                _reject_laundering(item)
    elif isinstance(value, (list, tuple, set)):
        for item in value:
            _reject_laundering(item)
    elif isinstance(value, str):
        normalized = _normalize_authority_token(value)
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
        }
        allowed_normalized = {_normalize_authority_token(item) for item in allowed_exact}
        if normalized in allowed_normalized:
            return
        for marker in FORBIDDEN_MARKERS:
            if _normalize_authority_token(marker) in normalized:
                raise ValueError(f"forbidden authority marker: {marker}")
