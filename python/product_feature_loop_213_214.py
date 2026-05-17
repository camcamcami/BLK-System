"""BLK-SYSTEM-213..214 product feature-loop fixtures.

These builders mark the transition from closure-only work into bounded
feature-producing loops. BLK-SYSTEM-213 records that BLK-test remains optional
non-authorizing diagnostic evidence and does not block the first feature loop.
BLK-SYSTEM-214 records one exact Kuronode feature commit plus verification and
reverse-patch/undo check evidence. This does not grant blanket future Kuronode
source/Git mutation, production BLK-test MCP, BLK-pipe runtime, Codex dispatch,
protected-body access, BEO/RTM authority, package/network tooling, or production
isolation claims.
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
from validation_profile_closure_210_212 import DEFAULT_212_PACKAGE_HASH

UPSTREAM_BLK212_RECONCILIATION_HASH = DEFAULT_212_PACKAGE_HASH
KURONODE_REPO = "/home/dad/code/Kuronode-v1"
KURONODE_FEATURE_PARENT_COMMIT = "ab2b4159fd812e21affeed4f49f39cdb8b0a24af"
KURONODE_FEATURE_COMMIT = "40f908b2a5d94991c2502018167d3a1c57031b2d"
KURONODE_FEATURE_PATCH_HASH = "sha256:8a42772e1cbb54df6c94b4d162a3f8e9ba6b3179d758d19cb99ec0b2ff4be061"
NEXT_FRONTIER = "NEXT_FRONTIER_SECOND_BOUNDED_KURONODE_FEATURE_LOOP_OR_OPERATOR_SELECTED_UNDO_NOT_GRANTED"

DENIED_AUTHORITIES = (
    "BLK_TEST_PRODUCTION_MCP_RUNTIME",
    "BLK_TEST_ORACLE_AUTHORITY",
    "AUTHORITY_FROM_BLK_TEST_PASS",
    "BROAD_BLK_PIPE_DISPATCH",
    "BLK_PIPE_RUNTIME_BEYOND_SEPARATE_EXACT_PAYLOAD_AUTHORITY",
    "LIVE_CODEX_DISPATCH",
    "TACTICAL_LLM_DISPATCH",
    "BEB_DISPATCH",
    "BEO_CLOSEOUT_EXECUTION",
    "BEO_PUBLICATION_SIGNING_STORAGE_LEDGER_REUSE",
    "RTM_GENERATION",
    "PRODUCTION_BLK_LINK",
    "RTM_DRIFT_REJECTION",
    "RTM_COVERAGE_TRUTH",
    "ACTIVE_VAULT_COMPARISON",
    "PROTECTED_BLK_REQ_BODY_READ_COPY_PARSE_HASH_SCAN",
    "BLANKET_TARGET_SOURCE_GIT_MUTATION",
    "PACKAGE_MANAGER_NETWORK_MODEL_BROWSER_CYBER_TOOLING",
    "PRODUCTION_ISOLATION_CLAIM",
)

REQUIRED_FALSE_SIDE_EFFECT_FLAGS = (
    "production_blk_test_mcp_authorized",
    "blk_test_oracle_authority_authorized",
    "authority_from_blk_test_pass_authorized",
    "blk_pipe_dispatch_authorized",
    "blk_pipe_runtime_authorized",
    "live_codex_dispatch_authorized",
    "tactical_llm_dispatch_authorized",
    "beb_dispatch_authorized",
    "beo_closeout_execution_authorized",
    "beo_publication_authorized",
    "rtm_generation_authorized",
    "production_blk_link_authorized",
    "rtm_drift_rejection_authorized",
    "rtm_coverage_truth_authorized",
    "active_vault_comparison_authorized",
    "protected_body_access_authorized",
    "blanket_kuronode_mutation_authorized",
    "package_network_model_browser_cyber_tooling_authorized",
    "production_isolation_claimed",
)

ALLOWED_KURONODE_FILES = (
    "packages/kuronode-graph/src/utils/GraphProjectionEngine.ts",
    "packages/kuronode-graph/tests/GraphProjectionEngine.test.ts",
)

KURONODE_VALIDATION_COMMANDS = (
    "npm run test -w @kuronode/kuronode-graph -- GraphProjectionEngine.test.ts",
    "npm run test -w @kuronode/kuronode-graph",
    "npm run build -w @kuronode/kuronode-graph",
    "npm run build -w kuronode-mcp",
)

UNDO_VERIFICATION_COMMANDS = (
    "git diff --binary ab2b4159fd812e21affeed4f49f39cdb8b0a24af 40f908b2a5d94991c2502018167d3a1c57031b2d -- packages/kuronode-graph/src/utils/GraphProjectionEngine.ts packages/kuronode-graph/tests/GraphProjectionEngine.test.ts > /tmp/kuronode-blk214.patch",
    "test -s /tmp/kuronode-blk214.patch",
    "printf '8a42772e1cbb54df6c94b4d162a3f8e9ba6b3179d758d19cb99ec0b2ff4be061  /tmp/kuronode-blk214.patch\\n' | sha256sum --check --strict -",
    "git apply --reverse --check /tmp/kuronode-blk214.patch",
)

CLOSEOUT_TRACEABILITY = {
    "existingRequirements": ["R-PRJ-038", "R-UIX-040", "R-PRJ-052", "R-PRJ-053"],
    "existingUseCases": ["UC-VIS-003", "UC-REQ-004"],
    "newRequirements": [],
    "newUseCases": [],
    "mcpCloseoutStatus": "PASS_STRICT",
}

CALLER_CONTROLLED_FIELDS = ("operator_notes", "caller_supplied_evidence_refs")
FORBIDDEN_COMPACT_TOKENS = {
    "blktestpassapproves",
    "blktestpassapproval",
    "productionblktestmcp",
    "blktestoracleauthority",
    "blanketkuronodesourcemutation",
    "blanketsourcemutation",
    "sourcegitmutationauthorized",
    "runtimeapproval",
    "runtimeexecutionauthorized",
    "livecodexexecutionauthorized",
    "codexapproval",
    "blkpipedispatchauthorized",
    "beopublicationgreenlit",
    "beopublicationauthorized",
    "publishbeo",
    "rtmgeneration",
    "rtmdriftrejection",
    "coveragetruth",
    "activevaulthashcomparison",
    "docsactive",
    "docsrequirementsactive",
    "docsprotected",
    "protectedbodytext",
    "requirementbody",
    "systemshall",
    "npminstall",
    "pipinstall",
    "curlhttps",
    "wgethttps",
    "goget",
    "privatekey",
    "apikey",
    "authorizationbearer",
}

PACKAGE_213_KEYS = {
    "sprint_id",
    "status",
    "upstream_blk212_hash",
    "decision",
    "unblock_findings",
    "denied_authorities",
    "operator_notes",
    "caller_supplied_evidence_refs",
    "package_hash",
    *REQUIRED_FALSE_SIDE_EFFECT_FLAGS,
}

PACKAGE_214_KEYS = {
    "sprint_id",
    "status",
    "upstream_213_package_hash",
    "feature_name",
    "kuronode_repo",
    "kuronode_parent_commit",
    "kuronode_feature_commit",
    "allowed_kuronode_files",
    "kuronode_validation_commands",
    "undo_verification_commands",
    "kuronode_feature_patch_hash",
    "closeout_traceability",
    "feature_loop_findings",
    "next_frontier",
    "exact_kuronode_feature_commit_recorded",
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


def _with_hash(package: dict[str, Any]) -> dict[str, Any]:
    finalized = copy.deepcopy(package)
    finalized["package_hash"] = canonical_package_hash(finalized)
    return finalized


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
    actual = package.get("package_hash")
    calculated = canonical_package_hash(package)
    errors: list[str] = []
    if actual != calculated:
        errors.append("package_hash must equal canonical package hash")
    if expected_hash is not None and actual != expected_hash:
        errors.append(f"package_hash must match canonical default {expected_hash}")
    return errors


def _scan_extra_tokens(value: Any, path: str) -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            for variant in decoded_authority_variants(str(key)):
                compact = compact_authority_text(variant)
                for token in FORBIDDEN_COMPACT_TOKENS:
                    if token in compact:
                        errors.append(f"{path}.{key} contains forbidden authority/tool/protected token {token!r}")
            errors.extend(_scan_extra_tokens(nested, f"{path}.{key}"))
    elif isinstance(value, (list, tuple, set)):
        for index, nested in enumerate(value):
            errors.extend(_scan_extra_tokens(nested, f"{path}[{index}]"))
    elif isinstance(value, str):
        for variant in decoded_authority_variants(value):
            compact = compact_authority_text(variant)
            for token in FORBIDDEN_COMPACT_TOKENS:
                if token in compact:
                    errors.append(f"{path} contains forbidden authority/tool/protected token {token!r}")
    return errors


def _scan_caller_controlled(package: dict[str, Any]) -> list[str]:
    payload = {field: package.get(field) for field in CALLER_CONTROLLED_FIELDS if field in package}
    errors = scan_for_authority_laundering(payload, "caller_controlled")
    errors.extend(_scan_extra_tokens(payload, "caller_controlled"))
    return errors


def _base_213() -> dict[str, Any]:
    return {
        "sprint_id": "BLK-SYSTEM-213",
        "status": "BLK_TEST_OPTIONAL_DIAGNOSTIC_UNBLOCK_READY",
        "upstream_blk212_hash": UPSTREAM_BLK212_RECONCILIATION_HASH,
        "decision": "BLK_TEST_DOES_NOT_BLOCK_FIRST_BOUNDED_KURONODE_FEATURE_LOOP",
        "unblock_findings": [
            "BLK-test is optional diagnostic evidence",
            "First feature loop may use Kuronode repo-local tests/build without production BLK-test MCP",
            "BLK-test remains a functional module, not the BLK-System test suite",
        ],
        "denied_authorities": list(DENIED_AUTHORITIES),
        "operator_notes": [
            "BLK-test remains disabled/gated diagnostic evidence for this transition.",
            "No production MCP, oracle authority, or PASS-as-approval behavior is granted.",
        ],
        "caller_supplied_evidence_refs": {},
        **_false_flags(),
    }


def _base_214(upstream_213_hash: str) -> dict[str, Any]:
    return {
        "sprint_id": "BLK-SYSTEM-214",
        "status": "BOUNDED_KURONODE_FEATURE_LOOP_EXECUTED",
        "upstream_213_package_hash": upstream_213_hash,
        "feature_name": "GraphProjectionEngine projection summary metrics",
        "kuronode_repo": KURONODE_REPO,
        "kuronode_parent_commit": KURONODE_FEATURE_PARENT_COMMIT,
        "kuronode_feature_commit": KURONODE_FEATURE_COMMIT,
        "allowed_kuronode_files": list(ALLOWED_KURONODE_FILES),
        "kuronode_validation_commands": list(KURONODE_VALIDATION_COMMANDS),
        "undo_verification_commands": list(UNDO_VERIFICATION_COMMANDS),
        "kuronode_feature_patch_hash": KURONODE_FEATURE_PATCH_HASH,
        "closeout_traceability": copy.deepcopy(CLOSEOUT_TRACEABILITY),
        "feature_loop_findings": [
            "First bounded Kuronode feature loop executed",
            "Projection summary path is observational and preserves legacy projection output",
            "Kuronode focused and graph-package verification passed",
            "Undo/reverse-patch check passed without undoing committed work",
        ],
        "next_frontier": NEXT_FRONTIER,
        "exact_kuronode_feature_commit_recorded": True,
        "denied_authorities": list(DENIED_AUTHORITIES),
        "operator_notes": [
            "User explicitly selected a small Kuronode feature for the first bounded feature loop.",
            "The exact committed feature does not grant future blanket source/Git mutation authority.",
        ],
        "caller_supplied_evidence_refs": {},
        **_false_flags(),
    }


DEFAULT_213_PACKAGE_HASH = canonical_package_hash(_base_213())
DEFAULT_214_PACKAGE_HASH = canonical_package_hash(_base_214(DEFAULT_213_PACKAGE_HASH))


def build_213_blk_test_optional_unblock_package() -> dict[str, Any]:
    return _with_hash(_base_213())


def validate_213_blk_test_optional_unblock_package(package: dict[str, Any]) -> list[str]:
    if not isinstance(package, dict):
        return ["BLK-SYSTEM-213 package must be an object"]
    errors: list[str] = []
    errors.extend(_validate_exact_keys(package, PACKAGE_213_KEYS, "BLK-SYSTEM-213 package"))
    if package.get("sprint_id") != "BLK-SYSTEM-213":
        errors.append("sprint_id must be BLK-SYSTEM-213")
    if package.get("status") != "BLK_TEST_OPTIONAL_DIAGNOSTIC_UNBLOCK_READY":
        errors.append("status must remain BLK-test optional diagnostic unblock")
    if package.get("upstream_blk212_hash") != UPSTREAM_BLK212_RECONCILIATION_HASH:
        errors.append("upstream_blk212_hash must be canonical BLK-SYSTEM-212 hash")
    if package.get("decision") != "BLK_TEST_DOES_NOT_BLOCK_FIRST_BOUNDED_KURONODE_FEATURE_LOOP":
        errors.append("decision must be exact non-blocking diagnostic decision")
    if package.get("unblock_findings") != _base_213()["unblock_findings"]:
        errors.append("unblock_findings must match exact BLK-test optional diagnostic findings")
    errors.extend(_validate_denied_authorities(package))
    errors.extend(_validate_false_flags(package))
    errors.extend(_scan_caller_controlled(package))
    errors.extend(_validate_hash(package, DEFAULT_213_PACKAGE_HASH))
    return errors


def build_214_kuronode_feature_loop_package(unblock_package: dict[str, Any]) -> dict[str, Any]:
    errors = validate_213_blk_test_optional_unblock_package(unblock_package)
    if errors or unblock_package.get("package_hash") != DEFAULT_213_PACKAGE_HASH:
        raise ValueError("BLK-SYSTEM-214 requires canonical BLK-SYSTEM-213 package")
    return _with_hash(_base_214(DEFAULT_213_PACKAGE_HASH))


def validate_214_kuronode_feature_loop_package(package: dict[str, Any]) -> list[str]:
    if not isinstance(package, dict):
        return ["BLK-SYSTEM-214 package must be an object"]
    errors: list[str] = []
    errors.extend(_validate_exact_keys(package, PACKAGE_214_KEYS, "BLK-SYSTEM-214 package"))
    if package.get("sprint_id") != "BLK-SYSTEM-214":
        errors.append("sprint_id must be BLK-SYSTEM-214")
    if package.get("status") != "BOUNDED_KURONODE_FEATURE_LOOP_EXECUTED":
        errors.append("status must be bounded Kuronode feature loop executed")
    if package.get("upstream_213_package_hash") != DEFAULT_213_PACKAGE_HASH:
        errors.append("upstream_213_package_hash must be canonical")
    if package.get("feature_name") != "GraphProjectionEngine projection summary metrics":
        errors.append("feature_name must match exact feature")
    if package.get("kuronode_repo") != KURONODE_REPO:
        errors.append("kuronode_repo must match exact target repo")
    if package.get("kuronode_parent_commit") != KURONODE_FEATURE_PARENT_COMMIT:
        errors.append("kuronode_parent_commit must match exact pre-feature commit")
    if package.get("kuronode_feature_commit") != KURONODE_FEATURE_COMMIT:
        errors.append("kuronode_feature_commit must match exact committed feature")
    if package.get("allowed_kuronode_files") != list(ALLOWED_KURONODE_FILES):
        errors.append("allowed_kuronode_files must match exact feature allowlist")
    if package.get("kuronode_validation_commands") != list(KURONODE_VALIDATION_COMMANDS):
        errors.append("kuronode_validation_commands must match exact verification list")
    if package.get("undo_verification_commands") != list(UNDO_VERIFICATION_COMMANDS):
        errors.append("undo_verification_commands must match exact reverse-patch checks")
    if package.get("kuronode_feature_patch_hash") != KURONODE_FEATURE_PATCH_HASH:
        errors.append("kuronode_feature_patch_hash must match exact feature diff patch hash")
    if package.get("closeout_traceability") != CLOSEOUT_TRACEABILITY:
        errors.append("closeout_traceability must match exact Kuronode MCP closeout traceability")
    if package.get("feature_loop_findings") != _base_214(DEFAULT_213_PACKAGE_HASH)["feature_loop_findings"]:
        errors.append("feature_loop_findings must match exact first feature-loop findings")
    if package.get("next_frontier") != NEXT_FRONTIER:
        errors.append("next frontier must remain not granted")
    if package.get("exact_kuronode_feature_commit_recorded") is not True:
        errors.append("exact_kuronode_feature_commit_recorded must be true for the exact committed feature")
    errors.extend(_validate_denied_authorities(package))
    errors.extend(_validate_false_flags(package))
    errors.extend(_scan_caller_controlled(package))
    errors.extend(_validate_hash(package, DEFAULT_214_PACKAGE_HASH))
    return errors


def build_product_feature_loop_packages() -> tuple[dict[str, Any], dict[str, Any]]:
    unblock = build_213_blk_test_optional_unblock_package()
    feature = build_214_kuronode_feature_loop_package(unblock)
    return unblock, feature
