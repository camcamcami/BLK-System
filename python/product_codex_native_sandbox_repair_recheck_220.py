"""BLK-SYSTEM-220 native Codex sandbox repair/recheck evidence.

This module records a deterministic, non-executing package for the host-admin
native Codex sandbox repair/recheck. The real probes were coordinated with the
operator during sprint execution. This module does not invoke Codex, bubblewrap,
subprocesses, Git, BLK-pipe, BLK-test, network clients, package managers,
protected BLK-req readers, BEO tooling, RTM tooling, or host configuration
mutators.
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
    DENIED_AUTHORITIES as BASE_DENIED_AUTHORITIES,
    REQUIRED_FALSE_SIDE_EFFECT_FLAGS as BASE_REQUIRED_FALSE_SIDE_EFFECT_FLAGS,
    canonical_package_hash,
)
from product_codex_native_sandbox_mitigation_219 import DEFAULT_219_PACKAGE_HASH

UPSTREAM_BLK219_PACKAGE_HASH = DEFAULT_219_PACKAGE_HASH
NEXT_FRONTIER_220 = "NEXT_FRONTIER_OPERATOR_SELECTED_BOUNDED_KURONODE_FEATURE_WITH_NATIVE_WORKSPACE_WRITE_RECHECK_OR_EXTERNAL_CONTAINMENT_NOT_GRANTED"

DENIED_AUTHORITIES = tuple(
    list(BASE_DENIED_AUTHORITIES)
    + [
        "HOST_CONFIGURATION_PERSISTENCE",
        "NATIVE_WORKSPACE_WRITE_REUSABLE_AUTHORITY",
        "NATIVE_SANDBOX_PASS_AS_RUNTIME_AUTHORITY",
        "PRODUCTION_ISOLATION_BY_CODEX_SANDBOX",
    ]
)

REQUIRED_FALSE_SIDE_EFFECT_FLAGS = tuple(
    list(BASE_REQUIRED_FALSE_SIDE_EFFECT_FLAGS)
    + [
        "host_configuration_persisted",
        "native_workspace_write_reusable_authority_authorized",
        "native_sandbox_pass_runtime_authority_authorized",
    ]
)

PACKAGE_220_KEYS = {
    "sprint_id",
    "status",
    "upstream_219_package_hash",
    "codex_configuration_doc",
    "pre_repair_evidence",
    "host_admin_repair_evidence",
    "passing_smoke_evidence",
    "current_host_state_after_recheck",
    "repair_decision",
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
    "nativecodexsandboxenforced",
    "sandboxenforced",
    "sandboxpassruntimeauthority",
    "nativeworkspacewriteauthorized",
    "nativeworkspacewritereusableauthority",
    "nativeworkspacewritealwayson",
    "alwayson",
    "permanentlyenabled",
    "hostconfigurationpersisted",
    "hostconfigurationmutation",
    "productionsandboxenforced",
    "productionisolationclaim",
    "productionisolationproven",
    "approvedforproduction",
    "approvedeverywhere",
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
    "beopublicationauthorized",
    "beopublicationgreenlit",
    "publishbeo",
    "rtmgeneration",
    "rtmdriftrejection",
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
                    errors.append(f"{path} contains forbidden authority/tooling/protected-body/sandbox wording {token!r}")
    return errors


def _base_220() -> dict[str, Any]:
    return {
        "sprint_id": "BLK-SYSTEM-220",
        "status": "NATIVE_CODEX_SANDBOX_REPAIR_RECHECK_RECORDED",
        "upstream_219_package_hash": UPSTREAM_BLK219_PACKAGE_HASH,
        "codex_configuration_doc": "BLK-121",
        "pre_repair_evidence": {
            "codex_cli_version": "codex-cli 0.130.0",
            "bubblewrap_version": "bubblewrap 0.9.0",
            "kernel": "Linux hermes-node 6.17.0-23-generic x86_64 Ubuntu 24.04.4 LTS",
            "newuidmap": "missing",
            "newgidmap": "missing",
            "subuid_entry": "dad:100000:65536",
            "subgid_entry": "dad:100000:65536",
            "apparmor_restrict_unprivileged_userns": "1",
            "unshare_result": "unshare --user --map-current-user true: write failed /proc/self/uid_map: Operation not permitted; rc=1",
            "bwrap_result": "bwrap --unshare-user --unshare-ipc --unshare-pid --unshare-net --ro-bind / / --proc /proc true: bwrap: loopback: Failed RTM_NEWADDR; rc=1",
            "codex_sandbox_result": "codex sandbox linux: bwrap: loopback: Failed RTM_NEWADDR; rc=1",
        },
        "host_admin_repair_evidence": {
            "operator_performed_admin_steps": True,
            "uidmap_installed": True,
            "newuidmap_mode": "4755 root:root",
            "newgidmap_mode": "4755 root:root",
            "bwrap_mode": "0755 root:root",
            "runtime_apparmor_restrict_unprivileged_userns": "0",
            "persisted_sysctl_change": False,
            "restored_apparmor_restrict_unprivileged_userns_after_test": "1",
            "repair_recipe": [
                "install uidmap so newuidmap/newgidmap exist setuid root",
                "set kernel.apparmor_restrict_unprivileged_userns=0 for the runtime recheck window",
                "run unshare, bwrap, and Codex workspace-write smoke as dad",
            ],
        },
        "passing_smoke_evidence": {
            "unshare_map_current_rc": 0,
            "unshare_map_root_rc": 0,
            "bwrap_user_rc": 0,
            "bwrap_net_rc": 0,
            "bwrap_full_rc": 0,
            "codex_exec_workspace_write_rc": 0,
            "codex_exec_sandbox": "workspace-write [workdir, /tmp, /home/dad/.codex/memories]",
            "codex_exec_approval": "never",
            "codex_exec_model": "gpt-5.5",
            "codex_exec_reasoning_effort": "low",
            "codex_last_message": "CODEX_WORKSPACE_WRITE_SMOKE_OK",
        },
        "current_host_state_after_recheck": {
            "apparmor_restrict_unprivileged_userns": "1",
            "native_sandbox_currently_available": False,
            "unshare_map_current_rc": 1,
            "bwrap_full_rc": 1,
            "reason": "runtime-only AppArmor userns relaxation was restored after the smoke test",
        },
        "repair_decision": {
            "native_sandbox_state": "REPAIR_RECHECK_VALIDATED_RUNTIME_ONLY",
            "native_workspace_write_pass_condition": "uidmap installed and kernel.apparmor_restrict_unprivileged_userns=0 during the run",
            "native_workspace_write_default_mode": "RECHECK_REQUIRED_BEFORE_USE",
            "external_containment_still_valid_fallback": True,
            "persistent_host_policy_change_not_made_by_this_sprint": True,
            "workspace_write_smoke_pass_is_not_reusable_codex_dispatch_authority": True,
            "workspace_write_smoke_pass_is_not_production_isolation_claim": True,
        },
        "next_frontier": NEXT_FRONTIER_220,
        "denied_authorities": list(DENIED_AUTHORITIES),
        "operator_notes": [],
        "caller_supplied_evidence_refs": {},
        **_false_flags(),
    }


def build_220_native_sandbox_repair_recheck_package() -> dict[str, Any]:
    return _with_hash(_base_220())


DEFAULT_220_PACKAGE_HASH = canonical_package_hash(_base_220())


def validate_220_native_sandbox_repair_recheck_package(package: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(package, dict):
        return ["package must be a dictionary"]
    keys = set(package)
    if keys != PACKAGE_220_KEYS:
        errors.append(f"BLK-SYSTEM-220 keys must be exact; missing={sorted(PACKAGE_220_KEYS - keys)} extra={sorted(keys - PACKAGE_220_KEYS)}")

    expected_scalars = {
        "sprint_id": "BLK-SYSTEM-220",
        "status": "NATIVE_CODEX_SANDBOX_REPAIR_RECHECK_RECORDED",
        "upstream_219_package_hash": UPSTREAM_BLK219_PACKAGE_HASH,
        "codex_configuration_doc": "BLK-121",
        "next_frontier": NEXT_FRONTIER_220,
        "package_hash": DEFAULT_220_PACKAGE_HASH,
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

    pre = package.get("pre_repair_evidence")
    if not isinstance(pre, dict):
        errors.append("pre_repair_evidence must be a dictionary")
    else:
        for key, expected in {
            "newuidmap": "missing",
            "newgidmap": "missing",
            "apparmor_restrict_unprivileged_userns": "1",
        }.items():
            if pre.get(key) != expected:
                errors.append(f"pre_repair_evidence.{key} must be {expected!r}")
        for key, marker in {
            "unshare_result": "uid_map: Operation not permitted",
            "bwrap_result": "Failed RTM_NEWADDR",
            "codex_sandbox_result": "Failed RTM_NEWADDR",
        }.items():
            if marker not in str(pre.get(key, "")):
                errors.append(f"pre_repair_evidence.{key} must bind observed marker {marker!r}")

    repair = package.get("host_admin_repair_evidence")
    if not isinstance(repair, dict):
        errors.append("host_admin_repair_evidence must be a dictionary")
    else:
        expected_repair = {
            "operator_performed_admin_steps": True,
            "uidmap_installed": True,
            "newuidmap_mode": "4755 root:root",
            "newgidmap_mode": "4755 root:root",
            "runtime_apparmor_restrict_unprivileged_userns": "0",
            "persisted_sysctl_change": False,
            "restored_apparmor_restrict_unprivileged_userns_after_test": "1",
        }
        for key, expected in expected_repair.items():
            if repair.get(key) != expected:
                errors.append(f"host_admin_repair_evidence.{key} must be {expected!r}")
        recipe = repair.get("repair_recipe")
        if not isinstance(recipe, list) or len(recipe) < 3:
            errors.append("host_admin_repair_evidence.repair_recipe must record the minimal repair recipe")

    smoke = package.get("passing_smoke_evidence")
    if not isinstance(smoke, dict):
        errors.append("passing_smoke_evidence must be a dictionary")
    else:
        for key in (
            "unshare_map_current_rc",
            "unshare_map_root_rc",
            "bwrap_user_rc",
            "bwrap_net_rc",
            "bwrap_full_rc",
            "codex_exec_workspace_write_rc",
        ):
            if smoke.get(key) != 0:
                errors.append(f"passing_smoke_evidence.{key} must be 0")
        if smoke.get("codex_last_message") != "CODEX_WORKSPACE_WRITE_SMOKE_OK":
            errors.append("passing_smoke_evidence.codex_last_message must bind the Codex smoke response")
        if smoke.get("codex_exec_sandbox") != "workspace-write [workdir, /tmp, /home/dad/.codex/memories]":
            errors.append("passing_smoke_evidence.codex_exec_sandbox must bind workspace-write sandbox evidence")

    current = package.get("current_host_state_after_recheck")
    if not isinstance(current, dict):
        errors.append("current_host_state_after_recheck must be a dictionary")
    else:
        if current.get("apparmor_restrict_unprivileged_userns") != "1":
            errors.append("current_host_state_after_recheck.apparmor_restrict_unprivileged_userns must record restored default 1")
        if current.get("native_sandbox_currently_available") is not False:
            errors.append("current_host_state_after_recheck.native_sandbox_currently_available must remain false after restored runtime-only repair")
        if current.get("unshare_map_current_rc") != 1:
            errors.append("current_host_state_after_recheck.unshare_map_current_rc must record restored failure")
        if current.get("bwrap_full_rc") != 1:
            errors.append("current_host_state_after_recheck.bwrap_full_rc must record restored failure")

    decision = package.get("repair_decision")
    if not isinstance(decision, dict):
        errors.append("repair_decision must be a dictionary")
    else:
        if decision.get("native_sandbox_state") != "REPAIR_RECHECK_VALIDATED_RUNTIME_ONLY":
            errors.append("repair_decision.native_sandbox_state must remain runtime-only validation")
        if decision.get("native_workspace_write_default_mode") != "RECHECK_REQUIRED_BEFORE_USE":
            errors.append("repair_decision.native_workspace_write_default_mode must require recheck before use")
        for key in (
            "external_containment_still_valid_fallback",
            "persistent_host_policy_change_not_made_by_this_sprint",
            "workspace_write_smoke_pass_is_not_reusable_codex_dispatch_authority",
            "workspace_write_smoke_pass_is_not_production_isolation_claim",
        ):
            if decision.get(key) is not True:
                errors.append(f"repair_decision.{key} must remain true")

    for field in CALLER_CONTROLLED_FIELDS:
        errors.extend(_scan_caller_controlled(package.get(field), f"package.{field}"))
    return errors


def build_and_validate_220_native_sandbox_repair_recheck_package() -> dict[str, Any]:
    package = build_220_native_sandbox_repair_recheck_package()
    errors = validate_220_native_sandbox_repair_recheck_package(package)
    if errors:
        raise ValueError("BLK-SYSTEM-220 package failed validation: " + "; ".join(errors))
    return package
