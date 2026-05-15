import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from metadata_bound_rtm_blk_link_reconciliation_request import (
    build_metadata_bound_rtm_blk_link_reconciliation_request,
    valid_metadata_bound_rtm_blk_link_reconciliation_request,
)
from test_metadata_bound_rtm_blk_link_reconciliation_request import valid_blk153_preflight_package

from bounded_metadata_rtm_blk_link_reconciliation_execution import (
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_OPERATOR_APPROVAL_TEXT_RAW,
    EXACT_PROOF_OBLIGATIONS,
    EXECUTION_PACKAGE_ID,
    EXECUTION_STATUS,
    RECONCILIATION_RECORD_ID,
    RUN_ID,
    SELECTED_FRONTIER,
    REQUIRED_FALSE_FLAGS,
    REQUIRED_TRUE_FLAGS,
    build_bounded_metadata_rtm_blk_link_reconciliation_execution,
    valid_bounded_metadata_reconciliation_execution_request,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "bounded_metadata_rtm_blk_link_reconciliation_execution.py"


def valid_blk154_request_package():
    preflight = valid_blk153_preflight_package()
    request = valid_metadata_bound_rtm_blk_link_reconciliation_request(preflight)
    return build_metadata_bound_rtm_blk_link_reconciliation_request(preflight, request)


def rehash_request_package(package):
    package["request_package_hash"] = _canonical_hash({k: v for k, v in package.items() if k != "request_package_hash"})
    return package


class BoundedMetadataRtmBlkLinkReconciliationExecutionTest(unittest.TestCase):
    def test_executes_one_bounded_metadata_reconciliation_record_for_exact_request(self):
        request_package = valid_blk154_request_package()
        execution_request = valid_bounded_metadata_reconciliation_execution_request(request_package)

        package = build_bounded_metadata_rtm_blk_link_reconciliation_execution(request_package, execution_request)

        self.assertEqual(package["execution_status"], EXECUTION_STATUS)
        self.assertEqual(package["execution_package_id"], EXECUTION_PACKAGE_ID)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["operator_approval_text_raw"], EXACT_OPERATOR_APPROVAL_TEXT_RAW)
        self.assertEqual(package["run_id_consumed"], RUN_ID)
        self.assertEqual(package["upstream_request_package_hash"], request_package["request_package_hash"])
        self.assertEqual(package["reconciliation_record_id"], RECONCILIATION_RECORD_ID)
        self.assertTrue(package["approval_capture_performed"])
        self.assertTrue(package["future_run_id_consumed"])
        self.assertTrue(package["metadata_reconciliation_executed"])
        self.assertFalse(package["rtm_generated"])
        self.assertFalse(package["production_blk_link_executed"])
        self.assertFalse(package["coverage_truth_established"])
        self.assertFalse(package["protected_body_reads"])
        record = package["reconciliation_record"]
        self.assertEqual(record["record_id"], RECONCILIATION_RECORD_ID)
        self.assertEqual(record["trace_identities"], request_package["exact_trace_identities"])
        self.assertTrue(record["metadata_hashes_reconciled"])
        self.assertEqual(record["mismatch_count"], 0)
        self.assertEqual(record["mismatches"], [])
        self.assertFalse(record["drift_rejection_performed"])
        self.assertFalse(record["coverage_truth_established"])
        self.assertFalse(record["protected_body_reads"])
        self.assertEqual(record["record_hash"], _canonical_hash({k: v for k, v in record.items() if k != "record_hash"}))
        for flag in REQUIRED_TRUE_FLAGS:
            self.assertIs(package[flag], True, flag)
        for flag in REQUIRED_FALSE_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        self.assertEqual(package["execution_request_hash"], _canonical_hash(execution_request))
        self.assertEqual(
            package["execution_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "execution_package_hash"}),
        )

    def test_rejects_forged_request_non_exact_approval_replay_and_bad_window(self):
        request_package = valid_blk154_request_package()
        execution_request = valid_bounded_metadata_reconciliation_execution_request(request_package)

        forged = copy.deepcopy(request_package)
        forged["request_package_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "request_package_hash does not match submitted BLK-154 package"):
            build_bounded_metadata_rtm_blk_link_reconciliation_execution(forged, execution_request)

        forged = copy.deepcopy(request_package)
        forged["request_package_id"] = "METADATA-BOUND-RTM-BLK-LINK-RECONCILIATION-REQUEST-155-001"
        rehash_request_package(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-154 request package required"):
            build_bounded_metadata_rtm_blk_link_reconciliation_execution(
                forged,
                valid_bounded_metadata_reconciliation_execution_request(forged),
            )

        cases = [
            ({"operator_approval_text_raw": "approve maybe"}, "operator_approval_text_raw must match exact BLK-SYSTEM-154-156 operator approval"),
            ({"run_id": "RUN-BLK-SYSTEM-155-OTHER"}, "run_id must be"),
            ({"replayed": True}, "execution request must not be replayed"),
            ({"stale": True}, "execution request must not be stale"),
            ({"expired": True}, "execution request must not be expired"),
            ({"expires_at": execution_request["requested_at"]}, "expires_at must be after requested_at"),
        ]
        for patch, message in cases:
            candidate = copy.deepcopy(execution_request)
            candidate.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_bounded_metadata_rtm_blk_link_reconciliation_execution(request_package, candidate)

    def test_rejects_adjacent_authority_laundering_and_side_effects(self):
        request_package = valid_blk154_request_package()
        base = valid_bounded_metadata_reconciliation_execution_request(request_package)
        cases = [
            ({"selected_frontier": "metadataReconciliationAndDriftRejection"}, "selected_frontier must be|authority-laundering text"),
            ({"rtm_generation_authorized": True}, "rtm_generation_authorized must remain false"),
            ({"rtm_generated": True}, "rtm_generated must remain false"),
            ({"production_blk_link_executed": True}, "production_blk_link_executed must remain false"),
            ({"coverage_truth_established": True}, "coverage_truth_established must remain false"),
            ({"protected_body_reads": True}, "protected_body_reads must remain false"),
            ({"operator_identity": "discord:684235178083745819-RTMGenerated"}, "authority-laundering text"),
            ({"execution_package_id": "BOUNDED-METADATA-RTM-BLK-LINK-RECONCILIATION-EXECUTION-155-docs%2525252Frequirements%2525252Factive"}, "authority-laundering text|protected body text"),
            ({"operator_attestation": base["operator_attestation"] | {"coverageTruth": True}}, "unexpected field"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"excluded_authorities": ["NOPE"]}, "excluded_authorities must match exact denied authority set"),
        ]
        for patch, message in cases:
            candidate = copy.deepcopy(base)
            candidate.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_bounded_metadata_rtm_blk_link_reconciliation_execution(request_package, candidate)

    def test_execution_request_hash_is_bound(self):
        request_package = valid_blk154_request_package()
        first = valid_bounded_metadata_reconciliation_execution_request(request_package)
        second = valid_bounded_metadata_reconciliation_execution_request(
            request_package,
            requested_at="2099-05-16T10:10:00+10:00",
            expires_at="2099-05-16T11:10:00+10:00",
        )

        first_package = build_bounded_metadata_rtm_blk_link_reconciliation_execution(request_package, first)
        second_package = build_bounded_metadata_rtm_blk_link_reconciliation_execution(request_package, second)

        self.assertNotEqual(first_package["execution_request_hash"], second_package["execution_request_hash"])
        self.assertNotEqual(first_package["execution_package_hash"], second_package["execution_package_hash"])

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
