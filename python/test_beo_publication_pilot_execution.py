import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from beo_publication_pilot_approval_decision import build_beo_publication_pilot_approval_decision
from test_beo_publication_pilot_approval_decision import valid_inputs as valid_approval_inputs

from beo_publication_pilot_execution import (
    EXECUTION_PACKAGE_ID,
    EXECUTION_SCOPE,
    EXECUTION_STATUS,
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY,
    SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS,
    build_beo_publication_pilot_execution,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "beo_publication_pilot_execution.py"


def valid_inputs():
    request_package, approval_decision = valid_approval_inputs()
    approval_package = build_beo_publication_pilot_approval_decision(request_package, approval_decision)
    execution_request = {
        "execution_package_id": EXECUTION_PACKAGE_ID,
        "operator_identity": "discord:684235178083745819",
        "execution_scope": EXECUTION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "approval_decision_package_id": approval_package["approval_decision_package_id"],
        "approval_decision_package_hash": approval_package["approval_decision_package_hash"],
        "approval_id": approval_package["approval_id"],
        "run_id": approval_package["future_run_id"],
        "beo_id": approval_package["beo_id"],
        "beo_hash": approval_package["beo_hash"],
        "target_id": approval_package["target_id"],
        "target_ref": approval_package["target_ref"],
        "execute_publication_pilot": True,
        "authoritative_external_publication": False,
        "live_approval_capture": False,
        "signer_key_material_access": False,
        "cryptographic_signing": False,
        "immutable_storage_write": False,
        "public_ledger_mutation": False,
        "rollback_revocation_supersession_execution": False,
        "rtm_generation": False,
        "drift_rejection": False,
        "protected_body_reads": False,
        "target_repo_scan_or_mutation": False,
        "source_or_git_mutation_by_fixture": False,
        "blk_test_codex_blk_pipe_runtime": False,
        "package_network_model_browser_cyber_tooling": False,
        "production_isolation_claim": False,
        "requested_at": "2099-05-12T14:30:00+10:00",
        "expires_at": "2099-05-12T14:45:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {
            "exact_blk086_approval_decision_reviewed": True,
            "run_id_consumed_once_for_local_pilot": True,
            "local_pilot_output_not_external_authoritative_publication": True,
            "signer_storage_ledger_rollback_side_effects_excluded": True,
            "rtm_generation_excluded": True,
            "protected_body_reads_excluded": True,
            "target_repo_scan_or_mutation_excluded": True,
            "no_adjacent_runtime_side_effects": True,
        },
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    return approval_package, execution_request


def rehash_approval_package(package):
    package["approval_decision_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "approval_decision_package_hash"}
    )
    return package


class BeoPublicationPilotExecutionTest(unittest.TestCase):
    def test_builds_exact_local_pilot_publication_output_without_adjacent_side_effects(self):
        approval_package, execution_request = valid_inputs()

        package = build_beo_publication_pilot_execution(approval_package, execution_request)

        self.assertEqual(package["execution_status"], EXECUTION_STATUS)
        self.assertEqual(package["execution_package_id"], EXECUTION_PACKAGE_ID)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["execution_scope"], EXECUTION_SCOPE)
        self.assertEqual(package["approval_decision_package_id"], approval_package["approval_decision_package_id"])
        self.assertEqual(package["approval_decision_package_hash"], approval_package["approval_decision_package_hash"])
        self.assertEqual(package["approval_id"], approval_package["approval_id"])
        self.assertEqual(package["run_id_consumed"], approval_package["future_run_id"])
        self.assertEqual(package["beo_id"], approval_package["beo_id"])
        self.assertEqual(package["beo_hash"], approval_package["beo_hash"])
        self.assertEqual(package["target_id"], approval_package["target_id"])
        self.assertEqual(package["target_ref"], approval_package["target_ref"])
        self.assertTrue(package["publication_pilot_executed"])
        self.assertTrue(package["future_run_id_consumed"])
        self.assertTrue(package["local_pilot_publication_artifact_emitted"])
        self.assertEqual(package["beo_publication"], "PILOT_LOCAL_PUBLISHED_BEO_OUTPUT_NOT_AUTHORITATIVE")
        self.assertEqual(package["rtm_status"], "NOT_GENERATED")
        self.assertEqual(package["next_required_authority"], NEXT_REQUIRED_AUTHORITY)
        self.assertIn("pilot_publication_artifact", package)
        artifact = package["pilot_publication_artifact"]
        self.assertEqual(artifact["published_beo_id"], approval_package["beo_id"])
        self.assertEqual(artifact["publication_mode"], "LOCAL_DETERMINISTIC_PILOT_ONLY")
        self.assertEqual(artifact["signature_status"], "NOT_SIGNED_NO_KEY_MATERIAL")
        self.assertEqual(artifact["storage_status"], "NOT_WRITTEN_LOCAL_RECEIPT_ONLY")
        self.assertEqual(artifact["ledger_status"], "NOT_APPENDED_LOCAL_RECEIPT_ONLY")
        self.assertEqual(artifact["rollback_status"], "NOT_EXECUTED_POLICY_BOUND_ONLY")
        self.assertEqual(artifact["rtm_status"], "NOT_GENERATED")
        self.assertIn("pilot_publication_artifact_hash", package)
        self.assertIn("execution_package_hash", package)
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)

    def test_rejects_wrong_frontier_or_adjacent_side_effect_flags(self):
        approval_package, execution_request = valid_inputs()
        hostile_cases = [
            ({"selected_frontier": "authoritative_beo_publication"}, "selected_frontier must be"),
            ({"execution_scope": "EXACT_BEO_PUBLICATION_PILOT_AND_RTM_GENERATION"}, "execution_scope must be"),
            ({"execute_publication_pilot": False}, "execute_publication_pilot must be true"),
            ({"authoritative_external_publication": True}, "authoritative_external_publication must remain false"),
            ({"live_approval_capture": True}, "live_approval_capture must remain false"),
            ({"signer_key_material_access": True}, "signer_key_material_access must remain false"),
            ({"cryptographic_signing": True}, "cryptographic_signing must remain false"),
            ({"immutable_storage_write": True}, "immutable_storage_write must remain false"),
            ({"public_ledger_mutation": True}, "public_ledger_mutation must remain false"),
            ({"rollback_revocation_supersession_execution": True}, "rollback_revocation_supersession_execution must remain false"),
            ({"rtm_generation": True}, "rtm_generation must remain false"),
            ({"protected_body_reads": True}, "protected_body_reads must remain false"),
            ({"target_repo_scan_or_mutation": True}, "target_repo_scan_or_mutation must remain false"),
        ]
        for patch, message in hostile_cases:
            request = copy.deepcopy(execution_request)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_beo_publication_pilot_execution(approval_package, request)

    def test_rejects_forged_or_mismatched_upstream_approval_package(self):
        approval_package, execution_request = valid_inputs()

        forged = copy.deepcopy(approval_package)
        forged["target_id"] = "BEO-PUBLICATION-TARGET-FORGED-087"
        with self.assertRaisesRegex(ValueError, "approval_decision_package_hash does not match canonical approval package"):
            build_beo_publication_pilot_execution(forged, execution_request)

        forged = copy.deepcopy(approval_package)
        forged["target_id"] = "BEO-PUBLICATION-TARGET-FORGED-087"
        rehash_approval_package(forged)
        request = copy.deepcopy(execution_request)
        request["approval_decision_package_hash"] = forged["approval_decision_package_hash"]
        request["target_id"] = forged["target_id"]
        with self.assertRaisesRegex(ValueError, "approval package must match canonical BLK-086 fixture"):
            build_beo_publication_pilot_execution(forged, request)

        forged = copy.deepcopy(approval_package)
        forged["publication_pilot_executed"] = True
        rehash_approval_package(forged)
        request = copy.deepcopy(execution_request)
        request["approval_decision_package_hash"] = forged["approval_decision_package_hash"]
        with self.assertRaisesRegex(ValueError, "approval package must remain not executed"):
            build_beo_publication_pilot_execution(forged, request)

        forged = copy.deepcopy(approval_package)
        forged["decided_at"] = "2099-05-12T13:00:00+10:00"
        forged["expires_at"] = "2099-05-12T13:30:00+10:00"
        rehash_approval_package(forged)
        request = copy.deepcopy(execution_request)
        request["approval_decision_package_hash"] = forged["approval_decision_package_hash"]
        with self.assertRaisesRegex(ValueError, "approval package must match canonical BLK-086 fixture"):
            build_beo_publication_pilot_execution(forged, request)

        forged = copy.deepcopy(approval_package)
        forged["operator_attestation"]["exact_blk085_request_reviewed"] = False
        rehash_approval_package(forged)
        request = copy.deepcopy(execution_request)
        request["approval_decision_package_hash"] = forged["approval_decision_package_hash"]
        with self.assertRaisesRegex(ValueError, "approval package must match canonical BLK-086 fixture"):
            build_beo_publication_pilot_execution(forged, request)

    def test_rejects_bad_expiry_replay_proof_obligations_and_denied_authorities(self):
        approval_package, execution_request = valid_inputs()
        hostile_cases = [
            ({"expired": True}, "execution request must not be expired"),
            ({"replayed": True}, "execution request must not be replayed"),
            ({"stale": True}, "execution request must not be stale"),
            ({"expires_at": execution_request["requested_at"]}, "expires_at must be after requested_at"),
            ({"requested_at": "2000-01-01T00:00:00+10:00", "expires_at": "2000-01-01T01:00:00+10:00"}, "execution request must not be calendar-expired"),
            ({"requested_at": "2099-05-12T13:30:00+10:00", "expires_at": "2099-05-12T14:30:00+10:00"}, "execution request must not predate BLK-086 approval decision"),
            ({"requested_at": "2099-05-12T14:59:00+10:00", "expires_at": "2099-05-12T16:00:00+10:00"}, "execution request window must end within BLK-086 approval expiry"),
            ({"requested_at": "2099-05-12T15:00:00+10:00", "expires_at": "2099-05-12T15:01:00+10:00"}, "execution request must be within BLK-086 approval expiry"),
            ({"requested_at": "2099-05-12T15:01:00+10:00", "expires_at": "2099-05-12T15:30:00+10:00"}, "execution request must be within BLK-086 approval expiry"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS) + [sorted(EXACT_PROOF_OBLIGATIONS)[0]]}, "proof_obligations must not contain duplicates"),
            ({"excluded_authorities": ["NOPE"]}, "excluded_authorities must match exact denied authority set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES) + [sorted(EXACT_EXCLUDED_AUTHORITIES)[0]]}, "excluded_authorities must not contain duplicates"),
        ]
        for patch, message in hostile_cases:
            request = copy.deepcopy(execution_request)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_beo_publication_pilot_execution(approval_package, request)

    def test_returned_package_defensively_copies_hash_bound_nested_inputs(self):
        approval_package, execution_request = valid_inputs()

        package = build_beo_publication_pilot_execution(approval_package, execution_request)

        self.assertIsNot(package["trace_artifacts"], approval_package["trace_artifacts"])
        self.assertIsNot(package["trace_artifacts"][0], approval_package["trace_artifacts"][0])
        self.assertIsNot(package["pilot_publication_artifact"]["trace_artifacts"], approval_package["trace_artifacts"])
        self.assertIsNot(package["operator_attestation"], execution_request["operator_attestation"])

        approval_package["trace_artifacts"][0]["id"] = "RTM-ID-LAUNDERED-AFTER-HASH"
        execution_request["operator_attestation"]["no_adjacent_runtime_side_effects"] = "mutated-after-hash"

        self.assertNotEqual(package["trace_artifacts"][0]["id"], "RTM-ID-LAUNDERED-AFTER-HASH")
        self.assertIs(package["operator_attestation"]["no_adjacent_runtime_side_effects"], True)
        self.assertEqual(
            package["pilot_publication_artifact_hash"],
            _canonical_hash(
                {
                    key: value
                    for key, value in package["pilot_publication_artifact"].items()
                    if key != "pilot_publication_artifact_hash"
                }
            ),
        )
        self.assertEqual(
            package["execution_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "execution_package_hash"}),
        )

    def test_requires_exact_ids_from_blk086_approval_decision(self):
        approval_package, execution_request = valid_inputs()
        hostile_cases = [
            ({"execution_package_id": "BEO-PUBLICATION-PILOT-EXECUTION-087-999"}, "execution_package_id must equal"),
            ({"execution_package_id": approval_package["approval_decision_package_id"]}, "execution_package_id must be fresh"),
            ({"approval_id": "APPROVAL-BLK-SYSTEM-087-OTHER"}, "approval_id must equal BLK-086 approval id"),
            ({"run_id": "RUN-BLK-SYSTEM-087-OTHER"}, "run_id must equal BLK-086 future run id"),
            ({"run_id": approval_package["approval_id"]}, "run_id must equal BLK-086 future run id"),
        ]
        for upstream_identity_key in ["upstream_request_package_id", "upstream_decision_package_id", "envelope_id", "beo_id", "target_id", "candidate_id"]:
            hostile_cases.append(({"execution_package_id": approval_package[upstream_identity_key]}, "execution_package_id must be fresh"))
        for patch, message in hostile_cases:
            request = copy.deepcopy(execution_request)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_beo_publication_pilot_execution(approval_package, request)

    def test_rejects_secret_adjacent_authority_source_git_and_tooling_laundering(self):
        approval_package, execution_request = valid_inputs()
        hostile_cases = [
            ({"operator_identity": "discord:684235178083745819-se%63ret"}, "secret-bearing field"),
            ({"execution_package_id": "BEO-PUBLICATION-PILOT-EXECUTION-087-RTMGeneration"}, "authority-laundering text"),
            ({"execution_package_id": "BEO-PUBLICATION-PILOT-EXECUTION-087-RTMID"}, "authority-laundering text"),
            ({"execution_package_id": "BEO-PUBLICATION-PILOT-EXECUTION-087-SignatureGenerated"}, "authority-laundering text"),
            ({"execution_package_id": "BEO-PUBLICATION-PILOT-EXECUTION-087-CryptographicSigning"}, "authority-laundering text"),
            ({"execution_package_id": "BEO-PUBLICATION-PILOT-EXECUTION-087-docs%252Factive"}, "authority-laundering text"),
            ({"execution_package_id": "BEO-PUBLICATION-PILOT-EXECUTION-087-sourceGitAuthorized"}, "authority-laundering text"),
            ({"execution_package_id": "BEO-PUBLICATION-PILOT-EXECUTION-087-packageManagersAuthorized"}, "authority-laundering text"),
            ({"execution_package_id": "BEO-PUBLICATION-PILOT-EXECUTION-087-networkAccessAuthorized"}, "authority-laundering text"),
            ({"execution_package_id": "BEO-PUBLICATION-PILOT-EXECUTION-087-modelServicesAuthorized"}, "authority-laundering text"),
            ({"execution_package_id": "BEO-PUBLICATION-PILOT-EXECUTION-087-browserToolsAuthorized"}, "authority-laundering text"),
            ({"execution_package_id": "BEO-PUBLICATION-PILOT-EXECUTION-087-cyberToolsAuthorized"}, "authority-laundering text"),
            ({"execution_package_id": "BEO-PUBLICATION-PILOT-EXECUTION-087-signerAuthorized"}, "authority-laundering text"),
            ({"execution_package_id": "BEO-PUBLICATION-PILOT-EXECUTION-087-storageAuthorized"}, "authority-laundering text"),
            ({"execution_package_id": "BEO-PUBLICATION-PILOT-EXECUTION-087-ledgerAuthorized"}, "authority-laundering text"),
            ({"execution_package_id": "BEO-PUBLICATION-PILOT-EXECUTION-087-rollbackAuthorityGranted"}, "authority-laundering text"),
            ({"execution_package_id": "BEO-PUBLICATION-PILOT-EXECUTION-087-productionSandboxAuthorized"}, "authority-laundering text"),
            ({"sourceMutationAttempted": False}, "forbidden authority field|unexpected field"),
        ]
        for patch, message in hostile_cases:
            request = copy.deepcopy(execution_request)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_beo_publication_pilot_execution(approval_package, request)

    def test_module_does_not_import_or_call_live_execution_tooling(self):
        tree = ast.parse(MODULE.read_text())
        imported = set()
        called = set()
        forbidden_imports = {"subprocess", "socket", "requests", "urllib.request", "http.client", "pathlib"}
        forbidden_calls = {"open", "exec", "eval", "__import__"}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
            if isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Name):
                    called.add(func.id)
                elif isinstance(func, ast.Attribute):
                    called.add(func.attr)
        self.assertEqual(imported & forbidden_imports, set())
        self.assertEqual(called & forbidden_calls, set())


if __name__ == "__main__":
    unittest.main()
