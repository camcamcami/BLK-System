import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from metadata_bound_external_beo_publication_approval_capture import (
    APPROVAL_DECISION_PACKAGE_ID as BLK128_APPROVAL_DECISION_PACKAGE_ID,
    APPROVAL_ID as BLK128_APPROVAL_ID,
    FUTURE_PUBLICATION_EXECUTION_RUN_ID as BLK128_FUTURE_RUN_ID,
    STATUS as BLK128_STATUS,
    build_metadata_bound_external_beo_publication_approval_capture,
)
from test_metadata_bound_external_beo_publication_approval_capture import valid_decision, valid_request_package

from metadata_bound_external_beo_publication_execution import (
    EXECUTION_PACKAGE_ID,
    EXECUTION_SCOPE,
    EXECUTION_STATUS,
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    RUN_ID,
    SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS,
    build_metadata_bound_external_beo_publication_execution,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "metadata_bound_external_beo_publication_execution.py"


def valid_approval_capture_package():
    return build_metadata_bound_external_beo_publication_approval_capture(valid_request_package(), valid_decision())


def valid_execution_request(approval_package=None, **overrides):
    if approval_package is None:
        approval_package = valid_approval_capture_package()
    request = {
        "execution_package_id": EXECUTION_PACKAGE_ID,
        "operator_identity": approval_package["operator_identity"],
        "execution_scope": EXECUTION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "approval_decision_package_id": approval_package["approval_decision_package_id"],
        "approval_capture_package_hash": approval_package["approval_capture_package_hash"],
        "approval_id": approval_package["approval_id"],
        "run_id": approval_package["future_publication_execution_run_id"],
        "upstream_request_package_id": approval_package["upstream_request_package_id"],
        "upstream_request_package_hash": approval_package["upstream_request_package_hash"],
        "beo_id": approval_package["beo_id"],
        "beb_id": approval_package["beb_id"],
        "exact_trace_identities": list(approval_package["exact_trace_identities"]),
        "execute_external_beo_publication": True,
        "signer_key_material_access": False,
        "cryptographic_signing": False,
        "immutable_storage_write": False,
        "public_ledger_mutation": False,
        "rollback_revocation_supersession_execution": False,
        "rtm_generation": False,
        "rtm_drift_rejection": False,
        "protected_body_reads": False,
        "target_repo_scan_or_mutation": False,
        "source_or_git_mutation_by_fixture": False,
        "blk_pipe_blk_test_codex_runtime": False,
        "package_network_model_browser_cyber_tooling": False,
        "production_isolation_claim": False,
        "requested_at": "2099-05-15T10:15:00+10:00",
        "expires_at": "2099-05-15T10:30:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {
            "exact_blk128_approval_capture_reviewed": True,
            "run_id_marked_consumed_in_record_only": True,
            "published_record_is_exact_metadata_bound_beo_identity": True,
            "trace_metadata_only_no_protected_body_copy": True,
            "signer_storage_ledger_rollback_side_effects_excluded": True,
            "rtm_generation_and_drift_excluded": True,
            "protected_body_reads_excluded": True,
            "target_source_git_mutation_excluded": True,
            "blk_pipe_blk_test_codex_tooling_excluded": True,
            "no_production_isolation_claim": True,
        },
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    request.update(overrides)
    return request


def rehash_approval_capture_package(package):
    package["approval_capture_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "approval_capture_package_hash"}
    )
    return package


class MetadataBoundExternalBeoPublicationExecutionTest(unittest.TestCase):
    def test_builds_exact_external_publication_record_without_adjacent_side_effects(self):
        approval_package = valid_approval_capture_package()
        execution_request = valid_execution_request(approval_package)

        package = build_metadata_bound_external_beo_publication_execution(approval_package, execution_request)

        self.assertEqual(package["execution_status"], EXECUTION_STATUS)
        self.assertEqual(package["execution_package_id"], EXECUTION_PACKAGE_ID)
        self.assertEqual(package["execution_scope"], EXECUTION_SCOPE)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["approval_decision_package_id"], BLK128_APPROVAL_DECISION_PACKAGE_ID)
        self.assertEqual(package["approval_capture_package_hash"], approval_package["approval_capture_package_hash"])
        self.assertEqual(package["approval_id"], BLK128_APPROVAL_ID)
        self.assertEqual(package["run_id_consumed"], RUN_ID)
        self.assertEqual(RUN_ID, BLK128_FUTURE_RUN_ID)
        self.assertTrue(package["external_beo_publication_executed"])
        self.assertTrue(package["future_publication_execution_run_id_consumed"])
        self.assertEqual(package["execution_request_hash"], _canonical_hash(execution_request))
        self.assertEqual(package["requested_at"], execution_request["requested_at"])
        self.assertEqual(package["expires_at"], execution_request["expires_at"])
        self.assertFalse(package["expired"])
        self.assertFalse(package["replayed"])
        self.assertFalse(package["stale"])
        self.assertEqual(package["beo_publication"], "PUBLISHED_EXTERNAL_BEO_RECORD")
        self.assertEqual(package["rtm_status"], "NOT_GENERATED")
        self.assertEqual(package["exact_trace_identities"], approval_package["exact_trace_identities"])
        self.assertIn("publication_record", package)
        record = package["publication_record"]
        self.assertEqual(record["publication_mode"], "EXTERNAL_BEO_PUBLICATION_RECORD_ONLY")
        self.assertEqual(record["published_beo_id"], approval_package["beo_id"])
        self.assertEqual(record["published_beb_id"], approval_package["beb_id"])
        self.assertEqual(record["exact_trace_identities"], approval_package["exact_trace_identities"])
        self.assertEqual(record["signature_status"], "NOT_SIGNED_NO_KEY_MATERIAL")
        self.assertEqual(record["storage_status"], "NOT_WRITTEN_REPOSITORY_RECORD_ONLY")
        self.assertEqual(record["ledger_status"], "NOT_APPENDED_REPOSITORY_RECORD_ONLY")
        self.assertEqual(record["rollback_status"], "NOT_EXECUTED_POLICY_BOUND_ONLY")
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(
            record["publication_record_hash"],
            _canonical_hash({key: value for key, value in record.items() if key != "publication_record_hash"}),
        )
        self.assertEqual(
            package["execution_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "execution_package_hash"}),
        )

    def test_rejects_forged_rehashed_or_already_executed_blk128_approval_capture_package(self):
        approval_package = valid_approval_capture_package()
        execution_request = valid_execution_request(approval_package)

        forged = copy.deepcopy(approval_package)
        forged["beo_id"] = "BEO_999"
        with self.assertRaisesRegex(ValueError, "approval_capture_package_hash does not match submitted BLK-128 package"):
            build_metadata_bound_external_beo_publication_execution(forged, execution_request)

        forged = copy.deepcopy(approval_package)
        forged["beo_id"] = "BEO_999"
        rehash_approval_capture_package(forged)
        request = valid_execution_request(forged)
        with self.assertRaisesRegex(ValueError, "approval package must match canonical BLK-128 approval capture"):
            build_metadata_bound_external_beo_publication_execution(forged, request)

        forged = copy.deepcopy(approval_package)
        forged["future_publication_execution_run_id_consumed"] = True
        rehash_approval_capture_package(forged)
        request = valid_execution_request(forged)
        with self.assertRaisesRegex(ValueError, "approval package must match canonical BLK-128 approval capture"):
            build_metadata_bound_external_beo_publication_execution(forged, request)

    def test_rejects_bad_scope_retargeting_replay_expiry_sets_unicode_ids_and_side_effects(self):
        approval_package = valid_approval_capture_package()
        base_request = valid_execution_request(approval_package)
        cases = [
            ({"execution_package_id": "BEO-PUBLICATION-EXECUTION-１２９-００１"}, "execution_package_id must be"),
            ({"selected_frontier": "rtm_generation"}, "selected_frontier must be"),
            ({"execution_scope": "EXTERNAL_BEO_PUBLICATION_AND_RTM_GENERATION"}, "execution_scope must be"),
            ({"execute_external_beo_publication": False}, "execute_external_beo_publication must be true"),
            ({"approval_decision_package_id": "BEO-PUBLICATION-APPROVAL-CAPTURE-128-999"}, "approval_decision_package_id must match"),
            ({"approval_id": "APPROVAL-BLK-SYSTEM-129-OTHER"}, "approval_id must match"),
            ({"run_id": "RUN-BLK-SYSTEM-129-OTHER"}, "run_id must match"),
            ({"run_id": BLK128_APPROVAL_ID}, "run_id must match"),
            ({"beo_id": "BEO_999"}, "beo_id must match"),
            ({"exact_trace_identities": ["REQ:REQ-１２９:sha256:" + "a" * 64]}, "exact_trace_identities id must be exact"),
            ({"expired": True}, "execution request must not be expired"),
            ({"replayed": True}, "execution request must not be replayed"),
            ({"stale": True}, "execution request must not be stale"),
            ({"expires_at": base_request["requested_at"]}, "expires_at must be after requested_at"),
            ({"requested_at": "2000-01-01T00:00:00+10:00", "expires_at": "2000-01-01T01:00:00+10:00"}, "execution request must not be calendar-expired"),
            ({"requested_at": "2099-05-15T09:00:00+10:00", "expires_at": "2099-05-15T10:20:00+10:00"}, "execution request must not predate BLK-128 approval capture"),
            ({"requested_at": "2099-05-15T10:30:00+10:00", "expires_at": "2099-05-15T11:30:00+10:00"}, "execution request window must end within BLK-128 approval expiry"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS) + [sorted(EXACT_PROOF_OBLIGATIONS)[0]]}, "proof_obligations must not contain duplicates"),
            ({"excluded_authorities": ["NOPE"]}, "excluded_authorities must match exact denied authority set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES) + [sorted(EXACT_EXCLUDED_AUTHORITIES)[0]]}, "excluded_authorities must not contain duplicates"),
        ]
        for patch, message in cases:
            request = copy.deepcopy(base_request)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_metadata_bound_external_beo_publication_execution(approval_package, request)

        for boolean_key in [
            "signer_key_material_access",
            "cryptographic_signing",
            "immutable_storage_write",
            "public_ledger_mutation",
            "rollback_revocation_supersession_execution",
            "rtm_generation",
            "rtm_drift_rejection",
            "protected_body_reads",
            "target_repo_scan_or_mutation",
            "source_or_git_mutation_by_fixture",
            "blk_pipe_blk_test_codex_runtime",
            "package_network_model_browser_cyber_tooling",
            "production_isolation_claim",
        ]:
            request = copy.deepcopy(base_request)
            request[boolean_key] = True
            with self.subTest(boolean_key=boolean_key):
                with self.assertRaisesRegex(ValueError, f"{boolean_key} must remain false"):
                    build_metadata_bound_external_beo_publication_execution(approval_package, request)

    def test_rejects_signing_storage_ledger_rtm_protected_source_git_tooling_and_extra_field_laundering(self):
        approval_package = valid_approval_capture_package()
        execution_request = valid_execution_request(approval_package)
        cases = [
            ({"operator_identity": "discord:684235178083745819-SigningGranted"}, "authority-laundering text"),
            ({"execution_package_id": "BEO-PUBLICATION-EXECUTION-129-SignatureGenerated"}, "authority-laundering text"),
            ({"execution_package_id": "BEO-PUBLICATION-EXECUTION-129-Signature%47enerated"}, "authority-laundering text"),
            ({"execution_package_id": "BEO-PUBLICATION-EXECUTION-129-ImmutableStorageWritten"}, "authority-laundering text"),
            ({"execution_package_id": "BEO-PUBLICATION-EXECUTION-129-PublicLedgerMutated"}, "authority-laundering text"),
            ({"execution_package_id": "BEO-PUBLICATION-EXECUTION-129-RTMGeneration"}, "authority-laundering text"),
            ({"execution_package_id": "BEO-PUBLICATION-EXECUTION-129-docs%2525252Frequirements%2525252Factive"}, "authority-laundering text|protected BLK-req body"),
            ({"execution_package_id": "BEO-PUBLICATION-EXECUTION-129-sourceGitAuthorized"}, "authority-laundering text"),
            ({"execution_package_id": "BEO-PUBLICATION-EXECUTION-129-packageManagersAuthorized"}, "authority-laundering text"),
            ({"execution_package_id": "BEO-PUBLICATION-EXECUTION-129-productionSandboxAuthorized"}, "authority-laundering text"),
            ({"sourceMutationAttempted": False}, "unexpected field"),
            ({"operator_attestation": execution_request["operator_attestation"] | {"SigningGranted": True}}, "unexpected field"),
        ]
        for patch, message in cases:
            request = copy.deepcopy(execution_request)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_metadata_bound_external_beo_publication_execution(approval_package, request)

    def test_execution_request_window_is_hash_bound_in_output_evidence(self):
        approval_package = valid_approval_capture_package()
        base_request = valid_execution_request(approval_package)
        alt_request = valid_execution_request(
            approval_package,
            requested_at="2099-05-15T10:20:00+10:00",
            expires_at="2099-05-15T10:45:00+10:00",
        )

        base_package = build_metadata_bound_external_beo_publication_execution(approval_package, base_request)
        alt_package = build_metadata_bound_external_beo_publication_execution(approval_package, alt_request)

        self.assertEqual(base_package["execution_request_hash"], _canonical_hash(base_request))
        self.assertEqual(alt_package["execution_request_hash"], _canonical_hash(alt_request))
        self.assertNotEqual(base_package["execution_request_hash"], alt_package["execution_request_hash"])
        self.assertNotEqual(base_package["execution_package_hash"], alt_package["execution_package_hash"])
        self.assertEqual(base_package["requested_at"], base_request["requested_at"])
        self.assertEqual(alt_package["requested_at"], alt_request["requested_at"])

    def test_returned_package_defensively_copies_hash_bound_nested_inputs(self):
        approval_package = valid_approval_capture_package()
        execution_request = valid_execution_request(approval_package)

        package = build_metadata_bound_external_beo_publication_execution(approval_package, execution_request)
        execution_request["operator_attestation"]["published_record_is_exact_metadata_bound_beo_identity"] = "mutated"
        approval_package["exact_trace_identities"].append("REQ:REQ-999:sha256:" + "f" * 64)

        self.assertIsNot(package["operator_attestation"], execution_request["operator_attestation"])
        self.assertIs(package["operator_attestation"]["published_record_is_exact_metadata_bound_beo_identity"], True)
        self.assertNotIn("REQ:REQ-999:sha256:" + "f" * 64, package["exact_trace_identities"])
        self.assertEqual(
            package["execution_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "execution_package_hash"}),
        )

    def test_module_has_no_live_runtime_external_tooling_or_signer_storage_ledger_imports(self):
        tree = ast.parse(MODULE.read_text())
        imported = set()
        calls = set()
        forbidden_imports = {"subprocess", "socket", "requests", "urllib3", "httpx", "shutil"}
        forbidden_calls = {"system", "popen", "Popen", "run", "call", "check_call", "check_output", "exec", "eval", "open", "urlopen", "request"}
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
