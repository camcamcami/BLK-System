import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from metadata_bound_rtm_generation_decision_request import (
    build_metadata_bound_rtm_generation_decision_request,
    valid_metadata_bound_rtm_generation_decision_request,
)
from test_metadata_bound_rtm_generation_decision_request import valid_blk156_review_package

from metadata_bound_rtm_generation_approval_execution import (
    APPROVAL_ID,
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_OPERATOR_APPROVAL_TEXT_RAW,
    EXACT_PROOF_OBLIGATIONS,
    EXECUTION_PACKAGE_ID,
    EXECUTION_SCOPE,
    EXECUTION_STATUS,
    NEXT_REQUIRED_AUTHORITY,
    RTM_RECORD_ID,
    RUN_ID,
    SELECTED_FRONTIER,
    REQUIRED_FALSE_FLAGS,
    REQUIRED_TRUE_FLAGS,
    build_metadata_bound_rtm_generation_approval_execution,
    valid_metadata_bound_rtm_generation_approval_execution_request,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "metadata_bound_rtm_generation_approval_execution.py"


def valid_blk157_request_package():
    review = valid_blk156_review_package()
    request = valid_metadata_bound_rtm_generation_decision_request(review)
    return build_metadata_bound_rtm_generation_decision_request(review, request)


def rehash_request_package(package):
    package["request_package_hash"] = _canonical_hash({k: v for k, v in package.items() if k != "request_package_hash"})
    return package


class MetadataBoundRtmGenerationApprovalExecutionTest(unittest.TestCase):
    def test_captures_exact_approval_and_executes_bounded_metadata_rtm_generation_record(self):
        request_package = valid_blk157_request_package()
        execution_request = valid_metadata_bound_rtm_generation_approval_execution_request(request_package)

        package = build_metadata_bound_rtm_generation_approval_execution(request_package, execution_request)

        self.assertEqual(package["execution_status"], EXECUTION_STATUS)
        self.assertEqual(package["execution_package_id"], EXECUTION_PACKAGE_ID)
        self.assertEqual(package["execution_scope"], EXECUTION_SCOPE)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["upstream_request_package_id"], "METADATA-BOUND-RTM-GENERATION-DECISION-REQUEST-157-001")
        self.assertEqual(package["upstream_request_package_hash"], "sha256:ed32e6e86952e0b67fe209115e7dba8fcf2334c218a6efbaeb69a5460cc8d556")
        self.assertEqual(package["upstream_decision_request_hash"], "sha256:06681a3744d08bb99d34864485ca83fa71d692de665e0d6ecf0a5dbb96d32fb1")
        self.assertEqual(package["upstream_reconciliation_record_hash"], "sha256:1a2e06f4cb0c539f44d55c49b798cc5251d2e9a821f47e8794ccc0719747d026")
        self.assertEqual(package["approval_id"], APPROVAL_ID)
        self.assertEqual(package["operator_approval_text_raw"], EXACT_OPERATOR_APPROVAL_TEXT_RAW)
        self.assertEqual(package["run_id_consumed"], RUN_ID)
        self.assertEqual(package["beo_id"], "BEO_126")
        self.assertEqual(package["beb_id"], "BEB_126")
        self.assertTrue(package["approval_capture_performed"])
        self.assertTrue(package["rtm_generation_approved"])
        self.assertTrue(package["rtm_generation_authorized"])
        self.assertTrue(package["metadata_bound_rtm_generation_executed"])
        self.assertTrue(package["rtm_record_emitted"])
        self.assertTrue(package["run_id_consumed_in_record"])
        self.assertEqual(package["next_required_authority"], NEXT_REQUIRED_AUTHORITY)
        self.assertEqual(package["execution_request_hash"], _canonical_hash(execution_request))
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        for flag in REQUIRED_TRUE_FLAGS:
            self.assertIs(package[flag], True, flag)
        for flag in REQUIRED_FALSE_FLAGS:
            self.assertIs(package[flag], False, flag)

        record = package["rtm_record"]
        self.assertEqual(package["rtm_record_id"], RTM_RECORD_ID)
        self.assertEqual(record["rtm_record_id"], RTM_RECORD_ID)
        self.assertEqual(record["generation_mode"], "METADATA_BOUND_RTM_GENERATION_RECORD_ONLY")
        self.assertEqual(record["consumed_run_id"], RUN_ID)
        self.assertEqual(record["trace_identities"], request_package["exact_trace_identities"])
        self.assertTrue(record["metadata_bound_rtm_generation_executed"])
        for nested_flag in (
            "active_vault_filesystem_read_performed",
            "protected_body_reads",
            "rtm_drift_rejection_performed",
            "coverage_truth_established",
            "reusable_blk_link_authority_granted",
            "production_blk_link_executed",
            "public_ledger_mutation",
        ):
            self.assertIs(record[nested_flag], False, nested_flag)
        self.assertEqual(
            package["rtm_record_hash"],
            _canonical_hash({key: value for key, value in record.items() if key != "rtm_record_hash"}),
        )
        self.assertEqual(
            package["execution_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "execution_package_hash"}),
        )

    def test_rejects_forged_rehashed_or_pre_approved_blk157_request_package(self):
        request_package = valid_blk157_request_package()
        execution_request = valid_metadata_bound_rtm_generation_approval_execution_request(request_package)

        forged = copy.deepcopy(request_package)
        forged["request_package_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "request_package_hash does not match submitted BLK-157 package"):
            build_metadata_bound_rtm_generation_approval_execution(forged, execution_request)

        forged = copy.deepcopy(request_package)
        forged["request_package_id"] = "METADATA-BOUND-RTM-GENERATION-DECISION-REQUEST-158-001"
        rehash_request_package(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-157 request package required"):
            build_metadata_bound_rtm_generation_approval_execution(
                forged,
                valid_metadata_bound_rtm_generation_approval_execution_request(forged),
            )

        forged = copy.deepcopy(request_package)
        forged["approval_capture_performed"] = True
        rehash_request_package(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-157 request package required|request_package approval_capture_performed must remain false"):
            build_metadata_bound_rtm_generation_approval_execution(
                forged,
                valid_metadata_bound_rtm_generation_approval_execution_request(forged),
            )

    def test_rejects_bad_scope_retargeting_replay_expiry_unicode_ids_and_side_effects(self):
        request_package = valid_blk157_request_package()
        base = valid_metadata_bound_rtm_generation_approval_execution_request(request_package)
        cases = [
            ({"execution_package_id": "METADATA-BOUND-RTM-GENERATION-APPROVAL-EXECUTION-１５８-001"}, "execution_package_id must be|authority-laundering text"),
            ({"selected_frontier": "rtmGenerationAndDriftRejection"}, "selected_frontier must be|authority-laundering text"),
            ({"execution_scope": "RTM_GENERATION_WITH_COVERAGE_TRUTH"}, "execution_scope must be|authority-laundering text"),
            ({"upstream_request_package_hash": "sha256:" + "0" * 64}, "upstream_request_package_hash must match"),
            ({"approval_id": "APPROVAL-BLK-SYSTEM-158-OTHER"}, "approval_id must be"),
            ({"run_id": "RUN-BLK-SYSTEM-１５８-METADATA-BOUND-RTM-GENERATION-001"}, "run_id must be|authority-laundering text"),
            ({"operator_approval_text_raw": "approved"}, "operator approval text must match exact BLK-SYSTEM-158 approval sentence"),
            ({"execute_metadata_bound_rtm_generation": False}, "execute_metadata_bound_rtm_generation must be true"),
            ({"exact_trace_identities": ["REQ:REQ-１５８:sha256:" + "a" * 64]}, "exact_trace_identities id must be exact"),
            ({"expired": True}, "execution request must not be expired"),
            ({"replayed": True}, "execution request must not be replayed"),
            ({"stale": True}, "execution request must not be stale"),
            ({"expires_at": base["requested_at"]}, "expires_at must be after requested_at"),
            ({"requested_at": "2099-05-16T12:59:00+10:00"}, "execution request must not predate BLK-157 request"),
            ({"requested_at": "2099-05-16T14:00:00+10:00", "expires_at": "2099-05-16T14:10:00+10:00"}, "execution request window must end within BLK-157 request expiry"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS) + [sorted(EXACT_PROOF_OBLIGATIONS)[0]]}, "proof_obligations must not contain duplicates"),
            ({"excluded_authorities": ["NOPE"]}, "excluded_authorities must match exact denied authority set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES) + [sorted(EXACT_EXCLUDED_AUTHORITIES)[0]]}, "excluded_authorities must not contain duplicates"),
        ]
        for patch, message in cases:
            request = copy.deepcopy(base)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_metadata_bound_rtm_generation_approval_execution(request_package, request)

        for boolean_key in REQUIRED_FALSE_FLAGS:
            request = copy.deepcopy(base)
            request[boolean_key] = True
            with self.subTest(boolean_key=boolean_key):
                with self.assertRaisesRegex(ValueError, f"{boolean_key} must remain false"):
                    build_metadata_bound_rtm_generation_approval_execution(request_package, request)

    def test_rejects_nested_authority_laundering_protected_paths_body_text_tooling_and_extra_fields(self):
        request_package = valid_blk157_request_package()
        base = valid_metadata_bound_rtm_generation_approval_execution_request(request_package)
        cases = [
            ({"operator_identity": "discord:684235178083745819-RTMGenerated"}, "authority-laundering text"),
            ({"execution_package_id": "METADATA-BOUND-RTM-GENERATION-APPROVAL-EXECUTION-158-DriftRejectionExecuted"}, "authority-laundering text"),
            ({"execution_package_id": "METADATA-BOUND-RTM-GENERATION-APPROVAL-EXECUTION-158-docs%2525252Frequirements%2525252Factive"}, "authority-laundering text|protected body text"),
            ({"execution_package_id": "METADATA-BOUND-RTM-GENERATION-APPROVAL-EXECUTION-158-The%20system%20shall"}, "protected body text"),
            ({"execution_package_id": "METADATA-BOUND-RTM-GENERATION-APPROVAL-EXECUTION-158-coverageTruthEstablished"}, "authority-laundering text"),
            ({"execution_package_id": "METADATA-BOUND-RTM-GENERATION-APPROVAL-EXECUTION-158-sourceMutationAuthorized"}, "authority-laundering text"),
            ({"sourceMutationAttempted": False}, "unexpected field"),
            ({"operator_attestation": base["operator_attestation"] | {"RTMGenerated": True}}, "unexpected field"),
        ]
        for patch, message in cases:
            request = copy.deepcopy(base)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_metadata_bound_rtm_generation_approval_execution(request_package, request)

    def test_execution_request_window_is_hash_bound_and_returned_inputs_are_defensively_copied(self):
        request_package = valid_blk157_request_package()
        base = valid_metadata_bound_rtm_generation_approval_execution_request(request_package)
        alt = valid_metadata_bound_rtm_generation_approval_execution_request(
            request_package,
            requested_at="2099-05-16T13:20:00+10:00",
            expires_at="2099-05-16T13:50:00+10:00",
        )

        base_package = build_metadata_bound_rtm_generation_approval_execution(request_package, base)
        alt_package = build_metadata_bound_rtm_generation_approval_execution(request_package, alt)

        self.assertEqual(base_package["execution_request_hash"], _canonical_hash(base))
        self.assertEqual(alt_package["execution_request_hash"], _canonical_hash(alt))
        self.assertNotEqual(base_package["execution_request_hash"], alt_package["execution_request_hash"])
        self.assertNotEqual(base_package["execution_package_hash"], alt_package["execution_package_hash"])

        base["operator_attestation"]["coverage_truth_excluded"] = "mutated"
        request_package["exact_trace_identities"].append("REQ:REQ-999:sha256:" + "f" * 64)
        self.assertIsNot(base_package["operator_attestation"], base["operator_attestation"])
        self.assertIs(base_package["operator_attestation"]["coverage_truth_excluded"], True)
        self.assertNotIn("REQ:REQ-999:sha256:" + "f" * 64, base_package["exact_trace_identities"])

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
