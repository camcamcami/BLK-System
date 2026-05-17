"""BLK-SYSTEM-218 third bounded Kuronode feature-loop evidence.

This module records one tiny Kuronode UI feature implemented through an external
Hermes-supervised Codex worker in a disposable worktree: CanonicalDataGrid now
shows the selected canonical requirement in the header. The evidence binds exact
Kuronode commits, patch hash, Codex telemetry, strict Kuronode closeout, and
validation output without granting reusable Codex dispatch, BLK-pipe runtime,
BEB/BEO execution, RTM authority, protected-body access, package/network tooling,
or blanket future Kuronode source/Git mutation authority.
"""

from __future__ import annotations

import copy
from typing import Any

from blk_authority_smuggling import (
    compact_authority_text,
    decoded_authority_variants,
    scan_for_authority_laundering,
)
from product_codex_config_containment_216 import (
    DENIED_AUTHORITIES,
    REQUIRED_FALSE_SIDE_EFFECT_FLAGS,
    canonical_package_hash,
)
from product_feature_loop_213_214 import KURONODE_REPO
from product_feature_loop_217 import DEFAULT_217_PACKAGE_HASH

UPSTREAM_BLK217_PACKAGE_HASH = DEFAULT_217_PACKAGE_HASH
KURONODE_FEATURE_PARENT_COMMIT_218 = "35605698633d41c7fc5f0f84548a7b56e3782530"
KURONODE_FEATURE_WORKER_COMMIT_218 = "27dc4f682ed84cf351764e97adef5010773322b1"
KURONODE_FEATURE_MERGE_COMMIT_218 = "af208ea57604707c7ae2b768f4f480d4c42ce7cf"
KURONODE_FEATURE_PATCH_HASH_218 = "sha256:e05df098cc5cc331966d07cda102689f3cd3388c949c23b6076dd348faae3533"
BLK218_CODEX_EVENTS_HASH = "sha256:671165d649ba500c2d259258015aa256de8b81130ace07dcaca4eea74686313e"
BLK218_CODEX_FINAL_MESSAGE_HASH = "sha256:0345fff9a147b6dd0014a82cce4865277c7d5b13222ccd79694b6d122670cc10"
BLK218_CODEX_PROMPT_HASH = "sha256:e80baf2fbe862c04a525cd5b30200ba91f37e14773934a33bb4b73bb88811f9a"
BLK218_KURONODE_CLOSEOUT_HASH = "sha256:4ca225e5731c30b9fe4e3e132668cac0d6473d337aa335272d35342f16cb0b41"
NEXT_FRONTIER_218 = "NEXT_FRONTIER_OPERATOR_SELECTED_BOUNDED_KURONODE_FEATURE_OR_OBSERVED_FAILURE_HARDENING_NOT_GRANTED"

ALLOWED_KURONODE_FILES_218 = (
    "packages/kuronode-graph/src/components/CanonicalDataGrid.test.tsx",
    "packages/kuronode-graph/src/components/CanonicalDataGrid.tsx",
)

KURONODE_VALIDATION_COMMANDS_218 = (
    "npm run test -w @kuronode/kuronode-graph -- CanonicalDataGrid.test.tsx",
    "npm run build -w @kuronode/kuronode-graph",
    "npm run test -w @kuronode/kuronode-graph",
    "git diff --check -- packages/kuronode-graph/src/components/CanonicalDataGrid.test.tsx packages/kuronode-graph/src/components/CanonicalDataGrid.tsx",
)

CODEX_INVOCATION_218 = {
    "model": "gpt-5.5",
    "reasoning_effort": "high",
    "sandbox": "danger-full-access inside disposable external worktree",
    "approval_mode": "never",
    "worktree": "temporary_worktree:/tmp/kuronode-blk218-feature",
    "ephemeral": True,
    "user_config_ignored": True,
    "rules_ignored": True,
    "hooks_disabled": True,
    "plugins_disabled": True,
    "goals_disabled": True,
    "json_telemetry_enabled": True,
    "output_last_message": "/tmp/blk218-codex-artifacts/final-message.md",
}

CLOSEOUT_TRACEABILITY_218 = {
    "existingRequirements": ["R-UIX-040", "R-PRJ-048"],
    "existingUseCases": ["UC-REQ-004"],
    "newRequirements": [],
    "newUseCases": [],
    "mcpCloseoutStatus": "PASS_STRICT",
    "closeout_hash": BLK218_KURONODE_CLOSEOUT_HASH,
}

PACKAGE_218_KEYS = {
    "sprint_id",
    "status",
    "upstream_217_package_hash",
    "feature_name",
    "kuronode_repo",
    "kuronode_parent_commit",
    "kuronode_feature_worker_commit",
    "kuronode_feature_merge_commit",
    "allowed_kuronode_files",
    "kuronode_validation_commands",
    "kuronode_feature_patch_hash",
    "codex_invocation",
    "external_supervised_codex_worker_used",
    "codex_telemetry",
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
    "blktestoracleauthority",
    "blanketkuronodesourcemutation",
    "blanketsourcemutation",
    "sourcegitmutationauthorized",
    "targetgitmutationauthorized",
    "runtimeapproval",
    "runtimeexecutionauthorized",
    "livecodexexecutionauthorized",
    "reusablecodexdispatch",
    "codexapproval",
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
    "productionsandboxenforced",
    "productionisolationclaim",
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


def _validate_exact_keys(package: dict[str, Any]) -> list[str]:
    keys = set(package)
    if keys != PACKAGE_218_KEYS:
        return [f"BLK-SYSTEM-218 package keys must be exact; missing={sorted(PACKAGE_218_KEYS - keys)} extra={sorted(keys - PACKAGE_218_KEYS)}"]
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
    return [f"{flag} must be explicit false" for flag in REQUIRED_FALSE_SIDE_EFFECT_FLAGS if package.get(flag) is not False]


def _validate_hash(package: dict[str, Any], expected_hash: str | None = None) -> list[str]:
    actual = package.get("package_hash")
    calculated = canonical_package_hash(package)
    errors: list[str] = []
    if actual != calculated:
        errors.append("package_hash must equal canonical package hash")
    if expected_hash is not None and actual != expected_hash:
        errors.append(f"package_hash must match canonical default {expected_hash}")
    return errors


def _base_218() -> dict[str, Any]:
    return {
        "sprint_id": "BLK-SYSTEM-218",
        "status": "THIRD_BOUNDED_KURONODE_FEATURE_LOOP_EXECUTED",
        "upstream_217_package_hash": UPSTREAM_BLK217_PACKAGE_HASH,
        "feature_name": "CanonicalDataGrid selected requirement header badge",
        "kuronode_repo": KURONODE_REPO,
        "kuronode_parent_commit": KURONODE_FEATURE_PARENT_COMMIT_218,
        "kuronode_feature_worker_commit": KURONODE_FEATURE_WORKER_COMMIT_218,
        "kuronode_feature_merge_commit": KURONODE_FEATURE_MERGE_COMMIT_218,
        "allowed_kuronode_files": list(ALLOWED_KURONODE_FILES_218),
        "kuronode_validation_commands": list(KURONODE_VALIDATION_COMMANDS_218),
        "kuronode_feature_patch_hash": KURONODE_FEATURE_PATCH_HASH_218,
        "codex_invocation": copy.deepcopy(CODEX_INVOCATION_218),
        "external_supervised_codex_worker_used": True,
        "codex_telemetry": {
            "events_jsonl_sha256": BLK218_CODEX_EVENTS_HASH,
            "final_message_sha256": BLK218_CODEX_FINAL_MESSAGE_HASH,
            "prompt_sha256": BLK218_CODEX_PROMPT_HASH,
            "events_jsonl_line_count": 43,
            "authoritative_evidence": False,
            "authoritative_evidence_source": "Hermes git diff, test, build, hash, and MCP closeout verification outside Codex telemetry",
        },
        "tdd_evidence": {
            "red_focused_test": "RED: selected-header test failed because Selected R-SELECTED was absent; 1 failed, 2 passed",
            "green_focused_test": "GREEN: CanonicalDataGrid.test.tsx passed with 3 passed",
            "test_first_observed": True,
        },
        "validation_evidence": {
            "focused_test": "CanonicalDataGrid.test.tsx: 3 passed",
            "graph_test_suite": "@kuronode/kuronode-graph vitest: 16 files passed, 54 passed",
            "graph_build": "npm run build -w @kuronode/kuronode-graph exited 0 with existing Vite chunk warnings",
            "diff_check": "git diff --check passed for exact changed paths",
        },
        "closeout_traceability": copy.deepcopy(CLOSEOUT_TRACEABILITY_218),
        "feature_loop_findings": [
            "Third bounded Kuronode feature loop executed with external supervised Codex assistance",
            "CanonicalDataGrid now displays a compact selected canonical requirement badge in the header while preserving the loaded count",
            "Focused RED/GREEN test, graph test suite, graph package build, strict MCP closeout, and exact patch hash evidence passed",
            "Codex telemetry captured the run but remains advisory rather than authority evidence",
            "Codex attempted repository-local closeout discovery unsuccessfully; Hermes performed the strict MCP closeout via stdio before accepting the feature",
        ],
        "post_merge_git_status_short": "",
        "next_frontier": NEXT_FRONTIER_218,
        "exact_kuronode_feature_commit_recorded": True,
        "denied_authorities": list(DENIED_AUTHORITIES),
        "operator_notes": [
            "User asked Hermes to plan and execute the next BLK-System sprint; Hermes selected one tiny Kuronode requirements-grid UI feature.",
            "Codex was used as an external tactical worker in a disposable worktree; BLK-System internal live-dispatch authority remains denied.",
        ],
        "caller_supplied_evidence_refs": {},
        **_false_flags(),
    }


DEFAULT_218_PACKAGE_HASH = canonical_package_hash(_base_218())


def build_218_selected_requirement_badge_feature_package() -> dict[str, Any]:
    return _with_hash(_base_218())


def validate_218_selected_requirement_badge_feature_package(package: dict[str, Any]) -> list[str]:
    if not isinstance(package, dict):
        return ["BLK-SYSTEM-218 package must be an object"]

    errors: list[str] = []
    errors.extend(_validate_exact_keys(package))
    errors.extend(_validate_denied_authorities(package))
    errors.extend(_validate_false_flags(package))
    errors.extend(_validate_hash(package, DEFAULT_218_PACKAGE_HASH))
    errors.extend(_scan_caller_controlled(package))

    if package.get("sprint_id") != "BLK-SYSTEM-218":
        errors.append("sprint_id must be BLK-SYSTEM-218")
    if package.get("status") != "THIRD_BOUNDED_KURONODE_FEATURE_LOOP_EXECUTED":
        errors.append("status must record third bounded feature loop execution")
    if package.get("upstream_217_package_hash") != UPSTREAM_BLK217_PACKAGE_HASH:
        errors.append("upstream_217_package_hash must match BLK-SYSTEM-217")
    if package.get("allowed_kuronode_files") != list(ALLOWED_KURONODE_FILES_218):
        errors.append("allowed_kuronode_files must match the exact BLK-SYSTEM-218 feature allowlist")
    if package.get("kuronode_feature_patch_hash") != KURONODE_FEATURE_PATCH_HASH_218:
        errors.append("kuronode_feature_patch_hash must match exact BLK-SYSTEM-218 patch hash")
    if package.get("post_merge_git_status_short") != "":
        errors.append("post_merge_git_status_short must be clean")
    if package.get("next_frontier") != NEXT_FRONTIER_218:
        errors.append("next_frontier must remain operator-selected and not granted")
    if package.get("exact_kuronode_feature_commit_recorded") is not True:
        errors.append("exact_kuronode_feature_commit_recorded must be true")

    for key in ("kuronode_parent_commit", "kuronode_feature_worker_commit", "kuronode_feature_merge_commit"):
        value = package.get(key)
        if not isinstance(value, str) or len(value) != 40 or any(ch not in "0123456789abcdef" for ch in value):
            errors.append(f"{key} must be a 40-character lowercase hex commit")

    closeout = package.get("closeout_traceability")
    if closeout != CLOSEOUT_TRACEABILITY_218:
        errors.append("closeout_traceability must match strict Kuronode MCP closeout evidence")

    telemetry = package.get("codex_telemetry")
    if not isinstance(telemetry, dict):
        errors.append("codex_telemetry must be an object")
    else:
        expected = {
            "events_jsonl_sha256": BLK218_CODEX_EVENTS_HASH,
            "final_message_sha256": BLK218_CODEX_FINAL_MESSAGE_HASH,
            "prompt_sha256": BLK218_CODEX_PROMPT_HASH,
            "events_jsonl_line_count": 43,
            "authoritative_evidence": False,
        }
        for key, value in expected.items():
            if telemetry.get(key) != value:
                errors.append(f"codex_telemetry.{key} must match BLK-SYSTEM-218 recorded value")

    return errors
