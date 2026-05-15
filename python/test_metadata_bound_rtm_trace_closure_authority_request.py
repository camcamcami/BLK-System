import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from metadata_bound_external_beo_publication_execution import build_metadata_bound_external_beo_publication_execution
from test_metadata_bound_external_beo_publication_execution import (
    valid_approval_capture_package,
    valid_execution_request,
)

from metadata_bound_rtm_trace_closure_authority_request import (
    AUTHORITY_REQUEST_PACKAGE_ID,
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY,
    REQUEST_SCOPE,
    REQUEST_STATUS,
    SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS,
    build_metadata_bound_rtm_trace_closure_authority_request,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "metadata_bound_rtm_trace_closure_authority_request.py"


def valid_blk129_execution_package():
    approval = valid_approval_capture_package()
    request = valid_execution_request(approval)
    return build_metadata_bound_external_beo_publication_execution(approval, request)


def valid_authority_request(upstream=None, **overrides):
    if upstream is None:
        upstream = valid_blk129_execution_package()
    request = {
        "authority_request_package_id": AUTHORITY_REQUEST_PACKAGE_ID,
        "operator_identity": "discord:684235178083745819",
        "request_scope": REQUEST_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_execution_package_id": upstream["execution_package_id"],
        "upstream_execution_package_hash": upstream["execution_package_hash"],
        "publication_record_hash": upstream["publication_record_hash"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "exact_trace_identities": list(upstream["exact_trace_identities"]),
        "request_future_exact_rtm_trace_closure_approval": True,
        "requested_at": "2099-05-15T11:15:00+10:00",
        "expires_at": "2099-05-15T12:15:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {
            "exact_blk129_publication_execution_reviewed": True,
            "external_beo_publication_record_is_hash_bound": True,
            "trace_metadata_only_no_protected_body_copy": True,
            "request_is_for_future_trace_closure_approval_not_execution": True,
            "local_non_authoritative_trace_closure_selected_for_next_rung": True,
            "production_blk_link_not_authorized": True,
            "rtm_generation_not_performed_by_request": True,
            "drift_rejection_excluded": True,
            "active_vault_hash_comparison_excluded": True,
            "coverage_truth_excluded": True,
            "protected_body_reads_excluded": True,
            "signer_storage_ledger_rollback_side_effects_excluded": True,
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


def rehash_execution_package(package):
    package["publication_record_hash"] = _canonical_hash(
        {key: value for key, value in package["publication_record"].items() if key != "publication_record_hash"}
    )
    package["publication_record"]["publication_record_hash"] = package["publication_record_hash"]
    package["execution_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "execution_package_hash"}
    )
    return package


class MetadataBoundRtmTraceClosureAuthorityRequestTest(unittest.TestCase):
    def test_builds_hash_bound_request_without_granting_trace_closure_or_rtm(self):
        upstream = valid_blk129_execution_package()
        request = valid_authority_request(upstream)

        package = build_metadata_bound_rtm_trace_closure_authority_request(upstream, request)

        self.assertEqual(package["request_status"], REQUEST_STATUS)
        self.assertEqual(package["authority_request_package_id"], AUTHORITY_REQUEST_PACKAGE_ID)
        self.assertEqual(package["request_scope"], REQUEST_SCOPE)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["upstream_execution_package_id"], "BEO-PUBLICATION-EXECUTION-129-001")
        self.assertEqual(
            package["upstream_execution_package_hash"],
            "sha256:80265ee8e5c5b4011b3e0c0e691f28b7fd74ca1c93b5a7b1d0a877300945af3c",
        )
        self.assertEqual(
            package["publication_record_hash"],
            "sha256:19aa4f377c06e103032fea28e91e82bec58f4f0c1f523e2f9797d8ab1df9d798",
        )
        self.assertEqual(package["beo_id"], "BEO_126")
        self.assertEqual(package["beb_id"], "BEB_126")
        self.assertEqual(package["exact_trace_identities"], upstream["exact_trace_identities"])
        self.assertEqual(package["requested_authority"], "ONE_FUTURE_LOCAL_NON_AUTHORITATIVE_RTM_TRACE_CLOSURE_APPROVAL")
        self.assertEqual(package["rtm_trace_closure_authority"], "REQUEST_ONLY_NOT_GRANTED")
        self.assertEqual(package["next_required_authority"], NEXT_REQUIRED_AUTHORITY)
        self.assertEqual(package["authority_request_hash"], _canonical_hash(request))
        self.assertEqual(package["requested_at"], request["requested_at"])
        self.assertEqual(package["expires_at"], request["expires_at"])
        self.assertFalse(package["expired"])
        self.assertFalse(package["replayed"])
        self.assertFalse(package["stale"])
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertRegex(package["authority_request_package_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(
            package["authority_request_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "authority_request_package_hash"}),
        )

    def test_rejects_forged_rehashed_or_wrong_blk129_publication_execution(self):
        upstream = valid_blk129_execution_package()
        request = valid_authority_request(upstream)

        forged = copy.deepcopy(upstream)
        forged["beo_id"] = "BEO_999"
        with self.assertRaisesRegex(ValueError, "execution_package_hash does not match submitted BLK-129 package"):
            build_metadata_bound_rtm_trace_closure_authority_request(forged, request)

        forged = copy.deepcopy(upstream)
        forged["beo_id"] = "BEO_999"
        rehash_execution_package(forged)
        forged_request = valid_authority_request(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-129 publication execution record"):
            build_metadata_bound_rtm_trace_closure_authority_request(forged, forged_request)

        forged = copy.deepcopy(upstream)
        forged["rtm_status"] = "GENERATED"
        rehash_execution_package(forged)
        forged_request = valid_authority_request(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-129 publication execution record"):
            build_metadata_bound_rtm_trace_closure_authority_request(forged, forged_request)

    def test_rejects_bad_scope_retargeting_replay_expiry_sets_unicode_ids_and_side_effects(self):
        upstream = valid_blk129_execution_package()
        base_request = valid_authority_request(upstream)
        cases = [
            ({"authority_request_package_id": "RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-１３０-００１"}, "authority_request_package_id must be"),
            ({"selected_frontier": "production_blk_link_execution"}, "selected_frontier must be"),
            ({"request_scope": "RTM_TRACE_CLOSURE_AND_RUNTIME_RTM_GENERATION"}, "request_scope must be"),
            ({"request_future_exact_rtm_trace_closure_approval": False}, "request_future_exact_rtm_trace_closure_approval must be true"),
            ({"upstream_execution_package_id": "BEO-PUBLICATION-EXECUTION-129-999"}, "upstream_execution_package_id must match"),
            ({"upstream_execution_package_hash": "sha256:" + "0" * 64}, "upstream_execution_package_hash must match"),
            ({"publication_record_hash": "sha256:" + "1" * 64}, "publication_record_hash must match"),
            ({"beo_id": "BEO_999"}, "beo_id must match"),
            ({"beb_id": "BEB_999"}, "beb_id must match"),
            ({"exact_trace_identities": ["REQ:REQ-１３０:sha256:" + "a" * 64]}, "exact_trace_identities id must be exact"),
            ({"expired": True}, "authority request must not be expired"),
            ({"replayed": True}, "authority request must not be replayed"),
            ({"stale": True}, "authority request must not be stale"),
            ({"expires_at": base_request["requested_at"]}, "expires_at must be after requested_at"),
            ({"requested_at": "2000-01-01T00:00:00+10:00", "expires_at": "2000-01-01T01:00:00+10:00"}, "authority request must not be calendar-expired"),
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
                    build_metadata_bound_rtm_trace_closure_authority_request(upstream, request)

        for boolean_key in SIDE_EFFECT_FLAGS:
            request = copy.deepcopy(base_request)
            request[boolean_key] = True
            with self.subTest(boolean_key=boolean_key):
                with self.assertRaisesRegex(ValueError, f"{boolean_key} must remain false"):
                    build_metadata_bound_rtm_trace_closure_authority_request(upstream, request)

    def test_rejects_nested_authority_laundering_protected_paths_body_text_tooling_and_extra_fields(self):
        upstream = valid_blk129_execution_package()
        base_request = valid_authority_request(upstream)
        cases = [
            ({"operator_identity": "discord:684235178083745819-RTMGenerationAuthorized"}, "authority-laundering text"),
            ({"authority_request_package_id": "RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-130-RTMGenerated"}, "authority-laundering text"),
            ({"authority_request_package_id": "RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-130-ActiveVaultHashComparison"}, "authority-laundering text"),
            ({"authority_request_package_id": "RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-130-docs%2525252Frequirements%2525252Factive"}, "authority-laundering text|protected BLK-req body"),
            ({"authority_request_package_id": "RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-130-The%20system%20shall"}, "protected body text"),
            ({"authority_request_package_id": "RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-130-productionBlkLinkAuthorized"}, "authority-laundering text"),
            ({"authority_request_package_id": "RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-130-coverageTruthEstablished"}, "authority-laundering text"),
            ({"authority_request_package_id": "RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-130-sourceMutationAuthorized"}, "authority-laundering text"),
            ({"authority_request_package_id": "RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-130-packageManagersAuthorized"}, "authority-laundering text"),
            ({"sourceMutationAttempted": False}, "unexpected field"),
            ({"operator_attestation": base_request["operator_attestation"] | {"RTMGenerationAuthorized": True}}, "unexpected field"),
        ]
        for patch, message in cases:
            request = copy.deepcopy(base_request)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_metadata_bound_rtm_trace_closure_authority_request(upstream, request)

    def test_authority_request_window_is_hash_bound_and_returned_inputs_are_defensively_copied(self):
        upstream = valid_blk129_execution_package()
        base_request = valid_authority_request(upstream)
        alt_request = valid_authority_request(upstream, requested_at="2099-05-15T11:30:00+10:00", expires_at="2099-05-15T12:30:00+10:00")

        base_package = build_metadata_bound_rtm_trace_closure_authority_request(upstream, base_request)
        alt_package = build_metadata_bound_rtm_trace_closure_authority_request(upstream, alt_request)

        self.assertEqual(base_package["authority_request_hash"], _canonical_hash(base_request))
        self.assertEqual(alt_package["authority_request_hash"], _canonical_hash(alt_request))
        self.assertNotEqual(base_package["authority_request_hash"], alt_package["authority_request_hash"])
        self.assertNotEqual(base_package["authority_request_package_hash"], alt_package["authority_request_package_hash"])

        base_request["operator_attestation"]["production_blk_link_not_authorized"] = "mutated"
        upstream["exact_trace_identities"].append("REQ:REQ-999:sha256:" + "f" * 64)
        self.assertIsNot(base_package["operator_attestation"], base_request["operator_attestation"])
        self.assertIs(base_package["operator_attestation"]["production_blk_link_not_authorized"], True)
        self.assertNotIn("REQ:REQ-999:sha256:" + "f" * 64, base_package["exact_trace_identities"])

    def test_module_has_no_live_runtime_tooling_or_protected_body_file_access(self):
        tree = ast.parse(MODULE.read_text())
        imported = set()
        calls = set()
        forbidden_imports = {"subprocess", "socket", "requests", "urllib3", "httpx", "shutil", "pathlib"}
        forbidden_calls = {"system", "popen", "Popen", "run", "call", "check_call", "check_output", "exec", "eval", "open", "read_text", "urlopen", "request"}
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
