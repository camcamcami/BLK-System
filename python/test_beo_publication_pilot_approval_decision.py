import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from beo_publication_pilot_execution_request import build_beo_publication_pilot_execution_request
from test_beo_publication_pilot_execution_request import valid_inputs as valid_request_inputs

from beo_publication_pilot_approval_decision import (
    APPROVAL_DECISION_CAPTURED,
    DECISION_SCOPE,
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS,
    build_beo_publication_pilot_approval_decision,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "beo_publication_pilot_approval_decision.py"


def valid_inputs():
    decision_package, execution_request = valid_request_inputs()
    request_package = build_beo_publication_pilot_execution_request(decision_package, execution_request)
    approval_decision = {
        "approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-001",
        "operator_identity": "discord:684235178083745819",
        "decision_scope": DECISION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_request_package_id": request_package["request_package_id"],
        "upstream_request_package_hash": request_package["request_package_hash"],
        "upstream_decision_package_id": request_package["upstream_decision_package_id"],
        "upstream_decision_package_hash": request_package["upstream_decision_package_hash"],
        "exact_beo_id": request_package["beo_id"],
        "exact_beo_hash": request_package["beo_hash"],
        "exact_target_id": request_package["target_id"],
        "approved_pilot_request_id": request_package["pilot_request_id"],
        "approval_id": request_package["future_approval_id_candidate"],
        "future_run_id": request_package["future_run_id_candidate"],
        "decision_result": "APPROVED_FOR_ONE_FUTURE_BEO_PUBLICATION_PILOT_EXECUTION_NOT_EXECUTED",
        "decided_at": "2099-05-12T14:00:00+10:00",
        "expires_at": "2099-05-12T15:00:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {
            "exact_blk085_request_reviewed": True,
            "approval_is_limited_to_one_future_pilot_execution_sprint": True,
            "publication_pilot_not_executed_by_this_decision": True,
            "signer_storage_ledger_rollback_side_effects_excluded": True,
            "rtm_generation_excluded": True,
            "protected_body_reads_excluded": True,
            "target_repo_scan_or_mutation_excluded": True,
            "no_runtime_side_effects": True,
        },
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    return request_package, approval_decision


def rehash_request_package(package):
    package["request_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "request_package_hash"}
    )
    return package


class BeoPublicationPilotApprovalDecisionTest(unittest.TestCase):
    def test_builds_exact_approval_decision_without_executing_publication_pilot(self):
        request_package, approval_decision = valid_inputs()

        package = build_beo_publication_pilot_approval_decision(request_package, approval_decision)

        self.assertEqual(package["approval_decision_status"], APPROVAL_DECISION_CAPTURED)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["decision_scope"], DECISION_SCOPE)
        self.assertEqual(package["upstream_request_package_id"], request_package["request_package_id"])
        self.assertEqual(package["upstream_request_package_hash"], request_package["request_package_hash"])
        self.assertEqual(package["upstream_decision_package_id"], request_package["upstream_decision_package_id"])
        self.assertEqual(package["upstream_decision_package_hash"], request_package["upstream_decision_package_hash"])
        self.assertEqual(package["beo_id"], request_package["beo_id"])
        self.assertEqual(package["beo_hash"], request_package["beo_hash"])
        self.assertEqual(package["target_id"], request_package["target_id"])
        self.assertEqual(package["target_ref"], request_package["target_ref"])
        self.assertEqual(package["approved_pilot_request_id"], request_package["pilot_request_id"])
        self.assertEqual(package["approval_id"], request_package["future_approval_id_candidate"])
        self.assertEqual(package["future_run_id"], request_package["future_run_id_candidate"])
        self.assertTrue(package["approval_decision_captured"])
        self.assertTrue(package["human_approval_granted"])
        self.assertTrue(package["publication_pilot_execution_approved_for_future_sprint"])
        self.assertFalse(package["publication_pilot_executed"])
        self.assertEqual(package["next_required_authority"], "EXACT_BEO_PUBLICATION_PILOT_EXECUTION_SPRINT_REQUIRED_NOT_RUN")
        self.assertEqual(package["beo_publication"], "APPROVAL_DECISION_CAPTURED_NOT_PUBLISHED")
        self.assertEqual(package["rtm_status"], "NOT_GENERATED")
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        self.assertIn("approval_decision_package_hash", package)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)

    def test_rejects_wrong_frontier_broad_decision_or_publication_side_effect_flags(self):
        request_package, approval_decision = valid_inputs()
        hostile_cases = [
            ({"selected_frontier": "beo_publication_pilot_execution"}, "selected_frontier must be beo_publication_pilot_approval_decision"),
            ({"secondary_frontier": "rtm_authority_request_after_publication_prerequisites"}, "forbidden authority field|unexpected field"),
            ({"decision_scope": "BEO_PUBLICATION_PILOT_APPROVAL_DECISION_AND_EXECUTION"}, "decision_scope must be"),
            ({"decision_result": "APPROVED_FOR_AUTHORITATIVE_BEO_PUBLICATION"}, "decision_result must be"),
            ({"publication_pilot_executed": True}, "forbidden authority field|unexpected field"),
            ({"publication_performed": True}, "forbidden authority field|unexpected field"),
            ({"signature_generated": True}, "forbidden authority field|unexpected field"),
        ]
        for patch, message in hostile_cases:
            decision = copy.deepcopy(approval_decision)
            decision.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_beo_publication_pilot_approval_decision(request_package, decision)

    def test_rejects_forged_or_mismatched_upstream_request_package(self):
        request_package, approval_decision = valid_inputs()

        forged = copy.deepcopy(request_package)
        forged["target_id"] = "BEO-PUBLICATION-TARGET-FORGED-086"
        with self.assertRaisesRegex(ValueError, "request_package_hash does not match canonical request package"):
            build_beo_publication_pilot_approval_decision(forged, approval_decision)

        forged = copy.deepcopy(request_package)
        forged["target_id"] = "BEO-PUBLICATION-TARGET-FORGED-086"
        rehash_request_package(forged)
        decision = copy.deepcopy(approval_decision)
        decision["upstream_request_package_hash"] = forged["request_package_hash"]
        decision["exact_target_id"] = forged["target_id"]
        with self.assertRaisesRegex(ValueError, "request package must match canonical BLK-085 fixture"):
            build_beo_publication_pilot_approval_decision(forged, decision)

        forged = copy.deepcopy(request_package)
        forged["request_status"] = "BEO_PUBLICATION_PILOT_EXECUTION_REQUEST_APPROVED"
        rehash_request_package(forged)
        decision = copy.deepcopy(approval_decision)
        decision["upstream_request_package_hash"] = forged["request_package_hash"]
        with self.assertRaisesRegex(ValueError, "request package must be BLK-085 request-ready"):
            build_beo_publication_pilot_approval_decision(forged, decision)

    def test_rejects_bad_expiry_replay_proof_obligations_and_denied_authorities(self):
        request_package, approval_decision = valid_inputs()
        hostile_cases = [
            ({"expired": True}, "approval decision must not be expired"),
            ({"replayed": True}, "approval decision must not be replayed"),
            ({"stale": True}, "approval decision must not be stale"),
            ({"expires_at": approval_decision["decided_at"]}, "expires_at must be after decided_at"),
            (
                {"decided_at": "2000-01-01T00:00:00+10:00", "expires_at": "2000-01-01T01:00:00+10:00"},
                "approval decision must not be calendar-expired",
            ),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS) + [sorted(EXACT_PROOF_OBLIGATIONS)[0]]}, "proof_obligations must not contain duplicates"),
            ({"excluded_authorities": ["NOPE"]}, "excluded_authorities must match exact denied authority set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES) + [sorted(EXACT_EXCLUDED_AUTHORITIES)[0]]}, "excluded_authorities must not contain duplicates"),
        ]
        for patch, message in hostile_cases:
            decision = copy.deepcopy(approval_decision)
            decision.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_beo_publication_pilot_approval_decision(request_package, decision)

    def test_requires_exact_fresh_ids_from_blk085_request(self):
        request_package, approval_decision = valid_inputs()
        reused = [
            ({"approval_decision_package_id": request_package["request_package_id"]}, "approval_decision_package_id must be fresh"),
            ({"approval_decision_package_id": request_package["pilot_request_id"]}, "approval_decision_package_id must be fresh"),
            ({"approval_decision_package_id": request_package["future_approval_id_candidate"]}, "approval decision package id must be distinct"),
            ({"approval_decision_package_id": request_package["future_run_id_candidate"]}, "approval_decision_package_id must be fresh"),
            ({"approval_id": "APPROVAL-BLK-SYSTEM-086-OTHER"}, "approval_id must equal BLK-085 future approval candidate"),
            ({"approval_id": request_package["request_package_id"]}, "approval_id must equal BLK-085 future approval candidate"),
            ({"future_run_id": "RUN-BLK-SYSTEM-086-OTHER"}, "future_run_id must equal BLK-085 future run candidate"),
            ({"future_run_id": request_package["future_approval_id_candidate"]}, "future_run_id must equal BLK-085 future run candidate"),
        ]
        for upstream_identity_key in ["upstream_decision_package_id", "envelope_id", "beo_id", "target_id", "candidate_id"]:
            reused.append(({"approval_decision_package_id": request_package[upstream_identity_key]}, "approval_decision_package_id must be fresh"))
        for patch, message in reused:
            decision = copy.deepcopy(approval_decision)
            decision.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_beo_publication_pilot_approval_decision(request_package, decision)

    def test_rejects_secret_adjacent_authority_source_git_and_tooling_laundering(self):
        request_package, approval_decision = valid_inputs()
        hostile_cases = [
            ({"operator_identity": "discord:684235178083745819-se%63ret"}, "secret-bearing field"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-approved-for-publication"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-publicationPilotExecuted"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-RTMGeneration"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-RTMAuthorized"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-beoPubApproved"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-ABPApproved"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-RTPBEO"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-RTMID"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-approvedForRuntimeExecution"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-liveExecutionAuthorized"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-runtimeApproval"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-publicationGreenlit"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-publicationAllowed"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-publicationPermitted"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-publicationAuthorityAllowed"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-publicationAuthorityPermitted"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-allowedForPublication"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-permittedForPublication"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-claimsAreAuthorized"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-isAuthorized"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-blkTestPassApproval"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-codexApproval"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-approvalInherited"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-SignatureGenerated"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-CryptographicSigning"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-live%45xecutionAuthorized"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-is%41uthorized"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-protectedBodyAuthorized"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-docs%252Factive"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-sourceGitAuthorized"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-packageManagersAuthorized"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-networkAccessAuthorized"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-modelServicesAuthorized"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-browserToolsAuthorized"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-cyberToolsAuthorized"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-signerAuthorized"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-storageAuthorized"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-ledgerAuthorized"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-rollbackAuthorityGranted"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-productionSandboxAuthorized"}, "authority-laundering text"),
            ({"sourceMutationAttempted": False}, "forbidden authority field|unexpected field"),
        ]
        for patch, message in hostile_cases:
            decision = copy.deepcopy(approval_decision)
            decision.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_beo_publication_pilot_approval_decision(request_package, decision)

    def test_requires_exact_approval_decision_package_id(self):
        request_package, approval_decision = valid_inputs()
        decision = copy.deepcopy(approval_decision)
        decision["approval_decision_package_id"] = "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-999"

        with self.assertRaisesRegex(ValueError, "approval_decision_package_id must equal BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-001"):
            build_beo_publication_pilot_approval_decision(request_package, decision)

    def test_module_has_no_live_runtime_or_external_tooling_imports_or_calls(self):
        tree = ast.parse(MODULE.read_text())
        forbidden_import_roots = {"subprocess", "socket", "requests", "urllib.request", "http", "shutil"}
        imported = set()
        calls = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    calls.append(node.func.attr)
                elif isinstance(node.func, ast.Name):
                    calls.append(node.func.id)
        self.assertFalse(any(name in forbidden_import_roots for name in imported), imported)
        for forbidden_call in ["Popen", "run", "system", "spawn", "check_call", "check_output", "urlopen", "request"]:
            self.assertNotIn(forbidden_call, calls)


if __name__ == "__main__":
    unittest.main()
