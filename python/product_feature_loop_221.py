"""BLK-SYSTEM-221 fourth bounded Kuronode feature-loop evidence.

This module records one tiny Hermes-direct Kuronode UI feature: the Canonical
Requirements data grid now states an explicit loading message while backend
requirements are being fetched. The package binds exact Kuronode commits, patch
hash, strict Kuronode closeout, and validation output without granting reusable
Codex dispatch, native workspace-write authority, BLK-pipe runtime, BEB/BEO
execution, RTM authority, protected-body access, package/network tooling, or
blanket future Kuronode source/Git mutation authority.
"""

from __future__ import annotations

import copy
from typing import Any

from blk_authority_smuggling import (
    compact_authority_text,
    decoded_authority_variants,
    scan_for_authority_laundering,
)
from product_codex_config_containment_216 import canonical_package_hash
from product_codex_native_sandbox_repair_recheck_220 import (
    DEFAULT_220_PACKAGE_HASH,
    DENIED_AUTHORITIES,
    REQUIRED_FALSE_SIDE_EFFECT_FLAGS,
)
from product_feature_loop_213_214 import KURONODE_REPO

UPSTREAM_BLK220_PACKAGE_HASH = DEFAULT_220_PACKAGE_HASH
KURONODE_FEATURE_PARENT_COMMIT_221 = "af208ea57604707c7ae2b768f4f480d4c42ce7cf"
KURONODE_FEATURE_WORKER_COMMIT_221 = "0b28d8a5070aeb6ccddc6d3ae2e15f962216ccbd"
KURONODE_FEATURE_MERGE_COMMIT_221 = "ce6e9ca396e79d1184ae9cc156789055ee852169"
KURONODE_FEATURE_PATCH_HASH_221 = "sha256:c51d084363750b810b777e1e71cac0d329e0df59c95a2bf57e1a8487bdc0325c"
BLK221_KURONODE_CLOSEOUT_HASH = "sha256:45fc5521e56d3f69bc6113e2a224020314237ccc2307110899035395d8a60c29"
NEXT_FRONTIER_221 = "NEXT_FRONTIER_OPERATOR_SELECTED_NEXT_BOUNDED_KURONODE_FEATURE_OR_OBSERVED_FAILURE_HARDENING_NOT_GRANTED"

ALLOWED_KURONODE_FILES_221 = (
    "packages/kuronode-graph/src/components/CanonicalDataGrid.test.tsx",
    "packages/kuronode-graph/src/components/CanonicalDataGrid.tsx",
)

KURONODE_VALIDATION_COMMANDS_221 = (
    "npm run test -w @kuronode/kuronode-graph -- CanonicalDataGrid.test.tsx",
    "npm run test -w @kuronode/kuronode-graph",
    "npm run build -w @kuronode/kuronode-graph",
    "git diff --check -- packages/kuronode-graph/src/components/CanonicalDataGrid.test.tsx packages/kuronode-graph/src/components/CanonicalDataGrid.tsx",
    "git apply --reverse --check /tmp/kuronode-blk221-merge.patch",
)

CLOSEOUT_TRACEABILITY_221 = {
    "existingRequirements": ["R-UIX-169", "R-UIX-170"],
    "existingUseCases": ["UC-REQ-004"],
    "newRequirements": [],
    "newUseCases": [],
    "mcpCloseoutStatus": "PASS_STRICT",
    "closeout_hash": BLK221_KURONODE_CLOSEOUT_HASH,
}

PACKAGE_221_KEYS = {
    "sprint_id",
    "status",
    "upstream_220_package_hash",
    "feature_name",
    "kuronode_repo",
    "kuronode_parent_commit",
    "kuronode_feature_worker_commit",
    "kuronode_feature_merge_commit",
    "allowed_kuronode_files",
    "kuronode_validation_commands",
    "kuronode_feature_patch_hash",
    "implementation_actor",
    "external_supervised_codex_worker_used",
    "native_workspace_write_recheck_used",
    "tdd_evidence",
    "validation_evidence",
    "closeout_traceability",
    "feature_loop_findings",
    "post_merge_git_status_short",
    "next_frontier",
    "exact_kuronode_feature_commit_recorded",
    "denied_authorities",
    "operator_notes",
    "caller_supplied_evidence_refs",
    "package_hash",
    *REQUIRED_FALSE_SIDE_EFFECT_FLAGS,
}

CALLER_CONTROLLED_FIELDS = ("operator_notes", "caller_supplied_evidence_refs")
FORBIDDEN_COMPACT_TOKENS = {
    "blktestpassapproval",
    "productionblktestmcp",
    "blanketkuronodesourcemutation",
    "blanketsourcemutation",
    "sourcegitmutationauthorized",
    "targetgitmutationauthorized",
    "runtimeapproval",
    "runtimeexecutionauthorized",
    "livecodexexecutionauthorized",
    "reusablecodexdispatch",
    "codexapproval",
    "nativeworkspacewritereusableauthority",
    "nativeworkspacewriteauthorized",
    "productionsandboxenforced",
    "productionisolationclaim",
    "blkpipedispatchauthorized",
    "bebdispatchauthorized",
    "beocloseoutexecution",
    "beopublicationgreenlit",
    "beopublicationauthorized",
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
    "protectedbody",
    "protectedbodytext",
    "requirementbody",
    "systemshall",
    "npminstall",
    "pipinstall",
    "uvpipinstall",
    "curlhttps",
    "wgethttps",
    "goget",
    "privatekey",
    "apikey",
    "authorizationbearer",
}


def _false_flags() -> dict[str, bool]:
    return {flag: False for flag in REQUIRED_FALSE_SIDE_EFFECT_FLAGS}


def _with_hash(package: dict[str, Any]) -> dict[str, Any]:
    finalized = copy.deepcopy(package)
    finalized["package_hash"] = canonical_package_hash(finalized)
    return finalized


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


def _base_221() -> dict[str, Any]:
    return {
        "sprint_id": "BLK-SYSTEM-221",
        "status": "FOURTH_BOUNDED_KURONODE_FEATURE_LOOP_EXECUTED",
        "upstream_220_package_hash": UPSTREAM_BLK220_PACKAGE_HASH,
        "feature_name": "CanonicalDataGrid explicit loading state copy",
        "kuronode_repo": KURONODE_REPO,
        "kuronode_parent_commit": KURONODE_FEATURE_PARENT_COMMIT_221,
        "kuronode_feature_worker_commit": KURONODE_FEATURE_WORKER_COMMIT_221,
        "kuronode_feature_merge_commit": KURONODE_FEATURE_MERGE_COMMIT_221,
        "allowed_kuronode_files": list(ALLOWED_KURONODE_FILES_221),
        "kuronode_validation_commands": list(KURONODE_VALIDATION_COMMANDS_221),
        "kuronode_feature_patch_hash": KURONODE_FEATURE_PATCH_HASH_221,
        "implementation_actor": "Hermes direct bounded edit",
        "external_supervised_codex_worker_used": False,
        "native_workspace_write_recheck_used": False,
        "tdd_evidence": {
            "red_focused_test": "RED: CanonicalDataGrid.test.tsx failed because Loading canonical requirements... was absent; 1 failed | 3 passed",
            "green_focused_test": "GREEN: CanonicalDataGrid.test.tsx passed with 4 passed",
            "test_first_observed": True,
        },
        "validation_evidence": {
            "focused_test": "CanonicalDataGrid.test.tsx: 4 passed",
            "graph_test_suite": "@kuronode/kuronode-graph vitest: 16 files passed, 55 passed",
            "graph_build": "npm run build -w @kuronode/kuronode-graph exited 0; Vite built in 940ms with pre-existing chunk warnings",
            "diff_check": "git diff --check passed for exact changed paths",
            "reverse_apply_check": "git apply --reverse --check /tmp/kuronode-blk221-merge.patch passed",
        },
        "closeout_traceability": copy.deepcopy(CLOSEOUT_TRACEABILITY_221),
        "feature_loop_findings": [
            "Fourth bounded Kuronode feature loop executed as a Hermes-direct exact-file edit, without Codex dispatch",
            "CanonicalDataGrid now displays explicit loading copy while preserving the spinner, selected requirement badge, loaded count, and projection summary badges",
            "Focused RED/GREEN test, full graph test suite, graph package build, strict MCP closeout, exact patch hash, and reverse-apply evidence passed",
            "No native workspace-write recheck was used because no tactical LLM worker was dispatched in this sprint",
        ],
        "post_merge_git_status_short": "",
        "next_frontier": NEXT_FRONTIER_221,
        "exact_kuronode_feature_commit_recorded": True,
        "denied_authorities": list(DENIED_AUTHORITIES),
        "operator_notes": [
            "User asked Hermes to plan and execute BLK-SYSTEM-221; Hermes selected one tiny requirements-grid loading-state feature.",
            "No Codex worker was used; BLK-System internal live-dispatch authority and sandbox reuse authority remain denied.",
        ],
        "caller_supplied_evidence_refs": {},
        **_false_flags(),
    }


DEFAULT_221_PACKAGE_HASH = canonical_package_hash(_base_221())


def build_221_loading_state_feature_package() -> dict[str, Any]:
    return _with_hash(_base_221())


def validate_221_loading_state_feature_package(package: dict[str, Any]) -> list[str]:
    if not isinstance(package, dict):
        return ["BLK-SYSTEM-221 package must be an object"]

    errors: list[str] = []
    keys = set(package)
    if keys != PACKAGE_221_KEYS:
        errors.append(f"BLK-SYSTEM-221 package keys must be exact; missing={sorted(PACKAGE_221_KEYS - keys)} extra={sorted(keys - PACKAGE_221_KEYS)}")

    expected_scalars = {
        "sprint_id": "BLK-SYSTEM-221",
        "status": "FOURTH_BOUNDED_KURONODE_FEATURE_LOOP_EXECUTED",
        "upstream_220_package_hash": UPSTREAM_BLK220_PACKAGE_HASH,
        "feature_name": "CanonicalDataGrid explicit loading state copy",
        "kuronode_feature_patch_hash": KURONODE_FEATURE_PATCH_HASH_221,
        "post_merge_git_status_short": "",
        "next_frontier": NEXT_FRONTIER_221,
        "package_hash": DEFAULT_221_PACKAGE_HASH,
    }
    for key, expected in expected_scalars.items():
        if package.get(key) != expected:
            errors.append(f"{key} must be {expected!r}")

    if package.get("allowed_kuronode_files") != list(ALLOWED_KURONODE_FILES_221):
        errors.append("allowed_kuronode_files must match the exact BLK-SYSTEM-221 feature allowlist")
    if package.get("closeout_traceability") != CLOSEOUT_TRACEABILITY_221:
        errors.append("closeout_traceability must match strict Kuronode MCP closeout evidence")
    if package.get("external_supervised_codex_worker_used") is not False:
        errors.append("external_supervised_codex_worker_used must be false for BLK-SYSTEM-221")
    if package.get("native_workspace_write_recheck_used") is not False:
        errors.append("native_workspace_write_recheck_used must be false because no Codex worker was dispatched")
    if package.get("exact_kuronode_feature_commit_recorded") is not True:
        errors.append("exact_kuronode_feature_commit_recorded must be true")
    if package.get("denied_authorities") != list(DENIED_AUTHORITIES):
        errors.append("denied_authorities must match exact ordered BLK-SYSTEM-220-derived list")
    denied = package.get("denied_authorities")
    if not isinstance(denied, list) or len(denied) != len(set(denied or [])) or not all(isinstance(item, str) for item in (denied or [])):
        errors.append("denied_authorities must be a duplicate-free list of strings")

    for flag in REQUIRED_FALSE_SIDE_EFFECT_FLAGS:
        if package.get(flag) is not False:
            errors.append(f"{flag} must remain false")

    calculated = canonical_package_hash(package)
    if package.get("package_hash") != calculated:
        errors.append("package_hash must equal canonical package hash")

    for key in ("kuronode_parent_commit", "kuronode_feature_worker_commit", "kuronode_feature_merge_commit"):
        value = package.get(key)
        if not isinstance(value, str) or len(value) != 40 or any(ch not in "0123456789abcdef" for ch in value):
            errors.append(f"{key} must be a 40-character lowercase hex commit")

    validation = package.get("validation_evidence")
    if not isinstance(validation, dict):
        errors.append("validation_evidence must be an object")
    else:
        for key in ("focused_test", "graph_test_suite", "graph_build", "diff_check", "reverse_apply_check"):
            if key not in validation:
                errors.append(f"validation_evidence.{key} is required")

    errors.extend(_scan_caller_controlled(package))
    return errors
