import copy
import unittest

from authoritative_beo_publication_authority_request import _canonical_hash
from rtm_generation_approval_decision import build_rtm_generation_approval_decision
from test_rtm_generation_approval_decision import valid_inputs as valid_approval_inputs

from exact_local_rtm_generation_pilot import (
    EXECUTION_PACKAGE_ID,
    EXECUTION_SCOPE,
    EXECUTION_STATUS,
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY,
    RTM_ID,
    RUN_ID_CONSUMED,
    SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS,
    build_exact_local_rtm_generation_pilot,
)


def valid_inputs():
    request_package, approval_decision = valid_approval_inputs()
    approval_package = build_rtm_generation_approval_decision(request_package, approval_decision)
    execution_request = {
        "execution_package_id": EXECUTION_PACKAGE_ID,
        "operator_identity": approval_package["operator_identity"],
        "execution_scope": EXECUTION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "approval_decision_package_id": approval_package["approval_decision_package_id"],
        "approval_decision_package_hash": approval_package["approval_decision_package_hash"],
        "approval_id": approval_package["approval_id"],
        "run_id_to_consume": RUN_ID_CONSUMED,
        "rtm_id": RTM_ID,
        "requested_at": "2099-05-12T16:10:00+10:00",
        "expires_at": "2099-05-12T16:50:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {
            "exact_blk089_approval_reviewed": True,
            "run_id_consumed_once_for_local_rtm_generation": True,
            "local_rtm_generation_only_not_external_ledger": True,
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
    return approval_package, execution_request


class ExactLocalRtmGenerationPilotTest(unittest.TestCase):
    def test_generates_local_rtm_ledger_bound_to_exact_blk089_approval(self):
        approval_package, execution_request = valid_inputs()

        package = build_exact_local_rtm_generation_pilot(approval_package, execution_request)

        self.assertEqual(package["execution_status"], EXECUTION_STATUS)
        self.assertEqual(package["execution_package_id"], EXECUTION_PACKAGE_ID)
        self.assertEqual(package["execution_scope"], EXECUTION_SCOPE)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["approval_decision_package_id"], approval_package["approval_decision_package_id"])
        self.assertEqual(package["approval_decision_package_hash"], approval_package["approval_decision_package_hash"])
        self.assertEqual(package["approval_id"], approval_package["approval_id"])
        self.assertEqual(package["run_id_consumed"], RUN_ID_CONSUMED)
        self.assertTrue(package["future_run_id_consumed"])
        self.assertEqual(package["rtm_id"], RTM_ID)
        self.assertEqual(package["rtm_status"], "PILOT_LOCAL_RTM_LEDGER_GENERATED_NOT_AUTHORITATIVE")
        self.assertEqual(package["rtm_authority"], "EXACT_LOCAL_PILOT_ONLY")
        self.assertEqual(package["next_required_authority"], NEXT_REQUIRED_AUTHORITY)
        self.assertEqual(package["local_rtm_ledger"]["rtm_id"], RTM_ID)
        self.assertEqual(package["local_rtm_ledger"]["beo_id"], approval_package["beo_id"])
        self.assertEqual(package["local_rtm_ledger"]["beo_hash"], approval_package["beo_hash"])
        self.assertEqual(package["local_rtm_ledger"]["trace_artifacts"], approval_package["trace_artifacts"])
        self.assertIn("rtm_ledger_hash", package["local_rtm_ledger"])
        self.assertEqual(package["rtm_ledger_hash"], package["local_rtm_ledger"]["rtm_ledger_hash"])
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(
            package["execution_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "execution_package_hash"}),
        )

    def test_rejects_forged_or_non_approval_upstream_package(self):
        approval_package, execution_request = valid_inputs()

        forged = copy.deepcopy(approval_package)
        forged["rtm_status"] = "APPROVAL_DECISION_CAPTURED_NOT_GENERATED_BUT_TAMPERED"
        with self.assertRaisesRegex(ValueError, "approval_decision_package_hash does not match submitted BLK-089 package"):
            build_exact_local_rtm_generation_pilot(forged, execution_request)

        forged = copy.deepcopy(approval_package)
        forged["rtm_generated"] = True
        forged["approval_decision_package_hash"] = _canonical_hash(
            {key: value for key, value in forged.items() if key != "approval_decision_package_hash"}
        )
        request = copy.deepcopy(execution_request)
        request["approval_decision_package_hash"] = forged["approval_decision_package_hash"]
        with self.assertRaisesRegex(ValueError, "BLK-089 approval decision must not already generate RTM"):
            build_exact_local_rtm_generation_pilot(forged, request)

        forged = copy.deepcopy(approval_package)
        forged["extra_protected_body_read_authority"] = "protected body read allowed"
        forged["approval_decision_package_hash"] = _canonical_hash(
            {key: value for key, value in forged.items() if key != "approval_decision_package_hash"}
        )
        request = copy.deepcopy(execution_request)
        request["approval_decision_package_hash"] = forged["approval_decision_package_hash"]
        with self.assertRaisesRegex(ValueError, "approval_package contains forbidden authority field"):
            build_exact_local_rtm_generation_pilot(forged, request)

        forged = copy.deepcopy(approval_package)
        forged["proof_obligations"] = []
        forged["approval_decision_package_hash"] = _canonical_hash(
            {key: value for key, value in forged.items() if key != "approval_decision_package_hash"}
        )
        request = copy.deepcopy(execution_request)
        request["approval_decision_package_hash"] = forged["approval_decision_package_hash"]
        with self.assertRaisesRegex(ValueError, "approval_package proof_obligations must match exact set"):
            build_exact_local_rtm_generation_pilot(forged, request)

        forged = copy.deepcopy(approval_package)
        forged["excluded_authorities"] = []
        forged["approval_decision_package_hash"] = _canonical_hash(
            {key: value for key, value in forged.items() if key != "approval_decision_package_hash"}
        )
        request = copy.deepcopy(execution_request)
        request["approval_decision_package_hash"] = forged["approval_decision_package_hash"]
        with self.assertRaisesRegex(ValueError, "approval_package excluded_authorities must match exact set"):
            build_exact_local_rtm_generation_pilot(forged, request)

    def test_rejects_interval_retargeting_replay_and_side_effects(self):
        approval_package, execution_request = valid_inputs()
        cases = [
            ({"execution_scope": "RTM_GENERATION_EXTERNAL_LEDGER"}, "execution_scope must be"),
            ({"selected_frontier": "rtm_drift_rejection"}, "selected_frontier must be"),
            ({"approval_decision_package_id": "RTM-GENERATION-APPROVAL-DECISION-OTHER"}, "approval_decision_package_id must match"),
            ({"approval_decision_package_hash": "sha256:" + "0" * 64}, "approval_decision_package_hash must match"),
            ({"run_id_to_consume": approval_package["approval_id"]}, "run_id_to_consume must match"),
            ({"rtm_id": "RTM-090-OTHER"}, "rtm_id must match"),
            ({"requested_at": "2099-05-12T15:59:59+10:00"}, "requested_at must not precede approval decision"),
            ({"requested_at": "2099-05-12T17:00:00+10:00"}, "requested_at must be before approval expiry"),
            ({"expires_at": "2099-05-12T17:01:00+10:00"}, "execution window must not exceed approval expiry"),
            ({"expired": True}, "execution request must not be expired"),
            ({"replayed": True}, "execution request must not be replayed"),
            ({"stale": True}, "execution request must not be stale"),
        ]
        for patch, message in cases:
            request = copy.deepcopy(execution_request)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_exact_local_rtm_generation_pilot(approval_package, request)

        for flag in SIDE_EFFECT_FLAGS:
            request = copy.deepcopy(execution_request)
            request[flag] = True
            with self.subTest(flag=flag):
                with self.assertRaisesRegex(ValueError, f"{flag} must remain false"):
                    build_exact_local_rtm_generation_pilot(approval_package, request)

    def test_rejects_exact_set_drift_extra_fields_and_laundering_text(self):
        approval_package, execution_request = valid_inputs()
        cases = [
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS) + [sorted(EXACT_PROOF_OBLIGATIONS)[0]]}, "proof_obligations must not contain duplicates"),
            ({"excluded_authorities": ["RTM_DRIFT_REJECTION"]}, "excluded_authorities must match exact denied authority set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES) + [sorted(EXACT_EXCLUDED_AUTHORITIES)[0]]}, "excluded_authorities must not contain duplicates"),
            ({"operator_identity": "discord:684235178083745819/driftRejection"}, "operator_identity contains authority-laundering text"),
            ({"operator_identity": "discord:684235178083745819/docs%252Factive"}, "operator_identity contains authority-laundering text"),
            ({"notes": "drift rejection authorized and public ledger appended"}, "execution_request contains unexpected field"),
        ]
        for patch, message in cases:
            request = copy.deepcopy(execution_request)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_exact_local_rtm_generation_pilot(approval_package, request)

    def test_returned_package_defensively_copies_nested_hash_bound_inputs(self):
        approval_package, execution_request = valid_inputs()

        package = build_exact_local_rtm_generation_pilot(approval_package, execution_request)
        approval_package["trace_artifacts"][0]["id"] = "REQ-DRIFT-LAUNDERED"
        execution_request["operator_attestation"]["local_rtm_generation_only_not_external_ledger"] = "mutated"

        self.assertIsNot(package["trace_artifacts"], approval_package["trace_artifacts"])
        self.assertIsNot(package["local_rtm_ledger"]["trace_artifacts"], approval_package["trace_artifacts"])
        self.assertEqual(package["trace_artifacts"][0]["id"], "REQ-001")
        self.assertIs(package["operator_attestation"]["local_rtm_generation_only_not_external_ledger"], True)
