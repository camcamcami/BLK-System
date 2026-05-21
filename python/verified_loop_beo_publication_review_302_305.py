"""BLK-SYSTEM-302..305 verified-loop BEO publication review package.

This module consumes the exact BLK-SYSTEM-301 BLK-test oracle verification
reconciliation and the BLK-SYSTEM-251 reusable BEO publication review kernel.
It records a metadata-only review package for the BEO publication path after a
verified loop execution. The package is review-only: it does not capture
approval, reserve or consume run IDs, publish a BEO, execute a BEO closeout,
reuse signer/storage/ledger authority, generate RTM, run production blk-link,
read protected bodies, start tooling, or mutate target/source/Git state.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import hashlib
import json
import re
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering


class VerifiedLoopBeoPublicationReviewValidationError(ValueError):
    """Raised when verified-loop BEO publication review evidence is unsafe."""


_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_ID_RE = re.compile(r"^[A-Z]+(?:-[A-Z0-9]+)+$")
_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$")

EXPECTED_301_RECONCILIATION_HASH = "sha256:7eb8fc4820cc541594479e1ab166164ea2ad0ca60c2a8571a213ecfbee0e8ac1"
EXPECTED_251_RECONCILIATION_HASH = "sha256:4e2acbff751aae66dda868d1e4e06c56b0f210b624a2affa7e4c658bda25dddd"
NEXT_FRONTIER_305 = "NEXT_FRONTIER_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_REQUIRED_NOT_GRANTED"

_MARKERS_302 = (
    "BLK_SYSTEM_302_VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_REQUEST_READY",
    "VERIFIED_LOOP_EVIDENCE_CONSUMED_FOR_BEO_REVIEW_ONLY",
    "BEO_PUBLICATION_APPROVAL_REQUEST_REQUIRED_NOT_GRANTED",
)
_MARKERS_303 = (
    "BLK_SYSTEM_303_VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_CONTRACT_READY",
    "EXACT_APPROVAL_STILL_REQUIRED_AFTER_REVIEW",
    "SIGNER_STORAGE_LEDGER_POLICIES_FALSE",
)
_MARKERS_304 = (
    "BLK_SYSTEM_304_VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_RECORDED",
    "READY_FOR_EXACT_APPROVAL_REQUEST_ONLY",
    "PASS_DOES_NOT_AUTHORIZE_PUBLICATION",
)
_MARKERS_305 = (
    "BLK_SYSTEM_305_VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_RECONCILED",
    "VERIFIED_LOOP_BEO_REVIEW_READY_NOT_PUBLICATION_AUTHORITY",
    "NEXT_EXACT_BEO_APPROVAL_REQUEST_REQUIRED_NOT_GRANTED",
)

_DENIED_AUTHORITIES = (
    "BEO_PUBLICATION_FROM_BLK_TEST_PASS_OR_REVIEW_ALONE",
    "BEO_CLOSEOUT_EXECUTION",
    "AUTHORITATIVE_BEO_PUBLICATION_EXECUTION",
    "REUSABLE_BEO_PUBLICATION_AUTHORITY",
    "SIGNER_KEY_MATERIAL_ACCESS_OR_REUSE",
    "IMMUTABLE_STORAGE_WRITE_OR_REUSE",
    "PUBLIC_LEDGER_APPEND_OR_REUSE",
    "ROLLBACK_REVOCATION_SUPERSESSION_EXECUTION",
    "RTM_GENERATION",
    "PRODUCTION_BLK_LINK",
    "DRIFT_REJECTION",
    "COVERAGE_TRUTH",
    "PROTECTED_BLK_REQ_BODY_ACCESS",
    "BEB_DISPATCH",
    "BLK_PIPE_BLK_TEST_CODEX_RUNTIME",
    "TARGET_SOURCE_GIT_MUTATION",
    "PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING",
    "PRODUCTION_ISOLATION_CLAIM",
    "APPROVAL_REUSE_OR_RUN_ID_REUSE",
)

_REVIEW_RULES = {
    "verified_loop_evidence_required": True,
    "reusable_beo_kernel_required": True,
    "blk_test_pass_is_evidence_not_approval": True,
    "exact_operator_approval_still_required": True,
    "publication_allowed_by_review": False,
    "beo_closeout_allowed_by_review": False,
    "run_id_reservation_allowed_by_review": False,
    "signer_storage_ledger_side_effects_allowed": False,
    "rtm_or_blk_link_allowed_by_review": False,
    "protected_body_access_allowed": False,
    "target_source_git_mutation_allowed": False,
}

_PUBLICATION_POLICIES = {
    "approval_policy": {
        "exact_operator_approval_required": True,
        "generic_approve_is_sufficient": False,
        "approval_reuse_allowed": False,
    },
    "run_id_policy": {
        "fresh_exact_run_id_required": True,
        "run_id_reserved_by_review": False,
        "run_id_consumed_by_review": False,
    },
    "signer_policy": {
        "signer_reuse_allowed": False,
        "signer_key_material_access_allowed": False,
        "signature_generation_allowed_by_review": False,
    },
    "storage_policy": {
        "storage_reuse_allowed": False,
        "immutable_storage_write_allowed_by_review": False,
    },
    "ledger_policy": {
        "ledger_reuse_allowed": False,
        "public_ledger_append_allowed_by_review": False,
    },
    "rollback_policy": {
        "rollback_allowed": False,
        "revocation_allowed": False,
        "supersession_allowed": False,
    },
}

_FALSE_SIDE_EFFECTS = {
    "beo_publication_approval_captured": False,
    "approval_reuse": False,
    "run_id_reserved": False,
    "run_id_consumed": False,
    "beo_closeout_execution": False,
    "beo_publication": False,
    "authoritative_beo_publication": False,
    "reusable_beo_publication": False,
    "signer_reuse": False,
    "signer_key_material_accessed": False,
    "signature_generated": False,
    "storage_reuse": False,
    "immutable_storage_written": False,
    "ledger_reuse": False,
    "public_ledger_mutated": False,
    "rollback_revocation_supersession": False,
    "rtm_generation": False,
    "production_blk_link": False,
    "drift_rejection": False,
    "coverage_truth": False,
    "protected_body_access": False,
    "beb_dispatch": False,
    "blk_test_transport_started": False,
    "blk_pipe_runtime": False,
    "codex_runtime": False,
    "runtime_tooling_executed": False,
    "target_source_git_mutation": False,
    "package_network_model_browser_cyber_tooling": False,
    "production_isolation_claim": False,
}
_REVIEW_SIDE_EFFECTS_302 = {"review_request_prepared": True, **_FALSE_SIDE_EFFECTS}
_REVIEW_SIDE_EFFECTS_303 = {"review_request_prepared": True, "review_contract_prepared": True, **_FALSE_SIDE_EFFECTS}
_REVIEW_SIDE_EFFECTS_304 = {
    "review_request_prepared": True,
    "review_contract_prepared": True,
    "review_recorded": True,
    **_FALSE_SIDE_EFFECTS,
}
_REVIEW_SIDE_EFFECTS_305 = {
    "review_request_prepared": True,
    "review_contract_prepared": True,
    "review_recorded": True,
    "review_reconciled": True,
    **_FALSE_SIDE_EFFECTS,
}

_REQUIRED_REVIEW_HASHES = (
    "verified_loop_reconciliation_hash",
    "verified_loop_record_hash",
    "verified_execution_record_hash",
    "legacy_oracle_reconciliation_hash",
    "reusable_beo_reconciliation_hash",
)
_REVIEW_ASSERTIONS = {
    "verified_loop_reconciled": True,
    "blk_test_passed": True,
    "pass_is_evidence_not_approval": True,
    "beo_draft_hash_available": True,
    "reusable_beo_kernel_ready": True,
    "exact_approval_request_required_next": True,
    "publication_not_executed": True,
    "source_git_mutation_absent": True,
    "protected_body_access_absent": True,
}

_EXPECTED_301_SIDE_EFFECTS = {
    "verification_contract_prepared": True,
    "verification_preflight_recorded": True,
    "verification_recorded": True,
    "verification_reconciled": True,
    "production_mcp_started": False,
    "generic_mcp_started": False,
    "blk_test_transport_started": False,
    "runtime_tooling_executed": False,
    "planner_dispatcher_authority": False,
    "oracle_source_of_truth_claimed": False,
    "blk_test_pass_as_approval": False,
    "source_git_mutation": False,
    "durable_target_source_git_mutation": False,
    "protected_body_accessed": False,
    "beo_closeout_execution": False,
    "beo_publication": False,
    "rtm_generation": False,
    "production_blk_link": False,
    "drift_rejection": False,
    "coverage_truth": False,
    "reusable_codex_dispatch": False,
    "broad_blk_pipe_dispatch": False,
    "package_manager_called": False,
    "network_model_browser_cyber_tooling": False,
    "production_isolation_claim": False,
}
_EXPECTED_251_FALSE_SIDE_EFFECT_KEYS = {
    "reusable_beo_publication_authorized",
    "future_run_authorized",
    "beo_published",
    "signer_reuse_authorized",
    "storage_reuse_authorized",
    "ledger_reuse_authorized",
    "rollback_revocation_supersession",
    "beo_closeout_execution",
    "rtm_generation",
    "production_blk_link",
    "drift_rejection",
    "coverage_truth",
    "protected_body_access",
    "beb_dispatch",
    "blk_pipe_blk_test_codex_runtime",
    "target_source_git_mutation",
    "package_network_model_browser_cyber_tooling",
    "production_isolation_claim",
    "public_ledger_mutated",
    "cryptographic_signature_generated",
}

_KEYS_301 = frozenset(
    {
        "status",
        "markers",
        "verification_contract_hash",
        "verification_preflight_hash",
        "verification_record_hash",
        "verified_loop_reconciliation_hash",
        "verified_execution_record_hash",
        "oracle_reconciliation_hash",
        "verdict",
        "blk_test_passed",
        "pass_is_approval",
        "reconciled_state",
        "next_frontier",
        "side_effects",
        "reconciliation_hash",
    }
)
_KEYS_251 = frozenset(
    {
        "sprint",
        "status",
        "markers",
        "integration_hash",
        "reconciled_state",
        "next_frontier",
        "side_effects",
        "reconciliation_hash",
    }
)
_KEYS_302 = frozenset(
    {
        "status",
        "markers",
        "request_id",
        "requested_at",
        "expires_at",
        "expired",
        "verification_reconciliation_hash",
        "verified_loop_record_hash",
        "verified_execution_record_hash",
        "legacy_oracle_reconciliation_hash",
        "reusable_beo_reconciliation_hash",
        "review_scope",
        "required_review_hashes",
        "denied_authorities",
        "side_effects",
        "review_request_hash",
    }
)
_KEYS_303 = frozenset(
    {
        "status",
        "markers",
        "review_request_hash",
        "verification_reconciliation_hash",
        "reusable_beo_reconciliation_hash",
        "review_rules",
        "publication_policies",
        "required_review_hashes",
        "denied_authorities",
        "side_effects",
        "contract_hash",
    }
)
_REPORT_KEYS = frozenset(
    {
        "review_id",
        "review_result",
        "reviewed_at",
        "verified_hashes",
        "review_assertions",
        "review_notes",
        "denied_side_effects",
    }
)
_KEYS_304 = frozenset(
    {
        "status",
        "markers",
        "contract_hash",
        "review_request_hash",
        "verification_reconciliation_hash",
        "reusable_beo_reconciliation_hash",
        "review_id",
        "review_result",
        "approval_captured",
        "publication_executed",
        "reviewed_at",
        "verified_hashes",
        "review_assertions",
        "review_notes",
        "side_effects",
        "review_record_hash",
    }
)
_KEYS_305 = frozenset(
    {
        "status",
        "markers",
        "contract_hash",
        "review_request_hash",
        "review_record_hash",
        "verification_reconciliation_hash",
        "reusable_beo_reconciliation_hash",
        "review_result",
        "reconciled_state",
        "next_frontier",
        "side_effects",
        "reconciliation_hash",
    }
)
_POLICY_TOP_KEYS = frozenset(
    {
        "approval_policy",
        "run_id_policy",
        "signer_policy",
        "storage_policy",
        "ledger_policy",
        "rollback_policy",
    }
)
_POLICY_NESTED_KEYS = {
    "approval_policy": frozenset(
        {"exact_operator_approval_required", "generic_approve_is_sufficient", "approval_reuse_allowed"}
    ),
    "run_id_policy": frozenset({"fresh_exact_run_id_required", "run_id_reserved_by_review", "run_id_consumed_by_review"}),
    "signer_policy": frozenset(
        {"signer_reuse_allowed", "signer_key_material_access_allowed", "signature_generation_allowed_by_review"}
    ),
    "storage_policy": frozenset({"storage_reuse_allowed", "immutable_storage_write_allowed_by_review"}),
    "ledger_policy": frozenset({"ledger_reuse_allowed", "public_ledger_append_allowed_by_review"}),
    "rollback_policy": frozenset({"rollback_allowed", "revocation_allowed", "supersession_allowed"}),
}
_ALLOWED_REVIEW_RESULTS = ("READY_FOR_EXACT_APPROVAL_REQUEST", "BLOCKED_BY_REVIEW_GAP")
_FORBIDDEN_ID_SEGMENTS = frozenset(
    {
        "APPROVED",
        "AUTHORIZED",
        "AUTHORISED",
        "GRANTED",
        "GREENLIT",
        "PERMITTED",
        "ALLOWED",
        "CAPTURED",
        "RESERVED",
        "CONSUMED",
        "REUSED",
        "PUBLISHED",
        "EXECUTED",
    }
)


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def hash_package(package: dict[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json(package).encode("utf-8")).hexdigest()


def _without_hash(package: dict[str, Any], field: str) -> dict[str, Any]:
    return {key: deepcopy(value) for key, value in package.items() if key != field}


def _deepcopy(value: Any) -> Any:
    return deepcopy(value)


def _require_dict(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise VerifiedLoopBeoPublicationReviewValidationError(f"{context} must be a dictionary")
    return value


def _require_allowed_keys(package: dict[str, Any], allowed: frozenset[str], context: str) -> None:
    extras = sorted(set(package) - allowed)
    if extras:
        raise VerifiedLoopBeoPublicationReviewValidationError(f"{context} unsupported field(s): {', '.join(extras)}")
    missing = sorted(allowed - set(package))
    if missing:
        raise VerifiedLoopBeoPublicationReviewValidationError(f"{context} missing field(s): {', '.join(missing)}")


def _require_hash(value: Any, context: str) -> None:
    if not isinstance(value, str) or not _HASH_RE.match(value):
        raise VerifiedLoopBeoPublicationReviewValidationError(f"{context} must be sha256:<64 lowercase hex>")


def _require_hash_field(package: dict[str, Any], field: str, context: str) -> None:
    _require_hash(package.get(field), f"{context}.{field}")
    expected = hash_package(_without_hash(package, field))
    if package[field] != expected:
        raise VerifiedLoopBeoPublicationReviewValidationError(f"{context} hash mismatch for {field}")


def _require_ascii_string(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value or any(ord(ch) > 127 for ch in value):
        raise VerifiedLoopBeoPublicationReviewValidationError(f"{context} must be a non-empty ASCII string")
    return value


def _reject_laundering(value: Any, context: str) -> None:
    errors = scan_for_authority_laundering(value, path=context)
    if errors:
        raise VerifiedLoopBeoPublicationReviewValidationError(
            f"{context} forbidden authority wording: {'; '.join(errors[:4])}"
        )


def _require_exact_id(value: Any, prefix: str, context: str) -> None:
    value = _require_ascii_string(value, context)
    if not value.startswith(prefix) or not _ID_RE.match(value):
        raise VerifiedLoopBeoPublicationReviewValidationError(f"{context} must be an exact ID with prefix {prefix}")
    forbidden = sorted(set(value.split("-")) & _FORBIDDEN_ID_SEGMENTS)
    if forbidden:
        raise VerifiedLoopBeoPublicationReviewValidationError(
            f"{context} contains forbidden authority segment(s): {', '.join(forbidden)}"
        )
    _reject_laundering(value, context)


def _parse_timestamp(value: Any, context: str) -> datetime:
    if not isinstance(value, str) or not _TIMESTAMP_RE.match(value):
        raise VerifiedLoopBeoPublicationReviewValidationError(f"{context} must be an ISO-8601 timestamp with timezone")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise VerifiedLoopBeoPublicationReviewValidationError(f"{context} must be parseable") from exc
    if parsed.tzinfo is None:
        raise VerifiedLoopBeoPublicationReviewValidationError(f"{context} must include timezone")
    return parsed


def _require_time_window(start: Any, end: Any, start_name: str, end_name: str) -> None:
    parsed_start = _parse_timestamp(start, start_name)
    parsed_end = _parse_timestamp(end, end_name)
    if parsed_end <= parsed_start:
        raise VerifiedLoopBeoPublicationReviewValidationError(f"{end_name} must be after {start_name}")


def _validation_now(tzinfo) -> datetime:
    return datetime.now(tz=tzinfo)


def _require_request_not_expired(expires_at: Any, context: str) -> None:
    parsed_end = _parse_timestamp(expires_at, "expires_at")
    if _validation_now(parsed_end.tzinfo) > parsed_end:
        raise VerifiedLoopBeoPublicationReviewValidationError(f"{context} request window expired/stale")


def _require_timestamp_within(value: Any, start: Any, end: Any, context: str) -> None:
    parsed_value = _parse_timestamp(value, context)
    parsed_start = _parse_timestamp(start, "requested_at")
    parsed_end = _parse_timestamp(end, "expires_at")
    if parsed_value < parsed_start or parsed_value > parsed_end:
        raise VerifiedLoopBeoPublicationReviewValidationError(f"{context} must be within request window")


def _compact(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def _reject_pass_as_approval(text: str, context: str) -> None:
    compact = _compact(text)
    bad_tokens = (
        "passapproves",
        "passauthorizes",
        "passgrants",
        "approvesbeopublication",
        "beopublicationgreenlit",
        "beopublicationauthorized",
        "signerreused",
        "ledgerappended",
        "immutablestoragewritten",
        "reviewgrantsbeopublication",
        "reviewauthorizesbeopublication",
        "reviewapprovesbeopublication",
        "reviewpermitsbeopublication",
        "reviewgreenlightsbeopublication",
        "reviewallowsbeopublication",
        "grantsbeopublication",
        "authorizesbeopublication",
        "approvesbeopublication",
        "permitsbeopublication",
        "greenlightsbeopublication",
        "allowsbeopublication",
        "reviewgrantsbeocloseoutexecution",
        "grantsbeocloseoutexecution",
        "reviewgrantssignerstorageledgerreuse",
        "grantssignerstorageledgerreuse",
        "reviewgrantsrtmgeneration",
        "grantsrtmgeneration",
        "reviewgrantsproductionblklink",
        "grantsproductionblklink",
        "reviewgrantsprotectedbodyaccess",
        "grantsprotectedbodyaccess",
        "reviewgrantstargetsourcegitmutation",
        "grantstargetsourcegitmutation",
        "reviewcapturesapproval",
        "capturesapproval",
        "reviewreservesrunid",
        "reservesrunid",
    )
    if any(token in compact for token in bad_tokens):
        raise VerifiedLoopBeoPublicationReviewValidationError(
            f"{context} forbidden authority wording: PASS/review text must not imply approval"
        )
    grant_tokens = (
        "grants",
        "authorizes",
        "authorises",
        "approves",
        "permits",
        "greenlights",
        "allows",
        "captures",
        "reserves",
        "consumes",
        "executes",
        "publishes",
        "reuses",
    )
    authority_subjects = (
        "approval",
        "publication",
        "publicationauthority",
        "beopublication",
        "beocloseout",
        "closeoutexecution",
        "signer",
        "storage",
        "ledger",
        "runid",
        "rtm",
        "rtmgeneration",
        "blklink",
        "protectedbody",
        "mutation",
        "gitmutation",
        "targetsourcegitmutation",
    )
    if any(grant in compact for grant in grant_tokens) and any(subject in compact for subject in authority_subjects):
        raise VerifiedLoopBeoPublicationReviewValidationError(
            f"{context} forbidden authority wording: review text must not grant authority"
        )


def _require_denied_authorities(value: Any, context: str) -> None:
    if not isinstance(value, list):
        raise VerifiedLoopBeoPublicationReviewValidationError(f"{context} denied_authorities must be a list")
    if value != list(_DENIED_AUTHORITIES):
        raise VerifiedLoopBeoPublicationReviewValidationError(f"{context} denied_authorities mismatch")
    if len(value) != len(set(value)):
        raise VerifiedLoopBeoPublicationReviewValidationError(f"{context} denied_authorities contains duplicates")


def _require_side_effects(value: Any, expected: dict[str, bool], context: str) -> None:
    if value != expected:
        if isinstance(value, dict):
            for key, expected_value in expected.items():
                if expected_value is False and value.get(key) is not False:
                    raise VerifiedLoopBeoPublicationReviewValidationError(
                        f"{context} side_effects {key} must remain false"
                    )
        raise VerifiedLoopBeoPublicationReviewValidationError(f"{context} side_effects mismatch")


def _expected_verified_hashes(
    contract: dict[str, Any],
    verification_reconciliation_301: dict[str, Any],
    reusable_beo_reconciliation_251: dict[str, Any],
) -> dict[str, str]:
    return {
        "verified_loop_reconciliation_hash": verification_reconciliation_301["reconciliation_hash"],
        "verified_loop_record_hash": verification_reconciliation_301["verification_record_hash"],
        "verified_execution_record_hash": verification_reconciliation_301["verified_execution_record_hash"],
        "legacy_oracle_reconciliation_hash": verification_reconciliation_301["oracle_reconciliation_hash"],
        "reusable_beo_reconciliation_hash": reusable_beo_reconciliation_251["reconciliation_hash"],
    }


def _validate_301_reconciliation(package: dict[str, Any]) -> dict[str, Any]:
    candidate = _require_dict(package, "BLK-SYSTEM-301 reconciliation")
    _require_allowed_keys(candidate, _KEYS_301, "BLK-SYSTEM-301 reconciliation")
    if candidate.get("reconciliation_hash") != EXPECTED_301_RECONCILIATION_HASH:
        raise VerifiedLoopBeoPublicationReviewValidationError("BLK-SYSTEM-301 canonical reconciliation hash mismatch")
    _require_hash_field(candidate, "reconciliation_hash", "BLK-SYSTEM-301 reconciliation")
    if candidate.get("status") != "EXACT_BLK_TEST_ORACLE_VERIFICATION_RECONCILED_VERIFIER_ONLY":
        raise VerifiedLoopBeoPublicationReviewValidationError("BLK-SYSTEM-301 status mismatch")
    if candidate.get("next_frontier") != "NEXT_FRONTIER_VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_REQUIRED_NOT_GRANTED":
        raise VerifiedLoopBeoPublicationReviewValidationError("BLK-SYSTEM-301 next frontier mismatch")
    if candidate.get("verdict") != "PASS" or candidate.get("blk_test_passed") is not True:
        raise VerifiedLoopBeoPublicationReviewValidationError("BLK-SYSTEM-301 must be PASS evidence")
    if candidate.get("pass_is_approval") is not False:
        raise VerifiedLoopBeoPublicationReviewValidationError("BLK-SYSTEM-301 PASS must not be approval")
    _require_side_effects(candidate.get("side_effects"), _EXPECTED_301_SIDE_EFFECTS, "BLK-SYSTEM-301")
    _reject_laundering(candidate, "BLK-SYSTEM-301 reconciliation")
    return _deepcopy(candidate)


def _validate_251_reconciliation(package: dict[str, Any]) -> dict[str, Any]:
    candidate = _require_dict(package, "BLK-SYSTEM-251 reconciliation")
    _require_allowed_keys(candidate, _KEYS_251, "BLK-SYSTEM-251 reconciliation")
    if candidate.get("reconciliation_hash") != EXPECTED_251_RECONCILIATION_HASH:
        raise VerifiedLoopBeoPublicationReviewValidationError("BLK-SYSTEM-251 canonical reconciliation hash mismatch")
    _require_hash_field(candidate, "reconciliation_hash", "BLK-SYSTEM-251 reconciliation")
    if candidate.get("status") != "REUSABLE_BEO_PUBLICATION_RECONCILED_PER_RUN_EXACT_APPROVAL_READY":
        raise VerifiedLoopBeoPublicationReviewValidationError("BLK-SYSTEM-251 status mismatch")
    if candidate.get("next_frontier") != "NEXT_FRONTIER_RTM_PRODUCTION_BLK_LINK_DRIFT_COVERAGE_REQUEST_NOT_GRANTED":
        raise VerifiedLoopBeoPublicationReviewValidationError("BLK-SYSTEM-251 next frontier mismatch")
    side_effects = candidate.get("side_effects")
    if not isinstance(side_effects, dict) or set(side_effects) != _EXPECTED_251_FALSE_SIDE_EFFECT_KEYS:
        raise VerifiedLoopBeoPublicationReviewValidationError("BLK-SYSTEM-251 side_effects key set mismatch")
    for key in _EXPECTED_251_FALSE_SIDE_EFFECT_KEYS:
        if side_effects.get(key) is not False:
            raise VerifiedLoopBeoPublicationReviewValidationError(f"BLK-SYSTEM-251 side_effects {key} must remain false")
    _reject_laundering(candidate, "BLK-SYSTEM-251 reconciliation")
    return _deepcopy(candidate)


def _validate_publication_policies(value: Any) -> dict[str, Any]:
    policies = _require_dict(value, "publication_policies")
    if set(policies) != _POLICY_TOP_KEYS:
        raise VerifiedLoopBeoPublicationReviewValidationError("publication_policies key set mismatch")
    for key, allowed in _POLICY_NESTED_KEYS.items():
        nested = _require_dict(policies.get(key), f"publication_policies.{key}")
        if set(nested) != allowed:
            raise VerifiedLoopBeoPublicationReviewValidationError(f"publication_policies.{key} key set mismatch")
        for nested_key, nested_value in nested.items():
            expected = _PUBLICATION_POLICIES[key][nested_key]
            if nested_value is not expected:
                raise VerifiedLoopBeoPublicationReviewValidationError(
                    f"publication_policies.{key}.{nested_key} mismatch"
                )
    _reject_laundering(policies, "publication_policies")
    return _deepcopy(policies)


def build_verified_loop_beo_publication_review_request_302(
    verification_reconciliation_301: dict[str, Any],
    reusable_beo_reconciliation_251: dict[str, Any],
    *,
    request_id: str,
    requested_at: str,
    expires_at: str,
) -> dict[str, Any]:
    """Build a review request over verified loop evidence without granting publication."""

    verification = _validate_301_reconciliation(verification_reconciliation_301)
    beo = _validate_251_reconciliation(reusable_beo_reconciliation_251)
    _require_exact_id(request_id, "BEO-REVIEW-REQUEST-", "request_id")
    _require_time_window(requested_at, expires_at, "requested_at", "expires_at")
    request = {
        "status": "VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_REQUEST_READY_NOT_GRANTED",
        "markers": list(_MARKERS_302),
        "request_id": request_id,
        "requested_at": requested_at,
        "expires_at": expires_at,
        "expired": False,
        "verification_reconciliation_hash": verification["reconciliation_hash"],
        "verified_loop_record_hash": verification["verification_record_hash"],
        "verified_execution_record_hash": verification["verified_execution_record_hash"],
        "legacy_oracle_reconciliation_hash": verification["oracle_reconciliation_hash"],
        "reusable_beo_reconciliation_hash": beo["reconciliation_hash"],
        "review_scope": "metadata_only_review_for_exact_beo_publication_approval_request",
        "required_review_hashes": list(_REQUIRED_REVIEW_HASHES),
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_REVIEW_SIDE_EFFECTS_302),
    }
    request["review_request_hash"] = hash_package(request)
    return validate_verified_loop_beo_publication_review_request_302(request, verification, beo)


def validate_verified_loop_beo_publication_review_request_302(
    review_request_302: dict[str, Any],
    verification_reconciliation_301: dict[str, Any],
    reusable_beo_reconciliation_251: dict[str, Any],
) -> dict[str, Any]:
    verification = _validate_301_reconciliation(verification_reconciliation_301)
    beo = _validate_251_reconciliation(reusable_beo_reconciliation_251)
    request = _require_dict(review_request_302, "review request")
    _require_allowed_keys(request, _KEYS_302, "review request")
    if request.get("status") != "VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_REQUEST_READY_NOT_GRANTED":
        raise VerifiedLoopBeoPublicationReviewValidationError("review request status mismatch")
    if tuple(request.get("markers", ())) != _MARKERS_302:
        raise VerifiedLoopBeoPublicationReviewValidationError("review request markers mismatch")
    _require_exact_id(request.get("request_id"), "BEO-REVIEW-REQUEST-", "request_id")
    _require_time_window(request.get("requested_at"), request.get("expires_at"), "requested_at", "expires_at")
    _require_request_not_expired(request.get("expires_at"), "review request")
    if request.get("expired") is not False:
        raise VerifiedLoopBeoPublicationReviewValidationError("review request expired must be false")
    expected = {
        "verification_reconciliation_hash": verification["reconciliation_hash"],
        "verified_loop_record_hash": verification["verification_record_hash"],
        "verified_execution_record_hash": verification["verified_execution_record_hash"],
        "legacy_oracle_reconciliation_hash": verification["oracle_reconciliation_hash"],
        "reusable_beo_reconciliation_hash": beo["reconciliation_hash"],
    }
    for field, value in expected.items():
        if request.get(field) != value:
            raise VerifiedLoopBeoPublicationReviewValidationError(f"review request {field} mismatch")
    if request.get("review_scope") != "metadata_only_review_for_exact_beo_publication_approval_request":
        raise VerifiedLoopBeoPublicationReviewValidationError("review request scope mismatch")
    if request.get("required_review_hashes") != list(_REQUIRED_REVIEW_HASHES):
        raise VerifiedLoopBeoPublicationReviewValidationError("review request required_review_hashes mismatch")
    _require_denied_authorities(request.get("denied_authorities"), "review request")
    _require_side_effects(request.get("side_effects"), _REVIEW_SIDE_EFFECTS_302, "review request")
    _require_hash_field(request, "review_request_hash", "review request")
    _reject_laundering(request, "review request")
    return _deepcopy(request)


def build_verified_loop_beo_publication_review_contract_303(
    review_request_302: dict[str, Any],
    verification_reconciliation_301: dict[str, Any],
    reusable_beo_reconciliation_251: dict[str, Any],
) -> dict[str, Any]:
    """Build a closed review contract while all publication authority stays denied."""

    request = validate_verified_loop_beo_publication_review_request_302(
        review_request_302,
        verification_reconciliation_301,
        reusable_beo_reconciliation_251,
    )
    contract = {
        "status": "VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_CONTRACT_READY",
        "markers": list(_MARKERS_303),
        "review_request_hash": request["review_request_hash"],
        "verification_reconciliation_hash": request["verification_reconciliation_hash"],
        "reusable_beo_reconciliation_hash": request["reusable_beo_reconciliation_hash"],
        "review_rules": dict(_REVIEW_RULES),
        "publication_policies": _deepcopy(_PUBLICATION_POLICIES),
        "required_review_hashes": list(_REQUIRED_REVIEW_HASHES),
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_REVIEW_SIDE_EFFECTS_303),
    }
    contract["contract_hash"] = hash_package(contract)
    return validate_verified_loop_beo_publication_review_contract_303(
        contract,
        request,
        verification_reconciliation_301,
        reusable_beo_reconciliation_251,
    )


def validate_verified_loop_beo_publication_review_contract_303(
    review_contract_303: dict[str, Any],
    review_request_302: dict[str, Any],
    verification_reconciliation_301: dict[str, Any],
    reusable_beo_reconciliation_251: dict[str, Any],
) -> dict[str, Any]:
    request = validate_verified_loop_beo_publication_review_request_302(
        review_request_302,
        verification_reconciliation_301,
        reusable_beo_reconciliation_251,
    )
    contract = _require_dict(review_contract_303, "review contract")
    _require_allowed_keys(contract, _KEYS_303, "review contract")
    if contract.get("status") != "VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_CONTRACT_READY":
        raise VerifiedLoopBeoPublicationReviewValidationError("review contract status mismatch")
    if tuple(contract.get("markers", ())) != _MARKERS_303:
        raise VerifiedLoopBeoPublicationReviewValidationError("review contract markers mismatch")
    expected = {
        "review_request_hash": request["review_request_hash"],
        "verification_reconciliation_hash": request["verification_reconciliation_hash"],
        "reusable_beo_reconciliation_hash": request["reusable_beo_reconciliation_hash"],
    }
    for field, value in expected.items():
        if contract.get(field) != value:
            raise VerifiedLoopBeoPublicationReviewValidationError(f"review contract {field} mismatch")
    if contract.get("review_rules") != _REVIEW_RULES:
        raise VerifiedLoopBeoPublicationReviewValidationError("review contract review_rules mismatch")
    _validate_publication_policies(contract.get("publication_policies"))
    if contract.get("required_review_hashes") != list(_REQUIRED_REVIEW_HASHES):
        raise VerifiedLoopBeoPublicationReviewValidationError("review contract required_review_hashes mismatch")
    _require_denied_authorities(contract.get("denied_authorities"), "review contract")
    _require_side_effects(contract.get("side_effects"), _REVIEW_SIDE_EFFECTS_303, "review contract")
    _require_hash_field(contract, "contract_hash", "review contract")
    _reject_laundering(contract, "review contract")
    return _deepcopy(contract)


def sample_verified_loop_beo_publication_review_report(
    review_contract_303: dict[str, Any],
    verification_reconciliation_301: dict[str, Any],
    reusable_beo_reconciliation_251: dict[str, Any],
    *,
    reviewed_at: str,
    review_result: str = "READY_FOR_EXACT_APPROVAL_REQUEST",
) -> dict[str, Any]:
    """Return one safe metadata-only BEO publication-path review report."""

    if review_result not in _ALLOWED_REVIEW_RESULTS:
        raise VerifiedLoopBeoPublicationReviewValidationError("review_result must use closed vocabulary")
    return {
        "review_id": "BEO-PUBLICATION-REVIEW-BLK-SYSTEM-304-001",
        "review_result": review_result,
        "reviewed_at": reviewed_at,
        "verified_hashes": _expected_verified_hashes(
            review_contract_303,
            verification_reconciliation_301,
            reusable_beo_reconciliation_251,
        ),
        "review_assertions": dict(_REVIEW_ASSERTIONS),
        "review_notes": "metadata-only review: exact approval request required next; no publication or mutation",
        "denied_side_effects": dict(_FALSE_SIDE_EFFECTS),
    }


def _validate_review_report(
    report: dict[str, Any],
    contract: dict[str, Any],
    request: dict[str, Any],
    verification: dict[str, Any],
    beo: dict[str, Any],
) -> dict[str, Any]:
    report = _require_dict(report, "review report")
    _require_allowed_keys(report, _REPORT_KEYS, "review report")
    _require_exact_id(report.get("review_id"), "BEO-PUBLICATION-REVIEW-", "review report review_id")
    if report.get("review_result") not in _ALLOWED_REVIEW_RESULTS:
        raise VerifiedLoopBeoPublicationReviewValidationError("review report result must use closed vocabulary")
    if report.get("review_result") != "READY_FOR_EXACT_APPROVAL_REQUEST":
        raise VerifiedLoopBeoPublicationReviewValidationError(
            "review report must be READY_FOR_EXACT_APPROVAL_REQUEST before approval frontier"
        )
    _require_timestamp_within(report.get("reviewed_at"), request["requested_at"], request["expires_at"], "reviewed_at")
    hashes = _require_dict(report.get("verified_hashes"), "review report verified_hashes")
    if tuple(hashes) != _REQUIRED_REVIEW_HASHES:
        raise VerifiedLoopBeoPublicationReviewValidationError("review report verified_hashes key order or set mismatch")
    expected_hashes = _expected_verified_hashes(contract, verification, beo)
    for field, expected in expected_hashes.items():
        if hashes.get(field) != expected:
            raise VerifiedLoopBeoPublicationReviewValidationError(f"review report verified hash {field} mismatch")
        _require_hash(hashes[field], f"review report verified_hashes.{field}")
    if report.get("review_assertions") != _REVIEW_ASSERTIONS:
        raise VerifiedLoopBeoPublicationReviewValidationError("review report assertions mismatch")
    if report.get("denied_side_effects") != _FALSE_SIDE_EFFECTS:
        raise VerifiedLoopBeoPublicationReviewValidationError("review report denied_side_effects mismatch")
    notes = report.get("review_notes")
    if not isinstance(notes, str) or len(notes) > 240:
        raise VerifiedLoopBeoPublicationReviewValidationError("review report notes must be a short string")
    _reject_pass_as_approval(notes, "review report")
    _reject_laundering(report, "review report")
    return _deepcopy(report)


def record_verified_loop_beo_publication_review_304(
    review_contract_303: dict[str, Any],
    review_request_302: dict[str, Any],
    verification_reconciliation_301: dict[str, Any],
    reusable_beo_reconciliation_251: dict[str, Any],
    *,
    review_report: dict[str, Any],
) -> dict[str, Any]:
    """Record metadata-only BEO publication review evidence."""

    contract = validate_verified_loop_beo_publication_review_contract_303(
        review_contract_303,
        review_request_302,
        verification_reconciliation_301,
        reusable_beo_reconciliation_251,
    )
    request = validate_verified_loop_beo_publication_review_request_302(
        review_request_302,
        verification_reconciliation_301,
        reusable_beo_reconciliation_251,
    )
    verification = _validate_301_reconciliation(verification_reconciliation_301)
    beo = _validate_251_reconciliation(reusable_beo_reconciliation_251)
    report = _validate_review_report(review_report, contract, request, verification, beo)
    record = {
        "status": "VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_RECORDED",
        "markers": list(_MARKERS_304),
        "contract_hash": contract["contract_hash"],
        "review_request_hash": request["review_request_hash"],
        "verification_reconciliation_hash": verification["reconciliation_hash"],
        "reusable_beo_reconciliation_hash": beo["reconciliation_hash"],
        "review_id": report["review_id"],
        "review_result": report["review_result"],
        "approval_captured": False,
        "publication_executed": False,
        "reviewed_at": report["reviewed_at"],
        "verified_hashes": report["verified_hashes"],
        "review_assertions": report["review_assertions"],
        "review_notes": report["review_notes"],
        "side_effects": dict(_REVIEW_SIDE_EFFECTS_304),
    }
    record["review_record_hash"] = hash_package(record)
    return validate_verified_loop_beo_publication_review_record_304(record, contract, request, verification, beo)


def validate_verified_loop_beo_publication_review_record_304(
    review_record_304: dict[str, Any],
    review_contract_303: dict[str, Any],
    review_request_302: dict[str, Any],
    verification_reconciliation_301: dict[str, Any],
    reusable_beo_reconciliation_251: dict[str, Any],
) -> dict[str, Any]:
    contract = validate_verified_loop_beo_publication_review_contract_303(
        review_contract_303,
        review_request_302,
        verification_reconciliation_301,
        reusable_beo_reconciliation_251,
    )
    request = validate_verified_loop_beo_publication_review_request_302(
        review_request_302,
        verification_reconciliation_301,
        reusable_beo_reconciliation_251,
    )
    verification = _validate_301_reconciliation(verification_reconciliation_301)
    beo = _validate_251_reconciliation(reusable_beo_reconciliation_251)
    record = _require_dict(review_record_304, "review record")
    _require_allowed_keys(record, _KEYS_304, "review record")
    if record.get("status") != "VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_RECORDED":
        raise VerifiedLoopBeoPublicationReviewValidationError("review record status mismatch")
    if tuple(record.get("markers", ())) != _MARKERS_304:
        raise VerifiedLoopBeoPublicationReviewValidationError("review record markers mismatch")
    expected = {
        "contract_hash": contract["contract_hash"],
        "review_request_hash": request["review_request_hash"],
        "verification_reconciliation_hash": verification["reconciliation_hash"],
        "reusable_beo_reconciliation_hash": beo["reconciliation_hash"],
    }
    for field, value in expected.items():
        if record.get(field) != value:
            raise VerifiedLoopBeoPublicationReviewValidationError(f"review record {field} mismatch")
    _require_exact_id(record.get("review_id"), "BEO-PUBLICATION-REVIEW-", "review record review_id")
    if record.get("review_result") not in _ALLOWED_REVIEW_RESULTS:
        raise VerifiedLoopBeoPublicationReviewValidationError("review record result must use closed vocabulary")
    if record.get("review_result") != "READY_FOR_EXACT_APPROVAL_REQUEST":
        raise VerifiedLoopBeoPublicationReviewValidationError(
            "review record must be READY_FOR_EXACT_APPROVAL_REQUEST before approval frontier"
        )
    if record.get("approval_captured") is not False:
        raise VerifiedLoopBeoPublicationReviewValidationError("review record must not capture approval")
    if record.get("publication_executed") is not False:
        raise VerifiedLoopBeoPublicationReviewValidationError("review record must not execute publication")
    _require_timestamp_within(record.get("reviewed_at"), request["requested_at"], request["expires_at"], "reviewed_at")
    hashes = _require_dict(record.get("verified_hashes"), "review record verified_hashes")
    if tuple(hashes) != _REQUIRED_REVIEW_HASHES:
        raise VerifiedLoopBeoPublicationReviewValidationError("review record verified_hashes key order or set mismatch")
    expected_hashes = _expected_verified_hashes(contract, verification, beo)
    for field, value in expected_hashes.items():
        if hashes.get(field) != value:
            raise VerifiedLoopBeoPublicationReviewValidationError(f"review record verified hash {field} mismatch")
    if record.get("review_assertions") != _REVIEW_ASSERTIONS:
        raise VerifiedLoopBeoPublicationReviewValidationError("review record assertions mismatch")
    _require_side_effects(record.get("side_effects"), _REVIEW_SIDE_EFFECTS_304, "review record")
    _require_hash_field(record, "review_record_hash", "review record")
    _reject_pass_as_approval(record.get("review_notes", ""), "review record")
    _reject_laundering(record, "review record")
    return _deepcopy(record)


def reconcile_verified_loop_beo_publication_review_305(
    review_contract_303: dict[str, Any],
    review_request_302: dict[str, Any],
    review_record_304: dict[str, Any],
    verification_reconciliation_301: dict[str, Any],
    reusable_beo_reconciliation_251: dict[str, Any],
) -> dict[str, Any]:
    """Reconcile verified-loop BEO review and select exact approval-request frontier."""

    contract = validate_verified_loop_beo_publication_review_contract_303(
        review_contract_303,
        review_request_302,
        verification_reconciliation_301,
        reusable_beo_reconciliation_251,
    )
    request = validate_verified_loop_beo_publication_review_request_302(
        review_request_302,
        verification_reconciliation_301,
        reusable_beo_reconciliation_251,
    )
    record = validate_verified_loop_beo_publication_review_record_304(
        review_record_304,
        contract,
        request,
        verification_reconciliation_301,
        reusable_beo_reconciliation_251,
    )
    reconciliation = {
        "status": "VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_RECONCILED",
        "markers": list(_MARKERS_305),
        "contract_hash": contract["contract_hash"],
        "review_request_hash": request["review_request_hash"],
        "review_record_hash": record["review_record_hash"],
        "verification_reconciliation_hash": record["verification_reconciliation_hash"],
        "reusable_beo_reconciliation_hash": record["reusable_beo_reconciliation_hash"],
        "review_result": record["review_result"],
        "reconciled_state": "verified_loop_beo_publication_review_ready_for_exact_approval_request_not_granted",
        "next_frontier": NEXT_FRONTIER_305,
        "side_effects": dict(_REVIEW_SIDE_EFFECTS_305),
    }
    reconciliation["reconciliation_hash"] = hash_package(reconciliation)
    return validate_verified_loop_beo_publication_review_reconciliation_305(
        reconciliation,
        contract,
        request,
        record,
        verification_reconciliation_301,
        reusable_beo_reconciliation_251,
    )


def validate_verified_loop_beo_publication_review_reconciliation_305(
    reconciliation_305: dict[str, Any],
    review_contract_303: dict[str, Any],
    review_request_302: dict[str, Any],
    review_record_304: dict[str, Any],
    verification_reconciliation_301: dict[str, Any],
    reusable_beo_reconciliation_251: dict[str, Any],
) -> dict[str, Any]:
    contract = validate_verified_loop_beo_publication_review_contract_303(
        review_contract_303,
        review_request_302,
        verification_reconciliation_301,
        reusable_beo_reconciliation_251,
    )
    request = validate_verified_loop_beo_publication_review_request_302(
        review_request_302,
        verification_reconciliation_301,
        reusable_beo_reconciliation_251,
    )
    record = validate_verified_loop_beo_publication_review_record_304(
        review_record_304,
        contract,
        request,
        verification_reconciliation_301,
        reusable_beo_reconciliation_251,
    )
    reconciliation = _require_dict(reconciliation_305, "review reconciliation")
    _require_allowed_keys(reconciliation, _KEYS_305, "review reconciliation")
    if reconciliation.get("status") != "VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_RECONCILED":
        raise VerifiedLoopBeoPublicationReviewValidationError("review reconciliation status mismatch")
    if tuple(reconciliation.get("markers", ())) != _MARKERS_305:
        raise VerifiedLoopBeoPublicationReviewValidationError("review reconciliation markers mismatch")
    expected = {
        "contract_hash": contract["contract_hash"],
        "review_request_hash": request["review_request_hash"],
        "review_record_hash": record["review_record_hash"],
        "verification_reconciliation_hash": record["verification_reconciliation_hash"],
        "reusable_beo_reconciliation_hash": record["reusable_beo_reconciliation_hash"],
        "review_result": record["review_result"],
        "reconciled_state": "verified_loop_beo_publication_review_ready_for_exact_approval_request_not_granted",
        "next_frontier": NEXT_FRONTIER_305,
    }
    for field, value in expected.items():
        if reconciliation.get(field) != value:
            raise VerifiedLoopBeoPublicationReviewValidationError(f"review reconciliation {field} mismatch")
    _require_side_effects(reconciliation.get("side_effects"), _REVIEW_SIDE_EFFECTS_305, "review reconciliation")
    _require_hash_field(reconciliation, "reconciliation_hash", "review reconciliation")
    _reject_laundering(reconciliation, "review reconciliation")
    return _deepcopy(reconciliation)
