"""BLK-SYSTEM-216 Codex configuration containment drill evidence.

This module records a non-executing containment drill for modern Codex CLI
permission-profile configuration. It builds deterministic evidence dictionaries
only. It does not invoke Codex, subprocesses, Git, BLK-pipe, BLK-test, network
clients, package managers, protected BLK-req readers, BEO tooling, or RTM tooling.
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
from product_feature_loop_215 import DEFAULT_215_PACKAGE_HASH

UPSTREAM_BLK215_PACKAGE_HASH = DEFAULT_215_PACKAGE_HASH
CODEX_CONFIG_DOC_ID = "BLK-121"
BLK121_DOC_PATH = "docs/BLK-121_codex-configuration-and-containment-contract.md"
NEXT_FRONTIER_216 = "NEXT_FRONTIER_THIRD_BOUNDED_KURONODE_FEATURE_LOOP_OR_EXACT_UNDO_WITH_CODEX_PROFILE_CONTAINMENT_AVAILABLE_NOT_GRANTED"

DENIED_AUTHORITIES = (
    "LIVE_CODEX_DISPATCH",
    "TACTICAL_LLM_DISPATCH",
    "REUSABLE_CODEX_DISPATCH",
    "CODEX_APPROVAL_AS_RUNTIME_AUTHORITY",
    "BROAD_BLK_PIPE_DISPATCH",
    "BLK_PIPE_RUNTIME_BEYOND_SEPARATE_EXACT_PAYLOAD_AUTHORITY",
    "BLK_TEST_PRODUCTION_MCP_RUNTIME",
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
    "live_codex_dispatch_authorized",
    "tactical_llm_dispatch_authorized",
    "reusable_codex_dispatch_authorized",
    "codex_approval_runtime_authority_authorized",
    "blk_pipe_dispatch_authorized",
    "blk_pipe_runtime_authorized",
    "production_blk_test_mcp_authorized",
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
    "native_sandbox_enforced",
    "production_isolation_claimed",
)

PACKAGE_216_KEYS = {
    "sprint_id",
    "status",
    "upstream_215_package_hash",
    "codex_configuration_doc",
    "codex_configuration_doc_path",
    "codex_cli_version",
    "recommended_codex_invocation",
    "permission_profile_contract",
    "host_sandbox_smoke_result",
    "containment_findings",
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
    "permissionprofileprovesproductionsandbox",
    "productionsandboxenforced",
    "sandboxenforced",
    "productionisolationclaim",
    "docsrequirements",
    "docsusecases",
    "protectedbody",
    "requirementbody",
    "systemshall",
    "npminstall",
    "pipinstall",
    "uvpipinstall",
    "goget",
    "curlhttps",
    "wgethttps",
    "networkaccesstrue",
    "beopublicationgreenlit",
    "publishbeo",
    "rtmgeneration",
    "rtmdriftrejection",
    "privatekey",
    "apikey",
    "authorizationbearer",
}

REQUIRED_PROFILE_ROOTS = {
    ".": "read",
    "packages/kuronode-graph/src/utils/GraphProjectionEngine.ts": "write",
    "packages/kuronode-graph/tests/GraphProjectionEngine.test.ts": "write",
    "packages/kuronode-ui/src/components/CanonicalDataGrid.tsx": "write",
    "packages/kuronode-ui/src/components/CanonicalDataGrid.test.tsx": "write",
    "**/.git/**": "none",
    "**/.env*": "none",
    "**/.codex/**": "none",
    "**/.agents/**": "none",
    "**/node_modules/**": "none",
    "docs/requirements/**": "none",
    "docs/use_cases/**": "none",
    "../**": "none",
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


def _scan_caller_controlled(value: Any, path: str) -> list[str]:
    errors = scan_for_authority_laundering(value, path=path, denied_keys=REQUIRED_FALSE_SIDE_EFFECT_FLAGS)
    if isinstance(value, dict):
        for key, nested in value.items():
            errors.extend(_scan_caller_controlled(nested, f"{path}.{key}"))
    elif isinstance(value, (list, tuple, set)):
        for index, nested in enumerate(value):
            errors.extend(_scan_caller_controlled(nested, f"{path}[{index}]"))
    elif isinstance(value, str):
        for variant in decoded_authority_variants(value):
            compact = compact_authority_text(variant)
            for token in FORBIDDEN_COMPACT_TOKENS:
                if token in compact:
                    errors.append(f"{path} contains forbidden authority/tooling/protected-body wording {token!r}")
    return errors


def _base_216() -> dict[str, Any]:
    return {
        "sprint_id": "BLK-SYSTEM-216",
        "status": "CODEX_PERMISSION_PROFILE_CONTAINMENT_DRILL_RECORDED",
        "upstream_215_package_hash": UPSTREAM_BLK215_PACKAGE_HASH,
        "codex_configuration_doc": CODEX_CONFIG_DOC_ID,
        "codex_configuration_doc_path": BLK121_DOC_PATH,
        "codex_cli_version": "codex-cli 0.130.0",
        "recommended_codex_invocation": {
            "model": "gpt-5.5",
            "reasoning_effort": "high",
            "sandbox_mode": "danger-full-access only inside external containment until native sandbox passes",
            "approval_policy": "never only for non-interactive externally-contained sprint packets",
            "required_args": [
                "codex",
                "--model",
                "gpt-5.5",
                "-c",
                "model_reasoning_effort=\"high\"",
                "-s",
                "danger-full-access",
                "-a",
                "never",
                "exec",
                "--ephemeral",
                "--ignore-user-config",
                "--ignore-rules",
                "--disable",
                "hooks",
                "--disable",
                "plugins",
                "--disable",
                "goals",
                "--json",
                "--output-last-message",
                "artifacts/codex/final-message.md",
                "-C",
                "<externally-contained-worktree>",
            ],
            "disabled_ambient_features": ["hooks", "plugins", "goals"],
            "forbidden_legacy_args": ["--isolated", "--yes", "--dry-run", "--deny-read"],
            "telemetry_required": True,
            "jsonl_telemetry_advisory_only": True,
        },
        "permission_profile_contract": {
            "default_permissions": "blk-kuronode-codex-feature",
            "filesystem": {":project_roots": dict(REQUIRED_PROFILE_ROOTS)},
            "network": {"enabled": False},
            "web_search": "disabled",
            "approval_policy": "never inside external containment; on-request otherwise",
            "glob_scan_max_depth": 4,
            "legacy_exec_deny_read_flags_supported": False,
            "profile_must_fail_closed_when_unavailable": True,
        },
        "host_sandbox_smoke_result": {
            "codex_cli_version": "codex-cli 0.130.0",
            "native_sandbox_status": "HOST_NATIVE_CODEX_SANDBOX_UNAVAILABLE_BWRAP_RTM_NEWADDR",
            "observed_failure": "bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted",
            "permission_profile_requires_direct_runtime_enforcement": True,
            "legacy_landlock_incompatible": True,
            "required_fallback": "DEVCONTAINER_OR_EXTERNAL_SANDBOX_FOR_DANGER_FULL_ACCESS",
        },
        "containment_findings": [
            "Codex 0.130.0 uses permission profiles rather than legacy root exec --deny-read flags.",
            "Sandbox mode and approval policy are separate controls; neither substitutes for exact file-boundary audit.",
            "Local native Linux sandbox is unavailable on this host, so permission-profile policy is contract evidence until an external container or future host sandbox smoke test enforces it directly.",
            "Future Codex-assisted feature loops must persist JSONL telemetry and final-message artifacts as advisory evidence, then rely on Git diff, exact allowlists, tests, and hostile audit as canonical evidence.",
        ],
        "next_frontier": NEXT_FRONTIER_216,
        "denied_authorities": list(DENIED_AUTHORITIES),
        "operator_notes": [],
        "caller_supplied_evidence_refs": {},
        **_false_flags(),
    }


def build_216_codex_config_containment_package() -> dict[str, Any]:
    return _with_hash(_base_216())


DEFAULT_216_PACKAGE_HASH = canonical_package_hash(_base_216())


def validate_216_codex_config_containment_package(package: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(package, dict):
        return ["package must be a dictionary"]
    keys = set(package)
    if keys != PACKAGE_216_KEYS:
        errors.append(f"BLK-SYSTEM-216 keys must be exact; missing={sorted(PACKAGE_216_KEYS - keys)} extra={sorted(keys - PACKAGE_216_KEYS)}")

    expected_scalars = {
        "sprint_id": "BLK-SYSTEM-216",
        "status": "CODEX_PERMISSION_PROFILE_CONTAINMENT_DRILL_RECORDED",
        "upstream_215_package_hash": UPSTREAM_BLK215_PACKAGE_HASH,
        "codex_configuration_doc": CODEX_CONFIG_DOC_ID,
        "codex_configuration_doc_path": BLK121_DOC_PATH,
        "codex_cli_version": "codex-cli 0.130.0",
        "next_frontier": NEXT_FRONTIER_216,
        "package_hash": DEFAULT_216_PACKAGE_HASH,
    }
    for key, expected in expected_scalars.items():
        if package.get(key) != expected:
            errors.append(f"{key} must be {expected!r}")

    if package.get("denied_authorities") != list(DENIED_AUTHORITIES):
        errors.append("denied_authorities must match exact ordered list")
    denied = package.get("denied_authorities")
    if not isinstance(denied, list) or len(denied) != len(set(denied or [])) or not all(isinstance(item, str) for item in (denied or [])):
        errors.append("denied_authorities must be a duplicate-free list of strings")

    for flag in REQUIRED_FALSE_SIDE_EFFECT_FLAGS:
        if package.get(flag) is not False:
            errors.append(f"{flag} must remain false")

    invocation = package.get("recommended_codex_invocation")
    if not isinstance(invocation, dict):
        errors.append("recommended_codex_invocation must be a dictionary")
    else:
        required_args = invocation.get("required_args")
        if not isinstance(required_args, list):
            errors.append("recommended_codex_invocation.required_args must be a list")
            required_args = []
        for required in ("--ephemeral", "--ignore-user-config", "--ignore-rules", "--json", "--output-last-message"):
            if required not in required_args:
                errors.append(f"recommended_codex_invocation missing {required}")
        for forbidden in ("--isolated", "--yes", "--dry-run"):
            if forbidden in required_args:
                errors.append(f"recommended_codex_invocation must not require legacy {forbidden}")
        if any(isinstance(arg, str) and arg.startswith("--deny-read") for arg in required_args):
            errors.append("recommended_codex_invocation must not use legacy --deny-read exec flags")
        if invocation.get("disabled_ambient_features") != ["hooks", "plugins", "goals"]:
            errors.append("recommended_codex_invocation must disable hooks/plugins/goals")
        if invocation.get("forbidden_legacy_args") != ["--isolated", "--yes", "--dry-run", "--deny-read"]:
            errors.append("recommended_codex_invocation must record exact forbidden legacy args")
        if invocation.get("jsonl_telemetry_advisory_only") is not True:
            errors.append("Codex telemetry must remain advisory evidence only")

    profile = package.get("permission_profile_contract")
    if not isinstance(profile, dict):
        errors.append("permission_profile_contract must be a dictionary")
    else:
        roots = (((profile.get("filesystem") or {}).get(":project_roots")) if isinstance(profile.get("filesystem"), dict) else None)
        if profile.get("default_permissions") != "blk-kuronode-codex-feature":
            errors.append("permission_profile default_permissions must be blk-kuronode-codex-feature")
        if roots != REQUIRED_PROFILE_ROOTS:
            errors.append("permission_profile filesystem roots must match exact BLK-SYSTEM-216 contract")
        if profile.get("network") != {"enabled": False}:
            errors.append("permission_profile network must be disabled")
        if profile.get("web_search") != "disabled":
            errors.append("permission_profile web_search must be disabled")
        if profile.get("glob_scan_max_depth") != 4:
            errors.append("permission_profile glob_scan_max_depth must be 4")
        if profile.get("legacy_exec_deny_read_flags_supported") is not False:
            errors.append("permission_profile must mark legacy exec deny-read flags unsupported")
        if profile.get("profile_must_fail_closed_when_unavailable") is not True:
            errors.append("permission_profile must fail closed when unavailable")

    host = package.get("host_sandbox_smoke_result")
    if not isinstance(host, dict):
        errors.append("host_sandbox_smoke_result must be a dictionary")
    else:
        if host.get("native_sandbox_status") != "HOST_NATIVE_CODEX_SANDBOX_UNAVAILABLE_BWRAP_RTM_NEWADDR":
            errors.append("host sandbox smoke result must record unavailable native sandbox")
        if "bwrap: loopback: Failed RTM_NEWADDR" not in str(host.get("observed_failure", "")):
            errors.append("host sandbox smoke result must bind observed bwrap RTM_NEWADDR failure")
        if host.get("required_fallback") != "DEVCONTAINER_OR_EXTERNAL_SANDBOX_FOR_DANGER_FULL_ACCESS":
            errors.append("host sandbox smoke result must require external containment fallback")
        if host.get("permission_profile_requires_direct_runtime_enforcement") is not True:
            errors.append("host sandbox smoke result must say permission profiles require direct runtime enforcement")

    for field in CALLER_CONTROLLED_FIELDS:
        errors.extend(_scan_caller_controlled(package.get(field), f"package.{field}"))
    return errors


def build_and_validate_216_codex_config_containment_package() -> dict[str, Any]:
    package = build_216_codex_config_containment_package()
    errors = validate_216_codex_config_containment_package(package)
    if errors:
        raise ValueError("BLK-SYSTEM-216 package failed validation: " + "; ".join(errors))
    return package
