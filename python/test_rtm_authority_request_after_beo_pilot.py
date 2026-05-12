import copy
import unittest

from authoritative_beo_publication_authority_request import _canonical_hash
from beo_publication_pilot_execution import build_beo_publication_pilot_execution
from test_beo_publication_pilot_execution import valid_inputs as valid_execution_inputs

from rtm_authority_request_after_beo_pilot import (
    AUTHORITY_REQUEST_PACKAGE_ID,
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY,
    REQUEST_SCOPE,
    REQUEST_STATUS,
    SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS,
    build_rtm_authority_request_after_beo_pilot,
)


def valid_inputs():
    approval_package, execution_request = valid_execution_inputs()
    execution_package = build_beo_publication_pilot_execution(approval_package, execution_request)
    authority_request = {
        "authority_request_package_id": AUTHORITY_REQUEST_PACKAGE_ID,
        "operator_identity": execution_package["operator_identity"],
        "request_scope": REQUEST_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_execution_package_id": execution_package["execution_package_id"],
        "upstream_execution_package_hash": execution_package["execution_package_hash"],
        "pilot_publication_artifact_hash": execution_package["pilot_publication_artifact_hash"],
        "beo_id": execution_package["beo_id"],
        "beo_hash": execution_package["beo_hash"],
        "target_id": execution_package["target_id"],
        "target_ref": execution_package["target_ref"],
        "request_future_exact_rtm_generation_authority": True,
        "human_rtm_approval_granted": False,
        "rtm_generation_authorized": False,
        "rtm_generated": False,
        "drift_rejection_authorized": False,
        "drift_decision_made": False,
        "active_vault_hash_comparison_performed": False,
        "coverage_matrix_created": False,
        "coverage_claim_promoted": False,
        "protected_body_reads": False,
        "authoritative_external_publication": False,
        "live_approval_capture_performed": False,
        "signer_key_material_access": False,
        "cryptographic_signing": False,
        "immutable_storage_write": False,
        "public_ledger_mutation": False,
        "rollback_revocation_supersession_execution": False,
        "target_repo_scan_or_mutation": False,
        "source_or_git_mutation_by_fixture": False,
        "beb_dispatch_authorized": False,
        "beo_closeout_execution_authorized": False,
        "blk_test_codex_blk_pipe_runtime": False,
        "package_network_model_browser_cyber_tooling": False,
        "production_isolation_claim": False,
        "requested_at": "2099-05-12T16:00:00+10:00",
        "expires_at": "2099-05-12T17:00:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {
            "exact_blk087_execution_package_reviewed": True,
            "local_pilot_artifact_is_not_external_authoritative_publication": True,
            "rtm_authority_is_requested_for_future_human_review_not_granted": True,
            "no_rtm_generation_or_drift_decision_performed": True,
            "no_active_vault_hash_comparison_or_coverage_claim": True,
            "protected_body_reads_excluded": True,
            "signer_storage_ledger_rollback_side_effects_excluded": True,
            "target_repo_scan_or_mutation_excluded": True,
            "no_adjacent_runtime_side_effects": True,
        },
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    return execution_package, authority_request


def rehash_execution_package(package):
    package["execution_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "execution_package_hash"}
    )
    return package


class RtmAuthorityRequestAfterBeoPilotTest(unittest.TestCase):
    def test_builds_request_only_package_bound_to_blk087_local_pilot_evidence(self):
        execution_package, authority_request = valid_inputs()

        package = build_rtm_authority_request_after_beo_pilot(execution_package, authority_request)

        self.assertEqual(package["request_status"], REQUEST_STATUS)
        self.assertEqual(package["authority_request_package_id"], AUTHORITY_REQUEST_PACKAGE_ID)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["request_scope"], REQUEST_SCOPE)
        self.assertEqual(package["upstream_execution_package_id"], execution_package["execution_package_id"])
        self.assertEqual(package["upstream_execution_package_hash"], execution_package["execution_package_hash"])
        self.assertEqual(package["pilot_publication_artifact_hash"], execution_package["pilot_publication_artifact_hash"])
        self.assertEqual(package["beo_id"], execution_package["beo_id"])
        self.assertEqual(package["beo_hash"], execution_package["beo_hash"])
        self.assertEqual(package["target_id"], execution_package["target_id"])
        self.assertEqual(package["target_ref"], execution_package["target_ref"])
        self.assertEqual(package["local_pilot_beo_publication"], "PILOT_LOCAL_PUBLISHED_BEO_OUTPUT_NOT_AUTHORITATIVE")
        self.assertEqual(package["requested_authority"], "FUTURE_EXACT_RTM_GENERATION_AUTHORITY_REQUESTED_FOR_HUMAN_REVIEW")
        self.assertTrue(package["human_rtm_approval_required"])
        self.assertFalse(package["human_rtm_approval_granted"])
        self.assertEqual(package["rtm_status"], "NOT_GENERATED")
        self.assertEqual(package["rtm_authority"], "REQUEST_ONLY_NOT_GRANTED")
        self.assertEqual(package["next_required_authority"], NEXT_REQUIRED_AUTHORITY)
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        self.assertIn("authority_request_package_hash", package)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)

    def test_rejects_forged_self_consistent_or_mismatched_blk087_execution_package(self):
        execution_package, authority_request = valid_inputs()

        forged = copy.deepcopy(execution_package)
        forged["pilot_publication_artifact"]["published_beo_id"] = "BEO-FORGED-088"
        with self.assertRaisesRegex(ValueError, "execution_package_hash does not match submitted BLK-087 package"):
            build_rtm_authority_request_after_beo_pilot(forged, authority_request)

        forged = copy.deepcopy(execution_package)
        forged["target_id"] = "BEO-PUBLICATION-TARGET-FORGED-088"
        forged["pilot_publication_artifact"]["target_id"] = forged["target_id"]
        forged["pilot_publication_artifact_hash"] = _canonical_hash(
            {
                key: value
                for key, value in forged["pilot_publication_artifact"].items()
                if key != "pilot_publication_artifact_hash"
            }
        )
        forged["pilot_publication_artifact"]["pilot_publication_artifact_hash"] = forged[
            "pilot_publication_artifact_hash"
        ]
        rehash_execution_package(forged)
        request = copy.deepcopy(authority_request)
        request["upstream_execution_package_hash"] = forged["execution_package_hash"]
        request["pilot_publication_artifact_hash"] = forged["pilot_publication_artifact_hash"]
        request["target_id"] = forged["target_id"]
        with self.assertRaisesRegex(ValueError, "BLK-087 execution package must match canonical local pilot fixture"):
            build_rtm_authority_request_after_beo_pilot(forged, request)

        forged = copy.deepcopy(execution_package)
        forged["rtm_status"] = "GENERATED"
        rehash_execution_package(forged)
        request = copy.deepcopy(authority_request)
        request["upstream_execution_package_hash"] = forged["execution_package_hash"]
        with self.assertRaisesRegex(ValueError, "BLK-087 package rtm_status must remain NOT_GENERATED"):
            build_rtm_authority_request_after_beo_pilot(forged, request)

    def test_rejects_request_side_effect_flags_approval_claims_bad_expiry_and_replay(self):
        execution_package, authority_request = valid_inputs()
        hostile_cases = [
            ({"selected_frontier": "rtm_generation"}, "selected_frontier must be"),
            ({"request_scope": "RTM_GENERATION_APPROVED_AFTER_BEO_PILOT"}, "request_scope must be"),
            ({"request_future_exact_rtm_generation_authority": False}, "request_future_exact_rtm_generation_authority must be true"),
            ({"human_rtm_approval_granted": True}, "human_rtm_approval_granted must remain false"),
            ({"rtm_generation_authorized": True}, "rtm_generation_authorized must remain false"),
            ({"rtm_generated": True}, "rtm_generated must remain false"),
            ({"drift_rejection_authorized": True}, "drift_rejection_authorized must remain false"),
            ({"drift_decision_made": True}, "drift_decision_made must remain false"),
            ({"active_vault_hash_comparison_performed": True}, "active_vault_hash_comparison_performed must remain false"),
            ({"coverage_matrix_created": True}, "coverage_matrix_created must remain false"),
            ({"protected_body_reads": True}, "protected_body_reads must remain false"),
            ({"authoritative_external_publication": True}, "authoritative_external_publication must remain false"),
            ({"signer_key_material_access": True}, "signer_key_material_access must remain false"),
            ({"beb_dispatch_authorized": True}, "beb_dispatch_authorized must remain false"),
            ({"beo_closeout_execution_authorized": True}, "beo_closeout_execution_authorized must remain false"),
            ({"expired": True}, "authority request must not be expired"),
            ({"replayed": True}, "authority request must not be replayed"),
            ({"stale": True}, "authority request must not be stale"),
            ({"expires_at": authority_request["requested_at"]}, "expires_at must be after requested_at"),
            ({"requested_at": "2000-01-01T00:00:00+10:00", "expires_at": "2000-01-01T01:00:00+10:00"}, "authority request must not be calendar-expired"),
        ]
        for patch, message in hostile_cases:
            request = copy.deepcopy(authority_request)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_rtm_authority_request_after_beo_pilot(execution_package, request)

    def test_rejects_exact_set_drift_duplicates_extra_fields_and_laundering_text(self):
        execution_package, authority_request = valid_inputs()
        hostile_cases = [
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS) + [sorted(EXACT_PROOF_OBLIGATIONS)[0]]}, "proof_obligations must not contain duplicates"),
            ({"excluded_authorities": ["RTM_GENERATION"]}, "excluded_authorities must match exact denied authority set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES) + [sorted(EXACT_EXCLUDED_AUTHORITIES)[0]]}, "excluded_authorities must not contain duplicates"),
            ({"rtm_authority": "APPROVED_FOR_LIVE_EXECUTION"}, "authority_request contains forbidden authority field"),
            ({"notes": "runtime pilot approved by operator; live pilot allowed"}, "authority_request contains unexpected field"),
            ({"operator_identity": "discord:684235178083745819/RTMGeneration"}, "operator_identity contains authority-laundering text"),
            ({"operator_identity": "discord:684235178083745819/%52%54%4dGenerated"}, "operator_identity contains authority-laundering text"),
            ({"operator_identity": "discord:684235178083745819/docs%252Factive"}, "operator_identity contains authority-laundering text"),
        ]
        for patch, message in hostile_cases:
            request = copy.deepcopy(authority_request)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_rtm_authority_request_after_beo_pilot(execution_package, request)

    def test_returned_package_defensively_copies_hash_bound_nested_inputs(self):
        execution_package, authority_request = valid_inputs()

        package = build_rtm_authority_request_after_beo_pilot(execution_package, authority_request)

        self.assertIsNot(package["trace_artifacts"], execution_package["trace_artifacts"])
        self.assertIsNot(package["trace_artifacts"][0], execution_package["trace_artifacts"][0])
        self.assertIsNot(package["pilot_publication_artifact"], execution_package["pilot_publication_artifact"])
        self.assertIsNot(package["operator_attestation"], authority_request["operator_attestation"])

        execution_package["trace_artifacts"][0]["id"] = "RTM-ID-LAUNDERED-AFTER-HASH"
        authority_request["operator_attestation"]["no_adjacent_runtime_side_effects"] = "mutated-after-hash"

        self.assertNotEqual(package["trace_artifacts"][0]["id"], "RTM-ID-LAUNDERED-AFTER-HASH")
        self.assertIs(package["operator_attestation"]["no_adjacent_runtime_side_effects"], True)
        self.assertEqual(
            package["authority_request_package_hash"],
            _canonical_hash(
                {key: value for key, value in package.items() if key != "authority_request_package_hash"}
            ),
        )
