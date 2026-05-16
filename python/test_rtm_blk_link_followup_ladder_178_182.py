import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from test_protected_body_verification_decision_engine_175_176 import valid_175_decision_package
from rtm_blk_link_protected_body_verification_integration_176 import (
    CANONICAL_BLK176_RECONCILIATION_PACKAGE_HASH,
    build_rtm_blk_link_protected_body_verification_integration_176,
    valid_rtm_blk_link_protected_body_verification_integration_176,
)

from rtm_blk_link_followup_ladder_178_182 import (
    APPROVAL_ID_179,
    CANONICAL_BLK178_AUTHORITY_REQUEST_PACKAGE_HASH,
    CANONICAL_BLK179_FOLLOWUP_EXECUTION_PACKAGE_HASH,
    CANONICAL_BLK180_RECONCILIATION_PACKAGE_HASH,
    CANONICAL_BLK181_EXPORT_PACKAGE_HASH,
    CANONICAL_BLK182_RECONCILIATION_PACKAGE_HASH,
    EXACT_EXCLUDED_AUTHORITIES_178,
    EXACT_EXCLUDED_AUTHORITIES_179,
    EXACT_EXCLUDED_AUTHORITIES_180,
    EXACT_EXCLUDED_AUTHORITIES_181,
    EXACT_EXCLUDED_AUTHORITIES_182,
    EXACT_OPERATOR_DECISION_TEXT_179,
    EXACT_PROOF_OBLIGATIONS_178,
    EXACT_PROOF_OBLIGATIONS_179,
    EXACT_PROOF_OBLIGATIONS_180,
    EXACT_PROOF_OBLIGATIONS_181,
    EXACT_PROOF_OBLIGATIONS_182,
    FOLLOWUP_EXECUTION_STATUS_179,
    REQUEST_STATUS_178,
    RUN_ID_CONSUMED_179,
    SIDE_EFFECT_FLAGS_178,
    SIDE_EFFECT_FLAGS_179,
    SIDE_EFFECT_FLAGS_180,
    SIDE_EFFECT_FLAGS_181,
    SIDE_EFFECT_FLAGS_182,
    build_rtm_blk_link_followup_authority_request_178,
    build_rtm_blk_link_followup_evidence_export_181,
    build_rtm_blk_link_followup_execution_record_179,
    build_rtm_blk_link_followup_post_execution_reconciliation_180,
    build_rtm_blk_link_followup_post_export_reconciliation_182,
    valid_rtm_blk_link_followup_authority_request_178,
    valid_rtm_blk_link_followup_evidence_export_181,
    valid_rtm_blk_link_followup_execution_record_179,
    valid_rtm_blk_link_followup_post_execution_reconciliation_180,
    valid_rtm_blk_link_followup_post_export_reconciliation_182,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "rtm_blk_link_followup_ladder_178_182.py"


def valid_176_reconciliation_package():
    decision175 = valid_175_decision_package()
    context176 = valid_rtm_blk_link_protected_body_verification_integration_176(decision175)
    return build_rtm_blk_link_protected_body_verification_integration_176(decision175, context176)


def valid_178_request_package():
    reconciliation176 = valid_176_reconciliation_package()
    request178 = valid_rtm_blk_link_followup_authority_request_178(reconciliation176)
    return build_rtm_blk_link_followup_authority_request_178(reconciliation176, request178)


def valid_179_execution_package():
    request178 = valid_178_request_package()
    execution179 = valid_rtm_blk_link_followup_execution_record_179(request178)
    return build_rtm_blk_link_followup_execution_record_179(request178, execution179)


def valid_180_reconciliation_package():
    execution179 = valid_179_execution_package()
    context180 = valid_rtm_blk_link_followup_post_execution_reconciliation_180(execution179)
    return build_rtm_blk_link_followup_post_execution_reconciliation_180(execution179, context180)


def valid_181_export_package():
    reconciliation180 = valid_180_reconciliation_package()
    export181 = valid_rtm_blk_link_followup_evidence_export_181(reconciliation180)
    return build_rtm_blk_link_followup_evidence_export_181(reconciliation180, export181)


class RTMBlkLinkFollowupLadder178182Test(unittest.TestCase):
    def test_178_emits_request_only_followup_package_bound_to_exact_176(self):
        reconciliation176 = valid_176_reconciliation_package()
        request178 = valid_rtm_blk_link_followup_authority_request_178(reconciliation176)

        package = build_rtm_blk_link_followup_authority_request_178(reconciliation176, request178)

        self.assertEqual(package["request_status"], REQUEST_STATUS_178)
        self.assertEqual(package["upstream_reconciliation_package_hash"], CANONICAL_BLK176_RECONCILIATION_PACKAGE_HASH)
        self.assertTrue(package["request_future_exact_followup_execution_approval"])
        self.assertFalse(package["approval_capture_performed"])
        self.assertFalse(package["future_run_id_reserved_or_consumed"])
        self.assertFalse(package["rtm_generated"])
        self.assertFalse(package["production_blk_link_live_execution_performed"])
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_178)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_178)
        for flag in SIDE_EFFECT_FLAGS_178:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(package["authority_request_hash"], _canonical_hash(request178))
        self.assertEqual(package["authority_request_package_hash"], _canonical_hash({k: v for k, v in package.items() if k != "authority_request_package_hash"}))
        self.assertEqual(package["authority_request_package_hash"], CANONICAL_BLK178_AUTHORITY_REQUEST_PACKAGE_HASH)

    def test_179_records_metadata_only_followup_execution_without_rtm_or_runtime_authority(self):
        request178 = valid_178_request_package()
        execution179 = valid_rtm_blk_link_followup_execution_record_179(request178)

        package = build_rtm_blk_link_followup_execution_record_179(request178, execution179)

        self.assertEqual(package["followup_execution_status"], FOLLOWUP_EXECUTION_STATUS_179)
        self.assertEqual(package["approval_id"], APPROVAL_ID_179)
        self.assertEqual(package["run_id_consumed"], RUN_ID_CONSUMED_179)
        self.assertEqual(package["operator_decision_text_raw"], EXACT_OPERATOR_DECISION_TEXT_179)
        self.assertTrue(package["operator_decision_captured"])
        self.assertTrue(package["one_run_id_consumed_in_record_only_evidence"])
        self.assertTrue(package["rtm_blk_link_followup_recorded"])
        self.assertEqual(package["upstream_authority_request_package_hash"], CANONICAL_BLK178_AUTHORITY_REQUEST_PACKAGE_HASH)
        self.assertEqual(package["protected_body_verification_lineage_hash"], request178["upstream_reconciliation_package_hash"])
        self.assertFalse(package["rtm_generated"])
        self.assertFalse(package["rtm_drift_rejection_performed"])
        self.assertFalse(package["coverage_truth_established"])
        self.assertFalse(package["protected_body_reads"])
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_179)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_179)
        true_flags = {"operator_decision_captured", "one_run_id_consumed_in_record_only_evidence", "rtm_blk_link_followup_recorded"}
        for flag in SIDE_EFFECT_FLAGS_179:
            self.assertIs(package[flag], flag in true_flags, flag)
        self.assertEqual(package["followup_execution_package_hash"], _canonical_hash({k: v for k, v in package.items() if k != "followup_execution_package_hash"}))
        self.assertEqual(package["followup_execution_package_hash"], CANONICAL_BLK179_FOLLOWUP_EXECUTION_PACKAGE_HASH)

    def test_180_reconciles_execution_and_selects_metadata_export_without_granting_it(self):
        execution179 = valid_179_execution_package()
        context180 = valid_rtm_blk_link_followup_post_execution_reconciliation_180(execution179)

        package = build_rtm_blk_link_followup_post_execution_reconciliation_180(execution179, context180)

        self.assertTrue(package["clean_followup_execution_reconciled"])
        self.assertFalse(package["observed_failure_requires_hardening"])
        self.assertEqual(package["upstream_followup_execution_package_hash"], CANONICAL_BLK179_FOLLOWUP_EXECUTION_PACKAGE_HASH)
        self.assertFalse(package["next_frontier_granted"])
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_180)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_180)
        for flag in SIDE_EFFECT_FLAGS_180:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(package["reconciliation_package_hash"], CANONICAL_BLK180_RECONCILIATION_PACKAGE_HASH)

    def test_181_exports_downstream_metadata_packet_from_clean_180_without_body_or_runtime_access(self):
        reconciliation180 = valid_180_reconciliation_package()
        export181 = valid_rtm_blk_link_followup_evidence_export_181(reconciliation180)

        package = build_rtm_blk_link_followup_evidence_export_181(reconciliation180, export181)

        self.assertTrue(package["downstream_metadata_export_emitted"])
        self.assertEqual(package["upstream_reconciliation_package_hash"], CANONICAL_BLK180_RECONCILIATION_PACKAGE_HASH)
        self.assertEqual(package["protected_body_verification_lineage_hash"], reconciliation180["protected_body_verification_lineage_hash"])
        self.assertEqual(package["export_manifest_hash"], _canonical_hash(package["export_manifest"]))
        for item in package["export_manifest"]["trace_evidence"]:
            self.assertIn("version_hash", item)
            self.assertNotIn("body_text", item)
            self.assertNotIn("protected_body_path", item)
        self.assertFalse(package["protected_body_reads"])
        self.assertFalse(package["rtm_generated"])
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_181)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_181)
        for flag in SIDE_EFFECT_FLAGS_181:
            self.assertIs(package[flag], flag == "downstream_metadata_export_emitted", flag)
        self.assertEqual(package["export_package_hash"], CANONICAL_BLK181_EXPORT_PACKAGE_HASH)

    def test_182_reconciles_export_and_names_next_operator_decision_without_granting_authority(self):
        export181 = valid_181_export_package()
        context182 = valid_rtm_blk_link_followup_post_export_reconciliation_182(export181)

        package = build_rtm_blk_link_followup_post_export_reconciliation_182(export181, context182)

        self.assertTrue(package["clean_export_reconciled"])
        self.assertEqual(package["upstream_export_package_hash"], CANONICAL_BLK181_EXPORT_PACKAGE_HASH)
        self.assertFalse(package["next_frontier_granted"])
        self.assertFalse(package["observed_failure_requires_hardening"])
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_182)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_182)
        for flag in SIDE_EFFECT_FLAGS_182:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(package["reconciliation_package_hash"], CANONICAL_BLK182_RECONCILIATION_PACKAGE_HASH)

    def test_ladder_rejects_rehashed_upstream_and_authority_laundering(self):
        reconciliation176 = valid_176_reconciliation_package()
        request178 = valid_rtm_blk_link_followup_authority_request_178(reconciliation176)
        request178["operator_identity"] = "discord:other-operator"
        with self.assertRaisesRegex(ValueError, "operator_identity must match upstream operator_identity"):
            build_rtm_blk_link_followup_authority_request_178(reconciliation176, request178)

        forged176 = copy.deepcopy(reconciliation176)
        forged176["rtm_generated"] = True
        forged176["reconciliation_package_hash"] = _canonical_hash({k: v for k, v in forged176.items() if k != "reconciliation_package_hash"})
        with self.assertRaisesRegex(ValueError, "canonical BLK-176 reconciliation package hash mismatch|rtm_generated"):
            build_rtm_blk_link_followup_authority_request_178(forged176, valid_rtm_blk_link_followup_authority_request_178(forged176))

        request178 = valid_178_request_package()
        execution179 = valid_rtm_blk_link_followup_execution_record_179(request178)
        for patch, message in [
            ({"followup_execution_package_id": "RTM-BLK-LINK-FOLLOWUP-EXECUTION-１７９-001"}, "followup_execution_package_id must be"),
            ({"operator_identity": "discord:684235178083745819 RTMGenerationAuthorized"}, "authority-laundering text"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_179) + [sorted(EXACT_EXCLUDED_AUTHORITIES_179)[0]]}, "excluded_authorities must not contain duplicates"),
            ({"operator_attestation": execution179["operator_attestation"] | {"coverageTruthEstablished": True}}, "unexpected field"),
        ]:
            candidate = copy.deepcopy(execution179)
            candidate.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_rtm_blk_link_followup_execution_record_179(request178, candidate)

        for flag in SIDE_EFFECT_FLAGS_179:
            if flag in {"operator_decision_captured", "one_run_id_consumed_in_record_only_evidence", "rtm_blk_link_followup_recorded"}:
                continue
            candidate = copy.deepcopy(execution179)
            candidate[flag] = True
            with self.subTest(flag=flag):
                with self.assertRaisesRegex(ValueError, f"{flag} must remain false"):
                    build_rtm_blk_link_followup_execution_record_179(request178, candidate)

        reconciliation180 = valid_180_reconciliation_package()
        export181 = valid_rtm_blk_link_followup_evidence_export_181(reconciliation180)
        export181["export_notes"] = "coverage%20truth%20established and docs%252Frequirements%252Factive%252FREQ-001.md"
        with self.assertRaisesRegex(ValueError, "authority-laundering text"):
            build_rtm_blk_link_followup_evidence_export_181(reconciliation180, export181)

    def test_hash_binding_and_defensive_copies_prevent_post_hash_mutation(self):
        request178 = valid_178_request_package()
        execution179 = valid_rtm_blk_link_followup_execution_record_179(request178)
        package = build_rtm_blk_link_followup_execution_record_179(request178, execution179)
        alt = valid_rtm_blk_link_followup_execution_record_179(
            request178,
            requested_at="2099-05-16T22:17:00+10:00",
            expires_at="2099-05-16T22:24:00+10:00",
        )
        alt_package = build_rtm_blk_link_followup_execution_record_179(request178, alt)

        self.assertNotEqual(package["followup_execution_request_hash"], alt_package["followup_execution_request_hash"])
        self.assertNotEqual(package["followup_execution_package_hash"], alt_package["followup_execution_package_hash"])
        execution179["operator_attestation"]["rtm_generation_excluded"] = "mutated"
        request178["exact_trace_identities"].append("REQ:REQ-999:sha256:" + "f" * 64)
        self.assertIsNot(package["operator_attestation"], execution179["operator_attestation"])
        self.assertIs(package["operator_attestation"]["rtm_generation_excluded"], True)
        self.assertNotIn("REQ:REQ-999:sha256:" + "f" * 64, package["exact_trace_identities"])

    def test_module_has_no_live_runtime_tooling_or_protected_body_file_access(self):
        tree = ast.parse(MODULE.read_text())
        imported = set()
        calls = set()
        forbidden_imports = {"subprocess", "socket", "requests", "urllib3", "httpx", "shutil", "pathlib", "os"}
        forbidden_calls = {"system", "popen", "Popen", "run", "call", "check_call", "check_output", "exec", "eval", "open", "read_text", "urlopen", "request", "__import__"}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
            elif isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Attribute):
                    calls.add(func.attr)
                elif isinstance(func, ast.Name):
                    calls.add(func.id)
        self.assertEqual(imported & forbidden_imports, set())
        self.assertEqual(calls & forbidden_calls, set())


if __name__ == "__main__":
    unittest.main()
