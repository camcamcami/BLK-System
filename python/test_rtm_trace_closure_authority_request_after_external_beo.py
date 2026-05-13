import copy
import json
import unittest
from pathlib import Path

from rtm_trace_closure_authority_request_after_external_beo import (
    AUTHORITY_REQUEST_PACKAGE_ID,
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY,
    REQUEST_STATUS,
    SELECTED_FRONTIER,
    build_rtm_trace_closure_authority_request,
)

ROOT = Path(__file__).resolve().parents[1]
BLK100_JSON = ROOT / "docs" / "outcomes" / "BLK-SYSTEM-100_external-beo-publication-execution.json"


def load_blk100_package():
    return json.loads(BLK100_JSON.read_text())


def valid_request():
    return {
        "authority_request_package_id": AUTHORITY_REQUEST_PACKAGE_ID,
        "operator_identity": "discord:684235178083745819",
        "request_scope": "RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_AFTER_EXTERNAL_BEO_PUBLICATION_REVIEW_ONLY",
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_execution_package_id": "BEO-PUBLICATION-EXECUTION-100-001",
        "upstream_execution_package_hash": "sha256:5269146b6b46e27e38878a327b1ac6180068d5c9e427067604b611512a72289d",
        "publication_record_hash": "sha256:1efbfd9b6b9d828b7b793c1c9c2b0f8115c36db69ef850e5a2f2ff94195923b4",
        "beo_id": "BEO-054-001",
        "beo_hash": "sha256:" + "a" * 64,
        "target_repo_path_metadata_only": "/home/dad/code/Kuronode-v1",
        "target_head_sha_metadata_only": "aebea51bed911c781a537d84d38b2dcb838b1368",
        "request_future_exact_rtm_trace_closure_authority": True,
        "human_rtm_trace_closure_approval_granted": False,
        "rtm_trace_closure_authorized": False,
        "rtm_trace_closure_executed": False,
        "rtm_generated": False,
        "rtm_drift_rejection_authorized": False,
        "drift_decision_made": False,
        "active_vault_hash_comparison_performed": False,
        "coverage_claim_promoted": False,
        "protected_body_reads": False,
        "signer_key_material_access": False,
        "cryptographic_signing": False,
        "immutable_storage_write": False,
        "public_ledger_mutation": False,
        "rollback_revocation_supersession_execution": False,
        "target_repo_scan_or_mutation": False,
        "source_or_git_mutation_by_fixture": False,
        "beb_dispatch_authorized": False,
        "beo_closeout_execution_authorized": False,
        "blk_pipe_blk_test_codex_runtime": False,
        "package_network_model_browser_cyber_tooling": False,
        "production_isolation_claim": False,
        "requested_at": "2026-05-13T21:00:00+10:00",
        "expires_at": "2026-12-31T23:59:59+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {
            "exact_blk100_publication_execution_reviewed": True,
            "external_beo_publication_record_is_hash_bound": True,
            "request_is_for_future_trace_closure_authority_not_execution": True,
            "rtm_generation_not_performed_by_request": True,
            "drift_rejection_excluded": True,
            "active_vault_hash_comparison_excluded": True,
            "protected_body_reads_excluded": True,
            "signer_storage_ledger_rollback_side_effects_excluded": True,
            "target_source_git_mutation_excluded": True,
            "no_adjacent_runtime_side_effects": True,
        },
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }


class RtmTraceClosureAuthorityRequestAfterExternalBeoTests(unittest.TestCase):
    def test_builds_hash_bound_request_without_granting_trace_closure(self):
        package = build_rtm_trace_closure_authority_request(load_blk100_package(), valid_request())

        self.assertEqual(package["request_status"], REQUEST_STATUS)
        self.assertEqual(package["authority_request_package_id"], AUTHORITY_REQUEST_PACKAGE_ID)
        self.assertEqual(package["upstream_execution_package_hash"], "sha256:5269146b6b46e27e38878a327b1ac6180068d5c9e427067604b611512a72289d")
        self.assertEqual(package["publication_record_hash"], "sha256:1efbfd9b6b9d828b7b793c1c9c2b0f8115c36db69ef850e5a2f2ff94195923b4")
        self.assertEqual(package["requested_authority"], "ONE_FUTURE_LOCAL_RTM_TRACE_CLOSURE_EXECUTION")
        self.assertEqual(package["next_required_authority"], NEXT_REQUIRED_AUTHORITY)
        self.assertEqual(package["rtm_trace_closure_authority"], "REQUEST_ONLY_NOT_GRANTED")
        self.assertFalse(package["rtm_trace_closure_executed"])
        self.assertFalse(package["rtm_generated"])
        self.assertFalse(package["protected_body_reads"])
        self.assertFalse(package["active_vault_hash_comparison_performed"])
        self.assertRegex(package["authority_request_package_hash"], r"^sha256:[0-9a-f]{64}$")

    def test_rejects_forged_blk100_execution_package_hash(self):
        upstream = load_blk100_package()
        upstream["execution_package_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "execution_package_hash does not match"):
            build_rtm_trace_closure_authority_request(upstream, valid_request())

    def test_rejects_self_consistent_but_noncanonical_blk100_identity(self):
        upstream = load_blk100_package()
        upstream["execution_package_id"] = "BEO-PUBLICATION-EXECUTION-100-999"
        from authoritative_beo_publication_authority_request import _canonical_hash
        upstream["execution_package_hash"] = _canonical_hash({k: v for k, v in upstream.items() if k != "execution_package_hash"})
        with self.assertRaisesRegex(ValueError, "canonical BLK-100"):
            build_rtm_trace_closure_authority_request(upstream, valid_request())

    def test_rejects_premature_trace_closure_or_rtm_generation(self):
        for key in ["rtm_trace_closure_executed", "rtm_generated", "active_vault_hash_comparison_performed", "protected_body_reads"]:
            request = valid_request()
            request[key] = True
            with self.subTest(key=key):
                with self.assertRaisesRegex(ValueError, f"{key} must remain false"):
                    build_rtm_trace_closure_authority_request(load_blk100_package(), request)

    def test_rejects_exact_denied_authority_drift(self):
        request = valid_request()
        request["excluded_authorities"] = sorted(EXACT_EXCLUDED_AUTHORITIES - {"PROTECTED_BLK_REQ_BODY_READ"})
        with self.assertRaisesRegex(ValueError, "excluded_authorities must match exact set"):
            build_rtm_trace_closure_authority_request(load_blk100_package(), request)

        request = valid_request()
        request["excluded_authorities"] = sorted(EXACT_EXCLUDED_AUTHORITIES) + ["APPROVED_FOR_LIVE_EXECUTION"]
        with self.assertRaisesRegex(ValueError, "excluded_authorities must match exact set"):
            build_rtm_trace_closure_authority_request(load_blk100_package(), request)

    def test_rejects_nested_authority_laundering_text(self):
        request = valid_request()
        request["operator_attestation"]["request_is_for_future_trace_closure_authority_not_execution"] = "runtime pilot approved; protected body read allowed"
        with self.assertRaisesRegex(ValueError, "authority-laundering text"):
            build_rtm_trace_closure_authority_request(load_blk100_package(), request)

    def test_rejects_consumed_blk100_run_id_reuse_in_request_strings(self):
        request = valid_request()
        request["target_repo_path_metadata_only"] = "RUN-BLK-SYSTEM-100-EXTERNAL-BEO-PUBLICATION-001 reused for trace closure"
        with self.assertRaisesRegex(ValueError, "RUN-BLK-SYSTEM-100"):
            build_rtm_trace_closure_authority_request(load_blk100_package(), request)


if __name__ == "__main__":
    unittest.main()
