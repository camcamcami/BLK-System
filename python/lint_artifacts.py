"""BLK-req legislative gateway contract and staged artifact helpers.

BLK-SYSTEM-116 introduced the contract-only surface. BLK-SYSTEM-117 adds
the version-aware staging linter. Later sprints extend this module with the
staging draft writer and canonical hash engine.

The module is intentionally local and deterministic: it does not dispatch
BLK-pipe, run BLK-test, publish BEOs, generate RTM artifacts, mutate target
repositories, or claim production isolation.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

BLK_REQ_DENIED_AUTHORITIES = {
    "BLK_PIPE_RUNTIME_DISPATCH",
    "TARGET_SOURCE_GIT_MUTATION",
    "BLK_TEST_RUNTIME",
    "BEO_PUBLICATION",
    "RTM_GENERATION",
    "RTM_DRIFT_REJECTION",
    "PROTECTED_ACTIVE_BODY_READS",
    "ACTIVE_VAULT_WRITE",
    "LIVE_CODEX_DISPATCH",
    "NETWORK_MODEL_BROWSER_CYBER_TOOLING",
    "PACKAGE_MANAGER_TOOLING",
    "SIGNER_STORAGE_LEDGER_ROLLBACK",
    "PRODUCTION_ISOLATION_CLAIM",
    "HITL_APPROVAL_CAPTURE",
    "ACTIVE_VAULT_PROMOTION",
    "EXACT_ID_RETRIEVAL",
}

_SIDE_EFFECT_FLAGS = {
    "blk_pipe_dispatch_performed",
    "target_source_git_mutation_performed",
    "blk_test_runtime_performed",
    "beo_publication_performed",
    "rtm_generation_performed",
    "rtm_drift_rejection_performed",
    "protected_active_body_read",
    "active_vault_write_performed",
    "live_codex_dispatch_performed",
    "network_model_browser_cyber_tooling_performed",
    "package_manager_tooling_performed",
    "signer_storage_ledger_rollback_performed",
    "production_isolation_claimed",
    "hitl_approval_capture_performed",
    "active_vault_promotion_performed",
    "exact_id_retrieval_performed",
}

_CONTRACT_KEYS = {
    "contract_marker",
    "contract_status",
    "sprint",
    "governing_docs",
    "allowed_local_backend_operations",
    "denied_authorities",
    "side_effect_flags",
    "notes",
}

_ALLOWED_OPERATIONS = [
    "BLK_SYSTEM_117_STAGING_LINTER",
    "BLK_SYSTEM_118_STAGING_DRAFT_WRITER",
    "BLK_SYSTEM_119_CANONICAL_VERSION_HASH_ENGINE",
]

_REQUIRED_DRAFT_FIELDS = {
    "id",
    "schema_version",
    "parent_hash",
    "version_hash",
    "status",
    "rationale",
    "linked_nodes",
}

_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_REQ_ID_RE = re.compile(r"^REQ-\d{3}$")
_UC_ID_RE = re.compile(r"^UC-\d{3}$")
_LINK_RE = re.compile(r"^\[\[(REQ|UC)-\d{3}\]\]$")
_WORD_RE = re.compile(r"\b[\w'-]+\b")
_REQ_CONJUNCTION_RE = re.compile(r"\b(and|or|while)\b", re.IGNORECASE)
_REQ_SUBJECTIVE_RE = re.compile(r"\b(fast|user[- ]friendly)\b", re.IGNORECASE)

_FORBIDDEN_COMPACT_WORDING = {
    "approvedforliveexecution",
    "approvedforruntimeexecution",
    "runtimeexecutionapproved",
    "runtimeexecutionauthorized",
    "liveexecutionauthorized",
    "blkpipeexecutionauthorized",
    "blkpipedispatchauthorized",
    "blktestruntimeauthorized",
    "productionblktestmcpauthorized",
    "beopublicationgranted",
    "beopublicationauthorized",
    "authoritativebeopublicationauthorized",
    "rtmgenerationauthorized",
    "runtimertmgenerationauthorized",
    "rtmdriftrejectionauthorized",
    "protectedbodyreadsauthorized",
    "protectedactivebodyreadsauthorized",
    "activevaultreadsauthorized",
    "activevaultwriteauthorized",
    "targetrepomutationauthorized",
    "sourcemutationauthorized",
    "gitmutationauthorized",
    "livecodexdispatchauthorized",
    "packagemanagertoolingauthorized",
    "networkmodelbrowsercybertoolingauthorized",
    "signerstorageledgerauthorized",
    "productionisolationclaimed",
    "hitlapprovalcaptured",
    "activevaultpromotionauthorized",
    "exactidretrievalauthorized",
}


def build_legislative_gateway_contract() -> dict[str, Any]:
    """Return the BLK-SYSTEM-116 local backend contract scaffold."""

    return {
        "contract_marker": "BLK_SYSTEM_116_BLK_REQ_LEGISLATIVE_GATEWAY_CONTRACT",
        "contract_status": "CONTRACT_READY_NOT_EXECUTION_AUTHORITY",
        "sprint": "BLK-SYSTEM-116",
        "governing_docs": ["BLK-002", "BLK-005", "BLK-006", "BLK-077", "BLK-079", "BLK-116"],
        "allowed_local_backend_operations": list(_ALLOWED_OPERATIONS),
        "denied_authorities": sorted(BLK_REQ_DENIED_AUTHORITIES),
        "side_effect_flags": {flag: False for flag in sorted(_SIDE_EFFECT_FLAGS)},
        "notes": [
            "BLK-SYSTEM-116 is a contract scaffold only.",
            "BLK-SYSTEM-117 through BLK-SYSTEM-119 may add local staging linting, staging draft writing, and canonical hash primitives.",
            "BLK-SYSTEM-120 and later approval, promotion, revision, and retrieval work require separate sprint scope.",
            "BLK-test is a BLK-System functional module, not BLK-System's test suite.",
        ],
    }


def validate_legislative_gateway_contract(contract: dict[str, Any]) -> list[str]:
    """Validate the BLK-SYSTEM-116 contract without granting authority."""

    errors: list[str] = []
    if not isinstance(contract, dict):
        return ["contract must be a dictionary"]

    extra = sorted(set(contract) - _CONTRACT_KEYS)
    missing = sorted(_CONTRACT_KEYS - set(contract))
    for key in extra:
        errors.append(f"unsupported contract field: {key}")
    for key in missing:
        errors.append(f"missing contract field: {key}")

    if contract.get("contract_marker") != "BLK_SYSTEM_116_BLK_REQ_LEGISLATIVE_GATEWAY_CONTRACT":
        errors.append("contract_marker must be BLK_SYSTEM_116_BLK_REQ_LEGISLATIVE_GATEWAY_CONTRACT")
    if contract.get("contract_status") != "CONTRACT_READY_NOT_EXECUTION_AUTHORITY":
        errors.append("contract_status must be CONTRACT_READY_NOT_EXECUTION_AUTHORITY")
    if contract.get("allowed_local_backend_operations") != _ALLOWED_OPERATIONS:
        errors.append("allowed_local_backend_operations must match BLK-SYSTEM-117/118/119 sequence")

    denied = contract.get("denied_authorities")
    if not isinstance(denied, list) or set(denied) != BLK_REQ_DENIED_AUTHORITIES or len(denied) != len(set(denied)):
        errors.append("denied_authorities must match exact BLK-116 set")

    flags = contract.get("side_effect_flags")
    if not isinstance(flags, dict):
        errors.append("side_effect_flags must be a dictionary")
    else:
        if set(flags) != _SIDE_EFFECT_FLAGS:
            errors.append("side_effect_flags must match exact BLK-116 set")
        for flag, value in flags.items():
            if value is not False:
                errors.append(f"side_effect_flags.{flag} must remain false")

    errors.extend(_scan_for_authority_laundering(contract))
    return _unique(errors)


def canonicalize_artifact_text(text: str) -> str:
    """Serialize the BLK-req version-hash input as deterministic JSON."""

    metadata, body, parse_errors = parse_artifact_text(text)
    diagnostics = list(parse_errors)
    diagnostics.extend(_validate_canonical_metadata(metadata, body))
    if diagnostics:
        codes = ", ".join(diagnostic["code"] for diagnostic in diagnostics)
        raise ValueError(f"artifact cannot be canonicalized: {codes}")
    payload = {
        "id": metadata["id"],
        "schema_version": metadata["schema_version"],
        "status": metadata["status"],
        "rationale": metadata["rationale"],
        "linked_nodes": list(metadata["linked_nodes"]),
        "body": body,
    }
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def compute_version_hash(text: str) -> str:
    """Compute `sha256:<64-lowercase-hex>` for canonical BLK-req text."""

    canonical = canonicalize_artifact_text(text)
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def preview_staging_version_hash(path: str | Path, *, workspace: str | Path | None = None) -> dict[str, Any]:
    """Compute a staging-only hash preview without promotion or active reads."""

    workspace_path = Path.cwd() if workspace is None else Path(workspace)
    classification = _classify_staging_artifact_path(Path(path), workspace_path)
    if classification["diagnostics"]:
        return _hash_preview_result(
            ok=False,
            version_hash=None,
            canonical_serialization=None,
            diagnostics=classification["diagnostics"],
            staging_body_read=False,
        )
    artifact_path = classification["path"]
    try:
        text = artifact_path.read_text(encoding="utf-8")
        canonical = canonicalize_artifact_text(text)
        version_hash = "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    except FileNotFoundError:
        return _hash_preview_result(
            ok=False,
            version_hash=None,
            canonical_serialization=None,
            diagnostics=[_diagnostic("FILE_NOT_FOUND", "artifact file does not exist", "path")],
            staging_body_read=False,
        )
    except ValueError as exc:
        return _hash_preview_result(
            ok=False,
            version_hash=None,
            canonical_serialization=None,
            diagnostics=[_diagnostic("CANONICALIZATION_FAILED", str(exc), "artifact")],
            staging_body_read=True,
        )
    return _hash_preview_result(
        ok=True,
        version_hash=version_hash,
        canonical_serialization=canonical,
        diagnostics=[],
        staging_body_read=True,
    )


def lint_artifact(path: str | Path, *, workspace: str | Path | None = None) -> dict[str, Any]:
    """Lint one staging artifact and return deterministic JSON-like diagnostics.

    Path classification happens before any file-body read. Only direct Markdown
    files under `docs/requirements/staging/` or `docs/use_cases/staging/` are
    eligible.
    """

    workspace_path = Path.cwd() if workspace is None else Path(workspace)
    classification = _classify_staging_artifact_path(Path(path), workspace_path)
    if classification["diagnostics"]:
        return _lint_result(
            ok=False,
            artifact_type=classification.get("artifact_type", "UNKNOWN"),
            schema_version=None,
            diagnostics=classification["diagnostics"],
            body_word_count=0,
            staging_body_read=False,
        )

    artifact_path = classification["path"]
    try:
        text = artifact_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return _lint_result(
            ok=False,
            artifact_type=classification["artifact_type"],
            schema_version=None,
            diagnostics=[_diagnostic("FILE_NOT_FOUND", "artifact file does not exist", "path")],
            body_word_count=0,
            staging_body_read=False,
        )
    except OSError as exc:
        return _lint_result(
            ok=False,
            artifact_type=classification["artifact_type"],
            schema_version=None,
            diagnostics=[_diagnostic("FILE_READ_FAILED", str(exc), "path")],
            body_word_count=0,
            staging_body_read=False,
        )

    return lint_artifact_text(text, artifact_type=classification["artifact_type"])


def build_draft_artifact_text(
    *,
    artifact_type: str,
    body: str,
    rationale: str,
    linked_nodes: list[str],
) -> str:
    """Build strict new-draft Markdown text for the BLK-req staging writer."""

    _normalize_artifact_type(artifact_type)
    if not isinstance(linked_nodes, list):
        raise ValueError("linked_nodes must be a list")
    metadata_lines = [
        "---",
        f"id: {_yaml_quote('TBD')}",
        f"schema_version: {_yaml_quote('1.0')}",
        f"parent_hash: {_yaml_quote('')}",
        f"version_hash: {_yaml_quote('PENDING')}",
        f"status: {_yaml_quote('DRAFT')}",
        f"rationale: {_yaml_quote(rationale)}",
    ]
    if linked_nodes:
        metadata_lines.append("linked_nodes:")
        for node in linked_nodes:
            metadata_lines.append(f"  - {_yaml_quote(node)}")
    else:
        metadata_lines.append("linked_nodes: []")
    metadata_lines.append("---")
    return "\n".join(metadata_lines) + "\n" + str(body).rstrip() + "\n"


def write_staging_draft(
    *,
    workspace: str | Path,
    artifact_type: str,
    title: str,
    body: str,
    rationale: str,
    linked_nodes: list[str],
    filename_slug: str | None = None,
    overwrite: bool = False,
) -> dict[str, Any]:
    """Validate and write a new BLK-req draft under the correct staging tree."""

    kind = _normalize_artifact_type(artifact_type)
    root = Path(workspace).resolve()
    slug = _validate_slug(filename_slug if filename_slug is not None else _slugify(title))
    rel_dir = Path("docs/requirements/staging") if kind == "REQ" else Path("docs/use_cases/staging")
    rel_path = rel_dir / f"{slug}.md"
    path = root / rel_path
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError("staging draft path escaped workspace") from exc

    text = build_draft_artifact_text(artifact_type=kind, body=body, rationale=rationale, linked_nodes=linked_nodes)
    lint = lint_artifact_text(text, artifact_type=kind)
    if not lint["ok"]:
        return _draft_result(
            status="STAGING_DRAFT_REJECTED",
            written=False,
            relative_path=rel_path,
            diagnostics=lint["diagnostics"],
            lint=lint,
        )
    symlink_diagnostic = _staging_symlink_diagnostic(path, root)
    if symlink_diagnostic is not None:
        return _draft_result(
            status="STAGING_DRAFT_REJECTED",
            written=False,
            relative_path=rel_path,
            diagnostics=[symlink_diagnostic],
            lint=lint,
        )
    if path.exists() and not overwrite:
        diagnostics = [_diagnostic("STAGING_DRAFT_EXISTS", "staging draft already exists", "path")]
        return _draft_result(
            status="STAGING_DRAFT_REJECTED",
            written=False,
            relative_path=rel_path,
            diagnostics=diagnostics,
            lint=lint,
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    symlink_diagnostic = _staging_symlink_diagnostic(path, root)
    if symlink_diagnostic is not None:
        return _draft_result(
            status="STAGING_DRAFT_REJECTED",
            written=False,
            relative_path=rel_path,
            diagnostics=[symlink_diagnostic],
            lint=lint,
        )
    path.write_text(text, encoding="utf-8")
    post_write_lint = lint_artifact(path, workspace=root)
    return _draft_result(
        status="STAGING_DRAFT_WRITTEN",
        written=True,
        relative_path=rel_path,
        diagnostics=post_write_lint["diagnostics"],
        lint=post_write_lint,
    )


def lint_artifact_text(text: str, *, artifact_type: str) -> dict[str, Any]:
    """Lint artifact text already constrained to a staging artifact type."""

    metadata, body, parse_errors = parse_artifact_text(text)
    diagnostics = list(parse_errors)
    if artifact_type not in {"REQ", "UC"}:
        diagnostics.append(_diagnostic("UNKNOWN_ARTIFACT_TYPE", "artifact type must be REQ or UC", "artifact_type"))

    diagnostics.extend(_validate_draft_metadata(metadata, artifact_type=artifact_type))
    diagnostics.extend(_validate_body(body, artifact_type=artifact_type))
    return _lint_result(
        ok=not diagnostics,
        artifact_type=artifact_type,
        schema_version=metadata.get("schema_version") if isinstance(metadata, dict) else None,
        diagnostics=diagnostics,
        body_word_count=_word_count(body),
        staging_body_read=True,
    )


def parse_artifact_text(text: str) -> tuple[dict[str, Any], str, list[dict[str, str]]]:
    """Parse a minimal YAML-frontmatter Markdown artifact.

    The parser deliberately supports only the BLK-req schema subset needed by
    the local backend: scalar strings and a `linked_nodes` string list.
    """

    if not isinstance(text, str):
        return {}, "", [_diagnostic("ARTIFACT_TEXT_TYPE", "artifact text must be a string", "artifact")]
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return {}, text, [_diagnostic("FRONTMATTER_MISSING", "artifact must start with YAML frontmatter", "frontmatter")]

    end_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end_index = index
            break
    if end_index is None:
        return {}, "".join(lines[1:]), [_diagnostic("FRONTMATTER_UNCLOSED", "frontmatter closing delimiter missing", "frontmatter")]

    metadata, parse_errors = _parse_frontmatter_lines(lines[1:end_index])
    body = "".join(lines[end_index + 1 :])
    return metadata, body, parse_errors


def _classify_staging_artifact_path(path: Path, workspace: Path) -> dict[str, Any]:
    diagnostics: list[dict[str, str]] = []
    root = workspace.resolve()
    candidate = path if path.is_absolute() else root / path
    resolved = candidate.resolve(strict=False)
    try:
        rel = resolved.relative_to(root)
    except ValueError:
        return {
            "artifact_type": "UNKNOWN",
            "path": resolved,
            "diagnostics": [_diagnostic("PATH_OUTSIDE_WORKSPACE", "artifact path must stay inside workspace", "path")],
        }

    parts = rel.parts
    artifact_type = "UNKNOWN"
    if len(parts) == 4 and parts[:3] == ("docs", "requirements", "staging"):
        artifact_type = "REQ"
    elif len(parts) == 4 and parts[:3] == ("docs", "use_cases", "staging"):
        artifact_type = "UC"
    else:
        diagnostics.append(_diagnostic("PATH_NOT_STAGING", "artifact path must target a staging directory", "path"))
    if resolved.suffix != ".md":
        diagnostics.append(_diagnostic("PATH_SUFFIX", "artifact path must end in .md", "path"))
    return {"artifact_type": artifact_type, "path": resolved, "diagnostics": diagnostics}


def _staging_symlink_diagnostic(path: Path, root: Path) -> dict[str, str] | None:
    """Reject symlinked staging write paths before any active-vault write can occur."""

    try:
        rel = path.relative_to(root)
    except ValueError:
        return _diagnostic("PATH_OUTSIDE_WORKSPACE", "staging draft path must stay inside workspace", "path")

    current = root
    for part in rel.parts:
        current = current / part
        try:
            if current.is_symlink():
                return _diagnostic("STAGING_PATH_SYMLINK", "staging draft path must not traverse symlinks", "path")
            if current.exists():
                current.resolve(strict=True).relative_to(root)
        except ValueError:
            return _diagnostic("PATH_OUTSIDE_WORKSPACE", "staging draft path must stay inside workspace", "path")
        except OSError:
            return _diagnostic("STAGING_PATH_UNRESOLVABLE", "staging draft path could not be resolved safely", "path")
    return None


def _parse_frontmatter_lines(lines: list[str]) -> tuple[dict[str, Any], list[dict[str, str]]]:
    metadata: dict[str, Any] = {}
    diagnostics: list[dict[str, str]] = []
    current_list_key: str | None = None

    for raw_line in lines:
        if not raw_line.strip():
            continue
        stripped = raw_line.strip()
        if stripped.startswith("- ") and current_list_key:
            metadata[current_list_key].append(_unquote(stripped[2:].strip()))
            continue
        if raw_line.startswith((" ", "\t")):
            diagnostics.append(_diagnostic("FRONTMATTER_UNSUPPORTED_INDENT", "unsupported frontmatter indentation", "frontmatter"))
            continue
        if ":" not in raw_line:
            diagnostics.append(_diagnostic("FRONTMATTER_PARSE", "frontmatter line must contain ':'", "frontmatter"))
            continue
        key, value = raw_line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key in metadata:
            diagnostics.append(_diagnostic("FRONTMATTER_DUPLICATE_KEY", "duplicate frontmatter key", key))
            continue
        if key == "linked_nodes":
            if value == "[]":
                metadata[key] = []
                current_list_key = None
            elif value == "":
                metadata[key] = []
                current_list_key = key
            else:
                metadata[key] = _unquote(value)
                current_list_key = None
        else:
            metadata[key] = _unquote(value)
            current_list_key = None
    return metadata, diagnostics


def _validate_draft_metadata(metadata: dict[str, Any], *, artifact_type: str) -> list[dict[str, str]]:
    diagnostics: list[dict[str, str]] = []
    missing = sorted(_REQUIRED_DRAFT_FIELDS - set(metadata))
    extra = sorted(set(metadata) - _REQUIRED_DRAFT_FIELDS)
    for field in missing:
        diagnostics.append(_diagnostic("METADATA_MISSING_FIELD", f"missing required metadata field {field}", field))
    for field in extra:
        diagnostics.append(_diagnostic("METADATA_UNSUPPORTED_FIELD", f"unsupported metadata field {field}", field))

    schema_version = metadata.get("schema_version")
    if schema_version != "1.0":
        diagnostics.append(_diagnostic("SCHEMA_VERSION_UNSUPPORTED", "schema_version must be 1.0", "schema_version"))
    if metadata.get("status") != "DRAFT":
        diagnostics.append(_diagnostic("STATUS_NOT_DRAFT", "staging artifacts must be DRAFT", "status"))
    if metadata.get("version_hash") != "PENDING":
        diagnostics.append(_diagnostic("VERSION_HASH_NOT_PENDING", "draft version_hash must be PENDING", "version_hash"))

    artifact_id = metadata.get("id")
    parent_hash = metadata.get("parent_hash")
    if artifact_id == "TBD":
        if parent_hash != "":
            diagnostics.append(_diagnostic("PARENT_HASH_FOR_NEW_DRAFT", "new drafts must use empty parent_hash", "parent_hash"))
    elif isinstance(artifact_id, str):
        expected_re = _REQ_ID_RE if artifact_type == "REQ" else _UC_ID_RE
        if not expected_re.match(artifact_id):
            diagnostics.append(_diagnostic("ID_PREFIX_MISMATCH", "artifact id must match path type or TBD", "id"))
        if not isinstance(parent_hash, str) or not _HASH_RE.match(parent_hash):
            diagnostics.append(_diagnostic("PARENT_HASH_REQUIRED_FOR_REVISION", "revision drafts require sha256 parent_hash", "parent_hash"))
    else:
        diagnostics.append(_diagnostic("ID_TYPE", "id must be a string", "id"))

    rationale = metadata.get("rationale")
    if not isinstance(rationale, str) or not rationale.strip():
        diagnostics.append(_diagnostic("RATIONALE_REQUIRED", "rationale must be a non-empty string", "rationale"))

    linked_nodes = metadata.get("linked_nodes")
    if not isinstance(linked_nodes, list):
        diagnostics.append(_diagnostic("LINKED_NODES_TYPE", "linked_nodes must be a list", "linked_nodes"))
    else:
        for node in linked_nodes:
            if not isinstance(node, str) or not _LINK_RE.match(node):
                diagnostics.append(_diagnostic("LINKED_NODE_SYNTAX", "linked nodes must use [[REQ-###]] or [[UC-###]]", "linked_nodes"))
                break
    return diagnostics


def _validate_canonical_metadata(metadata: dict[str, Any], body: str) -> list[dict[str, str]]:
    diagnostics: list[dict[str, str]] = []
    required = {"id", "schema_version", "status", "rationale", "linked_nodes"}
    allowed = required | {"parent_hash", "version_hash"}
    for field in sorted(required - set(metadata)):
        diagnostics.append(_diagnostic("CANONICAL_FIELD_MISSING", f"missing canonical field {field}", field))
    for field in sorted(set(metadata) - allowed):
        diagnostics.append(_diagnostic("CANONICAL_UNSUPPORTED_FIELD", f"unsupported canonical metadata field {field}", field))
    if metadata.get("schema_version") != "1.0":
        diagnostics.append(_diagnostic("SCHEMA_VERSION_UNSUPPORTED", "schema_version must be 1.0", "schema_version"))
    if metadata.get("status") not in {"DRAFT", "BASELINED"}:
        diagnostics.append(_diagnostic("CANONICAL_STATUS_UNSUPPORTED", "status must be DRAFT or BASELINED", "status"))
    artifact_id = metadata.get("id")
    if not isinstance(artifact_id, str) or not (artifact_id == "TBD" or _REQ_ID_RE.match(artifact_id) or _UC_ID_RE.match(artifact_id)):
        diagnostics.append(_diagnostic("CANONICAL_ID_INVALID", "id must be TBD, REQ-###, or UC-###", "id"))
    rationale = metadata.get("rationale")
    if not isinstance(rationale, str) or not rationale.strip():
        diagnostics.append(_diagnostic("RATIONALE_REQUIRED", "rationale must be a non-empty string", "rationale"))
    linked_nodes = metadata.get("linked_nodes")
    if not isinstance(linked_nodes, list):
        diagnostics.append(_diagnostic("LINKED_NODES_TYPE", "linked_nodes must be a list", "linked_nodes"))
    else:
        for node in linked_nodes:
            if not isinstance(node, str) or not _LINK_RE.match(node):
                diagnostics.append(_diagnostic("LINKED_NODE_SYNTAX", "linked nodes must use [[REQ-###]] or [[UC-###]]", "linked_nodes"))
                break
    if not isinstance(body, str) or not body.strip():
        diagnostics.append(_diagnostic("BODY_EMPTY", "artifact body must be non-empty", "body"))
    return diagnostics


def _validate_body(body: str, *, artifact_type: str) -> list[dict[str, str]]:
    diagnostics: list[dict[str, str]] = []
    if not body.strip():
        diagnostics.append(_diagnostic("BODY_EMPTY", "artifact body must be non-empty", "body"))
        return diagnostics
    if artifact_type == "REQ":
        prose_lines = [line for line in body.splitlines() if line.strip() and not _is_bullet_line(line)]
        prose = "\n".join(prose_lines)
        if _REQ_CONJUNCTION_RE.search(prose):
            diagnostics.append(_diagnostic("REQ_ATOMICITY_CONJUNCTION", "requirement body contains banned conjunction", "body"))
        if _REQ_SUBJECTIVE_RE.search(prose):
            diagnostics.append(_diagnostic("REQ_SUBJECTIVE_VOCABULARY", "requirement body contains subjective vocabulary", "body"))
    elif artifact_type == "UC" and _word_count(body) > 500:
        diagnostics.append(_diagnostic("UC_BODY_WORD_LIMIT", "use-case body exceeds 500 words", "body"))
    return diagnostics


def _hash_preview_result(
    *,
    ok: bool,
    version_hash: str | None,
    canonical_serialization: str | None,
    diagnostics: list[dict[str, str]],
    staging_body_read: bool,
) -> dict[str, Any]:
    return {
        "ok": ok,
        "version_hash": version_hash,
        "canonical_serialization": canonical_serialization,
        "diagnostics": diagnostics,
        "staging_body_read": staging_body_read,
        "active_vault_read": False,
        "active_vault_write": False,
        "protected_active_body_read": False,
        "baseline_promotion": False,
        "rtm_generation": False,
        "drift_decision": False,
    }


def _draft_result(
    *,
    status: str,
    written: bool,
    relative_path: Path,
    diagnostics: list[dict[str, str]],
    lint: dict[str, Any],
) -> dict[str, Any]:
    return {
        "status": status,
        "written": written,
        "relative_path": relative_path.as_posix(),
        "diagnostics": diagnostics,
        "lint": lint,
        "max_self_remediation_attempts": 3,
        "active_vault_read": False,
        "active_vault_write": False,
        "protected_active_body_read": False,
        "hitl_approval_capture": False,
        "baseline_promotion": False,
    }


def _normalize_artifact_type(artifact_type: str) -> str:
    aliases = {
        "REQ": "REQ",
        "REQUIREMENT": "REQ",
        "REQUIREMENTS": "REQ",
        "UC": "UC",
        "USE_CASE": "UC",
        "USE_CASES": "UC",
        "USE-CASE": "UC",
        "USE-CASES": "UC",
    }
    key = str(artifact_type).strip().upper().replace(" ", "_")
    if key not in aliases:
        raise ValueError("artifact_type must be REQ or UC")
    return aliases[key]


def _slugify(title: str) -> str:
    words = re.findall(r"[a-z0-9]+", str(title).casefold())
    return "-".join(words)


def _validate_slug(slug: str) -> str:
    normalized = str(slug).removesuffix(".md")
    if not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", normalized):
        raise ValueError("filename_slug must be lowercase alphanumeric hyphen text without path separators")
    if ".." in normalized or "/" in normalized or "\\" in normalized:
        raise ValueError("filename_slug must not contain path traversal")
    return normalized


def _yaml_quote(value: Any) -> str:
    return json.dumps(str(value), ensure_ascii=False)


def _lint_result(
    *,
    ok: bool,
    artifact_type: str,
    schema_version: str | None,
    diagnostics: list[dict[str, str]],
    body_word_count: int,
    staging_body_read: bool,
) -> dict[str, Any]:
    return {
        "ok": ok,
        "diagnostic_format": "BLK_REQ_LINTER_JSON_V1",
        "artifact_type": artifact_type,
        "schema_version": schema_version,
        "diagnostics": diagnostics,
        "body_word_count": body_word_count,
        "staging_body_read": staging_body_read,
        "active_vault_read": False,
        "protected_active_body_read": False,
        "active_vault_write": False,
        "rtm_generated": False,
        "beo_published": False,
    }


def _diagnostic(code: str, message: str, field: str) -> dict[str, str]:
    return {"code": code, "message": message, "field": field}


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _is_bullet_line(line: str) -> bool:
    stripped = line.lstrip()
    return stripped.startswith(("- ", "* ")) or bool(re.match(r"\d+\.\s+", stripped))


def _word_count(body: str) -> int:
    return len(_WORD_RE.findall(body))


def _scan_for_authority_laundering(value: Any, path: str = "contract") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            key_path = f"{path}.{key}"
            if path not in {"contract.side_effect_flags"}:
                errors.extend(_scan_text(str(key), key_path))
            errors.extend(_scan_for_authority_laundering(nested, key_path))
    elif isinstance(value, (list, tuple, set)):
        for index, nested in enumerate(value):
            nested_path = f"{path}[{index}]"
            if path == "contract.denied_authorities":
                continue
            errors.extend(_scan_for_authority_laundering(nested, nested_path))
    elif isinstance(value, str):
        errors.extend(_scan_text(value, path))
    return errors


def _scan_text(text: str, path: str) -> list[str]:
    compact = _compact(text)
    safe = compact
    for token in _FORBIDDEN_COMPACT_WORDING:
        safe = safe.replace(f"no{token}", "")
        safe = safe.replace(f"not{token}", "")
    return [f"forbidden authority wording at {path}: {token}" for token in sorted(_FORBIDDEN_COMPACT_WORDING) if token in safe]


def _compact(text: str) -> str:
    return "".join(char for char in str(text).casefold() if char.isalnum())


def _unique(items: list[str]) -> list[str]:
    seen = set()
    out: list[str] = []
    for item in items:
        if item not in seen:
            out.append(item)
            seen.add(item)
    return out


__all__ = [
    "BLK_REQ_DENIED_AUTHORITIES",
    "build_draft_artifact_text",
    "build_legislative_gateway_contract",
    "canonicalize_artifact_text",
    "compute_version_hash",
    "lint_artifact",
    "lint_artifact_text",
    "parse_artifact_text",
    "preview_staging_version_hash",
    "validate_legislative_gateway_contract",
    "write_staging_draft",
]
