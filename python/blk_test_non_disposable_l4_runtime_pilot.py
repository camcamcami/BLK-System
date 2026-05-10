"""BLK-SYSTEM-051 non-disposable L4 BLK-test runtime pilot.

This module implements one exact approved, evidence-only runtime slice for the
fixed tool ``run_ast_validation``. It does not start a BLK-test MCP server, does
not accept caller-supplied commands, does not mutate target source/Git state,
and does not publish BEO/RTM artifacts.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SPRINT = "BLK-SYSTEM-051"
APPROVAL_ID = "APPROVAL-BLK-SYSTEM-051-001"
RUN_ID = "RUN-BLK-SYSTEM-051-001"
EXPECTED_HEAD = "75e44c4066f7cbad38ed15afdc93a8eafd703340"
APPROVED_TARGET_REPO = Path("/home/dad/BLK-System")
APPROVED_SOURCE_SUBTREE = Path("/home/dad/BLK-System/python")
APPROVED_WORKSPACE = Path("/tmp/blk-system-051-non-disposable-l4-runtime-workspace")
REPLAY_LEDGER_PATH = Path("/tmp/blk-system-051-non-disposable-l4-runtime-replay-ledger.json")
_PROCESS_CONSUMED_APPROVAL_IDS: set[str] = set()
_PROCESS_CONSUMED_RUN_IDS: set[str] = set()
REQUESTED_TOOL = "run_ast_validation"
L4_PASS = "BLK_TEST_NON_DISPOSABLE_L4_RUNTIME_PILOT_PASS_EVIDENCE_ONLY"
L4_FAIL = "BLK_TEST_NON_DISPOSABLE_L4_RUNTIME_PILOT_FAIL_EVIDENCE_ONLY"
L4_BLOCKED = "BLK_TEST_NON_DISPOSABLE_L4_RUNTIME_PILOT_BLOCKED_EVIDENCE_ONLY"
MAX_LISTED_FILES = 80
MAX_DIAGNOSTICS = 25
MIN_OUTPUT_BYTE_LIMIT = 1024
SECRET_NAMES = {".env", ".ssh", ".aws", ".gnupg", "credentials", "secrets", "tokens"}
PROTECTED_PARTS = {"active", "requirements", "use_cases"}


@dataclass(frozen=True)
class L4RuntimeApprovalEnvelope:
    """Exact one-run non-disposable L4 runtime approval envelope."""

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
            raise ValueError(f"approval envelope fixed_tool must be {REQUESTED_TOOL}")
        if not self.sprint.startswith("BLK-SYSTEM-"):
            raise ValueError("approval envelope sprint must be a BLK-SYSTEM identifier")
        if self.marker_nonce_binding not in self.sprint:
            raise ValueError("marker_nonce_binding must include the approval envelope sprint")
        marker_path = Path(self.workspace_marker_name)
        if (
            marker_path.name != self.workspace_marker_name
            or not self.workspace_marker_name.startswith(".blk-system-")
            or self.workspace_marker_name in {".", ".."}
            or "/" in self.workspace_marker_name
            or "\\" in self.workspace_marker_name
        ):
            raise ValueError("workspace_marker_name must be a single hidden filename")
        for field_name in [
            "approved_target_repo",
            "approved_source_subtree",
            "approved_workspace",
            "replay_ledger_path",
        ]:
            object.__setattr__(self, field_name, Path(getattr(self, field_name)))


def _default_approval_envelope() -> L4RuntimeApprovalEnvelope:
    return L4RuntimeApprovalEnvelope(
        sprint=SPRINT,
        approval_id=APPROVAL_ID,
        run_id=RUN_ID,
        expected_head=EXPECTED_HEAD,
        approved_target_repo=APPROVED_TARGET_REPO,
        approved_source_subtree=APPROVED_SOURCE_SUBTREE,
        approved_workspace=APPROVED_WORKSPACE,
        replay_ledger_path=REPLAY_LEDGER_PATH,
        marker_nonce_binding=SPRINT,
        workspace_marker_name=".blk-system-051-non-disposable-l4-runtime-workspace",
        fixed_tool=REQUESTED_TOOL,
    )


def run_blk_test_non_disposable_l4_runtime_pilot(
    *,
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
    approval_envelope: L4RuntimeApprovalEnvelope | None = None,
) -> dict[str, Any]:
    """Run the exact approved non-disposable L4 pilot or return BLOCKED evidence.

    The function intentionally validates static schema/path/tool constraints
    before consuming replay IDs. It consumes the approval/run IDs before any
    workspace creation or tool execution, so a target-state mismatch cannot be
    retried under the same IDs.
    """
    envelope = approval_envelope or _default_approval_envelope()
    if used_approval_ids is None or used_run_ids is None:
        raise ValueError("caller-owned replay sets are required")
    if approval_id != envelope.approval_id:
        raise ValueError(f"approval_id must be {envelope.approval_id}")
    if run_id != envelope.run_id:
        raise ValueError(f"run_id must be {envelope.run_id}")
    if fixed_tool != envelope.fixed_tool:
        raise ValueError(f"fixed_tool must be {envelope.fixed_tool}")
    if expected_head != envelope.expected_head:
        raise ValueError("expected_head must match the approved exact target HEAD")
    if output_byte_limit < MIN_OUTPUT_BYTE_LIMIT:
        raise ValueError(f"output_byte_limit must be at least {MIN_OUTPUT_BYTE_LIMIT} bytes")
    if not workspace_marker_nonce or envelope.marker_nonce_binding not in workspace_marker_nonce:
        raise ValueError(f"workspace_marker_nonce must bind to {envelope.marker_nonce_binding}")

    _validate_exact_path_spelling(target_repo_path, source_subtree_path, workspace_clone_path, envelope)
    repo_input = Path(target_repo_path)
    source_input = Path(source_subtree_path)
    workspace_input = Path(workspace_clone_path)
    repo = repo_input.resolve()
    source = source_input.resolve()
    workspace = workspace_input.resolve()
    _validate_paths(repo, source, workspace, envelope)
    _reject_source_scope(source)

    if approval_id in used_approval_ids:
        raise ValueError("approval replay detected")
    if run_id in used_run_ids:
        raise ValueError("run replay detected")
    if approval_id in _PROCESS_CONSUMED_APPROVAL_IDS:
        raise ValueError("process approval replay detected")
    if run_id in _PROCESS_CONSUMED_RUN_IDS:
        raise ValueError("process run replay detected")
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

    if _parse_instant(now) >= _parse_instant(expires_at):
        return _blocked_evidence(
            sprint=envelope.sprint,
            block_reason="approval expired before runtime",
            approval_id=approval_id,
            run_id=run_id,
            repo=repo,
            source=source,
            workspace=workspace,
            expected_head=expected_head,
            actual_head=None,
            replay_consumed=True,
            output_byte_limit=output_byte_limit,
        )

    actual_head = _resolve_git_head(repo)
    if actual_head != expected_head:
        return _blocked_evidence(
            sprint=envelope.sprint,
            block_reason=f"target HEAD mismatch: expected {expected_head} actual {actual_head}",
            approval_id=approval_id,
            run_id=run_id,
            repo=repo,
            source=source,
            workspace=workspace,
            expected_head=expected_head,
            actual_head=actual_head,
            replay_consumed=True,
            output_byte_limit=output_byte_limit,
        )

    source_before = _snapshot_tree(source)
    git_before = _snapshot_git_metadata(repo / ".git")
    diagnostics: list[dict[str, Any]] = []
    files_checked: list[str] = []
    cleanup_verified = False
    fixed_tool_executed = False
    workspace_owned = False
    try:
        if workspace.exists():
            raise ValueError(f"workspace_clone_path already exists before {envelope.sprint} ownership is established")
        workspace_source = workspace / "source"
        workspace_source.parent.mkdir(parents=True)
        workspace_owned = True
        shutil.copytree(source, workspace_source, symlinks=False)
        marker = workspace / envelope.workspace_marker_name
        marker.write_text(
            json.dumps(
                {
                    "approval_id": approval_id,
                    "run_id": run_id,
                    "workspace_marker_nonce": workspace_marker_nonce,
                    "target_repo_path": str(repo),
                    "source_subtree_path": str(source),
                    "expected_head": expected_head,
                    "fixed_tool": envelope.fixed_tool,
                },
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        fixed_tool_executed = True
        for path in sorted(workspace_source.rglob("*.py")):
            rel = path.relative_to(workspace_source).as_posix()
            files_checked.append(rel)
            try:
                ast.parse(path.read_text(encoding="utf-8"), filename=rel)
            except SyntaxError as exc:
                if len(diagnostics) < MAX_DIAGNOSTICS:
                    diagnostics.append({"path": rel, "line": exc.lineno, "message": exc.msg})
        marker_payload = json.loads(marker.read_text(encoding="utf-8"))
        if marker_payload.get("workspace_marker_nonce") != workspace_marker_nonce:
            raise ValueError("workspace marker nonce mismatch before cleanup")
    finally:
        if workspace_owned and workspace.exists():
            shutil.rmtree(workspace)
        cleanup_verified = not workspace.exists() if workspace_owned else True

    source_after = _snapshot_tree(source)
    git_after = _snapshot_git_metadata(repo / ".git")
    source_mutation = source_before != source_after
    git_mutation = git_before != git_after
    status = "FAIL" if diagnostics else "PASS"
    pilot_status = L4_FAIL if diagnostics else L4_PASS
    block_reason = ""
    if source_mutation or git_mutation or not cleanup_verified:
        status = "BLOCKED"
        pilot_status = L4_BLOCKED
        block_reason = "source/Git mutation or workspace cleanup failure detected"

    evidence = _base_evidence(
        sprint=envelope.sprint,
        approval_id=approval_id,
        run_id=run_id,
        repo=repo,
        source=source,
        workspace=workspace,
        expected_head=expected_head,
        actual_head=actual_head,
        replay_consumed=True,
        output_byte_limit=output_byte_limit,
    )
    evidence.update(
        {
            "pilot_status": pilot_status,
            "status": status,
            "block_reason": block_reason,
            "fixed_tool_executed": fixed_tool_executed,
            "files_checked": files_checked[:MAX_LISTED_FILES],
            "files_checked_count": len(files_checked),
            "files_checked_truncated": len(files_checked) > MAX_LISTED_FILES,
            "diagnostics": diagnostics,
            "diagnostics_truncated": len(diagnostics) >= MAX_DIAGNOSTICS,
            "source_tree_hash_before": _tree_digest(source_before),
            "source_tree_hash_after": _tree_digest(source_after),
            "git_metadata_hash_before": _tree_digest(git_before),
            "git_metadata_hash_after": _tree_digest(git_after),
            "source_mutation_detected": source_mutation,
            "git_mutation_detected": git_mutation,
            "workspace_cleanup_verified": cleanup_verified,
        }
    )
    if _json_size(evidence) > output_byte_limit:
        evidence.update(
            {
                "pilot_status": L4_BLOCKED,
                "status": "BLOCKED",
                "block_reason": "output byte limit exceeded by bounded evidence",
                "files_checked": [],
                "files_checked_count": len(files_checked),
                "files_checked_truncated": True,
                "diagnostics": [],
                "diagnostics_truncated": bool(diagnostics),
            }
        )
    return _finalize_evidence(evidence, output_byte_limit)


def run_approved_blk_system_051_once(*, now: str, expires_at: str, used_approval_ids: set[str], used_run_ids: set[str]) -> dict[str, Any]:
    return run_blk_test_non_disposable_l4_runtime_pilot(
        target_repo_path=APPROVED_TARGET_REPO,
        source_subtree_path=APPROVED_SOURCE_SUBTREE,
        workspace_clone_path=APPROVED_WORKSPACE,
        approval_id=APPROVAL_ID,
        run_id=RUN_ID,
        expected_head=EXPECTED_HEAD,
        fixed_tool=REQUESTED_TOOL,
        expires_at=expires_at,
        now=now,
        used_approval_ids=used_approval_ids,
        used_run_ids=used_run_ids,
        workspace_marker_nonce="nonce-BLK-SYSTEM-051-non-disposable-l4-runtime-workspace-001",
        output_byte_limit=16384,
    )


def _validate_exact_path_spelling(
    target_repo_path: str | Path,
    source_subtree_path: str | Path,
    workspace_clone_path: str | Path,
    envelope: L4RuntimeApprovalEnvelope,
) -> None:
    _require_exact_spelling(label="target_repo_path", raw_path=target_repo_path, approved_path=envelope.approved_target_repo)
    _require_exact_spelling(label="source_subtree_path", raw_path=source_subtree_path, approved_path=envelope.approved_source_subtree)
    _require_exact_spelling(label="workspace_clone_path", raw_path=workspace_clone_path, approved_path=envelope.approved_workspace)


def _require_exact_spelling(*, label: str, raw_path: str | Path, approved_path: Path) -> None:
    raw_text = os.fspath(raw_path)
    approved_text = os.fspath(approved_path)
    try:
        same_target = Path(raw_text).resolve() == approved_path.resolve()
    except RuntimeError:
        same_target = False
    if same_target and raw_text != approved_text:
        raise ValueError(f"{label} must use the approved exact spelling")


def _validate_paths(repo: Path, source: Path, workspace: Path, envelope: L4RuntimeApprovalEnvelope) -> None:
    if repo != envelope.approved_target_repo.resolve():
        raise ValueError("target_repo_path must match the approved exact target")
    if source != envelope.approved_source_subtree.resolve():
        raise ValueError("source_subtree_path must match the approved exact source subtree")
    if workspace != envelope.approved_workspace.resolve():
        raise ValueError("workspace_clone_path must match the approved exact workspace")
    if not repo.is_dir() or not (repo / ".git").is_dir():
        raise ValueError("target_repo_path must be an existing Git repository")
    if not source.is_dir():
        raise ValueError("source_subtree_path must be an existing directory")
    if repo not in (source, *source.parents):
        raise ValueError("source_subtree_path must resolve inside target_repo_path")
    if repo in (workspace, *workspace.parents) or workspace in (repo, *repo.parents):
        raise ValueError("workspace_clone_path must not overlap target_repo_path")
    if workspace.anchor != "/":
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
    if len(head) == 40 and all(c in "0123456789abcdef" for c in head):
        return head
    if not head.startswith("ref: "):
        raise ValueError("target repository HEAD is not a safe ref")
    ref = head[5:].strip()
    if ".." in ref or not ref.startswith("refs/"):
        raise ValueError("target repository HEAD ref is unsafe")
    ref_path = (repo / ".git" / ref).resolve()
    git_dir = (repo / ".git").resolve()
    if git_dir not in (ref_path, *ref_path.parents):
        raise ValueError("target repository HEAD ref escapes .git")
    return ref_path.read_text(encoding="utf-8").strip()


def _blocked_evidence(**kwargs: Any) -> dict[str, Any]:
    block_reason = kwargs.pop("block_reason")
    output_byte_limit = kwargs["output_byte_limit"]
    evidence = _base_evidence(**kwargs)
    evidence.update(
        {
            "pilot_status": L4_BLOCKED,
            "status": "BLOCKED",
            "block_reason": block_reason,
            "fixed_tool_executed": False,
            "files_checked": [],
            "files_checked_count": 0,
            "files_checked_truncated": False,
            "diagnostics": [],
            "diagnostics_truncated": False,
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
    *,
    sprint: str,
    approval_id: str,
    run_id: str,
    repo: Path,
    source: Path,
    workspace: Path,
    expected_head: str,
    actual_head: str | None,
    replay_consumed: bool,
    output_byte_limit: int,
) -> dict[str, Any]:
    return {
        "sprint": sprint,
        "approval_id": approval_id,
        "run_id": run_id,
        "target_repo_path": str(repo),
        "source_subtree_path": str(source),
        "workspace_clone_path": str(workspace),
        "expected_head": expected_head,
        "actual_head": actual_head,
        "requested_tool": REQUESTED_TOOL,
        "replay_consumed_before_runtime": replay_consumed,
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
        "public_ledger_mutation": False,
        "production_isolation_claimed": False,
        "production_mcp_authority": False,
        "generic_mcp_authority": False,
        "reusable_service_started": False,
        "live_codex_execution": False,
        "arbitrary_shell_called": False,
        "package_manager_called": False,
        "network_called": False,
        "model_service_called": False,
        "browser_tooling_called": False,
        "cyber_tooling_called": False,
        "output_byte_limit": output_byte_limit,
        "evidence_json_bytes": 0,
    }


def _finalize_evidence(evidence: dict[str, Any], output_byte_limit: int) -> dict[str, Any]:
    for _ in range(5):
        size = _json_size(evidence)
        if evidence.get("evidence_json_bytes") == size:
            break
        evidence["evidence_json_bytes"] = size
    if _json_size(evidence) > output_byte_limit:
        compact = {
            "sprint": evidence["sprint"],
            "pilot_status": L4_BLOCKED,
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
        for _ in range(5):
            size = _json_size(compact)
            if compact.get("evidence_json_bytes") == size:
                break
            compact["evidence_json_bytes"] = size
        return compact
    return evidence


def _is_secret_name(name: str) -> bool:
    lowered = name.lower()
    if lowered in SECRET_NAMES:
        return True
    if lowered.startswith(".env."):
        return True
    if lowered.startswith(("credential", "secret", "secrets.", "secrets-", "secrets_", "token", "tokens.", "tokens-", "tokens_")):
        return True
    if lowered in {"id_rsa", "id_dsa", "id_ecdsa", "id_ed25519"}:
        return True
    if "private_key" in lowered or lowered.endswith(".pem"):
        return True
    return False


def _snapshot_tree(root: Path, *, suffix: str | None = None) -> dict[str, str]:
    root_st = root.stat()
    snapshot: dict[str, str] = {
        ".": f"dir:{root_st.st_mode}:{root_st.st_uid}:{root_st.st_gid}:{root_st.st_mtime_ns}:{root_st.st_ctime_ns}"
    }
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            st = path.lstat()
            link_payload = os.readlink(path)
            resolved = path.resolve()
            if root in (resolved, *resolved.parents):
                try:
                    target = resolved.relative_to(root).as_posix()
                except ValueError:
                    target = str(resolved)
            else:
                target = f"ESCAPE:{resolved}"
            snapshot[rel] = f"symlink:{st.st_mode}:{st.st_uid}:{st.st_gid}:{st.st_mtime_ns}:{st.st_ctime_ns}:{link_payload}:resolved:{target}"
        elif path.is_dir():
            st = path.stat()
            snapshot[rel] = f"dir:{st.st_mode}:{st.st_uid}:{st.st_gid}:{st.st_mtime_ns}:{st.st_ctime_ns}"
        elif path.is_file():
            if suffix is not None and path.suffix != suffix:
                continue
            st = path.stat()
            snapshot[rel] = f"file:{st.st_mode}:{st.st_uid}:{st.st_gid}:{st.st_size}:{st.st_mtime_ns}:{st.st_ctime_ns}:{_hash_bytes(path.read_bytes())}"
    return snapshot


def _snapshot_git_metadata(git_dir: Path) -> dict[str, str]:
    root_st = git_dir.stat()
    snapshot: dict[str, str] = {
        ".": f"dir:{root_st.st_mode}:{root_st.st_uid}:{root_st.st_gid}:{root_st.st_mtime_ns}:{root_st.st_ctime_ns}"
    }
    for path in sorted(git_dir.rglob("*")):
        if path.is_symlink():
            raise ValueError("git metadata symlinks are forbidden")
        rel = path.relative_to(git_dir).as_posix()
        if path.is_dir():
            st = path.stat()
            snapshot[rel] = f"dir:{st.st_mode}:{st.st_uid}:{st.st_gid}:{st.st_mtime_ns}:{st.st_ctime_ns}"
        elif path.is_file():
            data = path.read_bytes()
            st = path.stat()
            snapshot[rel] = f"file:{st.st_mode}:{st.st_uid}:{st.st_gid}:{len(data)}:{st.st_mtime_ns}:{st.st_ctime_ns}:{_hash_bytes(data)}"
    return snapshot


def _load_replay_ledger(replay_ledger_path: Path) -> dict[str, list[str]]:
    if not replay_ledger_path.exists():
        return {"approval_ids": [], "run_ids": []}
    data = json.loads(replay_ledger_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("durable replay ledger must be an object")
    approval_ids = data.get("approval_ids", [])
    run_ids = data.get("run_ids", [])
    if not isinstance(approval_ids, list) or not isinstance(run_ids, list):
        raise ValueError("durable replay ledger has invalid shape")
    return {"approval_ids": [str(v) for v in approval_ids], "run_ids": [str(v) for v in run_ids]}


def _write_replay_ledger(replay_ledger_path: Path, ledger: dict[str, list[str]]) -> None:
    replay_ledger_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = replay_ledger_path.with_suffix(replay_ledger_path.suffix + ".tmp")
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
    tmp.replace(replay_ledger_path)


def _tree_digest(snapshot: dict[str, str]) -> str:
    return _hash_bytes(json.dumps(snapshot, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def _hash_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _json_size(value: dict[str, Any]) -> int:
    return len(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def _parse_instant(value: str) -> datetime:
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)
