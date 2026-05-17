"""BLK-SYSTEM-207..209 Python adapter closure fixtures.

These builders close the Python adapter layer as a bounded packaging and report
normalization surface. They do not invoke blk-pipe, start subprocesses, execute
Codex, mutate source/Git state, read protected bodies, contact networks, or grant
runtime authority. Adapter evidence remains evidence only; any real blk-pipe
payload still requires separate exact authority outside these packages.
"""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any

from blk_authority_smuggling import (
    compact_authority_text,
    decoded_authority_variants,
    scan_for_authority_laundering,
)
from blk_pipe_bounded_enforcement_204_206 import DEFAULT_206_PACKAGE_HASH

SURFACE = "Python adapter layer"
UPSTREAM_BLK206_RECONCILIATION_HASH = DEFAULT_206_PACKAGE_HASH
NEXT_FRONTIER = "NEXT_FRONTIER_PYTHON_ADAPTER_CLOSED_VALIDATION_PROFILES_SELECTION_NOT_GRANTED"

DENIED_AUTHORITIES = (
    "BROAD_BLK_PIPE_DISPATCH",
    "PYTHON_ADAPTER_BLK_PIPE_DISPATCH_AUTHORITY",
    "BLK_PIPE_RUNTIME_BEYOND_SEPARATE_EXACT_PAYLOAD_AUTHORITY",
    "LIVE_CODEX_DISPATCH",
    "TACTICAL_LLM_DISPATCH",
    "BLK_TEST_MCP_PRODUCTION_RUNTIME",
    "BEB_DISPATCH",
    "BEO_CLOSEOUT_EXECUTION",
    "BEO_PUBLICATION_SIGNING_STORAGE_LEDGER_REUSE",
    "ROLLBACK_REVOCATION_SUPERSESSION_EXECUTION",
    "RTM_GENERATION",
    "PRODUCTION_BLK_LINK",
    "RTM_DRIFT_REJECTION",
    "RTM_COVERAGE_TRUTH",
    "ACTIVE_VAULT_COMPARISON",
    "PROTECTED_BLK_REQ_BODY_READ_COPY_PARSE_HASH_SCAN",
    "TARGET_SOURCE_GIT_MUTATION",
    "PACKAGE_MANAGER_NETWORK_MODEL_BROWSER_CYBER_TOOLING",
    "PRODUCTION_ISOLATION_CLAIM",
    "AUTHORITY_FROM_PASS_OR_ADAPTER_REPORT_EVIDENCE",
)

REQUIRED_FALSE_SIDE_EFFECT_FLAGS = (
    "blk_pipe_dispatch_authorized",
    "blk_pipe_runtime_authorized",
    "python_adapter_runtime_authorized",
    "runtime_tooling_authorized",
    "live_codex_dispatch_authorized",
    "tactical_llm_dispatch_authorized",
    "production_blk_test_mcp_authorized",
    "beb_dispatch_authorized",
    "beo_closeout_execution_authorized",
    "beo_publication_authorized",
    "rollback_revocation_supersession_authorized",
    "rtm_generation_authorized",
    "production_blk_link_authorized",
    "rtm_drift_rejection_authorized",
    "rtm_coverage_truth_authorized",
    "active_vault_comparison_authorized",
    "protected_body_access_authorized",
    "target_source_git_mutation_authorized",
    "package_network_model_browser_cyber_tooling_authorized",
    "production_isolation_claimed",
)

REVIEWED_SURFACE_FILES = (
    "python/blk_pipe_adapter.py",
    "python/test_blk_pipe_adapter.py",
)

BOUNDED_ADAPTER_SURFACES = (
    "payload_packaging",
    "pre_invocation_validation",
    "return_code_status_taxonomy",
    "report_field_normalization",
    "temporary_payload_file_cleanup",
    "ssh_agent_environment_scrub",
)

ADAPTER_CONTRACT = {
    "payload_packaging": "deterministic_local_packaging_only",
    "pre_invocation_validation": "fail_fast_local_checks_before_any_subprocess",
    "blk_pipe_invocation": "requires_separate_exact_payload_authority",
    "health_check": "availability_signal_not_authority",
    "validation_result_meaning": "PASS_is_diagnostic_evidence_not_runtime_or_mutation_authority",
    "report_fields": "normalized_evidence_only_not_authority_grants",
    "l2_packet_handling": "opaque_payload_forwarding_not_protected_body_read_authority",
    "environment_policy": "scrub_high_risk_ssh_agent_variables_only_not_sandbox_or_production_isolation",
}

CALLER_CONTROLLED_FIELDS = ("operator_notes", "caller_supplied_evidence_refs")
EXACT_REVIEW_FINDINGS = (
    "BLK-pipe adapter wraps payload files and report fields; it is not an authority source.",
    "Actual blk-pipe execution still requires separate exact payload authority and operator decision.",
    "Adapter status, PASS output, stderr, and raw reports are diagnostic evidence only.",
)
EXACT_OPERATOR_NOTES_207 = (
    "Python adapter closure records existing packaging/report behavior only.",
    "No live BLK-pipe, Codex, BLK-test MCP, RTM, BEO, protected-body, tooling, or mutation authority is granted.",
)
EXACT_OPERATOR_NOTES_208 = (
    "Adapter contract is closed as non-authorizing packaging evidence.",
    "No adapter field may become an authority grant field.",
)
EXACT_OPERATOR_NOTES_209 = (
    "Python adapter layer is boxed as a non-authorizing packaging surface.",
    "Validation profiles are selected as the next component surface only; no authority is granted here.",
)

FORBIDDEN_CALLER_COMPACT_TOKENS = {
    "blkpipeapproved",
    "blkpipesuccess",
    "blkpipedispatchauthorized",
    "blkpipeinvocationauthorized",
    "blkpipeexecutionauthorized",
    "pythonadapterauthority",
    "adapterdispatchauthority",
    "runtimeapproval",
    "runtimeapproved",
    "runtimeexecutionauthorized",
    "livecodexexecutionallowed",
    "codexapproval",
    "blktestpassapproval",
    "approvalinherited",
    "approvedforproduction",
    "approvalforproduction",
    "allowedforproduction",
    "permittedforproduction",
    "productionisolationclaimed",
    "productionisolationenforced",
    "productionisolationisenforced",
    "beopublicationauthorized",
    "authoritativebeopublication",
    "publishbeo",
    "rtmgeneration",
    "rtmgenerated",
    "rtmdriftrejection",
    "coveragetruth",
    "activevaulthashcomparison",
    "docsactive",
    "docsrequirementsactive",
    "docsrequirements",
    "docsusecases",
    "protectedbodytext",
    "blkreqbody",
    "reqbody",
    "bodytext",
    "systemshall",
    "curlhttps",
    "wgethttps",
    "pipinstall",
    "npminstall",
    "uvpipinstall",
    "goget",
    "privatekey",
    "apikey",
    "githubpat",
}

PACKAGE_207_KEYS = {
    "sprint_id",
    "surface",
    "status",
    "upstream_blk206_hash",
    "reviewed_surface_files",
    "bounded_adapter_surfaces",
    "review_findings",
    "denied_authorities",
    "operator_notes",
    "caller_supplied_evidence_refs",
    "package_hash",
    *REQUIRED_FALSE_SIDE_EFFECT_FLAGS,
}

PACKAGE_208_KEYS = {
    "sprint_id",
    "surface",
    "status",
    "upstream_207_package_hash",
    "adapter_contract",
    "authority_grant_fields",
    "side_effect_obligations",
    "denied_authorities",
    "operator_notes",
    "caller_supplied_evidence_refs",
    "package_hash",
    *REQUIRED_FALSE_SIDE_EFFECT_FLAGS,
}

PACKAGE_209_KEYS = {
    "sprint_id",
    "surface",
    "status",
    "upstream_207_package_hash",
    "upstream_208_package_hash",
    "next_frontier",
    "reconciliation_findings",
    "denied_authorities",
    "operator_notes",
    "caller_supplied_evidence_refs",
    "package_hash",
    *REQUIRED_FALSE_SIDE_EFFECT_FLAGS,
}


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def canonical_package_hash(package: dict[str, Any]) -> str:
    body = copy.deepcopy(package)
    body.pop("package_hash", None)
    return "sha256:" + hashlib.sha256(_canonical_bytes(body)).hexdigest()


def _false_flags() -> dict[str, bool]:
    return {flag: False for flag in REQUIRED_FALSE_SIDE_EFFECT_FLAGS}


def _validate_exact_keys(package: dict[str, Any], expected: set[str], label: str) -> list[str]:
    keys = set(package)
    if keys != expected:
        return [f"{label} keys must be exact; missing={sorted(expected - keys)} extra={sorted(keys - expected)}"]
    return []


def _validate_denied_authorities(package: dict[str, Any]) -> list[str]:
    denied = package.get("denied_authorities")
    if not isinstance(denied, list):
        return ["denied_authorities must be a list"]
    errors: list[str] = []
    if denied != list(DENIED_AUTHORITIES):
        errors.append("denied_authorities must match exact ordered list")
    if len(denied) != len(set(denied)):
        errors.append("denied_authorities must not contain duplicates")
    if not all(isinstance(item, str) for item in denied):
        errors.append("denied_authorities must contain only strings")
    return errors


def _validate_false_flags(package: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for flag in REQUIRED_FALSE_SIDE_EFFECT_FLAGS:
        if package.get(flag) is not False:
            errors.append(f"{flag} must be explicit false")
    return errors


def _validate_hash(package: dict[str, Any], expected_hash: str | None = None) -> list[str]:
    errors: list[str] = []
    actual = package.get("package_hash")
    calculated = canonical_package_hash(package)
    if actual != calculated:
        errors.append("package_hash must equal canonical package hash")
    if expected_hash is not None and actual != expected_hash:
        errors.append(f"package_hash must match canonical default {expected_hash}")
    return errors


def _scan_for_extra_tokens(value: Any, path: str) -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key)
            for key_variant in decoded_authority_variants(key_text):
                compact = compact_authority_text(key_variant)
                for token in FORBIDDEN_CALLER_COMPACT_TOKENS:
                    if token in compact:
                        errors.append(f"{path}.{key_text} contains forbidden adapter authority/protected token {token!r}")
            errors.extend(_scan_for_extra_tokens(nested, f"{path}.{key_text}"))
    elif isinstance(value, (list, tuple, set)):
        for index, nested in enumerate(value):
            errors.extend(_scan_for_extra_tokens(nested, f"{path}[{index}]"))
    elif isinstance(value, str):
        for variant in decoded_authority_variants(value):
            compact = compact_authority_text(variant)
            lowered = variant.lower()
            for token in FORBIDDEN_CALLER_COMPACT_TOKENS:
                if token in compact:
                    errors.append(f"{path} contains forbidden adapter authority/protected token {token!r}")
            if "authorization=" in lowered or "api_key" in lowered or "github_pat" in lowered:
                errors.append(f"{path} contains secret-like tooling text")
    return errors


def _scan_caller_controlled(package: dict[str, Any]) -> list[str]:
    caller_payload = {field: package.get(field) for field in CALLER_CONTROLLED_FIELDS if field in package}
    errors = scan_for_authority_laundering(caller_payload, "caller_controlled")
    errors.extend(_scan_for_extra_tokens(caller_payload, "caller_controlled"))
    return errors


def _base_207() -> dict[str, Any]:
    return {
        "sprint_id": "BLK-SYSTEM-207",
        "surface": SURFACE,
        "status": "PYTHON_ADAPTER_SURFACE_REVIEW_READY_NOT_AUTHORITY",
        "upstream_blk206_hash": UPSTREAM_BLK206_RECONCILIATION_HASH,
        "reviewed_surface_files": list(REVIEWED_SURFACE_FILES),
        "bounded_adapter_surfaces": list(BOUNDED_ADAPTER_SURFACES),
        "review_findings": list(EXACT_REVIEW_FINDINGS),
        "denied_authorities": list(DENIED_AUTHORITIES),
        "operator_notes": list(EXACT_OPERATOR_NOTES_207),
        "caller_supplied_evidence_refs": {},
        **_false_flags(),
    }


def _base_208(upstream_207_hash: str) -> dict[str, Any]:
    return {
        "sprint_id": "BLK-SYSTEM-208",
        "surface": SURFACE,
        "status": "PYTHON_ADAPTER_CONTRACT_READY_NOT_DISPATCH_AUTHORITY",
        "upstream_207_package_hash": upstream_207_hash,
        "adapter_contract": copy.deepcopy(ADAPTER_CONTRACT),
        "authority_grant_fields": [],
        "side_effect_obligations": _false_flags(),
        "denied_authorities": list(DENIED_AUTHORITIES),
        "operator_notes": list(EXACT_OPERATOR_NOTES_208),
        "caller_supplied_evidence_refs": {},
        **_false_flags(),
    }


def _base_209(upstream_207_hash: str, upstream_208_hash: str) -> dict[str, Any]:
    return {
        "sprint_id": "BLK-SYSTEM-209",
        "surface": SURFACE,
        "status": "PYTHON_ADAPTER_RECONCILED_CLEAN",
        "upstream_207_package_hash": upstream_207_hash,
        "upstream_208_package_hash": upstream_208_hash,
        "next_frontier": NEXT_FRONTIER,
        "reconciliation_findings": [
            "BLK_SYSTEM_207_PYTHON_ADAPTER_SURFACE_REVIEW_READY",
            "BLK_SYSTEM_208_PYTHON_ADAPTER_CONTRACT_READY",
            "Python adapter layer closed as a bounded non-authorizing packaging surface.",
            "validation profiles remain the next selected surface, not granted authority",
        ],
        "denied_authorities": list(DENIED_AUTHORITIES),
        "operator_notes": list(EXACT_OPERATOR_NOTES_209),
        "caller_supplied_evidence_refs": {},
        **_false_flags(),
    }


def _with_hash(package: dict[str, Any]) -> dict[str, Any]:
    finalized = copy.deepcopy(package)
    finalized["package_hash"] = canonical_package_hash(finalized)
    return finalized


DEFAULT_207_PACKAGE_HASH = canonical_package_hash(_base_207())
DEFAULT_208_PACKAGE_HASH = canonical_package_hash(_base_208(DEFAULT_207_PACKAGE_HASH))
DEFAULT_209_PACKAGE_HASH = canonical_package_hash(_base_209(DEFAULT_207_PACKAGE_HASH, DEFAULT_208_PACKAGE_HASH))


def build_207_adapter_surface_review_package() -> dict[str, Any]:
    return _with_hash(_base_207())


def validate_207_adapter_surface_review_package(package: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(package, dict):
        return ["BLK-SYSTEM-207 package must be an object"]
    errors.extend(_validate_exact_keys(package, PACKAGE_207_KEYS, "BLK-SYSTEM-207 package"))
    if package.get("sprint_id") != "BLK-SYSTEM-207":
        errors.append("sprint_id must be BLK-SYSTEM-207")
    if package.get("surface") != SURFACE:
        errors.append("surface must be Python adapter layer")
    if package.get("status") != "PYTHON_ADAPTER_SURFACE_REVIEW_READY_NOT_AUTHORITY":
        errors.append("status must remain review-ready not authority")
    if package.get("upstream_blk206_hash") != UPSTREAM_BLK206_RECONCILIATION_HASH:
        errors.append("upstream BLK-206 hash must be canonical")
    if package.get("reviewed_surface_files") != list(REVIEWED_SURFACE_FILES):
        errors.append("reviewed_surface_files must match exact adapter file list")
    if package.get("bounded_adapter_surfaces") != list(BOUNDED_ADAPTER_SURFACES):
        errors.append("bounded_adapter_surfaces must match exact bounded surface list")
    if package.get("review_findings") != list(EXACT_REVIEW_FINDINGS):
        errors.append("review_findings must match exact non-authorizing adapter review findings")
    errors.extend(_validate_denied_authorities(package))
    errors.extend(_validate_false_flags(package))
    errors.extend(_scan_caller_controlled(package))
    errors.extend(_validate_hash(package, DEFAULT_207_PACKAGE_HASH))
    return errors


def build_208_adapter_contract_package(review_package: dict[str, Any]) -> dict[str, Any]:
    errors = validate_207_adapter_surface_review_package(review_package)
    if errors or review_package.get("package_hash") != DEFAULT_207_PACKAGE_HASH:
        raise ValueError("BLK-SYSTEM-208 requires exact canonical BLK-SYSTEM-207 package")
    return _with_hash(_base_208(DEFAULT_207_PACKAGE_HASH))


def validate_208_adapter_contract_package(package: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(package, dict):
        return ["BLK-SYSTEM-208 package must be an object"]
    errors.extend(_validate_exact_keys(package, PACKAGE_208_KEYS, "BLK-SYSTEM-208 package"))
    if package.get("sprint_id") != "BLK-SYSTEM-208":
        errors.append("sprint_id must be BLK-SYSTEM-208")
    if package.get("surface") != SURFACE:
        errors.append("surface must be Python adapter layer")
    if package.get("status") != "PYTHON_ADAPTER_CONTRACT_READY_NOT_DISPATCH_AUTHORITY":
        errors.append("status must remain contract-ready not dispatch authority")
    if package.get("upstream_207_package_hash") != DEFAULT_207_PACKAGE_HASH:
        errors.append("upstream_207_package_hash must be canonical BLK-SYSTEM-207 hash")
    if package.get("adapter_contract") != ADAPTER_CONTRACT:
        errors.append("adapter_contract must match exact non-authorizing adapter contract")
    if package.get("authority_grant_fields") != []:
        errors.append("authority_grant_fields must be an empty list")
    if package.get("side_effect_obligations") != _false_flags():
        errors.append("side_effect_obligations must require every side effect flag explicit false")
    errors.extend(_validate_denied_authorities(package))
    errors.extend(_validate_false_flags(package))
    errors.extend(_scan_caller_controlled(package))
    errors.extend(_validate_hash(package, DEFAULT_208_PACKAGE_HASH))
    return errors


def build_209_adapter_reconciliation_package(review_package: dict[str, Any], contract_package: dict[str, Any]) -> dict[str, Any]:
    review_errors = validate_207_adapter_surface_review_package(review_package)
    contract_errors = validate_208_adapter_contract_package(contract_package)
    if review_errors or contract_errors:
        raise ValueError("BLK-SYSTEM-209 requires exact canonical 207 and 208 packages")
    if review_package.get("package_hash") != DEFAULT_207_PACKAGE_HASH or contract_package.get("package_hash") != DEFAULT_208_PACKAGE_HASH:
        raise ValueError("BLK-SYSTEM-209 requires default canonical upstream hashes")
    return _with_hash(_base_209(DEFAULT_207_PACKAGE_HASH, DEFAULT_208_PACKAGE_HASH))


def validate_209_adapter_reconciliation_package(package: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(package, dict):
        return ["BLK-SYSTEM-209 package must be an object"]
    errors.extend(_validate_exact_keys(package, PACKAGE_209_KEYS, "BLK-SYSTEM-209 package"))
    if package.get("sprint_id") != "BLK-SYSTEM-209":
        errors.append("sprint_id must be BLK-SYSTEM-209")
    if package.get("surface") != SURFACE:
        errors.append("surface must be Python adapter layer")
    if package.get("status") != "PYTHON_ADAPTER_RECONCILED_CLEAN":
        errors.append("status must be clean reconciliation")
    if package.get("upstream_207_package_hash") != DEFAULT_207_PACKAGE_HASH:
        errors.append("upstream_207_package_hash must be canonical")
    if package.get("upstream_208_package_hash") != DEFAULT_208_PACKAGE_HASH:
        errors.append("upstream_208_package_hash must be canonical")
    if package.get("next_frontier") != NEXT_FRONTIER:
        errors.append("next frontier must remain not granted")
    expected_findings = _base_209(DEFAULT_207_PACKAGE_HASH, DEFAULT_208_PACKAGE_HASH)["reconciliation_findings"]
    if package.get("reconciliation_findings") != expected_findings:
        errors.append("reconciliation_findings must match exact adapter closure findings")
    errors.extend(_validate_denied_authorities(package))
    errors.extend(_validate_false_flags(package))
    errors.extend(_scan_caller_controlled(package))
    errors.extend(_validate_hash(package, DEFAULT_209_PACKAGE_HASH))
    return errors


def build_python_adapter_closure_packages() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    review = build_207_adapter_surface_review_package()
    contract = build_208_adapter_contract_package(review)
    reconciliation = build_209_adapter_reconciliation_package(review, contract)
    return review, contract, reconciliation
