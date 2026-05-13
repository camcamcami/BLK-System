"""BLK-SYSTEM-097 bounded Kuronode workspace BLK-test evidence refresh.

This module implements exactly one evidence-only, read-only BLK-test functional
module refresh over the pinned Kuronode workspace target. It does not start
BLK-test MCP, invoke shell/tooling, mutate source/Git, publish BEOs, generate
RTM, or read protected BLK-req bodies.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from kuronode_power_of_ten_static_profile import evaluate_kuronode_power_of_ten_static_profile

SPRINT = "BLK-SYSTEM-097"
APPROVAL_ID = "APPROVAL-BLK-SYSTEM-097-KURONODE-EVIDENCE-REFRESH-001"
RUN_ID = "RUN-BLK-SYSTEM-097-KURONODE-EVIDENCE-REFRESH-001"
EXPECTED_HEAD = "aebea51bed911c781a537d84d38b2dcb838b1368"
APPROVED_TARGET_REPO = Path("/home/dad/code/Kuronode-v1")
APPROVED_SOURCE_SUBTREE = Path("/home/dad/code/Kuronode-v1/scripts")
APPROVED_WORKSPACE = Path("/tmp/blk-system-097-kuronode-evidence-refresh-workspace")
REPLAY_LEDGER_PATH = Path("/tmp/blk-system-097-kuronode-evidence-refresh-replay-ledger.json")
REQUESTED_TOOL = "run_ast_validation"
RUNTIME_AUTHORIZATION_STATUS = "BLK_SYSTEM_097_OPERATOR_AUTHORIZED_ONE_EXACT_EVIDENCE_REFRESH"
PASS_STATUS = "BLK_TEST_KURONODE_WORKSPACE_BOUNDED_EVIDENCE_REFRESH_PASS_EVIDENCE_ONLY"
FAIL_STATUS = "BLK_TEST_KURONODE_WORKSPACE_BOUNDED_EVIDENCE_REFRESH_FAIL_EVIDENCE_ONLY"
BLOCKED_STATUS = "BLK_TEST_KURONODE_WORKSPACE_BOUNDED_EVIDENCE_REFRESH_BLOCKED_EVIDENCE_ONLY"
MIN_OUTPUT_BYTE_LIMIT = 1024
MAX_LISTED_FILES = 80
MAX_FINDINGS = 40

PROOF_MARKERS = frozenset(
    {
        "USER_REQUESTED_EXECUTE_ALL_TASKS_FOR_BLK_SYSTEM_097",
        "OPERATOR_AUTHORIZED_BLK_SYSTEM_097_EXACT_EVIDENCE_REFRESH",
        "KURONODE_ORIGIN_MAIN_HEAD_RECHECKED",
        "READ_ONLY_RUN_AST_VALIDATION_ONLY",
        "REPLAY_CONSUMED_BEFORE_RUNTIME",
        "NO_SOURCE_OR_GIT_MUTATION_BY_BLK_TEST",
        "NO_PROTECTED_BODY_READ",
        "NO_BEO_RTM_COVERAGE_DRIFT_AUTHORITY",
    }
)

EXCLUDED_AUTHORITIES = frozenset(
    {
        "PRODUCTION_BLK_TEST_MCP",
        "GENERIC_BLK_TEST_MCP",
        "REUSABLE_BLK_TEST_SERVICE_STARTUP",
        "ARBITRARY_SHELL_OR_CALLER_SUPPLIED_COMMANDS",
        "DYNAMIC_TOOL_EXPANSION",
        "ELECTRON_OR_SMOKE_TEST_EXECUTION",
        "TYPESCRIPT_TOOLING_EXECUTION",
        "PACKAGE_MANAGER_INVOCATION",
        "NETWORK_ACCESS",
        "MODEL_SERVICE_ACCESS",
        "BROWSER_OR_CYBER_TOOLING",
        "KURONODE_SOURCE_MUTATION",
        "KURONODE_GIT_MUTATION",
        "KURONODE_REMOTE_PUSH",
        "CEB009_ARTIFACT_REUSE_AS_EXECUTABLE_FIXTURE",
        "BLK_TEST_AS_BLK_SYSTEM_TEST_SUITE_SEMANTICS",
        "PROTECTED_BLK_REQ_BODY_READ",
        "AUTHORITATIVE_BEO_PUBLICATION",
        "RUNTIME_PUBLISHED_BEO_OUTPUT",
        "RUNTIME_RTM_GENERATION",
        "RTM_DRIFT_REJECTION",
        "COVERAGE_MATRIX_OR_COVERAGE_CLAIM_PROMOTION",
        "ACTIVE_VAULT_HASH_COMPARISON",
        "PUBLIC_LEDGER_MUTATION",
        "SIGNER_STORAGE_ROLLBACK_REVOCATION_SUPERSESSION_OR_RELEASE_AUTHORITY",
        "PRODUCTION_SANDBOX_OR_HOST_SECRET_ISOLATION_CLAIM",
        "LIVE_CODEX_EXECUTION",
        "LIVE_TACTICAL_LLM_DISPATCH",
    }
)

NO_SIDE_EFFECT_FLAGS = frozenset(
    {
        "blk_test_mcp_started",
        "subprocess_started",
        "electron_started",
        "smoke_test_started",
        "typescript_tooling_executed",
        "package_manager_invoked",
        "network_accessed",
        "model_service_accessed",
        "browser_tooling_invoked",
        "cyber_tooling_invoked",
        "kuronode_source_mutated",
        "kuronode_git_mutated",
        "kuronode_remote_pushed",
        "protected_body_read",
        "beo_published",
        "rtm_generated",
        "drift_rejected",
        "coverage_claim_promoted",
        "active_vault_hash_" + "compared",
        "public_ledger_mutated",
        "signer_storage_rollback_authority_used",
        "production_isolation_claimed",
        "codex_started",
    }
)

_AUTHORIZATION_KEYS = frozenset(
    {
        "authorization_status",
        "operator_identity",
        "approval_id",
        "run_id",
        "approved_runtime_scope",
        "target_repo_path",
        "source_subtree_path",
        "target_branch",
        "target_head_sha",
        "observed_remote_head",
        "fixed_tool",
        "proof_markers",
        "excluded_authorities",
        "no_side_effects",
        "operator_note",
    }
)
_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_FORBIDDEN_TEXT_RE = re.compile(
    r"runtime[\s._:/-]*(?:approval|approved|authorized|authorised)|approved[\s._:/-]*for[\s._:/-]*runtime|"
    r"production[\s._:/-]*blk[\s._:/-]*test[\s._:/-]*mcp|generic[\s._:/-]*blk[\s._:/-]*test[\s._:/-]*mcp|"
    r"blk[\s._:/-]*system[\s._:/-]*test[\s._:/-]*suite|test[\s._:/-]*of[\s._:/-]*blk[\s._:/-]*system|"
    r"beo[\s._:/-]*(?:is[\s._:/-]*)?published|beo[\s._:/-]*publication|publish[\s._:/-]*beo|approval[\s._:/-]*to[\s._:/-]*(?:publish|release)|release[\s._:/-]*approved|deployment[\s._:/-]*approved|"
    r"pass[\s\S]{0,80}(?:approval|approve|authorize|authorise)|rtm[\s._:/-]*(?:generated|generation)|coverage[\s._:/-]*(?:truth|complete|claim)|drift[\s._:/-]*(?:decision|rejection)|"
    r"docs[\\/]+active|protected[\s._:/-]*body|active[\s._:/-]*vault[\s._:/-]*(?:hash[\s._:/-]*)?comparison|\.env|secret|credential|token|private[\s._:/-]*key|api[\s._:/-]*key|authorization|bearer|"
    r"git[\s._:/-]*(?:push|mutation|commit|staging|reset|checkout|stash|write)|source[\s._:/-]*(?:mutation|write)|"
    r"electron|playwright|smoke[\s._:/-]*test|npm|pnpm|yarn|tsc|eslint|prettier|curl|wget|ssh|codex|sandbox|seccomp|apparmor|selinux|host[\s._:/-]*secret[\s._:/-]*isolation",
    re.IGNORECASE,
)
_FORBIDDEN_COMPACT_TEXT = frozenset(
    {
        "approvedforruntime",
        "approvedforruntimeexecution",
        "runtimeapproval",
        "runtimeapproved",
        "runtimeauthorized",
        "productionblktestmcp",
        "genericblktestmcp",
        "blksystemtestsuite",
        "testofblksystem",
        "beoispublished",
        "beopublished",
        "beopublication",
        "publishbeo",
        "rtmgenerated",
        "rtmgeneration",
        "coveragetruth",
        "coveragecomplete",
        "coverageclaim",
        "driftdecision",
        "driftrejection",
        "activevaulthashcomparison",
        "activevaultcomparison",
        "docsactive",
        "protectedbody",
        "protectedbodyread",
        "privatekey",
        "apikey",
        "secret",
        "credential",
        "bearer",
        "hostsecretisolation",
        "gitmutation",
        "gitcommit",
        "gitpush",
        "sourcemutation",
        "sourcewrite",
        "packagemanager",
        "networkaccess",
        "modelservice",
        "browsertooling",
        "cybertooling",
        "electron",
        "playwright",
        "smoketest",
        "codex",
        "sandbox",
    }
)
_PROCESS_CONSUMED_APPROVAL_IDS: set[str] = set()
_PROCESS_CONSUMED_RUN_IDS: set[str] = set()


@dataclass(frozen=True)
class EvidenceRefreshEnvelope:
    sprint: str
    approval_id: str
    run_id: str
    expected_head: str
    approved_target_repo: Path
    approved_source_subtree: Path
    approved_workspace: Path
    replay_ledger_path: Path
    marker_nonce_binding: str
    workspace_marker_name: str
    fixed_tool: str = REQUESTED_TOOL

    def __post_init__(self) -> None:
        if self.fixed_tool != REQUESTED_TOOL:
            raise ValueError("fixed_tool must be run_ast_validation")
        if self.sprint != SPRINT:
            raise ValueError("sprint must equal BLK-SYSTEM-097")
        if self.sprint not in self.approval_id or self.sprint not in self.run_id:
            raise ValueError("approval_id and run_id must bind to sprint")
        if not _is_sha(self.expected_head):
            raise ValueError("expected_head must be a full SHA")
        if self.marker_nonce_binding not in self.sprint:
            raise ValueError("marker_nonce_binding must bind to sprint")
        marker = Path(self.workspace_marker_name)
        if marker.name != self.workspace_marker_name or not self.workspace_marker_name.startswith(".blk-system-") or "/" in self.workspace_marker_name or "\\" in self.workspace_marker_name:
            raise ValueError("workspace_marker_name must be a single hidden marker filename")
        for field_name in ["approved_target_repo", "approved_source_subtree", "approved_workspace", "replay_ledger_path"]:
            object.__setattr__(self, field_name, Path(getattr(self, field_name)))
        repo = self.approved_target_repo.resolve()
        workspace = self.approved_workspace.resolve()
        ledger = self.replay_ledger_path.resolve()
        if repo in (workspace, *workspace.parents) or workspace in (repo, *repo.parents):
            raise ValueError("workspace must not overlap target repository")
        if repo in (ledger, *ledger.parents) or workspace in (ledger, *ledger.parents) or ledger in (workspace, *workspace.parents):
            raise ValueError("ledger must not overlap target repository or workspace")


def default_runtime_envelope() -> EvidenceRefreshEnvelope:
    return EvidenceRefreshEnvelope(
        sprint=SPRINT,
        approval_id=APPROVAL_ID,
        run_id=RUN_ID,
        expected_head=EXPECTED_HEAD,
        approved_target_repo=APPROVED_TARGET_REPO,
        approved_source_subtree=APPROVED_SOURCE_SUBTREE,
        approved_workspace=APPROVED_WORKSPACE,
        replay_ledger_path=REPLAY_LEDGER_PATH,
        marker_nonce_binding=SPRINT,
        workspace_marker_name=".blk-system-097-kuronode-evidence-refresh-workspace",
    )


def build_runtime_authorization(*, approval_id: str, run_id: str, target_repo_path: str, source_subtree_path: str, expected_head: str, observed_remote_head: str) -> dict[str, Any]:
    authorization = {
        "authorization_status": RUNTIME_AUTHORIZATION_STATUS,
        "operator_identity": "discord:684235178083745819:camcamcami",
        "approval_id": approval_id,
        "run_id": run_id,
        "approved_runtime_scope": "ONE_EXACT_KURONODE_WORKSPACE_BOUNDED_EVIDENCE_REFRESH",
        "target_repo_path": target_repo_path,
        "source_subtree_path": source_subtree_path,
        "target_branch": "main",
        "target_head_sha": expected_head,
        "observed_remote_head": observed_remote_head,
        "fixed_tool": REQUESTED_TOOL,
        "proof_markers": sorted(PROOF_MARKERS),
        "excluded_authorities": sorted(EXCLUDED_AUTHORITIES),
        "no_side_effects": {key: False for key in NO_SIDE_EFFECT_FLAGS},
        "operator_note": "Operator selected one exact evidence-only BLK-SYSTEM-097 refresh; adjacent side effects remain denied.",
    }
    return authorization


def reset_process_replay_for_tests() -> None:
    _PROCESS_CONSUMED_APPROVAL_IDS.clear()
    _PROCESS_CONSUMED_RUN_IDS.clear()


def _run_bounded_blk_test_evidence_refresh_for_tests(
    *,
    runtime_authorization: dict[str, Any],
    target_repo_path: str | Path,
    source_subtree_path: str | Path,
    workspace_clone_path: str | Path,
    approval_id: str,
    run_id: str,
    expected_head: str,
    fixed_tool: str,
    expires_at: str,
    now: str,
    used_approval_ids: set[str] | None,
    used_run_ids: set[str] | None,
    workspace_marker_nonce: str,
    output_byte_limit: int = 16384,
    approval_envelope: EvidenceRefreshEnvelope | None = None,
    production_mode: bool = False,
) -> dict[str, Any]:
    envelope = approval_envelope or default_runtime_envelope()
    if used_approval_ids is None or used_run_ids is None:
        raise ValueError("caller-owned replay sets are required")
    if approval_id != envelope.approval_id or run_id != envelope.run_id:
        raise ValueError("approval_id/run_id must match the approved BLK-SYSTEM-097 envelope")
    if expected_head != envelope.expected_head or fixed_tool != envelope.fixed_tool:
        raise ValueError("expected_head/fixed_tool must match the approved BLK-SYSTEM-097 envelope")
    if not workspace_marker_nonce or envelope.marker_nonce_binding not in workspace_marker_nonce:
        raise ValueError("workspace_marker_nonce must bind to the runtime envelope")
    if production_mode and _default_runtime_ids_are_retired_by_committed_evidence():
        raise ValueError("BLK-SYSTEM-097 production runtime IDs are already retired by committed evidence")

    _validate_runtime_authorization(runtime_authorization, envelope)

    if approval_id in used_approval_ids or approval_id in _PROCESS_CONSUMED_APPROVAL_IDS:
        raise ValueError("approval replay detected")
    if run_id in used_run_ids or run_id in _PROCESS_CONSUMED_RUN_IDS:
        raise ValueError("run replay detected")
    ledger = _load_replay_ledger(envelope.replay_ledger_path)
    if approval_id in ledger.get("approval_ids", []):
        raise ValueError("durable approval replay detected")
    if run_id in ledger.get("run_ids", []):
        raise ValueError("durable run replay detected")

    used_approval_ids.add(approval_id)
    used_run_ids.add(run_id)
    ledger.setdefault("approval_ids", []).append(approval_id)
    ledger.setdefault("run_ids", []).append(run_id)
    _write_replay_ledger(envelope.replay_ledger_path, ledger)
    _PROCESS_CONSUMED_APPROVAL_IDS.add(approval_id)
    _PROCESS_CONSUMED_RUN_IDS.add(run_id)

    repo = _resolve_path_for_evidence(target_repo_path, envelope.approved_target_repo)
    source = _resolve_path_for_evidence(source_subtree_path, envelope.approved_source_subtree)
    workspace = _resolve_path_for_evidence(workspace_clone_path, envelope.approved_workspace)
    if output_byte_limit < MIN_OUTPUT_BYTE_LIMIT:
        raise ValueError(f"output_byte_limit must be at least {MIN_OUTPUT_BYTE_LIMIT}")
    try:
        _validate_exact_path_spelling(target_repo_path, source_subtree_path, workspace_clone_path, envelope)
        _validate_paths(repo, source, workspace, envelope)
        _reject_source_scope(source)
    except ValueError as exc:
        return _blocked_evidence(
            f"pre-runtime validation failed: {exc}",
            envelope,
            repo,
            source,
            workspace,
            approval_id,
            run_id,
            expected_head,
            None,
            output_byte_limit,
        )

    if _parse_instant(now) >= _parse_instant(expires_at):
        return _blocked_evidence("approval expired before runtime", envelope, repo, source, workspace, approval_id, run_id, expected_head, None, output_byte_limit)

    actual_head = _resolve_git_head(repo)
    if actual_head != expected_head:
        return _blocked_evidence(f"target HEAD mismatch: expected {expected_head} actual {actual_head}", envelope, repo, source, workspace, approval_id, run_id, expected_head, actual_head, output_byte_limit)

    observed_remote_head = _resolve_git_ref(repo, "refs/remotes/origin/main")
    if runtime_authorization["observed_remote_head"] != observed_remote_head:
        return _blocked_evidence(
            f"provided remote HEAD evidence mismatch: provided {runtime_authorization['observed_remote_head']} actual {observed_remote_head}",
            envelope,
            repo,
            source,
            workspace,
            approval_id,
            run_id,
            expected_head,
            actual_head,
            output_byte_limit,
            observed_remote_head=observed_remote_head,
        )
    if observed_remote_head != expected_head:
        return _blocked_evidence(
            f"observed remote HEAD mismatch: expected {expected_head} actual {observed_remote_head}",
            envelope,
            repo,
            source,
            workspace,
            approval_id,
            run_id,
            expected_head,
            actual_head,
            output_byte_limit,
            observed_remote_head=observed_remote_head,
        )

    if workspace.exists():
        return _blocked_evidence(
            "workspace_clone_path already exists before BLK-SYSTEM-097 ownership is established",
            envelope,
            repo,
            source,
            workspace,
            approval_id,
            run_id,
            expected_head,
            actual_head,
            output_byte_limit,
            observed_remote_head=observed_remote_head,
        )

    source_before = _snapshot_tree(source)
    git_before = _snapshot_git_metadata(repo / ".git")
    cleanup_verified = False
    workspace_owned = False
    files_checked: list[str] = []
    findings: list[dict[str, Any]] = []
    all_findings: list[dict[str, Any]] = []
    fixed_tool_executed = False
    runtime_exception: Exception | None = None
    try:
        workspace_source = workspace / "source"
        workspace_source.parent.mkdir(parents=True)
        workspace_owned = True
        shutil.copytree(source, workspace_source, symlinks=False)
        marker = workspace / envelope.workspace_marker_name
        marker.write_text(json.dumps({"approval_id": approval_id, "run_id": run_id, "nonce": workspace_marker_nonce, "expected_head": expected_head}, sort_keys=True) + "\n", encoding="utf-8")
        descriptors = []
        for path in sorted([*workspace_source.rglob("*.ts"), *workspace_source.rglob("*.tsx")]):
            rel = path.relative_to(workspace_source).as_posix()
            files_checked.append(rel)
            descriptors.append({"path": rel, "language": "tsx" if rel.endswith(".tsx") else "typescript", "content": path.read_text(encoding="utf-8")})
        fixed_tool_executed = True
        profile_request = _build_static_profile_request(descriptors)
        profile_result = evaluate_kuronode_power_of_ten_static_profile(files=descriptors, request=profile_request)
        all_findings = deepcopy(profile_result["findings"])
        findings = all_findings[:MAX_FINDINGS]
        marker_payload = json.loads(marker.read_text(encoding="utf-8"))
        if marker_payload.get("nonce") != workspace_marker_nonce:
            raise ValueError("workspace marker nonce mismatch before cleanup")
    except Exception as exc:
        runtime_exception = exc
    finally:
        if workspace_owned and workspace.exists():
            shutil.rmtree(workspace)
        cleanup_verified = not workspace.exists() if workspace_owned else True

    source_after = _snapshot_tree(source)
    git_after = _snapshot_git_metadata(repo / ".git")
    source_mutation = source_before != source_after
    git_mutation = git_before != git_after
    status = "FAIL" if findings else "PASS"
    pilot_status = FAIL_STATUS if findings else PASS_STATUS
    block_reason = ""
    if runtime_exception is not None:
        status = "BLOCKED"
        pilot_status = BLOCKED_STATUS
        block_reason = f"runtime exception after replay: {type(runtime_exception).__name__}"
    if source_mutation or git_mutation or not cleanup_verified:
        status = "BLOCKED"
        pilot_status = BLOCKED_STATUS
        block_reason = "source/Git mutation or workspace cleanup failure detected"

    evidence = _base_evidence(envelope, repo, source, workspace, approval_id, run_id, expected_head, actual_head, output_byte_limit, observed_remote_head=observed_remote_head)
    evidence.update(
        {
            "pilot_status": pilot_status,
            "status": status,
            "block_reason": block_reason,
            "fixed_tool_executed": fixed_tool_executed,
            "files_checked": files_checked[:MAX_LISTED_FILES],
            "files_checked_count": len(files_checked),
            "files_checked_truncated": len(files_checked) > MAX_LISTED_FILES,
            "findings": findings,
            "findings_count": len(all_findings),
            "findings_emitted_count": len(findings),
            "findings_truncated": len(all_findings) > MAX_FINDINGS,
            "source_tree_hash_before": _tree_digest(source_before),
            "source_tree_hash_after": _tree_digest(source_after),
            "git_metadata_hash_before": _tree_digest(git_before),
            "git_metadata_hash_after": _tree_digest(git_after),
            "source_mutation_detected": source_mutation,
            "git_mutation_detected": git_mutation,
            "workspace_cleanup_verified": cleanup_verified,
        }
    )
    return _finalize_evidence(evidence, output_byte_limit)


def run_bounded_blk_test_evidence_refresh(
    *,
    runtime_authorization: dict[str, Any],
    target_repo_path: str | Path,
    source_subtree_path: str | Path,
    workspace_clone_path: str | Path,
    approval_id: str,
    run_id: str,
    expected_head: str,
    fixed_tool: str,
    expires_at: str,
    now: str,
    used_approval_ids: set[str] | None,
    used_run_ids: set[str] | None,
    workspace_marker_nonce: str,
    output_byte_limit: int = 16384,
) -> dict[str, Any]:
    """Production entrypoint: exactly the default BLK-SYSTEM-097 Kuronode target."""

    return _run_bounded_blk_test_evidence_refresh_for_tests(
        runtime_authorization=runtime_authorization,
        target_repo_path=target_repo_path,
        source_subtree_path=source_subtree_path,
        workspace_clone_path=workspace_clone_path,
        approval_id=approval_id,
        run_id=run_id,
        expected_head=expected_head,
        fixed_tool=fixed_tool,
        expires_at=expires_at,
        now=now,
        used_approval_ids=used_approval_ids,
        used_run_ids=used_run_ids,
        workspace_marker_nonce=workspace_marker_nonce,
        output_byte_limit=output_byte_limit,
        approval_envelope=default_runtime_envelope(),
        production_mode=True,
    )


def runtime_ids_are_retired_by_evidence(evidence_path: str | Path) -> bool:
    path = Path(evidence_path)
    if not path.exists():
        return False
    try:
        evidence = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return evidence.get("approval_id") == APPROVAL_ID and evidence.get("run_id") == RUN_ID


def _default_runtime_ids_are_retired_by_committed_evidence() -> bool:
    evidence_path = Path(__file__).resolve().parents[1] / "docs" / "outcomes" / "BLK-SYSTEM-097_runtime-evidence.json"
    return runtime_ids_are_retired_by_evidence(evidence_path)


def _validate_runtime_authorization(auth: dict[str, Any], envelope: EvidenceRefreshEnvelope) -> None:
    _require_dict(auth, "runtime_authorization")
    _require_keys(auth, _AUTHORIZATION_KEYS, "runtime_authorization")
    # Most fields are exact structural controls. Scan only the freeform note;
    # exact-key and exact-value checks below reject structural smuggling.
    _scan_forbidden_text(auth.get("operator_note"), "runtime_authorization.operator_note")
    expected = {
        "authorization_status": RUNTIME_AUTHORIZATION_STATUS,
        "operator_identity": "discord:684235178083745819:camcamcami",
        "approval_id": envelope.approval_id,
        "run_id": envelope.run_id,
        "approved_runtime_scope": "ONE_EXACT_KURONODE_WORKSPACE_BOUNDED_EVIDENCE_REFRESH",
        "target_repo_path": str(envelope.approved_target_repo),
        "source_subtree_path": str(envelope.approved_source_subtree),
        "target_branch": "main",
        "target_head_sha": envelope.expected_head,
        "fixed_tool": REQUESTED_TOOL,
    }
    for key, value in expected.items():
        if auth.get(key) != value:
            raise ValueError(f"runtime_authorization {key} mismatch")
    if not _is_sha(_required_string(auth.get("observed_remote_head"), "observed_remote_head")):
        raise ValueError("observed_remote_head must be a full SHA")
    _validate_exact_string_set(auth.get("proof_markers"), PROOF_MARKERS, "proof_markers")
    _validate_exact_string_set(auth.get("excluded_authorities"), EXCLUDED_AUTHORITIES, "excluded_authorities")
    _validate_false_flags(auth.get("no_side_effects"), NO_SIDE_EFFECT_FLAGS, "no_side_effects")


def _build_static_profile_request(descriptors: list[dict[str, str]]) -> dict[str, Any]:
    source_hash = _canonical_hash_list(descriptors)
    return {
        "profile_name": "kuronode-power-of-ten-static",
        "request_status": "KURONODE_POWER_OF_TEN_STATIC_PROFILE_FIXTURE_ONLY",
        "request_id": "BLK-SYSTEM-097-KURONODE-EVIDENCE-REFRESH-RUN-AST-VALIDATION",
        "operator_identity": "discord:684235178083745819:camcamcami",
        "trace_artifacts": [
            {
                "kind": "SRC",
                "id": "KURONODE-SCRIPTS-SUBTREE-COPY",
                "version_hash": source_hash,
            }
        ],
        "source_bundle_id": "kuronode-workspace-scripts-subtree-read-only",
        "source_bundle_hash": source_hash,
        "excluded_authorities": [
            "LIVE_CODEX_EXECUTION",
            "LIVE_TACTICAL_LLM_DISPATCH",
            "SOURCE_OR_GIT_MUTATION",
            "LIVE_KURONODE_REPO_SCAN",
            "PACKAGE_MANAGER_INVOCATION",
            "NETWORK_ACCESS",
            "MODEL_SERVICE_ACCESS",
            "BROWSER_OR_CYBER_TOOLING",
            "PRODUCTION_BLK_TEST_MCP",
            "GENERIC_BLK_TEST_MCP",
            "REUSABLE_BLK_TEST_SERVICE_STARTUP",
            "ARBITRARY_SHELL_OR_CALLER_SUPPLIED_COMMANDS",
            "PROTECTED_BLK_REQ_BODY_READ",
            "AUTHORITATIVE_BEO_PUBLICATION",
            "RUNTIME_PUBLISHED_BEO_OUTPUT",
            "RTM_GENERATION",
            "RTM_DRIFT_REJECTION",
            "ACTIVE_VAULT_HASH_COMPARISON",
            "COVERAGE_MATRIX_OR_CLAIM",
            "PRODUCTION_SANDBOX_OR_HOST_SECRET_ISOLATION_CLAIM",
        ],
        "operator_note": "Fixture evaluator applied to copied read-only Kuronode scripts source descriptors by BLK-SYSTEM-097 evidence-refresh wrapper.",
    }


def _validate_exact_path_spelling(target_repo_path: str | Path, source_subtree_path: str | Path, workspace_clone_path: str | Path, envelope: EvidenceRefreshEnvelope) -> None:
    _require_exact_spelling("target_repo_path", target_repo_path, envelope.approved_target_repo)
    _require_exact_spelling("source_subtree_path", source_subtree_path, envelope.approved_source_subtree)
    _require_exact_spelling("workspace_clone_path", workspace_clone_path, envelope.approved_workspace)


def _resolve_path_for_evidence(raw_path: str | Path, fallback: Path) -> Path:
    try:
        return Path(os.fspath(raw_path)).resolve()
    except (OSError, RuntimeError, TypeError, ValueError):
        return fallback.resolve()


def _require_exact_spelling(label: str, raw_path: str | Path, approved_path: Path) -> None:
    if not isinstance(raw_path, str):
        raise ValueError(f"{label} must be supplied as a raw string exact spelling")
    raw_text = raw_path
    approved_text = os.fspath(approved_path)
    try:
        same_target = Path(raw_text).resolve() == approved_path.resolve()
    except RuntimeError:
        same_target = False
    if same_target and raw_text != approved_text:
        raise ValueError(f"{label} must use approved exact spelling")


def _validate_paths(repo: Path, source: Path, workspace: Path, envelope: EvidenceRefreshEnvelope) -> None:
    if repo != envelope.approved_target_repo.resolve():
        raise ValueError("target_repo_path must match approved target")
    if source != envelope.approved_source_subtree.resolve():
        raise ValueError("source_subtree_path must match approved source subtree")
    if workspace != envelope.approved_workspace.resolve():
        raise ValueError("workspace_clone_path must match approved workspace")
    if not repo.is_dir() or not (repo / ".git").is_dir():
        raise ValueError("target_repo_path must be a Git repository")
    if not source.is_dir():
        raise ValueError("source_subtree_path must be an existing directory")
    if repo not in (source, *source.parents):
        raise ValueError("source_subtree_path must resolve inside target_repo_path")
    if repo in (workspace, *workspace.parents) or workspace in (repo, *repo.parents):
        raise ValueError("workspace_clone_path must not overlap target_repo_path")
    if not workspace.is_absolute():
        raise ValueError("workspace_clone_path must be absolute")


def _reject_source_scope(source: Path) -> None:
    for candidate in [source, *source.rglob("*")]:
        if candidate.is_symlink():
            resolved = candidate.resolve()
            if source not in (resolved, *resolved.parents):
                raise ValueError("source scope contains symlink escape")
        parts = candidate.relative_to(source).parts if candidate != source else ()
        if ".git" in parts or candidate.name == ".git":
            raise ValueError("source scope contains git metadata")
        if _is_secret_name(candidate.name):
            raise ValueError("source scope contains secret descendant")
        joined = "/".join(parts)
        if joined.startswith("docs/active") or joined.startswith("docs/requirements") or joined.startswith("docs/use_cases"):
            raise ValueError("source scope contains protected BLK-req descendant")


def _resolve_git_head(repo: Path) -> str:
    head = (repo / ".git" / "HEAD").read_text(encoding="utf-8").strip()
    if _is_sha(head):
        return head
    if not head.startswith("ref: "):
        raise ValueError("target repository HEAD is not a safe ref")
    ref = head[5:].strip()
    return _resolve_git_ref(repo, ref)


def _resolve_git_ref(repo: Path, ref: str) -> str:
    if ".." in ref or not ref.startswith("refs/"):
        raise ValueError("target repository ref is unsafe")
    git_dir = (repo / ".git").resolve()
    ref_path = (git_dir / ref).resolve()
    if git_dir not in (ref_path, *ref_path.parents):
        raise ValueError("target repository ref escapes .git")
    if ref_path.exists():
        value = ref_path.read_text(encoding="utf-8").strip()
        if not _is_sha(value):
            raise ValueError("target repository ref is not a full SHA")
        return value
    packed_refs = git_dir / "packed-refs"
    if packed_refs.exists():
        for line in packed_refs.read_text(encoding="utf-8").splitlines():
            if not line or line.startswith("#") or line.startswith("^"):
                continue
            parts = line.split(" ", 1)
            if len(parts) == 2 and parts[1] == ref and _is_sha(parts[0]):
                return parts[0]
    raise ValueError(f"target repository ref missing: {ref}")


def _blocked_evidence(
    reason: str,
    envelope: EvidenceRefreshEnvelope,
    repo: Path,
    source: Path,
    workspace: Path,
    approval_id: str,
    run_id: str,
    expected_head: str,
    actual_head: str | None,
    output_byte_limit: int,
    *,
    observed_remote_head: str | None = None,
) -> dict[str, Any]:
    evidence = _base_evidence(envelope, repo, source, workspace, approval_id, run_id, expected_head, actual_head, output_byte_limit, observed_remote_head=observed_remote_head)
    evidence.update(
        {
            "pilot_status": BLOCKED_STATUS,
            "status": "BLOCKED",
            "block_reason": reason,
            "fixed_tool_executed": False,
            "files_checked": [],
            "files_checked_count": 0,
            "files_checked_truncated": False,
            "findings": [],
            "findings_count": 0,
            "findings_truncated": False,
            "source_tree_hash_before": "NOT_MEASURED_BEFORE_RUNTIME",
            "source_tree_hash_after": "NOT_MEASURED_BEFORE_RUNTIME",
            "git_metadata_hash_before": "NOT_MEASURED_BEFORE_RUNTIME",
            "git_metadata_hash_after": "NOT_MEASURED_BEFORE_RUNTIME",
            "source_mutation_detected": False,
            "git_mutation_detected": False,
            "workspace_cleanup_verified": True,
        }
    )
    return _finalize_evidence(evidence, output_byte_limit)


def _base_evidence(
    envelope: EvidenceRefreshEnvelope,
    repo: Path,
    source: Path,
    workspace: Path,
    approval_id: str,
    run_id: str,
    expected_head: str,
    actual_head: str | None,
    output_byte_limit: int,
    *,
    observed_remote_head: str | None = None,
) -> dict[str, Any]:
    return {
        "sprint": envelope.sprint,
        "approval_id": approval_id,
        "run_id": run_id,
        "target_repo_path": str(repo),
        "source_subtree_path": str(source),
        "workspace_clone_path": str(workspace),
        "expected_head": expected_head,
        "actual_head": actual_head,
        "observed_remote_head": observed_remote_head,
        "requested_tool": REQUESTED_TOOL,
        "replay_consumed_before_runtime": True,
        "source_write_allowed": False,
        "git_mutation_allowed": False,
        "staging_allowed": False,
        "commit_allowed": False,
        "push_allowed": False,
        "active_vault_read": False,
        "protected_body_read": False,
        "beo_publication": "DRAFT_ONLY",
        "rtm_status": "NOT_GENERATED",
        "rtm_drift_rejection": False,
        "coverage_claim_promoted": False,
        "public_ledger_mutation": False,
        "production_isolation_claimed": False,
        "production_mcp_authority": False,
        "generic_mcp_authority": False,
        "reusable_service_started": False,
        "live_codex_execution": False,
        "arbitrary_shell_called": False,
        "typescript_tooling_called": False,
        "package_manager_called": False,
        "network_called": False,
        "model_service_called": False,
        "browser_tooling_called": False,
        "cyber_tooling_called": False,
        "output_byte_limit": output_byte_limit,
        "evidence_json_bytes": 0,
    }


def _finalize_evidence(evidence: dict[str, Any], output_byte_limit: int) -> dict[str, Any]:
    for _ in range(6):
        size = _json_size(evidence)
        if evidence.get("evidence_json_bytes") == size:
            break
        evidence["evidence_json_bytes"] = size
    if _json_size(evidence) <= output_byte_limit:
        return evidence
    compact = {
        "sprint": evidence["sprint"],
        "pilot_status": BLOCKED_STATUS,
        "status": "BLOCKED",
        "block_reason": "output byte limit exceeded by bounded evidence",
        "approval_id": evidence["approval_id"],
        "run_id": evidence["run_id"],
        "requested_tool": REQUESTED_TOOL,
        "fixed_tool_executed": evidence.get("fixed_tool_executed", False),
        "workspace_cleanup_verified": evidence.get("workspace_cleanup_verified", False),
        "source_mutation_detected": evidence.get("source_mutation_detected", False),
        "git_mutation_detected": evidence.get("git_mutation_detected", False),
        "source_write_allowed": False,
        "git_mutation_allowed": False,
        "active_vault_read": False,
        "beo_publication": "DRAFT_ONLY",
        "rtm_status": "NOT_GENERATED",
        "production_isolation_claimed": False,
        "output_byte_limit": output_byte_limit,
        "evidence_json_bytes": 0,
    }
    for _ in range(6):
        size = _json_size(compact)
        if compact.get("evidence_json_bytes") == size:
            break
        compact["evidence_json_bytes"] = size
    if _json_size(compact) > output_byte_limit:
        raise ValueError("compact evidence cannot fit output_byte_limit")
    return compact


def _snapshot_tree(root: Path) -> dict[str, str]:
    st = root.stat()
    snapshot = {".": f"dir:{st.st_mode}:{st.st_uid}:{st.st_gid}:{st.st_mtime_ns}:{st.st_ctime_ns}"}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            link_st = path.lstat()
            payload = os.readlink(path)
            resolved = path.resolve()
            target = resolved.relative_to(root).as_posix() if root in (resolved, *resolved.parents) else f"ESCAPE:{resolved}"
            snapshot[rel] = f"symlink:{link_st.st_mode}:{link_st.st_uid}:{link_st.st_gid}:{link_st.st_mtime_ns}:{link_st.st_ctime_ns}:{payload}:resolved:{target}"
        elif path.is_dir():
            dir_st = path.stat()
            snapshot[rel] = f"dir:{dir_st.st_mode}:{dir_st.st_uid}:{dir_st.st_gid}:{dir_st.st_mtime_ns}:{dir_st.st_ctime_ns}"
        elif path.is_file():
            file_st = path.stat()
            snapshot[rel] = f"file:{file_st.st_mode}:{file_st.st_uid}:{file_st.st_gid}:{file_st.st_size}:{file_st.st_mtime_ns}:{file_st.st_ctime_ns}:{_hash_bytes(path.read_bytes())}"
    return snapshot


def _snapshot_git_metadata(git_dir: Path) -> dict[str, str]:
    st = git_dir.stat()
    snapshot = {".": f"dir:{st.st_mode}:{st.st_uid}:{st.st_gid}:{st.st_mtime_ns}:{st.st_ctime_ns}"}
    for path in sorted(git_dir.rglob("*")):
        if path.is_symlink():
            raise ValueError("git metadata symlinks are forbidden")
        rel = path.relative_to(git_dir).as_posix()
        if path.is_dir():
            dir_st = path.stat()
            snapshot[rel] = f"dir:{dir_st.st_mode}:{dir_st.st_uid}:{dir_st.st_gid}:{dir_st.st_mtime_ns}:{dir_st.st_ctime_ns}"
        elif path.is_file():
            data = path.read_bytes()
            file_st = path.stat()
            snapshot[rel] = f"file:{file_st.st_mode}:{file_st.st_uid}:{file_st.st_gid}:{len(data)}:{file_st.st_mtime_ns}:{file_st.st_ctime_ns}:{_hash_bytes(data)}"
    return snapshot


def _load_replay_ledger(path: Path) -> dict[str, list[str]]:
    if not path.exists():
        return {"approval_ids": [], "run_ids": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("durable replay ledger must be an object")
    approval_ids = data.get("approval_ids", [])
    run_ids = data.get("run_ids", [])
    if not isinstance(approval_ids, list) or not isinstance(run_ids, list):
        raise ValueError("durable replay ledger has invalid shape")
    return {"approval_ids": [str(v) for v in approval_ids], "run_ids": [str(v) for v in run_ids]}


def _write_replay_ledger(path: Path, ledger: dict[str, list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    if tmp.exists() or tmp.is_symlink():
        raise ValueError("durable replay ledger temporary path already exists")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(tmp, flags, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(ledger, sort_keys=True) + "\n")
    except Exception:
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass
        raise
    tmp.replace(path)


def _validate_exact_string_set(value: Any, expected: frozenset[str], field: str) -> None:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value) or len(value) != len(set(value)) or set(value) != expected:
        raise ValueError(f"{field} must match exact string set")


def _validate_false_flags(value: Any, expected: frozenset[str], field: str) -> None:
    _require_dict(value, field)
    if set(value) != expected:
        raise ValueError(f"{field} must contain exact side-effect flags")
    if any(flag is not False for flag in value.values()):
        raise ValueError(f"{field} must be all false")


def _scan_forbidden_text(value: Any, path: str) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            # BLK-SYSTEM-097 uses closed schemas; required structural keys such as
            # `authorization_status` are not free-text authority claims. Scan
            # values recursively, and rely on exact-key validation to reject
            # attacker-supplied laundering keys.
            _scan_forbidden_text(item, f"{path}.{key}")
    elif isinstance(value, list):
        for idx, item in enumerate(value):
            _scan_forbidden_text(item, f"{path}[{idx}]")
    elif isinstance(value, str):
        for variant in _decoded_variants(value):
            if _FORBIDDEN_TEXT_RE.search(variant):
                raise ValueError(f"forbidden authority text at {path}")
            compact = _compact_text(variant)
            if any(token in compact for token in _FORBIDDEN_COMPACT_TEXT):
                raise ValueError(f"forbidden authority text at {path}")


def _require_dict(value: Any, field: str) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{field} must be a dict")


def _require_keys(value: dict[str, Any], expected: frozenset[str], field: str) -> None:
    if set(value) != expected:
        raise ValueError(f"{field} must contain exact keys")


def _required_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} must be a non-empty string")
    return value


def _is_secret_name(name: str) -> bool:
    lowered = name.lower()
    compact = "".join(char for char in lowered if char.isalnum())
    if lowered in {".env", ".envrc", ".npmrc", ".pypirc", ".netrc", ".ssh", ".aws", ".gnupg", "credentials", "secrets", "tokens", "kubeconfig"}:
        return True
    if lowered.startswith((".env.", ".env-", ".env_", ".envrc.", ".envrc-", ".envrc_", ".npmrc.", ".npmrc-", ".npmrc_", "credential", "secret", "secrets.", "secrets-", "secrets_", "token", "tokens.", "tokens-", "tokens_", "access_token", "access-token", "api_key", "api-key")):
        return True
    if lowered in {"id_rsa", "id_dsa", "id_ecdsa", "id_ed25519", "service-account.json", "key.json", "private-key"}:
        return True
    secret_tokens = (
        "apikey",
        "accesskey",
        "accesstoken",
        "authtoken",
        "bearertoken",
        "privatekey",
        "secretkey",
        "clientsecret",
        "serviceaccount",
        "credential",
        "credentials",
    )
    return lowered.endswith(".pem") or any(token in compact for token in secret_tokens)


def _is_sha(value: str) -> bool:
    return len(value) == 40 and all(c in "0123456789abcdef" for c in value)


def _parse_instant(value: str) -> datetime:
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        raise ValueError("timestamp must be timezone-aware")
    return parsed.astimezone(timezone.utc)


def _decoded_variants(text: str) -> list[str]:
    variants = [text]
    current = text
    for _ in range(5):
        decoded = _percent_decode_once(current)
        if decoded == current:
            break
        variants.append(decoded)
        current = decoded
    return variants


def _percent_decode_once(text: str) -> str:
    out: list[str] = []
    index = 0
    hexdigits = "0123456789abcdefABCDEF"
    while index < len(text):
        if text[index] == "%" and index + 2 < len(text) and text[index + 1] in hexdigits and text[index + 2] in hexdigits:
            out.append(chr(int(text[index + 1 : index + 3], 16)))
            index += 3
        else:
            out.append(text[index])
            index += 1
    return "".join(out)


def _compact_text(text: str) -> str:
    return "".join(char for char in str(text).casefold() if char.isalnum())


def _canonical_hash(value: dict[str, Any]) -> str:
    return _hash_bytes(json.dumps(deepcopy(value), sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8"))


def _canonical_hash_list(value: list[dict[str, str]]) -> str:
    return _hash_bytes(json.dumps(deepcopy(value), sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8"))


def _tree_digest(snapshot: dict[str, str]) -> str:
    return _hash_bytes(json.dumps(snapshot, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def _hash_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _json_size(value: dict[str, Any]) -> int:
    return len(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8"))
