import copy
import unittest

from authoritative_beo_publication_authority_request import _canonical_hash
from exact_local_rtm_generation_pilot import build_exact_local_rtm_generation_pilot
from test_exact_local_rtm_generation_pilot import valid_inputs as valid_generation_inputs

from rtm_drift_rejection_authority_request import (
    AUTHORITY_REQUEST_PACKAGE_ID,
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY,
    REQUEST_SCOPE,
    REQUEST_STATUS,
    SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS,
    build_rtm_drift_rejection_authority_request,
)


def valid_inputs():
    approval_package, execution_request = valid_generation_inputs()
    generation_package = build_exact_local_rtm_generation_pilot(approval_package, execution_request)
    drift_request = {
        "authority_request_package_id": AUTHORITY_REQUEST_PACKAGE_ID,
        "operator_identity": generation_package["operator_identity"],
        "request_scope": REQUEST_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_rtm_generation_package_id": generation_package["execution_package_id"],
        "upstream_rtm_generation_package_hash": generation_package["execution_package_hash"],
        "rtm_id": generation_package["rtm_id"],
        "rtm_ledger_hash": generation_package["rtm_ledger_hash"],
        "beo_id": generation_package["beo_id"],
        "beo_hash": generation_package["beo_hash"],
        "target_id": generation_package["target_id"],
        "target_ref": generation_package["target_ref"],
        "request_future_exact_drift_rejection_authority": True,
        "human_drift_rejection_approval_granted": False,
        "requested_at": "2099-05-12T16:55:00+10:00",
        "expires_at": "2099-05-12T17:55:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {
            "exact_blk090_rtm_generation_package_reviewed": True,
            "local_rtm_ledger_evidence_bound": True,
            "drift_rejection_is_requested_for_future_review_not_granted": True,
            "no_drift_rejection_or_drift_decision_performed": True,
            "protected_body_reads_excluded": True,
            "external_ledger_and_signer_storage_side_effects_excluded": True,
            "target_repo_scan_or_mutation_excluded": True,
            "no_adjacent_runtime_side_effects": True,
        },
        **{flag: False for flag in SIDE_EFFECT_FLAGS},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    return generation_package, drift_request


class RtmDriftRejectionAuthorityRequestTest(unittest.TestCase):
    def test_builds_request_only_package_bound_to_local_rtm_generation_evidence(self):
        generation_package, drift_request = valid_inputs()

        package = build_rtm_drift_rejection_authority_request(generation_package, drift_request)

        self.assertEqual(package["request_status"], REQUEST_STATUS)
        self.assertEqual(package["authority_request_package_id"], AUTHORITY_REQUEST_PACKAGE_ID)
        self.assertEqual(package["request_scope"], REQUEST_SCOPE)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["upstream_rtm_generation_package_id"], generation_package["execution_package_id"])
        self.assertEqual(package["upstream_rtm_generation_package_hash"], generation_package["execution_package_hash"])
        self.assertEqual(package["rtm_id"], generation_package["rtm_id"])
        self.assertEqual(package["rtm_ledger_hash"], generation_package["rtm_ledger_hash"])
        self.assertEqual(package["drift_rejection_authority"], "DRIFT_REJECTION_REQUEST_ONLY_NOT_GRANTED")
        self.assertEqual(package["next_required_authority"], NEXT_REQUIRED_AUTHORITY)
        self.assertFalse(package["human_drift_rejection_approval_granted"])
        self.assertTrue(package["request_future_exact_drift_rejection_authority"])
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(
            package["authority_request_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "authority_request_package_hash"}),
        )

    def test_rejects_forged_or_non_local_rtm_generation_upstream_package(self):
        generation_package, drift_request = valid_inputs()

        forged = copy.deepcopy(generation_package)
        forged["rtm_ledger_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "execution_package_hash does not match submitted BLK-090 package"):
            build_rtm_drift_rejection_authority_request(forged, drift_request)

        forged = copy.deepcopy(generation_package)
        forged["drift_decision_made"] = True
        forged["execution_package_hash"] = _canonical_hash(
            {key: value for key, value in forged.items() if key != "execution_package_hash"}
        )
        request = copy.deepcopy(drift_request)
        request["upstream_rtm_generation_package_hash"] = forged["execution_package_hash"]
        with self.assertRaisesRegex(ValueError, "BLK-090 package must not already make drift decisions"):
            build_rtm_drift_rejection_authority_request(forged, request)

        forged = copy.deepcopy(generation_package)
        forged["extra_drift_rejection_authority"] = "drift rejection approved"
        forged["execution_package_hash"] = _canonical_hash(
            {key: value for key, value in forged.items() if key != "execution_package_hash"}
        )
        request = copy.deepcopy(drift_request)
        request["upstream_rtm_generation_package_hash"] = forged["execution_package_hash"]
        with self.assertRaisesRegex(ValueError, "generation_package contains forbidden authority field"):
            build_rtm_drift_rejection_authority_request(forged, request)

        forged = copy.deepcopy(generation_package)
        forged["local_rtm_ledger"]["protected_body_reads"] = True
        forged["local_rtm_ledger"]["drift_rejection_authorized"] = True
        forged["local_rtm_ledger"]["drift_review_state"] = "DRIFT_REJECTED"
        forged["local_rtm_ledger"]["rtm_ledger_hash"] = _canonical_hash(
            {key: value for key, value in forged["local_rtm_ledger"].items() if key != "rtm_ledger_hash"}
        )
        forged["rtm_ledger_hash"] = forged["local_rtm_ledger"]["rtm_ledger_hash"]
        forged["execution_package_hash"] = _canonical_hash(
            {key: value for key, value in forged.items() if key != "execution_package_hash"}
        )
        request = copy.deepcopy(drift_request)
        request["upstream_rtm_generation_package_hash"] = forged["execution_package_hash"]
        request["rtm_ledger_hash"] = forged["rtm_ledger_hash"]
        with self.assertRaisesRegex(ValueError, "local_rtm_ledger must remain no-drift no-protected-body evidence"):
            build_rtm_drift_rejection_authority_request(forged, request)

    def test_rejects_request_approval_replay_expiry_side_effects_and_retargeting(self):
        generation_package, drift_request = valid_inputs()
        cases = [
            ({"request_scope": "DRIFT_REJECTION_APPROVED"}, "request_scope must be"),
            ({"selected_frontier": "rtm_drift_rejection_execution"}, "selected_frontier must be"),
            ({"upstream_rtm_generation_package_id": "RTM-GENERATION-PILOT-EXECUTION-OTHER"}, "upstream_rtm_generation_package_id must match"),
            ({"upstream_rtm_generation_package_hash": "sha256:" + "0" * 64}, "upstream_rtm_generation_package_hash must match"),
            ({"rtm_ledger_hash": "sha256:" + "0" * 64}, "rtm_ledger_hash must match"),
            ({"request_future_exact_drift_rejection_authority": False}, "request_future_exact_drift_rejection_authority must be true"),
            ({"human_drift_rejection_approval_granted": True}, "human_drift_rejection_approval_granted must remain false"),
            ({"expired": True}, "drift rejection authority request must not be expired"),
            ({"replayed": True}, "drift rejection authority request must not be replayed"),
            ({"stale": True}, "drift rejection authority request must not be stale"),
            ({"expires_at": drift_request["requested_at"]}, "expires_at must be after requested_at"),
        ]
        for patch, message in cases:
            request = copy.deepcopy(drift_request)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_rtm_drift_rejection_authority_request(generation_package, request)

        for flag in SIDE_EFFECT_FLAGS:
            request = copy.deepcopy(drift_request)
            request[flag] = True
            with self.subTest(flag=flag):
                with self.assertRaisesRegex(ValueError, f"{flag} must remain false"):
                    build_rtm_drift_rejection_authority_request(generation_package, request)

    def test_rejects_exact_set_drift_extra_fields_and_laundering_text(self):
        generation_package, drift_request = valid_inputs()
        cases = [
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS) + [sorted(EXACT_PROOF_OBLIGATIONS)[0]]}, "proof_obligations must not contain duplicates"),
            ({"excluded_authorities": ["PROTECTED_BLK_REQ_BODY_READ"]}, "excluded_authorities must match exact denied authority set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES) + [sorted(EXACT_EXCLUDED_AUTHORITIES)[0]]}, "excluded_authorities must not contain duplicates"),
            ({"operator_identity": "discord:684235178083745819/driftRejectionApproved"}, "operator_identity contains authority-laundering text"),
            ({"operator_identity": "discord:684235178083745819/docs%252Factive"}, "operator_identity contains authority-laundering text"),
            ({"notes": "drift rejection approved and protected body read"}, "drift_rejection_request contains unexpected field"),
        ]
        for patch, message in cases:
            request = copy.deepcopy(drift_request)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_rtm_drift_rejection_authority_request(generation_package, request)

    def test_returned_package_defensively_copies_nested_hash_bound_inputs(self):
        generation_package, drift_request = valid_inputs()

        package = build_rtm_drift_rejection_authority_request(generation_package, drift_request)
        generation_package["local_rtm_ledger"]["drift_review_state"] = "DRIFT_REJECTED_AFTER_HASH"
        drift_request["operator_attestation"]["local_rtm_ledger_evidence_bound"] = "mutated"

        self.assertIsNot(package["local_rtm_ledger"], generation_package["local_rtm_ledger"])
        self.assertEqual(package["local_rtm_ledger"]["drift_review_state"], "DRIFT_REVIEW_REQUIRED_NOT_REJECTED")
        self.assertIs(package["operator_attestation"]["local_rtm_ledger_evidence_bound"], True)
