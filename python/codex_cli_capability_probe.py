"""Codex CLI capability probe helpers for BLK-SYSTEM-343.

The helpers are deliberately pure and non-executing: callers provide already
captured command output, and this module classifies/redacts it. A later route
integration sprint may consume the report, but this probe itself grants no
Codex, BLK-pipe, BEO/RTM, protected-body, runtime, or mutation authority.
"""

from __future__ import annotations

import re
from typing import Any, Mapping

REQUIRED_BASELINE_EXEC_FLAGS = (
    "--sandbox",
    "--ephemeral",
    "--ignore-user-config",
    "--ignore-rules",
    "--disable",
    "--json",
    "--output-last-message",
)

REQUIRED_ROUTE_CAPABILITIES = ("--sandbox workspace-write",)

SIDE_EFFECT_AUTHORITY_FALSES = {
    "live_codex_dispatch_authorized": False,
    "reusable_codex_dispatch_authorized": False,
    "broad_blk_pipe_dispatch_authorized": False,
    "beb_l2_authorship_authorized": False,
    "beo_publication_authorized": False,
    "beo_closeout_execution_authorized": False,
    "rtm_generation_authorized": False,
    "production_blk_link_authorized": False,
    "drift_rejection_authorized": False,
    "coverage_truth_authorized": False,
    "protected_body_access_authorized": False,
    "production_blk_test_mcp_authorized": False,
    "runtime_tooling_expansion_authorized": False,
    "kuronode_source_git_mutation_authorized": False,
    "package_network_model_browser_cyber_tooling_authorized": False,
    "production_isolation_claimed": False,
}

_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_SECRET_ASSIGNMENT_RE = re.compile(
    r"(?im)\b([A-Z0-9_]*(?:API_KEY|TOKEN|SECRET|PASSWORD)[A-Z0-9_]*\s*=\s*)\S+"
)
_SECRET_MAPPING_RE = re.compile(
    r"(?im)\b((?:api[_-]?key|token|secret|password)\s*[:=]\s*)\S+"
)


def redact_sensitive_diagnostics(text: str | None) -> str:
    """Redact credential-looking values and local profile paths from diagnostics."""
    if text is None:
        return ""
    redacted = str(text)
    redacted = _SECRET_ASSIGNMENT_RE.sub(lambda m: m.group(1) + "[REDACTED_SECRET]", redacted)
    redacted = _SECRET_MAPPING_RE.sub(lambda m: m.group(1) + "[REDACTED_SECRET]", redacted)
    redacted = _EMAIL_RE.sub("[REDACTED_EMAIL]", redacted)
    redacted = redacted.replace("/home/dad", "[REDACTED_HOME]")
    return redacted.strip()


def classify_exec_help_flags(exec_help_output: str | None) -> dict[str, object]:
    """Classify whether ``codex exec --help`` exposes the BLK route baseline."""
    help_text = "" if exec_help_output is None else str(exec_help_output)
    missing = [flag for flag in REQUIRED_BASELINE_EXEC_FLAGS if flag not in help_text]
    present = [flag for flag in REQUIRED_BASELINE_EXEC_FLAGS if flag not in missing]
    missing_capabilities = [
        capability
        for capability in REQUIRED_ROUTE_CAPABILITIES
        if not all(token in help_text for token in capability.split())
    ]
    return {
        "status": "BLOCKED" if missing or missing_capabilities else "READY",
        "required_flags": list(REQUIRED_BASELINE_EXEC_FLAGS),
        "present_required_flags": present,
        "missing_required_flags": missing,
        "required_route_capabilities": list(REQUIRED_ROUTE_CAPABILITIES),
        "missing_required_capabilities": missing_capabilities,
        "authority": "DIAGNOSTIC_ONLY_NOT_DISPATCH_AUTHORITY",
    }


def build_codex_cli_capability_report(
    *,
    codex_version_output: str | None,
    npm_latest_output: str | None,
    exec_help_output: str | None,
    doctor_output: str | None,
    private_bwrap_descriptor: Mapping[str, Any] | None,
) -> dict[str, object]:
    """Build a sanitized BLK-SYSTEM-343 local Codex CLI capability report."""
    help_inventory = classify_exec_help_flags(exec_help_output)
    descriptor = _sanitize_report_value(dict(private_bwrap_descriptor or {}))
    descriptor_status = descriptor.get("status", "UNKNOWN") if isinstance(descriptor, dict) else "UNKNOWN"
    descriptor_blockers = descriptor.get("blockers", []) if isinstance(descriptor, dict) else []
    descriptor_blockers_is_list = isinstance(descriptor_blockers, list)
    descriptor_has_blockers = descriptor_blockers_is_list and len(descriptor_blockers) > 0
    descriptor_has_malformed_blockers = (not descriptor_blockers_is_list) and bool(descriptor_blockers)
    blockers: list[dict[str, object]] = []
    if help_inventory["status"] != "READY":
        blockers.append(
            {
                "code": "CODEX_EXEC_BASELINE_FLAGS_MISSING",
                "missing_required_flags": list(help_inventory["missing_required_flags"]),
                "missing_required_capabilities": list(help_inventory["missing_required_capabilities"]),
            }
        )
    if descriptor_status == "READY" and descriptor_has_malformed_blockers:
        blockers.append(
            {
                "code": "PRIVATE_BWRAP_DESCRIPTOR_BLOCKERS_MALFORMED",
                "descriptor_status": descriptor_status,
                "descriptor_blockers_type": type(descriptor_blockers).__name__,
            }
        )
    elif descriptor_status == "READY" and descriptor_has_blockers:
        blockers.append(
            {
                "code": "PRIVATE_BWRAP_DESCRIPTOR_CONTRADICTORY",
                "descriptor_status": descriptor_status,
                "descriptor_blockers": list(descriptor_blockers),
            }
        )
    elif descriptor_status != "READY":
        blockers.append(
            {
                "code": "PRIVATE_BWRAP_DESCRIPTOR_NOT_READY",
                "descriptor_status": descriptor_status,
                "descriptor_blockers": list(descriptor_blockers) if isinstance(descriptor_blockers, list) else [],
            }
        )

    return {
        "report_id": "BLK_SYSTEM_343_CODEX_CLI_CAPABILITY_REPORT",
        "status": "BLOCKED" if blockers else "READY",
        "codex_cli_version": _first_nonempty_line(codex_version_output),
        "npm_latest_version": _first_nonempty_line(npm_latest_output),
        "exec_help_inventory": help_inventory,
        "doctor_evidence": {
            "authority": "ADVISORY_ONLY",
            "text": redact_sensitive_diagnostics(doctor_output),
        },
        "private_bwrap_descriptor": descriptor,
        "blockers": blockers,
        "side_effect_authority": dict(SIDE_EFFECT_AUTHORITY_FALSES),
        "authority_boundary": (
            "Capability evidence is diagnostic only. It grants no live/reusable Codex dispatch, "
            "BLK-pipe dispatch, BEB/L2 authorship, BEO publication, RTM/blk-link, protected-body, "
            "runtime/tooling, Kuronode mutation, or production-isolation authority."
        ),
    }


def _first_nonempty_line(text: str | None) -> str:
    for line in ("" if text is None else str(text)).splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def _sanitize_report_value(value: Any) -> Any:
    if isinstance(value, str):
        return redact_sensitive_diagnostics(value)
    if isinstance(value, list):
        return [_sanitize_report_value(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_sanitize_report_value(item) for item in value)
    if isinstance(value, dict):
        return {
            redact_sensitive_diagnostics(str(key)): _sanitize_report_value(item)
            for key, item in value.items()
        }
    return value
