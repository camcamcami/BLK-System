"""BLK-SYSTEM-210..212 validation-profile closure fixtures.

These builders close validation profiles as bounded repository-owned local argv
and capability-label evidence. They do not execute profiles, invoke blk-pipe,
start subprocesses, mutate source/Git state, contact networks, install packages,
read protected bodies, or grant runtime authority. PASS and capability labels
remain diagnostic evidence only.
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
from python_adapter_closure_207_209 import DEFAULT_209_PACKAGE_HASH

SURFACE = "Validation profiles"
UPSTREAM_BLK209_RECONCILIATION_HASH = DEFAULT_209_PACKAGE_HASH
NEXT_FRONTIER = "NEXT_FRONTIER_VALIDATION_PROFILES_CLOSED_BLK_TEST_SELECTION_NOT_GRANTED"

DENIED_AUTHORITIES = (
    "VALIDATION_PROFILE_RUNTIME_AUTHORITY",
    "AUTHORITY_FROM_PASS_OR_CAPABILITY_LABELS",
    "BROAD_BLK_PIPE_DISPATCH",
    "BLK_PIPE_RUNTIME_BEYOND_SEPARATE_EXACT_PAYLOAD_AUTHORITY",
    "PYTHON_ADAPTER_BLK_PIPE_DISPATCH_AUTHORITY",
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
)

REQUIRED_FALSE_SIDE_EFFECT_FLAGS = (
    "validation_profile_runtime_authorized",
    "authority_from_pass_authorized",
    "capability_label_authority_authorized",
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
    "internal/validationprofiles/profiles.go",
    "internal/validationprofiles/profiles_test.go",
    "internal/contracts/payload.go",
    "internal/contracts/report.go",
)

BOUNDED_PROFILE_SURFACES = (
    "structured_argv_registry",
    "repository_owned_profile_name_validation",
    "capability_label_evidence",
    "display_command_evidence",
    "defensive_copy_resolution",
    "trusted_local_legacy_command_boundary",
)

PROFILE_CONTRACT = {
    "structured_argv": "repository_owned_local_evidence_only_no_shell",
    "capability_labels": "diagnostic_labels_only",
    "display_commands": "human_readable_evidence_not_shell_execution_authority",
    "profile_names": "known_repository_owned_names_only",
    "pass_results": "PASS_is_diagnostic_evidence_not_runtime_or_mutation_authority",
    "legacy_validation_commands": "trusted_local_compatibility_only_not_autonomous_authority",
    "execution_semantics": "no_profile_execution_or_subprocess_in_this_closure_fixture",
    "tooling_scope": "no_package_network_model_browser_cyber_or_production_isolation_claim",
}

CALLER_CONTROLLED_FIELDS = ("operator_notes", "caller_supplied_evidence_refs")
EXACT_REVIEW_FINDINGS = (
    "Validation profiles resolve repository-owned argv/env specs and display evidence only.",
    "Capability labels and PASS output are diagnostic evidence, not authority grants.",
    "Profile closure does not execute profiles, invoke blk-pipe, install packages, or contact networks.",
)
EXACT_OPERATOR_NOTES_210 = (
    "Validation-profile closure records existing repository-owned argv/capability behavior only.",
    "No runtime, BLK-pipe, Codex, BLK-test MCP, RTM, BEO, protected-body, tooling, or mutation authority is granted.",
)
EXACT_OPERATOR_NOTES_211 = (
    "Validation-profile contract is closed as non-authorizing local evidence.",
    "No profile field, PASS result, or capability label may become an authority grant field.",
)
EXACT_OPERATOR_NOTES_212 = (
    "Validation profiles are boxed as non-authorizing local evidence.",
    "BLK-test is selected as the next component surface only; no authority is granted here.",
)

FORBIDDEN_CALLER_COMPACT_TOKENS = {
    "validationprofilepassapproval",
    "validationprofileapproved",
    "validationprofileruntimeauthorized",
    "profilecapabilityisauthorized",
    "profilecapabilityauthorized",
    "passgrantsruntime",
    "passgrantsmutation",
    "runtimeapproval",
    "runtimeapproved",
    "runtimeexecutionauthorized",
    "blkpipeapproved",
    "blkpipesuccess",
    "blkpipedispatchauthorized",
    "livecodexexecutionallowed",
    "codexapproval",
    "blktestpassapproval",
    "productionblktestmcpauthorized",
    "approvalinherited",
    "approvedforproduction",
    "approvalforproduction",
    "allowedforproduction",
    "permittedforproduction",
    "greenlitforproduction",
    "productionisolationclaimed",
    "productionisolationenforced",
    "productionsandboxenforced",
    "beopublicationauthorized",
    "authoritativebeopublication",
    "publishbeo",
    "rtmgeneration",
    "rtmdriftrejection",
    "coveragetruth",
    "activevaulthashcomparison",
    "docsactive",
    "docsrequirementsactive",
    "docsrequirements",
    "docsusecases",
    "docsprotected",
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
    "dockerbuild",
    "sshgit",
    "authorizationbearer",
    "authorizationbasic",
    "privatekey",
    "apikey",
    "githubpat",
}

PACKAGE_210_KEYS = {
    "sprint_id",
    "surface",
    "status",
    "upstream_blk209_hash",
    "reviewed_surface_files",
    "bounded_profile_surfaces",
    "review_findings",
    "denied_authorities",
    "operator_notes",
    "caller_supplied_evidence_refs",
    "package_hash",
    *REQUIRED_FALSE_SIDE_EFFECT_FLAGS,
}

PACKAGE_211_KEYS = {
    "sprint_id",
    "surface",
    "status",
    "upstream_210_package_hash",
    "profile_contract",
    "authority_grant_fields",
    "side_effect_obligations",
    "denied_authorities",
    "operator_notes",
    "caller_supplied_evidence_refs",
    "package_hash",
    *REQUIRED_FALSE_SIDE_EFFECT_FLAGS,
}

PACKAGE_212_KEYS = {
    "sprint_id",
    "surface",
    "status",
    "upstream_210_package_hash",
    "upstream_211_package_hash",
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
                        errors.append(f"{path}.{key_text} contains forbidden validation-profile authority/tool/protected token {token!r}")
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
                    errors.append(f"{path} contains forbidden validation-profile authority/tool/protected token {token!r}")
            if "authorization=" in lowered or "api_key" in lowered or "github_pat" in lowered:
                errors.append(f"{path} contains secret-like tooling text")
    return errors


def _scan_caller_controlled(package: dict[str, Any]) -> list[str]:
    caller_payload = {field: package.get(field) for field in CALLER_CONTROLLED_FIELDS if field in package}
    errors = scan_for_authority_laundering(caller_payload, "caller_controlled")
    errors.extend(_scan_for_extra_tokens(caller_payload, "caller_controlled"))
    return errors


def _base_210() -> dict[str, Any]:
    return {
        "sprint_id": "BLK-SYSTEM-210",
        "surface": SURFACE,
        "status": "VALIDATION_PROFILE_SURFACE_REVIEW_READY_NOT_AUTHORITY",
        "upstream_blk209_hash": UPSTREAM_BLK209_RECONCILIATION_HASH,
        "reviewed_surface_files": list(REVIEWED_SURFACE_FILES),
        "bounded_profile_surfaces": list(BOUNDED_PROFILE_SURFACES),
        "review_findings": list(EXACT_REVIEW_FINDINGS),
        "denied_authorities": list(DENIED_AUTHORITIES),
        "operator_notes": list(EXACT_OPERATOR_NOTES_210),
        "caller_supplied_evidence_refs": {},
        **_false_flags(),
    }


def _base_211(upstream_210_hash: str) -> dict[str, Any]:
    return {
        "sprint_id": "BLK-SYSTEM-211",
        "surface": SURFACE,
        "status": "VALIDATION_PROFILE_CONTRACT_READY_NOT_RUNTIME_AUTHORITY",
        "upstream_210_package_hash": upstream_210_hash,
        "profile_contract": copy.deepcopy(PROFILE_CONTRACT),
        "authority_grant_fields": [],
        "side_effect_obligations": _false_flags(),
        "denied_authorities": list(DENIED_AUTHORITIES),
        "operator_notes": list(EXACT_OPERATOR_NOTES_211),
        "caller_supplied_evidence_refs": {},
        **_false_flags(),
    }


def _base_212(upstream_210_hash: str, upstream_211_hash: str) -> dict[str, Any]:
    return {
        "sprint_id": "BLK-SYSTEM-212",
        "surface": SURFACE,
        "status": "VALIDATION_PROFILE_RECONCILED_CLEAN",
        "upstream_210_package_hash": upstream_210_hash,
        "upstream_211_package_hash": upstream_211_hash,
        "next_frontier": NEXT_FRONTIER,
        "reconciliation_findings": [
            "BLK_SYSTEM_210_VALIDATION_PROFILE_SURFACE_REVIEW_READY",
            "BLK_SYSTEM_211_VALIDATION_PROFILE_CONTRACT_READY",
            "Validation profiles closed as bounded non-authorizing local evidence.",
            "BLK-test remains the next selected surface, not granted authority",
        ],
        "denied_authorities": list(DENIED_AUTHORITIES),
        "operator_notes": list(EXACT_OPERATOR_NOTES_212),
        "caller_supplied_evidence_refs": {},
        **_false_flags(),
    }


def _with_hash(package: dict[str, Any]) -> dict[str, Any]:
    finalized = copy.deepcopy(package)
    finalized["package_hash"] = canonical_package_hash(finalized)
    return finalized


DEFAULT_210_PACKAGE_HASH = canonical_package_hash(_base_210())
DEFAULT_211_PACKAGE_HASH = canonical_package_hash(_base_211(DEFAULT_210_PACKAGE_HASH))
DEFAULT_212_PACKAGE_HASH = canonical_package_hash(_base_212(DEFAULT_210_PACKAGE_HASH, DEFAULT_211_PACKAGE_HASH))


def build_210_validation_profile_surface_review_package() -> dict[str, Any]:
    return _with_hash(_base_210())


def validate_210_validation_profile_surface_review_package(package: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(package, dict):
        return ["BLK-SYSTEM-210 package must be an object"]
    errors.extend(_validate_exact_keys(package, PACKAGE_210_KEYS, "BLK-SYSTEM-210 package"))
    if package.get("sprint_id") != "BLK-SYSTEM-210":
        errors.append("sprint_id must be BLK-SYSTEM-210")
    if package.get("surface") != SURFACE:
        errors.append("surface must be Validation profiles")
    if package.get("status") != "VALIDATION_PROFILE_SURFACE_REVIEW_READY_NOT_AUTHORITY":
        errors.append("status must remain review-ready not authority")
    if package.get("upstream_blk209_hash") != UPSTREAM_BLK209_RECONCILIATION_HASH:
        errors.append("upstream BLK-209 hash must be canonical")
    if package.get("reviewed_surface_files") != list(REVIEWED_SURFACE_FILES):
        errors.append("reviewed_surface_files must match exact validation-profile file list")
    if package.get("bounded_profile_surfaces") != list(BOUNDED_PROFILE_SURFACES):
        errors.append("bounded_profile_surfaces must match exact bounded surface list")
    if package.get("review_findings") != list(EXACT_REVIEW_FINDINGS):
        errors.append("review_findings must match exact non-authorizing validation-profile findings")
    errors.extend(_validate_denied_authorities(package))
    errors.extend(_validate_false_flags(package))
    errors.extend(_scan_caller_controlled(package))
    errors.extend(_validate_hash(package, DEFAULT_210_PACKAGE_HASH))
    return errors


def build_211_validation_profile_contract_package(review_package: dict[str, Any]) -> dict[str, Any]:
    errors = validate_210_validation_profile_surface_review_package(review_package)
    if errors or review_package.get("package_hash") != DEFAULT_210_PACKAGE_HASH:
        raise ValueError("BLK-SYSTEM-211 requires exact canonical BLK-SYSTEM-210 package")
    return _with_hash(_base_211(DEFAULT_210_PACKAGE_HASH))


def validate_211_validation_profile_contract_package(package: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(package, dict):
        return ["BLK-SYSTEM-211 package must be an object"]
    errors.extend(_validate_exact_keys(package, PACKAGE_211_KEYS, "BLK-SYSTEM-211 package"))
    if package.get("sprint_id") != "BLK-SYSTEM-211":
        errors.append("sprint_id must be BLK-SYSTEM-211")
    if package.get("surface") != SURFACE:
        errors.append("surface must be Validation profiles")
    if package.get("status") != "VALIDATION_PROFILE_CONTRACT_READY_NOT_RUNTIME_AUTHORITY":
        errors.append("status must remain contract-ready not runtime authority")
    if package.get("upstream_210_package_hash") != DEFAULT_210_PACKAGE_HASH:
        errors.append("upstream_210_package_hash must be canonical BLK-SYSTEM-210 hash")
    if package.get("profile_contract") != PROFILE_CONTRACT:
        errors.append("profile_contract must match exact non-authorizing validation-profile contract")
    if package.get("authority_grant_fields") != []:
        errors.append("authority_grant_fields must be an empty list")
    if package.get("side_effect_obligations") != _false_flags():
        errors.append("side_effect_obligations must require every side effect flag explicit false")
    errors.extend(_validate_denied_authorities(package))
    errors.extend(_validate_false_flags(package))
    errors.extend(_scan_caller_controlled(package))
    errors.extend(_validate_hash(package, DEFAULT_211_PACKAGE_HASH))
    return errors


def build_212_validation_profile_reconciliation_package(review_package: dict[str, Any], contract_package: dict[str, Any]) -> dict[str, Any]:
    review_errors = validate_210_validation_profile_surface_review_package(review_package)
    contract_errors = validate_211_validation_profile_contract_package(contract_package)
    if review_errors or contract_errors:
        raise ValueError("BLK-SYSTEM-212 requires exact canonical 210 and 211 packages")
    if review_package.get("package_hash") != DEFAULT_210_PACKAGE_HASH or contract_package.get("package_hash") != DEFAULT_211_PACKAGE_HASH:
        raise ValueError("BLK-SYSTEM-212 requires default canonical upstream hashes")
    return _with_hash(_base_212(DEFAULT_210_PACKAGE_HASH, DEFAULT_211_PACKAGE_HASH))


def validate_212_validation_profile_reconciliation_package(package: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(package, dict):
        return ["BLK-SYSTEM-212 package must be an object"]
    errors.extend(_validate_exact_keys(package, PACKAGE_212_KEYS, "BLK-SYSTEM-212 package"))
    if package.get("sprint_id") != "BLK-SYSTEM-212":
        errors.append("sprint_id must be BLK-SYSTEM-212")
    if package.get("surface") != SURFACE:
        errors.append("surface must be Validation profiles")
    if package.get("status") != "VALIDATION_PROFILE_RECONCILED_CLEAN":
        errors.append("status must be clean reconciliation")
    if package.get("upstream_210_package_hash") != DEFAULT_210_PACKAGE_HASH:
        errors.append("upstream_210_package_hash must be canonical")
    if package.get("upstream_211_package_hash") != DEFAULT_211_PACKAGE_HASH:
        errors.append("upstream_211_package_hash must be canonical")
    if package.get("next_frontier") != NEXT_FRONTIER:
        errors.append("next frontier must remain not granted")
    expected_findings = _base_212(DEFAULT_210_PACKAGE_HASH, DEFAULT_211_PACKAGE_HASH)["reconciliation_findings"]
    if package.get("reconciliation_findings") != expected_findings:
        errors.append("reconciliation_findings must match exact validation-profile closure findings")
    errors.extend(_validate_denied_authorities(package))
    errors.extend(_validate_false_flags(package))
    errors.extend(_scan_caller_controlled(package))
    errors.extend(_validate_hash(package, DEFAULT_212_PACKAGE_HASH))
    return errors


def build_validation_profile_closure_packages() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    review = build_210_validation_profile_surface_review_package()
    contract = build_211_validation_profile_contract_package(review)
    reconciliation = build_212_validation_profile_reconciliation_package(review, contract)
    return review, contract, reconciliation
