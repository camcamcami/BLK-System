import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from test_active_vault_hash_comparison_post_execution_reconciliation import (
    valid_blk140_execution_package,
    valid_reconciliation_context,
)
from active_vault_hash_comparison_post_execution_reconciliation import (
    build_active_vault_hash_comparison_post_execution_reconciliation,
)

from metadata_bound_rtm_generation_authority_request import (
    AUTHORITY_REQUEST_PACKAGE_ID,
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY,
    REQUEST_SCOPE,
    REQUEST_STATUS,
    SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS,
    build_metadata_bound_rtm_generation_authority_request,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "metadata_bound_rtm_generation_authority_request.py"


def valid_blk141_reconciliation_package():
    execution = valid_blk140_execution_package()
    return build_active_vault_hash_comparison_post_execution_reconciliation(
        execution,
        valid_reconciliation_context(execution),
    )


def valid_authority_request(reconciliation=None, **overrides):
    if reconciliation is None:
        reconciliation = valid_blk141_reconciliation_package()
    request = {
        "authority_request_package_id": AUTHORITY_REQUEST_PACKAGE_ID,
        "operator_identity": reconciliation["operator_identity"],
        "request_scope": REQUEST_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_reconciliation_package_id": reconciliation["reconciliation_package_id"],
        "upstream_reconciliation_package_hash": reconciliation["reconciliation_package_hash"],
        "upstream_reconciliation_context_hash": reconciliation["reconciliation_context_hash"],
        "upstream_execution_package_id": reconciliation["upstream_execution_package_id"],
        "upstream_execution_package_hash": reconciliation["upstream_execution_package_hash"],
        "upstream_comparison_record_id": reconciliation["upstream_comparison_record_id"],
        "upstream_comparison_record_hash": reconciliation["upstream_comparison_record_hash"],
        "beo_id": reconciliation["beo_id"],
        "beb_id": reconciliation["beb_id"],
        "exact_trace_identities": list(reconciliation["exact_trace_identities"]),
        "metadata_hashes_match": True,
        "request_future_exact_metadata_bound_rtm_generation_approval": True,
        "requested_at": "2099-05-15T14:00:00+10:00",
        "expires_at": "2099-05-16T14:00:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {
            "exact_blk141_reconciliation_reviewed": True,
            "clean_metadata_hash_comparison_verified": True,
            "request_is_for_future_approval_not_approval": True,
            "rtm_generation_not_approved_or_executed": True,
            "future_run_id_not_reserved_or_consumed": True,
            "protected_body_reads_excluded": True,
            "active_vault_filesystem_reads_excluded": True,
            "drift_rejection_excluded": True,
            "coverage_truth_excluded": True,
            "reusable_blk_link_excluded": True,
            "signer_storage_ledger_excluded": True,
            "beb_dispatch_beo_closeout_excluded": True,
            "target_source_git_mutation_excluded": True,
            "blk_pipe_blk_test_codex_tooling_excluded": True,
            "no_production_isolation_claim": True,
        },
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        request[flag] = False
    request.update(overrides)
    return request


def rehash_reconciliation_package(package):
    package["reconciliation_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "reconciliation_package_hash"}
    )
    return package


class MetadataBoundRtmGenerationAuthorityRequestTest(unittest.TestCase):
    def test_binds_exact_clean_blk141_reconciliation_without_approval_or_generation(self):
        reconciliation = valid_blk141_reconciliation_package()
        request = valid_authority_request(reconciliation)

        package = build_metadata_bound_rtm_generation_authority_request(reconciliation, request)

        self.assertEqual(package["request_status"], REQUEST_STATUS)
        self.assertEqual(package["authority_request_package_id"], AUTHORITY_REQUEST_PACKAGE_ID)
        self.assertEqual(package["request_scope"], REQUEST_SCOPE)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["requested_authority"], "ONE_FUTURE_METADATA_BOUND_RTM_GENERATION_APPROVAL_CAPTURE")
        self.assertEqual(package["upstream_reconciliation_package_id"], reconciliation["reconciliation_package_id"])
        self.assertEqual(package["upstream_reconciliation_package_hash"], reconciliation["reconciliation_package_hash"])
        self.assertEqual(package["upstream_reconciliation_context_hash"], reconciliation["reconciliation_context_hash"])
        self.assertEqual(package["upstream_comparison_record_hash"], reconciliation["upstream_comparison_record_hash"])
        self.assertEqual(package["exact_trace_identities"], reconciliation["exact_trace_identities"])
        self.assertTrue(package["request_future_exact_metadata_bound_rtm_generation_approval"])
        self.assertFalse(package["approval_capture_performed"])
        self.assertFalse(package["rtm_generation_approved"])
        self.assertFalse(package["rtm_generated"])
        self.assertFalse(package["future_run_id_reserved"])
        self.assertFalse(package["future_run_id_consumed"])
        self.assertEqual(package["next_required_authority"], NEXT_REQUIRED_AUTHORITY)
        self.assertEqual(package["authority_request_hash"], _canonical_hash(request))
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(
            package["authority_request_package_hash"],
            _canonical_hash({k: v for k, v in package.items() if k != "authority_request_package_hash"}),
        )

    def test_rejects_forged_mismatch_stale_replayed_expired_or_side_effecting_inputs(self):
        reconciliation = valid_blk141_reconciliation_package()
        request = valid_authority_request(reconciliation)

        forged = copy.deepcopy(reconciliation)
        forged["reconciliation_package_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "reconciliation_package_hash does not match submitted BLK-141 package"):
            build_metadata_bound_rtm_generation_authority_request(forged, request)

        forged = copy.deepcopy(reconciliation)
        forged["reconciliation_package_id"] = "ACTIVE-VAULT-HASH-COMPARISON-POST-EXECUTION-RECONCILIATION-１４１-001"
        rehash_reconciliation_package(forged)
        with self.assertRaisesRegex(ValueError, "reconciliation_package_id must match exact BLK-141 package"):
            build_metadata_bound_rtm_generation_authority_request(forged, valid_authority_request(forged))

        mismatch = copy.deepcopy(reconciliation)
        mismatch["metadata_hashes_match"] = False
        rehash_reconciliation_package(mismatch)
        with self.assertRaisesRegex(ValueError, "clean BLK-141 reconciliation required"):
            build_metadata_bound_rtm_generation_authority_request(mismatch, valid_authority_request(mismatch, metadata_hashes_match=False))

        for patch, message in [
            ({"upstream_reconciliation_package_hash": "sha256:" + "0" * 64}, "upstream_reconciliation_package_hash must match"),
            ({"metadata_hashes_match": False}, "metadata_hashes_match must match clean BLK-141 reconciliation"),
            ({"expires_at": "2099-05-15T14:00:00+10:00"}, "expires_at must be after requested_at"),
            ({"requested_at": "2026-05-15T14:00:00+10:00"}, "authority request must not be calendar-stale"),
            ({"expired": True}, "authority request must not be expired"),
            ({"replayed": True}, "authority request must not be replayed"),
            ({"stale": True}, "authority request must not be stale"),
            ({"approval_capture_performed": True}, "approval_capture_performed must remain false"),
            ({"rtm_generated": True}, "rtm_generated must remain false"),
            ({"future_run_id_reserved": True}, "future_run_id_reserved must remain false"),
        ]:
            candidate = copy.deepcopy(request)
            candidate.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_metadata_bound_rtm_generation_authority_request(reconciliation, candidate)

    def test_rejects_authority_laundering_protected_paths_bad_sets_and_extra_fields(self):
        reconciliation = valid_blk141_reconciliation_package()
        request = valid_authority_request(reconciliation)
        cases = [
            ({"operator_identity": "discord:684235178083745819-RTMGenerated"}, "authority-laundering text"),
            ({"operator_identity": "discord:684235178083745819-docs%2525252Frequirements%2525252Factive"}, "protected body text"),
            ({"operator_identity": "discord:684235178083745819-The%20system%20shall"}, "protected body text"),
            ({"sourceMutationAttempted": False}, "unexpected field"),
            ({"operator_attestation": request["operator_attestation"] | {"coverageMatrix": True}}, "unexpected field"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS) + [sorted(EXACT_PROOF_OBLIGATIONS)[0]]}, "proof_obligations must not contain duplicates"),
            ({"excluded_authorities": ["NOPE"]}, "excluded_authorities must match exact denied authority set"),
        ]
        for patch, message in cases:
            candidate = copy.deepcopy(request)
            candidate.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_metadata_bound_rtm_generation_authority_request(reconciliation, candidate)

    def test_returned_package_is_defensively_copied_and_hash_bound(self):
        reconciliation = valid_blk141_reconciliation_package()
        request = valid_authority_request(reconciliation)
        package = build_metadata_bound_rtm_generation_authority_request(reconciliation, request)

        request["operator_attestation"]["coverage_truth_excluded"] = "mutated"
        reconciliation["exact_trace_identities"].append("REQ:REQ-999:sha256:" + "9" * 64)

        self.assertIs(package["operator_attestation"]["coverage_truth_excluded"], True)
        self.assertNotIn("REQ:REQ-999:sha256:" + "9" * 64, package["exact_trace_identities"])

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
