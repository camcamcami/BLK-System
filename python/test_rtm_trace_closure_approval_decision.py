import copy
import json
import unittest
from pathlib import Path

from rtm_trace_closure_approval_decision import (
    APPROVAL_DECISION_PACKAGE_ID,
    APPROVAL_ID,
    DECISION_RESULT,
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    FUTURE_RUN_ID,
    NEXT_REQUIRED_AUTHORITY,
    STATUS,
    build_rtm_trace_closure_approval_decision,
)

ROOT = Path(__file__).resolve().parents[1]
BLK101_JSON = ROOT / "docs" / "outcomes" / "BLK-SYSTEM-101_rtm-trace-closure-authority-request.json"


def load_blk101_request():
    return json.loads(BLK101_JSON.read_text())


def valid_decision():
    return {
        "approval_decision_package_id": APPROVAL_DECISION_PACKAGE_ID,
        "operator_identity": "discord:684235178083745819",
        "decision_scope": "RTM_TRACE_CLOSURE_APPROVAL_DECISION_ONLY_NOT_EXECUTION",
        "selected_frontier": "rtm_trace_closure_approval_decision_capture",
        "upstream_authority_request_package_id": "RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-101-001",
        "upstream_authority_request_package_hash": "sha256:b050261c1c1938423795f56427571d49dcf1d028c5811b5e3985b644cfadbcde",
        "approval_id": APPROVAL_ID,
        "future_run_id": FUTURE_RUN_ID,
        "decision_result": DECISION_RESULT,
        "decided_at": "2026-05-13T21:10:00+10:00",
        "expires_at": "2026-12-31T23:59:59+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_approval_text_raw": "sequentially plan and then execute all tasks of blk-system-101, blk-system-102 and blk-system-103",
        "operator_attestation": {
            "exact_blk101_request_reviewed": True,
            "approval_limited_to_one_future_local_trace_closure_execution": True,
            "future_run_id_reserved_not_consumed": True,
            "trace_closure_not_executed_by_this_decision": True,
            "rtm_generation_not_performed_by_this_decision": True,
            "drift_rejection_excluded": True,
            "active_vault_hash_comparison_excluded": True,
            "protected_body_reads_excluded": True,
            "target_source_git_mutation_excluded": True,
            "no_adjacent_runtime_side_effects": True,
        },
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
        "rtm_trace_closure_executed": False,
        "rtm_generated": False,
        "rtm_drift_rejection_authorized": False,
        "drift_decision_made": False,
        "active_vault_hash_comparison_performed": False,
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
    }


class RtmTraceClosureApprovalDecisionTests(unittest.TestCase):
    def test_captures_exact_approval_without_executing_trace_closure(self):
        package = build_rtm_trace_closure_approval_decision(load_blk101_request(), valid_decision())

        self.assertEqual(package["approval_decision_status"], STATUS)
        self.assertEqual(package["approval_decision_package_id"], APPROVAL_DECISION_PACKAGE_ID)
        self.assertEqual(package["upstream_authority_request_package_hash"], "sha256:b050261c1c1938423795f56427571d49dcf1d028c5811b5e3985b644cfadbcde")
        self.assertEqual(package["approval_id"], APPROVAL_ID)
        self.assertEqual(package["future_run_id"], FUTURE_RUN_ID)
        self.assertEqual(package["next_required_authority"], NEXT_REQUIRED_AUTHORITY)
        self.assertTrue(package["approval_decision_captured"])
        self.assertTrue(package["human_rtm_trace_closure_approval_granted"])
        self.assertFalse(package["future_run_id_consumed"])
        self.assertFalse(package["rtm_trace_closure_executed"])
        self.assertFalse(package["rtm_generated"])
        self.assertRegex(package["approval_decision_package_hash"], r"^sha256:[0-9a-f]{64}$")

    def test_rejects_forged_blk101_request_hash(self):
        request = load_blk101_request()
        request["authority_request_package_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "authority_request_package_hash does not match"):
            build_rtm_trace_closure_approval_decision(request, valid_decision())

    def test_rejects_self_consistent_noncanonical_request(self):
        request = load_blk101_request()
        request["authority_request_package_id"] = "RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-101-999"
        from authoritative_beo_publication_authority_request import _canonical_hash
        request["authority_request_package_hash"] = _canonical_hash({k: v for k, v in request.items() if k != "authority_request_package_hash"})
        with self.assertRaisesRegex(ValueError, "canonical BLK-101"):
            build_rtm_trace_closure_approval_decision(request, valid_decision())

    def test_rejects_decision_window_outside_request_expiry(self):
        decision = valid_decision()
        decision["expires_at"] = "2027-01-01T00:00:00+10:00"
        with self.assertRaisesRegex(ValueError, "decision window must end within BLK-101 request expiry"):
            build_rtm_trace_closure_approval_decision(load_blk101_request(), decision)

    def test_rejects_execution_side_effects_in_decision(self):
        for key in ["rtm_trace_closure_executed", "rtm_generated", "protected_body_reads", "active_vault_hash_comparison_performed"]:
            decision = valid_decision()
            decision[key] = True
            with self.subTest(key=key):
                with self.assertRaisesRegex(ValueError, f"{key} must remain false"):
                    build_rtm_trace_closure_approval_decision(load_blk101_request(), decision)

    def test_rejects_denied_authority_drift(self):
        decision = valid_decision()
        decision["excluded_authorities"] = sorted(EXACT_EXCLUDED_AUTHORITIES - {"PROTECTED_BLK_REQ_BODY_READ"})
        with self.assertRaisesRegex(ValueError, "excluded_authorities must match exact set"):
            build_rtm_trace_closure_approval_decision(load_blk101_request(), decision)

    def test_rejects_laundering_text_outside_operator_approval_quote(self):
        decision = valid_decision()
        decision["operator_attestation"]["trace_closure_not_executed_by_this_decision"] = "RTMGenerated and protectedBodyRead allowed"
        with self.assertRaisesRegex(ValueError, "authority-laundering text"):
            build_rtm_trace_closure_approval_decision(load_blk101_request(), decision)


if __name__ == "__main__":
    unittest.main()
