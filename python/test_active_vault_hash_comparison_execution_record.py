import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from active_vault_hash_comparison_approval_capture import build_active_vault_hash_comparison_approval_capture
from test_active_vault_hash_comparison_authority_ladder import valid_approval_decision, valid_request_package

from active_vault_hash_comparison_execution_record import (
    COMPARISON_EXECUTION_PACKAGE_ID,
    COMPARISON_RECORD_ID,
    EXECUTION_SCOPE,
    EXECUTION_STATUS,
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    NEXT_FRONTIER,
    RUN_ID_CONSUMED,
    SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS,
    build_active_vault_hash_comparison_execution_record,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "active_vault_hash_comparison_execution_record.py"


def valid_blk139_approval_package():
    request = valid_request_package()
    approval_decision = valid_approval_decision(request)
    return build_active_vault_hash_comparison_approval_capture(request, approval_decision)


def metadata_records_from_approval(approval, **first_override):
    records = []
    for identity in approval["exact_trace_identities"]:
        kind, artifact_id, version_hash = identity.split(":", 2)
        records.append(
            {
                "kind": kind,
                "id": artifact_id,
                "version_hash": version_hash,
                "metadata_source": "CALLER_SUPPLIED_ACTIVE_VAULT_HASH_METADATA_ONLY",
                "body_included": False,
                "body_read": False,
                "body_copied": False,
                "body_hashed": False,
                "protected_path_accessed": False,
            }
        )
    records[0].update(first_override)
    return records


def valid_execution_request(approval=None, **overrides):
    if approval is None:
        approval = valid_blk139_approval_package()
    request = {
        "execution_package_id": COMPARISON_EXECUTION_PACKAGE_ID,
        "operator_identity": approval["operator_identity"],
        "execution_scope": EXECUTION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "approval_capture_package_id": approval["approval_capture_package_id"],
        "approval_capture_package_hash": approval["approval_capture_package_hash"],
        "approval_id": approval["approval_id"],
        "run_id_to_consume": approval["future_run_id"],
        "beo_id": approval["beo_id"],
        "beb_id": approval["beb_id"],
        "exact_trace_identities": list(approval["exact_trace_identities"]),
        "active_metadata_records": metadata_records_from_approval(approval),
        "requested_at": "2099-05-15T13:20:00+10:00",
        "expires_at": "2099-05-16T13:00:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {
            "exact_blk139_approval_reviewed": True,
            "future_run_id_consumed_once_in_record": True,
            "metadata_hash_only_comparison_scope_preserved": True,
            "no_active_vault_filesystem_read": True,
            "no_protected_body_reads": True,
            "no_protected_body_copy_parse_hash_scan": True,
            "no_rtm_generation": True,
            "no_drift_rejection_or_authoritative_drift_decision": True,
            "no_coverage_truth": True,
            "no_reusable_blk_link_authority": True,
            "no_beb_dispatch_or_beo_closeout": True,
            "no_signer_storage_ledger_side_effects": True,
            "no_target_source_git_mutation": True,
            "no_blk_pipe_blk_test_codex_tooling": True,
            "no_production_isolation_claim": True,
        },
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        request[flag] = False
    request.update(overrides)
    return request


def rehash_approval_package(package):
    package["approval_capture_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "approval_capture_package_hash"}
    )
    return package


class ActiveVaultHashComparisonExecutionRecordTest(unittest.TestCase):
    def test_consumes_exact_blk139_approval_and_emits_metadata_hash_match_record_only(self):
        approval = valid_blk139_approval_package()
        request = valid_execution_request(approval)

        package = build_active_vault_hash_comparison_execution_record(approval, request)

        self.assertEqual(package["execution_status"], EXECUTION_STATUS)
        self.assertEqual(package["execution_package_id"], COMPARISON_EXECUTION_PACKAGE_ID)
        self.assertEqual(package["comparison_record_id"], COMPARISON_RECORD_ID)
        self.assertEqual(package["execution_scope"], EXECUTION_SCOPE)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["approval_capture_package_id"], approval["approval_capture_package_id"])
        self.assertEqual(package["approval_capture_package_hash"], approval["approval_capture_package_hash"])
        self.assertEqual(package["approval_id"], approval["approval_id"])
        self.assertEqual(package["run_id_consumed"], RUN_ID_CONSUMED)
        self.assertTrue(package["future_run_id_consumed"])
        self.assertTrue(package["active_vault_hash_comparison_performed"])
        self.assertTrue(package["metadata_hashes_match"])
        self.assertEqual(package["comparison_result"], "ACTIVE_VAULT_METADATA_HASHES_MATCH_RECORDED_NOT_DRIFT_DECISION")
        self.assertEqual(package["next_frontier"], NEXT_FRONTIER)
        self.assertEqual(package["execution_request_hash"], _canonical_hash(request))
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        self.assertEqual(package["comparison_record"]["comparison_record_id"], COMPARISON_RECORD_ID)
        self.assertEqual(package["comparison_record"]["metadata_hashes_match"], True)
        self.assertFalse(package["comparison_record"]["drift_decision_made"])
        self.assertEqual(package["comparison_record_hash"], _canonical_hash({k: v for k, v in package["comparison_record"].items() if k != "comparison_record_hash"}))
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(package["active_vault_hash_comparison_performed"], True)
        self.assertEqual(package["execution_package_hash"], _canonical_hash({k: v for k, v in package.items() if k != "execution_package_hash"}))

    def test_records_version_hash_mismatch_without_drift_rejection_or_decision(self):
        approval = valid_blk139_approval_package()
        records = metadata_records_from_approval(approval, version_hash="sha256:" + "f" * 64)
        request = valid_execution_request(approval, active_metadata_records=records)

        package = build_active_vault_hash_comparison_execution_record(approval, request)

        self.assertFalse(package["metadata_hashes_match"])
        self.assertEqual(package["comparison_result"], "ACTIVE_VAULT_METADATA_HASH_MISMATCH_RECORDED_NOT_DRIFT_DECISION")
        self.assertTrue(package["active_vault_hash_comparison_performed"])
        self.assertFalse(package["drift_decision_made"])
        self.assertFalse(package["rtm_drift_rejection_performed"])
        mismatch = package["comparison_record"]["mismatches"][0]
        self.assertEqual(mismatch["kind"], "REQ")
        self.assertEqual(mismatch["id"], "REQ-001")
        self.assertEqual(mismatch["expected_version_hash"], "sha256:" + "a" * 64)
        self.assertEqual(mismatch["observed_version_hash"], "sha256:" + "f" * 64)

    def test_rejects_forged_wrong_or_replayed_approval_and_bad_execution_window(self):
        approval = valid_blk139_approval_package()
        request = valid_execution_request(approval)

        forged = copy.deepcopy(approval)
        forged["approval_capture_package_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "approval_capture_package_hash does not match submitted BLK-139 package"):
            build_active_vault_hash_comparison_execution_record(forged, request)

        forged = copy.deepcopy(approval)
        forged["future_run_id"] = "RUN-BLK-SYSTEM-１４０-ACTIVE-VAULT-HASH-COMPARISON-001"
        rehash_approval_package(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-139 approval package"):
            build_active_vault_hash_comparison_execution_record(forged, valid_execution_request(forged))

        for patch, message in [
            ({"run_id_to_consume": "RUN-BLK-SYSTEM-１４０-ACTIVE-VAULT-HASH-COMPARISON-001"}, "run_id_to_consume must be"),
            ({"requested_at": "2099-05-15T13:09:00+10:00"}, "requested_at must be at or after approval decided_at"),
            ({"requested_at": approval["expires_at"]}, "requested_at must be before approval expires_at"),
            ({"expires_at": "2099-05-17T13:00:00+10:00"}, "expires_at must not exceed approval expires_at"),
            ({"expired": True}, "execution request must not be expired"),
            ({"replayed": True}, "execution request must not be replayed"),
            ({"stale": True}, "execution request must not be stale"),
            ({"future_run_id_consumed": True}, "future_run_id_consumed must remain false before execution"),
            ({"rtm_generated": True}, "rtm_generated must remain false"),
        ]:
            candidate = copy.deepcopy(request)
            candidate.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_active_vault_hash_comparison_execution_record(approval, candidate)

    def test_rejects_extra_missing_duplicate_malformed_or_body_bearing_metadata_records(self):
        approval = valid_blk139_approval_package()
        base = valid_execution_request(approval)
        extra = metadata_records_from_approval(approval) + [
            {
                "kind": "REQ",
                "id": "REQ-999",
                "version_hash": "sha256:" + "9" * 64,
                "metadata_source": "CALLER_SUPPLIED_ACTIVE_VAULT_HASH_METADATA_ONLY",
                "body_included": False,
                "body_read": False,
                "body_copied": False,
                "body_hashed": False,
                "protected_path_accessed": False,
            }
        ]
        cases = [
            ({"active_metadata_records": extra}, "metadata kind/id must match approved trace identity"),
            ({"active_metadata_records": metadata_records_from_approval(approval)[:1]}, "active_metadata_records must match exact trace identity set"),
            ({"active_metadata_records": [metadata_records_from_approval(approval)[0], metadata_records_from_approval(approval)[0]]}, "active_metadata_records must not contain duplicates"),
            ({"active_metadata_records": metadata_records_from_approval(approval, kind="RTM")}, "metadata kind/id must match approved trace identity"),
            ({"active_metadata_records": metadata_records_from_approval(approval, version_hash="not-a-hash")}, "version_hash must be canonical sha256"),
            ({"active_metadata_records": metadata_records_from_approval(approval, body="The system shall...")}, "unexpected metadata field"),
            ({"active_metadata_records": metadata_records_from_approval(approval, body_read=True)}, "body_read must remain false"),
            ({"active_metadata_records": metadata_records_from_approval(approval, metadata_source="ACTIVE_VAULT_BODY_READ")}, "metadata_source must be"),
        ]
        for patch, message in cases:
            candidate = copy.deepcopy(base)
            candidate.update(patch)
            with self.subTest(message=message):
                with self.assertRaisesRegex(ValueError, message):
                    build_active_vault_hash_comparison_execution_record(approval, candidate)

    def test_rejects_authority_laundering_protected_paths_and_extra_fields(self):
        approval = valid_blk139_approval_package()
        base = valid_execution_request(approval)
        cases = [
            ({"execution_package_id": "ACTIVE-VAULT-HASH-COMPARISON-EXECUTION-140-docs%2525252Frequirements%2525252Factive"}, "protected body text"),
            ({"execution_package_id": "ACTIVE-VAULT-HASH-COMPARISON-EXECUTION-140-The%20system%20shall"}, "protected body text"),
            ({"selected_frontier": "activeVaultHashComparisonAndRTMGeneration"}, "selected_frontier must be|authority-laundering text"),
            ({"operator_identity": "discord:684235178083745819-DriftRejectionExecuted"}, "authority-laundering text"),
            ({"sourceMutationAttempted": False}, "unexpected field"),
            ({"operator_attestation": base["operator_attestation"] | {"RTMGenerated": True}}, "unexpected field"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS) + [sorted(EXACT_PROOF_OBLIGATIONS)[0]]}, "proof_obligations must not contain duplicates"),
            ({"excluded_authorities": ["NOPE"]}, "excluded_authorities must match exact denied authority set"),
        ]
        for patch, message in cases:
            candidate = copy.deepcopy(base)
            candidate.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_active_vault_hash_comparison_execution_record(approval, candidate)

    def test_returned_execution_record_is_defensively_copied_and_hash_bound(self):
        approval = valid_blk139_approval_package()
        request = valid_execution_request(approval)
        package = build_active_vault_hash_comparison_execution_record(approval, request)

        request["operator_attestation"]["no_coverage_truth"] = "mutated"
        request["active_metadata_records"][0]["version_hash"] = "sha256:" + "f" * 64
        approval["exact_trace_identities"].append("REQ:REQ-999:sha256:" + "9" * 64)

        self.assertIsNot(package["operator_attestation"], request["operator_attestation"])
        self.assertIs(package["operator_attestation"]["no_coverage_truth"], True)
        self.assertNotEqual(package["active_metadata_records"][0]["version_hash"], "sha256:" + "f" * 64)
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
