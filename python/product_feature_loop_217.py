"""BLK-SYSTEM-217 external Codex exact-undo exercise evidence.

This module records a bounded, non-mutating exact undo/revert exercise for the
BLK-SYSTEM-215 Codex-assisted Kuronode feature. The exercise ran in a disposable
Kuronode worktree and verified the bound reverse patch with Codex 0.130.0
telemetry enabled. It does not grant live Codex dispatch, BLK-pipe runtime,
BEB/BEO execution, protected-body access, package/network tooling, or blanket
future Kuronode source/Git mutation authority.
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
    DEFAULT_216_PACKAGE_HASH,
    DENIED_AUTHORITIES,
    REQUIRED_FALSE_SIDE_EFFECT_FLAGS,
    canonical_package_hash,
)
from product_feature_loop_213_214 import KURONODE_REPO

UPSTREAM_BLK216_PACKAGE_HASH = DEFAULT_216_PACKAGE_HASH
KURONODE_FEATURE_PARENT_COMMIT_217 = "40f908b2a5d94991c2502018167d3a1c57031b2d"
KURONODE_FEATURE_MERGE_COMMIT_217 = "35605698633d41c7fc5f0f84548a7b56e3782530"
KURONODE_UNDO_PATCH_HASH_217 = "sha256:088a62b1d73e0dec3f621ff2f44b62a3a94fa4f5998f2ef03a8915782a7a8b5e"
CODEX_UNDO_JSONL_HASH_217 = "sha256:9a768b0941f2a3ba699ad72ab2a5a1528e991ce89fdaa4d8ddabef7c77654e5a"
CODEX_UNDO_FINAL_MESSAGE_HASH_217 = "sha256:8a850ea863c9b49f89f79d3fcff8804b96bd031d2795336911c98ed8cd7c7599"
NEXT_FRONTIER_217 = "NEXT_FRONTIER_THIRD_BOUNDED_KURONODE_FEATURE_LOOP_AVAILABLE_AFTER_UNDO_CHECK_NOT_GRANTED"

ALLOWED_KURONODE_FILES_217 = (
    "docs/execution briefs/BEB-K2-001_Codex_Projection_Summary_Badges.md",
    "docs/execution briefs/BEO-K2-001_Codex_Projection_Summary_Badges_Outcome.md",
    "packages/kuronode-graph/src/components/CanonicalDataGrid.test.tsx",
    "packages/kuronode-graph/src/components/CanonicalDataGrid.tsx",
)

UNDO_VERIFICATION_COMMANDS_217 = (
    "git status --short",
    "git diff --binary 40f908b2a5d94991c2502018167d3a1c57031b2d 35605698633d41c7fc5f0f84548a7b56e3782530 -- 'packages/kuronode-graph/src/components/CanonicalDataGrid.tsx' 'packages/kuronode-graph/src/components/CanonicalDataGrid.test.tsx' 'docs/execution briefs/BEB-K2-001_Codex_Projection_Summary_Badges.md' 'docs/execution briefs/BEO-K2-001_Codex_Projection_Summary_Badges_Outcome.md' > /tmp/kuronode-blk217-undo-blk215.patch",
    "test -s /tmp/kuronode-blk217-undo-blk215.patch",
    "printf '088a62b1d73e0dec3f621ff2f44b62a3a94fa4f5998f2ef03a8915782a7a8b5e  /tmp/kuronode-blk217-undo-blk215.patch\\n' | sha256sum --check --strict -",
    "git apply --reverse --check /tmp/kuronode-blk217-undo-blk215.patch",
    "git status --short",
)

CODEX_INVOCATION_217 = {
    "model": "gpt-5.5",
    "reasoning_effort": "high",
    "sandbox": "danger-full-access inside disposable external worktree",
    "approval_mode": "never",
    "worktree": "temporary_worktree:/tmp/kuronode-blk217-undo",
    "ephemeral": True,
    "user_config_ignored": True,
    "rules_ignored": True,
    "hooks_disabled": True,
    "plugins_disabled": True,
    "goals_disabled": True,
    "json_telemetry_enabled": True,
    "output_last_message": "/tmp/blk217-codex-artifacts/final-message.md",
}

PACKAGE_217_KEYS = {
    "sprint_id",
    "status",
    "upstream_216_package_hash",
    "undo_target",
    "kuronode_repo",
    "kuronode_feature_parent_commit",
    "kuronode_feature_merge_commit",
    "allowed_kuronode_files",
    "undo_verification_commands",
    "undo_patch_sha256",
    "undo_patch_non_empty",
    "sha256_check_passed",
    "reverse_apply_check_passed",
    "final_git_status_short",
    "target_repo_commit_made",
    "tracked_file_mutation_remained",
    "codex_invocation",
    "external_supervised_codex_worker_used",
    "codex_telemetry",
    "undo_findings",
    "next_frontier",
    "denied_authorities",
    "operator_notes",
    "caller_supplied_evidence_refs",
    "package_hash",
    *REQUIRED_FALSE_SIDE_EFFECT_FLAGS,
}

CALLER_CONTROLLED_FIELDS = ("operator_notes", "caller_supplied_evidence_refs")
FORBIDDEN_COMPACT_TOKENS = {
    "codexapproval",
    "livecodexexecutionauthorized",
    "codexexecutionauthorized",
    "reusablecodexdispatch",
    "blanketkuronodesourcemutation",
    "blanketsourcemutation",
    "sourcegitmutationauthorized",
    "targetgitmutationauthorized",
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


def _base_217() -> dict[str, Any]:
    return {
        "sprint_id": "BLK-SYSTEM-217",
        "status": "CODEX_EXTERNAL_EXACT_UNDO_EXERCISE_RECORDED",
        "upstream_216_package_hash": UPSTREAM_BLK216_PACKAGE_HASH,
        "undo_target": "BLK-SYSTEM-215 CanonicalDataGrid projection summary badges",
        "kuronode_repo": KURONODE_REPO,
        "kuronode_feature_parent_commit": KURONODE_FEATURE_PARENT_COMMIT_217,
        "kuronode_feature_merge_commit": KURONODE_FEATURE_MERGE_COMMIT_217,
        "allowed_kuronode_files": list(ALLOWED_KURONODE_FILES_217),
        "undo_verification_commands": list(UNDO_VERIFICATION_COMMANDS_217),
        "undo_patch_sha256": KURONODE_UNDO_PATCH_HASH_217,
        "undo_patch_non_empty": True,
        "sha256_check_passed": True,
        "reverse_apply_check_passed": True,
        "final_git_status_short": "",
        "target_repo_commit_made": False,
        "tracked_file_mutation_remained": False,
        "codex_invocation": copy.deepcopy(CODEX_INVOCATION_217),
        "external_supervised_codex_worker_used": True,
        "codex_telemetry": {
            "events_jsonl_sha256": CODEX_UNDO_JSONL_HASH_217,
            "final_message_sha256": CODEX_UNDO_FINAL_MESSAGE_HASH_217,
            "events_jsonl_line_count": 21,
            "authoritative_evidence": False,
            "authoritative_evidence_source": "git status, patch SHA256, and git apply --reverse --check outside Codex telemetry",
        },
        "undo_findings": [
            "Exact reverse-patch check for the BLK-SYSTEM-215 Codex feature passed",
            "Bound patch was non-empty and matched the previously recorded SHA256",
            "Disposable worktree remained clean and no commit was made",
            "Codex telemetry captured the drill but remains advisory rather than authority evidence",
        ],
        "next_frontier": NEXT_FRONTIER_217,
        "denied_authorities": list(DENIED_AUTHORITIES),
        "operator_notes": [
            "User asked Hermes to plan and execute the next BLK-System sprint; Hermes selected the safer exact undo exercise from the BLK-077/079 fork.",
            "Codex was used as an external tactical worker in a disposable worktree; BLK-System internal live-dispatch authority remains denied.",
        ],
        "caller_supplied_evidence_refs": {},
        **_false_flags(),
    }


DEFAULT_217_PACKAGE_HASH = canonical_package_hash(_base_217())


def build_217_codex_exact_undo_exercise_package() -> dict[str, Any]:
    return _with_hash(_base_217())


def validate_217_codex_exact_undo_exercise_package(package: dict[str, Any]) -> list[str]:
    if not isinstance(package, dict):
        return ["BLK-SYSTEM-217 package must be an object"]
    errors: list[str] = []
    keys = set(package)
    if keys != PACKAGE_217_KEYS:
        errors.append(f"BLK-SYSTEM-217 package keys must be exact; missing={sorted(PACKAGE_217_KEYS - keys)} extra={sorted(keys - PACKAGE_217_KEYS)}")
    if package.get("sprint_id") != "BLK-SYSTEM-217":
        errors.append("sprint_id must be BLK-SYSTEM-217")
    if package.get("status") != "CODEX_EXTERNAL_EXACT_UNDO_EXERCISE_RECORDED":
        errors.append("status must record external Codex exact undo exercise")
    if package.get("upstream_216_package_hash") != DEFAULT_216_PACKAGE_HASH:
        errors.append("upstream_216_package_hash must be canonical BLK-SYSTEM-216 hash")
    if package.get("undo_target") != "BLK-SYSTEM-215 CanonicalDataGrid projection summary badges":
        errors.append("undo_target must match exact BLK-SYSTEM-215 feature")
    if package.get("kuronode_repo") != KURONODE_REPO:
        errors.append("kuronode_repo must match exact target repo")
    for key in ("kuronode_feature_parent_commit", "kuronode_feature_merge_commit"):
        value = package.get(key)
        if not isinstance(value, str) or len(value) != 40:
            errors.append(f"{key} must be a full 40-character Git commit")
    if package.get("kuronode_feature_parent_commit") != KURONODE_FEATURE_PARENT_COMMIT_217:
        errors.append("kuronode_feature_parent_commit must match exact pre-feature commit")
    if package.get("kuronode_feature_merge_commit") != KURONODE_FEATURE_MERGE_COMMIT_217:
        errors.append("kuronode_feature_merge_commit must match exact feature merge commit")
    if package.get("allowed_kuronode_files") != list(ALLOWED_KURONODE_FILES_217):
        errors.append("allowed_kuronode_files must match exact reverse-patch file scope")
    if package.get("undo_verification_commands") != list(UNDO_VERIFICATION_COMMANDS_217):
        errors.append("undo_verification_commands must match exact observed command list")
    if package.get("undo_patch_sha256") != KURONODE_UNDO_PATCH_HASH_217:
        errors.append("undo_patch_sha256 must match exact bound BLK-SYSTEM-215 feature patch hash")
    for key in ("undo_patch_non_empty", "sha256_check_passed", "reverse_apply_check_passed"):
        if package.get(key) is not True:
            errors.append(f"{key} must be true")
    if package.get("final_git_status_short") != "":
        errors.append("final_git_status_short must be empty")
    if package.get("target_repo_commit_made") is not False:
        errors.append("target_repo_commit_made must be false")
    if package.get("tracked_file_mutation_remained") is not False:
        errors.append("tracked_file_mutation_remained must be false")
    if package.get("codex_invocation") != CODEX_INVOCATION_217:
        errors.append("codex_invocation must match exact observed Codex run")
    if package.get("external_supervised_codex_worker_used") is not True:
        errors.append("external_supervised_codex_worker_used must be true for BLK-SYSTEM-217 evidence")
    if package.get("codex_telemetry") != _base_217()["codex_telemetry"]:
        errors.append("codex_telemetry must match exact advisory telemetry hashes")
    if package.get("undo_findings") != _base_217()["undo_findings"]:
        errors.append("undo_findings must match exact findings")
    if package.get("next_frontier") != NEXT_FRONTIER_217:
        errors.append("next_frontier must remain not granted")
    errors.extend(_validate_denied_authorities(package))
    errors.extend(_validate_false_flags(package))
    errors.extend(_scan_caller_controlled(package))
    errors.extend(_validate_hash(package, DEFAULT_217_PACKAGE_HASH))
    return errors
