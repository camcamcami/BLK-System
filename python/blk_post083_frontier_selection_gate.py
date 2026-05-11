from __future__ import annotations

from copy import deepcopy
from typing import Any

SELECTION_STATUS = "BLK_SYSTEM_POST_083_FRONTIER_SELECTION_GATE"
READY = "POST_083_FRONTIER_SELECTION_READY_FOR_HUMAN_DECISION_NOT_AUTHORITY"
BLOCKED = "POST_083_FRONTIER_SELECTION_BLOCKED_NOT_AUTHORIZED"
BLOCKED_PENDING_PUBLICATION_PREREQUISITES = "POST_083_FRONTIER_SELECTION_BLOCKED_PENDING_PUBLICATION_PREREQUISITES"
DISABLED = "POST_083_FRONTIER_ACTIVATION_DISABLED_NOT_AUTHORIZED"
MATURITY = "L0_L1_POST_083_SELECTION_FIXTURE_ONLY"

ALLOWED_FRONTIERS = frozenset(
    {
        "bounded_blk_test_evidence_refresh",
        "beo_publication_pilot_execution_request",
        "codex_live_dispatch_l3_smoke",
        "rtm_authority_request_after_publication_prerequisites",
        "bounded_consolidation_or_remediation_sprint",
    }
)

DENIED_FLAGS = (
    "runtime_authority_granted",
    "publication_approval_granted",
    "publication_pilot_execution_authorized",
    "publication_pilot_executed",
    "beo_published",
    "signer_key_material_accessed",
    "cryptographic_signing_performed",
    "immutable_storage_written",
    "public_ledger_mutated",
    "rollback_executed",
    "runtime_rtm_generation_authorized",
    "rtm_generated",
    "drift_rejection_authorized",
    "drift_rejection_performed",
    "blk_test_runtime_authorized",
    "blk_test_runtime_started",
    "production_blk_test_mcp_authorized",
    "codex_live_dispatch_authorized",
    "codex_subprocess_started",
    "blk_pipe_dispatch_authorized",
    "blk_pipe_dispatched",
    "target_repo_scan_authorized",
    "target_repo_scanned",
    "target_repo_mutation_authorized",
    "target_repo_mutated",
    "source_mutation_authorized",
    "git_mutation_authorized",
    "protected_body_read_authorized",
    "protected_body_copy_authorized",
    "protected_body_scan_authorized",
    "package_manager_authorized",
    "network_model_cyber_browser_tooling_authorized",
    "production_isolation_claimed",
)

TOP_LEVEL_KEYS = frozenset(
    {
        "selection_id",
        "selection_status",
        "review_status",
        "maturity",
        "roadmap_source",
        "current_state_source",
        "post083_source",
        "selected_frontier",
        "exactly_one_frontier_selected",
        "publication_prerequisites_satisfied",
        "governing_docs",
        "frontier_prerequisites",
        "decision_evidence",
        "required_future_approval_fields",
        "excluded_adjacent_authorities",
        "hostile_review_checklist",
        "disabled_activation_adapter_required",
        "validation_errors",
        *DENIED_FLAGS,
    }
)

REQUIRED_APPROVAL_FIELD_MARKERS = (
    "source system",
    "operator identity",
    "message/event id",
    "issued timestamp",
    "expires timestamp",
    "exact selected frontier",
    "exact future scope",
    "explicit excluded authorities",
    "fresh approval id",
    "fresh run id",
    "replay ledger",
    "operator stop controls",
    "hostile review",
)

REQUIRED_HOSTILE_REVIEW_MARKERS = (
    "next logical sprint is not approval",
    "BLK-083 decision package is not publication approval",
    "exactly one frontier",
    "adjacent authority inheritance",
    "RTM requires publication prerequisites",
    "protected body no read",
    "target repo no scan or mutation",
    "disabled adapter side effects",
    "generic authority laundering",
    "percent encoded authority laundering",
)

REQUIRED_EXCLUDED_AUTHORITIES = frozenset(
    {
        "actual_authoritative_beo_publication",
        "publication_approval_capture",
        "publication_pilot_execution",
        "signer_key_material_access",
        "cryptographic_signing",
        "immutable_storage_write",
        "public_ledger_mutation",
        "rollback_revocation_supersession_execution",
        "runtime_rtm_generation",
        "rtm_drift_rejection",
        "active_vault_hash_comparison",
        "coverage_claim_promotion",
        "protected_body_read_copy_parse_hash_summarize_scan_mutate",
        "target_repo_scan",
        "target_repo_mutation",
        "beb_dispatch_or_beo_closeout_execution",
        "blk_pipe_dispatch",
        "blk_test_runtime_or_production_mcp",
        "codex_live_execution",
        "package_manager_network_model_browser_cyber_tooling",
        "production_isolation_claim",
    }
)

SUSPICIOUS_KEY_TERMS = (
    "authority",
    "authorized",
    "authorization",
    "approval",
    "approved",
    "allowed",
    "grant",
    "claim",
    "publish",
    "publication",
    "runtime",
    "execution",
    "rtm",
    "drift",
    "protected",
    "secret",
    "token",
    "keymaterial",
    "targetrepo",
    "target_repo",
)

ALLOWED_SUSPICIOUS_KEYS = frozenset(
    {
        "required_future_approval_fields",
        "excluded_adjacent_authorities",
        "publication_prerequisites_satisfied",
        "next_logical_sprint_not_approval",
        "next_sprint_not_approval",
        "blk083_decision_package_not_publication_approval",
        "review_ready_not_runtime_authority",
        "fixture_ready_not_runtime_authority",
        "rtm_request_requires_publication_prerequisites",
        *DENIED_FLAGS,
    }
)

FORBIDDEN_COMPACT_MARKERS = (
    "approvedforliveexecution",
    "authorizedforliveexecution",
    "approvedforruntimeexecution",
    "readyforruntime",
    "runtimeapproved",
    "runtimeauthorized",
    "runtimeauthoritygranted",
    "liveexecutionauthorized",
    "beopublicationauthorized",
    "authoritativebeopublication",
    "beopubapproved",
    "abpapproved",
    "publishbeo",
    "publicationauthoritygranted",
    "approvedforpublication",
    "greenlitforpublication",
    "publicationpilotexecuted",
    "publicationpilotapproved",
    "signaturegenerated",
    "cryptographicsigning",
    "signerkeymaterial",
    "privatekey",
    "apikey",
    "secret",
    "token",
    "immutablestoragewrite",
    "publicledgerappend",
    "publicledgermutation",
    "rollbackexecuted",
    "rtmgeneration",
    "rtmgenerated",
    "rtmid",
    "driftrejectionauthority",
    "activevaulthashcomparison",
    "coverageclaim",
    "docsactive",
    "protectedbodyread",
    "protectedbodycopy",
    "protectedbodyscan",
    "targetreposcan",
    "targetrepomutation",
    "bebdispatch",
    "beocloseoutexecution",
    "blkpipeexecutionapproval",
    "blkpipedispatch",
    "blktestpassapproval",
    "productionblktestmcp",
    "codexapproval",
    "codexliveapproval",
    "packageinstall",
    "npminstall",
    "pipinstall",
    "goget",
    "curl",
    "wget",
    "https",
    "http",
    "productionsandboxenforced",
    "hostsecretisolation",
)


def build_post083_frontier_selection_gate(
    *,
    selection_id: str,
    selected_frontier: str,
    used_selection_ids: set[str],
    publication_prerequisites_satisfied: bool = False,
) -> dict[str, Any]:
    record = {
        "selection_id": selection_id,
        "selection_status": SELECTION_STATUS,
        "review_status": BLOCKED,
        "maturity": MATURITY,
        "roadmap_source": "BLK-077",
        "current_state_source": "BLK-079",
        "post083_source": "BLK-083",
        "selected_frontier": selected_frontier,
        "exactly_one_frontier_selected": True,
        "publication_prerequisites_satisfied": bool(publication_prerequisites_satisfied),
        "governing_docs": _governing_docs_for(selected_frontier),
        "frontier_prerequisites": _frontier_prerequisites_for(selected_frontier, publication_prerequisites_satisfied),
        "decision_evidence": {
            "next_logical_sprint_not_approval": True,
            "next_sprint_not_approval": True,
            "blk083_decision_package_not_publication_approval": True,
            "review_ready_not_runtime_authority": True,
            "fixture_ready_not_runtime_authority": True,
            "rtm_request_requires_publication_prerequisites": True,
        },
        "required_future_approval_fields": list(REQUIRED_APPROVAL_FIELD_MARKERS),
        "excluded_adjacent_authorities": sorted(REQUIRED_EXCLUDED_AUTHORITIES),
        "hostile_review_checklist": list(REQUIRED_HOSTILE_REVIEW_MARKERS),
        "disabled_activation_adapter_required": True,
        "validation_errors": [],
        **{flag: False for flag in DENIED_FLAGS},
    }
    return validate_post083_frontier_selection_gate(record, used_selection_ids=used_selection_ids)


def validate_post083_frontier_selection_gate(record: dict[str, Any], *, used_selection_ids: set[str]) -> dict[str, Any]:
    if used_selection_ids is None:
        raise ValueError("used_selection_ids must be supplied for replay protection")
    if not isinstance(record, dict):
        raise ValueError("post-083 frontier selection record must be a dictionary")

    evaluated = deepcopy(record)
    errors: list[str] = []

    unknown = sorted(set(evaluated) - TOP_LEVEL_KEYS)
    errors.extend(f"unsupported top-level key {key!r}" for key in unknown)

    if evaluated.get("selection_status") != SELECTION_STATUS:
        errors.append("selection_status invalid")
    if evaluated.get("maturity") != MATURITY:
        errors.append("maturity invalid")
    if evaluated.get("roadmap_source") != "BLK-077":
        errors.append("roadmap_source must be BLK-077")
    if evaluated.get("current_state_source") != "BLK-079":
        errors.append("current_state_source must be BLK-079")
    if evaluated.get("post083_source") != "BLK-083":
        errors.append("post083_source must be BLK-083")
    if evaluated.get("disabled_activation_adapter_required") is not True:
        errors.append("disabled_activation_adapter_required must be true")

    selection_id = evaluated.get("selection_id")
    if not isinstance(selection_id, str) or not selection_id.strip():
        errors.append("selection_id missing")
    elif selection_id in used_selection_ids:
        errors.append("selection replayed")

    frontier = evaluated.get("selected_frontier")
    if not isinstance(frontier, str) or frontier not in ALLOWED_FRONTIERS:
        errors.append("selected_frontier must name exactly one post-083 allowed frontier")
    if not isinstance(frontier, str) or evaluated.get("exactly_one_frontier_selected") is not True:
        errors.append("exactly_one_frontier_selected must be true for one selected_frontier")

    publication_prereq = evaluated.get("publication_prerequisites_satisfied")
    if not isinstance(publication_prereq, bool):
        errors.append("publication_prerequisites_satisfied must be boolean")
    if frontier == "rtm_authority_request_after_publication_prerequisites" and publication_prereq is not True:
        errors.append("publication prerequisites must be satisfied before RTM authority request selection")

    docs = evaluated.get("governing_docs")
    if not isinstance(docs, list) or "BLK-084" not in docs:
        errors.append("governing_docs must include BLK-084")
    elif isinstance(frontier, str) and frontier in ALLOWED_FRONTIERS:
        missing_docs = sorted(set(_governing_docs_for(frontier)) - set(docs))
        errors.extend(f"governing_docs missing {doc}" for doc in missing_docs)

    errors.extend(_decision_evidence_errors(evaluated.get("decision_evidence")))
    errors.extend(_required_marker_errors("required_future_approval_fields", evaluated.get("required_future_approval_fields"), REQUIRED_APPROVAL_FIELD_MARKERS))
    errors.extend(_required_set_errors("excluded_adjacent_authorities", evaluated.get("excluded_adjacent_authorities"), REQUIRED_EXCLUDED_AUTHORITIES))
    errors.extend(_required_marker_errors("hostile_review_checklist", evaluated.get("hostile_review_checklist"), REQUIRED_HOSTILE_REVIEW_MARKERS))

    for flag in DENIED_FLAGS:
        if evaluated.get(flag) is not False:
            errors.append(f"{flag} must be false")
        evaluated[flag] = False

    errors.extend(_authority_laundering_errors(evaluated))
    evaluated["validation_errors"] = errors
    if errors == ["publication prerequisites must be satisfied before RTM authority request selection"]:
        evaluated["review_status"] = BLOCKED_PENDING_PUBLICATION_PREREQUISITES
    else:
        evaluated["review_status"] = BLOCKED if errors else READY
    return evaluated


def simulate_disabled_post083_frontier_activation_adapter(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "adapter_result": DISABLED,
        "selection_id": record.get("selection_id") if isinstance(record, dict) else None,
        "selected_frontier": record.get("selected_frontier") if isinstance(record, dict) else None,
        "blocked_reasons": ["post-083 frontier activation adapter disabled; separate explicit authority required"],
        "publication_approval_captured": False,
        "publication_pilot_executed": False,
        "beo_published": False,
        "signer_key_material_accessed": False,
        "cryptographic_signing_performed": False,
        "immutable_storage_written": False,
        "public_ledger_mutated": False,
        "rollback_executed": False,
        "rtm_generated": False,
        "drift_rejection_performed": False,
        "blk_test_runtime_started": False,
        "codex_subprocess_started": False,
        "blk_pipe_dispatched": False,
        "target_repo_scanned": False,
        "target_repo_mutated": False,
        "source_mutation_attempted": False,
        "git_mutation_attempted": False,
        "protected_body_read_attempted": False,
        "protected_body_copy_attempted": False,
        "protected_body_scan_attempted": False,
        "package_manager_called": False,
        "network_called": False,
        "model_service_called": False,
        "browser_tooling_called": False,
        "cyber_tooling_called": False,
        "production_isolation_claimed": False,
    }


def _governing_docs_for(frontier: Any) -> list[str]:
    common = ["BLK-001", "BLK-003", "BLK-006", "BLK-077", "BLK-079", "BLK-084"]
    if frontier == "bounded_blk_test_evidence_refresh":
        return common + ["BLK-017", "BLK-018", "BLK-019", "BLK-020", "BLK-072", "BLK-073", "BLK-074"]
    if frontier == "beo_publication_pilot_execution_request":
        return common + ["BLK-022", "BLK-026", "BLK-057", "BLK-060", "BLK-083"]
    if frontier == "codex_live_dispatch_l3_smoke":
        return common + ["BLK-040", "BLK-041", "BLK-042", "BLK-043", "BLK-044"]
    if frontier == "rtm_authority_request_after_publication_prerequisites":
        return common + ["BLK-023", "BLK-027", "BLK-029", "BLK-030", "BLK-033", "BLK-083"]
    if frontier == "bounded_consolidation_or_remediation_sprint":
        return common
    return common


def _frontier_prerequisites_for(frontier: Any, publication_prerequisites_satisfied: bool) -> list[str]:
    if frontier == "bounded_blk_test_evidence_refresh":
        return [
            "fresh exact target identity required before any runtime evidence refresh",
            "fresh approval id and run id required before runtime",
            "evidence remains evidence only, not mutation, publication, RTM, or coverage authority",
        ]
    if frontier == "beo_publication_pilot_execution_request":
        return [
            "fresh explicit human publication pilot approval required",
            "BLK-083 decision package is request evidence only",
            "signer/storage/ledger/rollback policies must remain no-side-effect unless separately authorized",
        ]
    if frontier == "codex_live_dispatch_l3_smoke":
        return [
            "fresh explicit live Codex approval required",
            "exact model, CLI profile, timeout, output, and allowlists required",
            "source mutation requires BLK-pipe enforcement and exact allowlists",
        ]
    if frontier == "rtm_authority_request_after_publication_prerequisites":
        state = "satisfied" if publication_prerequisites_satisfied else "not satisfied"
        return [
            f"actual published-BEO publication prerequisites are {state}",
            "runtime RTM generation must not proceed from fixture/request-only publication evidence",
            "drift rejection remains separate from RTM generation",
        ]
    if frontier == "bounded_consolidation_or_remediation_sprint":
        return [
            "must name the concrete stale-doc, test, hostile-review, or gate failure being remediated",
            "must remain L0/L1 unless a separate exact authority envelope exists",
        ]
    return ["selected_frontier must be one current post-083 candidate"]


def _decision_evidence_errors(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["decision_evidence must be a dictionary"]
    required = (
        "next_logical_sprint_not_approval",
        "next_sprint_not_approval",
        "blk083_decision_package_not_publication_approval",
        "review_ready_not_runtime_authority",
        "fixture_ready_not_runtime_authority",
        "rtm_request_requires_publication_prerequisites",
    )
    return [f"decision_evidence.{key} must be true" for key in required if value.get(key) is not True]


def _required_marker_errors(path: str, value: Any, markers: tuple[str, ...]) -> list[str]:
    if not isinstance(value, list) or not value:
        return [f"{path} must be a non-empty list"]
    normalized_items = [str(item).casefold() for item in value]
    errors = []
    if len(value) != len(set(str(item) for item in value)):
        errors.append(f"{path} contains duplicate markers")
    for marker in markers:
        if not any(marker.casefold() in item for item in normalized_items):
            errors.append(f"{path} missing required marker {marker!r}")
    return errors


def _required_set_errors(path: str, value: Any, required: frozenset[str]) -> list[str]:
    if not isinstance(value, list):
        return [f"{path} must be a list"]
    if len(value) != len(set(value)):
        return [f"{path} contains duplicate entries"]
    actual = set(value)
    errors = [f"{path} missing {item}" for item in sorted(required - actual)]
    errors.extend(f"{path} extra {item}" for item in sorted(actual - required))
    return errors


def _authority_laundering_errors(value: Any, path: str = "record") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key)
            child_path = f"{path}.{key_text}"
            normalized_key = _compact(key_text)
            if path != "record" and ("frontier" in normalized_key or "selected" in normalized_key):
                errors.append(f"nested frontier selection at {child_path}: {key_text}")
            if path != "record" and key_text in DENIED_FLAGS:
                errors.append(f"forbidden nested denied authority key at {child_path}: {key_text}")
            if key_text not in ALLOWED_SUSPICIOUS_KEYS and any(term in normalized_key for term in SUSPICIOUS_KEY_TERMS):
                errors.append(f"forbidden authority-like key at {child_path}: {key_text}")
            if isinstance(child, str):
                errors.extend(_split_key_value_laundering_errors(key_text, child, child_path))
            if key_text not in ALLOWED_SUSPICIOUS_KEYS:
                errors.extend(_string_laundering_errors(key_text, child_path))
            errors.extend(_authority_laundering_errors(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            if isinstance(child, str) and child in ALLOWED_FRONTIERS and path != "record.selected_frontier":
                errors.append(f"nested frontier selection at {path}[{index}]: {child}")
            errors.extend(_authority_laundering_errors(child, f"{path}[{index}]"))
    elif isinstance(value, str):
        if value in ALLOWED_FRONTIERS and path != "record.selected_frontier":
            errors.append(f"nested frontier selection at {path}: {value}")
        if _safe_to_scan_string_path(path):
            errors.extend(_string_laundering_errors(value, path))
    return errors


def _split_key_value_laundering_errors(key: str, value: str, path: str) -> list[str]:
    normalized_key = _compact(key)
    normalized_values = [_compact(text) for text in _decoded_variants(value)]
    authority_key_terms = (
        "runtime",
        "live",
        "execution",
        "transport",
        "pilot",
        "publication",
        "publish",
        "generation",
        "drift",
        "protectedbody",
        "bodyread",
        "package",
        "network",
        "model",
        "browser",
        "cyber",
        "sandbox",
        "isolation",
        "targetrepo",
        "mutation",
        "signer",
        "ledger",
        "storage",
        "rollback",
    )
    positive_value_terms = ("approved", "authorized", "allowed", "granted", "claimed", "greenlit")
    if any(term in normalized_key for term in authority_key_terms) and any(
        any(term in variant for term in positive_value_terms) for variant in normalized_values
    ):
        return [f"split key/value authority laundering at {path}: {key}={value}"]
    return []


def _string_laundering_errors(value: str, path: str) -> list[str]:
    findings = []
    for decoded in _decoded_variants(value):
        compact = _compact(decoded)
        for marker in FORBIDDEN_COMPACT_MARKERS:
            if marker in compact:
                findings.append(f"forbidden authority wording at {path}: {value}")
                break
        if findings and findings[-1].endswith(f": {value}"):
            continue
        if _negative_only(decoded):
            continue
        positive_terms = ("approved", "authorized", "allowed", "granted", "greenlit")
        runtime_terms = (
            "runtime",
            "live",
            "execution",
            "execute",
            "transport",
            "pilot",
            "publication",
            "publish",
            "generation",
            "drift",
            "signing",
            "ledger",
            "storage",
            "rollback",
            "protected",
            "targetrepo",
            "mutation",
            "scan",
        )
        if any(term in compact for term in positive_terms) and any(term in compact for term in runtime_terms):
            findings.append(f"forbidden authority wording at {path}: {value}")
    return _unique(findings)


def _safe_to_scan_string_path(path: str) -> bool:
    skipped_prefixes = (
        "record.excluded_adjacent_authorities[",
        "record.required_future_approval_fields[",
        "record.hostile_review_checklist[",
        "record.frontier_prerequisites[",
        "record.governing_docs[",
    )
    skipped_exact = {
        "record.review_status",
        "record.selection_status",
        "record.maturity",
        "record.roadmap_source",
        "record.current_state_source",
        "record.post083_source",
        "record.selected_frontier",
        "record.selection_id",
    }
    return path not in skipped_exact and not any(path.startswith(prefix) for prefix in skipped_prefixes)


def _negative_only(text: str) -> bool:
    folded = text.casefold()
    compact = _compact(text)
    if any(marker in compact for marker in ("approvedfor", "authorizedfor", "greenlit", "allowedto", "granted")):
        return False
    return (
        "not approval" in folded
        or "not authority" in folded
        or "not runtime" in folded
        or "not execution" in folded
        or "required" in folded
        or "requires" in folded
        or "forbidden" in folded
        or "disabled" in folded
        or "no " in folded
    )


def _decoded_variants(text: str) -> list[str]:
    variants = [text]
    current = text
    for _ in range(5):
        decoded = _percent_decode_once(current)
        if decoded == current:
            break
        variants.append(decoded)
        current = decoded
    return variants


def _percent_decode_once(text: str) -> str:
    out: list[str] = []
    index = 0
    hexdigits = "0123456789abcdefABCDEF"
    while index < len(text):
        if (
            text[index] == "%"
            and index + 2 < len(text)
            and text[index + 1] in hexdigits
            and text[index + 2] in hexdigits
        ):
            out.append(chr(int(text[index + 1 : index + 3], 16)))
            index += 3
        else:
            out.append(text[index])
            index += 1
    return "".join(out)


def _compact(text: str) -> str:
    return "".join(ch for ch in text.casefold() if ch.isalnum())


def _unique(items: list[str]) -> list[str]:
    seen = set()
    unique_items = []
    for item in items:
        if item not in seen:
            unique_items.append(item)
            seen.add(item)
    return unique_items
