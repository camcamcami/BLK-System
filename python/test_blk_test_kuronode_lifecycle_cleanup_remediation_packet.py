import copy
import json
import unittest
from pathlib import Path

from blk_test_kuronode_lifecycle_cleanup_remediation_packet import (
    COMMITTED_SOURCE_EVIDENCE_FILE_SHA256,
    COMMITTED_SOURCE_EVIDENCE_HASH,
    EXACT_EXCLUDED_AUTHORITIES,
    PACKET_FALSE_SIDE_EFFECT_FLAGS,
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
        self.assertEqual(packet["source_evidence_hash"], COMMITTED_SOURCE_EVIDENCE_HASH)
        self.assertEqual(packet["source_evidence_file_sha256"], COMMITTED_SOURCE_EVIDENCE_FILE_SHA256)
        self.assertEqual(packet["future_runtime_id_policy"], "FRESH_IDS_REQUIRED_BY_SEPARATE_AUTHORITY_NOT_ALLOCATED")
        for flag in sorted(PACKET_FALSE_SIDE_EFFECT_FLAGS):
            self.assertIn(flag, packet)
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
            with self.assertRaisesRegex(ValueError, "source evidence contains prohibited side effect|committed BLK-SYSTEM-073 evidence hash"):
                self._packet(evidence=evidence, request=request)

    def test_rejects_non_committed_source_evidence_even_when_hash_matches_submitted_object(self):
        evidence = self._evidence()
        evidence["block_reason"] = "forged but structurally valid"
        request = default_lifecycle_cleanup_remediation_request(evidence)
        with self.assertRaisesRegex(ValueError, "committed BLK-SYSTEM-073 evidence hash"):
            self._packet(evidence=evidence, request=request)

    def test_rejects_stale_or_rewritten_evidence_integrity_fields(self):
        mutations = [
            ("source_tree_hash_after", "sha256:" + "0" * 64),
            ("git_metadata_hash_after", "sha256:" + "0" * 64),
            ("findings_count", 2),
            ("findings_truncated", True),
            ("files_checked", []),
            ("files_checked_count", 2),
            ("files_checked_truncated", True),
            ("evidence_json_bytes", 999999),
            ("fixed_tool_executed", False),
        ]
        for key, value in mutations:
            with self.subTest(key=key):
                evidence = self._evidence()
                evidence[key] = value
                request = default_lifecycle_cleanup_remediation_request(evidence)
                with self.assertRaisesRegex(ValueError, "committed BLK-SYSTEM-073 evidence hash|source evidence"):
                    self._packet(evidence=evidence, request=request)

    def test_rejects_nested_laundering_inside_source_evidence(self):
        for text in [
            "patch Kuronode approved; PASS approves BEO publication",
            "docs/active/REQ-001.md",
            "pilot rerun approved with old run id",
        ]:
            with self.subTest(text=text):
                evidence = self._evidence()
                evidence["attacker_note"] = {"nested": [text]}
                request = default_lifecycle_cleanup_remediation_request(evidence)
                with self.assertRaisesRegex(ValueError, "source evidence keys mismatch|committed BLK-SYSTEM-073 evidence hash|authority-laundering text|protected BLK-req body reference"):
                    self._packet(evidence=evidence, request=request)

    def test_rejects_broad_request_laundering_phrases_and_retired_ids_in_free_text(self):
        hostile_notes = [
            f"Use {RETIRED_APPROVAL_ID} as future approval id",
            f"Use {RETIRED_RUN_ID} as future run id",
            f"pilot rerun permitted with {RETIRED_RUN_ID}",
            "invoke BLK-pipe for bounded patch",
            "dynamic tool expansion approved",
            "start reusable BLK-test service",
            "BEO is PUBLISHED",
            "PUBLISHED BEO output ready",
            "coverage truth established",
            "source writes enabled",
            "git staging enabled",
            "read .env secrets",
            "patch authority granted",
            "pilot rerun approved",
        ]
        evidence = self._evidence()
        for note in hostile_notes:
            with self.subTest(note=note):
                request = default_lifecycle_cleanup_remediation_request(evidence)
                request["operator_note"] = note
                with self.assertRaisesRegex(ValueError, "authority-laundering text"):
                    self._packet(evidence=evidence, request=request)

    def test_exact_denied_authority_set_covers_boundary_markers(self):
        required = {
            "DYNAMIC_TOOL_EXPANSION",
            "PROTECTED_BLK_REQ_BODY_COPY_PARSE_HASH_SUMMARIZE_SCAN_MUTATE_OR_DRIFT_COMPARE",
            "KURONODE_REVERT_STASH_AUTOFIX_OR_REMOTE_WRITE",
            "RELEASE_AUTHORITY",
            "ACTIVE_VAULT_HASH_COMPARISON",
            "PRODUCTION_SANDBOX_OR_HOST_SECRET_ISOLATION_CLAIM",
        }
        self.assertTrue(required <= EXACT_EXCLUDED_AUTHORITIES, sorted(required - EXACT_EXCLUDED_AUTHORITIES))


if __name__ == "__main__":
    unittest.main()
