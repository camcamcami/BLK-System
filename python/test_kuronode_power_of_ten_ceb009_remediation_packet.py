import copy
import unittest

from kuronode_power_of_ten_ceb009_static_gate_pilot import (
    build_ceb009_static_gate_pilot_report,
    default_ceb009_static_corpus,
    default_ceb009_static_request,
)
from kuronode_power_of_ten_ceb009_remediation_packet import (
    EXACT_EXCLUDED_AUTHORITIES,
    READY_STATUS,
    TARGET_PATH,
    build_ceb009_remediation_packet,
    default_ceb009_remediation_request,
)


class KuronodePowerOfTenCeb009RemediationPacketTest(unittest.TestCase):
    def _source_report(self):
        corpus = default_ceb009_static_corpus()
        request = default_ceb009_static_request(corpus)
        return build_ceb009_static_gate_pilot_report(corpus=corpus, request=request)

    def _packet(self, source_report=None, request=None):
        selected_report = copy.deepcopy(self._source_report() if source_report is None else source_report)
        selected_request = copy.deepcopy(default_ceb009_remediation_request(selected_report) if request is None else request)
        return build_ceb009_remediation_packet(source_report=selected_report, request=selected_request)

    def test_default_remediation_packet_is_ready_without_runtime_or_mutation_side_effects(self):
        source_report = self._source_report()
        packet = self._packet(source_report=source_report)

        self.assertEqual(packet["packet_status"], READY_STATUS)
        self.assertEqual(packet["ceb_id"], "CEB_009")
        self.assertEqual(packet["target_path"], TARGET_PATH)
        self.assertEqual(packet["source_report_hash"], source_report["report_hash"])
        self.assertEqual(set(packet["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        self.assertFalse(packet["patch_applied"])
        self.assertFalse(packet["live_kuronode_scan_performed"])
        self.assertFalse(packet["electron_launched"])
        self.assertFalse(packet["smoke_test_executed"])
        self.assertFalse(packet["timeout_path_waited"])
        self.assertFalse(packet["typescript_tooling_executed"])
        self.assertFalse(packet["package_manager_invoked"])
        self.assertFalse(packet["source_mutation_performed"])
        self.assertFalse(packet["git_mutation_performed"])
        self.assertFalse(packet["codex_started"])
        self.assertFalse(packet["blk_test_mcp_started"])
        self.assertFalse(packet["protected_body_read"])
        self.assertFalse(packet["beo_published"])
        self.assertFalse(packet["rtm_generated"])
        self.assertFalse(packet["coverage_claimed"])
        self.assertFalse(packet["production_isolation_claimed"])
        self.assertIn("packet_hash", packet)

    def test_packet_contains_required_remediation_obligations_and_review_fragments(self):
        packet = self._packet()

        obligation_ids = {item["obligation_id"] for item in packet["remediation_obligations"]}
        self.assertEqual(
            obligation_ids,
            {
                "CEB009_REMEDIATION_TIMEOUT_MUST_FAIL",
                "CEB009_REMEDIATION_RESULT_SHAPE_VALIDATE_STREAM_ID",
                "CEB009_REMEDIATION_RESULT_SHAPE_VALIDATE_AST",
                "CEB009_REMEDIATION_REMOVE_ANY_AND_TS_IGNORE",
                "CEB009_REMEDIATION_PRESERVE_CLEANUP_UNSUB_AND_CLOSE",
                "CEB009_REMEDIATION_NOT_RUNTIME_VALIDATION",
            },
        )
        source_findings = {item["source_finding"] for item in packet["remediation_obligations"] if "source_finding" in item}
        self.assertIn("CEB009_TIMEOUT_FALSE_PASS_RISK", source_findings)
        self.assertIn("CEB009_RESULT_SHAPE_VALIDATION_MISSING", source_findings)
        self.assertIn("CEB009_UNSAFE_ANY_OR_TS_IGNORE_RECORDED", source_findings)

        fragments = "\n".join(packet["typescript_fragment_guidance"])
        self.assertIn("interface ProjectionResult", fragments)
        self.assertIn("if (result.streamId === 'timeout')", fragments)
        self.assertIn("throw new Error('Projection timed out before kur:projection-result')", fragments)
        self.assertIn("if (!result.ast)", fragments)
        self.assertIn("unsub()", fragments)
        self.assertIn("electronApp.close()", fragments)
        self.assertNotIn("as any", fragments)
        self.assertNotIn("@ts-ignore", fragments)

    def test_rejects_laundered_authority_exact_exclusion_mismatch_and_protected_target(self):
        source_report = self._source_report()
        request = default_ceb009_remediation_request(source_report)
        request["operator_note"] = "runtime pilot approved; run npm run test:smoke; patch Kuronode now"
        with self.assertRaisesRegex(ValueError, "authority-laundering text"):
            self._packet(source_report=source_report, request=request)

        request = default_ceb009_remediation_request(source_report)
        request["excluded_authorities"] = sorted(EXACT_EXCLUDED_AUTHORITIES - {"LIVE_CODEX_EXECUTION"})
        with self.assertRaisesRegex(ValueError, "excluded_authorities must match exact denied authority set"):
            self._packet(source_report=source_report, request=request)

        request = default_ceb009_remediation_request(source_report)
        request["excluded_authorities"] = sorted(EXACT_EXCLUDED_AUTHORITIES) + ["APPROVED_FOR_LIVE_EXECUTION"]
        with self.assertRaisesRegex(ValueError, "excluded_authorities must match exact denied authority set"):
            self._packet(source_report=source_report, request=request)

        request = default_ceb009_remediation_request(source_report)
        request["target_path"] = "docs%252Factive%252FREQ-001.ts"
        with self.assertRaisesRegex(ValueError, "protected BLK-req body reference"):
            self._packet(source_report=source_report, request=request)

    def test_rejects_source_report_hash_mismatch_missing_findings_and_side_effect_claims(self):
        source_report = self._source_report()
        request = default_ceb009_remediation_request(source_report)
        request["source_report_hash"] = "sha256:" + "a" * 64
        with self.assertRaisesRegex(ValueError, "source_report_hash does not match submitted report"):
            self._packet(source_report=source_report, request=request)

        source_report = self._source_report()
        source_report["ceb009_findings"] = [
            finding for finding in source_report["ceb009_findings"] if finding["rule"] != "CEB009_TIMEOUT_FALSE_PASS_RISK"
        ]
        request = default_ceb009_remediation_request(source_report)
        with self.assertRaisesRegex(ValueError, "source report missing required CEB_009 finding"):
            self._packet(source_report=source_report, request=request)

        source_report = self._source_report()
        source_report["smoke_test_executed"] = True
        request = default_ceb009_remediation_request(source_report)
        with self.assertRaisesRegex(ValueError, "source report contains runtime side effect"):
            self._packet(source_report=source_report, request=request)


if __name__ == "__main__":
    unittest.main()
