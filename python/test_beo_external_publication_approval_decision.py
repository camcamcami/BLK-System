import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from beo_publication_prerequisite_request_after_evidence_refresh import (
    REQUEST_PACKAGE_ID as BLK098_REQUEST_PACKAGE_ID,
    REQUEST_STATUS as BLK098_REQUEST_STATUS,
    build_beo_publication_prerequisite_request_after_evidence_refresh,
)
from test_beo_publication_prerequisite_request_after_evidence_refresh import valid_inputs as valid_blk098_inputs

from beo_external_publication_approval_decision import (
    APPROVAL_DECISION_PACKAGE_ID,
    APPROVAL_ID,
    DECISION_RESULT,
    DECISION_SCOPE,
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    FUTURE_PUBLICATION_EXECUTION_RUN_ID,
    NEXT_REQUIRED_AUTHORITY,
    OPERATOR_APPROVAL_TEXT_RAW,
    SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS,
    STATUS,
    build_beo_external_publication_approval_decision,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "beo_external_publication_approval_decision.py"


def valid_inputs():
    runtime_evidence, local_pilot_package, prerequisite_request = valid_blk098_inputs()
    request_package = build_beo_publication_prerequisite_request_after_evidence_refresh(
        runtime_evidence, local_pilot_package, prerequisite_request
    )
    approval_decision = {
        "approval_decision_package_id": APPROVAL_DECISION_PACKAGE_ID,
        "operator_identity": "discord:684235178083745819",
        "operator_approval_text_raw": OPERATOR_APPROVAL_TEXT_RAW,
        "operator_approved_request_package_id_normalized": BLK098_REQUEST_PACKAGE_ID,
        "decision_scope": DECISION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_request_package_id": request_package["request_package_id"],
        "upstream_request_package_hash": request_package["request_package_hash"],
        "upstream_request_status": request_package["request_status"],
        "exact_beo_id": request_package["beo_id"],
        "exact_beo_hash": request_package["beo_hash"],
        "exact_target_repo_path": request_package["target_repo_path"],
        "exact_target_head_sha": request_package["target_head_sha"],
        "approval_id": APPROVAL_ID,
        "future_publication_execution_run_id": FUTURE_PUBLICATION_EXECUTION_RUN_ID,
        "decision_result": DECISION_RESULT,
        "decided_at": "2099-05-13T19:10:00+10:00",
        "expires_at": "2099-05-14T19:10:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {
            "exact_blk098_request_reviewed": True,
            "operator_text_normalized_to_exact_request_id": True,
            "approval_limited_to_one_future_external_publication_execution_sprint": True,
            "external_publication_not_executed_by_this_decision": True,
            "future_run_id_reserved_not_consumed": True,
            "signer_storage_ledger_rollback_side_effects_excluded": True,
            "rtm_generation_and_drift_excluded": True,
            "protected_body_reads_excluded": True,
            "target_source_git_mutation_excluded": True,
            "blk_pipe_blk_test_codex_tooling_excluded": True,
            "no_production_isolation_claim": True,
        },
        **{flag: False for flag in SIDE_EFFECT_FLAGS},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    return request_package, approval_decision


def rehash_request_package(package):
    package["request_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "request_package_hash"}
    )
    return package


class BeoExternalPublicationApprovalDecisionTest(unittest.TestCase):
    def test_builds_exact_approval_decision_without_executing_external_publication(self):
        request_package, approval_decision = valid_inputs()

        package = build_beo_external_publication_approval_decision(request_package, approval_decision)

        self.assertEqual(package["approval_decision_status"], STATUS)
        self.assertEqual(package["approval_decision_package_id"], APPROVAL_DECISION_PACKAGE_ID)
        self.assertEqual(package["decision_scope"], DECISION_SCOPE)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["decision_result"], DECISION_RESULT)
        self.assertEqual(package["operator_approval_text_raw"], OPERATOR_APPROVAL_TEXT_RAW)
        self.assertEqual(package["operator_approved_request_package_id_normalized"], BLK098_REQUEST_PACKAGE_ID)
        self.assertEqual(package["upstream_request_package_id"], BLK098_REQUEST_PACKAGE_ID)
        self.assertEqual(package["upstream_request_package_hash"], request_package["request_package_hash"])
        self.assertEqual(package["upstream_request_status"], BLK098_REQUEST_STATUS)
        self.assertEqual(package["beo_id"], request_package["beo_id"])
        self.assertEqual(package["beo_hash"], request_package["beo_hash"])
        self.assertEqual(package["target_repo_path"], request_package["target_repo_path"])
        self.assertEqual(package["target_head_sha"], request_package["target_head_sha"])
        self.assertEqual(package["approval_id"], APPROVAL_ID)
        self.assertEqual(package["future_publication_execution_run_id"], FUTURE_PUBLICATION_EXECUTION_RUN_ID)
        self.assertTrue(package["approval_decision_captured"])
        self.assertTrue(package["human_external_beo_publication_approval_granted"])
        self.assertTrue(package["future_external_beo_publication_execution_approved"])
        self.assertFalse(package["future_publication_execution_run_id_consumed"])
        self.assertFalse(package["external_authoritative_publication_performed"])
        self.assertFalse(package["runtime_published_beo_output"])
        self.assertEqual(package["beo_publication_status"], "APPROVAL_DECISION_CAPTURED_NOT_PUBLISHED")
        self.assertEqual(package["rtm_status"], "NOT_GENERATED")
        self.assertEqual(package["next_required_authority"], NEXT_REQUIRED_AUTHORITY)
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(
            package["approval_decision_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "approval_decision_package_hash"}),
        )

    def test_rejects_forged_rehashed_or_already_authorized_blk098_request_package(self):
        request_package, approval_decision = valid_inputs()

        forged = copy.deepcopy(request_package)
        forged["target_head_sha"] = "deadbeef" * 5
        with self.assertRaisesRegex(ValueError, "request_package_hash does not match submitted BLK-098 package"):
            build_beo_external_publication_approval_decision(forged, approval_decision)

        forged = copy.deepcopy(request_package)
        forged["target_head_sha"] = "deadbeef" * 5
        rehash_request_package(forged)
        decision = copy.deepcopy(approval_decision)
        decision["upstream_request_package_hash"] = forged["request_package_hash"]
        decision["exact_target_head_sha"] = forged["target_head_sha"]
        with self.assertRaisesRegex(ValueError, "request package must match canonical BLK-098 prerequisite package"):
            build_beo_external_publication_approval_decision(forged, decision)

        forged = copy.deepcopy(request_package)
        forged["external_publication_approval_granted"] = True
        rehash_request_package(forged)
        decision = copy.deepcopy(approval_decision)
        decision["upstream_request_package_hash"] = forged["request_package_hash"]
        with self.assertRaisesRegex(ValueError, "BLK-098 request must remain not granted"):
            build_beo_external_publication_approval_decision(forged, decision)

    def test_rejects_retargeting_replay_expiry_bad_sets_and_side_effects(self):
        request_package, approval_decision = valid_inputs()
        cases = [
            ({"decision_scope": "EXTERNAL_BEO_PUBLICATION_APPROVAL_AND_EXECUTION"}, "decision_scope must be"),
            ({"selected_frontier": "external_beo_publication_execution"}, "selected_frontier must be"),
            ({"upstream_request_package_id": "BEO-PUBLICATION-PREREQUISITE-REQUEST-098-999"}, "upstream_request_package_id must match"),
            ({"upstream_request_package_hash": "sha256:" + "0" * 64}, "upstream_request_package_hash must match"),
            ({"upstream_request_status": "BEO_PUBLICATION_PREREQUISITE_REQUEST_APPROVED"}, "upstream_request_status must match"),
            ({"approval_id": request_package["request_package_id"]}, "approval_id must be fresh"),
            ({"future_publication_execution_run_id": request_package["request_package_id"]}, "future_publication_execution_run_id must be fresh"),
            ({"future_publication_execution_run_id": APPROVAL_ID}, "future_publication_execution_run_id must be fresh"),
            ({"decision_result": "APPROVED_AND_PUBLISHED"}, "decision_result must be"),
            ({"expired": True}, "approval decision must not be expired"),
            ({"replayed": True}, "approval decision must not be replayed"),
            ({"stale": True}, "approval decision must not be stale"),
            ({"expires_at": approval_decision["decided_at"]}, "expires_at must be after decided_at"),
            ({"decided_at": "2000-01-01T00:00:00+10:00", "expires_at": "2000-01-01T01:00:00+10:00"}, "approval decision must not be calendar-expired"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS) + [sorted(EXACT_PROOF_OBLIGATIONS)[0]]}, "proof_obligations must not contain duplicates"),
            ({"excluded_authorities": ["NOPE"]}, "excluded_authorities must match exact denied authority set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES) + [sorted(EXACT_EXCLUDED_AUTHORITIES)[0]]}, "excluded_authorities must not contain duplicates"),
        ]
        for patch, message in cases:
            decision = copy.deepcopy(approval_decision)
            decision.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_beo_external_publication_approval_decision(request_package, decision)

        for flag in SIDE_EFFECT_FLAGS:
            decision = copy.deepcopy(approval_decision)
            decision[flag] = True
            with self.subTest(flag=flag):
                with self.assertRaisesRegex(ValueError, f"{flag} must remain false"):
                    build_beo_external_publication_approval_decision(request_package, decision)

    def test_rejects_publication_authorized_signing_granted_and_protected_path_laundering(self):
        request_package, approval_decision = valid_inputs()
        cases = [
            ({"operator_identity": "discord:684235178083745819/PublicationAuthorized"}, "authority-laundering text"),
            ({"operator_approval_text_raw": "PublicationAuthorized"}, "authority-laundering text"),
            ({"operator_approval_text_raw": "SigningGranted"}, "authority-laundering text"),
            ({"operator_approval_text_raw": "BEOisPublished"}, "authority-laundering text"),
            ({"operator_approval_text_raw": "rtm_generation_authorized"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-APPROVAL-DECISION-099-PublicationAuthorized"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-APPROVAL-DECISION-099-SigningGranted"}, "authority-laundering text"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-APPROVAL-DECISION-099-docs%252Factive"}, "protected BLK-req body reference|authority-laundering text"),
            ({"notes": "harmless"}, "unexpected field"),
            ({"PublicationAuthorized": False}, "unexpected field"),
            ({"SigningGranted": False}, "unexpected field"),
            ({"operator_attestation": approval_decision["operator_attestation"] | {"PublicationAuthorized": True}}, "unexpected field"),
        ]
        for patch, message in cases:
            decision = copy.deepcopy(approval_decision)
            decision.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_beo_external_publication_approval_decision(request_package, decision)

    def test_returned_package_defensively_copies_hash_bound_nested_inputs(self):
        request_package, approval_decision = valid_inputs()

        package = build_beo_external_publication_approval_decision(request_package, approval_decision)
        approval_decision["operator_attestation"]["exact_blk098_request_reviewed"] = False

        self.assertIsNot(package["operator_attestation"], approval_decision["operator_attestation"])
        self.assertTrue(package["operator_attestation"]["exact_blk098_request_reviewed"])
        self.assertEqual(
            package["approval_decision_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "approval_decision_package_hash"}),
        )

    def test_module_has_no_live_runtime_external_tooling_or_signer_storage_ledger_imports(self):
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
        forbidden_imports = {"subprocess", "socket", "requests", "urllib3", "httpx", "shutil"}
        forbidden_calls = {"system", "popen", "Popen", "run", "call", "check_call", "check_output", "exec", "eval", "open", "urlopen", "request"}
        self.assertEqual(imported & forbidden_imports, set())
        self.assertEqual(calls & forbidden_calls, set())


if __name__ == "__main__":
    unittest.main()
