import ast
import copy
import json
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from beo_publication_pilot_execution import build_beo_publication_pilot_execution
from test_beo_publication_pilot_execution import valid_inputs as valid_blk087_inputs

from beo_publication_prerequisite_request_after_evidence_refresh import (
    CANONICAL_BLK087_EXECUTION_PACKAGE_HASH,
    CANONICAL_BLK087_PILOT_ARTIFACT_HASH,
    CANONICAL_BLK097_EVIDENCE_HASH,
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY,
    REQUEST_PACKAGE_ID,
    REQUEST_SCOPE,
    REQUEST_STATUS,
    SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS,
    build_beo_publication_prerequisite_request_after_evidence_refresh,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "beo_publication_prerequisite_request_after_evidence_refresh.py"
BLK097_EVIDENCE = ROOT / "docs" / "outcomes" / "BLK-SYSTEM-097_runtime-evidence.json"


def valid_inputs():
    runtime_evidence = json.loads(BLK097_EVIDENCE.read_text())
    approval_package, execution_request = valid_blk087_inputs()
    local_pilot_package = build_beo_publication_pilot_execution(approval_package, execution_request)
    request = {
        "request_package_id": REQUEST_PACKAGE_ID,
        "operator_identity": "discord:684235178083745819",
        "request_scope": REQUEST_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_blk097_evidence_hash": CANONICAL_BLK097_EVIDENCE_HASH,
        "upstream_blk087_execution_package_id": "BEO-PUBLICATION-PILOT-EXECUTION-087-001",
        "upstream_blk087_execution_package_hash": CANONICAL_BLK087_EXECUTION_PACKAGE_HASH,
        "upstream_blk087_pilot_artifact_hash": CANONICAL_BLK087_PILOT_ARTIFACT_HASH,
        "beo_id": "BEO-054-001",
        "beo_hash": "sha256:" + "a" * 64,
        "target_repo_path": "/home/dad/code/Kuronode-v1",
        "target_head_sha": "aebea51bed911c781a537d84d38b2dcb838b1368",
        "request_future_external_beo_publication_decision": True,
        "external_authoritative_publication_performed": False,
        "runtime_published_beo_output": False,
        "live_publication_approval_captured": False,
        "signer_key_material_accessed": False,
        "cryptographic_signature_generated": False,
        "immutable_storage_written": False,
        "public_ledger_mutated": False,
        "ledger_append_attempted": False,
        "rollback_executed": False,
        "revocation_executed": False,
        "supersession_executed": False,
        "rtm_generated": False,
        "rtm_drift_rejection_performed": False,
        "drift_decision_made": False,
        "active_vault_hash_comparison_performed": False,
        "coverage_claim_promoted": False,
        "protected_body_read": False,
        "target_repo_scanned": False,
        "target_repo_mutated": False,
        "source_mutation_attempted": False,
        "git_mutation_attempted": False,
        "beb_dispatch_authorized": False,
        "beo_closeout_execution_authorized": False,
        "blk_pipe_execution_authorized": False,
        "blk_test_runtime_authorized": False,
        "codex_live_execution_authorized": False,
        "package_network_model_browser_cyber_tooling_authorized": False,
        "production_isolation_claimed": False,
        "requested_at": "2026-05-13T17:00:00+10:00",
        "expires_at": "2026-05-14T17:00:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {
            "exact_blk097_evidence_reviewed": True,
            "exact_blk087_local_pilot_reviewed": True,
            "fresh_blk_test_pass_is_evidence_not_publication_approval": True,
            "local_pilot_artifact_is_not_external_publication": True,
            "request_is_for_future_human_decision_not_granted": True,
            "signer_storage_ledger_rollback_side_effects_excluded": True,
            "rtm_generation_and_drift_excluded": True,
            "protected_body_reads_excluded": True,
            "target_source_git_mutation_excluded": True,
            "no_adjacent_runtime_side_effects": True,
        },
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    return runtime_evidence, local_pilot_package, request


def rehash_package(package):
    package["execution_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "execution_package_hash"}
    )
    return package


class BeoPublicationPrerequisiteRequestAfterEvidenceRefreshTest(unittest.TestCase):
    def test_builds_review_only_request_bound_to_fresh_blk097_and_local_blk087_evidence(self):
        runtime_evidence, local_pilot_package, request = valid_inputs()

        package = build_beo_publication_prerequisite_request_after_evidence_refresh(
            runtime_evidence, local_pilot_package, request
        )

        self.assertEqual(package["request_status"], REQUEST_STATUS)
        self.assertEqual(package["request_package_id"], REQUEST_PACKAGE_ID)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["request_scope"], REQUEST_SCOPE)
        self.assertEqual(package["next_required_authority"], NEXT_REQUIRED_AUTHORITY)
        self.assertEqual(package["upstream_blk097_evidence_hash"], CANONICAL_BLK097_EVIDENCE_HASH)
        self.assertEqual(package["upstream_blk087_execution_package_hash"], CANONICAL_BLK087_EXECUTION_PACKAGE_HASH)
        self.assertEqual(package["upstream_blk087_pilot_artifact_hash"], CANONICAL_BLK087_PILOT_ARTIFACT_HASH)
        self.assertEqual(package["beo_id"], "BEO-054-001")
        self.assertEqual(package["target_repo_path"], "/home/dad/code/Kuronode-v1")
        self.assertEqual(package["target_head_sha"], "aebea51bed911c781a537d84d38b2dcb838b1368")
        self.assertTrue(package["future_external_publication_decision_requested"])
        self.assertFalse(package["external_publication_approval_granted"])
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertIn("request_package_hash", package)
        self.assertEqual(
            package["request_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "request_package_hash"}),
        )

    def test_rejects_non_pass_or_mutating_blk097_evidence(self):
        hostile_cases = [
            ({"status": "FAIL"}, "BLK-SYSTEM-097 evidence status must be PASS"),
            ({"pilot_status": "BLK_TEST_KURONODE_WORKSPACE_BOUNDED_EVIDENCE_REFRESH_FAIL_EVIDENCE_ONLY"}, "pilot_status must be"),
            ({"findings_count": 1, "findings": [{"id": "F-001"}]}, "findings_count must be 0"),
            ({"approval_id": "APPROVAL-BLK-SYSTEM-073-KURONODE-READONLY-001"}, "approval_id must be"),
            ({"run_id": "RUN-BLK-SYSTEM-073-KURONODE-READONLY-001"}, "run_id must be"),
            ({"target_repo_path": "/home/dad/code/Kuronode-v1/."}, "target_repo_path must be exact"),
            ({"expected_head": "deadbeef"}, "expected_head must be"),
            ({"observed_remote_head": "deadbeef"}, "observed_remote_head must be"),
            ({"source_mutation_detected": True}, "source_mutation_detected must remain false"),
            ({"git_mutation_detected": True}, "git_mutation_detected must remain false"),
            ({"protected_body_read": True}, "protected_body_read must remain false"),
            ({"coverage_claim_promoted": True}, "coverage_claim_promoted must remain false"),
            ({"beo_publication": "PUBLISHED"}, "beo_publication must remain DRAFT_ONLY"),
            ({"rtm_status": "GENERATED"}, "rtm_status must remain NOT_GENERATED"),
            ({"public_ledger_mutation": True}, "public_ledger_mutation must remain false"),
            ({"network_called": True}, "network_called must remain false"),
            ({"production_isolation_claimed": True}, "production_isolation_claimed must remain false"),
        ]
        for patch, message in hostile_cases:
            runtime_evidence, local_pilot_package, request = valid_inputs()
            runtime_evidence.update(patch)
            if "findings_count" in patch:
                runtime_evidence["findings_emitted_count"] = 1
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_beo_publication_prerequisite_request_after_evidence_refresh(
                        runtime_evidence, local_pilot_package, request
                    )

    def test_rejects_forged_or_mismatched_local_pilot_package(self):
        runtime_evidence, local_pilot_package, request = valid_inputs()
        forged = copy.deepcopy(local_pilot_package)
        forged["target_id"] = "BEO-PUBLICATION-TARGET-FORGED-098"
        with self.assertRaisesRegex(ValueError, "BLK-SYSTEM-087 package hash does not match submitted package"):
            build_beo_publication_prerequisite_request_after_evidence_refresh(runtime_evidence, forged, request)

        runtime_evidence, local_pilot_package, request = valid_inputs()
        forged = copy.deepcopy(local_pilot_package)
        forged["target_id"] = "BEO-PUBLICATION-TARGET-FORGED-098"
        rehash_package(forged)
        request["upstream_blk087_execution_package_hash"] = forged["execution_package_hash"]
        with self.assertRaisesRegex(ValueError, "BLK-SYSTEM-087 package must match canonical local pilot fixture"):
            build_beo_publication_prerequisite_request_after_evidence_refresh(runtime_evidence, forged, request)

        runtime_evidence, local_pilot_package, request = valid_inputs()
        forged = copy.deepcopy(local_pilot_package)
        forged["beo_publication"] = "EXTERNAL_AUTHORITATIVE_PUBLICATION"
        rehash_package(forged)
        request["upstream_blk087_execution_package_hash"] = forged["execution_package_hash"]
        with self.assertRaisesRegex(ValueError, "BLK-SYSTEM-087 package must match canonical local pilot fixture"):
            build_beo_publication_prerequisite_request_after_evidence_refresh(runtime_evidence, forged, request)

    def test_rejects_request_side_effect_flags_bad_proof_sets_and_duplicate_denials(self):
        side_effect_cases = [
            ({"selected_frontier": "external_authoritative_publication_execution"}, "selected_frontier must be"),
            ({"request_scope": "REQUEST_AND_PUBLICATION"}, "request_scope must be"),
            ({"request_future_external_beo_publication_decision": False}, "request_future_external_beo_publication_decision must be true"),
            ({"external_authoritative_publication_performed": True}, "external_authoritative_publication_performed must remain false"),
            ({"runtime_published_beo_output": True}, "runtime_published_beo_output must remain false"),
            ({"live_publication_approval_captured": True}, "live_publication_approval_captured must remain false"),
            ({"signer_key_material_accessed": True}, "signer_key_material_accessed must remain false"),
            ({"cryptographic_signature_generated": True}, "cryptographic_signature_generated must remain false"),
            ({"immutable_storage_written": True}, "immutable_storage_written must remain false"),
            ({"public_ledger_mutated": True}, "public_ledger_mutated must remain false"),
            ({"rollback_executed": True}, "rollback_executed must remain false"),
            ({"rtm_generated": True}, "rtm_generated must remain false"),
            ({"rtm_drift_rejection_performed": True}, "rtm_drift_rejection_performed must remain false"),
            ({"active_vault_hash_comparison_performed": True}, "active_vault_hash_comparison_performed must remain false"),
            ({"target_repo_mutated": True}, "target_repo_mutated must remain false"),
            ({"blk_pipe_execution_authorized": True}, "blk_pipe_execution_authorized must remain false"),
            ({"expired": True}, "request must not be expired"),
            ({"replayed": True}, "request must not be replayed"),
            ({"stale": True}, "request must not be stale"),
            ({"expires_at": "2026-05-13T17:00:00+10:00"}, "expires_at must be after requested_at"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS) + [sorted(EXACT_PROOF_OBLIGATIONS)[0]]}, "proof_obligations must not contain duplicates"),
            ({"excluded_authorities": ["NOPE"]}, "excluded_authorities must match exact denied authority set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES) + [sorted(EXACT_EXCLUDED_AUTHORITIES)[0]]}, "excluded_authorities must not contain duplicates"),
        ]
        for patch, message in side_effect_cases:
            runtime_evidence, local_pilot_package, request = valid_inputs()
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_beo_publication_prerequisite_request_after_evidence_refresh(
                        runtime_evidence, local_pilot_package, request
                    )

    def test_rejects_authority_laundering_and_protected_path_variants(self):
        hostile_cases = [
            ({"request_package_id": "BEO publication authorized"}, "authority-laundering text"),
            ({"operator_identity": "publication authority granted"}, "authority-laundering text"),
            ({"selected_frontier": "authoritativeBEOpublicationIsAuthorized"}, "selected_frontier must be"),
            ({"target_repo_path": "docs%252Factive%252FREQ-001.md"}, "target_repo_path must be exact"),
            ({"operator_attestation": {"exact_blk097_evidence_reviewed": True, "RTMGeneration": True}}, "unexpected field"),
            ({"operator_attestation": {"exact_blk097_evidence_reviewed": True, "privateKey": "SECRET"}}, "unexpected field"),
            ({"operator_attestation": valid_inputs()[2]["operator_attestation"] | {"notes": "BEO publication greenlit"}}, "unexpected field"),
        ]
        for patch, message in hostile_cases:
            runtime_evidence, local_pilot_package, request = valid_inputs()
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_beo_publication_prerequisite_request_after_evidence_refresh(
                        runtime_evidence, local_pilot_package, request
                    )

        runtime_evidence, local_pilot_package, request = valid_inputs()
        runtime_evidence["evidence_ref"] = "https://example.invalid/?file=docs%2Factive%2FREQ-001.md"
        with self.assertRaisesRegex(ValueError, "unexpected BLK-SYSTEM-097 evidence field"):
            build_beo_publication_prerequisite_request_after_evidence_refresh(
                runtime_evidence, local_pilot_package, request
            )

    def test_returned_package_defensively_copies_hash_bound_nested_inputs(self):
        runtime_evidence, local_pilot_package, request = valid_inputs()
        package = build_beo_publication_prerequisite_request_after_evidence_refresh(
            runtime_evidence, local_pilot_package, request
        )

        self.assertIsNot(package["blk097_evidence_summary"]["files_checked"], runtime_evidence["files_checked"])
        self.assertIsNot(package["blk087_trace_artifacts"], local_pilot_package["trace_artifacts"])
        self.assertIsNot(package["operator_attestation"], request["operator_attestation"])

        runtime_evidence["files_checked"].append("authorityLaundering.ts")
        local_pilot_package["trace_artifacts"][0]["id"] = "AUTHORITATIVEBEO"
        request["operator_attestation"]["exact_blk097_evidence_reviewed"] = False

        self.assertEqual(package["blk097_evidence_summary"]["files_checked"], ["smoke_test.ts"])
        self.assertEqual(package["blk087_trace_artifacts"][0]["id"], "REQ-001")
        self.assertTrue(package["operator_attestation"]["exact_blk097_evidence_reviewed"])
        self.assertEqual(
            package["request_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "request_package_hash"}),
        )

    def test_module_has_no_live_runtime_or_external_side_effect_imports(self):
        tree = ast.parse(MODULE.read_text())
        imported = set()
        calls = set()
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
        forbidden_imports = {"subprocess", "socket", "requests", "urllib3", "httpx"}
        forbidden_calls = {"system", "popen", "Popen", "run", "call", "check_call", "check_output", "exec", "eval", "open"}
        self.assertEqual(imported & forbidden_imports, set())
        self.assertEqual(calls & forbidden_calls, set())


if __name__ == "__main__":
    unittest.main()
