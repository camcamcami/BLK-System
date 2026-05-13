import copy
import unittest

from authoritative_beo_publication_authority_request import _canonical_hash
from rtm_drift_rejection_approval_decision import build_rtm_drift_rejection_approval_decision
from test_rtm_drift_rejection_approval_decision import valid_inputs as valid_approval_inputs

from exact_local_rtm_drift_rejection_execution import (
    DRIFT_REJECTION_ID,
    DRIFT_REJECTION_RESULT,
    EXECUTION_PACKAGE_ID,
    EXECUTION_SCOPE,
    EXECUTION_STATUS,
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY,
    RUN_ID_CONSUMED,
    SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS,
    build_exact_local_rtm_drift_rejection_execution,
)


def valid_inputs():
    request_package, approval_decision = valid_approval_inputs()
    approval_package = build_rtm_drift_rejection_approval_decision(request_package, approval_decision)
    execution_request = {
        "execution_package_id": EXECUTION_PACKAGE_ID,
        "operator_identity": approval_package["operator_identity"],
        "execution_scope": EXECUTION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "approval_decision_package_id": approval_package["approval_decision_package_id"],
        "approval_decision_package_hash": approval_package["approval_decision_package_hash"],
        "approval_id": approval_package["approval_id"],
        "run_id_to_consume": approval_package["future_run_id"],
        "rtm_id": approval_package["rtm_id"],
        "requested_at": "2099-05-12T18:15:00+10:00",
        "expires_at": "2099-05-12T18:45:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {
            "exact_blk093_approval_reviewed": True,
            "run_id_consumed_once_for_local_drift_rejection": True,
            "local_drift_rejection_only_not_runtime_blk_link": True,
            "authoritative_drift_decision_excluded": True,
            "protected_body_reads_excluded": True,
            "active_vault_comparison_excluded": True,
            "external_ledger_and_signer_storage_side_effects_excluded": True,
            "target_repo_scan_or_mutation_excluded": True,
            "no_adjacent_runtime_side_effects": True,
        },
        **{flag: False for flag in SIDE_EFFECT_FLAGS},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    return approval_package, execution_request


def _rebind_ledger_and_approval_hash(approval_package, execution_request):
    approval_package["local_rtm_ledger"]["rtm_ledger_hash"] = _canonical_hash(
        {key: value for key, value in approval_package["local_rtm_ledger"].items() if key != "rtm_ledger_hash"}
    )
    approval_package["rtm_ledger_hash"] = approval_package["local_rtm_ledger"]["rtm_ledger_hash"]
    _rebind_approval_hash(approval_package, execution_request)


def _rebind_approval_hash(approval_package, execution_request):
    approval_package["approval_decision_package_hash"] = _canonical_hash(
        {key: value for key, value in approval_package.items() if key != "approval_decision_package_hash"}
    )
    execution_request["approval_decision_package_hash"] = approval_package["approval_decision_package_hash"]


class ExactLocalRtmDriftRejectionExecutionTest(unittest.TestCase):
    def test_builds_exact_local_drift_rejection_execution_without_authoritative_side_effects(self):
        approval_package, execution_request = valid_inputs()

        package = build_exact_local_rtm_drift_rejection_execution(approval_package, execution_request)

        self.assertEqual(package["execution_status"], EXECUTION_STATUS)
        self.assertEqual(package["execution_package_id"], EXECUTION_PACKAGE_ID)
        self.assertEqual(package["execution_scope"], EXECUTION_SCOPE)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["approval_decision_package_id"], approval_package["approval_decision_package_id"])
        self.assertEqual(package["approval_decision_package_hash"], approval_package["approval_decision_package_hash"])
        self.assertEqual(package["approval_id"], approval_package["approval_id"])
        self.assertEqual(package["run_id_consumed"], RUN_ID_CONSUMED)
        self.assertTrue(package["future_run_id_consumed"])
        self.assertTrue(package["local_rtm_drift_rejection_executed"])
        self.assertEqual(package["drift_rejection_result"], DRIFT_REJECTION_RESULT)
        self.assertEqual(package["next_required_authority"], NEXT_REQUIRED_AUTHORITY)
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)
        record = package["local_drift_rejection_record"]
        self.assertEqual(record["drift_rejection_id"], DRIFT_REJECTION_ID)
        self.assertEqual(record["drift_rejection_result"], DRIFT_REJECTION_RESULT)
        self.assertEqual(record["rtm_id"], approval_package["rtm_id"])
        self.assertEqual(record["rtm_ledger_hash"], approval_package["rtm_ledger_hash"])
        self.assertEqual(record["input_drift_review_state"], "DRIFT_REVIEW_REQUIRED_NOT_REJECTED")
        self.assertEqual(record["output_drift_review_state"], "LOCAL_DRIFT_REJECTION_RECORDED_NOT_AUTHORITATIVE")
        self.assertEqual(record["hash_binding_mode"], "LOCAL_HASH_ONLY_NO_PROTECTED_BODY_READS")
        self.assertIs(record["authoritative_drift_decision_made"], False)
        self.assertIs(record["active_vault_hash_comparison_performed"], False)
        self.assertIs(record["protected_body_reads"], False)
        self.assertIs(record["protected_body_hashing"], False)
        self.assertEqual(record["external_ledger_state"], "NOT_APPENDED_LOCAL_FIXTURE_ONLY")
        self.assertEqual(
            package["local_drift_rejection_record_hash"],
            _canonical_hash({key: value for key, value in record.items() if key != "local_drift_rejection_record_hash"}),
        )
        self.assertEqual(
            package["execution_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "execution_package_hash"}),
        )

    def test_rejects_forged_approval_consumed_run_and_polluted_ledger(self):
        approval_package, execution_request = valid_inputs()

        forged = copy.deepcopy(approval_package)
        forged["approval_decision_package_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "approval_decision_package_hash does not match submitted BLK-093 package"):
            build_exact_local_rtm_drift_rejection_execution(forged, execution_request)

        forged = copy.deepcopy(approval_package)
        forged["future_run_id_consumed"] = True
        forged["approval_decision_package_hash"] = _canonical_hash(
            {key: value for key, value in forged.items() if key != "approval_decision_package_hash"}
        )
        request = copy.deepcopy(execution_request)
        request["approval_decision_package_hash"] = forged["approval_decision_package_hash"]
        with self.assertRaisesRegex(ValueError, "BLK-093 approval future run ID must not be consumed yet"):
            build_exact_local_rtm_drift_rejection_execution(forged, request)

        forged = copy.deepcopy(approval_package)
        forged["local_rtm_ledger"]["drift_decision_made"] = True
        forged["local_rtm_ledger"]["rtm_ledger_hash"] = _canonical_hash(
            {key: value for key, value in forged["local_rtm_ledger"].items() if key != "rtm_ledger_hash"}
        )
        forged["rtm_ledger_hash"] = forged["local_rtm_ledger"]["rtm_ledger_hash"]
        forged["approval_decision_package_hash"] = _canonical_hash(
            {key: value for key, value in forged.items() if key != "approval_decision_package_hash"}
        )
        request = copy.deepcopy(execution_request)
        request["approval_decision_package_hash"] = forged["approval_decision_package_hash"]
        with self.assertRaisesRegex(ValueError, "local_rtm_ledger must remain pending local drift-review evidence"):
            build_exact_local_rtm_drift_rejection_execution(forged, request)

        forged = copy.deepcopy(approval_package)
        forged["excluded_authorities"] = ["PROTECTED_BLK_REQ_BODY_READ"]
        forged["approval_decision_package_hash"] = _canonical_hash(
            {key: value for key, value in forged.items() if key != "approval_decision_package_hash"}
        )
        request = copy.deepcopy(execution_request)
        request["approval_decision_package_hash"] = forged["approval_decision_package_hash"]
        with self.assertRaisesRegex(ValueError, "approval_package excluded_authorities must match exact set"):
            build_exact_local_rtm_drift_rejection_execution(forged, request)

    def test_rejects_replay_window_retargeting_and_side_effects(self):
        approval_package, execution_request = valid_inputs()
        cases = [
            ({"execution_scope": "RUNTIME_RTM_DRIFT_REJECTION"}, "execution_scope must be"),
            ({"selected_frontier": "runtime_blk_link_trace_closure"}, "selected_frontier must be"),
            ({"approval_decision_package_id": "RTM-DRIFT-REJECTION-APPROVAL-DECISION-OTHER"}, "approval_decision_package_id must match"),
            ({"approval_decision_package_hash": "sha256:" + "0" * 64}, "approval_decision_package_hash must match"),
            ({"approval_id": "APPROVAL-OTHER"}, "approval_id must match"),
            ({"run_id_to_consume": "RUN-OTHER"}, "run_id_to_consume must match approved BLK-093 future run ID"),
            ({"rtm_id": "RTM-OTHER"}, "rtm_id must match BLK-093 approval package"),
            ({"expired": True}, "execution request must not be expired"),
            ({"replayed": True}, "execution request must not be replayed"),
            ({"stale": True}, "execution request must not be stale"),
            ({"requested_at": "2099-05-12T17:59:59+10:00"}, "requested_at must not precede approval decision"),
            ({"requested_at": "2099-05-12T19:00:00+10:00", "expires_at": "2099-05-12T19:00:01+10:00"}, "requested_at must be before approval expiry"),
            ({"expires_at": "2099-05-12T19:00:01+10:00"}, "execution window must not exceed approval expiry"),
            ({"expires_at": "2099-05-12T18:15:00+10:00"}, "expires_at must be after requested_at"),
        ]
        for patch, message in cases:
            request = copy.deepcopy(execution_request)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_exact_local_rtm_drift_rejection_execution(approval_package, request)

        for flag in SIDE_EFFECT_FLAGS:
            request = copy.deepcopy(execution_request)
            request[flag] = True
            with self.subTest(flag=flag):
                with self.assertRaisesRegex(ValueError, f"{flag} must remain false"):
                    build_exact_local_rtm_drift_rejection_execution(approval_package, request)

    def test_rejects_exact_set_drift_extra_fields_and_laundering_text(self):
        approval_package, execution_request = valid_inputs()
        cases = [
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS) + [sorted(EXACT_PROOF_OBLIGATIONS)[0]]}, "proof_obligations must not contain duplicates"),
            ({"excluded_authorities": ["PROTECTED_BLK_REQ_BODY_READ"]}, "excluded_authorities must match exact denied authority set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES) + [sorted(EXACT_EXCLUDED_AUTHORITIES)[0]]}, "excluded_authorities must not contain duplicates"),
            ({"operator_identity": "discord:684235178083745819/protectedBodyRead"}, "operator_identity contains authority-laundering text"),
            ({"operator_identity": "discord:684235178083745819/ActiveVaultHashComparison"}, "operator_identity contains authority-laundering text"),
            ({"operator_identity": "discord:684235178083745819/runtimeBlkLinkTraceClosure"}, "operator_identity contains authority-laundering text"),
            ({"operator_identity": "discord:684235178083745819/authoritativeDriftDecisionMade"}, "operator_identity contains authority-laundering text"),
            ({"notes": "external ledger mutation authorized"}, "execution_request contains unexpected field"),
        ]
        for patch, message in cases:
            request = copy.deepcopy(execution_request)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_exact_local_rtm_drift_rejection_execution(approval_package, request)

    def test_rejects_self_hashed_lookalike_approval_identity_and_upstream_fields(self):
        approval_package, execution_request = valid_inputs()
        cases = [
            ("upstream_authority_request_package_id", "RTM-DRIFT-REJECTION-AUTHORITY-REQUEST-OTHER"),
            ("upstream_authority_request_package_hash", "sha256:" + "1" * 64),
            ("upstream_rtm_generation_package_id", "RTM-GENERATION-PILOT-EXECUTION-OTHER"),
            ("upstream_rtm_generation_package_hash", "sha256:" + "2" * 64),
            ("operator_identity", "discord:999999999999999999"),
            ("rtm_id", "RTM-OTHER"),
            ("beo_id", "BEO-OTHER"),
            ("target_id", "TARGET-OTHER"),
        ]
        for key, value in cases:
            forged = copy.deepcopy(approval_package)
            request = copy.deepcopy(execution_request)
            forged[key] = value
            if key == "operator_identity":
                request["operator_identity"] = value
            if key == "rtm_id":
                forged["local_rtm_ledger"]["rtm_id"] = value
                request["rtm_id"] = value
                _rebind_ledger_and_approval_hash(forged, request)
            else:
                _rebind_approval_hash(forged, request)
            with self.subTest(key=key):
                with self.assertRaisesRegex(ValueError, "canonical BLK-093"):
                    build_exact_local_rtm_drift_rejection_execution(forged, request)

    def test_rejects_corrupt_approval_attestation_and_calendar_expiry(self):
        approval_package, execution_request = valid_inputs()

        forged = copy.deepcopy(approval_package)
        request = copy.deepcopy(execution_request)
        forged["operator_attestation"]["no_drift_decision_made_by_this_decision"] = False
        _rebind_approval_hash(forged, request)
        with self.assertRaisesRegex(ValueError, "approval_package.operator_attestation"):
            build_exact_local_rtm_drift_rejection_execution(forged, request)

        forged = copy.deepcopy(approval_package)
        request = copy.deepcopy(execution_request)
        forged["decided_at"] = "2000-05-12T18:00:00+10:00"
        forged["expires_at"] = "2000-05-12T19:00:00+10:00"
        request["requested_at"] = "2000-05-12T18:15:00+10:00"
        request["expires_at"] = "2000-05-12T18:45:00+10:00"
        _rebind_approval_hash(forged, request)
        with self.assertRaisesRegex(ValueError, "approval decision must not be calendar-expired"):
            build_exact_local_rtm_drift_rejection_execution(forged, request)

    def test_rejects_nested_local_rtm_ledger_laundering_and_bad_hashes(self):
        approval_package, execution_request = valid_inputs()
        cases = [
            ({"pilot_publication_artifact_hash": "not-a-hash"}, "pilot_publication_artifact_hash must be a sha256 hash"),
            ({"trace_artifacts": "external ledger mutation authorized"}, "trace_artifacts must be a list"),
            ({"trace_artifacts": [{"kind": "REQ", "id": "protectedBodyReadAuthorized", "version_hash": "sha256:" + "c" * 64}]}, "trace_artifacts\[0\].id contains authority-laundering text"),
            ({"trace_artifacts": [{"kind": "REQ", "id": "REQ-001", "version_hash": "not-a-hash"}]}, "trace_artifacts\[0\].version_hash must be a sha256 hash"),
        ]
        for patch, message in cases:
            forged = copy.deepcopy(approval_package)
            request = copy.deepcopy(execution_request)
            forged["local_rtm_ledger"].update(patch)
            _rebind_ledger_and_approval_hash(forged, request)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_exact_local_rtm_drift_rejection_execution(forged, request)

    def test_returned_package_defensively_copies_nested_hash_bound_inputs(self):
        approval_package, execution_request = valid_inputs()

        package = build_exact_local_rtm_drift_rejection_execution(approval_package, execution_request)
        approval_package["local_rtm_ledger"]["drift_review_state"] = "DRIFT_REJECTED_AFTER_HASH"
        execution_request["operator_attestation"]["local_drift_rejection_only_not_runtime_blk_link"] = "mutated"

        self.assertIsNot(package["local_rtm_ledger"], approval_package["local_rtm_ledger"])
        self.assertEqual(package["local_rtm_ledger"]["drift_review_state"], "DRIFT_REVIEW_REQUIRED_NOT_REJECTED")
        self.assertIs(package["operator_attestation"]["local_drift_rejection_only_not_runtime_blk_link"], True)
