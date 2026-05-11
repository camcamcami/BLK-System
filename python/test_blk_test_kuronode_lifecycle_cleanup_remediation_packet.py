import copy
import json
import unittest
from pathlib import Path

from blk_test_kuronode_lifecycle_cleanup_remediation_packet import (
    EXACT_EXCLUDED_AUTHORITIES,
    READY_STATUS,
    RETIRED_APPROVAL_ID,
    RETIRED_RUN_ID,
    TARGET_FINDING_LINE,
    TARGET_FINDING_PATH,
    TARGET_FINDING_RULE,
    build_lifecycle_cleanup_remediation_packet,
    default_lifecycle_cleanup_remediation_request,
    load_committed_blk_system_073_evidence,
)

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_PATH = ROOT / "docs" / "outcomes" / "BLK-SYSTEM-073_runtime-evidence.json"


class BlkTestKuronodeLifecycleCleanupRemediationPacketTest(unittest.TestCase):
    def _evidence(self):
        return load_committed_blk_system_073_evidence(EVIDENCE_PATH)

    def _packet(self, evidence=None, request=None):
        selected_evidence = copy.deepcopy(self._evidence() if evidence is None else evidence)
        selected_request = copy.deepcopy(
            default_lifecycle_cleanup_remediation_request(selected_evidence) if request is None else request
        )
        return build_lifecycle_cleanup_remediation_packet(evidence=selected_evidence, request=selected_request)

    def test_default_packet_is_review_ready_without_runtime_or_kuronode_mutation(self):
        evidence = self._evidence()
        packet = self._packet(evidence=evidence)

        self.assertEqual(packet["packet_status"], READY_STATUS)
        self.assertEqual(packet["source_sprint"], "BLK-SYSTEM-073")
        self.assertEqual(packet["source_pilot_status"], "BLK_TEST_KURONODE_WORKSPACE_READ_ONLY_PILOT_FAIL_EVIDENCE_ONLY")
        self.assertEqual(packet["finding"], {
            "path": TARGET_FINDING_PATH,
            "line": TARGET_FINDING_LINE,
            "rule": TARGET_FINDING_RULE,
        })
        self.assertEqual(packet["retired_runtime_ids"], {
            "approval_id": RETIRED_APPROVAL_ID,
            "run_id": RETIRED_RUN_ID,
        })
        self.assertEqual(set(packet["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        self.assertIn("packet_hash", packet)
        self.assertTrue(packet["source_evidence_hash"].startswith("sha256:"))
        self.assertEqual(packet["future_runtime_id_policy"], "FRESH_IDS_REQUIRED_BY_SEPARATE_AUTHORITY_NOT_ALLOCATED")
        for flag in [
            "pilot_rerun_performed",
            "kuronode_source_mutation_performed",
            "kuronode_git_mutation_performed",
            "blk_pipe_invoked",
            "codex_started",
            "electron_launched",
            "smoke_test_executed",
            "typescript_tooling_executed",
            "package_manager_invoked",
            "production_blk_test_mcp_started",
            "protected_body_read",
            "beo_published",
            "rtm_generated",
            "coverage_claim_promoted",
            "drift_rejection_performed",
        ]:
            self.assertIs(packet[flag], False, flag)

    def test_packet_contains_required_lifecycle_cleanup_obligations(self):
        packet = self._packet()
        obligations = {item["obligation_id"]: item for item in packet["remediation_obligations"]}

        self.assertEqual(
            set(obligations),
            {
                "LIFECYCLE_CLEANUP_ADD_DETERMINISTIC_TEARDOWN",
                "LIFECYCLE_CLEANUP_ASSERT_NO_ESCAPED_PROCESS_OR_LISTENER",
                "LIFECYCLE_CLEANUP_PRESERVE_TIMEOUT_AS_FAILURE",
                "LIFECYCLE_CLEANUP_ADD_FOCUSED_REGRESSION",
                "LIFECYCLE_CLEANUP_REQUIRE_FRESH_RUNTIME_IDS_FOR_RECHECK",
                "LIFECYCLE_CLEANUP_NOT_PATCH_AUTHORITY",
            },
        )
        joined = json.dumps(packet["remediation_guidance"], sort_keys=True)
        self.assertIn("finally", joined)
        self.assertIn("unsubscribe", joined)
        self.assertIn("close", joined)
        self.assertIn("line 53", joined)
        self.assertNotIn("npm run test:smoke", joined)
        self.assertNotIn("APPROVAL-BLK-SYSTEM-073-KURONODE-WORKSPACE-001", joined)

    def test_rejects_non_fail_or_missing_exact_lifecycle_finding(self):
        evidence = self._evidence()
        evidence["status"] = "PASS"
        request = default_lifecycle_cleanup_remediation_request(evidence)
        with self.assertRaisesRegex(ValueError, "must be BLK-SYSTEM-073 FAIL evidence"):
            self._packet(evidence=evidence, request=request)

        evidence = self._evidence()
        evidence["findings"] = [{"path": TARGET_FINDING_PATH, "line": TARGET_FINDING_LINE, "rule": "OTHER_RULE"}]
        request = default_lifecycle_cleanup_remediation_request(evidence)
        with self.assertRaisesRegex(ValueError, "missing exact lifecycle cleanup finding"):
            self._packet(evidence=evidence, request=request)

    def test_rejects_retired_runtime_id_reuse_and_forged_evidence_hash(self):
        evidence = self._evidence()
        request = default_lifecycle_cleanup_remediation_request(evidence)
        request["proposed_future_approval_id"] = RETIRED_APPROVAL_ID
        with self.assertRaisesRegex(ValueError, "retired BLK-SYSTEM-073 runtime ID"):
            self._packet(evidence=evidence, request=request)

        evidence = self._evidence()
        request = default_lifecycle_cleanup_remediation_request(evidence)
        request["source_evidence_hash"] = "sha256:" + "a" * 64
        with self.assertRaisesRegex(ValueError, "source_evidence_hash does not match submitted evidence"):
            self._packet(evidence=evidence, request=request)

    def test_rejects_laundered_authority_exact_exclusion_mismatch_and_protected_paths(self):
        evidence = self._evidence()
        request = default_lifecycle_cleanup_remediation_request(evidence)
        request["operator_note"] = {
            "safe": "fixture only",
            "nested": ["runtime pilot approved; patch Kuronode; PASS approves BEO publication"],
        }
        with self.assertRaisesRegex(ValueError, "authority-laundering text"):
            self._packet(evidence=evidence, request=request)

        request = default_lifecycle_cleanup_remediation_request(evidence)
        request["excluded_authorities"] = sorted(EXACT_EXCLUDED_AUTHORITIES - {"LIVE_CODEX_EXECUTION"})
        with self.assertRaisesRegex(ValueError, "excluded_authorities must match exact denied authority set"):
            self._packet(evidence=evidence, request=request)

        request = default_lifecycle_cleanup_remediation_request(evidence)
        request["target_patch_path"] = "docs%252Factive%252FREQ-001.md"
        with self.assertRaisesRegex(ValueError, "protected BLK-req body reference"):
            self._packet(evidence=evidence, request=request)

    def test_rejects_source_evidence_side_effect_claims(self):
        for key in [
            "source_mutation_detected",
            "git_mutation_detected",
            "production_mcp_authority",
            "generic_mcp_authority",
            "protected_body_read",
            "coverage_claim_promoted",
            "live_codex_execution",
            "package_manager_called",
            "typescript_tooling_called",
        ]:
            evidence = self._evidence()
            evidence[key] = True
            request = default_lifecycle_cleanup_remediation_request(evidence)
            with self.assertRaisesRegex(ValueError, "source evidence contains prohibited side effect"):
                self._packet(evidence=evidence, request=request)


if __name__ == "__main__":
    unittest.main()
