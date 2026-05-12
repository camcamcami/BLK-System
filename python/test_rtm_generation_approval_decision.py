import copy
import unittest

from authoritative_beo_publication_authority_request import _canonical_hash
from rtm_authority_request_after_beo_pilot import build_rtm_authority_request_after_beo_pilot
from test_rtm_authority_request_after_beo_pilot import valid_inputs as valid_request_inputs

from rtm_generation_approval_decision import (
    APPROVAL_DECISION_PACKAGE_ID,
    APPROVAL_ID,
    DECISION_RESULT,
    DECISION_SCOPE,
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    FUTURE_RUN_ID,
    NEXT_REQUIRED_AUTHORITY,
    SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS,
    STATUS,
    build_rtm_generation_approval_decision,
)


def valid_inputs():
    execution_package, authority_request = valid_request_inputs()
    request_package = build_rtm_authority_request_after_beo_pilot(execution_package, authority_request)
    approval_decision = {
        "approval_decision_package_id": APPROVAL_DECISION_PACKAGE_ID,
        "operator_identity": request_package["operator_identity"],
        "decision_scope": DECISION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_authority_request_package_id": request_package["authority_request_package_id"],
        "upstream_authority_request_package_hash": request_package["authority_request_package_hash"],
        "approval_id": APPROVAL_ID,
        "future_run_id": FUTURE_RUN_ID,
        "decision_result": DECISION_RESULT,
        "decided_at": "2099-05-12T16:00:00+10:00",
        "expires_at": "2099-05-12T17:00:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {
            "exact_blk088_request_reviewed": True,
            "approval_limited_to_one_future_local_rtm_generation_pilot": True,
            "rtm_not_generated_by_this_decision": True,
            "drift_rejection_excluded": True,
            "protected_body_reads_excluded": True,
            "signer_storage_ledger_rollback_side_effects_excluded": True,
            "target_repo_scan_or_mutation_excluded": True,
            "no_adjacent_runtime_side_effects": True,
        },
        **{flag: False for flag in SIDE_EFFECT_FLAGS},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    return request_package, approval_decision


class RtmGenerationApprovalDecisionTest(unittest.TestCase):
    def test_builds_exact_approval_decision_without_generating_rtm(self):
        request_package, approval_decision = valid_inputs()

        package = build_rtm_generation_approval_decision(request_package, approval_decision)

        self.assertEqual(package["approval_decision_status"], STATUS)
        self.assertEqual(package["approval_decision_package_id"], APPROVAL_DECISION_PACKAGE_ID)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["decision_scope"], DECISION_SCOPE)
        self.assertEqual(package["decision_result"], DECISION_RESULT)
        self.assertEqual(package["upstream_authority_request_package_id"], request_package["authority_request_package_id"])
        self.assertEqual(package["upstream_authority_request_package_hash"], request_package["authority_request_package_hash"])
        self.assertEqual(package["approval_id"], APPROVAL_ID)
        self.assertEqual(package["future_run_id"], FUTURE_RUN_ID)
        self.assertTrue(package["approval_decision_captured"])
        self.assertTrue(package["human_rtm_generation_approval_granted"])
        self.assertTrue(package["future_local_rtm_generation_pilot_approved"])
        self.assertFalse(package["rtm_generated"])
        self.assertEqual(package["rtm_status"], "APPROVAL_DECISION_CAPTURED_NOT_GENERATED")
        self.assertEqual(package["next_required_authority"], NEXT_REQUIRED_AUTHORITY)
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(
            package["approval_decision_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "approval_decision_package_hash"}),
        )

    def test_rejects_forged_or_non_request_upstream_package(self):
        request_package, approval_decision = valid_inputs()

        forged = copy.deepcopy(request_package)
        forged["rtm_authority"] = "REQUEST_ONLY_NOT_GRANTED_BUT_TAMPERED"
        with self.assertRaisesRegex(ValueError, "authority_request_package_hash does not match submitted BLK-088 package"):
            build_rtm_generation_approval_decision(forged, approval_decision)

        forged = copy.deepcopy(request_package)
        forged["rtm_status"] = "GENERATED"
        forged["authority_request_package_hash"] = _canonical_hash(
            {key: value for key, value in forged.items() if key != "authority_request_package_hash"}
        )
        decision = copy.deepcopy(approval_decision)
        decision["upstream_authority_request_package_hash"] = forged["authority_request_package_hash"]
        with self.assertRaisesRegex(ValueError, "BLK-088 request must remain not generated"):
            build_rtm_generation_approval_decision(forged, decision)

        forged = copy.deepcopy(request_package)
        forged["extra_drift_rejection_authority"] = "DRIFT_REJECTION_APPROVED"
        forged["authority_request_package_hash"] = _canonical_hash(
            {key: value for key, value in forged.items() if key != "authority_request_package_hash"}
        )
        decision = copy.deepcopy(approval_decision)
        decision["upstream_authority_request_package_hash"] = forged["authority_request_package_hash"]
        with self.assertRaisesRegex(ValueError, "request_package contains forbidden authority field"):
            build_rtm_generation_approval_decision(forged, decision)

    def test_rejects_scope_retargeting_replay_expiry_and_side_effects(self):
        request_package, approval_decision = valid_inputs()
        cases = [
            ({"decision_scope": "RTM_GENERATION_EXECUTION"}, "decision_scope must be"),
            ({"selected_frontier": "rtm_generation_pilot_execution"}, "selected_frontier must be"),
            ({"upstream_authority_request_package_id": "RTM-AUTHORITY-REQUEST-AFTER-BEO-PILOT-OTHER"}, "upstream_authority_request_package_id must match"),
            ({"upstream_authority_request_package_hash": "sha256:" + "0" * 64}, "upstream_authority_request_package_hash must match"),
            ({"approval_id": request_package["authority_request_package_id"]}, "approval_id must be fresh"),
            ({"future_run_id": request_package["authority_request_package_id"]}, "future_run_id must be fresh"),
            ({"decision_result": "APPROVED_FOR_RUNTIME_RTM_GENERATION_NOW"}, "decision_result must be"),
            ({"expired": True}, "approval decision must not be expired"),
            ({"replayed": True}, "approval decision must not be replayed"),
            ({"stale": True}, "approval decision must not be stale"),
            ({"expires_at": approval_decision["decided_at"]}, "expires_at must be after decided_at"),
            ({"decided_at": "2000-01-01T00:00:00+10:00", "expires_at": "2000-01-01T01:00:00+10:00"}, "approval decision must not be calendar-expired"),
        ]
        for patch, message in cases:
            decision = copy.deepcopy(approval_decision)
            decision.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_rtm_generation_approval_decision(request_package, decision)

        for flag in SIDE_EFFECT_FLAGS:
            decision = copy.deepcopy(approval_decision)
            decision[flag] = True
            with self.subTest(flag=flag):
                with self.assertRaisesRegex(ValueError, f"{flag} must remain false"):
                    build_rtm_generation_approval_decision(request_package, decision)

    def test_rejects_exact_set_drift_extra_fields_and_laundering_text(self):
        request_package, approval_decision = valid_inputs()
        cases = [
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS) + [sorted(EXACT_PROOF_OBLIGATIONS)[0]]}, "proof_obligations must not contain duplicates"),
            ({"excluded_authorities": ["RTM_DRIFT_REJECTION"]}, "excluded_authorities must match exact denied authority set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES) + [sorted(EXACT_EXCLUDED_AUTHORITIES)[0]]}, "excluded_authorities must not contain duplicates"),
            ({"operator_identity": "discord:684235178083745819/RTMGenerated"}, "operator_identity contains authority-laundering text"),
            ({"operator_identity": "discord:684235178083745819/%64rift%52ejection"}, "operator_identity contains authority-laundering text"),
            ({"operator_identity": "discord:684235178083745819/docs%252Factive"}, "operator_identity contains authority-laundering text"),
            ({"notes": "RTM generated and drift rejection authorized"}, "approval_decision contains unexpected field"),
        ]
        for patch, message in cases:
            decision = copy.deepcopy(approval_decision)
            decision.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_rtm_generation_approval_decision(request_package, decision)

    def test_returned_package_defensively_copies_nested_attestation(self):
        request_package, approval_decision = valid_inputs()

        package = build_rtm_generation_approval_decision(request_package, approval_decision)
        approval_decision["operator_attestation"]["rtm_not_generated_by_this_decision"] = "mutated"

        self.assertIsNot(package["operator_attestation"], approval_decision["operator_attestation"])
        self.assertIs(package["operator_attestation"]["rtm_not_generated_by_this_decision"], True)
