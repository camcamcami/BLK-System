"""BLK-SYSTEM-204..206 BLK-pipe bounded enforcement closure fixtures.

These builders produce deterministic evidence packages that close BLK-pipe as a
bounded, non-authorizing enforcement surface. They do not invoke BLK-pipe, run
validation profiles, mutate Git/source state, contact networks, or grant runtime
authority. Evidence is evidence only.
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

BLK203_BRIDGE_RECONCILIATION_HASH = "sha256:402c1620e40d3dfaa907af697670752fe7d8e3b394d0211d646b296d1fc99650"
SURFACE = "BLK-pipe blast shield"
NEXT_FRONTIER = "NEXT_FRONTIER_BLK_PIPE_CLOSED_NEXT_COMPONENT_SELECTION_NOT_GRANTED"

DENIED_AUTHORITIES = (
    "BROAD_BLK_PIPE_DISPATCH",
    "BLK_PIPE_RUNTIME_BEYOND_EXACT_APPROVED_PAYLOAD",
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
    "AUTHORITY_FROM_PASS_OR_DIAGNOSTIC_EVIDENCE",
)

REQUIRED_FALSE_SIDE_EFFECT_FLAGS = (
    "broad_dispatch_authorized",
    "blk_pipe_runtime_authorized",
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

BOUND_EVIDENCE_SURFACES = (
    "validation_profile_argv_evidence_only",
    "failure_class_denial_route_cleanup_status",
    "allowed_modified_and_new_file_allowlists",
    "diff_summary_and_trace_artifact_hashes",
    "engine_output_byte_cap_and_timeout_status",
)

SURFACE_FILES = (
    "internal/contracts/report.go",
    "internal/pipe/run.go",
    "internal/validationprofiles/profiles.go",
    "python/blk_pipe_adapter.py",
)

REPORT_EVIDENCE_CONTRACT = {
    "validation_profile_capabilities": "diagnostic_labels_only",
    "resolved_validation_argv": "repository_owned_structured_argv_evidence_only",
    "failure_class": "denial_taxonomy_not_permission",
    "denial_route": "fail_closed_route_not_permission",
    "cleanup_status": "post_run_evidence_not_production_isolation",
    "diff_summary": "bounded_change_summary_not_mutation_authority",
    "trace_artifacts": "metadata_hashes_only_not_protected_body_access",
}

CALLER_CONTROLLED_FIELDS = ("operator_notes", "caller_supplied_evidence_refs")
EXACT_OPERATOR_NOTES = (
    "BLK-pipe closure records existing bounded enforcement surfaces only.",
    "PASS or diagnostic evidence is not runtime, mutation, RTM, BEO, BLK-test MCP, or production-isolation authority.",
)

# Extra compact hostile probes beyond the shared scanner. Keep these module-local
# so fixture-owned denial constants remain usable while caller text is strict.
FORBIDDEN_CALLER_COMPACT_TOKENS = {
    "blkpipesuccess",
    "blkpiperuntimeapproved",
    "blkpipeapproved",
    "blkpipedispatchauthorized",
    "approvalinherited",
    "codexapproval",
    "blktestpassapproval",
    "productionisolationclaimed",
    "productionisolationenforced",
    "approvedforproduction",
    "approvalforproduction",
    "allowedforproduction",
    "permittedforproduction",
    "docsactive",
    "docsrequirementsactive",
    "protectedbodytext",
    "blkbreqbody",  # catches common typo variants when compacted near body text
    "blkreqbody",
    "reqbody",
    "bodytext",
    "systemshall",
    "curlhttps",
    "wgethttps",
    "pipinstall",
    "npminstall",
    "goget",
}

PACKAGE_204_KEYS = {
    "sprint_id",
    "surface",
    "status",
    "upstream_blk203_hash",
    "surface_files",
    "bounded_evidence_surfaces",
    "denied_authorities",
    "operator_notes",
    "caller_supplied_evidence_refs",
    "package_hash",
    *REQUIRED_FALSE_SIDE_EFFECT_FLAGS,
}

PACKAGE_205_KEYS = {
    "sprint_id",
    "surface",
    "status",
    "upstream_204_package_hash",
    "report_evidence_contract",
    "authority_grant_fields",
    "side_effect_obligations",
    "denied_authorities",
    "operator_notes",
    "caller_supplied_evidence_refs",
    "package_hash",
    *REQUIRED_FALSE_SIDE_EFFECT_FLAGS,
}

PACKAGE_206_KEYS = {
    "sprint_id",
    "surface",
    "status",
    "upstream_204_package_hash",
    "upstream_205_package_hash",
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


def _scan_caller_controlled(package: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    caller_payload = {field: package.get(field) for field in CALLER_CONTROLLED_FIELDS if field in package}
    errors.extend(scan_for_authority_laundering(caller_payload, "caller_controlled"))
    errors.extend(_scan_for_extra_tokens(caller_payload, "caller_controlled"))
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
                        errors.append(f"{path}.{key_text} contains forbidden BLK-pipe authority/protected token {token!r}")
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
                    errors.append(f"{path} contains forbidden BLK-pipe authority/protected token {token!r}")
            if "authorization=" in lowered or "api_key" in lowered or "github_pat" in lowered:
                errors.append(f"{path} contains secret-like tooling text")
    return errors


def _validate_exact_keys(package: dict[str, Any], expected: set[str], label: str) -> list[str]:
    errors: list[str] = []
    keys = set(package)
    if keys != expected:
        errors.append(f"{label} keys must be exact; missing={sorted(expected - keys)} extra={sorted(keys - expected)}")
    return errors


def _validate_denied_authorities(package: dict[str, Any]) -> list[str]:
    denied = package.get("denied_authorities")
    if denied != list(DENIED_AUTHORITIES):
        return ["denied_authorities must match exact ordered list"]
    if len(denied) != len(set(denied)):
        return ["denied_authorities must not contain duplicates"]
    if not all(isinstance(item, str) for item in denied):
        return ["denied_authorities must contain only strings"]
    return []


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


def _base_204() -> dict[str, Any]:
    return {
        "sprint_id": "BLK-SYSTEM-204",
        "surface": SURFACE,
        "status": "BLK_PIPE_SURFACE_REVIEW_READY_NOT_AUTHORITY",
        "upstream_blk203_hash": BLK203_BRIDGE_RECONCILIATION_HASH,
        "surface_files": list(SURFACE_FILES),
        "bounded_evidence_surfaces": list(BOUND_EVIDENCE_SURFACES),
        "denied_authorities": list(DENIED_AUTHORITIES),
        "operator_notes": list(EXACT_OPERATOR_NOTES),
        "caller_supplied_evidence_refs": {},
        **_false_flags(),
    }


def _base_205(upstream_204_hash: str) -> dict[str, Any]:
    return {
        "sprint_id": "BLK-SYSTEM-205",
        "surface": SURFACE,
        "status": "BLK_PIPE_BOUNDED_ENFORCEMENT_CONTRACT_READY_NOT_AUTHORITY",
        "upstream_204_package_hash": upstream_204_hash,
        "report_evidence_contract": dict(REPORT_EVIDENCE_CONTRACT),
        "authority_grant_fields": [],
        "side_effect_obligations": _false_flags(),
        "denied_authorities": list(DENIED_AUTHORITIES),
        "operator_notes": [
            "BLK-pipe report fields are bounded evidence and never authority grants.",
            "Validation profile capability labels remain diagnostic only.",
        ],
        "caller_supplied_evidence_refs": {},
        **_false_flags(),
    }


def _base_206(upstream_204_hash: str, upstream_205_hash: str) -> dict[str, Any]:
    return {
        "sprint_id": "BLK-SYSTEM-206",
        "surface": SURFACE,
        "status": "BLK_PIPE_BOUNDED_ENFORCEMENT_RECONCILED_CLEAN",
        "upstream_204_package_hash": upstream_204_hash,
        "upstream_205_package_hash": upstream_205_hash,
        "next_frontier": NEXT_FRONTIER,
        "reconciliation_findings": [
            "BLK_SYSTEM_204_BLK_PIPE_SURFACE_REVIEW_READY",
            "BLK_SYSTEM_205_BLK_PIPE_BOUNDED_ENFORCEMENT_CONTRACT_READY",
            "BLK-pipe is closed as a bounded non-authorizing enforcement surface.",
        ],
        "denied_authorities": list(DENIED_AUTHORITIES),
        "operator_notes": [
            "Clean reconciliation: BLK-pipe evidence is boxed, bounded, and non-authorizing.",
            "Next component selection remains not granted.",
        ],
        "caller_supplied_evidence_refs": {},
        **_false_flags(),
    }


def _with_hash(package: dict[str, Any]) -> dict[str, Any]:
    finalized = copy.deepcopy(package)
    finalized["package_hash"] = canonical_package_hash(finalized)
    return finalized


DEFAULT_204_PACKAGE_HASH = canonical_package_hash(_base_204())
DEFAULT_205_PACKAGE_HASH = canonical_package_hash(_base_205(DEFAULT_204_PACKAGE_HASH))
DEFAULT_206_PACKAGE_HASH = canonical_package_hash(_base_206(DEFAULT_204_PACKAGE_HASH, DEFAULT_205_PACKAGE_HASH))


def build_204_surface_review_package() -> dict[str, Any]:
    return _with_hash(_base_204())


def validate_204_surface_review_package(package: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    errors.extend(_validate_exact_keys(package, PACKAGE_204_KEYS, "BLK-SYSTEM-204 package"))
    if package.get("sprint_id") != "BLK-SYSTEM-204":
        errors.append("sprint_id must be BLK-SYSTEM-204")
    if package.get("surface") != SURFACE:
        errors.append("surface must be BLK-pipe blast shield")
    if package.get("status") != "BLK_PIPE_SURFACE_REVIEW_READY_NOT_AUTHORITY":
        errors.append("status must remain review-ready not authority")
    if package.get("upstream_blk203_hash") != BLK203_BRIDGE_RECONCILIATION_HASH:
        errors.append("upstream BLK-203 hash must be canonical")
    if package.get("surface_files") != list(SURFACE_FILES):
        errors.append("surface_files must match exact reviewed surface list")
    if package.get("bounded_evidence_surfaces") != list(BOUND_EVIDENCE_SURFACES):
        errors.append("bounded_evidence_surfaces must match exact evidence list")
    errors.extend(_validate_denied_authorities(package))
    errors.extend(_validate_false_flags(package))
    errors.extend(_scan_caller_controlled(package))
    errors.extend(_validate_hash(package, DEFAULT_204_PACKAGE_HASH))
    return errors


def build_205_enforcement_contract_package(review_package: dict[str, Any]) -> dict[str, Any]:
    errors = validate_204_surface_review_package(review_package)
    if errors or review_package.get("package_hash") != DEFAULT_204_PACKAGE_HASH:
        raise ValueError("BLK-SYSTEM-205 requires exact canonical BLK-SYSTEM-204 package")
    return _with_hash(_base_205(DEFAULT_204_PACKAGE_HASH))


def validate_205_enforcement_contract_package(package: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    errors.extend(_validate_exact_keys(package, PACKAGE_205_KEYS, "BLK-SYSTEM-205 package"))
    if package.get("sprint_id") != "BLK-SYSTEM-205":
        errors.append("sprint_id must be BLK-SYSTEM-205")
    if package.get("surface") != SURFACE:
        errors.append("surface must be BLK-pipe blast shield")
    if package.get("status") != "BLK_PIPE_BOUNDED_ENFORCEMENT_CONTRACT_READY_NOT_AUTHORITY":
        errors.append("status must remain contract-ready not authority")
    if package.get("upstream_204_package_hash") != DEFAULT_204_PACKAGE_HASH:
        errors.append("upstream_204_package_hash must be canonical BLK-SYSTEM-204 hash")
    if package.get("report_evidence_contract") != REPORT_EVIDENCE_CONTRACT:
        errors.append("report_evidence_contract must match exact non-authorizing report contract")
    if package.get("authority_grant_fields") != []:
        errors.append("authority_grant_fields must be an empty list")
    side_effects = package.get("side_effect_obligations")
    if side_effects != _false_flags():
        errors.append("side_effect_obligations must require every side effect flag explicit false")
    errors.extend(_validate_denied_authorities(package))
    errors.extend(_validate_false_flags(package))
    errors.extend(_scan_caller_controlled(package))
    errors.extend(_validate_hash(package, DEFAULT_205_PACKAGE_HASH))
    return errors


def build_206_reconciliation_package(review_package: dict[str, Any], contract_package: dict[str, Any]) -> dict[str, Any]:
    review_errors = validate_204_surface_review_package(review_package)
    contract_errors = validate_205_enforcement_contract_package(contract_package)
    if review_errors or contract_errors:
        raise ValueError("BLK-SYSTEM-206 requires exact canonical 204 and 205 packages")
    if review_package.get("package_hash") != DEFAULT_204_PACKAGE_HASH or contract_package.get("package_hash") != DEFAULT_205_PACKAGE_HASH:
        raise ValueError("BLK-SYSTEM-206 requires default canonical upstream hashes")
    return _with_hash(_base_206(DEFAULT_204_PACKAGE_HASH, DEFAULT_205_PACKAGE_HASH))


def validate_206_reconciliation_package(package: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    errors.extend(_validate_exact_keys(package, PACKAGE_206_KEYS, "BLK-SYSTEM-206 package"))
    if package.get("sprint_id") != "BLK-SYSTEM-206":
        errors.append("sprint_id must be BLK-SYSTEM-206")
    if package.get("surface") != SURFACE:
        errors.append("surface must be BLK-pipe blast shield")
    if package.get("status") != "BLK_PIPE_BOUNDED_ENFORCEMENT_RECONCILED_CLEAN":
        errors.append("status must be clean reconciliation")
    if package.get("upstream_204_package_hash") != DEFAULT_204_PACKAGE_HASH:
        errors.append("upstream_204_package_hash must be canonical")
    if package.get("upstream_205_package_hash") != DEFAULT_205_PACKAGE_HASH:
        errors.append("upstream_205_package_hash must be canonical")
    if package.get("next_frontier") != NEXT_FRONTIER:
        errors.append("next frontier must remain not granted")
    expected_findings = _base_206(DEFAULT_204_PACKAGE_HASH, DEFAULT_205_PACKAGE_HASH)["reconciliation_findings"]
    if package.get("reconciliation_findings") != expected_findings:
        errors.append("reconciliation_findings must match exact bounded closure findings")
    errors.extend(_validate_denied_authorities(package))
    errors.extend(_validate_false_flags(package))
    errors.extend(_scan_caller_controlled(package))
    errors.extend(_validate_hash(package, DEFAULT_206_PACKAGE_HASH))
    return errors


def build_blk_pipe_closure_packages() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    review = build_204_surface_review_package()
    contract = build_205_enforcement_contract_package(review)
    reconciliation = build_206_reconciliation_package(review, contract)
    return review, contract, reconciliation
