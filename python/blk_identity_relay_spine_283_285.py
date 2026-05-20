"""BLK-SYSTEM-283..285 identity/relay provenance spine packages.

These builders are deterministic, local, and non-runtime. They create hash-bound
records that can be consumed by later HITL / BLK-003 work without granting
approval, dispatch, runtime, publication, RTM, protected-body, or mutation
authority.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import hashlib
import json
import re
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering
import blk_root_doctrine_gap_ladder_237_241 as root_ladder


class IdentityRelayValidationError(ValueError):
    """Raised when identity/relay evidence fails closed."""


_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_ID_RE = re.compile(r"^[A-Z]+(?:-[A-Z0-9]+)+$")
_ALLOWED_METADATA_KEYS = frozenset({"display_name", "external_ref", "summary", "version", "purpose"})
_ALLOWED_RECORD_KINDS = ("actor", "artifact", "approval", "run", "source_system")
_RECORD_PREFIXES = {
    "actor": "ACTOR-",
    "artifact": "ARTIFACT-",
    "approval": "APPROVAL-",
    "run": "RUN-",
    "source_system": "SOURCE-",
}
_ALLOWED_MESSAGE_TYPES = (
    "HITL_APPROVAL_SIGNAL",
    "BEB_PACKET_SIGNAL",
    "BEO_DRAFT_SIGNAL",
    "STATUS_SIGNAL",
    "RTM_TRACE_SIGNAL",
)
_ALLOWED_TARGET_COMPONENTS = (
    "hermes",
    "operator",
    "blk-id",
    "blk-relay",
    "blk-req",
    "blk-pipe",
    "blk-test",
    "blk-link",
    "codex",
)

_IDENTITY_CONTRACT_SIDE_EFFECTS = {
    "approval_authority_granted": False,
    "runtime_authority_granted": False,
    "network_runtime_created": False,
    "relay_runtime_created": False,
    "source_git_mutation": False,
    "protected_body_access": False,
    "beo_publication_authority": False,
    "rtm_generation_authority": False,
}
_IDENTITY_RECORD_SIDE_EFFECTS = {
    "approval_authority_granted": False,
    "runtime_authority_granted": False,
    "source_git_mutation": False,
    "protected_body_access": False,
    "beo_publication_authority": False,
    "rtm_generation_authority": False,
}
_RELAY_CONTRACT_SIDE_EFFECTS = {
    "network_runtime_created": False,
    "message_dispatch_authorized": False,
    "approval_authority_granted": False,
    "runtime_tooling": False,
    "source_git_mutation": False,
    "protected_body_access": False,
    "beo_publication_authority": False,
    "rtm_generation_authority": False,
}
_RELAY_ENVELOPE_SIDE_EFFECTS = dict(_RELAY_CONTRACT_SIDE_EFFECTS)
_LOOP_EVIDENCE_SIDE_EFFECTS = {
    "loop_runtime_execution": False,
    "approval_authority_granted": False,
    "message_dispatch_authorized": False,
    "network_runtime_created": False,
    "source_git_mutation": False,
    "protected_body_access": False,
    "beo_closeout_execution": False,
    "beo_publication_authority": False,
    "rtm_generation_authority": False,
    "production_blk_link_authority": False,
    "production_blk_test_mcp": False,
}

_IDENTITY_CONTRACT_KEYS = frozenset(
    {
        "status",
        "markers",
        "record_kinds",
        "record_id_prefixes",
        "required_fields",
        "timestamp_policy",
        "hash_policy",
        "metadata_keys",
        "side_effects",
        "identity_contract_hash",
    }
)
_IDENTITY_RECORD_KEYS = frozenset(
    {
        "status",
        "markers",
        "contract_hash",
        "record_kind",
        "record_id",
        "source_system_id",
        "subject_hash",
        "created_at",
        "metadata",
        "side_effects",
        "identity_hash",
    }
)
_RELAY_CONTRACT_KEYS = frozenset(
    {
        "status",
        "markers",
        "identity_contract_hash",
        "message_types",
        "target_components",
        "required_fields",
        "hash_policy",
        "side_effects",
        "relay_contract_hash",
    }
)
_RELAY_ENVELOPE_KEYS = frozenset(
    {
        "status",
        "markers",
        "relay_contract_hash",
        "identity_contract_hash",
        "envelope_id",
        "message_type",
        "target_component",
        "source_identity_hash",
        "payload_hash",
        "created_at",
        "trace_identity_hashes",
        "metadata",
        "side_effects",
        "relay_hash",
    }
)
_LOOP_EVIDENCE_KEYS = frozenset(
    {
        "status",
        "markers",
        "identity_contract_hash",
        "relay_contract_hash",
        "loop_kernel_hash",
        "identity_record_sample_hash",
        "relay_envelope_sample_hash",
        "loop_binding",
        "side_effects",
        "loop_evidence_hash",
    }
)


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def hash_package(package: dict[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json(package).encode("utf-8")).hexdigest()


def _without_hash(package: dict[str, Any], key: str) -> dict[str, Any]:
    return {k: deepcopy(v) for k, v in package.items() if k != key}


def _deepcopy(value: Any) -> Any:
    return deepcopy(value)


def _require_dict(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise IdentityRelayValidationError(f"{context} must be a dictionary")
    return value


def _require_allowed_keys(package: dict[str, Any], allowed: frozenset[str], context: str) -> None:
    _require_dict(package, context)
    extras = sorted(set(package) - allowed)
    if extras:
        raise IdentityRelayValidationError(f"{context} unsupported field(s): {', '.join(extras)}")
    missing = sorted(allowed - set(package))
    if missing:
        raise IdentityRelayValidationError(f"{context} missing field(s): {', '.join(missing)}")


def _require_hash(value: Any, context: str) -> None:
    if not isinstance(value, str) or not _HASH_RE.match(value):
        raise IdentityRelayValidationError(f"{context} must be sha256:<64 hex>")


def _require_hash_field(package: dict[str, Any], field: str, context: str) -> None:
    _require_hash(package.get(field), f"{context}.{field}")
    expected = hash_package(_without_hash(package, field))
    if package[field] != expected:
        raise IdentityRelayValidationError(f"{context} hash mismatch for {field}")


def _require_exact_side_effects(package: dict[str, Any], expected: dict[str, bool], context: str) -> None:
    side_effects = package.get("side_effects")
    if side_effects != expected:
        raise IdentityRelayValidationError(f"{context} side_effects mismatch")


def _reject_laundering(value: Any, context: str) -> None:
    errors = scan_for_authority_laundering(value, context)
    if errors:
        raise IdentityRelayValidationError(f"{context} forbidden authority wording: {'; '.join(errors[:4])}")


def _require_ascii(text: str, context: str) -> None:
    if not isinstance(text, str) or any(ord(ch) > 127 for ch in text):
        raise IdentityRelayValidationError(f"{context} must contain ASCII characters only")


def _require_exact_id(text: str, prefix: str, context: str) -> None:
    _require_ascii(text, context)
    if not text.startswith(prefix) or not _ID_RE.match(text):
        raise IdentityRelayValidationError(f"{context} must be an exact ASCII ID with prefix {prefix}")


def _require_timestamp(value: Any, context: str) -> None:
    if not isinstance(value, str):
        raise IdentityRelayValidationError(f"{context} must be a timestamp string")
    candidate = value.replace("Z", "+00:00") if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise IdentityRelayValidationError(f"{context} must be ISO-8601") from exc
    if parsed.tzinfo is None:
        raise IdentityRelayValidationError(f"{context} must be timezone-aware")


def _validate_metadata(metadata: Any, context: str) -> dict[str, str]:
    if metadata is None:
        return {}
    if not isinstance(metadata, dict):
        raise IdentityRelayValidationError(f"{context} metadata must be a dictionary")
    extras = sorted(set(metadata) - _ALLOWED_METADATA_KEYS)
    if extras:
        raise IdentityRelayValidationError(f"{context} metadata unsupported field(s): {', '.join(extras)}")
    for key, value in metadata.items():
        _require_ascii(str(key), f"{context}.metadata key")
        if not isinstance(value, str):
            raise IdentityRelayValidationError(f"{context}.metadata.{key} must be a string")
        _require_ascii(value, f"{context}.metadata.{key}")
        if len(value) > 240:
            raise IdentityRelayValidationError(f"{context}.metadata.{key} too large")
    _reject_laundering(metadata, f"{context}.metadata")
    return dict(metadata)


def _validate_identity_contract(package: dict[str, Any]) -> dict[str, Any]:
    _require_allowed_keys(package, _IDENTITY_CONTRACT_KEYS, "identity contract")
    if package.get("status") != "BLK_IDENTITY_SPINE_CONTRACT_READY":
        raise IdentityRelayValidationError("identity contract status mismatch")
    if "BLK_SYSTEM_283_BLK_IDENTITY_SPINE_CONTRACT_READY" not in package.get("markers", []):
        raise IdentityRelayValidationError("identity contract marker missing")
    if tuple(package.get("record_kinds", [])) != _ALLOWED_RECORD_KINDS:
        raise IdentityRelayValidationError("identity contract record_kinds mismatch")
    if package.get("record_id_prefixes") != _RECORD_PREFIXES:
        raise IdentityRelayValidationError("identity contract record_id_prefixes mismatch")
    if set(package.get("metadata_keys", [])) != set(_ALLOWED_METADATA_KEYS):
        raise IdentityRelayValidationError("identity contract metadata_keys mismatch")
    _require_exact_side_effects(package, _IDENTITY_CONTRACT_SIDE_EFFECTS, "identity contract")
    _require_hash_field(package, "identity_contract_hash", "identity contract")
    _reject_laundering(package, "identity contract")
    return _deepcopy(package)


def build_blk_id_identity_spine_contract_283() -> dict[str, Any]:
    package = {
        "status": "BLK_IDENTITY_SPINE_CONTRACT_READY",
        "markers": [
            "BLK_SYSTEM_283_BLK_IDENTITY_SPINE_CONTRACT_READY",
            "ASCII_EXACT_IDENTITY_RECORDS_READY",
            "NO_APPROVAL_RUNTIME_OR_MUTATION_AUTHORITY",
        ],
        "record_kinds": list(_ALLOWED_RECORD_KINDS),
        "record_id_prefixes": dict(_RECORD_PREFIXES),
        "required_fields": [
            "record_kind",
            "record_id",
            "source_system_id",
            "subject_hash",
            "created_at",
            "metadata",
        ],
        "timestamp_policy": "timezone_aware_iso8601_required",
        "hash_policy": "canonical_json_sort_keys_sha256_excluding_hash_field",
        "metadata_keys": sorted(_ALLOWED_METADATA_KEYS),
        "side_effects": dict(_IDENTITY_CONTRACT_SIDE_EFFECTS),
    }
    package["identity_contract_hash"] = hash_package(package)
    return _validate_identity_contract(package)


def build_identity_record_283(
    identity_contract: dict[str, Any],
    *,
    record_kind: str,
    record_id: str,
    source_system_id: str,
    subject_hash: str,
    created_at: str,
    metadata: dict[str, str] | None = None,
) -> dict[str, Any]:
    contract = _validate_identity_contract(identity_contract)
    if record_kind not in _RECORD_PREFIXES:
        raise IdentityRelayValidationError("identity record record_kind unsupported")
    _require_exact_id(record_id, _RECORD_PREFIXES[record_kind], "identity record record_id")
    _require_exact_id(source_system_id, "SOURCE-", "identity record source_system_id")
    _require_hash(subject_hash, "identity record subject_hash")
    _require_timestamp(created_at, "identity record created_at")
    metadata_value = _validate_metadata(metadata or {}, "identity record")
    package = {
        "status": "BLK_IDENTITY_RECORD_BOUND",
        "markers": [
            "BLK_IDENTITY_RECORD_CANONICAL_HASH_BOUND",
            "NO_APPROVAL_RUNTIME_OR_MUTATION_AUTHORITY",
        ],
        "contract_hash": contract["identity_contract_hash"],
        "record_kind": record_kind,
        "record_id": record_id,
        "source_system_id": source_system_id,
        "subject_hash": subject_hash,
        "created_at": created_at,
        "metadata": metadata_value,
        "side_effects": dict(_IDENTITY_RECORD_SIDE_EFFECTS),
    }
    package["identity_hash"] = hash_package(package)
    return validate_identity_record_283(package, contract)


def _validate_identity_record_against_hash(record: dict[str, Any], contract_hash: str, context: str) -> None:
    _require_allowed_keys(record, _IDENTITY_RECORD_KEYS, context)
    if record.get("status") != "BLK_IDENTITY_RECORD_BOUND":
        raise IdentityRelayValidationError(f"{context} status mismatch")
    if "BLK_IDENTITY_RECORD_CANONICAL_HASH_BOUND" not in record.get("markers", []):
        raise IdentityRelayValidationError(f"{context} marker missing")
    if record.get("contract_hash") != contract_hash:
        raise IdentityRelayValidationError(f"{context} contract_hash mismatch")
    record_kind = record.get("record_kind")
    if not isinstance(record_kind, str) or record_kind not in _RECORD_PREFIXES:
        raise IdentityRelayValidationError(f"{context} record_kind unsupported")
    record_id = record.get("record_id")
    source_system_id = record.get("source_system_id")
    if not isinstance(record_id, str):
        raise IdentityRelayValidationError(f"{context} record_id must be a string")
    if not isinstance(source_system_id, str):
        raise IdentityRelayValidationError(f"{context} source_system_id must be a string")
    _require_exact_id(record_id, _RECORD_PREFIXES[record_kind], f"{context} record_id")
    _require_exact_id(source_system_id, "SOURCE-", f"{context} source_system_id")
    _require_hash(record.get("subject_hash"), f"{context} subject_hash")
    _require_timestamp(record.get("created_at"), f"{context} created_at")
    _validate_metadata(record.get("metadata"), context)
    _require_exact_side_effects(record, _IDENTITY_RECORD_SIDE_EFFECTS, context)
    _require_hash_field(record, "identity_hash", context)
    _reject_laundering(record, context)


def validate_identity_record_283(record: dict[str, Any], identity_contract: dict[str, Any]) -> dict[str, Any]:
    contract = _validate_identity_contract(identity_contract)
    _validate_identity_record_against_hash(record, contract["identity_contract_hash"], "identity record")
    return _deepcopy(record)


def _validate_relay_contract(package: dict[str, Any], identity_contract: dict[str, Any] | None = None) -> dict[str, Any]:
    _require_allowed_keys(package, _RELAY_CONTRACT_KEYS, "relay contract")
    if package.get("status") != "BLK_RELAY_ENVELOPE_CONTRACT_READY":
        raise IdentityRelayValidationError("relay contract status mismatch")
    if "BLK_SYSTEM_284_BLK_RELAY_ENVELOPE_CONTRACT_READY" not in package.get("markers", []):
        raise IdentityRelayValidationError("relay contract marker missing")
    if tuple(package.get("message_types", [])) != _ALLOWED_MESSAGE_TYPES:
        raise IdentityRelayValidationError("relay contract message_types mismatch")
    if tuple(package.get("target_components", [])) != _ALLOWED_TARGET_COMPONENTS:
        raise IdentityRelayValidationError("relay contract target_components mismatch")
    if identity_contract is not None:
        contract = _validate_identity_contract(identity_contract)
        if package.get("identity_contract_hash") != contract["identity_contract_hash"]:
            raise IdentityRelayValidationError("relay contract identity_contract_hash mismatch")
    else:
        _require_hash(package.get("identity_contract_hash"), "relay contract identity_contract_hash")
    _require_exact_side_effects(package, _RELAY_CONTRACT_SIDE_EFFECTS, "relay contract")
    _require_hash_field(package, "relay_contract_hash", "relay contract")
    _reject_laundering(package, "relay contract")
    return _deepcopy(package)


def build_blk_relay_envelope_contract_284(identity_contract: dict[str, Any]) -> dict[str, Any]:
    contract = _validate_identity_contract(identity_contract)
    package = {
        "status": "BLK_RELAY_ENVELOPE_CONTRACT_READY",
        "markers": [
            "BLK_SYSTEM_284_BLK_RELAY_ENVELOPE_CONTRACT_READY",
            "TYPED_SIGNAL_ENVELOPE_CONTRACT_READY",
            "NO_MESSAGE_DISPATCH_OR_NETWORK_RUNTIME_AUTHORITY",
        ],
        "identity_contract_hash": contract["identity_contract_hash"],
        "message_types": list(_ALLOWED_MESSAGE_TYPES),
        "target_components": list(_ALLOWED_TARGET_COMPONENTS),
        "required_fields": [
            "envelope_id",
            "message_type",
            "target_component",
            "source_identity_hash",
            "payload_hash",
            "created_at",
            "trace_identity_hashes",
        ],
        "hash_policy": "canonical_json_sort_keys_sha256_excluding_hash_field",
        "side_effects": dict(_RELAY_CONTRACT_SIDE_EFFECTS),
    }
    package["relay_contract_hash"] = hash_package(package)
    return _validate_relay_contract(package, contract)


def build_relay_envelope_284(
    relay_contract: dict[str, Any],
    *,
    source_identity_record: dict[str, Any],
    envelope_id: str,
    message_type: str,
    target_component: str,
    payload_hash: str,
    created_at: str,
    trace_identity_hashes: list[str] | None = None,
    metadata: dict[str, str] | None = None,
) -> dict[str, Any]:
    contract = _validate_relay_contract(relay_contract)
    _validate_identity_record_against_hash(
        source_identity_record,
        contract["identity_contract_hash"],
        "identity record",
    )
    _require_exact_id(envelope_id, "RELAY-", "relay envelope envelope_id")
    if message_type not in _ALLOWED_MESSAGE_TYPES:
        raise IdentityRelayValidationError("relay envelope message_type unsupported")
    if target_component not in _ALLOWED_TARGET_COMPONENTS:
        raise IdentityRelayValidationError("relay envelope target_component unsupported")
    _require_hash(payload_hash, "relay envelope payload_hash")
    _require_timestamp(created_at, "relay envelope created_at")
    trace_hashes = list(trace_identity_hashes or [source_identity_record["identity_hash"]])
    if not trace_hashes:
        raise IdentityRelayValidationError("relay envelope trace_identity_hashes must not be empty")
    for value in trace_hashes:
        _require_hash(value, "relay envelope trace_identity_hashes item")
    if source_identity_record["identity_hash"] not in trace_hashes:
        raise IdentityRelayValidationError("relay envelope must trace source identity hash")
    metadata_value = _validate_metadata(metadata or {}, "relay envelope")
    package = {
        "status": "BLK_RELAY_ENVELOPE_BOUND",
        "markers": [
            "BLK_RELAY_TYPED_SIGNAL_HASH_BOUND",
            "NO_MESSAGE_DISPATCH_OR_NETWORK_RUNTIME_AUTHORITY",
        ],
        "relay_contract_hash": contract["relay_contract_hash"],
        "identity_contract_hash": contract["identity_contract_hash"],
        "envelope_id": envelope_id,
        "message_type": message_type,
        "target_component": target_component,
        "source_identity_hash": source_identity_record["identity_hash"],
        "payload_hash": payload_hash,
        "created_at": created_at,
        "trace_identity_hashes": trace_hashes,
        "metadata": metadata_value,
        "side_effects": dict(_RELAY_ENVELOPE_SIDE_EFFECTS),
    }
    package["relay_hash"] = hash_package(package)
    return validate_relay_envelope_284(package, contract, source_identity_record)


def validate_relay_envelope_284(
    envelope: dict[str, Any],
    relay_contract: dict[str, Any],
    source_identity_record: dict[str, Any],
) -> dict[str, Any]:
    contract = _validate_relay_contract(relay_contract)
    _validate_identity_record_against_hash(source_identity_record, contract["identity_contract_hash"], "identity record")
    _require_allowed_keys(envelope, _RELAY_ENVELOPE_KEYS, "relay envelope")
    if envelope.get("status") != "BLK_RELAY_ENVELOPE_BOUND":
        raise IdentityRelayValidationError("relay envelope status mismatch")
    if "BLK_RELAY_TYPED_SIGNAL_HASH_BOUND" not in envelope.get("markers", []):
        raise IdentityRelayValidationError("relay envelope marker missing")
    if envelope.get("relay_contract_hash") != contract["relay_contract_hash"]:
        raise IdentityRelayValidationError("relay envelope relay_contract_hash mismatch")
    if envelope.get("identity_contract_hash") != contract["identity_contract_hash"]:
        raise IdentityRelayValidationError("relay envelope identity_contract_hash mismatch")
    envelope_id = envelope.get("envelope_id")
    if not isinstance(envelope_id, str):
        raise IdentityRelayValidationError("relay envelope envelope_id must be a string")
    _require_exact_id(envelope_id, "RELAY-", "relay envelope envelope_id")
    if envelope.get("message_type") not in _ALLOWED_MESSAGE_TYPES:
        raise IdentityRelayValidationError("relay envelope message_type unsupported")
    if envelope.get("target_component") not in _ALLOWED_TARGET_COMPONENTS:
        raise IdentityRelayValidationError("relay envelope target_component unsupported")
    if envelope.get("source_identity_hash") != source_identity_record["identity_hash"]:
        raise IdentityRelayValidationError("relay envelope source_identity_hash mismatch")
    _require_hash(envelope.get("payload_hash"), "relay envelope payload_hash")
    _require_timestamp(envelope.get("created_at"), "relay envelope created_at")
    trace_hashes = envelope.get("trace_identity_hashes")
    if not isinstance(trace_hashes, list) or not trace_hashes:
        raise IdentityRelayValidationError("relay envelope trace_identity_hashes must be a non-empty list")
    for value in trace_hashes:
        _require_hash(value, "relay envelope trace_identity_hashes item")
    if source_identity_record["identity_hash"] not in trace_hashes:
        raise IdentityRelayValidationError("relay envelope must trace source identity hash")
    _validate_metadata(envelope.get("metadata"), "relay envelope")
    _require_exact_side_effects(envelope, _RELAY_ENVELOPE_SIDE_EFFECTS, "relay envelope")
    _require_hash_field(envelope, "relay_hash", "relay envelope")
    _reject_laundering(envelope, "relay envelope")
    return _deepcopy(envelope)


def _validate_loop_kernel_241(loop_kernel: dict[str, Any]) -> dict[str, Any]:
    try:
        root_ladder._validate_241_loop(loop_kernel)
    except Exception as exc:  # noqa: BLE001 - translate upstream validation to this package's error type.
        raise IdentityRelayValidationError(f"loop package invalid: {exc}") from exc
    if loop_kernel["side_effects"].get("loop_runtime_execution") is not False:
        raise IdentityRelayValidationError("loop package side_effects.loop_runtime_execution must remain false")
    return _deepcopy(loop_kernel)


def build_identity_relay_loop_evidence_285(
    identity_contract: dict[str, Any],
    relay_contract: dict[str, Any],
    loop_kernel: dict[str, Any],
) -> dict[str, Any]:
    identity = _validate_identity_contract(identity_contract)
    relay = _validate_relay_contract(relay_contract, identity)
    loop = _validate_loop_kernel_241(loop_kernel)
    sample_identity = build_identity_record_283(
        identity,
        record_kind="run",
        record_id="RUN-BLK-SYSTEM-285-LOOP-EVIDENCE",
        source_system_id="SOURCE-LOCAL",
        subject_hash=loop["loop_kernel_hash"],
        created_at="2026-05-20T20:02:00Z",
        metadata={"summary": "BLK-003 loop identity binding evidence only"},
    )
    sample_envelope = build_relay_envelope_284(
        relay,
        source_identity_record=sample_identity,
        envelope_id="RELAY-BLK-SYSTEM-285-LOOP-EVIDENCE",
        message_type="HITL_APPROVAL_SIGNAL",
        target_component="blk-pipe",
        payload_hash=loop["loop_kernel_hash"],
        created_at="2026-05-20T20:03:00Z",
        trace_identity_hashes=[sample_identity["identity_hash"]],
        metadata={"summary": "per-iteration approval signal evidence only"},
    )
    package = {
        "status": "IDENTITY_RELAY_LOOP_EVIDENCE_READY",
        "markers": [
            "BLK_SYSTEM_285_IDENTITY_RELAY_LOOP_EVIDENCE_READY",
            "BLK003_LOOP_IDENTITY_RELAY_BINDING_READY",
            "NO_LOOP_RUNTIME_OR_DISPATCH_AUTHORITY",
        ],
        "identity_contract_hash": identity["identity_contract_hash"],
        "relay_contract_hash": relay["relay_contract_hash"],
        "loop_kernel_hash": loop["loop_kernel_hash"],
        "identity_record_sample_hash": sample_identity["identity_hash"],
        "relay_envelope_sample_hash": sample_envelope["relay_hash"],
        "loop_binding": {
            "per_iteration_identity_required": True,
            "relay_envelope_required_per_signal": True,
            "approval_record_identity_required_before_dispatch": True,
            "dispatch_authority_remains_external": True,
            "beo_closeout_execution_remains_external": True,
        },
        "side_effects": dict(_LOOP_EVIDENCE_SIDE_EFFECTS),
    }
    package["loop_evidence_hash"] = hash_package(package)
    return validate_identity_relay_loop_evidence_285(package, identity, relay, loop)


def validate_identity_relay_loop_evidence_285(
    evidence: dict[str, Any],
    identity_contract: dict[str, Any],
    relay_contract: dict[str, Any],
    loop_kernel: dict[str, Any],
) -> dict[str, Any]:
    identity = _validate_identity_contract(identity_contract)
    relay = _validate_relay_contract(relay_contract, identity)
    loop = _validate_loop_kernel_241(loop_kernel)
    _require_allowed_keys(evidence, _LOOP_EVIDENCE_KEYS, "loop evidence")
    if evidence.get("status") != "IDENTITY_RELAY_LOOP_EVIDENCE_READY":
        raise IdentityRelayValidationError("loop evidence status mismatch")
    if "BLK_SYSTEM_285_IDENTITY_RELAY_LOOP_EVIDENCE_READY" not in evidence.get("markers", []):
        raise IdentityRelayValidationError("loop evidence marker missing")
    if evidence.get("identity_contract_hash") != identity["identity_contract_hash"]:
        raise IdentityRelayValidationError("loop evidence identity_contract_hash mismatch")
    if evidence.get("relay_contract_hash") != relay["relay_contract_hash"]:
        raise IdentityRelayValidationError("loop evidence relay_contract_hash mismatch")
    if evidence.get("loop_kernel_hash") != loop["loop_kernel_hash"]:
        raise IdentityRelayValidationError("loop evidence loop_kernel_hash mismatch")
    _require_hash(evidence.get("identity_record_sample_hash"), "loop evidence identity_record_sample_hash")
    _require_hash(evidence.get("relay_envelope_sample_hash"), "loop evidence relay_envelope_sample_hash")
    binding = evidence.get("loop_binding")
    if binding != {
        "per_iteration_identity_required": True,
        "relay_envelope_required_per_signal": True,
        "approval_record_identity_required_before_dispatch": True,
        "dispatch_authority_remains_external": True,
        "beo_closeout_execution_remains_external": True,
    }:
        raise IdentityRelayValidationError("loop evidence loop_binding mismatch")
    _require_exact_side_effects(evidence, _LOOP_EVIDENCE_SIDE_EFFECTS, "loop evidence")
    _require_hash_field(evidence, "loop_evidence_hash", "loop evidence")
    _reject_laundering(evidence, "loop evidence")
    return _deepcopy(evidence)
