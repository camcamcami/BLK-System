"""BLK-SYSTEM-215 supervised Codex Kuronode feature-loop evidence.

BLK-SYSTEM-215 records one bounded Kuronode feature implemented through an
external Hermes-supervised Codex worker. It proves the exact Codex-assisted
feature commit, validation, strict Kuronode closeout, and reverse-patch evidence
without converting that run into reusable BLK-System live Codex dispatch,
BLK-pipe runtime, protected-body access, BEO/RTM authority, package/network
permission, or blanket future Kuronode source/Git mutation.
"""

from __future__ import annotations

import copy
from typing import Any

from blk_authority_smuggling import (
    compact_authority_text,
    decoded_authority_variants,
    scan_for_authority_laundering,
)
from product_feature_loop_213_214 import (
    DEFAULT_214_PACKAGE_HASH,
    DENIED_AUTHORITIES,
    KURONODE_REPO,
    REQUIRED_FALSE_SIDE_EFFECT_FLAGS,
    canonical_package_hash,
)

UPSTREAM_BLK214_FEATURE_LOOP_HASH = DEFAULT_214_PACKAGE_HASH
KURONODE_PARENT_COMMIT_215 = "40f908b2a5d94991c2502018167d3a1c57031b2d"
KURONODE_CODEX_WORKER_COMMIT_215 = "148d74b57febe828be359511488b3379622d132c"
KURONODE_FEATURE_MERGE_COMMIT_215 = "35605698633d41c7fc5f0f84548a7b56e3782530"
KURONODE_FEATURE_PATCH_HASH_215 = "sha256:088a62b1d73e0dec3f621ff2f44b62a3a94fa4f5998f2ef03a8915782a7a8b5e"
NEXT_FRONTIER_215 = "NEXT_FRONTIER_THIRD_BOUNDED_KURONODE_FEATURE_LOOP_OR_OPERATOR_SELECTED_UNDO_NOT_GRANTED"

ALLOWED_KURONODE_FILES_215 = (
    "docs/execution briefs/BEB-K2-001_Codex_Projection_Summary_Badges.md",
    "docs/execution briefs/BEO-K2-001_Codex_Projection_Summary_Badges_Outcome.md",
    "packages/kuronode-graph/src/components/CanonicalDataGrid.test.tsx",
    "packages/kuronode-graph/src/components/CanonicalDataGrid.tsx",
)

KURONODE_VALIDATION_COMMANDS_215 = (
    "npm run test -w @kuronode/kuronode-graph -- src/components/CanonicalDataGrid.test.tsx",
    "npm run test -w @kuronode/kuronode-graph -- tests/GraphProjectionEngine.test.ts src/components/CanonicalDataGrid.test.tsx",
    "npm run test -w @kuronode/kuronode-graph",
    "npm run build -w @kuronode/kuronode-graph",
)

UNDO_VERIFICATION_COMMANDS_215 = (
    "git diff --binary 40f908b2a5d94991c2502018167d3a1c57031b2d 35605698633d41c7fc5f0f84548a7b56e3782530 -- 'packages/kuronode-graph/src/components/CanonicalDataGrid.tsx' 'packages/kuronode-graph/src/components/CanonicalDataGrid.test.tsx' 'docs/execution briefs/BEB-K2-001_Codex_Projection_Summary_Badges.md' 'docs/execution briefs/BEO-K2-001_Codex_Projection_Summary_Badges_Outcome.md' > /tmp/kuronode-blk215.patch",
    "test -s /tmp/kuronode-blk215.patch",
    "printf '088a62b1d73e0dec3f621ff2f44b62a3a94fa4f5998f2ef03a8915782a7a8b5e  /tmp/kuronode-blk215.patch\\n' | sha256sum --check --strict -",
    "git apply --reverse --check /tmp/kuronode-blk215.patch",
)

CODEX_INVOCATION_215 = {
    "model": "gpt-5.5",
    "reasoning_effort": "high",
    "sandbox": "danger-full-access",
    "approval_mode": "never",
    "isolation": "temporary_worktree:/tmp/kuronode-codex-feature-215",
    "user_config_ignored": True,
    "rules_ignored": True,
    "ephemeral": True,
}

CLOSEOUT_TRACEABILITY_215 = {
    "existingRequirements": ["R-UIX-040", "R-PRJ-048"],
    "existingUseCases": ["UC-REQ-004"],
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
    "reusablecodexdispatchauthorized",
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

PACKAGE_215_KEYS = {
    "sprint_id",
    "status",
    "upstream_214_package_hash",
    "feature_name",
    "kuronode_repo",
    "kuronode_parent_commit",
    "kuronode_codex_worker_commit",
    "kuronode_feature_merge_commit",
    "allowed_kuronode_files",
    "kuronode_validation_commands",
    "undo_verification_commands",
    "kuronode_feature_patch_hash",
    "codex_invocation",
    "external_supervised_codex_worker_used",
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


def _with_hash(package: dict[str, Any]) -> dict[str, Any]:
    finalized = copy.deepcopy(package)
    finalized["package_hash"] = canonical_package_hash(finalized)
    return finalized


def _false_flags() -> dict[str, bool]:
    return {flag: False for flag in REQUIRED_FALSE_SIDE_EFFECT_FLAGS}


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
    return [f"{flag} must be explicit false" for flag in REQUIRED_FALSE_SIDE_EFFECT_FLAGS if package.get(flag) is not False]


def _validate_exact_keys(package: dict[str, Any]) -> list[str]:
    keys = set(package)
    if keys != PACKAGE_215_KEYS:
        return [f"BLK-SYSTEM-215 package keys must be exact; missing={sorted(PACKAGE_215_KEYS - keys)} extra={sorted(keys - PACKAGE_215_KEYS)}"]
    return []


def _validate_hash(package: dict[str, Any], expected_hash: str | None = None) -> list[str]:
    actual = package.get("package_hash")
    calculated = canonical_package_hash(package)
    errors: list[str] = []
    if actual != calculated:
        errors.append("package_hash must equal canonical package hash")
    if expected_hash is not None and actual != expected_hash:
        errors.append(f"package_hash must match canonical default {expected_hash}")
    return errors


def _base_215() -> dict[str, Any]:
    return {
        "sprint_id": "BLK-SYSTEM-215",
        "status": "SUPERVISED_CODEX_KURONODE_FEATURE_LOOP_EXECUTED",
        "upstream_214_package_hash": UPSTREAM_BLK214_FEATURE_LOOP_HASH,
        "feature_name": "CanonicalDataGrid projection summary badges",
        "kuronode_repo": KURONODE_REPO,
        "kuronode_parent_commit": KURONODE_PARENT_COMMIT_215,
        "kuronode_codex_worker_commit": KURONODE_CODEX_WORKER_COMMIT_215,
        "kuronode_feature_merge_commit": KURONODE_FEATURE_MERGE_COMMIT_215,
        "allowed_kuronode_files": list(ALLOWED_KURONODE_FILES_215),
        "kuronode_validation_commands": list(KURONODE_VALIDATION_COMMANDS_215),
        "undo_verification_commands": list(UNDO_VERIFICATION_COMMANDS_215),
        "kuronode_feature_patch_hash": KURONODE_FEATURE_PATCH_HASH_215,
        "codex_invocation": copy.deepcopy(CODEX_INVOCATION_215),
        "external_supervised_codex_worker_used": True,
        "closeout_traceability": copy.deepcopy(CLOSEOUT_TRACEABILITY_215),
        "feature_loop_findings": [
            "Second bounded Kuronode feature loop executed with external supervised Codex assistance",
            "CanonicalDataGrid now displays full projected row, shared trace, warning, root, and max-depth metrics from GraphProjectionEngine summary output",
            "Kuronode focused tests, graph package test suite, graph package build, strict MCP closeout, and reverse-patch check passed",
            "The Codex run remains sprint-local evidence and does not authorize reusable BLK-System live Codex dispatch",
        ],
        "next_frontier": NEXT_FRONTIER_215,
        "exact_kuronode_feature_commit_recorded": True,
        "denied_authorities": list(DENIED_AUTHORITIES),
        "operator_notes": [
            "User explicitly selected the next feature sprint and asked Hermes to use Codex for it.",
            "Codex was used as an external tactical worker in a temporary worktree; BLK-System internal live-dispatch authority remains denied.",
        ],
        "caller_supplied_evidence_refs": {},
        **_false_flags(),
    }


DEFAULT_215_PACKAGE_HASH = canonical_package_hash(_base_215())


def build_215_supervised_codex_feature_loop_package() -> dict[str, Any]:
    return _with_hash(_base_215())


def validate_215_supervised_codex_feature_loop_package(package: dict[str, Any]) -> list[str]:
    if not isinstance(package, dict):
        return ["BLK-SYSTEM-215 package must be an object"]
    errors: list[str] = []
    errors.extend(_validate_exact_keys(package))
    if package.get("sprint_id") != "BLK-SYSTEM-215":
        errors.append("sprint_id must be BLK-SYSTEM-215")
    if package.get("status") != "SUPERVISED_CODEX_KURONODE_FEATURE_LOOP_EXECUTED":
        errors.append("status must record supervised Codex Kuronode feature loop execution")
    if package.get("upstream_214_package_hash") != DEFAULT_214_PACKAGE_HASH:
        errors.append("upstream_214_package_hash must be canonical BLK-SYSTEM-214 hash")
    if package.get("feature_name") != "CanonicalDataGrid projection summary badges":
        errors.append("feature_name must match exact feature")
    if package.get("kuronode_repo") != KURONODE_REPO:
        errors.append("kuronode_repo must match exact target repo")
    for key in ("kuronode_parent_commit", "kuronode_codex_worker_commit", "kuronode_feature_merge_commit"):
        value = package.get(key)
        if not isinstance(value, str) or len(value) != 40:
            errors.append(f"{key} must be a full 40-character Git commit")
    if package.get("kuronode_parent_commit") != KURONODE_PARENT_COMMIT_215:
        errors.append("kuronode_parent_commit must match exact pre-feature main commit")
    if package.get("kuronode_codex_worker_commit") != KURONODE_CODEX_WORKER_COMMIT_215:
        errors.append("kuronode_codex_worker_commit must match exact worker commit")
    if package.get("kuronode_feature_merge_commit") != KURONODE_FEATURE_MERGE_COMMIT_215:
        errors.append("kuronode_feature_merge_commit must match exact pushed main merge commit")
    if package.get("allowed_kuronode_files") != list(ALLOWED_KURONODE_FILES_215):
        errors.append("allowed_kuronode_files must match exact Codex feature allowlist")
    if package.get("kuronode_validation_commands") != list(KURONODE_VALIDATION_COMMANDS_215):
        errors.append("kuronode_validation_commands must match exact verification list")
    if package.get("undo_verification_commands") != list(UNDO_VERIFICATION_COMMANDS_215):
        errors.append("undo_verification_commands must match exact reverse-patch checks")
    if package.get("kuronode_feature_patch_hash") != KURONODE_FEATURE_PATCH_HASH_215:
        errors.append("kuronode_feature_patch_hash must match exact feature diff patch hash")
    if package.get("codex_invocation") != CODEX_INVOCATION_215:
        errors.append("codex_invocation must match exact supervised external Codex invocation evidence")
    if package.get("external_supervised_codex_worker_used") is not True:
        errors.append("external_supervised_codex_worker_used must be true for BLK-SYSTEM-215 evidence")
    if package.get("closeout_traceability") != CLOSEOUT_TRACEABILITY_215:
        errors.append("closeout_traceability must match exact Kuronode MCP closeout traceability")
    if package.get("feature_loop_findings") != _base_215()["feature_loop_findings"]:
        errors.append("feature_loop_findings must match exact supervised Codex feature-loop findings")
    if package.get("next_frontier") != NEXT_FRONTIER_215:
        errors.append("next frontier must remain not granted")
    if package.get("exact_kuronode_feature_commit_recorded") is not True:
        errors.append("exact_kuronode_feature_commit_recorded must be true")
    errors.extend(_validate_denied_authorities(package))
    errors.extend(_validate_false_flags(package))
    errors.extend(_scan_caller_controlled(package))
    errors.extend(_validate_hash(package, DEFAULT_215_PACKAGE_HASH))
    return errors
