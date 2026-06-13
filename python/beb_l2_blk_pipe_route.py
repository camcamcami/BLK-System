"""BEB-L2 drop route for Kuronode Codex work through BLK-pipe.

The route is deliberately closed: the drop manifest selects an exact approved
BEB/L2 artifact pair and exact target commit, while BLK-System injects the Codex
engine and validation-profile execution surface. Caller manifests cannot name a
shell engine, validation commands, trace artifacts, or the L2 body directly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Iterable

from blk_pipe_adapter import BlkPipeAdapter


class RouteError(ValueError):
    """Raised when a BEB-L2 drop is unsafe or malformed before BLK-pipe dispatch."""


_CORE_DROP_FIELDS = {
    "target_project",
    "beb_id",
    "l2_id",
    "beb_path",
    "beb_sha256",
    "l2_path",
    "l2_sha256",
    "work_dir",
    "target_branch",
    "target_hash",
    "allowed_modified_files",
    "allowed_new_files",
    "validation_profiles",
}
_OPTIONAL_DROP_FIELDS = {
    "beo_id",
    "beo_path",
    "beo_sha256",
}
_OPTIONAL_PROFILE_DROP_FIELDS = {
    "readiness_profiles",
}
_ALLOWED_DROP_FIELDS = _CORE_DROP_FIELDS | _OPTIONAL_DROP_FIELDS | _OPTIONAL_PROFILE_DROP_FIELDS
_FORBIDDEN_DROP_FIELDS = {
    "engine",
    "engine_args",
    "engine_command",
    "validation_commands",
    "l2_packet",
    "trace_artifacts",
}
_TRACE_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_GIT_HASH_RE = re.compile(r"^[0-9a-f]{40}$")
_K2_SEQUENCE_RE = r"(?:00[1-9]|0[1-9][0-9]|[1-9][0-9]{2})"
_FAMILY_SEQUENCE_RE = r"[A-Z][A-Z0-9]{1,7}-" + _K2_SEQUENCE_RE
_LEGACY_SEQUENCE_RE = r"[A-Za-z0-9_-]+"
_BEB_ID_RE = re.compile(rf"^BEB(?:_{_LEGACY_SEQUENCE_RE}|-{_FAMILY_SEQUENCE_RE})$")
_L2_ID_RE = re.compile(rf"^L2(?:_{_LEGACY_SEQUENCE_RE}|-{_FAMILY_SEQUENCE_RE})$")
_BEO_ID_RE = re.compile(rf"^BEO(?:_{_LEGACY_SEQUENCE_RE}|-{_FAMILY_SEQUENCE_RE})$")
_ARTIFACT_SLUG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
_ALLOWED_VALIDATION_PROFILES = {
    "go-test",
    "go-vet",
    "go-full",
    "python-unittest",
    "docs-doctrine-gates",
    "kuronode-power-of-ten-static-fixture",
    "kuronode-worktree-static",
    "kuronode-worktree-focused-node",
}
_CALLER_OBJECT_CONTROL_PLANE_PROFILE = "kuronode-caller-object-control-plane-v1"
_RENDERER_PUBLIC_SURFACE_PROFILE = "kuronode-renderer-public-surface-v1"
_AGENT_A_PROMOTION_REQUEST_PROFILE = "kuronode-agent-a-promotion-request-v1"
_DEFAULT_CLEAN_WORKTREE_ROOT = Path("/tmp/blk-system-clean-worktrees")
_ALLOWED_READINESS_PROFILES = {
    _CALLER_OBJECT_CONTROL_PLANE_PROFILE,
    _RENDERER_PUBLIC_SURFACE_PROFILE,
    _AGENT_A_PROMOTION_REQUEST_PROFILE,
}
_READINESS_PROFILE_PROBES = {
    _CALLER_OBJECT_CONTROL_PLANE_PROFILE: (
        ("KCP-001", "direct accepted ready input"),
        ("KCP-002", "wrapper accepted ready input"),
        ("KCP-003", "top-level denied raw/authority/source/provider/parser/import/export/mutation fail closed"),
        ("KCP-004", "nested denied raw/authority/source/provider/parser/import/export/mutation fail closed"),
        ("KCP-005", "raw marker values fail closed and do not serialize back out"),
        ("KCP-006", "duplicate filters or entries beyond cap fail closed"),
        ("KCP-007", "proxy/getter/callable/symbol inputs fail closed without invoking caller code"),
        ("KCP-008", "public capability/result objects deeply frozen and public getters have no mutable prototype"),
        ("KCP-009", "helper vocabulary confined to owning module/tests"),
        ("KCP-010", "downstream compatibility probe for the paired payload/capability surface"),
        ("KCP-011", "deep hostile object graph hits a bounded circuit breaker without throwing"),
        ("KCP-012", "caller authority/status/trust laundering fields force fail-closed false readiness"),
    ),
    _RENDERER_PUBLIC_SURFACE_PROFILE: (
        ("KRP-001", "exact public renderer export/key set is asserted; no full app/model/view-model exposure unless explicitly authorized"),
        ("KRP-002", "denied-authority/status/security rows derive from a fixed catalog, not arbitrary object keys"),
        ("KRP-003", "hostile JavaScript objects, proxies, getters, symbols, and descriptor traps fail closed without leaking raw fields"),
        ("KRP-004", "public presentation objects are deeply frozen and expose no callable, DOM, prototype, or mutable handles"),
        ("KRP-005", "markup and visible rows are static and escaped; raw source/model/path/provider/prompt/credential/diagnostic/telemetry fragments are forbidden"),
        ("KRP-006", "canvas/layout/persistence/filesystem/provider/import/export/mutation/RTM/blk-link/BEO-publication authorities remain visibly denied"),
        ("KRP-007", "degraded, warning, stale, contradictory, or untrusted evidence chooses the stricter visible fail-closed state"),
        ("KRP-008", "conditional pre-dispatch evidence for renderer-visible public surfaces only; the profile does not authorize source/Git mutation and does not make this profile mandatory for non-renderer slices"),
    ),
    _AGENT_A_PROMOTION_REQUEST_PROFILE: (
        ("KAPR-001", "promotion request/preflight envelope remains pure data and request-only; it does not authorize source/Git mutation, approval, import, adoption, promotion execution, or canonical mutation"),
        ("KAPR-002", "JSON-like finite evidence graphs are the only accepted caller evidence shape; non-plain containers fail closed before hashing"),
        ("KAPR-003", "Map, Set, Date, RegExp, typed array, boxed primitive, class instance, promise, error, callable, and symbol inputs fail closed without iteration or coercion"),
        ("KAPR-004", "NaN/Infinity/null hash-alias probes fail closed before canonical JSON hashing"),
        ("KAPR-005", "own enumerable __proto__ evidence is represented as data or rejected; prototype mutation cannot hide authority text"),
        ("KAPR-006", "proxy, revoked-proxy, getter/accessor, blockedReasons.length trap, and descriptor trap inputs fail closed without invoking caller code"),
        ("KAPR-007", "contentFingerprint and candidate identity fields require exact primitive strings; object-to-string coercion must not leak or pass"),
        ("KAPR-008", "nested exact blk-link, RTM, BEO publication, provider-call, source/Git mutation, save/export/session-persistence, and approval-capture claims are denied"),
        ("KAPR-009", "returned request/preflight descriptors are deeply frozen and preserve false denied-authority flags"),
        ("KAPR-010", "closeout includes hostile probes for readiness-array getters, nested denied tokens, __proto__, Map hiding, and NaN/Infinity/null hash aliases"),
    ),
}
_READINESS_PROFILE_SECTION_HEADING = "## Readiness profile probe card"
_READINESS_PROFILE_NON_AUTHORITY_DISCLAIMER = (
    "These probes are required pre-dispatch checklist evidence only. They do not authorize source/Git mutation, parser execution, provider/runtime dispatch, BEO publication, RTM generation, or reusable BLK-pipe/Codex authority beyond the exact approved drop."
)
_PROTECTED_ALLOWLIST_PREFIXES = ("docs/active/", "docs/requirements/", "docs/use_cases/")
_PROTECTED_BLK_REQ_SEGMENTS = (
    ("docs", "active"),
    ("docs", "requirements"),
    ("docs", "use_cases"),
)
_GLOB_CHARS = set("*?[")


def build_kuronode_codex_engine_args(
    *,
    model: str = "gpt-5.5",
    reasoning_effort: str = "xhigh",
    beb_id: str | None = None,
    target_hash: str | None = None,
) -> list[str]:
    """Return the BLK-System-owned Codex argv for Kuronode BEB-L2 dispatch."""
    model = _required_string(model, "model")
    reasoning_effort = _required_string(reasoning_effort, "reasoning_effort")
    if model != "gpt-5.5":
        raise RouteError("codex model must be gpt-5.5 for the current route contract")
    if reasoning_effort != "xhigh":
        raise RouteError("reasoning_effort must be xhigh for the current route contract")
    final_message_artifact = "artifacts/codex/final-message.md"
    if beb_id is not None or target_hash is not None:
        final_message_artifact = str(_prepare_external_codex_final_message_artifact(beb_id, target_hash))
    return [
        "exec",
        "--sandbox",
        "workspace-write",
        "-",
        "--json",
        "--ephemeral",
        "--ignore-user-config",
        "--ignore-rules",
        "--disable",
        "hooks",
        "--disable",
        "plugins",
        "--disable",
        "goals",
        "--model",
        model,
        "-c",
        f'model_reasoning_effort="{reasoning_effort}"',
        "--output-last-message",
        final_message_artifact,
    ]


def prepare_beb_l2_drop_package(
    *,
    package_dir: str | Path,
    beb_id: str,
    l2_id: str,
    work_dir: str | Path,
    target_branch: str,
    target_hash: str,
    objective: str,
    l2_instructions: str,
    allowed_modified_files: list[str],
    allowed_new_files: list[str],
    validation_profiles: list[str],
    trace_artifacts: list[dict[str, str]],
    readiness_profiles: list[str] | None = None,
    beo_id: str | None = None,
    artifact_slug: str | None = None,
    obsidian_mirror_dir: str | Path | None = None,
    extra_manifest_fields: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a hash-bound BEB/L2/drop package from a small trusted spec.

    This is an ergonomics helper only: it writes the artifacts and returns the
    approval hash that must still be passed as trusted configuration before
    dispatch. It deliberately refuses caller-controlled engine/L2 manifest fields.
    """
    safe_beb_id = _required_pattern(beb_id, "beb_id", _BEB_ID_RE)
    safe_l2_id = _required_pattern(l2_id, "l2_id", _L2_ID_RE)
    safe_work_dir = _required_absolute_path(str(work_dir), "work_dir")
    safe_target_branch = _required_string(target_branch, "target_branch")
    safe_target_hash = _required_pattern(target_hash, "target_hash", _GIT_HASH_RE)
    safe_objective = _required_string(objective, "objective")
    safe_l2_instructions = _required_string(l2_instructions, "l2_instructions")
    safe_allowed_modified = _required_path_list(allowed_modified_files, "allowed_modified_files")
    safe_allowed_new = _required_path_list(allowed_new_files, "allowed_new_files")
    safe_validation_profiles = _required_validation_profiles(validation_profiles)
    safe_trace_artifacts = _required_trace_artifacts(trace_artifacts)
    safe_readiness_profiles = _optional_readiness_profiles(readiness_profiles)
    safe_beo_id = _required_matching_beo_id(beo_id, safe_beb_id)
    _assert_l2_matches_beb(safe_l2_id, safe_beb_id)
    safe_artifact_slug = _optional_artifact_slug(artifact_slug)

    extra = dict(extra_manifest_fields or {})
    if extra:
        forbidden = sorted(field for field in extra if field in _FORBIDDEN_DROP_FIELDS)
        if forbidden:
            raise RouteError(f"drop package cannot supply caller-controlled manifest fields: {', '.join(forbidden)}")
        raise RouteError(f"drop package cannot override canonical manifest fields: {', '.join(sorted(extra))}")

    package_candidate = Path(package_dir).expanduser()
    package_unresolved = package_candidate if package_candidate.is_absolute() else Path.cwd() / package_candidate
    _reject_symlinked_components(package_unresolved, "BEB-L2 package_dir")
    package_path = package_candidate.resolve()
    _reject_symlinked_components(package_path, "BEB-L2 package_dir")
    package_path.mkdir(parents=True, exist_ok=True, mode=0o700)
    _reject_symlinked_components(package_path, "BEB-L2 package_dir")

    beb_path = package_path / _artifact_filename(safe_beb_id, safe_artifact_slug)
    l2_path = package_path / _artifact_filename(safe_l2_id, safe_artifact_slug)
    beo_path = package_path / _artifact_filename(safe_beo_id, safe_artifact_slug)
    drop_path = package_path / "drop.json"
    for path in (beb_path, l2_path, beo_path, drop_path):
        if path.is_symlink():
            raise RouteError("BEB-L2 package artifact paths must not be symlinks")

    trace_lines = []
    for artifact in safe_trace_artifacts:
        trace_lines.extend(
            [
                f"  - kind: \"{artifact['kind']}\"",
                f"    id: \"{artifact['id']}\"",
                f"    version_hash: \"{artifact['version_hash']}\"",
            ]
        )
    readiness_lines = _readiness_profile_section_lines(safe_readiness_profiles)
    beb_text = "\n".join(
        [
            "---",
            f"beb_id: \"{safe_beb_id}\"",
            f"beo_id: \"{safe_beo_id}\"",
            f"l2_id: \"{safe_l2_id}\"",
            "trace_artifacts:",
            *trace_lines,
            "---",
            f"# {safe_beb_id}",
            "",
            safe_objective,
            "",
            *readiness_lines,
        ]
    )
    l2_text = "\n".join(
        [
            f"L2_ID: {safe_l2_id}",
            f"BEB_ID: {safe_beb_id}",
            f"BEO_ID: {safe_beo_id}",
            "MODEL: gpt-5.5",
            "ROUTE: BEB-L2 -> BLK-pipe -> Codex workspace-write",
            "",
            safe_l2_instructions,
            "",
            *readiness_lines,
        ]
    )
    beo_text = "\n".join(
        [
            "---",
            f"beo_id: \"{safe_beo_id}\"",
            f"beb_id: \"{safe_beb_id}\"",
            f"l2_id: \"{safe_l2_id}\"",
            "status: \"BEO_TEMPLATE_PENDING_EXECUTION_EVIDENCE\"",
            "trace_artifacts:",
            *trace_lines,
            "---",
            f"# {safe_beo_id}",
            "",
            "BEO_TEMPLATE_PENDING_EXECUTION_EVIDENCE",
            "",
            "This matching BEO artifact is a bounded outcome/evidence template for the paired BEB. It is not BEO publication, runtime approval, RTM generation, signer/storage/ledger action, or reusable dispatch authority.",
            "",
        ]
    )
    beb_path.write_text(beb_text)
    l2_path.write_text(l2_text)
    beo_path.write_text(beo_text)

    manifest = {
        "target_project": "kuronode",
        "beb_id": safe_beb_id,
        "beo_id": safe_beo_id,
        "l2_id": safe_l2_id,
        "beb_path": str(beb_path),
        "beb_sha256": _file_sha256(beb_path),
        "beo_path": str(beo_path),
        "beo_sha256": _file_sha256(beo_path),
        "l2_path": str(l2_path),
        "l2_sha256": _file_sha256(l2_path),
        "work_dir": safe_work_dir,
        "target_branch": safe_target_branch,
        "target_hash": safe_target_hash,
        "allowed_modified_files": safe_allowed_modified,
        "allowed_new_files": safe_allowed_new,
        "validation_profiles": safe_validation_profiles,
    }
    if safe_readiness_profiles:
        manifest["readiness_profiles"] = safe_readiness_profiles
    drop_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    approved_drop_sha256 = _file_sha256(drop_path)
    obsidian_mirror_paths = _write_obsidian_view_mirrors(
        obsidian_mirror_dir,
        artifacts=[beb_path, l2_path, beo_path],
    )
    return {
        "status": "BEB_L2_DROP_PACKAGE_READY",
        "package_dir": str(package_path),
        "beb_id": safe_beb_id,
        "beo_id": safe_beo_id,
        "l2_id": safe_l2_id,
        "beb_path": str(beb_path),
        "beb_sha256": manifest["beb_sha256"],
        "beo_path": str(beo_path),
        "beo_sha256": manifest["beo_sha256"],
        "l2_path": str(l2_path),
        "l2_sha256": manifest["l2_sha256"],
        "drop_path": str(drop_path),
        "approved_drop_sha256": approved_drop_sha256,
        "obsidian_mirror_paths": [str(path) for path in obsidian_mirror_paths],
        "readiness_profiles": safe_readiness_profiles,
        "target_hash": safe_target_hash,
        "manifest_approval_required": True,
        "dispatch_authorized": False,
    }


def scan_final_beo_closeout_placeholders(beo_text: str, *, beo_id: str | None = None) -> dict[str, Any]:
    """Fail closed before a final BEO hash freeze if closeout metadata is still placeholder-like."""
    text = _required_string(beo_text, "beo_text")
    blockers: list[dict[str, Any]] = []
    lowered = text.casefold()
    if beo_id is not None:
        safe_beo_id = _required_pattern(beo_id, "beo_id", _BEO_ID_RE)
        if safe_beo_id not in text:
            blockers.append({
                "code": "BEO_ID_MISMATCH",
                "message": "final BEO text must contain the expected BEO id before hash freeze",
                "paths": [],
            })
    status_matches = re.findall(r'^\s*status:\s*"?([^"\n]+)"?\s*$', text, re.MULTILINE)
    if not status_matches:
        blockers.append({
            "code": "MISSING_FINAL_BEO_STATUS",
            "message": "final BEO must include an explicit closed/final status before hash freeze",
            "paths": [],
        })
    elif len(status_matches) > 1:
        blockers.append({
            "code": "DUPLICATE_FINAL_BEO_STATUS",
            "message": "final BEO must include exactly one unambiguous status before hash freeze",
            "paths": [],
        })
    else:
        normalized_status = status_matches[0].strip().casefold()
        if normalized_status not in {"closed", "final", "complete", "completed"}:
            blockers.append({
                "code": "PENDING_BEO_TEMPLATE_STATUS"
                if normalized_status in {"pending", "beo_template_pending_execution_evidence"}
                else "NON_FINAL_BEO_STATUS",
                "message": "final BEO status must be closed/final before the BEO hash is frozen",
                "paths": [],
            })
    pending_markers = (
        "BEO_TEMPLATE_PENDING_EXECUTION_EVIDENCE",
        'status: "pending"',
        "status: pending",
        'status: "beo_template_pending_execution_evidence"',
    )
    if any(marker.casefold() in lowered for marker in pending_markers) and not any(
        blocker["code"] == "PENDING_BEO_TEMPLATE_STATUS" for blocker in blockers
    ):
        blockers.append({
            "code": "PENDING_BEO_TEMPLATE_STATUS",
            "message": "final BEO status must be closed/final before the BEO hash is frozen",
            "paths": [],
        })
    placeholder_patterns = (
        "this kuronode closeout metadata commit",
        "this closeout metadata commit",
        "pending-k2",
        "pending closeout",
        "pending dispatch",
        "placeholder",
        "tbd",
        "todo",
    )
    for pattern in placeholder_patterns:
        if pattern in lowered:
            blockers.append({
                "code": "PLACEHOLDER_CLOSEOUT_METADATA_COMMIT" if "commit" in pattern or "pending" in pattern else "PLACEHOLDER_CLOSEOUT_TEXT",
                "message": f"final BEO contains placeholder text: {pattern}",
                "paths": [],
            })
            break
    commit_match = re.search(r'closeout_metadata_commit:\s*"?([^"\n]+)"?', text)
    if commit_match is None:
        blockers.append({
            "code": "MISSING_CLOSEOUT_METADATA_COMMIT",
            "message": "final BEO must bind the exact closeout metadata commit before hash freeze",
            "paths": [],
        })
    else:
        commit_value = commit_match.group(1).strip()
        if not _GIT_HASH_RE.match(commit_value):
            blockers.append({
                "code": "INVALID_CLOSEOUT_METADATA_COMMIT",
                "message": "closeout_metadata_commit must be a full 40-character lowercase Git hash",
                "paths": [],
            })
    canonical_sha256 = "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()
    return {
        "status": "FINAL_BEO_PLACEHOLDER_SCAN_BLOCKED" if blockers else "FINAL_BEO_PLACEHOLDER_SCAN_PASS",
        "hash_freeze_allowed": not blockers,
        "canonical_sha256": canonical_sha256,
        "blockers": blockers,
    }


def archive_k2_route_evidence(*, package_dir: str | Path, route_summaries: list[dict[str, Any]]) -> dict[str, Any]:
    """Materialize sanitized K2 route evidence under a route package directory.

    This is archival only. It copies compact route summaries and Codex final-message
    artifacts into the package evidence root but never grants dispatch or BEO/RTM
    authority.
    """
    if not isinstance(route_summaries, list) or not route_summaries:
        raise RouteError("route_summaries must be a non-empty list")
    package_candidate = Path(package_dir).expanduser()
    package_unresolved = package_candidate if package_candidate.is_absolute() else Path.cwd() / package_candidate
    _reject_symlinked_components(package_unresolved, "K2 route package_dir")
    package_path = package_candidate.resolve()
    package_path.mkdir(parents=True, exist_ok=True, mode=0o700)
    _reject_symlinked_components(package_path, "K2 route package_dir")
    evidence_dir = package_path / "route-evidence"
    if evidence_dir.is_symlink():
        raise RouteError("K2 route evidence directory must not be a symlink")
    evidence_dir.mkdir(parents=True, exist_ok=True, mode=0o700)

    archive_field_allowlist = {
        "status",
        "exit_code",
        "beb_id",
        "beo_id",
        "l2_id",
        "work_dir",
        "target_branch",
        "target_hash",
        "pre_engine_hash",
        "commit_hash",
        "drop_manifest_path",
        "drop_manifest_sha256",
        "payload_sha256",
        "final_message_artifact_path",
        "final_message_sha256",
        "final_message_bytes",
        "codex_final_message_authoritative",
        "engine_logs_sha256",
        "engine_logs_bytes",
        "validation_logs_sha256",
        "validation_logs_bytes",
        "validation_log_count",
        "stderr_sha256",
        "raw_logs_embedded",
        "reusable_codex_dispatch_authorized",
        "broad_blk_pipe_dispatch_authorized",
        "beo_publication_authorized",
        "rtm_generation_authorized",
        "source_cleanup_authorized",
        "worktree_creation_authorized",
        "route_summary_artifact_path",
        "route_summary_artifact_sha256",
    }
    raw_route_log_keys = {
        "engine_logs",
        "validation_logs",
        "stdout",
        "stderr",
        "raw_report",
        "raw_result",
        "raw_logs",
        "engine_output",
        "validation_output",
        "raw_output",
        "full_log",
        "full_logs",
    }
    raw_route_log_markers = (
        "raw engine log",
        "raw engine logs",
        "raw validation log",
        "raw validation logs",
        "read-only .git/index.lock",
    )
    denied_archive_authority_fields = {
        "dispatch_authorized",
        "beo_publication_authorized",
        "rtm_generation_authorized",
        "reusable_codex_dispatch_authorized",
        "broad_blk_pipe_dispatch_authorized",
        "source_cleanup_authorized",
        "worktree_creation_authorized",
        "codex_final_message_authoritative",
    }
    optional_archive_sha_fields = {
        "payload_sha256",
        "final_message_sha256",
        "engine_logs_sha256",
        "validation_logs_sha256",
        "stderr_sha256",
        "route_summary_artifact_sha256",
    }
    archive_integer_fields = {
        "exit_code",
        "final_message_bytes",
        "engine_logs_bytes",
        "validation_logs_bytes",
        "validation_log_count",
    }
    archive_authority_markers = (
        "approved",
        "approval",
        "authorized",
        "authorised",
        "greenlit",
        "permitted",
        "publication",
        "beo_publication",
        "rtm",
        "rtm_generation",
        "blk_link",
        "blk-link",
        "production_blk_link",
        "production blk-link",
        "next_k2_selection",
        "k2-024",
        "approval granted",
    )
    archive_pathish_fields = {
        "work_dir",
        "drop_manifest_path",
        "final_message_artifact_path",
        "route_summary_artifact_path",
    }

    def contains_raw_route_log(value: Any) -> bool:
        if isinstance(value, str):
            lowered = value.casefold()
            return any(marker in lowered for marker in raw_route_log_markers)
        if isinstance(value, dict):
            for key, nested in value.items():
                key_text = str(key).casefold()
                if key_text in raw_route_log_keys:
                    return True
                if contains_raw_route_log(nested):
                    return True
        elif isinstance(value, (list, tuple, set)):
            return any(contains_raw_route_log(item) for item in value)
        return False

    def contains_archive_authority_laundering(value: str) -> bool:
        lowered = value.casefold()
        return any(marker in lowered for marker in archive_authority_markers)

    def validate_archive_scalar(field_name: str, value: Any) -> Any:
        if isinstance(value, (dict, list, tuple, set)):
            raise RouteError(f"route_summary.{field_name} must be scalar sanitized evidence")
        if field_name == "raw_logs_embedded":
            if value is not False:
                raise RouteError("route_summary.raw_logs_embedded must be false")
            return False
        if field_name in archive_integer_fields:
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise RouteError(f"route_summary.{field_name} must be a non-negative integer")
            return value
        if isinstance(value, bool) or not isinstance(value, str):
            raise RouteError(f"route_summary.{field_name} must be a string")
        if "\n" in value or "\r" in value:
            raise RouteError(f"route_summary.{field_name} must be single-line sanitized evidence")
        if contains_raw_route_log(value) or contains_archive_authority_laundering(value):
            raise RouteError(f"route_summary.{field_name} contains forbidden raw or authority-laundering evidence")
        if field_name == "status" and not re.fullmatch(r"[A-Z0-9_ -]{0,64}", value):
            raise RouteError("route_summary.status must be a compact uppercase status token")
        if field_name in archive_pathish_fields and not re.fullmatch(r"[A-Za-z0-9_./:+=@%~-]{0,4096}", value):
            raise RouteError(f"route_summary.{field_name} must be a compact path token")
        if field_name == "target_branch" and not re.fullmatch(r"[A-Za-z0-9_./:+=@%~-]{0,512}", value):
            raise RouteError("route_summary.target_branch must be a compact branch token")
        return value

    records: list[dict[str, Any]] = []
    for index, summary in enumerate(route_summaries, start=1):
        if not isinstance(summary, dict):
            raise RouteError("route_summaries entries must be objects")
        if summary.get("raw_logs_embedded") is not False or contains_raw_route_log(summary):
            raise RouteError("route evidence cannot archive raw route logs; use hashes/byte counts plus final-message artifacts only")
        beb_id = _required_pattern(summary.get("beb_id"), "route_summary.beb_id", _BEB_ID_RE)
        l2_id = _required_pattern(summary.get("l2_id"), "route_summary.l2_id", _L2_ID_RE)
        beo_id = str(summary.get("beo_id") or "")
        if beo_id:
            _required_pattern(beo_id, "route_summary.beo_id", _BEO_ID_RE)
        _required_pattern(summary.get("target_hash"), "route_summary.target_hash", _GIT_HASH_RE)
        commit_hash = str(summary.get("commit_hash") or "")
        if commit_hash:
            _required_pattern(commit_hash, "route_summary.commit_hash", _GIT_HASH_RE)
        _required_sha256(summary.get("drop_manifest_sha256"), "route_summary.drop_manifest_sha256")
        for sha_field in sorted(optional_archive_sha_fields):
            sha_value = summary.get(sha_field)
            if sha_value not in (None, ""):
                _required_sha256(sha_value, f"route_summary.{sha_field}")

        summary_out = evidence_dir / f"route-summary-{index:03d}.json"
        if summary_out.is_symlink():
            raise RouteError("route summary archive destination must not be a symlink")
        sanitized_summary = {
            key: validate_archive_scalar(key, summary[key])
            for key in sorted(archive_field_allowlist)
            if key in summary and key not in denied_archive_authority_fields
        }
        for denied_field in denied_archive_authority_fields:
            sanitized_summary[denied_field] = False
        summary_out.write_bytes(_canonical_json_bytes(sanitized_summary))

        final_message_out_text = ""
        final_message_sha = ""
        final_message_source = str(summary.get("final_message_artifact_path") or "")
        if final_message_source:
            final_message_path = _require_non_protected_artifact_path(
                Path(final_message_source).expanduser(),
                "final_message_artifact_path",
            )
            if final_message_path.is_symlink() or not final_message_path.is_file():
                raise RouteError("Codex final-message artifact must be a regular file before archival")
            final_message_path = _require_non_protected_artifact_path(
                final_message_path.resolve(),
                "final_message_artifact_path",
            )
            expected_final_sha = str(summary.get("final_message_sha256") or "")
            if not expected_final_sha:
                raise RouteError("route_summary.final_message_sha256 is required when final_message_artifact_path is archived")
            _required_sha256(expected_final_sha, "route_summary.final_message_sha256")
            _assert_file_sha256(final_message_path, expected_final_sha, "final_message_artifact_path")
            final_message_bytes = final_message_path.read_bytes()
            final_message_text = final_message_bytes.decode("utf-8", errors="replace")
            if contains_raw_route_log(final_message_text) or contains_archive_authority_laundering(final_message_text):
                raise RouteError(
                    "Codex final-message artifact contains forbidden raw or authority-laundering evidence"
                )
            final_message_out = evidence_dir / f"codex-final-message-{index:03d}.md"
            if final_message_out.is_symlink():
                raise RouteError("Codex final-message archive destination must not be a symlink")
            final_message_out.write_bytes(final_message_bytes)
            final_message_out_text = str(final_message_out.resolve())
            final_message_sha = _file_sha256(final_message_out)

        records.append({
            "sequence": index,
            "beb_id": beb_id,
            "beo_id": beo_id,
            "l2_id": l2_id,
            "target_hash": str(summary.get("target_hash")),
            "commit_hash": commit_hash,
            "drop_manifest_sha256": str(summary.get("drop_manifest_sha256")),
            "route_summary_path": str(summary_out.resolve()),
            "route_summary_sha256": _file_sha256(summary_out),
            "codex_final_message_path": final_message_out_text,
            "codex_final_message_sha256": final_message_sha,
            "codex_final_message_authoritative": False,
            "raw_logs_embedded": False,
        })

    index_body = {
        "status": "K2_ROUTE_EVIDENCE_ARCHIVE_READY",
        "route_evidence": records,
        "dispatch_authorized": False,
        "beo_publication_authorized": False,
        "rtm_generation_authorized": False,
        "reusable_codex_dispatch_authorized": False,
    }
    index_path = evidence_dir / "evidence-index.json"
    if index_path.is_symlink():
        raise RouteError("route evidence index destination must not be a symlink")
    index_path.write_bytes(_canonical_json_bytes(index_body))
    return {
        "status": "K2_ROUTE_EVIDENCE_ARCHIVE_READY",
        "package_dir": str(package_path),
        "evidence_dir": str(evidence_dir.resolve()),
        "evidence_index_path": str(index_path.resolve()),
        "evidence_index_sha256": _file_sha256(index_path),
        "evidence_count": len(records),
        "dispatch_authorized": False,
        "beo_publication_authorized": False,
        "rtm_generation_authorized": False,
        "reusable_codex_dispatch_authorized": False,
    }


_REQUIRED_FALLBACK_DENIED_AUTHORITIES = frozenset({
    "BEO_PUBLICATION",
    "BROAD_BLK_PIPE_DISPATCH",
    "NEXT_K2_SELECTION",
    "REUSABLE_CODEX_DISPATCH",
    "RTM_GENERATION",
    "SOURCE_CLEANUP",
    "WORKTREE_CREATION",
})
_REQUIRED_FALLBACK_EVIDENCE = frozenset({
    "final_message",
    "focused_red_green",
    "full_verification",
    "patch_sha256",
    "prompt",
})
_ALLOWED_FALLBACK_REASONS = frozenset({
    "ENGINE_TIMEOUT",
    "MODEL_DEGRADATION",
    "ROUTE_BUG",
    "GIT_DIRTY",
    "OTHER",
})


def evaluate_route_closeout_gate(
    *,
    route_summaries: list[dict[str, Any]],
    fallback_authorization: dict[str, Any] | None = None,
    fallback_remediation_rounds: int = 0,
) -> dict[str, Any]:
    """Decide whether K2 closeout has governed route evidence or an explicit fallback exception.

    A normal K2 closeout needs a successful BLK-pipe route commit. External Codex
    fallback is accepted only as an explicit one-off exception package and never as
    normal governed-route evidence.
    """
    blockers: list[dict[str, Any]] = []
    if not isinstance(route_summaries, list) or not route_summaries:
        return {
            "status": "ROUTE_CLOSEOUT_GATE_BLOCKED",
            "normal_closeout_allowed": False,
            "fallback_exception_allowed": False,
            "external_codex_fallback_authorized": False,
            "successful_route_count": 0,
            "non_executed_route_count": 0,
            "required_action": "repair_or_reroute_through_blk_pipe",
            "blockers": [{
                "code": "MISSING_ROUTE_SUMMARIES",
                "message": "route closeout requires at least one BLK-pipe route summary",
            }],
        }
    if isinstance(fallback_remediation_rounds, bool) or not isinstance(fallback_remediation_rounds, int) or fallback_remediation_rounds < 0:
        blockers.append({
            "code": "INVALID_FALLBACK_REMEDIATION_ROUNDS",
            "message": "fallback_remediation_rounds must be a non-negative integer",
        })
        fallback_remediation_rounds = 0

    successful_routes: list[dict[str, Any]] = []
    non_executed_routes: list[dict[str, Any]] = []
    failure_statuses: set[str] = set()
    target_hashes: set[str] = set()
    for index, summary in enumerate(route_summaries, start=1):
        if not isinstance(summary, dict):
            blockers.append({
                "code": "INVALID_ROUTE_SUMMARY",
                "message": "route summary must be an object",
                "sequence": index,
            })
            continue
        status = str(summary.get("status") or "")
        commit_hash = str(summary.get("commit_hash") or "")
        target_hash = str(summary.get("target_hash") or "")
        if target_hash:
            try:
                _required_pattern(target_hash, f"route_summaries[{index}].target_hash", _GIT_HASH_RE)
                target_hashes.add(target_hash)
            except RouteError as exc:
                blockers.append({"code": "INVALID_ROUTE_TARGET_HASH", "message": str(exc), "sequence": index})
        else:
            blockers.append({
                "code": "INVALID_ROUTE_TARGET_HASH",
                "message": f"route_summaries[{index}].target_hash must be a full 40-character Git hash",
                "sequence": index,
            })
        try:
            _required_pattern(str(summary.get("beb_id") or ""), f"route_summaries[{index}].beb_id", _BEB_ID_RE)
            _required_pattern(str(summary.get("l2_id") or ""), f"route_summaries[{index}].l2_id", _L2_ID_RE)
            beo_id = str(summary.get("beo_id") or "")
            if beo_id:
                _required_pattern(beo_id, f"route_summaries[{index}].beo_id", _BEO_ID_RE)
            _required_sha256(summary.get("drop_manifest_sha256"), f"route_summaries[{index}].drop_manifest_sha256")
        except RouteError as exc:
            blockers.append({"code": "INVALID_ROUTE_SUMMARY_IDENTITY", "message": str(exc), "sequence": index})
        exit_code = summary.get("exit_code")
        engine_bytes = summary.get("engine_logs_bytes", 0)
        final_bytes = summary.get("final_message_bytes", 0)
        validation_count = summary.get("validation_log_count", 0)
        has_success_shape = (
            status == "SUCCESS"
            and isinstance(exit_code, int)
            and not isinstance(exit_code, bool)
            and exit_code == 0
            and bool(_GIT_HASH_RE.fullmatch(commit_hash))
            and isinstance(engine_bytes, int)
            and not isinstance(engine_bytes, bool)
            and engine_bytes > 0
            and isinstance(final_bytes, int)
            and not isinstance(final_bytes, bool)
            and final_bytes > 0
            and isinstance(validation_count, int)
            and not isinstance(validation_count, bool)
            and validation_count > 0
        )
        if has_success_shape:
            successful_routes.append(summary)
            continue
        failure_statuses.add(status)
        non_executed_routes.append(summary)

    if blockers:
        return {
            "status": "ROUTE_CLOSEOUT_GATE_BLOCKED",
            "normal_closeout_allowed": False,
            "fallback_exception_allowed": False,
            "external_codex_fallback_authorized": False,
            "successful_route_count": len(successful_routes),
            "non_executed_route_count": len(non_executed_routes),
            "required_action": "repair_or_reroute_through_blk_pipe",
            "blockers": blockers,
        }

    if successful_routes:
        return {
            "status": "ROUTE_CLOSEOUT_GATE_PASS",
            "normal_closeout_allowed": True,
            "fallback_exception_allowed": False,
            "external_codex_fallback_authorized": False,
            "successful_route_count": len(successful_routes),
            "non_executed_route_count": len(non_executed_routes),
            "required_action": "normal_closeout_allowed",
            "blockers": [],
        }

    blockers.append({
        "code": "NO_SUCCESSFUL_BLK_PIPE_ROUTE_COMMIT",
        "message": "normal K2 closeout requires at least one successful BLK-pipe route summary with a route commit",
    })
    if non_executed_routes:
        blockers.append({
            "code": "NON_EXECUTED_ROUTE_EVIDENCE",
            "message": "available route summaries are pre-dispatch, failed, or missing route-commit evidence",
            "statuses": sorted(status for status in failure_statuses if status),
        })

    fallback_errors: list[str] = []
    if fallback_authorization is not None:
        fallback_errors = _validate_one_off_fallback_authorization(
            fallback_authorization,
            failure_statuses=failure_statuses,
            target_hashes=target_hashes,
            fallback_remediation_rounds=fallback_remediation_rounds,
        )
        if not fallback_errors:
            return {
                "status": "ROUTE_CLOSEOUT_GATE_FALLBACK_EXCEPTION",
                "normal_closeout_allowed": False,
                "fallback_exception_allowed": True,
                "external_codex_fallback_authorized": True,
                "successful_route_count": 0,
                "non_executed_route_count": len(non_executed_routes),
                "required_action": "fallback_exception_closeout_only",
                "blockers": [],
            }
        blockers.append({
            "code": "FALLBACK_AUTHORIZATION_INVALID",
            "message": "fallback authorization must be exact, one-off, bounded, and evidence-bound",
            "errors": fallback_errors,
        })
        if any(error.startswith("fallback_remediation_rounds exceeds") for error in fallback_errors):
            blockers.append({
                "code": "FALLBACK_REMEDIATION_CEILING_EXCEEDED",
                "message": "fallback remediation rounds exceed the authorized ceiling",
            })

    return {
        "status": "ROUTE_CLOSEOUT_GATE_BLOCKED",
        "normal_closeout_allowed": False,
        "fallback_exception_allowed": False,
        "external_codex_fallback_authorized": False,
        "successful_route_count": 0,
        "non_executed_route_count": len(non_executed_routes),
        "required_action": "repair_or_reroute_through_blk_pipe",
        "blockers": blockers,
    }


def _validate_one_off_fallback_authorization(
    authorization: dict[str, Any],
    *,
    failure_statuses: set[str],
    target_hashes: set[str],
    fallback_remediation_rounds: int,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(authorization, dict):
        return ["fallback_authorization must be an object"]
    if authorization.get("fallback_authorized") is not True:
        errors.append("fallback_authorized must be true")
    if authorization.get("authorization_scope") != "ONE_OFF_EXTERNAL_CODEX_FALLBACK":
        errors.append("authorization_scope must be ONE_OFF_EXTERNAL_CODEX_FALLBACK")
    if authorization.get("authorized_by") != "operator":
        errors.append("authorized_by must be operator")
    reason = str(authorization.get("reason") or "")
    if reason not in _ALLOWED_FALLBACK_REASONS:
        errors.append("reason must be an approved fallback reason")
    failure_status = str(authorization.get("route_failure_status") or "")
    if not failure_status or failure_status not in failure_statuses:
        errors.append("route_failure_status must match an observed failed route status")
    target_hash = str(authorization.get("target_hash") or "")
    if not _GIT_HASH_RE.fullmatch(target_hash):
        errors.append("target_hash must be a full 40-character Git hash")
    elif not target_hashes:
        errors.append("target_hash must match a validated failed route target_hash")
    elif target_hash not in target_hashes:
        errors.append("target_hash must match the failed route target_hash")
    allowed_files = authorization.get("allowed_files")
    if not isinstance(allowed_files, list) or not allowed_files:
        errors.append("allowed_files must be a non-empty list")
    else:
        for path in allowed_files:
            if not isinstance(path, str) or not path or path.startswith("/") or ".." in Path(path).parts:
                errors.append("allowed_files must contain only relative safe path strings")
                break
    denied = authorization.get("denied_authorities")
    if (
        not isinstance(denied, list)
        or not all(isinstance(item, str) for item in denied)
        or len(set(denied)) != len(denied)
        or frozenset(denied) != _REQUIRED_FALLBACK_DENIED_AUTHORITIES
        or len(denied) != len(_REQUIRED_FALLBACK_DENIED_AUTHORITIES)
    ):
        errors.append("denied_authorities must exactly cover the required fallback denial set")
    evidence = authorization.get("evidence_required")
    if (
        not isinstance(evidence, list)
        or not all(isinstance(item, str) for item in evidence)
        or len(set(evidence)) != len(evidence)
        or frozenset(evidence) != _REQUIRED_FALLBACK_EVIDENCE
        or len(evidence) != len(_REQUIRED_FALLBACK_EVIDENCE)
    ):
        errors.append("evidence_required must exactly cover prompt/final_message/patch_sha256/focused_red_green/full_verification")
    ceiling = authorization.get("max_remediation_rounds")
    if isinstance(ceiling, bool) or not isinstance(ceiling, int) or ceiling < 0 or ceiling > 3:
        errors.append("max_remediation_rounds must be an integer from 0 to 3")
    elif fallback_remediation_rounds > ceiling:
        errors.append("fallback_remediation_rounds exceeds max_remediation_rounds")
    if authorization.get("external_codex_model") != "gpt-5.4":
        errors.append("external_codex_model must be gpt-5.4 for the one-off fallback policy")
    return errors


def scan_k2_final_closeout_artifacts(
    *,
    beo_path: str | Path,
    expected_beo_id: str,
    expected_closeout_metadata_commit: str,
    expected_final_beo_sha256: str | None = None,
    roadmap_paths: Iterable[str | Path] | None = None,
    obsidian_execution_root: str | Path | None = None,
    route_summaries: list[dict[str, Any]] | None = None,
    fallback_authorization: dict[str, Any] | None = None,
    fallback_remediation_rounds: int = 0,
) -> dict[str, Any]:
    """Check final K2 BEO/roadmap/mirror closeout consistency before reconciliation."""
    safe_beo_id = _required_pattern(expected_beo_id, "expected_beo_id", _BEO_ID_RE)
    safe_commit = _required_pattern(expected_closeout_metadata_commit, "expected_closeout_metadata_commit", _GIT_HASH_RE)
    blockers: list[dict[str, Any]] = []
    roadmap_path_list = list(roadmap_paths or [])
    if not roadmap_path_list:
        blockers.append({
            "code": "MISSING_ROADMAP_PATHS",
            "message": "final K2 closeout scan requires at least one canonical or mirror roadmap path",
            "paths": [],
        })
    if obsidian_execution_root is None:
        blockers.append({
            "code": "MISSING_OBSIDIAN_EXECUTION_ROOT",
            "message": "final K2 closeout scan requires the Obsidian execution mirror root so visible BEO count and metadata can be checked",
            "paths": [],
        })
    if expected_final_beo_sha256:
        expected_sha = _required_sha256(expected_final_beo_sha256, "expected_final_beo_sha256")
    else:
        expected_sha = ""
        blockers.append({
            "code": "EXPECTED_FINAL_BEO_SHA_REQUIRED",
            "message": "final K2 closeout scan requires the expected final BEO SHA before hash reconciliation is allowed",
            "paths": [str(beo_path)],
        })
    beo = Path(beo_path).expanduser()
    final_beo_sha = ""
    if beo.is_symlink() or not beo.is_file():
        blockers.append({"code": "FINAL_BEO_FILE_UNAVAILABLE", "message": "final BEO path must be a regular file", "paths": [str(beo)]})
        beo_text = ""
    else:
        beo_text = beo.read_text()
        final_beo_sha = _file_sha256(beo)
        placeholder_scan = scan_final_beo_closeout_placeholders(beo_text, beo_id=safe_beo_id)
        blockers.extend(placeholder_scan["blockers"])
        commit_match = re.search(r'closeout_metadata_commit:\s*"?([^"\n]+)"?', beo_text)
        if commit_match is None or commit_match.group(1).strip() != safe_commit:
            blockers.append({
                "code": "CLOSEOUT_METADATA_COMMIT_MISMATCH",
                "message": "final BEO must bind the expected closeout metadata commit",
                "paths": [str(beo)],
            })
        if expected_sha and final_beo_sha != expected_sha:
            blockers.append({
                "code": "FINAL_BEO_SHA_MISMATCH",
                "message": "final BEO SHA does not match the expected reconciliation hash",
                "paths": [str(beo)],
                "actual": final_beo_sha,
                "expected": expected_sha,
            })

    for raw_path in roadmap_path_list:
        path = Path(raw_path).expanduser()
        if path.is_symlink() or not path.is_file():
            blockers.append({"code": "ROADMAP_FILE_UNAVAILABLE", "message": "roadmap path must be a regular file", "paths": [str(path)]})
            continue
        text = path.read_text()
        sequence_lines = [
            line
            for line in text.splitlines()
            if re.match(r"^\s*first_unconsumed_sequence\s*:", line, re.IGNORECASE)
        ]
        if not sequence_lines:
            blockers.append({
                "code": "MISSING_FIRST_UNCONSUMED_SEQUENCE_NULL",
                "message": "closed K2 roadmap must explicitly bind first_unconsumed_sequence: null",
                "paths": [str(path)],
            })
        elif len(sequence_lines) != 1 or sequence_lines[0] != "first_unconsumed_sequence: null":
            blockers.append({
                "code": "NEXT_K2_SEQUENCE_STILL_SELECTED",
                "message": "closed K2 roadmap must leave first_unconsumed_sequence null until a new operator selection exists",
                "paths": [str(path)],
            })
        lowered = text.casefold()
        if "pending dispatch" in lowered or "pending-k2" in lowered:
            blockers.append({
                "code": "STALE_ROADMAP_PENDING_WORDING",
                "message": "closed K2 roadmap or mirror still contains pending dispatch wording",
                "paths": [str(path)],
            })

    visible_beo_count = 0
    if obsidian_execution_root is not None:
        mirror_root = Path(obsidian_execution_root).expanduser()
        if mirror_root.is_symlink() or not mirror_root.exists():
            blockers.append({"code": "OBSIDIAN_EXECUTION_ROOT_UNAVAILABLE", "message": "Obsidian execution mirror root must exist and not be a symlink", "paths": [str(mirror_root)]})
        else:
            visible_beos = sorted((mirror_root / "BEOs").glob(f"{safe_beo_id}*.md")) if (mirror_root / "BEOs").exists() else []
            visible_beo_count = len(visible_beos)
            if visible_beo_count != 1:
                blockers.append({
                    "code": "VISIBLE_BEO_MIRROR_COUNT",
                    "message": "K2 closeout must have exactly one visible Obsidian BEO mirror; remediation templates belong under BDOC support folders",
                    "paths": [str(path) for path in visible_beos],
                })
            for mirror in visible_beos:
                text = mirror.read_text() if mirror.is_file() and not mirror.is_symlink() else ""
                if not text.startswith("> VIEW COPY — DO NOT EDIT\n") or "Canonical sha256:" not in text or "Canonical commit:" not in text:
                    blockers.append({
                        "code": "OBSIDIAN_BEO_MIRROR_METADATA_INCOMPLETE",
                        "message": "visible BEO mirror must be marked non-authoritative and bind canonical SHA/commit metadata",
                        "paths": [str(mirror)],
                    })
                sha_match = re.search(r"^Canonical sha256:\s*(sha256:[0-9a-f]{64})\s*$", text, re.MULTILINE)
                mirror_sha = sha_match.group(1) if sha_match else ""
                if not expected_sha or mirror_sha != expected_sha:
                    blockers.append({
                        "code": "OBSIDIAN_BEO_MIRROR_SHA_MISMATCH",
                        "message": "visible BEO mirror must carry the final canonical BEO SHA",
                        "paths": [str(mirror)],
                    })
                commit_match = re.search(r"^Canonical commit:\s*([0-9a-f]{40})\s*$", text, re.MULTILINE)
                if commit_match is None:
                    blockers.append({
                        "code": "OBSIDIAN_BEO_MIRROR_COMMIT_MISMATCH",
                        "message": "visible BEO mirror must carry a full 40-character canonical commit hash",
                        "paths": [str(mirror)],
                    })

    if route_summaries is None:
        route_closeout_gate = {
            "status": "ROUTE_CLOSEOUT_GATE_BLOCKED",
            "normal_closeout_allowed": False,
            "fallback_exception_allowed": False,
            "external_codex_fallback_authorized": False,
            "successful_route_count": 0,
            "non_executed_route_count": 0,
            "required_action": "repair_or_reroute_through_blk_pipe",
            "blockers": [{
                "code": "MISSING_ROUTE_CLOSEOUT_GATE_EVIDENCE",
                "message": "final K2 closeout scan requires route summaries or an explicit fallback exception gate",
            }],
        }
        blockers.append({
            "code": "MISSING_ROUTE_CLOSEOUT_GATE_EVIDENCE",
            "message": "final K2 closeout scan requires route summaries or an explicit fallback exception gate",
            "paths": [str(beo_path)],
        })
    else:
        expected_route_beb_id, expected_route_l2_id = _derive_matching_beb_l2_ids_from_beo(safe_beo_id)
        for index, summary in enumerate(route_summaries, start=1):
            if not isinstance(summary, dict):
                continue
            if (
                summary.get("beo_id") != safe_beo_id
                or summary.get("beb_id") != expected_route_beb_id
                or summary.get("l2_id") != expected_route_l2_id
            ):
                blockers.append({
                    "code": "ROUTE_SUMMARY_IDENTITY_MISMATCH",
                    "message": "route summaries must match the exact BEO/BEB/L2 family and sequence being closed",
                    "paths": [str(beo_path)],
                    "sequence": index,
                    "expected_beo_id": safe_beo_id,
                    "expected_beb_id": expected_route_beb_id,
                    "expected_l2_id": expected_route_l2_id,
                })
        route_closeout_gate = evaluate_route_closeout_gate(
            route_summaries=route_summaries,
            fallback_authorization=fallback_authorization,
            fallback_remediation_rounds=fallback_remediation_rounds,
        )
        if route_closeout_gate["status"] == "ROUTE_CLOSEOUT_GATE_BLOCKED":
            blockers.append({
                "code": "ROUTE_CLOSEOUT_GATE_BLOCKED",
                "message": "final K2 closeout cannot proceed without successful BLK-pipe route commit or explicit one-off fallback authorization",
                "paths": [str(beo_path)],
                "gate_blocker_codes": [item["code"] for item in route_closeout_gate["blockers"]],
            })

    return {
        "status": "K2_FINAL_CLOSEOUT_SCAN_BLOCKED" if blockers else "K2_FINAL_CLOSEOUT_SCAN_PASS",
        "hash_reconciliation_allowed": not blockers,
        "beo_id": safe_beo_id,
        "final_beo_sha256": final_beo_sha,
        "expected_closeout_metadata_commit": safe_commit,
        "visible_beo_mirror_count": visible_beo_count,
        "route_closeout_gate": route_closeout_gate,
        "blockers": blockers,
        "beo_publication_authorized": False,
        "rtm_generation_authorized": False,
        "next_k2_selection_authorized": False,
    }


def scan_repo_local_hygiene(repo_root: str | Path) -> dict[str, Any]:
    """Report repo-local cache artifacts that must not be staged in BLK-System closeouts."""
    root = Path(repo_root).expanduser().resolve()
    forbidden: set[str] = set()
    if root.exists():
        for path in root.rglob("*"):
            rel = path.relative_to(root).as_posix()
            if path.name == "__pycache__":
                forbidden.add(rel)
            if path.suffix == ".pyc" or "__pycache__" in path.parts:
                forbidden.add(rel)
    blockers = []
    if forbidden:
        blockers.append({
            "code": "REPO_LOCAL_PYCACHE",
            "message": "repo-local __pycache__/.pyc artifacts must be removed before exact-path staging",
            "paths": sorted(forbidden),
        })
    return {
        "status": "REPO_LOCAL_HYGIENE_BLOCKED" if blockers else "REPO_LOCAL_HYGIENE_PASS",
        "repo_root": str(root),
        "forbidden_paths": sorted(forbidden),
        "blockers": blockers,
        "mutation_performed": False,
        "staging_authorized": False,
        "dispatch_authorized": False,
    }


def build_route_commit_message(beb_id: str) -> str:
    safe_beb_id = _required_pattern(beb_id, "beb_id", _BEB_ID_RE)
    message = f"blk-pipe: {safe_beb_id}"
    if any(ch in message for ch in "\r\n") or len(message.encode("utf-8")) > 120:
        raise RouteError("commit message must be one bounded single line")
    return message


def build_hostile_review_record(
    *,
    beb_id: str,
    parent_hash: str,
    feature_hash: str,
    verdict: str,
    blockers: list[str],
    allowed_files: list[str],
    retry_count: int,
    remediation_parent_hash: str | None = None,
    remediation_feature_hash: str | None = None,
) -> dict[str, Any]:
    safe_beb_id = _required_pattern(beb_id, "beb_id", _BEB_ID_RE)
    safe_parent = _required_pattern(parent_hash, "parent_hash", _GIT_HASH_RE)
    safe_feature = _required_pattern(feature_hash, "feature_hash", _GIT_HASH_RE)
    safe_allowed_files = _required_path_list(allowed_files, "allowed_files")
    if not isinstance(retry_count, int) or retry_count < 0 or retry_count > 3:
        raise RouteError("retry_count must be an integer in the bounded 0..3 retry ceiling")
    safe_verdict = _required_string(verdict, "verdict").upper()
    if safe_verdict not in {"PASS", "BLOCKED"}:
        raise RouteError("verdict must be PASS or BLOCKED")
    safe_blockers = _required_string_list(blockers, "blockers") if blockers else []
    if safe_verdict == "PASS" and safe_blockers:
        raise RouteError("PASS hostile review records must not include blockers")
    if safe_verdict == "BLOCKED" and not safe_blockers:
        raise RouteError("BLOCKED hostile review records must include blockers")
    remediation_parent = ""
    remediation_feature = ""
    if safe_verdict == "PASS" and (remediation_parent_hash is None or remediation_feature_hash is None):
        raise RouteError("PASS hostile review records require remediation parent/feature hash binding")
    if remediation_parent_hash is not None or remediation_feature_hash is not None:
        remediation_parent = _required_pattern(remediation_parent_hash, "remediation_parent_hash", _GIT_HASH_RE)
        remediation_feature = _required_pattern(remediation_feature_hash, "remediation_feature_hash", _GIT_HASH_RE)
        if remediation_parent != safe_feature:
            raise RouteError("remediation_parent_hash must equal the reviewed feature_hash")
    state = "HOSTILE_REVIEW_PASS" if safe_verdict == "PASS" else "HOSTILE_REVIEW_BLOCKED"
    return {
        "status": "HOSTILE_REVIEW_RECORDED",
        "beb_id": safe_beb_id,
        "parent_hash": safe_parent,
        "feature_hash": safe_feature,
        "verdict": safe_verdict,
        "state": state,
        "next_required_state": "CLOSEOUT_READY" if safe_verdict == "PASS" else "REMEDIATION_PACKET_REQUIRED",
        "blockers": safe_blockers,
        "allowed_files": safe_allowed_files,
        "retry_count": retry_count,
        "remediation_parent_hash": remediation_parent,
        "remediation_feature_hash": remediation_feature,
        "closeout_ready": safe_verdict == "PASS",
        "remediation_auto_authorized": False,
        "beo_publication_authorized": False,
        "rtm_generation_authorized": False,
        "reusable_codex_dispatch_authorized": False,
    }


def _allowlist_companion_suggestions(
    repo: Path,
    allowed_modified_files: list[str],
    allowed_new_files: list[str],
    *,
    readiness_profiles: list[str] | None = None,
) -> list[dict[str, Any]]:
    authorized = set(allowed_modified_files) | set(allowed_new_files)
    suggestions: list[dict[str, Any]] = []
    suffixes = [".test.ts", ".spec.ts", ".test.tsx", ".spec.tsx"]
    for rel in allowed_modified_files:
        if rel in authorized and any(rel.endswith(suffix) for suffix in suffixes):
            continue
        path = Path(rel)
        stem = path.name
        for source_ext in (".tsx", ".ts", ".jsx", ".js"):
            if stem.endswith(source_ext):
                base = stem[: -len(source_ext)]
                for suffix in suffixes:
                    candidate = path.with_name(base + suffix).as_posix()
                    if candidate in authorized:
                        continue
                    if (repo / candidate).is_file():
                        suggestions.append({
                            "kind": "existing_companion_test_not_authorized",
                            "source_file": rel,
                            "suggested_file": candidate,
                            "message": "Existing companion test file is not in allowed_modified_files/allowed_new_files; add explicitly if intended.",
                            "auto_authorized": False,
                        })
                break
    requested_profiles = set(readiness_profiles or [])
    caller_object_candidates = [
        rel for rel in (*allowed_modified_files, *allowed_new_files)
        if rel == "src/shared/view-intent-parameters.mjs" or rel == "tests/view-intent-parameters.test.mjs"
    ]
    if caller_object_candidates and _CALLER_OBJECT_CONTROL_PLANE_PROFILE not in requested_profiles:
        suggestions.append({
            "kind": "readiness_profile_recommended",
            "profile": _CALLER_OBJECT_CONTROL_PLANE_PROFILE,
            "source_file": "src/shared/view-intent-parameters.mjs"
            if "src/shared/view-intent-parameters.mjs" in caller_object_candidates
            else caller_object_candidates[0],
            "message": "Caller-object control-plane packages should include the Kuronode adversarial readiness profile; add explicitly if intended.",
            "auto_authorized": False,
        })
    renderer_public_surface_candidates = [
        rel for rel in (*allowed_modified_files, *allowed_new_files)
        if _looks_like_renderer_public_surface_candidate(rel)
    ]
    if renderer_public_surface_candidates and _RENDERER_PUBLIC_SURFACE_PROFILE not in requested_profiles:
        preferred = "src/renderer/App.tsx" if "src/renderer/App.tsx" in renderer_public_surface_candidates else renderer_public_surface_candidates[0]
        suggestions.append({
            "kind": "readiness_profile_recommended",
            "profile": _RENDERER_PUBLIC_SURFACE_PROFILE,
            "source_file": preferred,
            "message": "Renderer-visible/public-surface packages should include the conditional K2 renderer public-surface readiness profile; add explicitly if intended, but do not make it mandatory for unrelated slices.",
            "auto_authorized": False,
        })
    agent_a_promotion_candidates = [
        rel for rel in (*allowed_modified_files, *allowed_new_files)
        if rel == "src/shared/agent-a-promotion-request.mjs" or rel == "tests/agent-a-promotion-request.test.mjs"
    ]
    if agent_a_promotion_candidates and _AGENT_A_PROMOTION_REQUEST_PROFILE not in requested_profiles:
        preferred = "src/shared/agent-a-promotion-request.mjs" if "src/shared/agent-a-promotion-request.mjs" in agent_a_promotion_candidates else agent_a_promotion_candidates[0]
        suggestions.append({
            "kind": "readiness_profile_recommended",
            "profile": _AGENT_A_PROMOTION_REQUEST_PROFILE,
            "source_file": preferred,
            "message": "Agent A promotion-request/preflight packages should include the K2 Agent A evidence-graph hostile-readiness profile; add explicitly if intended.",
            "auto_authorized": False,
        })
    return sorted(suggestions, key=lambda item: (item["source_file"], item.get("suggested_file", item.get("profile", ""))))


def _looks_like_renderer_public_surface_candidate(rel: str) -> bool:
    path = Path(rel)
    text = path.as_posix()
    if text.startswith("src/renderer/") and path.suffix in {".tsx", ".ts", ".jsx", ".js"}:
        return True
    if text.startswith("tests/renderer-") and text.endswith((".test.mjs", ".test.js", ".test.ts", ".test.tsx")):
        return True
    return False


def process_drop_file(
    drop_path: str | Path,
    *,
    adapter: Any | None = None,
    allowed_work_dirs: Iterable[str | Path] | None = None,
    trusted_roots: Iterable[str | Path] | None = None,
    approved_drop_sha256: str | None = None,
    progress_callback: Any | None = None,
    progress_interval_seconds: float = 30.0,
) -> Any:
    """Validate one exact BEB-L2 drop and invoke BLK-pipe through the adapter."""
    allowed_dirs = _required_resolved_roots(allowed_work_dirs, "allowed_work_dirs")
    roots = _required_resolved_roots(trusted_roots, "trusted_roots")
    approved_hash = _required_sha256(approved_drop_sha256, "approved_drop_sha256")
    drop_file = _require_under_roots(Path(drop_path), roots, "drop_path")
    drop = _load_drop_manifest(drop_file)
    _assert_file_sha256(drop_file, approved_hash, "drop_path")

    work_dir = _require_exact_resolved_path(drop["work_dir"], allowed_dirs, "work_dir")
    beb_path = _require_non_protected_artifact_path(
        _require_under_roots(Path(drop["beb_path"]), roots, "beb_path"),
        "beb_path",
    )
    l2_path = _require_non_protected_artifact_path(
        _require_under_roots(Path(drop["l2_path"]), roots, "l2_path"),
        "l2_path",
    )
    beo_text = ""
    if "beo_path" in drop:
        beo_path = _require_non_protected_artifact_path(
            _require_under_roots(Path(drop["beo_path"]), roots, "beo_path"),
            "beo_path",
        )
        _assert_distinct_artifact_paths(beb_path, l2_path, beo_path)
        beo_text = _read_verified_text_file(beo_path, drop["beo_sha256"], "beo_path")
    beb_text = _read_verified_text_file(beb_path, drop["beb_sha256"], "beb_path")
    l2_packet = _read_verified_text_file(l2_path, drop["l2_sha256"], "l2_path")
    beb_metadata = _parse_beb_frontmatter(beb_text)

    _assert_bound_ids(drop, beb_metadata, l2_packet, beo_text)
    trace_artifacts = _parse_trace_artifacts(beb_metadata)

    report = _preflight_validated_drop(drop, work_dir, trace_artifacts, beb_text=beb_text, l2_packet=l2_packet)
    if report["status"] != "READY":
        codes = ", ".join(blocker["code"] for blocker in report["blockers"])
        raise RouteError(f"drop preflight blocked before BLK-pipe dispatch: {codes}")
    runner = adapter if adapter is not None else BlkPipeAdapter()
    engine_args = build_kuronode_codex_engine_args(beb_id=drop["beb_id"], target_hash=drop["target_hash"])
    result = runner.execute_sprint(
        beb_id=drop["beb_id"],
        work_dir=work_dir,
        target_branch=drop["target_branch"],
        engine="codex",
        engine_args=engine_args,
        l2_packet=l2_packet,
        validation_profiles=drop["validation_profiles"],
        allowed_modified_files=drop["allowed_modified_files"],
        allowed_new_files=drop["allowed_new_files"],
        trace_artifacts=trace_artifacts,
        target_hash=drop["target_hash"],
        commit_message=build_route_commit_message(drop["beb_id"]),
        progress_callback=progress_callback,
        progress_interval_seconds=progress_interval_seconds,
    )
    return _attach_route_summary(
        result,
        drop=drop,
        drop_path=drop_file,
        approved_drop_sha256=approved_hash,
        engine_args=engine_args,
    )


def preflight_drop_file(
    drop_path: str | Path,
    *,
    allowed_work_dirs: Iterable[str | Path] | None = None,
    trusted_roots: Iterable[str | Path] | None = None,
    approved_drop_sha256: str | None = None,
) -> dict[str, Any]:
    """Validate one exact BEB-L2 drop and inspect repo readiness without running Codex."""
    allowed_dirs = _required_resolved_roots(allowed_work_dirs, "allowed_work_dirs")
    roots = _required_resolved_roots(trusted_roots, "trusted_roots")
    approved_hash = _required_sha256(approved_drop_sha256, "approved_drop_sha256")
    drop_file = _require_under_roots(Path(drop_path), roots, "drop_path")
    drop = _load_drop_manifest(drop_file)
    _assert_file_sha256(drop_file, approved_hash, "drop_path")

    work_dir = _require_exact_resolved_path(drop["work_dir"], allowed_dirs, "work_dir")
    beb_path = _require_non_protected_artifact_path(
        _require_under_roots(Path(drop["beb_path"]), roots, "beb_path"),
        "beb_path",
    )
    l2_path = _require_non_protected_artifact_path(
        _require_under_roots(Path(drop["l2_path"]), roots, "l2_path"),
        "l2_path",
    )
    beo_text = ""
    if "beo_path" in drop:
        beo_path = _require_non_protected_artifact_path(
            _require_under_roots(Path(drop["beo_path"]), roots, "beo_path"),
            "beo_path",
        )
        _assert_distinct_artifact_paths(beb_path, l2_path, beo_path)
        beo_text = _read_verified_text_file(beo_path, drop["beo_sha256"], "beo_path")
    beb_text = _read_verified_text_file(beb_path, drop["beb_sha256"], "beb_path")
    l2_packet = _read_verified_text_file(l2_path, drop["l2_sha256"], "l2_path")
    beb_metadata = _parse_beb_frontmatter(beb_text)

    _assert_bound_ids(drop, beb_metadata, l2_packet, beo_text)
    trace_artifacts = _parse_trace_artifacts(beb_metadata)
    return _preflight_validated_drop(drop, work_dir, trace_artifacts, beb_text=beb_text, l2_packet=l2_packet)


def build_ignored_residue_cleanup_plan(
    drop_path: str | Path,
    *,
    allowed_work_dirs: Iterable[str | Path] | None = None,
    trusted_roots: Iterable[str | Path] | None = None,
    approved_drop_sha256: str | None = None,
) -> dict[str, Any]:
    """Return non-mutating cleanup evidence for ignored residue that blocks BEB-L2 dispatch."""
    report = preflight_drop_file(
        drop_path,
        allowed_work_dirs=allowed_work_dirs,
        trusted_roots=trusted_roots,
        approved_drop_sha256=approved_drop_sha256,
    )
    blockers = list(report["blockers"])
    ignored_blockers = [blocker for blocker in blockers if blocker["code"] == "PREEXISTING_IGNORED_OR_UNTRACKED"]
    non_cleanup_blockers = [blocker for blocker in blockers if blocker["code"] != "PREEXISTING_IGNORED_OR_UNTRACKED"]
    dry_run_command = ["git", "clean", "-ndX"]
    plan = {
        "status": "NO_CLEANUP_REQUIRED",
        "beb_id": report["beb_id"],
        "l2_id": report["l2_id"],
        "work_dir": report["work_dir"],
        "target_branch": report["target_branch"],
        "target_hash": report["target_hash"],
        "cleanup_authorized": False,
        "mutation_performed": False,
        "dispatch_authorized": False,
        "dry_run_command": dry_run_command,
        "ignored_residue_paths": sorted({path for blocker in ignored_blockers for path in blocker["paths"]}),
        "dry_run_paths": [],
        "blockers": blockers,
    }
    if "beo_id" in report:
        plan["beo_id"] = report["beo_id"]
    if non_cleanup_blockers:
        plan["status"] = "BLOCKED_BY_NON_CLEANUP_PREFLIGHT"
        plan["dry_run_command"] = []
        return plan
    if ignored_blockers:
        dry_run_paths = _git_clean_dry_run_paths(Path(report["work_dir"]))
        plan["status"] = "CLEANUP_REQUIRED"
        plan["dry_run_paths"] = dry_run_paths
    return plan


def build_clean_worktree_drop_manifest(
    drop_path: str | Path,
    *,
    clean_work_dir: str | Path,
    clean_worktree_roots: Iterable[str | Path] | None = None,
    allowed_work_dirs: Iterable[str | Path] | None = None,
    trusted_roots: Iterable[str | Path] | None = None,
    approved_drop_sha256: str | None = None,
    manifest_output_path: str | Path | None = None,
) -> dict[str, Any]:
    """Retarget one approved drop to a clean worktree candidate without creating or dispatching it."""
    allowed_dirs = _required_resolved_roots(allowed_work_dirs, "allowed_work_dirs")
    roots = _required_resolved_roots(trusted_roots, "trusted_roots")
    clean_roots = _required_resolved_roots(clean_worktree_roots, "clean_worktree_roots")
    approved_hash = _required_sha256(approved_drop_sha256, "approved_drop_sha256")
    drop_file = _require_under_roots(Path(drop_path), roots, "drop_path")
    drop = _load_drop_manifest(drop_file)
    _assert_file_sha256(drop_file, approved_hash, "drop_path")

    source_work_dir = Path(_require_exact_resolved_path(drop["work_dir"], allowed_dirs, "work_dir"))
    clean_dir = _require_under_roots(Path(clean_work_dir), clean_roots, "clean_work_dir")
    if clean_dir == source_work_dir or source_work_dir in clean_dir.parents:
        raise RouteError("clean_work_dir must not be the source work_dir or inside it")

    beb_path = _require_non_protected_artifact_path(
        _require_under_roots(Path(drop["beb_path"]), roots, "beb_path"),
        "beb_path",
    )
    l2_path = _require_non_protected_artifact_path(
        _require_under_roots(Path(drop["l2_path"]), roots, "l2_path"),
        "l2_path",
    )
    beo_text = ""
    if "beo_path" in drop:
        beo_path = _require_non_protected_artifact_path(
            _require_under_roots(Path(drop["beo_path"]), roots, "beo_path"),
            "beo_path",
        )
        _assert_distinct_artifact_paths(beb_path, l2_path, beo_path)
        beo_text = _read_verified_text_file(beo_path, drop["beo_sha256"], "beo_path")
    beb_text = _read_verified_text_file(beb_path, drop["beb_sha256"], "beb_path")
    l2_packet = _read_verified_text_file(l2_path, drop["l2_sha256"], "l2_path")
    beb_metadata = _parse_beb_frontmatter(beb_text)
    _assert_bound_ids(drop, beb_metadata, l2_packet, beo_text)
    _parse_trace_artifacts(beb_metadata)

    clean_manifest = dict(drop)
    clean_manifest["work_dir"] = str(clean_dir)
    canonical_manifest_bytes = _canonical_json_bytes(clean_manifest)
    manifest_path_text = ""
    if manifest_output_path is not None:
        manifest_path = _require_under_roots(Path(manifest_output_path), roots, "clean_worktree_manifest_output")
        if manifest_path.is_symlink():
            raise RouteError("clean_worktree_manifest_output must not be a symlink")
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_bytes(canonical_manifest_bytes)
        manifest_path_text = str(manifest_path)
    result = {
        "status": "CLEAN_WORKTREE_MANIFEST_READY",
        "beb_id": drop["beb_id"],
        "l2_id": drop["l2_id"],
        "source_work_dir": str(source_work_dir),
        "clean_work_dir": str(clean_dir),
        "target_branch": drop["target_branch"],
        "target_hash": drop["target_hash"],
        "drop_manifest": clean_manifest,
        "drop_manifest_sha256": "sha256:" + hashlib.sha256(canonical_manifest_bytes).hexdigest(),
        "drop_manifest_path": manifest_path_text,
        "manifest_approval_required": True,
        "worktree_creation_authorized": False,
        "source_mutation_authorized": False,
        "dispatch_authorized": False,
    }
    if "beo_id" in drop:
        result["beo_id"] = drop["beo_id"]
    return result


def dispatch_inbox_once(
    inbox_dir: str | Path,
    processed_dir: str | Path,
    failed_dir: str | Path,
    *,
    adapter: Any | None = None,
    allowed_work_dirs: Iterable[str | Path] | None = None,
    trusted_roots: Iterable[str | Path] | None = None,
    approved_drop_sha256s: Iterable[str] | None = None,
    progress_callback: Any | None = None,
) -> Any:
    """Process the first sorted `*.json` drop from an inbox directory."""
    roots = _required_resolved_roots(trusted_roots, "trusted_roots")
    approved_hashes = _required_approved_hashes(approved_drop_sha256s)
    inbox = _require_under_roots(Path(inbox_dir), roots, "inbox_dir")
    processed = _require_under_roots(Path(processed_dir), roots, "processed_dir")
    failed = _require_under_roots(Path(failed_dir), roots, "failed_dir")
    drops = sorted(inbox.glob("*.json"))
    if not drops:
        return {"status": "NOOP", "processed": 0}

    drop_path = drops[0]
    try:
        approved_hash = _file_sha256(drop_path)
        if approved_hash not in approved_hashes:
            raise RouteError("drop_path sha256 is not in trusted approved_drop_sha256s")
        report = process_drop_file(
            drop_path,
            adapter=adapter,
            allowed_work_dirs=allowed_work_dirs,
            trusted_roots=trusted_roots,
            approved_drop_sha256=approved_hash,
            progress_callback=progress_callback,
        )
    except Exception as exc:
        failed.mkdir(parents=True, exist_ok=True)
        destination = failed / drop_path.name
        if destination.exists():
            raise RouteError("failed_dir destination already exists; refusing overwrite") from exc
        shutil.move(str(drop_path), destination)
        error_path = failed / f"{drop_path.name}.error.txt"
        if error_path.exists():
            raise RouteError("failed_dir error destination already exists; refusing overwrite") from exc
        error_path.write_text(f"{type(exc).__name__}: {exc}\n")
        raise

    processed.mkdir(parents=True, exist_ok=True)
    destination = processed / drop_path.name
    if destination.exists():
        raise RouteError("processed_dir destination already exists; refusing overwrite")
    shutil.move(str(drop_path), destination)
    return report


def _preflight_validated_drop(
    drop: dict[str, Any],
    work_dir: str,
    trace_artifacts: list[dict[str, str]],
    *,
    beb_text: str,
    l2_packet: str,
) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    repo = Path(work_dir)
    head = _git_output(repo, ["rev-parse", "HEAD"])
    branch = _git_output(repo, ["rev-parse", "--abbrev-ref", "HEAD"])
    if head is None:
        blockers.append({"code": "GIT_HEAD_UNAVAILABLE", "message": "work_dir is not a readable Git repository", "paths": []})
    elif head != drop["target_hash"]:
        blockers.append({
            "code": "TARGET_HEAD_MISMATCH",
            "message": "current HEAD does not match target_hash",
            "paths": [],
            "actual": head,
            "expected": drop["target_hash"],
        })
    if branch is not None and branch != drop["target_branch"]:
        blockers.append({
            "code": "TARGET_BRANCH_MISMATCH",
            "message": "current branch does not match target_branch",
            "paths": [],
            "actual": branch,
            "expected": drop["target_branch"],
        })

    dirty_paths = _git_status_paths(repo, ["status", "--porcelain=v1", "--untracked-files=all"])
    if dirty_paths:
        blockers.append({
            "code": "GIT_DIRTY",
            "message": "tracked or untracked worktree changes exist before Codex dispatch",
            "paths": dirty_paths,
        })
    ignored_paths = _git_status_paths(repo, ["status", "--porcelain=v1", "--ignored=matching", "--untracked-files=all"], prefix="!!")
    if ignored_paths:
        blockers.append({
            "code": "PREEXISTING_IGNORED_OR_UNTRACKED",
            "message": "ignored residue exists and would make BLK-pipe cleanup destructive or noisy; retarget to a trusted sterile clean worktree before dispatch",
            "paths": ignored_paths,
            "recommended_action": "retarget_to_trusted_sterile_clean_worktree",
        })

    readiness_profiles = list(drop["readiness_profiles"])
    blockers.extend(_readiness_profile_blockers(readiness_profiles, beb_text=beb_text, l2_packet=l2_packet))
    allowlist_suggestions = _allowlist_companion_suggestions(
        repo,
        list(drop["allowed_modified_files"]),
        list(drop["allowed_new_files"]),
        readiness_profiles=readiness_profiles,
    )

    clean_worktree_retarget_recommended = bool(ignored_paths or dirty_paths)
    default_clean_worktree_path = _default_clean_worktree_path(drop) if clean_worktree_retarget_recommended else ""
    clean_preflight_parity = {
        "source": "internal/gitguard.EnsureClean",
        "gitguard_command": ["git", "status", "--porcelain", "--untracked-files=all"],
        "would_blk_pipe_git_dirty": bool(dirty_paths),
        "dirty_paths": dirty_paths,
        "ignored_detection_command": ["git", "status", "--porcelain=v1", "--ignored=matching", "--untracked-files=all"],
        "ignored_paths": ignored_paths,
        "recommended_action": "retarget_to_trusted_sterile_clean_worktree" if dirty_paths or ignored_paths else "none",
    }
    report = {
        "status": "BLOCKED" if blockers else "READY",
        "beb_id": drop["beb_id"],
        "l2_id": drop["l2_id"],
        "work_dir": work_dir,
        "target_branch": drop["target_branch"],
        "target_hash": drop["target_hash"],
        "allowed_modified_files": list(drop["allowed_modified_files"]),
        "allowed_new_files": list(drop["allowed_new_files"]),
        "validation_profiles": list(drop["validation_profiles"]),
        "readiness_profiles": readiness_profiles,
        "trace_artifacts": list(trace_artifacts),
        "allowlist_suggestions": allowlist_suggestions,
        "clean_preflight_parity": clean_preflight_parity,
        "clean_worktree_retarget_recommended": clean_worktree_retarget_recommended,
        "default_clean_worktree_root": str(_DEFAULT_CLEAN_WORKTREE_ROOT),
        "default_clean_worktree_path": str(default_clean_worktree_path),
        "source_cleanup_authorized": False,
        "worktree_creation_authorized": False,
        "dispatch_authorized": False,
        "blockers": blockers,
    }
    if "beo_id" in drop:
        report["beo_id"] = drop["beo_id"]
    return report


def _default_clean_worktree_path(drop: dict[str, Any]) -> Path:
    project = re.sub(r"[^a-z0-9]+", "-", str(drop.get("target_project", "kuronode")).casefold()).strip("-") or "kuronode"
    beb_slug = re.sub(r"[^a-z0-9]+", "-", str(drop.get("beb_id", "beb")).casefold()).strip("-") or "beb"
    target_prefix = str(drop.get("target_hash", "unknown"))[:12]
    return _DEFAULT_CLEAN_WORKTREE_ROOT / f"{project}-{beb_slug}-{target_prefix}"


def _git_output(repo: Path, args: list[str]) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def _git_status_paths(repo: Path, args: list[str], prefix: str | None = None) -> list[str]:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        return []
    paths: list[str] = []
    for line in result.stdout.splitlines():
        if not line:
            continue
        if prefix is not None and not line.startswith(prefix):
            continue
        path = line[3:] if len(line) > 3 else line
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths.append(path)
    return sorted(set(paths))


def _git_clean_dry_run_paths(repo: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "clean", "-ndX"],
            cwd=repo,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        return []
    prefix = "Would remove "
    paths = []
    for line in result.stdout.splitlines():
        if line.startswith(prefix):
            paths.append(line[len(prefix) :].strip())
    return sorted(set(paths))


def _load_drop_manifest(drop_path: Path) -> dict[str, Any]:
    if not drop_path.is_file():
        raise RouteError(f"drop_path is not a file: {drop_path}")
    try:
        data = json.loads(drop_path.read_text())
    except json.JSONDecodeError as exc:
        raise RouteError(f"drop manifest is not valid JSON: {exc.msg}") from exc
    if not isinstance(data, dict):
        raise RouteError("drop manifest must be a JSON object")

    forbidden = sorted(field for field in data if field in _FORBIDDEN_DROP_FIELDS)
    if forbidden:
        raise RouteError(f"drop manifest cannot supply caller-controlled fields: {', '.join(forbidden)}")
    unknown = sorted(set(data) - _ALLOWED_DROP_FIELDS)
    if unknown:
        raise RouteError(f"drop manifest contains unsupported fields: {', '.join(unknown)}")

    missing = [field for field in sorted(_CORE_DROP_FIELDS) if field not in data]
    if missing:
        raise RouteError(f"drop manifest missing required fields: {', '.join(missing)}")
    optional_present = set(data) & _OPTIONAL_DROP_FIELDS
    if optional_present and optional_present != _OPTIONAL_DROP_FIELDS:
        missing_optional = ", ".join(sorted(_OPTIONAL_DROP_FIELDS - optional_present))
        raise RouteError(f"drop manifest BEO fields must be supplied together: {missing_optional}")

    target_project = _required_string(data["target_project"], "target_project")
    if target_project != "kuronode":
        raise RouteError("target_project must equal kuronode")

    normalized = {
        "target_project": target_project,
        "beb_id": _required_pattern(data["beb_id"], "beb_id", _BEB_ID_RE),
        "l2_id": _required_pattern(data["l2_id"], "l2_id", _L2_ID_RE),
        "beb_path": _required_absolute_path(data["beb_path"], "beb_path"),
        "beb_sha256": _required_sha256(data["beb_sha256"], "beb_sha256"),
        "l2_path": _required_absolute_path(data["l2_path"], "l2_path"),
        "l2_sha256": _required_sha256(data["l2_sha256"], "l2_sha256"),
        "work_dir": _required_absolute_path(data["work_dir"], "work_dir"),
        "target_branch": _required_string(data["target_branch"], "target_branch"),
        "target_hash": _required_pattern(data["target_hash"], "target_hash", _GIT_HASH_RE),
        "allowed_modified_files": _required_path_list(data["allowed_modified_files"], "allowed_modified_files"),
        "allowed_new_files": _required_path_list(data["allowed_new_files"], "allowed_new_files"),
        "validation_profiles": _required_validation_profiles(data["validation_profiles"]),
        "readiness_profiles": _optional_readiness_profiles(data.get("readiness_profiles")),
    }
    if optional_present:
        normalized["beo_id"] = _required_pattern(data["beo_id"], "beo_id", _BEO_ID_RE)
        normalized["beo_path"] = _required_absolute_path(data["beo_path"], "beo_path")
        normalized["beo_sha256"] = _required_sha256(data["beo_sha256"], "beo_sha256")
    return normalized


def _required_resolved_roots(paths: Iterable[str | Path] | None, field_name: str) -> tuple[Path, ...]:
    if paths is None:
        raise RouteError(f"{field_name} must be supplied by trusted configuration")
    roots = tuple(Path(path).expanduser().resolve() for path in paths)
    if not roots:
        raise RouteError(f"{field_name} must not be empty")
    return roots


def _required_approved_hashes(hashes: Iterable[str] | None) -> set[str]:
    if hashes is None:
        raise RouteError("approved_drop_sha256s must be supplied by trusted configuration")
    approved = {_required_sha256(value, "approved_drop_sha256s[]") for value in hashes}
    if not approved:
        raise RouteError("approved_drop_sha256s must not be empty")
    return approved


def _file_sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _optional_artifact_slug(value: str | None) -> str | None:
    if value is None:
        return None
    slug = _required_string(value, "artifact_slug")
    if not _ARTIFACT_SLUG_RE.match(slug):
        raise RouteError("artifact_slug must be a filesystem-safe slug")
    return slug


def _artifact_filename(artifact_id: str, slug: str | None) -> str:
    stem = artifact_id if slug is None else f"{artifact_id}_{slug}"
    return f"{stem}.md"


def _write_obsidian_view_mirrors(
    mirror_dir: str | Path | None,
    *,
    artifacts: list[Path],
) -> list[Path]:
    if mirror_dir is None:
        return []
    mirror_candidate = Path(mirror_dir).expanduser()
    mirror_unresolved = mirror_candidate if mirror_candidate.is_absolute() else Path.cwd() / mirror_candidate
    _reject_symlinked_components(mirror_unresolved, "Obsidian mirror_dir")
    mirror_root = mirror_candidate.resolve()
    _reject_symlinked_components(mirror_root, "Obsidian mirror_dir")
    mirror_root.mkdir(parents=True, exist_ok=True)
    _reject_symlinked_components(mirror_root, "Obsidian mirror_dir")
    mirror_paths: list[Path] = []
    for source_path in artifacts:
        source = source_path.resolve(strict=True)
        destination = mirror_root / source.name
        if destination.is_symlink():
            raise RouteError("Obsidian mirror artifact path must not be a symlink")
        if destination.exists():
            if not destination.is_file():
                raise RouteError("existing Obsidian mirror destination must be a generated view-copy file")
            existing_text = destination.read_text()
            if not existing_text.startswith("> VIEW COPY — DO NOT EDIT\n"):
                raise RouteError("existing Obsidian mirror destination is not a generated view copy")
        header = "\n".join(
            [
                "> VIEW COPY — DO NOT EDIT",
                f"> Canonical source: {source}",
                f"> Canonical sha256: {_file_sha256(source)}",
                "> BLK-System consumes the canonical route package, not this Obsidian mirror.",
                "",
                "---",
                "",
            ]
        )
        tmp_destination = mirror_root / f".{source.name}.tmp"
        if tmp_destination.exists() or tmp_destination.is_symlink():
            raise RouteError("Obsidian mirror temp destination already exists")
        tmp_destination.write_text(header + source.read_text())
        tmp_destination.chmod(0o444)
        tmp_destination.replace(destination)
        destination.chmod(0o444)
        mirror_paths.append(destination)
    return mirror_paths


def _prepare_external_codex_final_message_artifact(beb_id: str | None, target_hash: str | None) -> Path:
    safe_beb_id = _required_pattern(beb_id, "beb_id", _BEB_ID_RE)
    safe_target_hash = _required_pattern(target_hash, "target_hash", _GIT_HASH_RE)
    artifact_root = Path("/tmp/blk-system-beb-l2-codex")
    artifact_dir = artifact_root / safe_beb_id / safe_target_hash[:12]
    _prepare_private_external_artifact_dir(artifact_root, artifact_dir)
    final_message = artifact_dir / "final-message.md"
    if final_message.is_symlink():
        raise RouteError("Codex final-message artifact path must not be a symlink")
    if final_message.exists():
        final_message.unlink()
    return final_message


def _prepare_private_external_artifact_dir(artifact_root: Path, artifact_dir: Path) -> None:
    _reject_symlinked_components(artifact_dir)
    artifact_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    _reject_symlinked_components(artifact_dir)
    try:
        artifact_root.chmod(0o700)
        artifact_dir.parent.chmod(0o700)
        artifact_dir.chmod(0o700)
    except PermissionError as exc:
        raise RouteError("Codex final-message artifact path must be private to the current user") from exc
    root_real = artifact_root.resolve(strict=True)
    dir_real = artifact_dir.resolve(strict=True)
    if dir_real != root_real and root_real not in dir_real.parents:
        raise RouteError("Codex final-message artifact path must remain under the external artifact root")


def _reject_symlinked_components(path: Path, field_name: str = "Codex final-message artifact path") -> None:
    current = Path(path.anchor or "/")
    for part in path.parts[1:]:
        current = current / part
        if current.is_symlink():
            raise RouteError(f"{field_name} must not contain symlinked components")


def _canonical_json_bytes(data: dict[str, Any]) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _json_sha256(data: dict[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json_bytes(data)).hexdigest()


def _text_sha256(value: Any) -> str:
    text = "" if value is None else str(value)
    return "sha256:" + hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def _result_to_dict(result: Any) -> dict[str, Any]:
    if is_dataclass(result):
        return asdict(result)
    if isinstance(result, dict):
        return dict(result)
    return {"status": getattr(result, "status", ""), "raw_result_type": type(result).__name__}


def _final_message_path_from_engine_args(engine_args: list[str]) -> Path | None:
    try:
        output_index = engine_args.index("--output-last-message") + 1
    except ValueError:
        return None
    if output_index >= len(engine_args):
        return None
    return Path(engine_args[output_index])


def _write_authoritative_route_summary(summary: dict[str, Any]) -> tuple[str, str]:
    root = Path("/tmp/blk-system-route-summaries")
    beb_dir = root / re.sub(r"[^A-Za-z0-9_.-]+", "-", str(summary.get("beb_id") or "beb")).strip("-. _")
    target_prefix = str(summary.get("target_hash") or "unknown")[:12] or "unknown"
    artifact_dir = beb_dir / target_prefix
    _prepare_private_external_artifact_dir(root, artifact_dir)
    path = artifact_dir / f"{str(summary.get('drop_manifest_sha256', '')).removeprefix('sha256:')[:16] or 'summary'}.json"
    if path.is_symlink():
        raise RouteError("route summary artifact path must not be a symlink")
    path.write_bytes(_canonical_json_bytes(summary))
    return str(path), _file_sha256(path)


def _build_authoritative_route_summary(
    result: Any,
    *,
    drop: dict[str, Any],
    drop_path: Path,
    approved_drop_sha256: str,
    engine_args: list[str],
) -> dict[str, Any]:
    result_dict = _result_to_dict(result)
    final_message = _final_message_path_from_engine_args(engine_args)
    final_message_sha256 = ""
    final_message_bytes = 0
    final_message_path = ""
    if final_message is not None:
        final_message_path = str(final_message)
        if final_message.is_file() and not final_message.is_symlink():
            final_message_sha256 = _file_sha256(final_message)
            final_message_bytes = final_message.stat().st_size
    validation_logs = result_dict.get("validation_logs") or {}
    validation_serialized = json.dumps(validation_logs, sort_keys=True) if validation_logs else ""
    summary = {
        "status": str(result_dict.get("status") or ""),
        "exit_code": int(result_dict.get("exit_code") or 0),
        "beb_id": drop["beb_id"],
        "beo_id": drop.get("beo_id", ""),
        "l2_id": drop["l2_id"],
        "work_dir": drop["work_dir"],
        "target_branch": drop["target_branch"],
        "target_hash": drop["target_hash"],
        "pre_engine_hash": str(result_dict.get("pre_engine_hash") or ""),
        "commit_hash": str(result_dict.get("commit_hash") or ""),
        "drop_manifest_path": str(drop_path),
        "drop_manifest_sha256": approved_drop_sha256,
        "payload_sha256": str(result_dict.get("payload_sha256") or ""),
        "final_message_artifact_path": final_message_path,
        "final_message_sha256": final_message_sha256,
        "final_message_bytes": final_message_bytes,
        "codex_final_message_authoritative": False,
        "engine_logs_sha256": _text_sha256(result_dict.get("engine_logs")),
        "engine_logs_bytes": len(str(result_dict.get("engine_logs") or "").encode("utf-8", errors="replace")),
        "validation_logs_sha256": _text_sha256(validation_serialized),
        "validation_logs_bytes": len(validation_serialized.encode("utf-8")),
        "validation_log_count": len(validation_logs) if isinstance(validation_logs, dict) else 0,
        "stderr_sha256": _text_sha256(result_dict.get("stderr")),
        "raw_logs_embedded": False,
        "reusable_codex_dispatch_authorized": False,
        "broad_blk_pipe_dispatch_authorized": False,
        "beo_publication_authorized": False,
        "rtm_generation_authorized": False,
        "source_cleanup_authorized": False,
        "worktree_creation_authorized": False,
    }
    artifact_path, artifact_sha = _write_authoritative_route_summary(summary)
    summary["route_summary_artifact_path"] = artifact_path
    summary["route_summary_artifact_sha256"] = artifact_sha
    return summary


def _attach_route_summary(
    result: Any,
    *,
    drop: dict[str, Any],
    drop_path: Path,
    approved_drop_sha256: str,
    engine_args: list[str],
) -> Any:
    summary = _build_authoritative_route_summary(
        result,
        drop=drop,
        drop_path=drop_path,
        approved_drop_sha256=approved_drop_sha256,
        engine_args=engine_args,
    )
    if is_dataclass(result):
        setattr(result, "route_summary", summary)
        setattr(result, "raw_report", {**(getattr(result, "raw_report", None) or {}), "route_summary": summary})
        return result
    if isinstance(result, dict):
        return {**result, "route_summary": summary}
    return {"status": getattr(result, "status", ""), "route_summary": summary, "raw_result": result}


def _assert_file_sha256(path: Path, expected_sha256: str, field_name: str) -> None:
    actual = _file_sha256(path)
    if actual != expected_sha256:
        raise RouteError(f"{field_name} sha256 does not match trusted configuration")


def _require_under_roots(path: Path, roots: tuple[Path, ...], field_name: str) -> Path:
    resolved = path.expanduser().resolve()
    if not any(resolved == root or root in resolved.parents for root in roots):
        raise RouteError(f"{field_name} must be under a trusted root")
    return resolved


def _require_non_protected_artifact_path(path: Path, field_name: str) -> Path:
    parts = tuple(part.casefold() for part in path.parts)
    for index in range(len(parts) - 1):
        pair = (parts[index], parts[index + 1])
        if pair in _PROTECTED_BLK_REQ_SEGMENTS:
            raise RouteError(
                f"{field_name} must not point at protected BLK-req paths; "
                "BEB/L2 artifacts must be package-owned metadata"
            )
    return path


def _assert_distinct_artifact_paths(*paths: Path) -> None:
    resolved = [path.expanduser().resolve() for path in paths]
    if len(set(resolved)) != len(resolved):
        raise RouteError("BEB, L2, and BEO artifact paths must be distinct")


def _require_exact_resolved_path(path: str, allowed: tuple[Path, ...], field_name: str) -> str:
    resolved = Path(path).expanduser().resolve()
    if resolved not in allowed:
        raise RouteError(f"{field_name} must match an approved Kuronode work_dir")
    return str(resolved)


def _read_verified_text_file(path: Path, expected_sha256: str, field_name: str) -> str:
    if not path.is_file():
        raise RouteError(f"{field_name} does not point to a file")
    data = path.read_bytes()
    actual = "sha256:" + hashlib.sha256(data).hexdigest()
    if actual != expected_sha256:
        raise RouteError(f"{field_name} sha256 does not match manifest")
    return data.decode()


def _parse_beb_frontmatter(text: str) -> list[str]:
    if not text.startswith("---\n"):
        raise RouteError("BEB file missing frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise RouteError("BEB file missing closing frontmatter fence")
    return text[4:end].splitlines()


def _frontmatter_scalar(lines: list[str], key: str) -> str:
    pattern = re.compile(rf"^{re.escape(key)}:\s*\"([^\"]+)\"\s*$")
    for line in lines:
        match = pattern.match(line)
        if match:
            return match.group(1)
    raise RouteError(f"BEB frontmatter missing {key}")


def _assert_bound_ids(drop: dict[str, Any], beb_metadata: list[str], l2_packet: str, beo_text: str = "") -> None:
    beb_id = _frontmatter_scalar(beb_metadata, "beb_id")
    l2_id = _frontmatter_scalar(beb_metadata, "l2_id")
    if drop["beb_id"] != beb_id:
        raise RouteError("drop beb_id does not match BEB frontmatter")
    if drop["l2_id"] != l2_id:
        raise RouteError("drop l2_id does not match BEB frontmatter")
    _assert_l2_matches_beb(l2_id, beb_id)
    if "beo_id" in drop:
        beo_id = _frontmatter_scalar(beb_metadata, "beo_id")
        if drop["beo_id"] != beo_id:
            raise RouteError("drop beo_id does not match BEB frontmatter")
        expected_beo_id = _required_matching_beo_id(drop["beo_id"], beb_id)
        if f"BEO_ID: {expected_beo_id}" not in l2_packet:
            raise RouteError("L2 packet does not bind to BEO identity")
        if beo_text:
            beo_metadata = _parse_beb_frontmatter(beo_text)
            if _frontmatter_scalar(beo_metadata, "beo_id") != expected_beo_id:
                raise RouteError("BEO frontmatter does not match drop beo_id")
            if _frontmatter_scalar(beo_metadata, "beb_id") != beb_id:
                raise RouteError("BEO frontmatter does not match paired BEB identity")
            if _frontmatter_scalar(beo_metadata, "l2_id") != l2_id:
                raise RouteError("BEO frontmatter does not match paired L2 identity")
            if _frontmatter_scalar(beo_metadata, "status") != "BEO_TEMPLATE_PENDING_EXECUTION_EVIDENCE":
                raise RouteError("BEO status must be BEO_TEMPLATE_PENDING_EXECUTION_EVIDENCE")
            if _parse_trace_artifacts(beo_metadata) != _parse_trace_artifacts(beb_metadata):
                raise RouteError("BEO trace_artifacts must match paired BEB trace_artifacts")
        else:
            raise RouteError("BEO artifact must not be empty")
    if f"BEB_ID: {beb_id}" not in l2_packet:
        raise RouteError("L2 packet does not bind to BEB identity")
    if f"L2_ID: {l2_id}" not in l2_packet:
        raise RouteError("L2 packet does not bind to L2 identity")


def _parse_trace_artifacts(lines: list[str]) -> list[dict[str, str]]:
    try:
        index = lines.index("trace_artifacts:") + 1
    except ValueError as exc:
        raise RouteError("BEB frontmatter missing trace_artifacts") from exc

    artifacts: list[dict[str, str]] = []
    while index < len(lines):
        line = lines[index]
        if line and not line.startswith("  "):
            break
        match = re.match(r"^\s{2}-\s+kind:\s*\"([^\"]+)\"\s*$", line)
        if not match:
            index += 1
            continue
        artifact = {"kind": match.group(1)}
        for next_line in lines[index + 1 : index + 3]:
            scalar = re.match(r"^\s{4}(id|version_hash):\s*\"([^\"]+)\"\s*$", next_line)
            if scalar:
                artifact[scalar.group(1)] = scalar.group(2)
        if set(artifact) != {"kind", "id", "version_hash"}:
            raise RouteError("BEB trace_artifacts entry is incomplete")
        if not _TRACE_HASH_RE.match(artifact["version_hash"]):
            raise RouteError("trace_artifacts.version_hash must match sha256:<64-lowercase-hex>")
        artifacts.append(artifact)
        index += 3

    if not artifacts:
        raise RouteError("BEB frontmatter missing trace_artifacts entries")
    return artifacts


def derive_matching_beo_id(beb_id: str) -> str:
    """Return the required BEO identity for a BEB identity in the same family/sequence."""
    safe_beb_id = _required_pattern(beb_id, "beb_id", _BEB_ID_RE)
    if safe_beb_id.startswith("BEB-"):
        return "BEO-" + safe_beb_id[len("BEB-") :]
    if safe_beb_id.startswith("BEB_"):
        return "BEO_" + safe_beb_id[len("BEB_") :]
    raise RouteError("beb_id has invalid format")


def _derive_matching_beb_l2_ids_from_beo(beo_id: str) -> tuple[str, str]:
    safe_beo_id = _required_pattern(beo_id, "beo_id", _BEO_ID_RE)
    if safe_beo_id.startswith("BEO-"):
        suffix = safe_beo_id[len("BEO-") :]
        return "BEB-" + suffix, "L2-" + suffix
    if safe_beo_id.startswith("BEO_"):
        suffix = safe_beo_id[len("BEO_") :]
        return "BEB_" + suffix, "L2_" + suffix
    raise RouteError("beo_id has invalid format")


def _derive_matching_l2_id(beb_id: str) -> str:
    safe_beb_id = _required_pattern(beb_id, "beb_id", _BEB_ID_RE)
    if safe_beb_id.startswith("BEB-"):
        return "L2-" + safe_beb_id[len("BEB-") :]
    if safe_beb_id.startswith("BEB_"):
        return "L2_" + safe_beb_id[len("BEB_") :]
    raise RouteError("beb_id has invalid format")


def _required_matching_beo_id(beo_id: str | None, beb_id: str) -> str:
    expected = derive_matching_beo_id(beb_id)
    if beo_id is None:
        return expected
    safe_beo_id = _required_pattern(beo_id, "beo_id", _BEO_ID_RE)
    if safe_beo_id != expected:
        raise RouteError("beo_id must match BEB family and sequence")
    return safe_beo_id


def _assert_l2_matches_beb(l2_id: str, beb_id: str) -> None:
    expected = _derive_matching_l2_id(beb_id)
    if l2_id != expected:
        raise RouteError("l2_id must match BEB family and sequence")


def _required_trace_artifacts(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list) or not value:
        raise RouteError("trace_artifacts must be a non-empty list")
    artifacts: list[dict[str, str]] = []
    for index, artifact in enumerate(value):
        if not isinstance(artifact, dict):
            raise RouteError(f"trace_artifacts[{index}] must be an object")
        kind = _required_string(artifact.get("kind"), f"trace_artifacts[{index}].kind")
        artifact_id = _required_string(artifact.get("id"), f"trace_artifacts[{index}].id")
        version_hash = _required_sha256(artifact.get("version_hash"), f"trace_artifacts[{index}].version_hash")
        artifacts.append({"kind": kind, "id": artifact_id, "version_hash": version_hash})
    return artifacts


def _required_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RouteError(f"{field_name} must be a non-empty string")
    return value.strip()


def _required_pattern(value: Any, field_name: str, pattern: re.Pattern[str]) -> str:
    text = _required_string(value, field_name)
    if not pattern.match(text):
        raise RouteError(f"{field_name} has invalid format")
    return text


def _required_sha256(value: Any, field_name: str) -> str:
    return _required_pattern(value, field_name, _TRACE_HASH_RE)


def _required_absolute_path(value: Any, field_name: str) -> str:
    text = _required_string(value, field_name)
    if not Path(text).is_absolute():
        raise RouteError(f"{field_name} must be absolute")
    return text


def _required_validation_profiles(value: Any) -> list[str]:
    profiles = _required_string_list(value, "validation_profiles")
    unknown = sorted(set(profiles) - _ALLOWED_VALIDATION_PROFILES)
    if unknown:
        raise RouteError(f"validation_profiles contain unsupported profiles: {', '.join(unknown)}")
    return profiles


def _optional_readiness_profiles(value: Any) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise RouteError("readiness_profiles must be a list")
    if not value:
        return []
    profiles = [_required_string(item, "readiness_profiles[]") for item in value]
    unknown = sorted(set(profiles) - _ALLOWED_READINESS_PROFILES)
    if unknown:
        raise RouteError(f"readiness_profiles contain unsupported profiles: {', '.join(unknown)}")
    if len(set(profiles)) != len(profiles):
        raise RouteError("readiness_profiles must not contain duplicates")
    return profiles


def _readiness_profile_section_lines(profiles: list[str]) -> list[str]:
    if not profiles:
        return []
    lines = [
        _READINESS_PROFILE_SECTION_HEADING,
        "",
        _READINESS_PROFILE_NON_AUTHORITY_DISCLAIMER,
        "",
    ]
    for profile in profiles:
        lines.extend([f"### {profile}", ""])
        for probe_id, description in _READINESS_PROFILE_PROBES[profile]:
            lines.append(f"- [ ] {probe_id} {description}")
        lines.append("")
    return lines


def _readiness_profile_blockers(profiles: list[str], *, beb_text: str, l2_packet: str) -> list[dict[str, Any]]:
    blockers: list[dict[str, Any]] = []
    for profile in profiles:
        profile_heading = f"### {profile}"
        required_card_markers = (
            _READINESS_PROFILE_SECTION_HEADING,
            _READINESS_PROFILE_NON_AUTHORITY_DISCLAIMER,
            profile_heading,
        )
        if any(marker not in beb_text or marker not in l2_packet for marker in required_card_markers):
            blockers.append({
                "code": "MISSING_READINESS_PROFILE_CARD",
                "message": "readiness profile requires the generated non-authorizing probe-card section in both BEB and L2 artifacts",
                "profile": profile,
                "paths": [],
            })
        for probe_id, description in _READINESS_PROFILE_PROBES[profile]:
            required_phrase = f"- [ ] {probe_id} {description}"
            if required_phrase not in beb_text or required_phrase not in l2_packet:
                blockers.append({
                    "code": "MISSING_READINESS_PROBE",
                    "message": "readiness profile probe card is incomplete in the hash-bound BEB/L2 artifacts",
                    "profile": profile,
                    "probe_id": probe_id,
                    "probe": description,
                    "paths": [],
                })
    return blockers


def _required_string_list(value: Any, field_name: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise RouteError(f"{field_name} must be a non-empty list")
    return [_required_string(item, f"{field_name}[]") for item in value]


def _required_path_list(value: Any, field_name: str) -> list[str]:
    if not isinstance(value, list):
        raise RouteError(f"{field_name} must be a list")
    paths: list[str] = []
    for item in value:
        raw_path = _required_string(item, f"{field_name}[]")
        path = raw_path.replace("\\", "/")
        if path.startswith("/"):
            raise RouteError(f"{field_name} entries must be relative")
        parts = [part for part in path.split("/") if part]
        if ".." in parts:
            raise RouteError(f"{field_name} entries must not contain path traversal")
        normalized = "/".join(parts)
        if normalized in {"", "."} or normalized.startswith(":") or any(char in normalized for char in _GLOB_CHARS):
            raise RouteError(f"{field_name} entries must be explicit relative files")
        if any(normalized == prefix.rstrip("/") or normalized.startswith(prefix) for prefix in _PROTECTED_ALLOWLIST_PREFIXES):
            raise RouteError(f"{field_name} entries must not target protected BLK-req paths")
        paths.append(normalized)
    return paths


def _jsonable_report(report: Any) -> Any:
    if is_dataclass(report):
        return asdict(report)
    return report


_PROGRESS_STATUS_EVENTS = {
    "preflight_ready",
    "blk_pipe_launching",
    "blk_pipe_started",
    "codex_started",
    "codex_completed",
    "codex_failed",
    "validation_started",
    "validation_passed",
    "validation_failed",
    "testing_completed",
    "testing_failed",
    "blk_pipe_finished",
}


def _progress_status_line(event: dict[str, Any]) -> str | None:
    event_name = event.get("event", "")
    if event_name not in _PROGRESS_STATUS_EVENTS:
        return None
    beb_id = event.get("beb_id") or "unknown-beb"
    status = event.get("status") or ""
    failure_class = event.get("failure_class") or ""
    timeout_seconds = event.get("timeout_seconds") or 0
    validation_count = event.get("validation_command_count")
    if event_name == "preflight_ready":
        return f"[BLK status] {beb_id} preflight ready"
    if event_name == "blk_pipe_launching":
        return f"[BLK status] {beb_id} BLK-pipe launching"
    if event_name == "blk_pipe_started":
        return f"[BLK status] {beb_id} started"
    if event_name == "codex_started":
        return f"[BLK status] {beb_id} Codex started"
    if event_name == "codex_completed":
        return f"[BLK status] {beb_id} Codex completed: {status}"
    if event_name == "codex_failed":
        parts = [f"[BLK status] {beb_id} Codex failed: {status}"]
        if failure_class:
            parts.append(f"failure_class={failure_class}")
        if timeout_seconds:
            parts.append(f"timeout_seconds={timeout_seconds}")
        return " ".join(parts)
    if event_name == "validation_started":
        return f"[BLK status] {beb_id} validation started validation_commands={validation_count}"
    if event_name == "validation_passed":
        return f"[BLK status] {beb_id} validation passed: {status}"
    if event_name == "validation_failed":
        return f"[BLK status] {beb_id} validation failed: {status}"
    if event_name == "testing_completed":
        return f"[BLK status] {beb_id} testing completed: {status} validation_commands={validation_count}"
    if event_name == "testing_failed":
        parts = [f"[BLK status] {beb_id} testing failed: {status}"]
        if failure_class:
            parts.append(f"failure_class={failure_class}")
        return " ".join(parts)
    if event_name == "blk_pipe_finished":
        return f"[BLK status] {beb_id} finished: {status}"
    return None


def _write_progress_status_stderr(event: dict[str, Any]) -> None:
    line = _progress_status_line(event)
    if line is not None:
        print(line, file=sys.stderr, flush=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Dispatch BEB-L2 drops through BLK-pipe/Codex")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--drop", help="absolute path to one drop manifest JSON")
    group.add_argument("--inbox", help="directory containing queued *.json drop manifests")
    parser.add_argument("--processed-dir", default=".blk-pipe/processed")
    parser.add_argument("--failed-dir", default=".blk-pipe/failed")
    parser.add_argument("--allowed-work-dir", action="append", required=True)
    parser.add_argument("--trusted-root", action="append", required=True)
    parser.add_argument("--approved-drop-sha256", action="append", required=True)
    parser.add_argument("--preflight", action="store_true", help="validate one --drop and inspect repo readiness without invoking BLK-pipe")
    parser.add_argument("--cleanup-plan", action="store_true", help="emit non-mutating ignored-residue cleanup evidence for one --drop")
    parser.add_argument("--clean-worktree-manifest", action="store_true", help="emit a retargeted drop manifest for a trusted clean worktree without dispatch")
    parser.add_argument("--clean-work-dir", help="absolute path to the clean worktree candidate for --clean-worktree-manifest")
    parser.add_argument("--clean-worktree-root", action="append", help="trusted root for clean worktree candidates")
    parser.add_argument("--clean-worktree-manifest-output", help="write the retargeted manifest using exact compact canonical JSON bytes")
    parser.add_argument(
        "--progress-stderr",
        action="store_true",
        help="emit operator-facing BLK status updates to stderr during dispatch",
    )
    args = parser.parse_args(argv)

    planning_modes = [args.preflight, args.cleanup_plan, args.clean_worktree_manifest]
    if sum(1 for enabled in planning_modes if enabled) > 1:
        raise RouteError("--preflight, --cleanup-plan, and --clean-worktree-manifest are mutually exclusive")
    if any(planning_modes) and not args.drop:
        raise RouteError("--preflight/--cleanup-plan/--clean-worktree-manifest require --drop")
    if args.clean_worktree_manifest and (not args.clean_work_dir or not args.clean_worktree_root):
        raise RouteError("--clean-worktree-manifest requires --clean-work-dir and --clean-worktree-root")
    if not args.clean_worktree_manifest and (args.clean_work_dir or args.clean_worktree_root or args.clean_worktree_manifest_output):
        raise RouteError("--clean-work-dir/--clean-worktree-root/--clean-worktree-manifest-output require --clean-worktree-manifest")

    if args.drop:
        if len(args.approved_drop_sha256) != 1:
            raise RouteError("--drop requires exactly one --approved-drop-sha256")
        if args.clean_worktree_manifest:
            report = build_clean_worktree_drop_manifest(
                args.drop,
                clean_work_dir=args.clean_work_dir,
                clean_worktree_roots=args.clean_worktree_root,
                allowed_work_dirs=args.allowed_work_dir,
                trusted_roots=args.trusted_root,
                approved_drop_sha256=args.approved_drop_sha256[0],
                manifest_output_path=args.clean_worktree_manifest_output,
            )
        elif args.cleanup_plan:
            report = build_ignored_residue_cleanup_plan(
                args.drop,
                allowed_work_dirs=args.allowed_work_dir,
                trusted_roots=args.trusted_root,
                approved_drop_sha256=args.approved_drop_sha256[0],
            )
        elif args.preflight:
            report = preflight_drop_file(
                args.drop,
                allowed_work_dirs=args.allowed_work_dir,
                trusted_roots=args.trusted_root,
                approved_drop_sha256=args.approved_drop_sha256[0],
            )
        else:
            report = process_drop_file(
                args.drop,
                allowed_work_dirs=args.allowed_work_dir,
                trusted_roots=args.trusted_root,
                approved_drop_sha256=args.approved_drop_sha256[0],
                progress_callback=_write_progress_status_stderr if args.progress_stderr else None,
            )
    else:
        report = dispatch_inbox_once(
            args.inbox,
            args.processed_dir,
            args.failed_dir,
            allowed_work_dirs=args.allowed_work_dir,
            trusted_roots=args.trusted_root,
            approved_drop_sha256s=args.approved_drop_sha256,
            progress_callback=_write_progress_status_stderr if args.progress_stderr else None,
        )
    print(json.dumps(_jsonable_report(report), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
