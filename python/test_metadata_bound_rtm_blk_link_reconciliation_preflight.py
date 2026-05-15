import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from authoritative_beo_publication_finality import build_authoritative_beo_publication_finality, valid_authoritative_finality_request
from test_authoritative_beo_publication_finality import valid_closure_package

from metadata_bound_rtm_blk_link_reconciliation_preflight import (
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY,
    PREFLIGHT_PACKAGE_ID,
    PREFLIGHT_SCOPE,
    PREFLIGHT_STATUS,
    SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS,
    build_metadata_bound_rtm_blk_link_reconciliation_preflight,
    valid_metadata_bound_rtm_blk_link_reconciliation_preflight_request,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "metadata_bound_rtm_blk_link_reconciliation_preflight.py"


def valid_blk152_finality_package():
    closure = valid_closure_package()
    request = valid_authoritative_finality_request(closure)
    return build_authoritative_beo_publication_finality(closure, request)


def rehash_finality_package(package):
    package["signature_receipt"]["signature_hash"] = _canonical_hash(
        {key: value for key, value in package["signature_receipt"].items() if key != "signature_hash"}
    )
    package["signature_hash"] = package["signature_receipt"]["signature_hash"]
    package["immutable_storage_receipt"]["signature_hash"] = package["signature_hash"]
    package["immutable_storage_receipt"]["storage_receipt_hash"] = _canonical_hash(
        {key: value for key, value in package["immutable_storage_receipt"].items() if key != "storage_receipt_hash"}
    )
    package["storage_receipt_hash"] = package["immutable_storage_receipt"]["storage_receipt_hash"]
    package["public_ledger_entry"]["signature_hash"] = package["signature_hash"]
    package["public_ledger_entry"]["storage_receipt_hash"] = package["storage_receipt_hash"]
    package["public_ledger_entry"]["ledger_entry_hash"] = _canonical_hash(
        {key: value for key, value in package["public_ledger_entry"].items() if key != "ledger_entry_hash"}
    )
    package["ledger_entry_hash"] = package["public_ledger_entry"]["ledger_entry_hash"]
    package["finality_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "finality_package_hash"}
    )
    return package


class MetadataBoundRtmBlkLinkReconciliationPreflightTest(unittest.TestCase):
    def test_builds_review_only_preflight_bound_to_exact_blk152_finality(self):
        finality = valid_blk152_finality_package()
        request = valid_metadata_bound_rtm_blk_link_reconciliation_preflight_request(finality)

        package = build_metadata_bound_rtm_blk_link_reconciliation_preflight(finality, request)

        self.assertEqual(package["preflight_status"], PREFLIGHT_STATUS)
        self.assertEqual(package["preflight_package_id"], PREFLIGHT_PACKAGE_ID)
        self.assertEqual(package["preflight_scope"], PREFLIGHT_SCOPE)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["operator_identity"], "discord:684235178083745819")
        self.assertEqual(package["upstream_finality_package_id"], "AUTHORITATIVE-BEO-PUBLICATION-FINALITY-152-001")
        self.assertEqual(
            package["upstream_finality_package_hash"],
            "sha256:fa661ce760a5df8d8c1d893a8b71b4ccbfa5b882e683e594511aa30984ba09a3",
        )
        self.assertEqual(
            package["upstream_signature_hash"],
            "sha256:3e93c9707b993453e221278287357470dcef6a424068a8bfbdf058868d5e3d5f",
        )
        self.assertEqual(
            package["upstream_storage_receipt_hash"],
            "sha256:f2bf49758e082ac68eb134f0c269f6f3e0bb8e32fa096f4d3bb049020cba60f3",
        )
        self.assertEqual(
            package["upstream_ledger_entry_hash"],
            "sha256:54e41a65821e6c05e203ee36734cb1a37d7a798519393c7de61b82a562f984f0",
        )
        self.assertEqual(package["beo_id"], "BEO_126")
        self.assertEqual(package["beb_id"], "BEB_126")
        self.assertTrue(package["metadata_only_reconciliation_preflight_ready"])
        self.assertFalse(package["operator_decision_captured"])
        self.assertFalse(package["future_run_id_reserved"])
        self.assertEqual(package["next_required_authority"], NEXT_REQUIRED_AUTHORITY)
        self.assertEqual(package["preflight_request_hash"], _canonical_hash(request))
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(
            package["preflight_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "preflight_package_hash"}),
        )

    def test_rejects_forged_rehashed_or_non_final_blk152_package(self):
        finality = valid_blk152_finality_package()
        request = valid_metadata_bound_rtm_blk_link_reconciliation_preflight_request(finality)

        forged = copy.deepcopy(finality)
        forged["finality_package_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "finality_package_hash does not match submitted BLK-152 finality package"):
            build_metadata_bound_rtm_blk_link_reconciliation_preflight(forged, request)

        forged = copy.deepcopy(finality)
        forged["finality_package_id"] = "AUTHORITATIVE-BEO-PUBLICATION-FINALITY-153-001"
        rehash_finality_package(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-152 finality package required"):
            build_metadata_bound_rtm_blk_link_reconciliation_preflight(
                forged,
                valid_metadata_bound_rtm_blk_link_reconciliation_preflight_request(forged),
            )

        forged = copy.deepcopy(finality)
        forged["rtm_status"] = "GENERATED"
        rehash_finality_package(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-152 finality package required|rtm_status must remain NOT_GENERATED"):
            build_metadata_bound_rtm_blk_link_reconciliation_preflight(
                forged,
                valid_metadata_bound_rtm_blk_link_reconciliation_preflight_request(forged),
            )

    def test_request_rejects_approval_execution_drift_coverage_protected_body_and_bad_sets(self):
        finality = valid_blk152_finality_package()
        base = valid_metadata_bound_rtm_blk_link_reconciliation_preflight_request(finality)
        cases = [
            ({"preflight_package_id": "METADATA-BOUND-RTM-BLK-LINK-RECONCILIATION-PREFLIGHT-１５３-001"}, "preflight_package_id must be"),
            ({"selected_frontier": "metadataBoundRtmBlkLinkGenerateRTM"}, "selected_frontier must be|authority-laundering text"),
            ({"operator_decision_captured": True}, "operator_decision_captured must remain false"),
            ({"future_run_id_reserved": True}, "future_run_id_reserved must remain false"),
            ({"rtm_generated": True}, "rtm_generated must remain false"),
            ({"rtm_drift_rejection_authorized": True}, "rtm_drift_rejection_authorized must remain false"),
            ({"coverage_truth_established": True}, "coverage_truth_established must remain false"),
            ({"protected_body_reads": True}, "protected_body_reads must remain false"),
            ({"reusable_blk_link_authority_granted": True}, "reusable_blk_link_authority_granted must remain false"),
            ({"signer_storage_ledger_reuse_authorized": True}, "signer_storage_ledger_reuse_authorized must remain false"),
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
                    build_metadata_bound_rtm_blk_link_reconciliation_preflight(finality, request)

    def test_rejects_nested_authority_laundering_protected_paths_body_text_tooling_and_extra_fields(self):
        finality = valid_blk152_finality_package()
        base = valid_metadata_bound_rtm_blk_link_reconciliation_preflight_request(finality)
        cases = [
            ({"operator_identity": "discord:684235178083745819-RTMGenerated"}, "authority-laundering text"),
            ({"preflight_scope": "PREFLIGHT_AND_COVERAGE_TRUTH"}, "preflight_scope must be|authority-laundering text"),
            ({"preflight_package_id": "METADATA-BOUND-RTM-BLK-LINK-RECONCILIATION-PREFLIGHT-153-docs%2525252Frequirements%2525252Factive"}, "authority-laundering text|protected body text"),
            ({"preflight_package_id": "METADATA-BOUND-RTM-BLK-LINK-RECONCILIATION-PREFLIGHT-153-The%20system%20shall"}, "protected body text"),
            ({"curlWrapper": False}, "unexpected field"),
            ({"operator_attestation": base["operator_attestation"] | {"generateRTM": True}}, "unexpected field"),
            ({"required_future_evidence": base["required_future_evidence"] + [{"reqBody": "The system shall remain hidden."}]}, "protected body text|authority-laundering text"),
        ]
        for patch, message in cases:
            request = copy.deepcopy(base)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_metadata_bound_rtm_blk_link_reconciliation_preflight(finality, request)

    def test_preflight_request_hash_is_bound_and_returned_inputs_are_defensively_copied(self):
        finality = valid_blk152_finality_package()
        base = valid_metadata_bound_rtm_blk_link_reconciliation_preflight_request(finality)
        alt = valid_metadata_bound_rtm_blk_link_reconciliation_preflight_request(
            finality,
            requested_at="2099-05-16T08:10:00+10:00",
            expires_at="2099-05-16T09:10:00+10:00",
        )

        base_package = build_metadata_bound_rtm_blk_link_reconciliation_preflight(finality, base)
        alt_package = build_metadata_bound_rtm_blk_link_reconciliation_preflight(finality, alt)

        self.assertEqual(base_package["preflight_request_hash"], _canonical_hash(base))
        self.assertEqual(alt_package["preflight_request_hash"], _canonical_hash(alt))
        self.assertNotEqual(base_package["preflight_request_hash"], alt_package["preflight_request_hash"])
        self.assertNotEqual(base_package["preflight_package_hash"], alt_package["preflight_package_hash"])

        base["operator_attestation"]["no_drift_rejection_or_coverage_truth"] = "mutated"
        finality["exact_trace_identities"].append("REQ:REQ-999:sha256:" + "9" * 64)
        self.assertIs(base_package["operator_attestation"]["no_drift_rejection_or_coverage_truth"], True)
        self.assertNotIn("REQ:REQ-999:sha256:" + "9" * 64, base_package["exact_trace_identities"])

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
