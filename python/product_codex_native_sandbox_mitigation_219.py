"""BLK-SYSTEM-219 native Codex sandbox mitigation evidence.

This module records a deterministic, non-executing mitigation package for the
observed native Codex Linux sandbox failure on this host. The real host probes
were run manually during sprint execution; this module only packages the
observed evidence and fail-closed mitigation decision. It does not invoke Codex,
bubblewrap, subprocesses, Git, BLK-pipe, BLK-test, network clients, package
managers, protected BLK-req readers, BEO tooling, RTM tooling, or host
configuration mutators.
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
from product_feature_loop_218 import DEFAULT_218_PACKAGE_HASH

UPSTREAM_BLK218_PACKAGE_HASH = DEFAULT_218_PACKAGE_HASH
NEXT_FRONTIER_219 = "NEXT_FRONTIER_OPERATOR_SELECTED_BOUNDED_KURONODE_FEATURE_WITH_EXTERNAL_CONTAINMENT_OR_HOST_ADMIN_SANDBOX_REPAIR_NOT_GRANTED"

DENIED_AUTHORITIES = tuple(
    list(BASE_DENIED_AUTHORITIES)
    + [
        "HOST_CONFIGURATION_MUTATION",
        "NATIVE_SANDBOX_PASS_AS_RUNTIME_AUTHORITY",
    ]
)

REQUIRED_FALSE_SIDE_EFFECT_FLAGS = tuple(
    list(BASE_REQUIRED_FALSE_SIDE_EFFECT_FLAGS)
    + [
        "host_configuration_mutated",
        "native_sandbox_pass_runtime_authority_authorized",
    ]
)

PACKAGE_219_KEYS = {
    "sprint_id",
    "status",
    "upstream_218_package_hash",
    "codex_configuration_doc",
    "host_probe_evidence",
    "root_cause_assessment",
    "mitigation_decision",
    "required_recheck_commands",
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
    "productionsandboxenforced",
    "productionisolationclaim",
    "nativeworkspacewriteauthorized",
    "hostconfigurationmutated",
    "hostconfigurationmutation",
    "sandboxpassruntimeauthority",
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


def _base_219() -> dict[str, Any]:
    return {
        "sprint_id": "BLK-SYSTEM-219",
        "status": "NATIVE_CODEX_SANDBOX_MITIGATION_RECORDED",
        "upstream_218_package_hash": UPSTREAM_BLK218_PACKAGE_HASH,
        "codex_configuration_doc": "BLK-121",
        "host_probe_evidence": {
            "codex_cli_version": "codex-cli 0.130.0",
            "bubblewrap_version": "bubblewrap 0.9.0",
            "kernel": "Linux hermes-node 6.17.0-23-generic x86_64 Ubuntu 24.04 lineage",
            "kernel_unprivileged_userns_clone": "1",
            "user_max_user_namespaces": "63858",
            "user_max_net_namespaces": "63858",
            "apparmor_enabled": "Y",
            "apparmor_profile": "unconfined",
            "apparmor_restrict_unprivileged_userns": "1",
            "bubblewrap_binary_mode": "0755 root:root without setuid bit or file capabilities",
            "subuid_entry": "dad:100000:65536",
            "subgid_entry": "dad:100000:65536",
            "unshare_user_result": "unshare: write failed /proc/self/uid_map: Operation not permitted; rc=1",
            "unshare_user_net_result": "unshare: write failed /proc/self/uid_map: Operation not permitted; rc=1",
            "bwrap_userns_result": "bwrap: setting up uid map: Permission denied; rc=1",
            "bwrap_network_result": "bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted; rc=1",
            "codex_sandbox_result": "bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted; rc=1",
        },
        "root_cause_assessment": {
            "primary_blocker": "UNPRIVILEGED_USER_NAMESPACE_SETUP_BLOCKED_FOR_BWRAP",
            "secondary_blocker": "BWRAP_NETWORK_NAMESPACE_LOOPBACK_CONFIGURATION_DENIED",
            "evidence": [
                "kernel.unprivileged_userns_clone and namespace count limits are not zero, but uid_map writes fail with EPERM",
                "bubblewrap is not installed setuid and has no file capabilities, so it depends on unprivileged user namespace setup",
                "Codex native sandbox delegates to bubblewrap and fails before it can enforce the permission profile",
            ],
            "probable_host_policy": "Ubuntu/AppArmor unprivileged-user-namespace restriction or equivalent host policy blocks this user context",
        },
        "mitigation_decision": {
            "native_sandbox_state": "HOST_BLOCKED_FAIL_CLOSED",
            "active_codex_mode": "EXTERNAL_CONTAINMENT_REQUIRED",
            "workspace_write_allowed_on_this_host": False,
            "danger_full_access_allowed_only_inside_external_containment": True,
            "host_admin_repair_required_before_native_workspace_write": True,
            "admin_repair_not_executed_by_this_sprint": True,
            "required_after_any_admin_repair": "rerun Codex native sandbox smoke and update evidence only after PASS",
        },
        "required_recheck_commands": [
            "codex --version",
            "sysctl kernel.unprivileged_userns_clone kernel.apparmor_restrict_unprivileged_userns user.max_user_namespaces user.max_net_namespaces",
            "unshare -Ur true",
            "bwrap --unshare-user --ro-bind / / true",
            "bwrap --unshare-net --ro-bind / / true",
            "CODEX_HOME=<temp-config> codex sandbox linux --permissions-profile blk-smoke -C /home/dad/BLK-System true",
        ],
        "next_frontier": NEXT_FRONTIER_219,
        "denied_authorities": list(DENIED_AUTHORITIES),
        "operator_notes": [],
        "caller_supplied_evidence_refs": {},
        **_false_flags(),
    }


def build_219_native_sandbox_mitigation_package() -> dict[str, Any]:
    return _with_hash(_base_219())


DEFAULT_219_PACKAGE_HASH = canonical_package_hash(_base_219())


def validate_219_native_sandbox_mitigation_package(package: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(package, dict):
        return ["package must be a dictionary"]
    keys = set(package)
    if keys != PACKAGE_219_KEYS:
        errors.append(f"BLK-SYSTEM-219 keys must be exact; missing={sorted(PACKAGE_219_KEYS - keys)} extra={sorted(keys - PACKAGE_219_KEYS)}")

    expected_scalars = {
        "sprint_id": "BLK-SYSTEM-219",
        "status": "NATIVE_CODEX_SANDBOX_MITIGATION_RECORDED",
        "upstream_218_package_hash": UPSTREAM_BLK218_PACKAGE_HASH,
        "codex_configuration_doc": "BLK-121",
        "next_frontier": NEXT_FRONTIER_219,
        "package_hash": DEFAULT_219_PACKAGE_HASH,
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

    host = package.get("host_probe_evidence")
    if not isinstance(host, dict):
        errors.append("host_probe_evidence must be a dictionary")
    else:
        required_host_markers = {
            "codex_cli_version": "codex-cli 0.130.0",
            "bubblewrap_version": "bubblewrap 0.9.0",
            "kernel_unprivileged_userns_clone": "1",
            "apparmor_restrict_unprivileged_userns": "1",
        }
        for key, expected in required_host_markers.items():
            if host.get(key) != expected:
                errors.append(f"host_probe_evidence.{key} must be {expected!r}")
        for key, marker in {
            "unshare_user_result": "write failed /proc/self/uid_map: Operation not permitted",
            "bwrap_userns_result": "bwrap: setting up uid map: Permission denied",
            "bwrap_network_result": "bwrap: loopback: Failed RTM_NEWADDR",
            "codex_sandbox_result": "bwrap: loopback: Failed RTM_NEWADDR",
        }.items():
            if marker not in str(host.get(key, "")):
                errors.append(f"host_probe_evidence.{key} must bind observed marker {marker!r}")

    root = package.get("root_cause_assessment")
    if not isinstance(root, dict):
        errors.append("root_cause_assessment must be a dictionary")
    else:
        if root.get("primary_blocker") != "UNPRIVILEGED_USER_NAMESPACE_SETUP_BLOCKED_FOR_BWRAP":
            errors.append("root_cause_assessment must keep the user-namespace blocker")
        if root.get("secondary_blocker") != "BWRAP_NETWORK_NAMESPACE_LOOPBACK_CONFIGURATION_DENIED":
            errors.append("root_cause_assessment must keep the network namespace blocker")

    mitigation = package.get("mitigation_decision")
    if not isinstance(mitigation, dict):
        errors.append("mitigation_decision must be a dictionary")
    else:
        if mitigation.get("native_sandbox_state") != "HOST_BLOCKED_FAIL_CLOSED":
            errors.append("mitigation_decision.native_sandbox_state must remain HOST_BLOCKED_FAIL_CLOSED")
        if mitigation.get("active_codex_mode") != "EXTERNAL_CONTAINMENT_REQUIRED":
            errors.append("mitigation_decision.active_codex_mode must require external containment")
        for key in (
            "workspace_write_allowed_on_this_host",
        ):
            if mitigation.get(key) is not False:
                errors.append(f"mitigation_decision.{key} must remain false")
        for key in (
            "danger_full_access_allowed_only_inside_external_containment",
            "host_admin_repair_required_before_native_workspace_write",
            "admin_repair_not_executed_by_this_sprint",
        ):
            if mitigation.get(key) is not True:
                errors.append(f"mitigation_decision.{key} must remain true")

    commands = package.get("required_recheck_commands")
    if not isinstance(commands, list) or not all(isinstance(command, str) for command in commands):
        errors.append("required_recheck_commands must be a list of strings")
    else:
        for required in ("unshare -Ur true", "bwrap --unshare-user", "codex sandbox linux"):
            if not any(required in command for command in commands):
                errors.append(f"required_recheck_commands missing {required!r}")

    for field in CALLER_CONTROLLED_FIELDS:
        errors.extend(_scan_caller_controlled(package.get(field), f"package.{field}"))
    return errors


def build_and_validate_219_native_sandbox_mitigation_package() -> dict[str, Any]:
    package = build_219_native_sandbox_mitigation_package()
    errors = validate_219_native_sandbox_mitigation_package(package)
    if errors:
        raise ValueError("BLK-SYSTEM-219 package failed validation: " + "; ".join(errors))
    return package
