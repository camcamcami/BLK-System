"""BLK-req legislative gateway contract and staged artifact helpers.

BLK-SYSTEM-116 starts this module with a contract-only surface. Later sprints
extend it with the staging linter, draft writer, and canonical hash engine.
The module is intentionally local and deterministic: it does not dispatch
BLK-pipe, run BLK-test, publish BEOs, generate RTM artifacts, mutate target
repositories, or claim production isolation.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

BLK_REQ_DENIED_AUTHORITIES = {
    "BLK_PIPE_RUNTIME_DISPATCH",
    "TARGET_SOURCE_GIT_MUTATION",
    "BLK_TEST_RUNTIME",
    "BEO_PUBLICATION",
    "RTM_GENERATION",
    "RTM_DRIFT_REJECTION",
    "PROTECTED_ACTIVE_BODY_READS",
    "ACTIVE_VAULT_WRITE",
    "LIVE_CODEX_DISPATCH",
    "NETWORK_MODEL_BROWSER_CYBER_TOOLING",
    "PACKAGE_MANAGER_TOOLING",
    "SIGNER_STORAGE_LEDGER_ROLLBACK",
    "PRODUCTION_ISOLATION_CLAIM",
    "HITL_APPROVAL_CAPTURE",
    "ACTIVE_VAULT_PROMOTION",
    "EXACT_ID_RETRIEVAL",
}

_SIDE_EFFECT_FLAGS = {
    "blk_pipe_dispatch_performed",
    "target_source_git_mutation_performed",
    "blk_test_runtime_performed",
    "beo_publication_performed",
    "rtm_generation_performed",
    "rtm_drift_rejection_performed",
    "protected_active_body_read",
    "active_vault_write_performed",
    "live_codex_dispatch_performed",
    "network_model_browser_cyber_tooling_performed",
    "package_manager_tooling_performed",
    "signer_storage_ledger_rollback_performed",
    "production_isolation_claimed",
    "hitl_approval_capture_performed",
    "active_vault_promotion_performed",
    "exact_id_retrieval_performed",
}

_CONTRACT_KEYS = {
    "contract_marker",
    "contract_status",
    "sprint",
    "governing_docs",
    "allowed_local_backend_operations",
    "denied_authorities",
    "side_effect_flags",
    "notes",
}

_ALLOWED_OPERATIONS = [
    "BLK_SYSTEM_117_STAGING_LINTER",
    "BLK_SYSTEM_118_STAGING_DRAFT_WRITER",
    "BLK_SYSTEM_119_CANONICAL_VERSION_HASH_ENGINE",
]

_FORBIDDEN_COMPACT_WORDING = {
    "approvedforliveexecution",
    "approvedforruntimeexecution",
    "runtimeexecutionapproved",
    "runtimeexecutionauthorized",
    "liveexecutionauthorized",
    "blkpipeexecutionauthorized",
    "blkpipedispatchauthorized",
    "blktestruntimeauthorized",
    "productionblktestmcpauthorized",
    "beopublicationgranted",
    "beopublicationauthorized",
    "authoritativebeopublicationauthorized",
    "rtmgenerationauthorized",
    "runtimertmgenerationauthorized",
    "rtmdriftrejectionauthorized",
    "protectedbodyreadsauthorized",
    "protectedactivebodyreadsauthorized",
    "activevaultreadsauthorized",
    "activevaultwriteauthorized",
    "targetrepomutationauthorized",
    "sourcemutationauthorized",
    "gitmutationauthorized",
    "livecodexdispatchauthorized",
    "packagemanagertoolingauthorized",
    "networkmodelbrowsercybertoolingauthorized",
    "signerstorageledgerauthorized",
    "productionisolationclaimed",
    "hitlapprovalcaptured",
    "activevaultpromotionauthorized",
    "exactidretrievalauthorized",
}


def build_legislative_gateway_contract() -> dict[str, Any]:
    """Return the BLK-SYSTEM-116 local backend contract scaffold."""

    return {
        "contract_marker": "BLK_SYSTEM_116_BLK_REQ_LEGISLATIVE_GATEWAY_CONTRACT",
        "contract_status": "CONTRACT_READY_NOT_EXECUTION_AUTHORITY",
        "sprint": "BLK-SYSTEM-116",
        "governing_docs": ["BLK-002", "BLK-005", "BLK-006", "BLK-077", "BLK-079", "BLK-116"],
        "allowed_local_backend_operations": list(_ALLOWED_OPERATIONS),
        "denied_authorities": sorted(BLK_REQ_DENIED_AUTHORITIES),
        "side_effect_flags": {flag: False for flag in sorted(_SIDE_EFFECT_FLAGS)},
        "notes": [
            "BLK-SYSTEM-116 is a contract scaffold only.",
            "BLK-SYSTEM-117 through BLK-SYSTEM-119 may add local staging linting, staging draft writing, and canonical hash primitives.",
            "BLK-SYSTEM-120 and later approval, promotion, revision, and retrieval work require separate sprint scope.",
            "BLK-test is a BLK-System functional module, not BLK-System's test suite.",
        ],
    }


def validate_legislative_gateway_contract(contract: dict[str, Any]) -> list[str]:
    """Validate the BLK-SYSTEM-116 contract without granting authority."""

    errors: list[str] = []
    if not isinstance(contract, dict):
        return ["contract must be a dictionary"]

    extra = sorted(set(contract) - _CONTRACT_KEYS)
    missing = sorted(_CONTRACT_KEYS - set(contract))
    for key in extra:
        errors.append(f"unsupported contract field: {key}")
    for key in missing:
        errors.append(f"missing contract field: {key}")

    if contract.get("contract_marker") != "BLK_SYSTEM_116_BLK_REQ_LEGISLATIVE_GATEWAY_CONTRACT":
        errors.append("contract_marker must be BLK_SYSTEM_116_BLK_REQ_LEGISLATIVE_GATEWAY_CONTRACT")
    if contract.get("contract_status") != "CONTRACT_READY_NOT_EXECUTION_AUTHORITY":
        errors.append("contract_status must be CONTRACT_READY_NOT_EXECUTION_AUTHORITY")
    if contract.get("allowed_local_backend_operations") != _ALLOWED_OPERATIONS:
        errors.append("allowed_local_backend_operations must match BLK-SYSTEM-117/118/119 sequence")

    denied = contract.get("denied_authorities")
    if not isinstance(denied, list) or set(denied) != BLK_REQ_DENIED_AUTHORITIES or len(denied) != len(set(denied)):
        errors.append("denied_authorities must match exact BLK-116 set")

    flags = contract.get("side_effect_flags")
    if not isinstance(flags, dict):
        errors.append("side_effect_flags must be a dictionary")
    else:
        if set(flags) != _SIDE_EFFECT_FLAGS:
            errors.append("side_effect_flags must match exact BLK-116 set")
        for flag, value in flags.items():
            if value is not False:
                errors.append(f"side_effect_flags.{flag} must remain false")

    errors.extend(_scan_for_authority_laundering(contract))
    return _unique(errors)


def _scan_for_authority_laundering(value: Any, path: str = "contract") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            key_path = f"{path}.{key}"
            if path not in {"contract.side_effect_flags"}:
                errors.extend(_scan_text(str(key), key_path))
            errors.extend(_scan_for_authority_laundering(nested, key_path))
    elif isinstance(value, (list, tuple, set)):
        for index, nested in enumerate(value):
            nested_path = f"{path}[{index}]"
            if path == "contract.denied_authorities":
                continue
            errors.extend(_scan_for_authority_laundering(nested, nested_path))
    elif isinstance(value, str):
        errors.extend(_scan_text(value, path))
    return errors


def _scan_text(text: str, path: str) -> list[str]:
    compact = _compact(text)
    safe = compact
    for token in _FORBIDDEN_COMPACT_WORDING:
        safe = safe.replace(f"no{token}", "")
        safe = safe.replace(f"not{token}", "")
    return [f"forbidden authority wording at {path}: {token}" for token in sorted(_FORBIDDEN_COMPACT_WORDING) if token in safe]


def _compact(text: str) -> str:
    return "".join(char for char in str(text).casefold() if char.isalnum())


def _unique(items: list[str]) -> list[str]:
    seen = set()
    out: list[str] = []
    for item in items:
        if item not in seen:
            out.append(item)
            seen.add(item)
    return out


__all__ = [
    "BLK_REQ_DENIED_AUTHORITIES",
    "build_legislative_gateway_contract",
    "validate_legislative_gateway_contract",
]
