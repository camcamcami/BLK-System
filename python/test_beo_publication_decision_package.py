import copy
import ast
import unittest
from pathlib import Path

from authoritative_beo_publication_approval_envelope import build_authoritative_beo_publication_approval_envelope
from authoritative_beo_publication_authority_request import _canonical_hash
from test_authoritative_beo_publication_approval_envelope import valid_envelope_inputs

from beo_publication_decision_package import (
    DECISION_PACKAGE_READY,
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS,
    build_beo_publication_decision_package,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "beo_publication_decision_package.py"


def valid_inputs():
    envelope = build_authoritative_beo_publication_approval_envelope(*valid_envelope_inputs())
    decision_request = {
        "decision_package_id": "BEO-PUBLICATION-DECISION-PACKAGE-083-001",
        "operator_identity": "discord:684235178083745819",
        "decision_scope": "BEO_PUBLICATION_DECISION_PACKAGE_ONLY_NOT_PUBLICATION_APPROVAL",
        "selected_frontier": SELECTED_FRONTIER,
        "requested_at": "2099-05-12T07:30:00+10:00",
        "expires_at": "2099-05-12T08:30:00+10:00",
        "exact_envelope_id": envelope["envelope_id"],
        "exact_envelope_hash": envelope["envelope_hash"],
        "exact_beo_id": envelope["beo_id"],
        "exact_beo_hash": envelope["beo_hash"],
        "exact_target_id": envelope["target_id"],
        "pilot_request_id": "BEO-PUBLICATION-PILOT-REQUEST-083-001",
        "future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-084-BEO-PUBLICATION-PILOT-001",
        "future_run_id_candidate": "RUN-BLK-SYSTEM-084-BEO-PUBLICATION-PILOT-001",
        "approval_granted": False,
        "publication_approved": False,
        "pilot_execution_authorized": False,
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {
            "decision_package_not_approval": True,
            "publication_pilot_requires_future_human_approval": True,
            "rtm_generation_excluded": True,
            "protected_body_reads_excluded": True,
            "no_side_effects": True,
        },
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    return envelope, decision_request


class BeoPublicationDecisionPackageTest(unittest.TestCase):
    def test_builds_review_ready_decision_package_without_approval_or_publication(self):
        envelope, decision_request = valid_inputs()

        package = build_beo_publication_decision_package(envelope, decision_request)

        self.assertEqual(package["decision_status"], DECISION_PACKAGE_READY)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["decision_scope"], "BEO_PUBLICATION_DECISION_PACKAGE_ONLY_NOT_PUBLICATION_APPROVAL")
        self.assertEqual(package["envelope_id"], envelope["envelope_id"])
        self.assertEqual(package["envelope_hash"], envelope["envelope_hash"])
        self.assertEqual(package["beo_id"], envelope["beo_id"])
        self.assertEqual(package["beo_hash"], envelope["beo_hash"])
        self.assertEqual(package["target_id"], envelope["target_id"])
        self.assertTrue(package["future_publication_pilot_requires_explicit_approval"])
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        self.assertIn("decision_package_hash", package)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)

    def test_rejects_wrong_or_multiple_frontiers_and_positive_approval_flags(self):
        envelope, decision_request = valid_inputs()
        hostile_cases = [
            ({"selected_frontier": "codex_l3_smoke"}, "selected_frontier must be beo_publication_pilot_request"),
            ({"secondary_frontier": "rtm_generation_request"}, "unexpected field"),
            ({"approval_granted": True}, "approval_granted must remain false"),
            ({"publication_approved": True}, "publication_approved must remain false"),
            ({"pilot_execution_authorized": True}, "pilot_execution_authorized must remain false"),
        ]
        for patch, message in hostile_cases:
            request = copy.deepcopy(decision_request)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_beo_publication_decision_package(envelope, request)

    def test_rejects_forged_or_mismatched_upstream_envelope_identity(self):
        envelope, decision_request = valid_inputs()
        forged = copy.deepcopy(envelope)
        forged["target_id"] = "BEO-PUBLICATION-TARGET-FORGED-083"
        with self.assertRaisesRegex(ValueError, "envelope_hash does not match canonical approval envelope"):
            build_beo_publication_decision_package(forged, decision_request)

        forged = copy.deepcopy(envelope)
        forged["target_id"] = "BEO-PUBLICATION-TARGET-FORGED-083"
        forged["envelope_hash"] = _canonical_hash({key: value for key, value in forged.items() if key != "envelope_hash"})
        request = copy.deepcopy(decision_request)
        request["exact_envelope_hash"] = forged["envelope_hash"]
        with self.assertRaisesRegex(ValueError, "exact_target_id does not match approval envelope"):
            build_beo_publication_decision_package(forged, request)

        forged = copy.deepcopy(envelope)
        forged["publication_performed"] = True
        forged["envelope_hash"] = _canonical_hash({key: value for key, value in forged.items() if key != "envelope_hash"})
        request = copy.deepcopy(decision_request)
        request["exact_envelope_hash"] = forged["envelope_hash"]
        with self.assertRaisesRegex(ValueError, "publication_performed must remain false"):
            build_beo_publication_decision_package(forged, request)

    def test_rejects_bad_expiry_replay_proof_obligations_and_denied_authorities(self):
        envelope, decision_request = valid_inputs()
        hostile_cases = [
            ({"expired": True}, "decision request must not be expired"),
            ({"replayed": True}, "decision request must not be replayed"),
            ({"stale": True}, "decision request must not be stale"),
            ({"requested_at": "not-a-timestamp"}, "requested_at must be an ISO timestamp"),
            ({"expires_at": "2099-05-12T07:00:00+10:00"}, "expires_at must be after requested_at"),
            ({"proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS - {"SIGNER_POLICY_WITHOUT_KEY_MATERIAL_BOUND"})}, "proof_obligations must match exact set"),
            ({"proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS) + ["SIGNER_POLICY_WITHOUT_KEY_MATERIAL_BOUND"]}, "proof_obligations must not contain duplicates"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES - {"RTM_GENERATION"})}, "excluded_authorities must match exact denied authority set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES) + ["ACTUAL_AUTHORITATIVE_BEO_PUBLICATION"]}, "excluded_authorities must not contain duplicates"),
        ]
        for patch, message in hostile_cases:
            request = copy.deepcopy(decision_request)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_beo_publication_decision_package(envelope, request)

    def test_rejects_publication_rtm_protected_body_tooling_and_secret_laundering(self):
        envelope, decision_request = valid_inputs()
        hostile_cases = [
            ({"publicationAuthority": True}, "forbidden authority field"),
            ({"operator_attestation": {**decision_request["operator_attestation"], "publishBEO": True}}, "forbidden authority field"),
            ({"operator_attestation": {**decision_request["operator_attestation"], "RTMGeneration": True}}, "forbidden authority field"),
            ({"operator_attestation": {**decision_request["operator_attestation"], "protected_body_path": "docs/active/BLK-001.md"}}, "forbidden authority field"),
            ({"operator_attestation": {**decision_request["operator_attestation"], "signerKeyMaterial": "SECRET"}}, "secret-bearing field"),
            ({"operator_attestation": {**decision_request["operator_attestation"], "npm_run_publish": True}}, "forbidden authority field"),
            ({"operator_attestation": {**decision_request["operator_attestation"], "target_repo_mutation_authorized": True}}, "forbidden authority field"),
        ]
        for patch, message in hostile_cases:
            request = copy.deepcopy(decision_request)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_beo_publication_decision_package(envelope, request)

    def test_module_contains_no_live_surface_imports_or_calls(self):
        tree = ast.parse(MODULE.read_text())
        forbidden_imports = {"subprocess", "socket", "requests", "urllib", "http", "git", "os", "pathlib"}
        forbidden_calls = {"eval", "exec", "__import__", "compile", "open", "system", "popen"}
        offenders = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name.split(".")[0] for alias in node.names]
                offenders.extend(name for name in names if name in forbidden_imports)
            if isinstance(node, ast.ImportFrom):
                names = [alias.name.split(".")[0] for alias in node.names]
                if node.module:
                    names.append(node.module.split(".")[0])
                offenders.extend(name for name in names if name in forbidden_imports)
            if isinstance(node, ast.Call):
                func = node.func
                name = ""
                if isinstance(func, ast.Name):
                    name = func.id
                elif isinstance(func, ast.Attribute):
                    name = func.attr
                if name in forbidden_calls:
                    offenders.append(name)

        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
