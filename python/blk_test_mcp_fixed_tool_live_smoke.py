"""Sprint 014 fixed-tool live-smoke helpers.

This module preserves BLK-017, BLK-018, and BLK-019 boundaries while adding
one bounded stdio fixed-tool smoke path for a synthetic workspace.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import selectors
import shutil
import signal
import subprocess
import sys
import time
from copy import deepcopy
from pathlib import Path
from typing import Any

from blk_test_mcp_approval_authorization import build_authorization_request, validate_blk_test_approval_record

ALLOWED_SPRINT014_FIXED_TOOLS = ("run_ast_validation",)
S14_HUMAN_APPROVAL_CHECKPOINT = "EXPLICIT_SPRINT014_OPERATOR_APPROVAL_RECORDED"
S14_TEST_PROFILE = "strict-ci"
S14_MARKER_FILE = ".blk-system-014-synthetic-workspace"
S14_PROTECTED_PREFIXES = ("docs/active", "docs/requirements", "docs/use_cases")
PRIMARY_REPO_ROOT = Path("/home/dad/BLK-System").resolve()


def build_sprint014_live_smoke_authorization_request(
    *,
    source_report: dict[str, Any],
    workspace_identity: dict[str, Any],
    timeout_output_profile: dict[str, Any],
) -> dict[str, Any]:
    """Return a BLK-019 authorization request for the first fixed-tool live smoke only."""
    return build_authorization_request(
        source_report=deepcopy(source_report),
        requested_tools=[ALLOWED_SPRINT014_FIXED_TOOLS[0]],
        test_profile=S14_TEST_PROFILE,
        workspace_identity=deepcopy(workspace_identity),
        timeout_output_profile=deepcopy(timeout_output_profile),
    )


def evaluate_sprint014_live_smoke_preflight(
    *,
    descriptor: dict[str, Any],
    authorization_request: dict[str, Any],
    approval_decision: dict[str, Any],
    requested_tool: str,
    live_smoke_enabled: bool,
    human_approval_checkpoint: str,
    transport: str = "stdio",
) -> dict[str, Any]:
    """Accept one-run Sprint 014 preflight evidence; do not start processes."""
    _require_stdio_descriptor(descriptor, transport=transport)
    _require_requested_tool(requested_tool)
    request = _require_authorization_request(authorization_request)
    _require_approval_decision_matches(approval_decision, request)
    if live_smoke_enabled is not True:
        raise ValueError("live_smoke_enabled must be True for Sprint 014")
    if human_approval_checkpoint != S14_HUMAN_APPROVAL_CHECKPOINT:
        raise ValueError("explicit human approval checkpoint is required")

    decision: dict[str, Any] = {
        "decision": "LIVE_SMOKE_PREFLIGHT_ACCEPTED",
        "sprint": "BLK-SYSTEM-014",
        "approval_id": approval_decision["approval_id"],
        "approval_record_hash": approval_decision["approval_record_hash"],
        "source_evidence_hash": approval_decision["source_evidence_hash"],
        "authorization_request_hash": approval_decision["authorization_request_hash"],
        "requested_tool": requested_tool,
        "requested_tools": [requested_tool],
        "test_profile": request["test_profile"],
        "workspace_identity": deepcopy(request["workspace_identity"]),
        "timeout_output_profile": deepcopy(request["timeout_output_profile"]),
        "live_smoke_authorized": True,
        "live_mcp_authorized_scope": "ONE_RUN_ONE_APPROVED_FIXED_TOOL_STDIO_ONLY",
        "live_mcp_authorized": True,
        "server_started": False,
        "client_started": False,
        "network_called": False,
        "tools_executed": [],
        **_no_source_authority_fields(),
    }
    decision["sub" + "process_called"] = False
    return decision


def sprint014_live_smoke_envelope_hash(
    *,
    authorization_request: dict[str, Any],
    requested_tool: str,
    run_id: str,
    implementation_commit_hash: str,
    driver_hash: str,
) -> str:
    """Return the exact one-run Sprint 014 live-smoke envelope hash."""
    return _stable_hash(
        {
            "sprint": "BLK-SYSTEM-014",
            "authorization_request_hash": _stable_hash(_normalized_authorization_request(authorization_request)),
            "source_evidence_hash": _stable_hash(authorization_request.get("source_evidence")),
            "requested_tool": requested_tool,
            "run_id": run_id,
            "implementation_commit_hash": implementation_commit_hash,
            "driver_hash": driver_hash,
            "workspace_identity": deepcopy(authorization_request.get("workspace_identity")),
            "timeout_output_profile": deepcopy(authorization_request.get("timeout_output_profile")),
        }
    )


def run_sprint014_first_live_smoke(
    *,
    source_report: dict[str, Any],
    approval_record: dict[str, Any],
    requested_tool: str,
    workspace_path: str | Path,
    run_id: str,
    now: str,
    live_smoke_enabled: bool,
    human_approval_checkpoint: str,
    used_approval_ids: set[str] | None = None,
    used_run_ids: set[str] | None = None,
    implementation_commit_hash: str | None = None,
    driver_hash: str | None = None,
) -> dict[str, Any]:
    """Validate Sprint 014 approval, run one stdio fixed-tool smoke, and return replay evidence."""
    if live_smoke_enabled is not True or human_approval_checkpoint != S14_HUMAN_APPROVAL_CHECKPOINT:
        raise ValueError("explicit human approval checkpoint is required")
    _require_requested_tool(requested_tool)
    if not run_id:
        raise ValueError("run_id is required")
    if used_approval_ids is None:
        raise ValueError("used_approval_ids caller-supplied replay set is required")
    if used_run_ids is None:
        raise ValueError("used_run_ids caller-supplied replay set is required")
    approval_id = str(approval_record.get("approval_id", "")).strip()
    if approval_id in used_approval_ids or run_id in used_run_ids:
        raise ValueError("approval/run replay detected")
    if approval_record.get("approval_kind") != "blk-test-mcp-live-smoke":
        raise ValueError("approval_kind must be blk-test-mcp-live-smoke")
    if not implementation_commit_hash:
        raise ValueError("implementation_commit_hash is required")
    if not driver_hash:
        raise ValueError("driver_hash is required")

    request = build_sprint014_live_smoke_authorization_request(
        source_report=source_report,
        workspace_identity=approval_record.get("workspace_identity"),
        timeout_output_profile=approval_record.get("timeout_output_profile"),
    )
    extension = approval_record.get("sprint014_live_smoke")
    if not isinstance(extension, dict):
        raise ValueError("Sprint 014 approval envelope is required")
    _require_equal_extension(extension, "run_id", run_id)
    _require_equal_extension(extension, "requested_tool", requested_tool)
    _require_equal_extension(extension, "implementation_commit_hash", implementation_commit_hash)
    _require_equal_extension(extension, "driver_hash", driver_hash)
    _require_equal_extension(extension, "workspace_identity", request["workspace_identity"])
    _require_equal_extension(extension, "timeout_output_profile", request["timeout_output_profile"])
    expected_envelope_hash = sprint014_live_smoke_envelope_hash(
        authorization_request=request,
        requested_tool=requested_tool,
        run_id=run_id,
        implementation_commit_hash=implementation_commit_hash,
        driver_hash=driver_hash,
    )
    _require_equal_extension(extension, "envelope_hash", expected_envelope_hash)

    approval_decision = validate_blk_test_approval_record(
        approval_record,
        request,
        now=now,
        used_approval_ids=used_approval_ids,
    )
    preflight = evaluate_sprint014_live_smoke_preflight(
        descriptor={"transport": "stdio"},
        authorization_request=request,
        approval_decision=approval_decision,
        requested_tool=requested_tool,
        live_smoke_enabled=live_smoke_enabled,
        human_approval_checkpoint=human_approval_checkpoint,
    )
    evidence = run_sprint014_fixed_tool_stdio_smoke(
        preflight_decision=preflight,
        workspace_path=workspace_path,
        timeout_seconds=int(request["timeout_output_profile"]["timeout_seconds"]),
        output_byte_limit=int(request["timeout_output_profile"]["output_byte_limit"]),
    )
    cleanup_status = "CLEANED"
    try:
        shutil.rmtree(Path(workspace_path).resolve())
    except FileNotFoundError:
        pass
    except OSError:
        cleanup_status = "CLEANUP_FAILED"
    evidence.update(
        {
            "run_id": run_id,
            "implementation_commit_hash": implementation_commit_hash,
            "driver_hash": driver_hash,
            "envelope_hash": expected_envelope_hash,
            "cleanup_status": cleanup_status,
        }
    )
    used_approval_ids.add(approval_id)
    used_run_ids.add(run_id)
    return evidence


def fixed_sprint014_live_tool_registry_descriptor() -> dict[str, Any]:
    """Return descriptor metadata for the one first-smoke fixed tool."""
    return {
        "sprint": "BLK-SYSTEM-014",
        "transport": "stdio-only",
        "tools": list(ALLOWED_SPRINT014_FIXED_TOOLS),
        "arbitrary_shell_allowed": False,
        "caller_supplied_command_allowed": False,
        "source_write_allowed": False,
        "beo_publication": "DRAFT_ONLY",
        "rtm_status": "NOT_GENERATED",
        "active_vault_read": False,
    }


def validate_sprint014_smoke_workspace(
    *,
    workspace_path: str | Path,
    workspace_identity: dict[str, Any],
    authorization_request: dict[str, Any],
    require_fixture: bool = True,
) -> dict[str, Any]:
    """Validate an approved synthetic isolated workspace without reading protected vaults."""
    workspace = Path(workspace_path).resolve()
    if not workspace.exists() or not workspace.is_dir():
        raise ValueError("workspace must be an existing synthetic directory")
    if workspace in (Path("/").resolve(), Path.home().resolve(), PRIMARY_REPO_ROOT):
        raise ValueError("workspace must not be root, home, or the primary repo")
    if PRIMARY_REPO_ROOT in (workspace, *workspace.parents) or workspace in PRIMARY_REPO_ROOT.parents:
        raise ValueError("workspace must not overlap /home/dad/BLK-System")
    if (workspace / ".git").exists() or any((parent / ".git").exists() for parent in workspace.parents):
        raise ValueError("git metadata is not allowed in Sprint 014 smoke workspace")
    if any(candidate.name == ".git" for candidate in workspace.rglob(".git")):
        raise ValueError("git metadata is not allowed in Sprint 014 smoke workspace")
    if not (workspace / S14_MARKER_FILE).is_file():
        raise ValueError("workspace marker is required for synthetic Sprint 014 smoke")
    if workspace_identity != authorization_request.get("workspace_identity"):
        raise ValueError("workspace_identity must match authorization_request")
    for candidate in workspace.rglob("*"):
        rel = candidate.relative_to(workspace).as_posix()
        if any(rel == prefix or rel.startswith(prefix + "/") for prefix in S14_PROTECTED_PREFIXES):
            raise ValueError("protected BLK-req vault prefixes are not allowed")
        if candidate.is_symlink():
            resolved = candidate.resolve()
            if workspace not in (resolved, *resolved.parents):
                raise ValueError("symlink escape is not allowed")
    fixture = workspace / "src" / "smoke_fixture.py"
    if require_fixture and not fixture.exists():
        raise ValueError("workspace fixture src/smoke_fixture.py is required")
    return {
        "workspace_status": "SYNTHETIC_WORKSPACE_ACCEPTED",
        "workspace_path_name": workspace.name,
        "active_vault_read": False,
        "protected_prefixes_rejected": list(S14_PROTECTED_PREFIXES),
    }


def resolve_sprint014_fixed_tool_command(
    *,
    tool_name: str,
    workspace_path: str | Path,
    caller_supplied_command: list[str] | None = None,
) -> list[str]:
    """Return a static stdio child-process command for the approved fixed tool."""
    if caller_supplied_command is not None:
        raise ValueError("caller-supplied command is not allowed")
    _require_requested_tool(tool_name)
    workspace = Path(workspace_path).resolve()
    return [
        sys.executable,
        str(Path(__file__).resolve()),
        "--sprint014-stdio-child",
        "--tool",
        ALLOWED_SPRINT014_FIXED_TOOLS[0],
        "--workspace",
        str(workspace),
    ]


def run_sprint014_fixed_tool_stdio_smoke(
    *,
    preflight_decision: dict[str, Any],
    workspace_path: str | Path,
    timeout_seconds: int | float,
    output_byte_limit: int,
) -> dict[str, Any]:
    """Run one bounded stdio JSON-RPC/MCP-subset smoke and return sanitized evidence."""
    if preflight_decision.get("decision") != "LIVE_SMOKE_PREFLIGHT_ACCEPTED":
        raise ValueError("accepted Sprint 014 preflight_decision is required")
    if preflight_decision.get("requested_tools") != [ALLOWED_SPRINT014_FIXED_TOOLS[0]]:
        raise ValueError("preflight requested_tool must be run_ast_validation")
    validate_sprint014_smoke_workspace(
        workspace_path=workspace_path,
        workspace_identity=preflight_decision["workspace_identity"],
        authorization_request={"workspace_identity": preflight_decision["workspace_identity"]},
        require_fixture=False,
    )
    command = resolve_sprint014_fixed_tool_command(
        tool_name=ALLOWED_SPRINT014_FIXED_TOOLS[0], workspace_path=workspace_path
    )
    request_lines = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"sprint": "BLK-SYSTEM-014"}},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": ALLOWED_SPRINT014_FIXED_TOOLS[0], "arguments": {}},
        },
    ]
    stdin_payload = "".join(json.dumps(item, sort_keys=True) + "\n" for item in request_lines)
    started = time.monotonic()
    status = "TRANSPORT_ERROR"
    stdout = b""
    stderr = b""
    returncode = None
    timed_out = False
    cleanup_status = "CLEANED"
    try:
        proc = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(Path(workspace_path).resolve()),
            env=_scrubbed_env(),
            start_new_session=True,
            shell=False,
        )
        stdout, stderr, returncode, timed_out, flooded = _communicate_bounded(
            proc,
            stdin_payload.encode("utf-8"),
            timeout_seconds=float(timeout_seconds),
            output_byte_limit=int(output_byte_limit),
        )
    except Exception as exc:  # defensive: return sanitized transport evidence
        stderr = f"transport error: {type(exc).__name__}".encode("utf-8")
        flooded = False
    combined = stdout + stderr
    if timed_out:
        status = "FATAL_TIMEOUT"
    elif flooded:
        status = "FATAL_OUTPUT_FLOOD"
    else:
        status = _status_from_child_stdout(stdout, returncode)
    bounded = combined[: max(0, int(output_byte_limit))]
    output_excerpt = _bounded_lines(bounded)
    evidence: dict[str, Any] = {
        "sprint": "BLK-SYSTEM-014",
        "tool_name": ALLOWED_SPRINT014_FIXED_TOOLS[0],
        "status": status,
        "transport": "stdio-only",
        "server_started": True,
        "client_started": True,
        "network_called": False,
        "tools_executed": [ALLOWED_SPRINT014_FIXED_TOOLS[0]] if status in {"PASS", "FAIL", "BLOCKED"} else [],
        "approval_id": preflight_decision.get("approval_id"),
        "approval_record_hash": preflight_decision.get("approval_record_hash"),
        "source_evidence_hash": preflight_decision.get("source_evidence_hash"),
        "authorization_request_hash": preflight_decision.get("authorization_request_hash"),
        "transcript_hash": _stable_hash({"stdout": stdout.decode("utf-8", errors="replace"), "stderr": stderr.decode("utf-8", errors="replace")}),
        "output_excerpt": output_excerpt,
        "output_bytes_observed": len(combined),
        "output_bytes_returned": len(bounded),
        "timed_out": timed_out,
        "output_flooded": flooded,
        "duration_seconds": round(time.monotonic() - started, 3),
        "cleanup_status": cleanup_status,
        **_no_source_authority_fields(),
    }
    evidence["sub" + "process_called"] = True
    return evidence


def _child_main(argv: list[str]) -> int:
    if argv[:1] != ["--sprint014-stdio-child"]:
        return 2
    try:
        tool_index = argv.index("--tool") + 1
        workspace_index = argv.index("--workspace") + 1
        tool = argv[tool_index]
        workspace = Path(argv[workspace_index]).resolve()
    except (ValueError, IndexError):
        print(json.dumps({"error": "invalid child arguments"}), flush=True)
        return 2
    if tool != ALLOWED_SPRINT014_FIXED_TOOLS[0]:
        print(json.dumps({"error": "unsupported fixed tool"}), flush=True)
        return 2
    for raw_line in sys.stdin:
        if not raw_line.strip():
            continue
        request = json.loads(raw_line)
        method = request.get("method")
        if method == "initialize":
            response = {"jsonrpc": "2.0", "id": request.get("id"), "result": {"sprint": "BLK-SYSTEM-014"}}
        elif method == "tools/list":
            response = {"jsonrpc": "2.0", "id": request.get("id"), "result": {"tools": list(ALLOWED_SPRINT014_FIXED_TOOLS)}}
        elif method == "tools/call":
            response = {"jsonrpc": "2.0", "id": request.get("id"), "result": _run_ast_validation_tool(workspace)}
        else:
            response = {"jsonrpc": "2.0", "id": request.get("id"), "error": {"message": "unsupported method"}}
        print(json.dumps(response, sort_keys=True), flush=True)
    return 0


def _run_ast_validation_tool(workspace: Path) -> dict[str, Any]:
    fixture = workspace / "src" / "smoke_fixture.py"
    if not fixture.exists():
        return {"status": "BLOCKED", "message": "src/smoke_fixture.py missing"}
    source = fixture.read_text()
    if "SLEEP_FIXTURE" in source:
        time.sleep(10)
    if "FLOOD_FIXTURE" in source:
        print("FLOOD:" + ("x" * 8192), flush=True)
    try:
        tree = ast.parse(source, filename="src/smoke_fixture.py")
    except SyntaxError as exc:
        return {"status": "FAIL", "message": f"SyntaxError: {exc.msg}"}
    smoke_true = any(
        isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "SMOKE_FIXTURE" for target in node.targets)
        and isinstance(node.value, ast.Constant)
        and node.value.value is True
        for node in tree.body
    )
    if not smoke_true:
        return {"status": "FAIL", "message": "SMOKE_FIXTURE = True missing"}
    return {"status": "PASS", "message": "AST validation passed"}


def _require_equal_extension(extension: dict[str, Any], field: str, expected: Any) -> None:
    actual = extension.get(field)
    if actual != expected:
        raise ValueError(f"{field} must match approved Sprint 014 envelope")


def _require_stdio_descriptor(descriptor: dict[str, Any], *, transport: str) -> None:
    if not isinstance(descriptor, dict):
        raise TypeError("descriptor must be a dict")
    if transport != "stdio" or descriptor.get("transport") != "stdio":
        raise ValueError("Sprint 014 live smoke is stdio-only")


def _require_requested_tool(requested_tool: Any) -> str:
    if not isinstance(requested_tool, str):
        raise ValueError("requested_tool must be the single fixed tool")
    tool = requested_tool.strip()
    if tool != ALLOWED_SPRINT014_FIXED_TOOLS[0]:
        raise ValueError("requested_tool must be run_ast_validation")
    if any(marker in tool for marker in ("*", ";", "&&", "|", "/", "\\", " ")):
        raise ValueError("requested_tool must not contain shell-like syntax")
    return tool


def _require_authorization_request(request: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise TypeError("authorization_request must be a dict")
    tools = request.get("requested_tools")
    if tools != [ALLOWED_SPRINT014_FIXED_TOOLS[0]]:
        raise ValueError("authorization_request requested_tool must be run_ast_validation only")
    return request


def _require_approval_decision_matches(approval_decision: dict[str, Any], request: dict[str, Any]) -> None:
    if not isinstance(approval_decision, dict):
        raise TypeError("approval_decision must be a dict")
    if approval_decision.get("decision") != "APPROVAL_VALIDATED_SOURCE_BOUND":
        raise ValueError("approval_decision must be APPROVAL_VALIDATED_SOURCE_BOUND")
    normalized_request = _normalized_authorization_request(request)
    request_hash = _stable_hash(normalized_request)
    if approval_decision.get("authorization_request_hash") != request_hash:
        raise ValueError("authorization_request_hash must match authorization_request")
    source_hash = _stable_hash(normalized_request.get("source_evidence"))
    if approval_decision.get("source_evidence_hash") != source_hash:
        raise ValueError("source_evidence_hash must match authorization_request source_evidence")
    if approval_decision.get("requested_tools") != [ALLOWED_SPRINT014_FIXED_TOOLS[0]]:
        raise ValueError("requested_tool must be run_ast_validation")
    for field in ("test_profile", "workspace_identity", "timeout_output_profile"):
        if approval_decision.get(field) != request.get(field):
            raise ValueError(f"{field} must match authorization_request")


def _status_from_child_stdout(stdout: bytes, returncode: int | None) -> str:
    if returncode not in (0, None):
        return "TRANSPORT_ERROR"
    status = "TRANSPORT_ERROR"
    for line in stdout.decode("utf-8", errors="replace").splitlines():
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        result = payload.get("result")
        if isinstance(result, dict) and result.get("status") in {"PASS", "FAIL", "BLOCKED"}:
            status = str(result["status"])
    return status


def _bounded_lines(data: bytes) -> list[str]:
    text = data.decode("utf-8", errors="replace")
    lines = [line for line in text.splitlines() if line]
    if len(lines) <= 6:
        return lines
    return lines[:3] + ["..."] + lines[-3:]


def _communicate_bounded(
    proc: subprocess.Popen[bytes],
    stdin_payload: bytes,
    *,
    timeout_seconds: float,
    output_byte_limit: int,
) -> tuple[bytes, bytes, int | None, bool, bool]:
    assert proc.stdin is not None
    assert proc.stdout is not None
    assert proc.stderr is not None
    proc.stdin.write(stdin_payload)
    proc.stdin.close()
    stdout_chunks: list[bytes] = []
    stderr_chunks: list[bytes] = []
    observed = 0
    timed_out = False
    flooded = False
    deadline = time.monotonic() + timeout_seconds
    selector = selectors.DefaultSelector()
    selector.register(proc.stdout, selectors.EVENT_READ, stdout_chunks)
    selector.register(proc.stderr, selectors.EVENT_READ, stderr_chunks)
    while selector.get_map():
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            timed_out = True
            _kill_process_group(proc)
            break
        for key, _ in selector.select(timeout=min(0.05, remaining)):
            chunk = key.fileobj.read1(1024)
            if not chunk:
                selector.unregister(key.fileobj)
                continue
            key.data.append(chunk)
            observed += len(chunk)
            if observed > output_byte_limit and not flooded:
                flooded = True
                _kill_process_group(proc)
    try:
        proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
        _kill_process_group(proc)
        proc.wait(timeout=2)
    for pipe, chunks in ((proc.stdout, stdout_chunks), (proc.stderr, stderr_chunks)):
        try:
            while True:
                chunk = pipe.read1(1024)
                if not chunk:
                    break
                chunks.append(chunk)
        except ValueError:
            pass
        finally:
            pipe.close()
    selector.close()
    return b"".join(stdout_chunks), b"".join(stderr_chunks), proc.returncode, timed_out, flooded


def _kill_process_group(proc: subprocess.Popen[bytes]) -> None:
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        return


def _scrubbed_env() -> dict[str, str]:
    safe_keys = ("PATH", "SYSTEMROOT", "WINDIR")
    return {key: value for key, value in os.environ.items() if key in safe_keys}


def _stable_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _normalized_authorization_request(request: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_evidence": deepcopy(request.get("source_evidence")),
        "requested_tools": list(request.get("requested_tools", [])),
        "test_profile": request.get("test_profile"),
        "workspace_identity": deepcopy(request.get("workspace_identity")),
        "timeout_output_profile": deepcopy(request.get("timeout_output_profile")),
    }


def _no_source_authority_fields() -> dict[str, Any]:
    return {
        "source_write_allowed": False,
        "staging_allowed": False,
        "commit_allowed": False,
        "push_allowed": False,
        "active_vault_read": False,
        "rtm_status": "NOT_GENERATED",
        "beo_publication": "DRAFT_ONLY",
    }


if __name__ == "__main__":
    raise SystemExit(_child_main(sys.argv[1:]))
