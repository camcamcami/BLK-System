"""BLK-SYSTEM-050 non-disposable L4 exact-target approval envelope.

This module validates whether a future non-disposable BLK-test L4 pilot
approval envelope is complete enough for human review. It never approves or
executes that pilot.
"""

from __future__ import annotations

import hashlib
import posixpath
import re
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

SPRINT = "BLK-SYSTEM-050"
ENVELOPE_READY = "NON_DISPOSABLE_L4_EXACT_TARGET_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME"
BLOCKED = "NON_DISPOSABLE_L4_EXACT_TARGET_APPROVAL_ENVELOPE_BLOCKED_NOT_RUNTIME"
SELECTED_FRONTIER = "blk_test_non_disposable_l4_run_ast_validation"
REQUEST_GATE_READY = "NON_DISPOSABLE_L4_PILOT_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME"

REQUIRED_ENVELOPE_KEYS = frozenset(
    {
        "selected_frontier",
        "target_repo_path",
        "source_subtree_path",
        "branch_or_worktree",
        "workspace_clone_path",
        "workspace_marker_nonce",
        "path_resolution_safety",
        "fixed_tool",
        "timeout_output_profile",
        "approval_id",
        "run_id",
        "issued_at",
        "expires_at",
        "operator_identity",
        "source_system",
        "cleanup_rollback_obligations",
        "operator_stop_control",
        "hostile_review_criteria",
        "excluded_authorities",
        "no_side_effects",
    }
)

REQUIRED_REQUEST_GATE_KEYS = frozenset(
    {
        "sprint",
        "decision",
        "runtime_approved",
        "non_disposable_runtime_executed",
        "requested_future_tool",
        "beo_publication",
        "rtm_status",
        "source_write_allowed",
        "protected_body_read_allowed",
        "production_mcp_authorized",
        "hostile_review_verdict",
        "final_verification",
        "artifact_sha256",
    }
)

EXPECTED_ARTIFACT_PATHS = {
    "request_gate_module": "python/blk_test_l4_evidence_trust_request_gate.py",
    "request_gate_tests": "python/test_blk_test_l4_evidence_trust_request_gate.py",
    "request_gate_boundary": "docs/BLK-052_blk-test-l4-evidence-trust-and-non-disposable-request-gate.md",
    "request_gate_closeout": "docs/outcomes/BLK-SYSTEM-049_sprint-closeout.md",
    "request_gate_review": "docs/reviews/BLK-SYSTEM-049_blk-test-l4-evidence-trust-request-gate-hostile-review.md",
}

EXPECTED_HOSTILE_REVIEW_CRITERIA = frozenset(
    {
        "approval inheritance",
        "target inheritance",
        "replay and expiry bypass",
        "single-frontier enforcement",
        "protected-body leakage",
        "BEO/RTM/publication/drift laundering",
    }
)

EXPECTED_EXCLUDED_AUTHORITIES = frozenset(
    {
        "production BLK-test MCP",
        "generic BLK-test MCP",
        "reusable BLK-test service startup",
        "live Codex execution",
        "source mutation",
        "protected BLK-req body reads",
        "BEO publication",
        "RTM generation",
        "drift rejection",
        "public ledger mutation",
        "signer/storage/rollback authority",
        "non-disposable runtime execution",
        "arbitrary shell and caller-supplied commands",
        "dynamic tool expansion",
        "package-manager/network/model/browser/cyber tooling",
        "protected body copying/parsing/hashing/summarizing/scanning/mutation/drift comparison",
        "runtime RTM drift rejection",
        "revocation/supersession/release authority",
        "Git mutation operations",
        "production isolation claims",
    }
)

REQUIRED_SIDE_EFFECT_FLAGS = frozenset(
    {
        "runtime_executed",
        "subprocess_started",
        "source_mutation_detected",
        "git_mutation_detected",
        "staging_allowed",
        "commit_allowed",
        "push_allowed",
        "reset_allowed",
        "checkout_allowed",
        "revert_allowed",
        "active_vault_read",
        "beo_published",
        "rtm_generated",
        "drift_rejected",
        "network_called",
        "package_manager_called",
        "model_service_called",
        "browser_tooling_called",
        "cyber_tooling_called",
        "production_isolation_claimed",
    }
)

RUNTIME_APPROVAL_KEY_RE = re.compile(r"(?:^|[_\-.\s])runtime(?:[_\-.\s])?(?:approval|approved|authorized|authorization)(?:$|[_\-.\s])", re.I)
CAMEL_RUNTIME_APPROVAL_RE = re.compile(r"runtime(?:Approval|Approved|Authorized|Authorization)")
FORBIDDEN_TEXT_PATTERNS = (
    re.compile(r"approved\s*for\s*live\s*execution", re.I),
    re.compile(r"authori[sz]es?\s+authoritative\s+BEO\s+publication", re.I),
    re.compile(r"authoritative\s+BEO\s+publication", re.I),
    re.compile(r"publish(?:ed|es)?\s+BEO", re.I),
    re.compile(r"runtime\s+RTM\s+generation", re.I),
    re.compile(r"RTM\s+generation\s+is\s+allowed", re.I),
    re.compile(r"coverage\s+truth", re.I),
    re.compile(r"drift\s+rejection\s+approved", re.I),
    re.compile(r"read\s+protected\s+BLK[- ]req\s+body", re.I),
    re.compile(r"protected\s+body\s+read", re.I),
    re.compile(r"production\s+BLK[- ]test\s+MCP\s+authorized", re.I),
    re.compile(r"generic\s+BLK[- ]test\s+MCP\s+authorized", re.I),
    re.compile(r"source\s+mutation\s+allowed", re.I),
    re.compile(r"git\s+mutation\s+allowed", re.I),
    re.compile(r"package[- ]manager\s+allowed", re.I),
    re.compile(r"network\s+allowed", re.I),
    re.compile(r"model\s+service\s+allowed", re.I),
    re.compile(r"browser\s+tooling\s+allowed", re.I),
    re.compile(r"cyber\s+tooling\s+allowed", re.I),
    re.compile(r"production\s+isolation\s+enforced", re.I),
    re.compile(r"APPROVED_FOR_LIVE_EXECUTION"),
    re.compile(r"runtime\s+execution\s+is\s+authori[sz]ed", re.I),
    re.compile(r"runtime\s+approval\s+granted", re.I),
    re.compile(r"runtime\s+approval\s*:", re.I),
    re.compile(r"runtime\s+authorized", re.I),
    re.compile(r"live\s+execution\s+authorized", re.I),
    re.compile(r"approved\s+for\s+runtime", re.I),
    re.compile(r"selected[_-]?frontier\s*[=:]", re.I),
    re.compile(r"secondary\s+frontier", re.I),
    re.compile(r"production[_-]?mcp[_-]?authority", re.I),
    re.compile(r"runtime[-_\s]+execution[-_\s]+authori[sz]ed", re.I),
    re.compile(r"codex[_-]live[_-]dispatch[_-]l3[_-]smoke", re.I),
    re.compile(r"live[-_\s]+dispatch", re.I),
    re.compile(r"also\s+select", re.I),
)
PROTECTED_PATH_PARTS = {"active", "requirements", "use_cases", ".ssh", ".env", "secrets", "private"}


def evaluate_non_disposable_l4_exact_target_approval_envelope(
    *,
    request_gate_evidence: dict[str, Any],
    approval_envelope: dict[str, Any],
    evidence_artifacts: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate a non-runtime approval envelope for later human review."""

    _reject_runtime_approval_keys(request_gate_evidence, allowed_false_keys={"runtime_approved"})
    _reject_runtime_approval_keys(approval_envelope)
    _reject_laundering(request_gate_evidence)
    _reject_laundering(approval_envelope, skip_exact_sets=True)

    errors: list[str] = []
    errors.extend(_validate_request_gate_evidence(request_gate_evidence))
    errors.extend(_validate_envelope(approval_envelope))
    errors.extend(_validate_evidence_artifacts(evidence_artifacts))
    errors.extend(_validate_request_artifact_binding(request_gate_evidence, evidence_artifacts))

    decision = BLOCKED if errors else ENVELOPE_READY
    side_effects = approval_envelope.get("no_side_effects") if isinstance(approval_envelope, dict) else {}
    return {
        "sprint": SPRINT,
        "decision": decision,
        "errors": errors,
        "selected_frontier": approval_envelope.get("selected_frontier") if isinstance(approval_envelope, dict) else None,
        "runtime_approved": False,
        "non_disposable_runtime_executed": False,
        "subprocess_started": False,
        "requested_future_tool": approval_envelope.get("fixed_tool") if isinstance(approval_envelope, dict) else None,
        "beo_publication": "DRAFT_ONLY",
        "rtm_status": "NOT_GENERATED",
        "source_write_allowed": False,
        "protected_body_read_allowed": False,
        "production_mcp_authorized": False,
        "approval_envelope": deepcopy(approval_envelope) if isinstance(approval_envelope, dict) else {},
    }


def _validate_request_gate_evidence(evidence: dict[str, Any]) -> list[str]:
    if not isinstance(evidence, dict):
        return ["request_gate_evidence must be a dict"]
    errors: list[str] = []
    keys = set(evidence)
    missing = sorted(REQUIRED_REQUEST_GATE_KEYS - keys)
    extra = sorted(keys - REQUIRED_REQUEST_GATE_KEYS)
    errors.extend(f"request_gate_evidence missing {key}" for key in missing)
    if extra:
        errors.append(f"request_gate_evidence unsupported keys: {extra}")
    expected = {
        "sprint": "BLK-SYSTEM-049",
        "decision": REQUEST_GATE_READY,
        "requested_future_tool": "run_ast_validation",
        "beo_publication": "DRAFT_ONLY",
        "rtm_status": "NOT_GENERATED",
        "hostile_review_verdict": "PASS after remediation",
    }
    for key, value in expected.items():
        if evidence.get(key) != value:
            errors.append(f"request_gate_evidence.{key} must be {value}")
    for key in (
        "runtime_approved",
        "non_disposable_runtime_executed",
        "source_write_allowed",
        "protected_body_read_allowed",
        "production_mcp_authorized",
    ):
        if evidence.get(key) is not False:
            errors.append(f"request_gate_evidence.{key} must be false")
    verification = str(evidence.get("final_verification", ""))
    if not re.fullmatch(r"Ran 616 tests( in [0-9]+(?:\.[0-9]+)?s)? — OK", verification):
        errors.append("request_gate_evidence.final_verification must be exact BLK-SYSTEM-049 full-suite OK summary")
    if any(marker in verification.upper().replace("-", " ").replace("_", " ") for marker in ("NOT OK", "FAILED", "ERROR", "SKIPPED")):
        errors.append("request_gate_evidence.final_verification contains failure marker")
    return errors


def _validate_envelope(envelope: dict[str, Any]) -> list[str]:
    if not isinstance(envelope, dict):
        return ["approval_envelope must be a dict"]
    errors: list[str] = []
    keys = set(envelope)
    missing = sorted(REQUIRED_ENVELOPE_KEYS - keys)
    extra = sorted(keys - REQUIRED_ENVELOPE_KEYS)
    errors.extend(f"approval_envelope missing {key}" for key in missing)
    if extra:
        errors.append(f"approval_envelope unsupported keys: {extra}")

    if envelope.get("selected_frontier") != SELECTED_FRONTIER:
        errors.append("selected_frontier must be exactly blk_test_non_disposable_l4_run_ast_validation")
    if envelope.get("fixed_tool") != "run_ast_validation":
        errors.append("fixed_tool must remain run_ast_validation")

    errors.extend(_validate_paths(envelope))
    errors.extend(_validate_path_resolution_safety(envelope.get("path_resolution_safety")))
    errors.extend(_validate_profile(envelope.get("timeout_output_profile")))
    errors.extend(_validate_replay_and_expiry(envelope))
    errors.extend(_validate_obligations(envelope))
    errors.extend(_validate_side_effects(envelope.get("no_side_effects")))
    return errors


def _validate_paths(envelope: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    normalized: dict[str, str] = {}
    for key in ("target_repo_path", "source_subtree_path", "workspace_clone_path"):
        value = envelope.get(key)
        if not isinstance(value, str):
            errors.append(f"{key} must be a string")
            continue
        lowered = value.lower()
        if any(marker in lowered for marker in ("${", "{target_repo_path}", "$target_repo", "same as", "inherit")):
            errors.append(f"{key} must not use inherited or templated path references")
        raw_parts = Path(value).parts
        norm = posixpath.normpath(value)
        normalized[key] = norm
        if ".." in raw_parts:
            errors.append(f"{key} must not contain traversal")
        if not value.startswith("/"):
            errors.append(f"{key} must be absolute")
        if norm == "/home/dad/BLK-System" or norm.startswith("/home/dad/BLK-System/"):
            errors.append(f"{key} must not target the BLK-System repo")
        if any(part in PROTECTED_PATH_PARTS for part in Path(norm).parts):
            errors.append(f"{key} must not name protected or secret paths")
    target = normalized.get("target_repo_path", "")
    source = normalized.get("source_subtree_path", "")
    workspace = normalized.get("workspace_clone_path", "")
    if target and source and not source.startswith(target.rstrip("/") + "/"):
        errors.append("source_subtree_path must be inside target_repo_path")
    if workspace and target and (workspace == target or workspace.startswith(target.rstrip("/") + "/")):
        errors.append("workspace_clone_path must be outside target_repo_path")
    if workspace and source and (workspace == source or workspace.startswith(source.rstrip("/") + "/")):
        errors.append("workspace_clone_path must be outside source_subtree_path")
    branch = envelope.get("branch_or_worktree")
    if not isinstance(branch, str) or not re.fullmatch(r"[A-Za-z0-9._/-]+@[0-9a-f]{40}", branch):
        errors.append("branch_or_worktree must include branch@40hex")
    elif ".." in branch or any(marker in branch.lower() for marker in ("${", "$target", "same as", "inherit")):
        errors.append("branch_or_worktree must not contain traversal or inherited references")
    nonce = envelope.get("workspace_marker_nonce")
    if not isinstance(nonce, str) or not re.fullmatch(r"nonce-BLK-SYSTEM-050-[A-Za-z0-9_-]{16,}", nonce):
        errors.append("workspace_marker_nonce must be BLK-SYSTEM-050 nonce")
    return errors


def _validate_path_resolution_safety(value: Any) -> list[str]:
    expected = {
        "resolved_paths_prechecked": True,
        "symlink_descendants_rejected": True,
        "workspace_cleanup_bound_to_nonce": True,
    }
    if not isinstance(value, dict):
        return ["path_resolution_safety must be a dict"]
    if value != expected:
        return ["path_resolution_safety must contain exact resolved-path, symlink, and nonce cleanup proofs"]
    return []


def _validate_profile(profile: Any) -> list[str]:
    if not isinstance(profile, dict):
        return ["timeout_output_profile must be a dict"]
    errors: list[str] = []
    if set(profile) != {"timeout_seconds", "output_byte_limit"}:
        errors.append("timeout_output_profile keys must be exact")
    timeout = profile.get("timeout_seconds")
    output = profile.get("output_byte_limit")
    if not isinstance(timeout, int) or not 1 <= timeout <= 120:
        errors.append("timeout_seconds must be between 1 and 120")
    if not isinstance(output, int) or not 1 <= output <= 65536:
        errors.append("output_byte_limit must be between 1 and 65536")
    return errors


def _validate_replay_and_expiry(envelope: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    approval_id = envelope.get("approval_id")
    run_id = envelope.get("run_id")
    if not isinstance(approval_id, str) or not re.fullmatch(r"BLK-SYSTEM-050-APPROVAL-REQUEST-[0-9]{4}", approval_id):
        errors.append("approval_id must be a BLK-SYSTEM-050 approval request id")
    elif approval_id.endswith("-0000"):
        errors.append("approval_id must not use placeholder 0000")
    if not isinstance(run_id, str) or not re.fullmatch(r"BLK-SYSTEM-050-RUN-REQUEST-[0-9]{4}", run_id):
        errors.append("run_id must be a BLK-SYSTEM-050 run request id")
    elif run_id.endswith("-0000"):
        errors.append("run_id must not use placeholder 0000")
    if approval_id == run_id:
        errors.append("approval_id and run_id must be distinct")
    issued = _parse_iso(envelope.get("issued_at"), "issued_at", errors)
    expires = _parse_iso(envelope.get("expires_at"), "expires_at", errors)
    if issued and expires:
        if issued.tzinfo is None or issued.utcoffset() is None or expires.tzinfo is None or expires.utcoffset() is None:
            errors.append("issued_at and expires_at must include timezone offsets")
        if expires <= issued:
            errors.append("expires_at must be after issued_at")
        if (expires - issued).total_seconds() > 3600:
            errors.append("approval envelope TTL must not exceed 3600 seconds")
    for key in ("operator_identity", "source_system", "operator_stop_control"):
        if not isinstance(envelope.get(key), str) or not envelope.get(key):
            errors.append(f"{key} must be a non-empty string")
    return errors


def _parse_iso(value: Any, key: str, errors: list[str]) -> datetime | None:
    if not isinstance(value, str):
        errors.append(f"{key} must be an ISO timestamp string")
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        errors.append(f"{key} must be an ISO timestamp")
        return None


def _validate_obligations(envelope: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    obligations = envelope.get("cleanup_rollback_obligations")
    required_obligations = {
        "delete wrapper-owned workspace after run",
        "preserve target repository read-only",
        "record non-success evidence on timeout or output cap",
    }
    if not isinstance(obligations, list) or set(obligations) != required_obligations:
        errors.append("cleanup_rollback_obligations must match exact required obligations")
    criteria = envelope.get("hostile_review_criteria")
    if not isinstance(criteria, list) or set(criteria) != EXPECTED_HOSTILE_REVIEW_CRITERIA:
        errors.append("hostile_review_criteria must match exact criteria set")
    excluded = envelope.get("excluded_authorities")
    if not isinstance(excluded, list) or set(excluded) != EXPECTED_EXCLUDED_AUTHORITIES:
        errors.append("excluded_authorities must match exact denial set")
    return errors


def _validate_side_effects(side_effects: Any) -> list[str]:
    if not isinstance(side_effects, dict):
        return ["no_side_effects must be a dict"]
    errors: list[str] = []
    keys = set(side_effects)
    if keys != REQUIRED_SIDE_EFFECT_FLAGS:
        errors.append("no_side_effects keys must be exact")
    for key in REQUIRED_SIDE_EFFECT_FLAGS:
        if side_effects.get(key) is not False:
            errors.append(f"no_side_effects.{key} must be false")
    return errors


def _validate_evidence_artifacts(artifacts: dict[str, Any] | None) -> list[str]:
    if not isinstance(artifacts, dict):
        return ["evidence_artifacts must be a dict"]
    errors: list[str] = []
    keys = set(artifacts)
    expected = set(EXPECTED_ARTIFACT_PATHS)
    if keys != expected:
        errors.append("evidence_artifacts keys must match expected request-gate artifacts")
    for key, rel in EXPECTED_ARTIFACT_PATHS.items():
        descriptor = artifacts.get(key)
        if not isinstance(descriptor, dict):
            errors.append(f"artifact {key} descriptor missing")
            continue
        if set(descriptor) != {"path", "sha256"}:
            errors.append(f"artifact {key} descriptor keys must be exact")
        if descriptor.get("path") != rel:
            errors.append(f"artifact {key} path must be {rel}")
            continue
        path = Path(rel)
        if not (ROOT / path).exists():
            errors.append(f"artifact {key} path missing")
            continue
        actual = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        if descriptor.get("sha256") != actual:
            errors.append(f"artifact {key} sha256 mismatch")
    return errors


def _validate_request_artifact_binding(evidence: dict[str, Any], artifacts: dict[str, Any] | None) -> list[str]:
    if not isinstance(evidence, dict) or not isinstance(artifacts, dict):
        return []
    bound = evidence.get("artifact_sha256")
    if not isinstance(bound, dict):
        return ["request_gate_evidence.artifact_sha256 must bind expected artifacts"]
    errors: list[str] = []
    if set(bound) != set(EXPECTED_ARTIFACT_PATHS):
        errors.append("request_gate_evidence.artifact_sha256 keys must match expected artifacts")
    for key in EXPECTED_ARTIFACT_PATHS:
        descriptor = artifacts.get(key)
        if not isinstance(descriptor, dict):
            continue
        if bound.get(key) != descriptor.get("sha256"):
            errors.append(f"request_gate_evidence artifact binding mismatch for {key}")
    return errors


def _reject_runtime_approval_keys(value: Any, *, allowed_false_keys: set[str] | None = None) -> None:
    allowed_false_keys = allowed_false_keys or set()
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key)
            if key_text in allowed_false_keys:
                continue
            normalized = re.sub(r"[^a-z0-9]+", " ", key_text.lower())
            compact = re.sub(r"[^A-Za-z0-9]", "", key_text)
            if RUNTIME_APPROVAL_KEY_RE.search(key_text) or CAMEL_RUNTIME_APPROVAL_RE.search(key_text):
                raise ValueError(f"runtime approval key forbidden: {key_text}")
            if "runtime" in normalized and any(term in normalized for term in ("approval", "approved", "authorized", "authorization")):
                raise ValueError(f"runtime approval key forbidden: {key_text}")
            if compact.lower() in {"runtimeapproval", "runtimeapproved", "runtimeauthorized", "runtimeauthorization"}:
                raise ValueError(f"runtime approval key forbidden: {key_text}")
            _reject_runtime_approval_keys(nested, allowed_false_keys=allowed_false_keys)
    elif isinstance(value, list):
        for nested in value:
            _reject_runtime_approval_keys(nested, allowed_false_keys=allowed_false_keys)


def _reject_laundering(value: Any, *, skip_exact_sets: bool = False) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            if skip_exact_sets and key in {"excluded_authorities", "hostile_review_criteria"}:
                continue
            _reject_laundering(nested, skip_exact_sets=skip_exact_sets)
    elif isinstance(value, list):
        for nested in value:
            _reject_laundering(nested, skip_exact_sets=skip_exact_sets)
    elif isinstance(value, str):
        normalized = re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()
        compact = re.sub(r"[^a-z0-9]+", "", value.lower())
        normalized_pairs = (
            "runtime approval",
            "runtime authorized",
            "live execution authorized",
            "approved for runtime",
            "secondary frontier",
            "selected frontier",
        )
        compact_pairs = (
            "runtimeapproval",
            "runtimeauthorized",
            "liveexecutionauthorized",
            "approvedforruntime",
            "secondaryfrontier",
            "selectedfrontier",
        )
        if any(pair in normalized for pair in normalized_pairs) or any(pair in compact for pair in compact_pairs):
            raise ValueError("forbidden authority marker: normalized runtime/frontier wording")
        for pattern in FORBIDDEN_TEXT_PATTERNS:
            if pattern.search(value):
                raise ValueError(f"forbidden authority marker: {pattern.pattern}")
