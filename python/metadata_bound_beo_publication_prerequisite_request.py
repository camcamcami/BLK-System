"""BLK-SYSTEM-127 metadata-bound BEO publication prerequisite request.

This module packages the BLK-SYSTEM-126 review-only decision gate and the
BLK-SYSTEM-125 metadata-only BEO/RTM interface into a deterministic prerequisite
request for a future external BEO publication approval-capture decision. It does
not approve publication, publish BEOs, sign, write storage, append ledgers,
generate RTM, run BLK-pipe/BLK-test/Codex, read protected bodies, or mutate
source/Git/target state.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any
from urllib.parse import unquote

from authoritative_beo_publication_authority_request import _canonical_hash
from beo_publication_path_decision_gate import (
    DECISION_GATE_READY,
    DECISION_SCOPE as GATE_DECISION_SCOPE,
    EXACT_EXCLUDED_AUTHORITIES as GATE_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as GATE_PROOF_OBLIGATIONS,
    SELECTED_NEXT_RUNG as GATE_SELECTED_NEXT_RUNG,
)

REQUEST_STATUS = "METADATA_BOUND_BEO_PUBLICATION_PREREQUISITE_REQUEST_READY_NOT_GRANTED"
REQUEST_PACKAGE_ID = "BEO-PUBLICATION-PREREQUISITE-REQUEST-127-001"
REQUEST_SCOPE = "METADATA_BOUND_BEO_PUBLICATION_PREREQUISITE_REQUEST_REVIEW_ONLY_NOT_PUBLICATION"
SELECTED_FRONTIER = "metadata_bound_beo_publication_prerequisite_request"
NEXT_REQUIRED_AUTHORITY = "EXPLICIT_HUMAN_EXTERNAL_BEO_PUBLICATION_APPROVAL_CAPTURE_REQUIRED_NOT_GRANTED"
DISABLED_ADAPTER_RESULT = "EXTERNAL_BEO_PUBLICATION_REQUEST_ADAPTER_DISABLED_NOT_AUTHORIZED"

SIDE_EFFECT_FLAGS = (
    "external_beo_publication_approval_captured",
    "beo_publication_approval_granted",
    "beo_publication_authorized",
    "beo_publication_performed",
    "runtime_published_beo_output",
    "signature_generated",
    "signer_key_material_accessed",
    "cryptographic_signing_performed",
    "immutable_storage_written",
    "storage_write_attempted",
    "public_ledger_mutated",
    "ledger_append_attempted",
    "rollback_executed",
    "revocation_executed",
    "supersession_executed",
    "rtm_generation_authorized",
    "rtm_generated",
    "rtm_drift_rejection_authorized",
    "drift_rejection_performed",
    "drift_decision_made",
    "active_vault_hash_comparison_performed",
    "coverage_claim_promoted",
    "coverage_matrix_generated",
    "protected_body_read",
    "protected_body_copy_attempted",
    "protected_body_hashing_attempted",
    "beb_dispatch_authorized",
    "beo_closeout_execution_authorized",
    "blk_pipe_execution_authorized",
    "blk_test_runtime_authorized",
    "codex_live_execution_authorized",
    "target_repo_scanned",
    "target_repo_mutated",
    "source_mutation_attempted",
    "git_mutation_attempted",
    "package_network_model_browser_cyber_tooling_authorized",
    "production_isolation_claimed",
)

EXACT_EXCLUDED_AUTHORITIES = {
    "BEB_DISPATCH",
    "BEO_CLOSEOUT_EXECUTION",
    "BEO_PUBLICATION_APPROVAL_CAPTURE",
    "AUTHORITATIVE_BEO_PUBLICATION",
    "RUNTIME_PUBLISHED_BEO_OUTPUT",
    "SIGNER_KEY_MATERIAL_ACCESS",
    "CRYPTOGRAPHIC_SIGNING",
    "IMMUTABLE_STORAGE_WRITE",
    "PUBLIC_LEDGER_APPEND_OR_MUTATION",
    "ROLLBACK_REVOCATION_SUPERSESSION_EXECUTION",
    "RTM_GENERATION",
    "RTM_DRIFT_REJECTION",
    "ACTIVE_VAULT_HASH_COMPARISON",
    "COVERAGE_MATRIX_OR_CLAIM_PROMOTION",
    "PROTECTED_BLK_REQ_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION",
    "BLK_PIPE_RUNTIME_DISPATCH",
    "BLK_TEST_RUNTIME_OR_PRODUCTION_MCP",
    "LIVE_CODEX_EXECUTION",
    "TARGET_REPO_SCAN_OR_MUTATION",
    "SOURCE_OR_GIT_MUTATION",
    "PACKAGE_MANAGER_NETWORK_MODEL_BROWSER_OR_CYBER_TOOLING",
    "PRODUCTION_SANDBOX_OR_HOST_SECRET_ISOLATION_CLAIM",
}

EXACT_PROOF_OBLIGATIONS = {
    "BLK125_METADATA_INTERFACE_IDENTITY_AND_HASH_BOUND",
    "BLK126_DECISION_GATE_IDENTITY_AND_HASH_BOUND",
    "BEO_AND_BEB_IDS_BOUND",
    "TRACE_METADATA_IDS_AND_VERSION_HASHES_BOUND",
    "TRACE_METADATA_ONLY_NO_PROTECTED_BODY_COPY",
    "DRAFT_ONLY_BEO_PUBLICATION_BOUNDARY_PRESERVED",
    "RTM_NOT_GENERATED_BOUNDARY_PRESERVED",
    "PREREQUISITE_REQUEST_ONLY_NOT_APPROVAL_CAPTURE",
    "PUBLICATION_APPROVAL_AND_EXECUTION_EXCLUDED",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_SIDE_EFFECTS_EXCLUDED",
    "RTM_GENERATION_AND_DRIFT_EXCLUDED",
    "BLK_PIPE_BLK_TEST_CODEX_RUNTIME_EXCLUDED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
    "SEPARATE_HUMAN_DECISION_REQUIRED_FOR_APPROVAL_CAPTURE",
    "SEPARATE_EXECUTION_SPRINT_REQUIRED_AFTER_APPROVAL",
}

_INTERFACE_KEYS = frozenset(
    {
        "interface_id",
        "source",
        "beo_id",
        "beb_id",
        "beo_status",
        "beo_publication",
        "rtm_status",
        "rtm_authority",
        "trace_artifacts",
        "metadata_handoff_status",
        "active_vault_read",
        "requirements_resolved",
        "protected_body_copied",
        "beb_dispatch_executed",
        "beo_closeout_executed",
        "beo_publication_attempted",
        "rtm_generation_executed",
        "drift_decision_executed",
        "signer_storage_ledger_touched",
        "reason",
    }
)

_GATE_KEYS = frozenset(
    {
        "decision_id",
        "decision_status",
        "decision_scope",
        "operator_identity",
        "selected_next_rung",
        "next_required_authority",
        "interface_id",
        "interface_hash",
        "beo_id",
        "beb_id",
        "beo_status",
        "beo_publication",
        "rtm_status",
        "rtm_authority",
        "metadata_handoff_status",
        "trace_artifacts",
        "exact_trace_identities",
        "future_request_id_candidate",
        "future_publication_prerequisite_request_required",
        "future_publication_prerequisite_request_authorized",
        "requested_at",
        "expires_at",
        "proof_obligations",
        "excluded_authorities",
        "decision_gate_hash",
    }
    | {
        "future_publication_prerequisite_request_authorized",
        "publication_approval_captured",
        "beo_publication_authorized",
        "beo_publication_attempted",
        "publication_performed",
        "runtime_published_beo_output",
        "signature_generated",
        "signer_key_material_accessed",
        "immutable_storage_written",
        "storage_write_attempted",
        "public_ledger_mutated",
        "ledger_append_attempted",
        "rollback_executed",
        "revocation_executed",
        "supersession_executed",
        "rtm_generation_authorized",
        "rtm_generated",
        "rtm_drift_rejection_authorized",
        "drift_rejection_performed",
        "drift_decision_made",
        "active_vault_hash_comparison_performed",
        "coverage_claim_promoted",
        "protected_body_read",
        "protected_body_copy_attempted",
        "beb_dispatch_authorized",
        "beo_closeout_execution_authorized",
        "blk_pipe_execution_authorized",
        "blk_test_runtime_authorized",
        "codex_live_execution_authorized",
        "target_repo_scanned",
        "target_repo_mutated",
        "source_mutation_attempted",
        "git_mutation_attempted",
        "package_network_model_browser_cyber_tooling_authorized",
        "production_isolation_claimed",
    }
)

_REQUEST_KEYS = frozenset(
    {
        "request_package_id",
        "operator_identity",
        "request_scope",
        "selected_frontier",
        "requested_at",
        "expires_at",
        "upstream_decision_id",
        "upstream_decision_gate_hash",
        "upstream_interface_id",
        "upstream_interface_hash",
        "exact_beo_id",
        "exact_beb_id",
        "exact_trace_identities",
        "request_external_beo_publication_approval_capture",
        "expired",
        "replayed",
        "stale",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        *SIDE_EFFECT_FLAGS,
    }
)

_ATTESTATION_KEYS = frozenset(
    {
        "metadata_interface_reviewed",
        "decision_gate_reviewed",
        "request_is_prerequisite_only_not_approval",
        "future_approval_capture_requires_separate_human_decision",
        "publication_execution_requires_separate_sprint_after_approval",
        "protected_body_reads_excluded",
        "signer_storage_ledger_rollback_side_effects_excluded",
        "rtm_generation_and_drift_excluded",
        "target_source_git_mutation_excluded",
        "no_adjacent_runtime_side_effects",
    }
)

_FALSE_INTERFACE_FLAGS = (
    "active_vault_read",
    "requirements_resolved",
    "protected_body_copied",
    "beb_dispatch_executed",
    "beo_closeout_executed",
    "beo_publication_attempted",
    "rtm_generation_executed",
    "drift_decision_executed",
    "signer_storage_ledger_touched",
)

_HASH_PREFIX = "sha256:"
_HASH_EXAMPLE = _HASH_PREFIX + "0" * 64
_EXPECTED_INTERFACE_REASON = "RTM generation remains disabled; fixture preserves opaque trace metadata only"
_SECRET_MARKERS = (
    "privatekey",
    "signerkeymaterial",
    "keymaterial",
    "apikey",
    "token",
    "password",
    "passphrase",
    "secret",
)
_AUTHORITY_MARKERS = (
    "approvedforpublication",
    "publicationapprovalgranted",
    "publicationauthoritygranted",
    "publicationauthority",
    "beopublicationauthorized",
    "beopublicationauthorised",
    "authoritativebeopublication",
    "publishbeo",
    "beopubapproved",
    "abpapproved",
    "greenlit",
    "publicationallowed",
    "publicationpermitted",
    "rtmgeneration",
    "rtmgenerated",
    "generatertm",
    "rtmid",
    "rtmdriftrejection",
    "driftrejection",
    "driftdecision",
    "activevaulthashcomparison",
    "coveragematrix",
    "coverageclaim",
    "coveragepromotion",
    "signaturegenerated",
    "cryptographicsigning",
    "immutablestoragewritten",
    "immutablestoragewrite",
    "publicledgerappend",
    "publicledgermutation",
    "publicledgermutated",
    "ledgerappend",
    "rollbackexecuted",
    "revocationexecuted",
    "supersessionexecuted",
    "docsactive",
    "docsrequirements",
    "docsusecases",
    "requirementsactive",
    "usecasesactive",
    "protectedblkreqbody",
    "protectedbody",
    "bodyexcerpt",
    "bodytext",
    "systemshall",
    "bebdispatch",
    "beocloseout",
    "blkpipedispatch",
    "blkpipeexecution",
    "blktestruntime",
    "productionblktestmcp",
    "codexlive",
    "codexapproval",
    "targetreposcan",
    "targetrepomutation",
    "sourcemutation",
    "gitmutation",
    "gitcommit",
    "gitpush",
    "packagemanager",
    "npminstall",
    "pipinstall",
    "goget",
    "networkcalled",
    "curl",
    "wget",
    "http",
    "https",
    "browsertooling",
    "cybertooling",
    "modelservice",
    "productionisolation",
    "productionsandbox",
    "hostsecretisolation",
)


def build_metadata_bound_beo_publication_prerequisite_request(
    interface: dict[str, Any],
    decision_gate: dict[str, Any],
    request: dict[str, Any],
) -> dict[str, Any]:
    """Build a metadata-bound, review-only prerequisite request package."""

    normalized_interface = _validate_interface(interface)
    normalized_gate = _validate_decision_gate(decision_gate, normalized_interface)
    normalized_request = _validate_request(request, normalized_interface, normalized_gate)

    package = {
        "request_status": REQUEST_STATUS,
        "request_package_id": REQUEST_PACKAGE_ID,
        "operator_identity": normalized_request["operator_identity"],
        "request_scope": REQUEST_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY,
        "upstream_decision_id": normalized_gate["decision_id"],
        "upstream_decision_gate_hash": normalized_gate["decision_gate_hash"],
        "upstream_interface_id": normalized_interface["interface_id"],
        "upstream_interface_hash": _canonical_hash(normalized_interface),
        "beo_id": normalized_interface["beo_id"],
        "beb_id": normalized_interface["beb_id"],
        "beo_status": normalized_interface["beo_status"],
        "beo_publication": normalized_interface["beo_publication"],
        "rtm_status": normalized_interface["rtm_status"],
        "rtm_authority": normalized_interface["rtm_authority"],
        "metadata_handoff_status": normalized_interface["metadata_handoff_status"],
        "trace_artifacts": deepcopy(normalized_interface["trace_artifacts"]),
        "exact_trace_identities": list(normalized_request["exact_trace_identities"]),
        "external_beo_publication_approval_capture_requested": True,
        "external_beo_publication_approval_captured": False,
        "publication_execution_requires_separate_sprint_after_approval": True,
        "decision_gate_summary": {
            "decision_id": normalized_gate["decision_id"],
            "decision_status": normalized_gate["decision_status"],
            "decision_scope": normalized_gate["decision_scope"],
            "selected_next_rung": normalized_gate["selected_next_rung"],
            "decision_gate_hash": normalized_gate["decision_gate_hash"],
            "future_request_id_candidate": normalized_gate["future_request_id_candidate"],
        },
        "operator_attestation": deepcopy(normalized_request["operator_attestation"]),
        "proof_obligations": list(normalized_request["proof_obligations"]),
        "excluded_authorities": list(normalized_request["excluded_authorities"]),
        "requested_at": normalized_request["requested_at"],
        "expires_at": normalized_request["expires_at"],
        **{flag: False for flag in SIDE_EFFECT_FLAGS},
    }
    package["request_package_hash"] = _canonical_hash(package)
    return package


def simulate_disabled_external_beo_publication_request_adapter(record: dict[str, Any]) -> dict[str, Any]:
    """Return fail-closed adapter evidence without external publication side effects."""

    request_package_id = None
    selected_frontier = None
    if isinstance(record, dict):
        candidate_id = record.get("request_package_id")
        if (
            record.get("selected_frontier") == SELECTED_FRONTIER
            and candidate_id == REQUEST_PACKAGE_ID
        ):
            request_package_id = candidate_id
            selected_frontier = SELECTED_FRONTIER

    return {
        "adapter_result": DISABLED_ADAPTER_RESULT,
        "request_package_id": request_package_id,
        "selected_frontier": selected_frontier,
        "blocked_reasons": ["External BEO publication approval/execution requires separate explicit authority"],
        "blk_pipe_dispatched": False,
        "blk_test_runtime_started": False,
        "codex_subprocess_started": False,
        "package_manager_called": False,
        "network_called": False,
        "model_service_called": False,
        "browser_tooling_called": False,
        "cyber_tooling_called": False,
        **{flag: False for flag in SIDE_EFFECT_FLAGS},
    }


def _validate_interface(interface: Any) -> dict[str, Any]:
    if not isinstance(interface, dict):
        raise ValueError("interface must be a dictionary")
    unknown = sorted(set(interface) - _INTERFACE_KEYS)
    if unknown:
        raise ValueError(f"metadata interface rejects unexpected field {unknown[0]!r}")
    normalized = deepcopy(interface)
    if _required_string(normalized.get("source"), "source") != "beo-rtm-interface-fixture":
        raise ValueError("source must be beo-rtm-interface-fixture")
    if not _matches_prefix_digits(_required_string(normalized.get("interface_id"), "interface_id"), "BEO_RTM_IFACE_"):
        raise ValueError("interface_id must be exact BEO_RTM_IFACE_###")
    if not _matches_prefix_digits(_required_string(normalized.get("beo_id"), "beo_id"), "BEO_"):
        raise ValueError("beo_id must be exact BEO_###")
    if not _matches_prefix_digits(_required_string(normalized.get("beb_id"), "beb_id"), "BEB_"):
        raise ValueError("beb_id must be exact BEB_###")
    if normalized.get("beo_status") != "PASS":
        raise ValueError("beo_status must be PASS")
    if normalized.get("beo_publication") != "DRAFT_ONLY":
        raise ValueError("beo_publication must remain DRAFT_ONLY")
    if normalized.get("rtm_status") != "NOT_GENERATED":
        raise ValueError("rtm_status must remain NOT_GENERATED")
    if normalized.get("rtm_authority") != "DISABLED_INTERFACE_ONLY":
        raise ValueError("rtm_authority must remain DISABLED_INTERFACE_ONLY")
    if normalized.get("metadata_handoff_status") != "BLK_REQ_TRACE_METADATA_ONLY":
        raise ValueError("metadata_handoff_status must be BLK_REQ_TRACE_METADATA_ONLY")
    if normalized.get("reason") != _EXPECTED_INTERFACE_REASON:
        raise ValueError("metadata interface reason must match BLK-SYSTEM-125 disabled RTM boundary")
    for flag in _FALSE_INTERFACE_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    normalized["trace_artifacts"] = _validate_trace_artifacts(normalized.get("trace_artifacts"))
    return normalized


def _validate_decision_gate(gate: Any, interface: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(gate, dict):
        raise ValueError("decision_gate must be a dictionary")
    unknown = sorted(set(gate) - _GATE_KEYS)
    if unknown:
        raise ValueError(f"decision gate rejects unexpected field {unknown[0]!r}")
    normalized = deepcopy(gate)
    gate_hash = _required_hash(normalized.get("decision_gate_hash"), "decision_gate_hash")
    recomputed = _canonical_hash({key: value for key, value in normalized.items() if key != "decision_gate_hash"})
    if gate_hash != recomputed:
        raise ValueError("decision_gate_hash does not match submitted decision gate")
    decision_id = _required_string(normalized.get("decision_id"), "decision_id")
    _reject_laundered_string(decision_id, "decision_gate.decision_id")
    if not _matches_hyphenated_suffix(decision_id, "BEO-PUBLICATION-PATH-DECISION-GATE-", 3, 3):
        raise ValueError("decision gate decision_id must be exact BEO-PUBLICATION-PATH-DECISION-GATE-###-###")
    if decision_id != "BEO-PUBLICATION-PATH-DECISION-GATE-126-001":
        raise ValueError("decision gate decision_id must be exact BEO-PUBLICATION-PATH-DECISION-GATE-126-001")
    operator_identity = _required_string(normalized.get("operator_identity"), "operator_identity")
    _reject_laundered_string(operator_identity, "decision_gate.operator_identity")
    if not _matches_discord_identity(operator_identity):
        raise ValueError("decision gate operator_identity must be discord:<snowflake>")
    if normalized.get("decision_status") != DECISION_GATE_READY:
        raise ValueError("decision gate status must be ready")
    if normalized.get("decision_scope") != GATE_DECISION_SCOPE:
        raise ValueError("decision gate scope must be review-only")
    if normalized.get("selected_next_rung") != GATE_SELECTED_NEXT_RUNG:
        raise ValueError(f"decision gate selected_next_rung must be {GATE_SELECTED_NEXT_RUNG}")
    if normalized.get("future_request_id_candidate") != REQUEST_PACKAGE_ID:
        raise ValueError("decision gate future_request_id_candidate must match BLK-SYSTEM-127 request id")
    if normalized.get("future_publication_prerequisite_request_required") is not True:
        raise ValueError("decision gate must require future prerequisite request")
    if normalized.get("future_publication_prerequisite_request_authorized") is not False:
        raise ValueError("decision gate future request authorization must remain false")
    if normalized.get("interface_id") != interface["interface_id"]:
        raise ValueError("decision gate interface_id does not match metadata interface")
    if normalized.get("interface_hash") != _canonical_hash(interface):
        raise ValueError("decision gate interface_hash does not match metadata interface")
    if normalized.get("beo_id") != interface["beo_id"]:
        raise ValueError("decision gate beo_id does not match metadata interface")
    if normalized.get("beb_id") != interface["beb_id"]:
        raise ValueError("decision gate beb_id does not match metadata interface")
    if normalized.get("beo_publication") != "DRAFT_ONLY":
        raise ValueError("decision gate beo_publication must remain DRAFT_ONLY")
    if normalized.get("rtm_status") != "NOT_GENERATED":
        raise ValueError("decision gate rtm_status must remain NOT_GENERATED")
    normalized["trace_artifacts"] = _validate_trace_artifacts(normalized.get("trace_artifacts"))
    if normalized["trace_artifacts"] != interface["trace_artifacts"]:
        raise ValueError("decision gate trace_artifacts must match metadata interface")
    if _validate_exact_trace_identities(normalized.get("exact_trace_identities")) != _trace_identity_strings(interface["trace_artifacts"]):
        raise ValueError("decision gate exact_trace_identities must match metadata interface")
    if _required_exact_set(normalized.get("proof_obligations"), GATE_PROOF_OBLIGATIONS, "proof_obligations") != sorted(GATE_PROOF_OBLIGATIONS):
        raise ValueError("decision gate proof_obligations must match exact set")
    if _required_exact_set(normalized.get("excluded_authorities"), GATE_EXCLUDED_AUTHORITIES, "excluded_authorities") != sorted(GATE_EXCLUDED_AUTHORITIES):
        raise ValueError("decision gate excluded_authorities must match exact denied authority set")
    for flag in set(_GATE_KEYS) - {
        "decision_id",
        "decision_status",
        "decision_scope",
        "operator_identity",
        "selected_next_rung",
        "next_required_authority",
        "interface_id",
        "interface_hash",
        "beo_id",
        "beb_id",
        "beo_status",
        "beo_publication",
        "rtm_status",
        "rtm_authority",
        "metadata_handoff_status",
        "trace_artifacts",
        "exact_trace_identities",
        "future_request_id_candidate",
        "future_publication_prerequisite_request_required",
        "requested_at",
        "expires_at",
        "proof_obligations",
        "excluded_authorities",
        "decision_gate_hash",
    }:
        if normalized.get(flag) is not False:
            raise ValueError(f"decision gate {flag} must remain false")
    return normalized


def _validate_request(request: Any, interface: dict[str, Any], gate: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("request must be a dictionary")
    unknown = sorted(set(request) - _REQUEST_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    normalized = deepcopy(request)
    request_id = _required_string(normalized.get("request_package_id"), "request_package_id")
    _reject_laundered_string(request_id, "request_package_id")
    if not _matches_hyphenated_suffix(request_id, "BEO-PUBLICATION-PREREQUISITE-REQUEST-", 3, 3):
        raise ValueError("request_package_id must be exact BEO-PUBLICATION-PREREQUISITE-REQUEST-###-###")
    if request_id != REQUEST_PACKAGE_ID:
        raise ValueError(f"request_package_id must be {REQUEST_PACKAGE_ID}")
    operator_identity = _required_string(normalized.get("operator_identity"), "operator_identity")
    _reject_laundered_string(operator_identity, "operator_identity")
    if not _matches_discord_identity(operator_identity):
        raise ValueError("operator_identity must be discord:<snowflake>")
    if normalized.get("request_scope") != REQUEST_SCOPE:
        raise ValueError(f"request_scope must be {REQUEST_SCOPE}")
    if normalized.get("selected_frontier") != SELECTED_FRONTIER:
        raise ValueError(f"selected_frontier must be {SELECTED_FRONTIER}")
    requested = _parse_timestamp(normalized.get("requested_at"), "requested_at")
    expires = _parse_timestamp(normalized.get("expires_at"), "expires_at")
    if expires <= requested:
        raise ValueError("expires_at must be after requested_at")
    if normalized.get("expired") is not False:
        raise ValueError("request must not be expired")
    if normalized.get("replayed") is not False:
        raise ValueError("request must not be replayed")
    if normalized.get("stale") is not False:
        raise ValueError("request must not be stale")
    if normalized.get("request_external_beo_publication_approval_capture") is not True:
        raise ValueError("request_external_beo_publication_approval_capture must be true")
    if normalized.get("upstream_decision_id") != gate["decision_id"]:
        raise ValueError("upstream_decision_id does not match decision gate")
    if normalized.get("upstream_decision_gate_hash") != gate["decision_gate_hash"]:
        raise ValueError("upstream_decision_gate_hash does not match decision gate")
    if normalized.get("upstream_interface_id") != interface["interface_id"]:
        raise ValueError("upstream_interface_id does not match metadata interface")
    if normalized.get("upstream_interface_hash") != _canonical_hash(interface):
        raise ValueError("upstream_interface_hash does not match metadata interface")
    if normalized.get("exact_beo_id") != interface["beo_id"]:
        raise ValueError("exact_beo_id does not match metadata interface")
    if normalized.get("exact_beb_id") != interface["beb_id"]:
        raise ValueError("exact_beb_id does not match metadata interface")
    exact_trace_identities = _validate_exact_trace_identities(normalized.get("exact_trace_identities"))
    if exact_trace_identities != _trace_identity_strings(interface["trace_artifacts"]):
        raise ValueError("exact_trace_identities must match metadata interface")
    normalized["exact_trace_identities"] = exact_trace_identities
    normalized["operator_attestation"] = _validate_attestation(normalized.get("operator_attestation"))
    normalized["proof_obligations"] = _required_exact_set(normalized.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS, "proof_obligations")
    normalized["excluded_authorities"] = _required_exact_set(normalized.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities")
    for flag in SIDE_EFFECT_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
        normalized[flag] = False
    return normalized


def _validate_trace_artifacts(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list) or not value:
        raise ValueError("trace_artifacts must be a non-empty list")
    normalized = []
    seen = set()
    for artifact in value:
        if not isinstance(artifact, dict):
            raise ValueError("trace_artifacts must contain dictionaries")
        _scan_allowed_trace_values(artifact)
        unknown = sorted(set(artifact) - {"kind", "id", "version_hash"})
        if unknown:
            raise ValueError(f"trace_artifacts rejects unsupported key {unknown[0]!r}")
        kind = _required_string(artifact.get("kind"), "trace_artifacts.kind")
        artifact_id = _required_string(artifact.get("id"), "trace_artifacts.id")
        version_hash = _required_hash(artifact.get("version_hash"), "trace_artifacts.version_hash")
        if kind not in {"REQ", "UC"}:
            raise ValueError("trace_artifacts.kind must be REQ or UC")
        if not artifact_id.startswith(f"{kind}-"):
            raise ValueError("trace_artifacts.kind must match id prefix")
        suffix = artifact_id.removeprefix(f"{kind}-")
        if len(suffix) != 3 or not _is_ascii_digits(suffix):
            raise ValueError("trace_artifacts.id must be exact REQ-### or UC-###")
        identity = (kind, artifact_id)
        if identity in seen:
            raise ValueError("duplicate trace_artifacts identity")
        seen.add(identity)
        normalized.append({"kind": kind, "id": artifact_id, "version_hash": version_hash})
    return normalized


def _scan_allowed_trace_values(artifact: dict[str, Any]) -> None:
    for key, value in artifact.items():
        if key not in {"kind", "id", "version_hash"}:
            continue
        if isinstance(value, str):
            _reject_laundered_string(value, f"trace_artifacts.{key}")


def _validate_attestation(value: Any) -> dict[str, bool]:
    if not isinstance(value, dict):
        raise ValueError("operator_attestation must be a dictionary")
    unknown = sorted(set(value) - _ATTESTATION_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    normalized = {}
    for key in sorted(_ATTESTATION_KEYS):
        if value.get(key) is not True:
            raise ValueError(f"operator_attestation.{key} must be true")
        normalized[key] = True
    return normalized


def _trace_identity_strings(trace_artifacts: list[dict[str, str]]) -> list[str]:
    return [f"{item['kind']}:{item['id']}:{item['version_hash']}" for item in trace_artifacts]


def _validate_exact_trace_identities(value: Any) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValueError("exact_trace_identities must be a non-empty list")
    identities = []
    seen = set()
    for item in value:
        text = _required_string(item, "exact_trace_identities item")
        _reject_laundered_string(text, "exact_trace_identities")
        parts = text.split(":", 3)
        if len(parts) != 4 or parts[0] not in {"REQ", "UC"} or parts[2] != "sha256":
            raise ValueError("exact_trace_identities must use KIND:ID:sha256:<64 hex>")
        prefix, artifact_id, _, digest = parts
        if not artifact_id.startswith(f"{prefix}-"):
            raise ValueError("exact_trace_identities kind must match id prefix")
        suffix = artifact_id.removeprefix(f"{prefix}-")
        if len(suffix) != 3 or not _is_ascii_digits(suffix):
            raise ValueError("exact_trace_identities id must be exact REQ-### or UC-###")
        _required_hash(f"sha256:{digest}", "exact_trace_identities.version_hash")
        if text in seen:
            raise ValueError("exact_trace_identities must not contain duplicates")
        seen.add(text)
        identities.append(text)
    return identities


def _required_exact_set(value: Any, required: set[str], field: str) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{field} must be a list")
    if len(value) != len(set(value)):
        raise ValueError(f"{field} must not contain duplicates")
    actual = set(value)
    if actual != required:
        if field == "excluded_authorities":
            raise ValueError("excluded_authorities must match exact denied authority set")
        raise ValueError(f"{field} must match exact set")
    return sorted(actual)


def _parse_timestamp(value: Any, field: str) -> datetime:
    text = _required_string(value, field)
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"{field} must be an ISO timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{field} must include timezone")
    return parsed


def _required_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value


def _required_hash(value: Any, field: str) -> str:
    text = _required_string(value, field)
    if len(text) != len(_HASH_EXAMPLE) or not text.startswith(_HASH_PREFIX):
        raise ValueError(f"{field} must be canonical sha256:<64 lowercase hex>")
    digest = text.removeprefix(_HASH_PREFIX)
    if any(ch not in "0123456789abcdef" for ch in digest):
        raise ValueError(f"{field} must be canonical sha256:<64 lowercase hex>")
    return text


def _matches_prefix_digits(value: str, prefix: str, digits: int = 3) -> bool:
    suffix = value.removeprefix(prefix)
    return value.startswith(prefix) and len(suffix) == digits and _is_ascii_digits(suffix)


def _matches_hyphenated_suffix(value: str, prefix: str, *digit_groups: int) -> bool:
    if not value.startswith(prefix):
        return False
    suffix = value.removeprefix(prefix)
    parts = suffix.split("-")
    return len(parts) == len(digit_groups) and all(
        len(part) == width and _is_ascii_digits(part) for part, width in zip(parts, digit_groups)
    )


def _matches_discord_identity(value: str) -> bool:
    prefix = "discord:"
    suffix = value.removeprefix(prefix)
    return value.startswith(prefix) and 17 <= len(suffix) <= 20 and _is_ascii_digits(suffix)


def _is_ascii_digits(value: str) -> bool:
    return bool(value) and all(ch in "0123456789" for ch in value)


def _reject_laundered_string(text: str, field: str) -> None:
    for variant in _decoded_variants(text):
        compact = _compact(variant)
        if any(marker in compact for marker in _SECRET_MARKERS):
            raise ValueError(f"secret-bearing field {field}")
        if any(marker in compact for marker in _AUTHORITY_MARKERS):
            raise ValueError(f"authority-laundering text in {field}")


def _decoded_variants(text: str) -> list[str]:
    variants = [text]
    current = text
    for _ in range(8):
        decoded = unquote(current)
        if decoded == current:
            break
        variants.append(decoded)
        current = decoded
    return variants


def _compact(text: str) -> str:
    return "".join(ch for ch in text.casefold() if ch.isalnum())
