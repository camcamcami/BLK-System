"""BLK-SYSTEM-329 verified-loop BEO publication bounded execution kernel.

This development package prepares the deterministic receipt/replay kernel needed
for a future exact current BEO publication side-effect package. It consumes the
BLK-SYSTEM-315 non-approval reconciliation and BLK-SYSTEM-328 development
authority distinction, but it does not capture approval, reserve or consume a run
ID, publish a BEO, emit signer/storage/ledger side effects, generate RTM, run
production ``blk-link``, read protected bodies, start tooling, or mutate target
source/Git outside BLK-System development.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering
from blk_system_development_authority_distinction_328 import (
    EXPECTED_328_DEVELOPMENT_AUTHORITY_HASH,
    validate_development_authority_distinction_328,
)
from verified_loop_beo_publication_approval_request_306_309 import (
    _DENIED_AUTHORITIES as _BASE_DENIED_AUTHORITIES,
    _FALSE_SIDE_EFFECTS,
    _hash_text,
    hash_package,
)
from verified_loop_beo_publication_live_challenge_guard_313_315 import (
    EXPECTED_315_RECONCILIATION_HASH,
    validate_verified_loop_beo_publication_live_challenge_guard_reconciliation_315,
)


class VerifiedLoopBeoPublicationBoundedExecutionKernel329ValidationError(ValueError):
    """Raised when BLK-SYSTEM-329 evidence crosses a boundary."""


OPERATOR_DIRECTIVE_329 = "plan and execute the next blk-system sprint package"
NEXT_FRONTIER_329 = (
    "NEXT_FRONTIER_VERIFIED_LOOP_BEO_PUBLICATION_BOUNDED_EXECUTION_KERNEL_READY_"
    "EXACT_SIDE_EFFECT_PACKAGE_REQUIRED"
)
EXPECTED_329_EXECUTION_KERNEL_HASH: str | None = (
    "sha256:b0562eeb3d2b2b65e4f95b2ce396c2004ddf47e443452152e69137a85336284a"
)

_MARKERS_329 = (
    "BLK_SYSTEM_329_VERIFIED_LOOP_BEO_PUBLICATION_BOUNDED_EXECUTION_KERNEL_READY",
    "RECEIPT_AND_REPLAY_REQUIREMENTS_PREPARED_NOT_EXECUTED",
    "EXACT_SIDE_EFFECT_PACKAGE_STILL_REQUIRED",
)
_EXECUTION_PREREQUISITES_329 = {
    "prior_315_reconciliation_required": True,
    "development_authority_distinction_required": True,
    "development_authority_is_not_product_approval": True,
    "current_exact_side_effect_package_required": True,
    "current_operator_decision_split_required": True,
    "one_fresh_run_id_required_before_publication": True,
    "request_window_hash_required": True,
    "receipt_hashes_required_before_finality": True,
    "expired_or_prior_challenge_reuse_allowed": False,
    "generic_directive_as_product_approval_allowed": False,
}
_RECEIPT_POLICY_329 = {
    "required_receipt_kinds": [
        "signature_receipt",
        "immutable_storage_receipt",
        "public_ledger_entry",
    ],
    "signature_receipt_must_bind_execution_request_hash": True,
    "immutable_storage_receipt_must_bind_signature_receipt_hash": True,
    "public_ledger_entry_must_bind_storage_receipt_hash": True,
    "receipt_hashes_must_feed_finality_record_hash": True,
    "external_signer_key_material_access_allowed": False,
    "external_immutable_storage_write_allowed_by_kernel": False,
    "external_public_ledger_append_allowed_by_kernel": False,
    "receipt_self_attestation_allowed": False,
}
_REPLAY_GUARD_329 = {
    "future_execution_must_reject_previously_consumed_run_id": True,
    "future_execution_must_bind_run_id_to_exact_request_hash": True,
    "future_execution_must_bind_request_interval_to_approval_interval": True,
    "run_id_reserved_by_kernel": False,
    "run_id_consumed_by_kernel": False,
    "global_replay_prevention_claimed_by_kernel": False,
    "durable_replay_ledger_required_for_global_claim": True,
}
_DENIED_AUTHORITIES_329 = tuple(_BASE_DENIED_AUTHORITIES) + (
    "PRIOR_SHORT_APPROVE_CHALLENGE_REUSE",
    "GENERIC_DEVELOPMENT_DIRECTIVE_AS_PRODUCT_APPROVAL",
    "RUN_ID_REPLAY_OR_GLOBAL_REPLAY_CLAIM",
    "RECEIPT_SELF_ATTESTATION_AS_EXTERNAL_SIDE_EFFECT",
)
_SIDE_EFFECTS_329 = {
    "bounded_execution_kernel_prepared": True,
    "receipt_policy_prepared": True,
    "replay_guard_prepared": True,
    "product_side_effects_executed": False,
    **_FALSE_SIDE_EFFECTS,
}
_ALLOWED_KEYS_329 = frozenset(
    {
        "status",
        "markers",
        "prior_reconciliation_hash",
        "development_authority_hash",
        "operator_directive_hash",
        "execution_prerequisites",
        "receipt_policy",
        "replay_guard",
        "next_frontier",
        "denied_authorities",
        "side_effects",
        "execution_kernel_hash",
    }
)


def build_verified_loop_beo_publication_bounded_execution_kernel_329(
    reconciliation_315: dict[str, Any],
    distinction_328: dict[str, Any],
    *,
    operator_directive: str,
) -> dict[str, Any]:
    """Prepare receipt/replay execution-kernel evidence without side effects."""

    try:
        prior = validate_verified_loop_beo_publication_live_challenge_guard_reconciliation_315(
            reconciliation_315,
        )
    except ValueError as exc:
        raise VerifiedLoopBeoPublicationBoundedExecutionKernel329ValidationError(
            f"prior reconciliation invalid: {exc}"
        ) from exc
    try:
        distinction = validate_development_authority_distinction_328(distinction_328)
    except ValueError as exc:
        raise VerifiedLoopBeoPublicationBoundedExecutionKernel329ValidationError(
            f"development authority distinction invalid: {exc}"
        ) from exc

    if operator_directive != OPERATOR_DIRECTIVE_329:
        _reject_freeform(operator_directive, "operator_directive")
        raise VerifiedLoopBeoPublicationBoundedExecutionKernel329ValidationError(
            "operator_directive mismatch"
        )

    package = {
        "status": "BLK_SYSTEM_329_VERIFIED_LOOP_BEO_PUBLICATION_BOUNDED_EXECUTION_KERNEL_READY",
        "markers": list(_MARKERS_329),
        "prior_reconciliation_hash": prior["reconciliation_hash"],
        "development_authority_hash": distinction["distinction_hash"],
        "operator_directive_hash": _hash_text(operator_directive),
        "execution_prerequisites": deepcopy(_EXECUTION_PREREQUISITES_329),
        "receipt_policy": deepcopy(_RECEIPT_POLICY_329),
        "replay_guard": deepcopy(_REPLAY_GUARD_329),
        "next_frontier": NEXT_FRONTIER_329,
        "denied_authorities": list(_DENIED_AUTHORITIES_329),
        "side_effects": dict(_SIDE_EFFECTS_329),
    }
    package["execution_kernel_hash"] = hash_package(package)
    return validate_verified_loop_beo_publication_bounded_execution_kernel_329(package)


def validate_verified_loop_beo_publication_bounded_execution_kernel_329(
    package_329: dict[str, Any],
) -> dict[str, Any]:
    """Validate the BLK-SYSTEM-329 kernel package and canonical hash."""

    package = _require_dict(package_329, "BLK-SYSTEM-329 package")
    _require_allowed_keys(package, _ALLOWED_KEYS_329, "BLK-SYSTEM-329 package")
    if package.get("status") != "BLK_SYSTEM_329_VERIFIED_LOOP_BEO_PUBLICATION_BOUNDED_EXECUTION_KERNEL_READY":
        raise VerifiedLoopBeoPublicationBoundedExecutionKernel329ValidationError("status mismatch")
    if tuple(package.get("markers", ())) != _MARKERS_329:
        raise VerifiedLoopBeoPublicationBoundedExecutionKernel329ValidationError("markers mismatch")
    if package.get("prior_reconciliation_hash") != EXPECTED_315_RECONCILIATION_HASH:
        raise VerifiedLoopBeoPublicationBoundedExecutionKernel329ValidationError(
            "prior reconciliation hash mismatch"
        )
    if package.get("development_authority_hash") != EXPECTED_328_DEVELOPMENT_AUTHORITY_HASH:
        raise VerifiedLoopBeoPublicationBoundedExecutionKernel329ValidationError(
            "development authority hash mismatch"
        )
    if package.get("operator_directive_hash") != _hash_text(OPERATOR_DIRECTIVE_329):
        raise VerifiedLoopBeoPublicationBoundedExecutionKernel329ValidationError(
            "operator_directive_hash mismatch"
        )
    _require_exact_nested(
        package.get("execution_prerequisites"),
        _EXECUTION_PREREQUISITES_329,
        "execution_prerequisites",
    )
    _require_exact_nested(package.get("receipt_policy"), _RECEIPT_POLICY_329, "receipt_policy")
    _require_exact_nested(package.get("replay_guard"), _REPLAY_GUARD_329, "replay_guard")
    if package.get("next_frontier") != NEXT_FRONTIER_329:
        raise VerifiedLoopBeoPublicationBoundedExecutionKernel329ValidationError("next_frontier mismatch")
    _require_exact_list(package.get("denied_authorities"), _DENIED_AUTHORITIES_329, "denied_authorities")
    _require_exact_nested(package.get("side_effects"), _SIDE_EFFECTS_329, "side_effects")
    _require_hash(package, "execution_kernel_hash")
    if EXPECTED_329_EXECUTION_KERNEL_HASH is not None:
        if package["execution_kernel_hash"] != EXPECTED_329_EXECUTION_KERNEL_HASH:
            raise VerifiedLoopBeoPublicationBoundedExecutionKernel329ValidationError(
                "BLK-SYSTEM-329 canonical hash mismatch"
            )
    return deepcopy(package)


def _require_dict(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise VerifiedLoopBeoPublicationBoundedExecutionKernel329ValidationError(
            f"{context} must be a dictionary"
        )
    return value


def _require_allowed_keys(value: dict[str, Any], allowed: frozenset[str], context: str) -> None:
    extras = sorted(set(value) - set(allowed))
    missing = sorted(set(allowed) - set(value))
    if extras or missing:
        raise VerifiedLoopBeoPublicationBoundedExecutionKernel329ValidationError(
            f"{context} key mismatch extras={extras} missing={missing}"
        )


def _require_exact_nested(value: Any, expected: dict[str, Any], field: str) -> None:
    nested = _require_dict(value, field)
    _require_allowed_keys(nested, frozenset(expected), field)
    if nested != expected:
        raise VerifiedLoopBeoPublicationBoundedExecutionKernel329ValidationError(f"{field} mismatch")


def _require_exact_list(value: Any, expected: tuple[str, ...], field: str) -> None:
    if not isinstance(value, list):
        raise VerifiedLoopBeoPublicationBoundedExecutionKernel329ValidationError(f"{field} must be a list")
    if tuple(value) != expected:
        raise VerifiedLoopBeoPublicationBoundedExecutionKernel329ValidationError(f"{field} mismatch")
    if len(value) != len(set(value)):
        raise VerifiedLoopBeoPublicationBoundedExecutionKernel329ValidationError(
            f"{field} must not contain duplicates"
        )


def _require_hash(package: dict[str, Any], field: str) -> None:
    value = package.get(field)
    if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
        raise VerifiedLoopBeoPublicationBoundedExecutionKernel329ValidationError(
            f"{field} must be sha256:<64 hex>"
        )
    body = {key: val for key, val in package.items() if key != field}
    if hash_package(body) != value:
        raise VerifiedLoopBeoPublicationBoundedExecutionKernel329ValidationError(
            f"{field} canonical hash mismatch"
        )


def _reject_freeform(value: Any, path: str) -> None:
    findings = scan_for_authority_laundering(value, path, _DENIED_AUTHORITIES_329)
    if findings:
        raise VerifiedLoopBeoPublicationBoundedExecutionKernel329ValidationError("; ".join(findings))
