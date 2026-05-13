import json
import unittest
from pathlib import Path

from exact_local_rtm_trace_closure_execution import (
    EXECUTION_PACKAGE_ID,
    EXECUTION_STATUS,
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    RUN_ID_CONSUMED,
    build_exact_local_rtm_trace_closure_execution,
)

ROOT = Path(__file__).resolve().parents[1]
BLK102_JSON = ROOT / "docs" / "outcomes" / "BLK-SYSTEM-102_rtm-trace-closure-approval-decision.json"


def load_blk102_approval():
    return json.loads(BLK102_JSON.read_text())


def valid_execution_request():
    return {
        "execution_package_id": EXECUTION_PACKAGE_ID,
        "operator_identity": "discord:684235178083745819",
        "execution_scope": "EXACT_LOCAL_RTM_TRACE_CLOSURE_EXECUTION_RECORD_ONLY",
        "selected_frontier": "exact_local_rtm_trace_closure_execution",
        "approval_decision_package_id": "RTM-TRACE-CLOSURE-APPROVAL-DECISION-102-001",
        "approval_decision_package_hash": "sha256:9211e14961b8c0f380812372d2b2a1ae091daf17709af375985f94015af0fecb",
        "approval_id": "APPROVAL-BLK-SYSTEM-101-RTM-TRACE-CLOSURE-001",
        "run_id_to_consume": RUN_ID_CONSUMED,
        "requested_at": "2026-05-13T21:20:00+10:00",
        "expires_at": "2026-12-31T23:59:59+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {
            "exact_blk102_approval_reviewed": True,
            "run_id_consumed_once_for_local_trace_closure": True,
            "local_trace_closure_record_only_not_production_blk_link": True,
            "rtm_generation_not_performed": True,
            "drift_rejection_excluded": True,
            "active_vault_hash_comparison_excluded": True,
            "protected_body_reads_excluded": True,
            "public_ledger_mutation_excluded": True,
            "target_source_git_mutation_excluded": True,
            "no_adjacent_runtime_side_effects": True,
        },
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
        "rtm_generated": False,
        "rtm_drift_rejection_performed": False,
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


class ExactLocalRtmTraceClosureExecutionTests(unittest.TestCase):
    def test_executes_exact_local_trace_closure_record_without_adjacent_authority(self):
        package = build_exact_local_rtm_trace_closure_execution(load_blk102_approval(), valid_execution_request())

        self.assertEqual(package["execution_status"], EXECUTION_STATUS)
        self.assertEqual(package["execution_package_id"], EXECUTION_PACKAGE_ID)
        self.assertEqual(package["run_id_consumed"], RUN_ID_CONSUMED)
        self.assertTrue(package["future_run_id_consumed"])
        self.assertTrue(package["local_rtm_trace_closure_record_emitted"])
        self.assertEqual(package["trace_closure_record"]["trace_closure_status"], "PILOT_LOCAL_RTM_TRACE_CLOSURE_RECORDED_NOT_AUTHORITATIVE")
        self.assertEqual(package["trace_closure_record"]["publication_record_hash"], "sha256:1efbfd9b6b9d828b7b793c1c9c2b0f8115c36db69ef850e5a2f2ff94195923b4")
        self.assertFalse(package["rtm_generated"])
        self.assertFalse(package["active_vault_hash_comparison_performed"])
        self.assertFalse(package["protected_body_reads"])
        self.assertFalse(package["drift_decision_made"])
        self.assertRegex(package["execution_package_hash"], r"^sha256:[0-9a-f]{64}$")

    def test_rejects_forged_blk102_approval_hash(self):
        approval = load_blk102_approval()
        approval["approval_decision_package_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "approval_decision_package_hash does not match"):
            build_exact_local_rtm_trace_closure_execution(approval, valid_execution_request())

    def test_rejects_self_consistent_noncanonical_approval(self):
        approval = load_blk102_approval()
        approval["future_run_id"] = "RUN-BLK-SYSTEM-103-RTM-TRACE-CLOSURE-999"
        from authoritative_beo_publication_authority_request import _canonical_hash
        approval["approval_decision_package_hash"] = _canonical_hash({k: v for k, v in approval.items() if k != "approval_decision_package_hash"})
        with self.assertRaisesRegex(ValueError, "canonical BLK-102"):
            build_exact_local_rtm_trace_closure_execution(approval, valid_execution_request())

    def test_rejects_replay_or_wrong_run_id(self):
        request = valid_execution_request()
        request["replayed"] = True
        with self.assertRaisesRegex(ValueError, "execution request must not be replayed"):
            build_exact_local_rtm_trace_closure_execution(load_blk102_approval(), request)

        request = valid_execution_request()
        request["run_id_to_consume"] = "RUN-BLK-SYSTEM-103-RTM-TRACE-CLOSURE-999"
        with self.assertRaisesRegex(ValueError, "run_id_to_consume must match"):
            build_exact_local_rtm_trace_closure_execution(load_blk102_approval(), request)

    def test_rejects_protected_or_active_vault_side_effects(self):
        for key in ["protected_body_reads", "active_vault_hash_comparison_performed", "drift_decision_made", "public_ledger_mutation", "rtm_generated"]:
            request = valid_execution_request()
            request[key] = True
            with self.subTest(key=key):
                with self.assertRaisesRegex(ValueError, f"{key} must remain false"):
                    build_exact_local_rtm_trace_closure_execution(load_blk102_approval(), request)

    def test_rejects_denied_authority_drift(self):
        request = valid_execution_request()
        request["excluded_authorities"] = sorted(EXACT_EXCLUDED_AUTHORITIES - {"PROTECTED_BLK_REQ_BODY_READ"})
        with self.assertRaisesRegex(ValueError, "excluded_authorities must match exact set"):
            build_exact_local_rtm_trace_closure_execution(load_blk102_approval(), request)

    def test_rejects_nested_authority_laundering_text(self):
        request = valid_execution_request()
        request["operator_attestation"]["local_trace_closure_record_only_not_production_blk_link"] = "activeVaultHashComparison and protectedBodyRead are authorized"
        with self.assertRaisesRegex(ValueError, "authority-laundering text"):
            build_exact_local_rtm_trace_closure_execution(load_blk102_approval(), request)


if __name__ == "__main__":
    unittest.main()
