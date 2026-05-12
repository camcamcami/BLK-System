import ast
import copy
import unittest
from pathlib import Path

from beo_publication_decision_package import build_beo_publication_decision_package
from test_beo_publication_decision_package import valid_inputs as valid_decision_inputs

from beo_publication_pilot_execution_request import (
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    REQUEST_READY,
    SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS,
    build_beo_publication_pilot_execution_request,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "beo_publication_pilot_execution_request.py"


def valid_inputs():
    envelope, decision_request = valid_decision_inputs()
    decision_package = build_beo_publication_decision_package(envelope, decision_request)
    execution_request = {
        "request_package_id": "BEO-PUBLICATION-PILOT-EXECUTION-REQUEST-085-001",
        "operator_identity": "discord:684235178083745819",
        "request_scope": "BEO_PUBLICATION_PILOT_EXECUTION_REQUEST_GATE_ONLY_NOT_APPROVAL_NOT_EXECUTION",
        "selected_frontier": SELECTED_FRONTIER,
        "requested_at": "2099-05-12T12:30:00+10:00",
        "expires_at": "2099-05-12T13:30:00+10:00",
        "upstream_decision_package_id": decision_package["decision_package_id"],
        "upstream_decision_package_hash": decision_package["decision_package_hash"],
        "exact_beo_id": decision_package["beo_id"],
        "exact_beo_hash": decision_package["beo_hash"],
        "exact_target_id": decision_package["target_id"],
        "pilot_request_id": "BEO-PUBLICATION-PILOT-EXECUTION-REQUEST-085-PILOT-001",
        "future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001",
        "future_run_id_candidate": "RUN-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001",
        "approval_granted": False,
        "publication_approved": False,
        "pilot_execution_authorized": False,
        "publication_performed": False,
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {
            "request_package_not_approval": True,
            "pilot_requires_future_explicit_human_approval": True,
            "publication_not_performed": True,
            "rtm_generation_excluded": True,
            "protected_body_reads_excluded": True,
            "no_side_effects": True,
        },
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    return decision_package, execution_request


def rehash_decision_package(package):
    from authoritative_beo_publication_authority_request import _canonical_hash

    package["decision_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "decision_package_hash"}
    )
    return package


class BeoPublicationPilotExecutionRequestTest(unittest.TestCase):
    def test_builds_request_ready_package_without_approval_or_execution(self):
        decision_package, execution_request = valid_inputs()

        package = build_beo_publication_pilot_execution_request(decision_package, execution_request)

        self.assertEqual(package["request_status"], REQUEST_READY)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["request_scope"], "BEO_PUBLICATION_PILOT_EXECUTION_REQUEST_GATE_ONLY_NOT_APPROVAL_NOT_EXECUTION")
        self.assertEqual(package["upstream_decision_package_id"], decision_package["decision_package_id"])
        self.assertEqual(package["upstream_decision_package_hash"], decision_package["decision_package_hash"])
        self.assertEqual(package["beo_id"], decision_package["beo_id"])
        self.assertEqual(package["beo_hash"], decision_package["beo_hash"])
        self.assertEqual(package["target_id"], decision_package["target_id"])
        self.assertEqual(package["target_ref"], decision_package["target_ref"])
        self.assertEqual(package["source_evidence_hash"], decision_package["source_evidence_hash"])
        self.assertEqual(package["trace_artifacts"], decision_package["trace_artifacts"])
        self.assertTrue(package["approval_required_before_execution"])
        self.assertEqual(package["next_required_authority"], "EXPLICIT_HUMAN_PUBLICATION_PILOT_APPROVAL_REQUIRED_NOT_GRANTED")
        self.assertEqual(package["beo_publication"], "PILOT_EXECUTION_REQUEST_ONLY_NOT_APPROVED_NOT_PUBLISHED")
        self.assertEqual(package["rtm_status"], "NOT_GENERATED")
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        self.assertIn("request_package_hash", package)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)

    def test_rejects_wrong_or_multiple_frontiers_and_positive_authority_flags(self):
        decision_package, execution_request = valid_inputs()
        hostile_cases = [
            ({"selected_frontier": "bounded_blk_test_evidence_refresh"}, "selected_frontier must be beo_publication_pilot_execution_request"),
            ({"secondary_frontier": "rtm_authority_request_after_publication_prerequisites"}, "forbidden authority field|unexpected field"),
            ({"approval_granted": True}, "approval_granted must remain false"),
            ({"publication_approved": True}, "publication_approved must remain false"),
            ({"pilot_execution_authorized": True}, "pilot_execution_authorized must remain false"),
            ({"publication_performed": True}, "publication_performed must remain false"),
        ]
        for patch, message in hostile_cases:
            request = copy.deepcopy(execution_request)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_beo_publication_pilot_execution_request(decision_package, request)

    def test_rejects_forged_or_mismatched_upstream_decision_package(self):
        decision_package, execution_request = valid_inputs()
        forged = copy.deepcopy(decision_package)
        forged["target_id"] = "BEO-PUBLICATION-TARGET-FORGED-085"
        with self.assertRaisesRegex(ValueError, "decision_package_hash does not match canonical decision package"):
            build_beo_publication_pilot_execution_request(forged, execution_request)

        forged = copy.deepcopy(decision_package)
        forged["target_id"] = "BEO-PUBLICATION-TARGET-FORGED-085"
        rehash_decision_package(forged)
        request = copy.deepcopy(execution_request)
        request["upstream_decision_package_hash"] = forged["decision_package_hash"]
        with self.assertRaisesRegex(ValueError, "exact_target_id does not match decision package"):
            build_beo_publication_pilot_execution_request(forged, request)

        forged = copy.deepcopy(decision_package)
        forged["target_id"] = "BEO-PUBLICATION-TARGET-FORGED-085"
        rehash_decision_package(forged)
        request = copy.deepcopy(execution_request)
        request["upstream_decision_package_hash"] = forged["decision_package_hash"]
        request["exact_target_id"] = forged["target_id"]
        with self.assertRaisesRegex(ValueError, "decision package must match canonical BLK-083 fixture"):
            build_beo_publication_pilot_execution_request(forged, request)

        forged = copy.deepcopy(decision_package)
        forged["beo_id"] = "BEO-FORGED-085-001"
        forged["beo_hash"] = "sha256:" + "9" * 64
        rehash_decision_package(forged)
        request = copy.deepcopy(execution_request)
        request["upstream_decision_package_hash"] = forged["decision_package_hash"]
        request["exact_beo_id"] = forged["beo_id"]
        request["exact_beo_hash"] = forged["beo_hash"]
        with self.assertRaisesRegex(ValueError, "decision package must match canonical BLK-083 fixture"):
            build_beo_publication_pilot_execution_request(forged, request)

        forged = copy.deepcopy(decision_package)
        forged["decision_status"] = "BEO_PUBLICATION_DECISION_PACKAGE_PUBLISHED"
        rehash_decision_package(forged)
        request = copy.deepcopy(execution_request)
        request["upstream_decision_package_hash"] = forged["decision_package_hash"]
        with self.assertRaisesRegex(ValueError, "decision package must be BLK-083 ready for human review"):
            build_beo_publication_pilot_execution_request(forged, request)

    def test_rejects_reused_upstream_approval_or_run_ids(self):
        decision_package, execution_request = valid_inputs()
        reused = [
            ({"request_package_id": decision_package["envelope_approval_id"]}, "request_package_id must be fresh"),
            ({"request_package_id": decision_package["envelope_run_id"]}, "request_package_id must be fresh"),
            ({"request_package_id": decision_package["pilot_request_id"]}, "request_package_id must be fresh"),
            ({"request_package_id": decision_package["future_approval_id_candidate"]}, "request_package_id must be fresh"),
            ({"request_package_id": decision_package["future_run_id_candidate"]}, "request_package_id must be fresh"),
            ({"request_package_id": execution_request["future_approval_id_candidate"]}, "request identifiers must be fresh and distinct"),
            ({"future_approval_id_candidate": decision_package["envelope_approval_id"]}, "future_approval_id_candidate must be fresh"),
            ({"future_approval_id_candidate": decision_package["future_approval_id_candidate"]}, "future_approval_id_candidate must be fresh"),
            ({"future_approval_id_candidate": decision_package["envelope_run_id"]}, "future_approval_id_candidate must be fresh"),
            ({"future_approval_id_candidate": execution_request["request_package_id"]}, "request identifiers must be fresh and distinct"),
            ({"future_approval_id_candidate": execution_request["future_run_id_candidate"]}, "future approval and run candidates must be distinct"),
            ({"future_run_id_candidate": decision_package["envelope_run_id"]}, "future_run_id_candidate must be fresh"),
            ({"future_run_id_candidate": decision_package["future_run_id_candidate"]}, "future_run_id_candidate must be fresh"),
            ({"future_run_id_candidate": decision_package["envelope_approval_id"]}, "future_run_id_candidate must be fresh"),
            ({"future_run_id_candidate": execution_request["request_package_id"]}, "request identifiers must be fresh and distinct"),
            ({"pilot_request_id": decision_package["envelope_approval_id"]}, "pilot_request_id must be fresh"),
            ({"pilot_request_id": decision_package["envelope_run_id"]}, "pilot_request_id must be fresh"),
            ({"pilot_request_id": decision_package["future_approval_id_candidate"]}, "pilot_request_id must be fresh"),
            ({"pilot_request_id": decision_package["future_run_id_candidate"]}, "pilot_request_id must be fresh"),
            ({"pilot_request_id": decision_package["pilot_request_id"]}, "pilot_request_id must be fresh"),
            ({"request_package_id": decision_package["decision_package_id"]}, "request_package_id must be fresh"),
        ]
        for upstream_identity_key in ["beo_id", "target_id", "candidate_id"]:
            reused.extend(
                [
                    ({"request_package_id": decision_package[upstream_identity_key]}, "request_package_id must be fresh"),
                    ({"pilot_request_id": decision_package[upstream_identity_key]}, "pilot_request_id must be fresh"),
                    (
                        {"future_approval_id_candidate": decision_package[upstream_identity_key]},
                        "future_approval_id_candidate must be fresh",
                    ),
                    ({"future_run_id_candidate": decision_package[upstream_identity_key]}, "future_run_id_candidate must be fresh"),
                ]
            )
        for patch, message in reused:
            request = copy.deepcopy(execution_request)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_beo_publication_pilot_execution_request(decision_package, request)

    def test_rejects_bad_expiry_replay_proof_obligations_and_denied_authorities(self):
        decision_package, execution_request = valid_inputs()
        hostile_cases = [
            ({"expired": True}, "execution request must not be expired"),
            ({"replayed": True}, "execution request must not be replayed"),
            ({"stale": True}, "execution request must not be stale"),
            ({"expires_at": execution_request["requested_at"]}, "expires_at must be after requested_at"),
            (
                {"requested_at": "2000-01-01T00:00:00+10:00", "expires_at": "2000-01-01T01:00:00+10:00"},
                "execution request must not be calendar-expired",
            ),
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
                    build_beo_publication_pilot_execution_request(decision_package, request)

    def test_rejects_authority_secret_source_git_and_tooling_laundering(self):
        decision_package, execution_request = valid_inputs()
        hostile_cases = [
            ({"operator_identity": "discord:684235178083745819-approved-for-publication-secret-token"}, "secret-bearing field"),
            ({"operator_identity": "discord:684235178083745819-se%63ret"}, "secret-bearing field"),
            ({"request_package_id": "BEO-PUBLICATION-PILOT-REQUEST-approved-for-publication"}, "authority-laundering text"),
            ({"request_package_id": "BEO-PUBLICATION-PILOT-REQUEST-approved%2Dfor%2Dpublication"}, "authority-laundering text"),
            ({"pilot_request_id": "BEO-PUBLICATION-PILOT-REQUEST-publicationPilotExecutionAuthorized"}, "authority-laundering text"),
            ({"pilot_request_id": "BEO-PUBLICATION-PILOT-REQUEST-publication%50ilot%45xecution%41uthorized"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-RTMGeneration"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-RTMAuthorityGranted"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-RTMAuthorityBeforePublicationPrerequisites"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-RTMAuthorized"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-protectedBodyReadAuthorized"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-protectedBodyAuthorized"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-packageManagerAuthorized"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-packageManagersAuthorized"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-networkAuthorized"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-networkAccessAuthorized"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-modelServiceAuthorized"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-modelServicesAuthorized"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-browserToolingAuthorized"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-browserToolsAuthorized"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-cyberToolingAuthorized"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-cyberToolsAuthorized"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-signerAuthorityGranted"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-signerAuthorized"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-storageWriteAuthorized"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-storageAuthorized"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-ledgerAppendAuthorized"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-ledgerAuthorized"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-rollbackAuthorized"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-rollbackAuthorityGranted"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-productionIsolationAuthorized"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-productionSandboxAuthorized"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-targetRepoAuthority"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-targetRepositoryAuthority"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-targetRepoAuthorized"}, "authority-laundering text"),
            ({"future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-sourceGitAuthorized"}, "authority-laundering text"),
            ({"future_run_id_candidate": "RUN-BLK-SYSTEM-085-docs%252Factive"}, "authority-laundering text"),
            ({"future_run_id_candidate": "RUN-BLK-SYSTEM-085-gitCommitAuthorized"}, "authority-laundering text"),
            ({"future_run_id_candidate": "RUN-BLK-SYSTEM-085-packageManagerIsAuthorized"}, "authority-laundering text"),
            ({"future_run_id_candidate": "RUN-BLK-SYSTEM-085-productionIsolationIsClaimed"}, "authority-laundering text"),
            ({"sourceMutationAttempted": False}, "forbidden authority field|unexpected field"),
        ]
        for patch, message in hostile_cases:
            request = copy.deepcopy(execution_request)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_beo_publication_pilot_execution_request(decision_package, request)

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
