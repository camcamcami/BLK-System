"""Fixture-only authoritative BEO publication authority request.

This module validates and builds deterministic local request-readiness packages
for a future authoritative BEO publication decision. It does not publish BEOs,
sign artifacts, write storage, mutate public ledgers, execute rollback, generate
RTM output, or read protected BLK-req bodies.
"""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from typing import Any
from urllib.parse import unquote

AUTHORITY_REQUEST_READY = "AUTHORITATIVE_BEO_PUBLICATION_AUTHORITY_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_PUBLICATION"
APPROVAL_SCOPE = "AUTHORITATIVE_BEO_PUBLICATION_AUTHORITY_REQUEST_ONLY"
CANDIDATE_STATUS = "PUBLICATION_CANDIDATE_FIXTURE_ONLY"
DRAFT_ONLY = "DRAFT_ONLY"
NOT_GENERATED = "NOT_GENERATED"
HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")

EXACT_EXCLUDED_AUTHORITIES = {
    "AUTHORITATIVE_BEO_PUBLICATION",
    "RUNTIME_PUBLISHED_BEO_OUTPUT",
    "LIVE_PUBLICATION_APPROVAL_CAPTURE",
    "SIGNER_KEY_MATERIAL_ACCESS",
    "CRYPTOGRAPHIC_SIGNING",
    "IMMUTABLE_STORAGE_WRITE",
    "PUBLIC_LEDGER_MUTATION",
    "ROLLBACK_EXECUTION",
    "REVOCATION_EXECUTION",
    "SUPERSESSION_EXECUTION",
    "RTM_GENERATION",
    "RTM_DRIFT_REJECTION",
    "ACTIVE_VAULT_HASH_COMPARISON",
    "COVERAGE_MATRIX",
    "COVERAGE_CLAIM",
    "DRIFT_DECISION",
    "PROTECTED_BLK_REQ_BODY_READ",
}

_SOURCE_CANDIDATE_KEYS = {
    "candidate_id",
    "candidate_status",
    "beo_id",
    "beo_hash",
    "beb_id",
    "status",
    "source_evidence",
    "trace_artifacts",
    "beo_publication",
    "rtm_status",
    "published",
    "active_vault_read",
    "key_material_accessed",
    "immutable_storage_written",
    "public_ledger_mutated",
    "rollback_executed",
    "operator_note",
    "evidence_ref",
}
_SOURCE_EVIDENCE_KEYS = {"run_id", "tool_name", "source_evidence_hash", "cleanup_status"}
_TRACE_ARTIFACT_KEYS = {"kind", "id", "version_hash"}
_APPROVAL_REQUEST_KEYS = {
    "request_id",
    "operator_identity",
    "request_hash",
    "approved_candidate_id",
    "approved_beo_id",
    "approved_beo_hash",
    "source_evidence_hash",
    "approval_scope",
    "requested_at",
    "expired",
    "replayed",
    "stale",
    "excluded_authorities",
}
_SIGNER_POLICY_KEYS = {"signer_identity", "signer_policy_hash", "key_material_accessed", "signature_generated", "secret_read"}
_STORAGE_POLICY_KEYS = {"storage_target_identity", "storage_policy_hash", "immutable_storage_written", "storage_write_attempted"}
_LEDGER_POLICY_KEYS = {"ledger_target_identity", "ledger_policy_hash", "public_ledger_mutated", "ledger_append_attempted"}
_ROLLBACK_POLICY_KEYS = {"rollback_fixture_identity", "rollback_policy_hash", "rollback_executed", "revocation_executed", "supersession_executed"}

_PUBLICATION_AUTHORITY_FIELDS = {
    "published_at",
    "publication_authority",
    "beo_publication_authority",
    "live_publication_approval_captured",
    "signature",
    "signer_key_material",
    "key_material",
    "private" + "_key",
}
_SIDE_EFFECT_FIELDS = {
    "published",
    "publication_performed",
    "signature_generated",
    "key_material_accessed",
    "immutable_storage_written",
    "storage_write_attempted",
    "public_ledger_mutated",
    "ledger_append_attempted",
    "rollback_executed",
    "revocation_executed",
    "supersession_executed",
    "secret_read",
}
_RTM_AUTHORITY_FIELDS = {
    "rtm",
    "rtm_id",
    "rtm_generated",
    "requirements",
    "coverage",
    "coverage_matrix",
    "coverage_status",
    "drift",
    "drift_status",
    "drift_decision",
    "drift_decision_made",
    "active_vault_hash_comparison",
}
_SECRET_KEYS = {
    "secret",
    "secret_value",
    "token",
    "api_key",
    "password",
    "passphrase",
    "private" + "_key",
    "key_material",
    "signer_key_material",
}
_FORBIDDEN_TEXT_RE = re.compile(
    r"\b(authoritative[_\s-]+beo[_\s-]+publication|beo[_\s-]+publication[_\s-]+approved|publish(?:ed)?[_\s-]+beo|published|"
    r"runtime[_\s-]+published[_\s-]+beo|rtm[_\s-]+generation|drift[_\s-]+rejection|public[_\s-]+ledger[_\s-]+mutation|"
    r"signer[_\s-]+key[_\s-]+material|immutable[_\s-]+storage[_\s-]+write|rollback[_\s-]+execut(?:e|ion))\b",
    re.IGNORECASE,
)
_PROTECTED_BODY_RE = re.compile(r"docs[\\/]+(?:active|requirements|use_cases)[\\/]+|protected\s+blk-req\s+body", re.IGNORECASE)


def build_authoritative_beo_publication_authority_request(
    source_candidate: dict[str, Any],
    approval_request: dict[str, Any],
    signer_policy: dict[str, Any],
    storage_policy: dict[str, Any],
    ledger_policy: dict[str, Any],
    rollback_policy: dict[str, Any],
) -> dict[str, Any]:
    """Build a request-readiness fixture and prove no publication side effects."""

    candidate = _validate_source_candidate(source_candidate)
    approval = _validate_approval_request(
        approval_request,
        expected_candidate_id=candidate["candidate_id"],
        expected_beo_id=candidate["beo_id"],
        expected_beo_hash=candidate["beo_hash"],
        expected_source_evidence_hash=candidate["source_evidence_hash"],
    )
    signer = _validate_signer_policy(signer_policy)
    storage = _validate_storage_policy(storage_policy)
    ledger = _validate_ledger_policy(ledger_policy)
    rollback = _validate_rollback_policy(rollback_policy)

    request = {
        "request_status": AUTHORITY_REQUEST_READY,
        "request_id": approval["request_id"],
        "operator_identity": approval["operator_identity"],
        "approval_scope": APPROVAL_SCOPE,
        "candidate_id": candidate["candidate_id"],
        "beo_id": candidate["beo_id"],
        "beo_hash": candidate["beo_hash"],
        "beb_id": candidate["beb_id"],
        "source_evidence_hash": candidate["source_evidence_hash"],
        "trace_artifacts": candidate["trace_artifacts"],
        "signer_policy": signer,
        "storage_policy": storage,
        "ledger_policy": ledger,
        "rollback_policy": rollback,
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
        "publication_performed": False,
        "beo_publication": "AUTHORITY_REQUEST_ONLY_NOT_PUBLISHED",
        "runtime_published_beo_output": False,
        "live_publication_approval_captured": False,
        "signature_generated": False,
        "key_material_accessed": False,
        "immutable_storage_written": False,
        "public_ledger_mutated": False,
        "rollback_executed": False,
        "revocation_executed": False,
        "supersession_executed": False,
        "rtm_generated": False,
        "rtm_status": NOT_GENERATED,
        "drift_decision_made": False,
        "protected_body_read": False,
        "active_vault_read": False,
    }
    request["request_hash"] = _canonical_hash({k: v for k, v in request.items() if k != "request_hash"})
    return request


def _validate_source_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    _require_dict(candidate, "source_candidate")
    _reject_forbidden_fields(candidate, "source_candidate")
    _enforce_allowed_keys(candidate, _SOURCE_CANDIDATE_KEYS, "source_candidate")
    if _required_string(candidate.get("candidate_status"), "candidate_status") != CANDIDATE_STATUS:
        raise ValueError("candidate_status must be PUBLICATION_CANDIDATE_FIXTURE_ONLY")
    status = _required_string(candidate.get("status"), "status")
    if status not in {"PASS", "FAIL"}:
        raise ValueError("source candidate status must be PASS or FAIL")
    if status != "PASS":
        raise ValueError("source candidate status must be PASS for publication authority request")
    if _required_string(candidate.get("beo_publication"), "beo_publication") != DRAFT_ONLY:
        raise ValueError("beo_publication must remain DRAFT_ONLY")
    if _required_string(candidate.get("rtm_status"), "rtm_status") != NOT_GENERATED:
        raise ValueError("rtm_status must remain NOT_GENERATED")
    for flag in [
        "published",
        "active_vault_read",
        "key_material_accessed",
        "immutable_storage_written",
        "public_ledger_mutated",
        "rollback_executed",
    ]:
        _required_false(candidate.get(flag), flag)
    evidence = _require_dict(candidate.get("source_evidence"), "source_evidence")
    _enforce_allowed_keys(evidence, _SOURCE_EVIDENCE_KEYS, "source_evidence")
    if _required_string(evidence.get("cleanup_status"), "cleanup_status") != "CLEANED":
        raise ValueError("cleanup_status must be CLEANED")
    trace_artifacts = _validate_trace_artifacts(candidate.get("trace_artifacts"))
    _scan_nested(
        {
            key: value
            for key, value in candidate.items()
            if key not in {"candidate_status", "beo_publication", "rtm_status", "status"}
        },
        "source_candidate",
    )
    return {
        "candidate_id": _required_string(candidate.get("candidate_id"), "candidate_id"),
        "beo_id": _required_string(candidate.get("beo_id"), "beo_id"),
        "beo_hash": _required_hash(candidate.get("beo_hash"), "beo_hash"),
        "beb_id": _required_string(candidate.get("beb_id"), "beb_id"),
        "source_evidence_hash": _required_hash(evidence.get("source_evidence_hash"), "source_evidence_hash"),
        "trace_artifacts": trace_artifacts,
    }


def _validate_approval_request(
    approval: dict[str, Any],
    *,
    expected_candidate_id: str,
    expected_beo_id: str,
    expected_beo_hash: str,
    expected_source_evidence_hash: str,
) -> dict[str, Any]:
    _require_dict(approval, "approval_request")
    _reject_forbidden_fields(approval, "approval_request")
    _enforce_allowed_keys(approval, _APPROVAL_REQUEST_KEYS, "approval_request")
    if _required_string(approval.get("approval_scope"), "approval_scope") != APPROVAL_SCOPE:
        raise ValueError("approval_scope must be AUTHORITATIVE_BEO_PUBLICATION_AUTHORITY_REQUEST_ONLY")
    if _required_string(approval.get("approved_candidate_id"), "approved_candidate_id") != expected_candidate_id:
        raise ValueError("approved_candidate_id does not match source candidate")
    if _required_string(approval.get("approved_beo_id"), "approved_beo_id") != expected_beo_id:
        raise ValueError("approved_beo_id does not match source candidate")
    if _required_hash(approval.get("approved_beo_hash"), "approved_beo_hash") != expected_beo_hash:
        raise ValueError("approved_beo_hash does not match source candidate")
    if _required_hash(approval.get("source_evidence_hash"), "source_evidence_hash") != expected_source_evidence_hash:
        raise ValueError("source_evidence_hash does not match source candidate")
    excluded = approval.get("excluded_authorities")
    if (
        not isinstance(excluded, list)
        or not all(isinstance(item, str) for item in excluded)
        or set(excluded) != EXACT_EXCLUDED_AUTHORITIES
        or len(excluded) != len(EXACT_EXCLUDED_AUTHORITIES)
    ):
        raise ValueError("excluded_authorities must match exact denied authority set")
    for flag in ["expired", "replayed", "stale"]:
        if _required_bool(approval.get(flag), flag) is True:
            raise ValueError(f"approval_request must not be {flag}")
    _scan_nested({key: value for key, value in approval.items() if key not in {"excluded_authorities", "approval_scope"}}, "approval_request")
    return {
        "request_id": _required_string(approval.get("request_id"), "request_id"),
        "operator_identity": _required_string(approval.get("operator_identity"), "operator_identity"),
        "request_hash": _required_hash(approval.get("request_hash"), "request_hash"),
    }


def _validate_signer_policy(signer: dict[str, Any]) -> dict[str, Any]:
    _require_dict(signer, "signer_policy")
    _reject_secret_fields(signer, "signer_policy")
    _scan_nested(signer, "signer_policy")
    _enforce_allowed_keys(signer, _SIGNER_POLICY_KEYS, "signer_policy")
    return {
        "signer_identity": _required_string(signer.get("signer_identity"), "signer_identity"),
        "signer_policy_hash": _required_hash(signer.get("signer_policy_hash"), "signer_policy_hash"),
        "key_material_accessed": _required_false(signer.get("key_material_accessed"), "key_material_accessed"),
        "signature_generated": _required_false(signer.get("signature_generated"), "signature_generated"),
        "secret_read": _required_false(signer.get("secret_read"), "secret_read"),
    }


def _validate_storage_policy(storage: dict[str, Any]) -> dict[str, Any]:
    _require_dict(storage, "storage_policy")
    _scan_nested(storage, "storage_policy")
    _enforce_allowed_keys(storage, _STORAGE_POLICY_KEYS, "storage_policy")
    return {
        "storage_target_identity": _required_string(storage.get("storage_target_identity"), "storage_target_identity"),
        "storage_policy_hash": _required_hash(storage.get("storage_policy_hash"), "storage_policy_hash"),
        "immutable_storage_written": _required_false(storage.get("immutable_storage_written"), "immutable_storage_written"),
        "storage_write_attempted": _required_false(storage.get("storage_write_attempted"), "storage_write_attempted"),
    }


def _validate_ledger_policy(ledger: dict[str, Any]) -> dict[str, Any]:
    _require_dict(ledger, "ledger_policy")
    _scan_nested(ledger, "ledger_policy")
    _enforce_allowed_keys(ledger, _LEDGER_POLICY_KEYS, "ledger_policy")
    return {
        "ledger_target_identity": _required_string(ledger.get("ledger_target_identity"), "ledger_target_identity"),
        "ledger_policy_hash": _required_hash(ledger.get("ledger_policy_hash"), "ledger_policy_hash"),
        "public_ledger_mutated": _required_false(ledger.get("public_ledger_mutated"), "public_ledger_mutated"),
        "ledger_append_attempted": _required_false(ledger.get("ledger_append_attempted"), "ledger_append_attempted"),
    }


def _validate_rollback_policy(rollback: dict[str, Any]) -> dict[str, Any]:
    _require_dict(rollback, "rollback_policy")
    _scan_nested(rollback, "rollback_policy")
    _enforce_allowed_keys(rollback, _ROLLBACK_POLICY_KEYS, "rollback_policy")
    return {
        "rollback_fixture_identity": _required_string(rollback.get("rollback_fixture_identity"), "rollback_fixture_identity"),
        "rollback_policy_hash": _required_hash(rollback.get("rollback_policy_hash"), "rollback_policy_hash"),
        "rollback_executed": _required_false(rollback.get("rollback_executed"), "rollback_executed"),
        "revocation_executed": _required_false(rollback.get("revocation_executed"), "revocation_executed"),
        "supersession_executed": _required_false(rollback.get("supersession_executed"), "supersession_executed"),
    }


def _validate_trace_artifacts(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list) or not value:
        raise ValueError("trace_artifacts must be a non-empty list")
    result: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for item in value:
        artifact = _require_dict(item, "trace_artifact")
        _enforce_allowed_keys(artifact, _TRACE_ARTIFACT_KEYS, "trace_artifact")
        kind = _required_string(artifact.get("kind"), "kind")
        artifact_id = _required_string(artifact.get("id"), "id")
        version_hash = _required_hash(artifact.get("version_hash"), "version_hash")
        key = (kind, artifact_id)
        if key in seen:
            raise ValueError("duplicate trace artifact identity")
        seen.add(key)
        result.append({"kind": kind, "id": artifact_id, "version_hash": version_hash})
    return result


def _reject_forbidden_fields(value: dict[str, Any], label: str) -> None:
    forbidden = sorted((_PUBLICATION_AUTHORITY_FIELDS | _RTM_AUTHORITY_FIELDS).intersection(value))
    if forbidden:
        raise ValueError(f"{label} rejects forbidden authority field: {forbidden[0]}")


def _reject_secret_fields(value: dict[str, Any], label: str) -> None:
    forbidden = sorted(_SECRET_KEYS.intersection(value))
    if forbidden:
        raise ValueError(f"{label} rejects secret-bearing field: {forbidden[0]}")


def _enforce_allowed_keys(value: dict[str, Any], allowed: set[str], label: str) -> None:
    unexpected = sorted(set(value) - allowed)
    if unexpected:
        raise ValueError(f"{label} rejects unexpected field: {unexpected[0]}")


def _scan_nested(value: Any, label: str) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key)
            key_norm = _normalize_text(key_text)
            key_compact = _compact_text(key_text)
            if key_text in _SIDE_EFFECT_FIELDS:
                if item is not False:
                    raise ValueError(f"{key_text} must be false")
                continue
            if (
                key_text in _SECRET_KEYS
                or "private key" in key_norm
                or "key material" in key_norm
                or "secret" in key_norm
                or _contains_secret_key_compact(key_compact)
            ):
                raise ValueError(f"{label} rejects secret-bearing field: {key_text}")
            if (
                key_text in _PUBLICATION_AUTHORITY_FIELDS
                or key_text in _RTM_AUTHORITY_FIELDS
                or _contains_forbidden_authority_key(key_norm, key_compact)
            ):
                raise ValueError(f"{label} rejects forbidden authority field: {key_text}")
            _scan_nested(item, label)
    elif isinstance(value, list):
        for item in value:
            _scan_nested(item, label)
    elif isinstance(value, str):
        if _PROTECTED_BODY_RE.search(value) or _contains_protected_body_reference(value):
            raise ValueError(f"{label} rejects protected BLK-req body reference")
        if _FORBIDDEN_TEXT_RE.search(value) or _contains_forbidden_text(value):
            raise ValueError(f"{label} rejects authority-laundering text")


def _normalize_text(value: str) -> str:
    spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", value)
    spaced = re.sub(r"[^A-Za-z0-9]+", " ", spaced)
    return " ".join(spaced.lower().split())


def _compact_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def _contains_secret_key_compact(compact: str) -> bool:
    secret_tokens = [
        "privatekey",
        "keymaterial",
        "signerkeymaterial",
        "apikey",
        "secret",
        "token",
        "password",
        "passphrase",
    ]
    return any(token in compact for token in secret_tokens)


def _contains_protected_body_reference(value: str) -> bool:
    decoded = value.lower()
    for _ in range(3):
        decoded = unquote(decoded)
    normalized = decoded.replace("\\", "/")
    normalized = re.sub(r"^[a-z]+://", "", normalized)
    normalized = re.sub(r"[?#=&]+", "/", normalized)
    normalized = re.sub(r"/+", "/", normalized.strip())
    while normalized.startswith("./") or normalized.startswith("../"):
        normalized = normalized.split("/", 1)[1]
    protected_prefixes = ("docs/active", "docs/requirements", "docs/use_cases")
    return any(
        normalized == prefix
        or normalized.startswith(prefix + "/")
        or f"/{prefix}" in normalized
        for prefix in protected_prefixes
    )


def _contains_forbidden_authority_key(normalized: str, compact: str) -> bool:
    authority_key_phrases = [
        "publication authority",
        "beo publication authority",
        "runtime published beo output",
        "rtm generation",
        "drift decision",
        "drift rejection",
        "coverage matrix",
        "coverage claim",
        "public ledger mutation",
        "immutable storage write",
        "rollback execution",
        "revocation execution",
        "supersession execution",
        "live publication approval",
        "active vault hash comparison",
        "signature generated",
        "cryptographic signing",
        "rtm id",
        "rtm status",
        "rtm generated",
    ]
    authority_key_tokens = [
        "published",
        "authoritativebeopublication",
        "authoritative_beo_publication",
        "beopubapproved",
        "beopubauth",
        "abpapproved",
        "rtpbeo",
        "publishbeo",
        "approvalinherited",
        "inheritedapproval",
        "reusedapproval",
        "codexapproval",
        "blkpipesuccess",
        "blktestpassapproval",
        "publishedat",
        "publishedbeooutput",
        "beopublicationapproved",
        "publicationperformed",
        "publicledgermutated",
        "immutablestoragewritten",
        "storagewriteattempted",
        "ledgerappendattempted",
        "rollbackexecuted",
        "revocationexecuted",
        "supersessionexecuted",
        "publicationauthority",
        "beopublicationauthority",
        "runtimepublishedbeooutput",
        "rtmgeneration",
        "rtmgenerated",
        "rtmid",
        "rtmstatus",
        "activaulthashcomparison",
        "activevaulthashcomparison",
        "signaturegenerated",
        "signature",
        "cryptographicsigning",
        "driftdecision",
        "driftrejection",
        "coveragematrix",
        "coverageclaim",
        "publicledgermutation",
        "immutablestoragewrite",
        "rollbackexecution",
        "revocationexecution",
        "supersessionexecution",
    ]
    return any(phrase in normalized for phrase in authority_key_phrases) or any(
        token in compact for token in authority_key_tokens
    )


def _contains_forbidden_text(value: str) -> bool:
    normalized = _normalize_text(value)
    compact = _compact_text(value)
    forbidden_phrases = [
        "authoritative beo publication",
        "beo publication approved",
        "publish beo",
        "published beo",
        "beo publication authorized",
        "beo publication authorization",
        "beo publication authorised",
        "beo publication authorisation",
        "publication authority granted",
        "approved for publication",
        "beo publication greenlit",
        "beo publication allowed",
        "publication approval granted",
        "beo publication permitted",
        "beo pub approved",
        "beo pub auth",
        "auth beo pub approved",
        "abp approved",
        "rtpbeo output",
        "runtime published beo",
        "rtm generation",
        "rtm generated",
        "rtm id",
        "rtm status",
        "active vault hash comparison",
        "signature generated",
        "cryptographic signing",
        "drift rejection",
        "drift decision",
        "coverage matrix",
        "coverage claim",
        "public ledger mutation",
        "signer key material",
        "immutable storage write",
        "rollback execute",
        "rollback execution",
        "blk test pass approval",
        "blk pipe success",
        "codex approval",
        "publication candidate fixture",
        "published input fixture",
        "approval inherited",
        "inherit approval",
        "inherited approval",
        "reused as approval",
        "reused approval",
    ]
    forbidden_tokens = [
        "beopublicationauthorized",
        "beopublicationauthorization",
        "beopublicationauthorised",
        "beopublicationauthorisation",
        "publicationauthoritygranted",
        "approvedforpublication",
        "beopublicationgreenlit",
        "beopublicationallowed",
        "publicationapprovalgranted",
        "beopublicationpermitted",
        "beopubapproved",
        "beopubauth",
        "abpapproved",
        "rtpbeo",
        "publicledgermutated",
        "immutablestoragewritten",
        "storagewriteattempted",
        "ledgerappendattempted",
        "rollbackexecuted",
        "revocationexecuted",
        "supersessionexecuted",
        "authoritativebeopublication",
        "beopublicationapproved",
        "publishbeo",
        "publishedbeo",
        "runtimepublishedbeo",
        "rtmgeneration",
        "rtmgenerated",
        "rtmid",
        "rtmstatus",
        "activevaulthashcomparison",
        "signaturegenerated",
        "cryptographicsigning",
        "driftrejection",
        "driftdecision",
        "coveragematrix",
        "coverageclaim",
        "publicledgermutation",
        "signerkeymaterial",
        "immutablestoragewrite",
        "rollbackexecute",
        "rollbackexecution",
        "blktestpassapproval",
        "blkpipesuccess",
        "codexapproval",
        "publicationcandidatefixture",
        "publishedinputfixture",
        "inheritapproval",
        "inheritedapproval",
        "reusedasapproval",
        "reusedapproval",
    ]
    return (
        normalized == "published"
        or any(phrase in normalized for phrase in forbidden_phrases)
        or any(token in compact for token in forbidden_tokens)
    )


def _require_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a dictionary")
    return value


def _required_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value


def _required_hash(value: Any, label: str) -> str:
    text = _required_string(value, label)
    if not HASH_RE.match(text):
        raise ValueError(f"{label} must be a sha256 hash")
    return text


def _required_bool(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{label} must be boolean")
    return value


def _required_false(value: Any, label: str) -> bool:
    if _required_bool(value, label) is not False:
        raise ValueError(f"{label} must be false")
    return False


def _canonical_hash(value: Any) -> str:
    stable = json.dumps(deepcopy(value), sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(stable).hexdigest()
