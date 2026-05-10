"""Fixture-only Kuronode TypeScript Power-of-Ten static profile.

This module evaluates caller-supplied TypeScript/TSX descriptors against a
small deterministic subset of BLK-058. It does not scan live Kuronode files,
execute TypeScript tooling, invoke package managers, start BLK-test MCP, start
Codex, mutate source/Git, publish BEOs, generate RTM, or read protected BLK-req
bodies.
"""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from pathlib import PurePosixPath
from typing import Any

from authoritative_beo_publication_authority_request import (
    _canonical_hash,
    _contains_forbidden_text,
    _contains_protected_body_reference,
    _enforce_allowed_keys,
    _required_hash,
    _required_string,
    _scan_nested,
    _validate_trace_artifacts,
)

PASS_STATUS = "KURONODE_POWER_OF_TEN_STATIC_PROFILE_PASS_FIXTURE_ONLY"
BLOCKED_STATUS = "KURONODE_POWER_OF_TEN_STATIC_PROFILE_BLOCKED_FIXTURE_ONLY"
PROFILE_NAME = "kuronode-power-of-ten-static"
REQUEST_STATUS = "KURONODE_POWER_OF_TEN_STATIC_PROFILE_FIXTURE_ONLY"
MAX_FUNCTION_LINES = 60

EXACT_EXCLUDED_AUTHORITIES = {
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
}

_REQUEST_KEYS = {
    "profile_name",
    "request_status",
    "request_id",
    "operator_identity",
    "trace_artifacts",
    "source_bundle_id",
    "source_bundle_hash",
    "excluded_authorities",
    "operator_note",
}
_FILE_KEYS = {"path", "language", "content"}
_TS_EXTENSIONS = (".ts", ".tsx")
_TS_LANGUAGES = {"typescript", "tsx"}
_AUTHORITY_TEXT_RE = re.compile(
    r"\b(production\s+blk[-_\s]*test\s+mcp|generic\s+blk[-_\s]*test\s+mcp|live\s+codex|"
    r"codex\s+execution\s+authorized|source\s+mutation\s+authorized|git\s+mutation\s+authorized|"
    r"package\s+manager\s+authorized|package\s+manager|npm\s+install|pnpm\s+install|yarn\s+install|"
    r"\b(?:tsc|eslint|typecheck|linter)\b|live\s+kuronode\s+(?:repository\s+)?scan|"
    r"beo\s+publication\s+(?:authorized|authorised|approved|greenlit|allowed|permitted)|"
    r"authoritative\s+beo\s+publication|rtm\s+generation|drift\s+rejection|protected\s+body\s+read)\b",
    re.IGNORECASE,
)


def evaluate_kuronode_power_of_ten_static_profile(*, files: list[dict[str, Any]], request: dict[str, Any]) -> dict[str, Any]:
    """Evaluate fixture descriptors against the BLK-058 static profile."""

    validated_files = _validate_files(files)
    validated_request = _validate_request(request, validated_files)

    findings: list[dict[str, Any]] = []
    for file_desc in validated_files:
        findings.extend(_evaluate_file(file_desc))

    result = {
        "profile_status": BLOCKED_STATUS if findings else PASS_STATUS,
        "profile_name": PROFILE_NAME,
        "request_id": validated_request["request_id"],
        "operator_identity": validated_request["operator_identity"],
        "source_bundle_id": validated_request["source_bundle_id"],
        "source_bundle_hash": validated_request["source_bundle_hash"],
        "trace_artifacts": validated_request["trace_artifacts"],
        "checked_file_count": len(validated_files),
        "findings": findings,
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
        "live_kuronode_scan_performed": False,
        "source_mutation_performed": False,
        "blk_test_mcp_started": False,
        "codex_started": False,
        "package_manager_invoked": False,
        "network_accessed": False,
        "protected_body_read": False,
        "beo_published": False,
        "rtm_generated": False,
        "production_sandbox_claimed": False,
    }
    result["profile_hash"] = _canonical_hash({key: value for key, value in result.items() if key != "profile_hash"})
    return result


def _validate_request(request: dict[str, Any], files: list[dict[str, str]]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("request must be a dictionary")
    _scan_nested({key: value for key, value in request.items() if key != "excluded_authorities"}, "request")
    _scan_for_authority_text(request, "request")
    _enforce_allowed_keys(request, _REQUEST_KEYS, "request")
    if _required_string(request.get("profile_name"), "profile_name") != PROFILE_NAME:
        raise ValueError("profile_name must be kuronode-power-of-ten-static")
    if _required_string(request.get("request_status"), "request_status") != REQUEST_STATUS:
        raise ValueError("request_status must be KURONODE_POWER_OF_TEN_STATIC_PROFILE_FIXTURE_ONLY")
    _validate_excluded_authorities(request.get("excluded_authorities"))
    source_bundle_hash = _required_hash(request.get("source_bundle_hash"), "source_bundle_hash")
    if source_bundle_hash != _source_bundle_hash(files):
        raise ValueError("source_bundle_hash does not match submitted file descriptors")
    return {
        "request_id": _required_string(request.get("request_id"), "request_id"),
        "operator_identity": _required_string(request.get("operator_identity"), "operator_identity"),
        "source_bundle_id": _required_string(request.get("source_bundle_id"), "source_bundle_id"),
        "source_bundle_hash": source_bundle_hash,
        "trace_artifacts": _validate_trace_artifacts(request.get("trace_artifacts")),
    }


def _source_bundle_hash(files: list[dict[str, str]]) -> str:
    stable = json.dumps(deepcopy(files), sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(stable).hexdigest()


def _validate_excluded_authorities(excluded: Any) -> None:
    if (
        not isinstance(excluded, list)
        or not all(isinstance(item, str) for item in excluded)
        or set(excluded) != EXACT_EXCLUDED_AUTHORITIES
        or len(excluded) != len(EXACT_EXCLUDED_AUTHORITIES)
    ):
        raise ValueError("excluded_authorities must match exact denied authority set")


def _validate_files(files: list[dict[str, Any]]) -> list[dict[str, str]]:
    if not isinstance(files, list) or not files:
        raise ValueError("files must be a non-empty list")
    result: list[dict[str, str]] = []
    seen: set[str] = set()
    for file_desc in files:
        if not isinstance(file_desc, dict):
            raise ValueError("file descriptor must be a dictionary")
        _enforce_allowed_keys(file_desc, _FILE_KEYS, "file descriptor")
        path = _validate_file_path(file_desc.get("path"))
        if path in seen:
            raise ValueError("duplicate file path")
        seen.add(path)
        language = _required_string(file_desc.get("language"), "language").lower()
        if language not in _TS_LANGUAGES:
            raise ValueError("language must be typescript or tsx")
        content = _required_string(file_desc.get("content"), "content")
        result.append({"path": path, "language": language, "content": content})
    return result


def _validate_file_path(value: Any) -> str:
    path = _required_string(value, "path").replace("\\", "/")
    if _contains_protected_body_reference(path):
        raise ValueError("file path rejects protected BLK-req body reference")
    pure = PurePosixPath(path)
    if pure.is_absolute() or ".." in pure.parts or str(pure) != path or path.startswith("./"):
        raise ValueError("file path must be a normalized relative path")
    if not path.endswith(_TS_EXTENSIONS):
        raise ValueError("file path must target .ts or .tsx")
    return path


def _evaluate_file(file_desc: dict[str, str]) -> list[dict[str, Any]]:
    path = file_desc["path"]
    content = file_desc["content"]
    findings: list[dict[str, Any]] = []
    findings.extend(_scan_text_authority(path, content))
    findings.extend(_scan_recursion(path, content))
    findings.extend(_scan_pattern(path, content, r"while\s*\(\s*true\s*\)", "UNBOUNDED_WHILE_TRUE_FORBIDDEN"))
    findings.extend(_scan_pattern(path, content, r"\beval\s*\(|\bnew\s+Function\s*\(", "DYNAMIC_CODE_EXECUTION_FORBIDDEN"))
    findings.extend(_scan_pattern(path, content, r"\bvar\s+", "VAR_DECLARATION_FORBIDDEN"))
    findings.extend(_scan_pattern(path, content, r"(?::\s*any\b|<\s*any\s*>|\bas\s+any\b)", "EXPLICIT_ANY_FORBIDDEN"))
    findings.extend(_scan_pattern(path, content, r"\bvoid\s+[A-Za-z_$][\w$]*\s*\(", "FLOATING_PROMISE_FORBIDDEN"))
    findings.extend(_scan_pattern(path, content, r"[A-Za-z0-9_\]\)]!\.", "NON_NULL_ASSERTION_FORBIDDEN"))
    findings.extend(_scan_function_lengths(path, content))
    findings.extend(_scan_lifecycle_cleanup(path, content))
    return findings


def _scan_text_authority(path: str, content: str) -> list[dict[str, Any]]:
    findings = []
    for line_no, line in enumerate(content.splitlines(), start=1):
        if _contains_protected_body_reference(line) or _AUTHORITY_TEXT_RE.search(line) or _contains_forbidden_text(line):
            findings.append(_finding(path, line_no, "AUTHORITY_LAUNDERING_TEXT_FORBIDDEN"))
    return findings


def _scan_recursion(path: str, content: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for match in re.finditer(r"(?:function\s+([A-Za-z_$][\w$]*)\s*\([^)]*\)\s*(?::[^\{]+)?\{|(?:const|let)\s+([A-Za-z_$][\w$]*)\s*=\s*\([^)]*\)\s*(?::[^=]+)?=>\s*\{)", content):
        name = match.group(1) or match.group(2)
        body_start = match.end()
        body_end = _find_matching_brace(content, match.end() - 1)
        body = content[body_start:body_end]
        if re.search(rf"\b{re.escape(name)}\s*\(", body):
            line_no = content[: match.start()].count("\n") + 1
            findings.append(_finding(path, line_no, "RECURSION_FORBIDDEN"))
    return findings


def _scan_pattern(path: str, content: str, pattern: str, rule: str) -> list[dict[str, Any]]:
    findings = []
    regex = re.compile(pattern)
    for line_no, line in enumerate(content.splitlines(), start=1):
        if regex.search(line):
            findings.append(_finding(path, line_no, rule))
    return findings


def _scan_function_lengths(path: str, content: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for match in re.finditer(
        r"(?:function\s+[A-Za-z_$][\w$]*\s*\([^)]*\)\s*(?::[^\{]+)?\{|(?:public\s+|private\s+|protected\s+|static\s+)?[A-Za-z_$][\w$]*\s*\([^)]*\)\s*(?::[^\{]+)?\{)",
        content,
    ):
        body_end = _find_matching_brace(content, match.end() - 1)
        function_text = content[match.start() : body_end + 1]
        physical_lines = [line for line in function_text.splitlines() if line.strip() and not line.strip().startswith("//")]
        if len(physical_lines) > MAX_FUNCTION_LINES:
            line_no = content[: match.start()].count("\n") + 1
            findings.append(_finding(path, line_no, "FUNCTION_TOO_LONG", {"line_count": len(physical_lines)}))
    return findings


def _scan_lifecycle_cleanup(path: str, content: str) -> list[dict[str, Any]]:
    lifecycle_patterns = [
        r"\bnew\s+Worker\s*\(",
        r"\bsetInterval\s*\(",
        r"\bsetTimeout\s*\(",
        r"\bnew\s+MutationObserver\s*\(",
        r"\bnew\s+ResizeObserver\s*\(",
        r"\bnew\s+IntersectionObserver\s*\(",
        r"\bnew\s+Parser\s*\(",
        r"\bnew\s+Tree\s*\(",
        r"\bnew\s+dia\.Paper\s*\(",
        r"\bnew\s+dia\.Cell\s*\(",
    ]
    cleanup_re = re.compile(r"\b(terminate|clearInterval|clearTimeout|disconnect|dispose|delete|remove|cleanup|teardown|destroy)\b")
    if not any(re.search(pattern, content) for pattern in lifecycle_patterns):
        return []
    content_without_comments = "\n".join(line for line in content.splitlines() if not line.strip().startswith("//"))
    if cleanup_re.search(content_without_comments):
        return []
    line_no = 1
    for index, line in enumerate(content.splitlines(), start=1):
        if any(re.search(pattern, line) for pattern in lifecycle_patterns):
            line_no = index
            break
    return [_finding(path, line_no, "LIFECYCLE_CLEANUP_REQUIRED")]


def _find_matching_brace(content: str, open_index: int) -> int:
    depth = 0
    for index in range(open_index, len(content)):
        char = content[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index
    return len(content) - 1


def _scan_for_authority_text(value: Any, label: str) -> None:
    if isinstance(value, dict):
        for item in value.values():
            _scan_for_authority_text(item, label)
    elif isinstance(value, list):
        for item in value:
            _scan_for_authority_text(item, label)
    elif isinstance(value, str):
        if _AUTHORITY_TEXT_RE.search(value):
            raise ValueError(f"{label} rejects authority-laundering text")


def _finding(path: str, line: int, rule: str, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    finding = {"path": path, "line": line, "rule": rule}
    if extra:
        finding.update(extra)
    return finding
