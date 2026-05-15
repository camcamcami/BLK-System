from copy import deepcopy

from blk_authority_smuggling import scan_for_authority_laundering
from blk_current_state_authority_index import DENIED_FLAGS, evaluate_current_state_authority_index

READY = "AUTHORITY_RESUMPTION_PREFLIGHT_REVIEW_ONLY_NOT_APPROVAL"
BLOCKED = "AUTHORITY_RESUMPTION_PREFLIGHT_BLOCKED"
PREFLIGHT_ID = "AUTHORITY-RESUMPTION-PREFLIGHT-150-001"
CURRENT_FRONTIER = "NEXT_FRONTIER_POST_BEO_PUBLICATION_FINALITY_NO_AUTHORITY_RUNG_SELECTED"

TOP_LEVEL_KEYS = {
    "preflight_id",
    "preflight_status",
    "source_index_id",
    "source_index_evaluation",
    "current_frontier",
    "operator_decision_required_before_resumption",
    "selected_authority_rung",
    "candidate_authority_rungs",
    "required_evidence_before_selection",
    "side_effects",
    "evaluation",
    "validation_errors",
    *DENIED_FLAGS,
}

CANDIDATE_KEYS = {"rung", "status", "evidence_required"}
CANDIDATE_STATUS = "candidate_not_selected"
EXPECTED_SIDE_EFFECTS = {
    "approval_captured": False,
    "run_id_reserved": False,
    "run_id_consumed": False,
    "execution_attempted": False,
    "rtm_generated": False,
    "beo_published": False,
    "drift_rejected": False,
    "protected_body_accessed": False,
    "source_git_mutated": False,
    "signer_storage_ledger_touched": False,
}

DEFAULT_CANDIDATE_AUTHORITY_RUNGS = (
    {
        "rung": "continue_hardening_only",
        "status": CANDIDATE_STATUS,
        "evidence_required": [
            "operator states hardening remains the selected production posture",
            "proposed patch reduces authority misuse or documentation burden",
        ],
    },
    {
        "rung": "metadata_bound_rtm_or_blk_link_path",
        "status": CANDIDATE_STATUS,
        "evidence_required": [
            "explicit operator decision naming the exact RTM or blk-link scope",
            "fresh package hashes for any upstream reconciliation evidence",
            "separate denial of drift rejection, coverage truth, and protected-body access unless named",
        ],
    },
    {
        "rung": "beo_publication_or_closeout_path",
        "status": CANDIDATE_STATUS,
        "evidence_required": [
            "explicit operator decision naming publication or closeout scope",
            "signer/storage/ledger policy stated as denied unless separately named",
            "metadata-only prerequisite hashes without protected-body text",
        ],
    },
    {
        "rung": "codex_blk_pipe_or_blk_test_runtime_path",
        "status": CANDIDATE_STATUS,
        "evidence_required": [
            "explicit operator decision naming exact runtime entrypoint and target",
            "fresh allowlist for source/Git mutation, package, network, model, browser, and cyber surfaces",
            "proof that BLK-test remains a functional module, not repository test-suite authority",
        ],
    },
)

REQUIRED_EVIDENCE_BEFORE_SELECTION = (
    "current hardening-only index evaluates ready without granting authority",
    "operator explicitly names one future authority scope before any request, approval, or execution package",
    "all adjacent authorities remain denied unless the operator names them exactly",
    "protected requirement bodies remain isolated; metadata/hash evidence only",
    "one sprint closeout records any future authority movement",
)


def build_authority_resumption_preflight(*, current_index=None):
    source_index = evaluate_current_state_authority_index(current_index)
    record = {
        "preflight_id": PREFLIGHT_ID,
        "preflight_status": READY,
        "source_index_id": source_index.get("index_id"),
        "source_index_evaluation": source_index.get("evaluation"),
        "current_frontier": CURRENT_FRONTIER,
        "operator_decision_required_before_resumption": True,
        "selected_authority_rung": None,
        "candidate_authority_rungs": deepcopy(list(DEFAULT_CANDIDATE_AUTHORITY_RUNGS)),
        "required_evidence_before_selection": list(REQUIRED_EVIDENCE_BEFORE_SELECTION),
        "side_effects": deepcopy(EXPECTED_SIDE_EFFECTS),
        "evaluation": READY,
        "validation_errors": [],
    }
    for flag in DENIED_FLAGS:
        record[flag] = False
    return record


def validate_authority_resumption_preflight(record):
    errors = []
    if not isinstance(record, dict):
        return ["record must be a dictionary"]

    for key in sorted(set(record) - TOP_LEVEL_KEYS):
        errors.append(f"unsupported top-level key {key!r}")

    expected_scalars = {
        "preflight_id": PREFLIGHT_ID,
        "preflight_status": READY,
        "source_index_id": "blk_system_current_state_authority_index",
        "source_index_evaluation": "CURRENT_STATE_INDEX_READY_FOR_OPERATOR_REVIEW_NOT_AUTHORITY",
        "current_frontier": CURRENT_FRONTIER,
    }
    for key, expected in expected_scalars.items():
        if record.get(key) != expected:
            errors.append(f"{key} must be {expected!r}")

    if record.get("operator_decision_required_before_resumption") is not True:
        errors.append("operator_decision_required_before_resumption must remain true")
    if record.get("selected_authority_rung") is not None:
        errors.append("selected_authority_rung must remain null")
    if record.get("evaluation") not in {READY, BLOCKED, None}:
        errors.append("evaluation must be a preflight status")
    if "validation_errors" in record and not isinstance(record.get("validation_errors"), list):
        errors.append("validation_errors must be a list")

    for flag in DENIED_FLAGS:
        if record.get(flag) is not False:
            errors.append(f"{flag} must remain false")

    side_effects = record.get("side_effects")
    if side_effects != EXPECTED_SIDE_EFFECTS:
        errors.append("side_effects must match the exact no-side-effect contract")
        if isinstance(side_effects, dict):
            for key, expected in EXPECTED_SIDE_EFFECTS.items():
                if side_effects.get(key) is not expected:
                    errors.append(f"{key} must remain false")

    candidates = record.get("candidate_authority_rungs")
    if not isinstance(candidates, list) or not candidates:
        errors.append("candidate_authority_rungs must be a non-empty list")
        candidates = []
    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, dict):
            errors.append(f"candidate_authority_rungs[{index}] must be a dictionary")
            continue
        extra = sorted(set(candidate) - CANDIDATE_KEYS)
        for key in extra:
            errors.append(f"candidate_authority_rungs[{index}] has unsupported key {key!r}")
        if candidate.get("status") != CANDIDATE_STATUS:
            errors.append(f"candidate_authority_rungs[{index}].status must be {CANDIDATE_STATUS!r}")
        if not isinstance(candidate.get("rung"), str) or not candidate.get("rung"):
            errors.append(f"candidate_authority_rungs[{index}].rung must be a non-empty string")
        evidence = candidate.get("evidence_required")
        if not isinstance(evidence, list) or not evidence or not all(isinstance(item, str) and item for item in evidence):
            errors.append(f"candidate_authority_rungs[{index}].evidence_required must be a non-empty string list")

    required = record.get("required_evidence_before_selection")
    if not isinstance(required, list) or not required or not all(isinstance(item, str) and item for item in required):
        errors.append("required_evidence_before_selection must be a non-empty string list")

    scan_candidate = {k: v for k, v in record.items() if k not in DENIED_FLAGS and k != "validation_errors"}
    errors.extend(scan_for_authority_laundering(scan_candidate, denied_keys=DENIED_FLAGS))
    return errors


def evaluate_authority_resumption_preflight(record=None):
    candidate = build_authority_resumption_preflight() if record is None else deepcopy(record)
    errors = validate_authority_resumption_preflight(candidate)
    candidate["evaluation"] = BLOCKED if errors else READY
    candidate["validation_errors"] = errors
    for flag in DENIED_FLAGS:
        candidate[flag] = False
    return candidate
