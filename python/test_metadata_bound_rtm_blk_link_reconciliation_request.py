import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from metadata_bound_rtm_blk_link_reconciliation_preflight import (
    build_metadata_bound_rtm_blk_link_reconciliation_preflight,
    valid_metadata_bound_rtm_blk_link_reconciliation_preflight_request,
)
from test_metadata_bound_rtm_blk_link_reconciliation_preflight import valid_blk152_finality_package

from metadata_bound_rtm_blk_link_reconciliation_request import (
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY,
    REQUEST_PACKAGE_ID,
    REQUEST_SCOPE,
    REQUEST_STATUS,
    SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS,
    build_metadata_bound_rtm_blk_link_reconciliation_request,
    valid_metadata_bound_rtm_blk_link_reconciliation_request,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "metadata_bound_rtm_blk_link_reconciliation_request.py"


def valid_blk153_preflight_package():
    finality = valid_blk152_finality_package()
    request = valid_metadata_bound_rtm_blk_link_reconciliation_preflight_request(finality)
    return build_metadata_bound_rtm_blk_link_reconciliation_preflight(finality, request)


def rehash_preflight_package(package):
    package["preflight_package_hash"] = _canonical_hash({k: v for k, v in package.items() if k != "preflight_package_hash"})
    return package


class MetadataBoundRtmBlkLinkReconciliationRequestTest(unittest.TestCase):
    def test_builds_request_only_package_bound_to_exact_blk153_preflight(self):
        preflight = valid_blk153_preflight_package()
        request = valid_metadata_bound_rtm_blk_link_reconciliation_request(preflight)

        package = build_metadata_bound_rtm_blk_link_reconciliation_request(preflight, request)

        self.assertEqual(package["request_status"], REQUEST_STATUS)
        self.assertEqual(package["request_package_id"], REQUEST_PACKAGE_ID)
        self.assertEqual(package["request_scope"], REQUEST_SCOPE)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["upstream_preflight_package_id"], "METADATA-BOUND-RTM-BLK-LINK-RECONCILIATION-PREFLIGHT-153-001")
        self.assertEqual(package["upstream_preflight_package_hash"], "sha256:06bedb092d14d483ca12e41226330dc7a2a62e3b7235f9215af9aa8e2b13f936")
        self.assertEqual(package["beo_id"], "BEO_126")
        self.assertEqual(package["beb_id"], "BEB_126")
        self.assertTrue(package["request_future_bounded_metadata_reconciliation_approval"])
        self.assertEqual(package["next_required_authority"], NEXT_REQUIRED_AUTHORITY)
        self.assertFalse(package["approval_capture_performed"])
        self.assertFalse(package["future_run_id_reserved"])
        self.assertFalse(package["rtm_generated"])
        self.assertFalse(package["production_blk_link_executed"])
        self.assertEqual(package["authority_request_hash"], _canonical_hash(request))
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(
            package["request_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "request_package_hash"}),
        )

    def test_rejects_forged_rehashed_or_wrong_blk153_preflight(self):
        preflight = valid_blk153_preflight_package()
        request = valid_metadata_bound_rtm_blk_link_reconciliation_request(preflight)

        forged = copy.deepcopy(preflight)
        forged["preflight_package_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "preflight_package_hash does not match submitted BLK-153 package"):
            build_metadata_bound_rtm_blk_link_reconciliation_request(forged, request)

        forged = copy.deepcopy(preflight)
        forged["preflight_package_id"] = "METADATA-BOUND-RTM-BLK-LINK-RECONCILIATION-PREFLIGHT-154-001"
        rehash_preflight_package(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-153 preflight package required"):
            build_metadata_bound_rtm_blk_link_reconciliation_request(
                forged,
                valid_metadata_bound_rtm_blk_link_reconciliation_request(forged),
            )

    def test_request_rejects_approval_execution_drift_coverage_protected_body_and_bad_sets(self):
        preflight = valid_blk153_preflight_package()
        base = valid_metadata_bound_rtm_blk_link_reconciliation_request(preflight)
        cases = [
            ({"request_package_id": "METADATA-BOUND-RTM-BLK-LINK-RECONCILIATION-REQUEST-１５４-001"}, "request_package_id must be"),
            ({"selected_frontier": "metadataBoundRtmBlkLinkGenerateRTM"}, "selected_frontier must be|authority-laundering text"),
            ({"approval_capture_performed": True}, "approval_capture_performed must remain false"),
            ({"future_run_id_reserved": True}, "future_run_id_reserved must remain false"),
            ({"rtm_generated": True}, "rtm_generated must remain false"),
            ({"rtm_drift_rejection_authorized": True}, "rtm_drift_rejection_authorized must remain false"),
            ({"coverage_truth_established": True}, "coverage_truth_established must remain false"),
            ({"protected_body_reads": True}, "protected_body_reads must remain false"),
            ({"reusable_blk_link_authority_granted": True}, "reusable_blk_link_authority_granted must remain false"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"excluded_authorities": ["NOPE"]}, "excluded_authorities must match exact denied authority set"),
        ]
        for patch, message in cases:
            request = copy.deepcopy(base)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_metadata_bound_rtm_blk_link_reconciliation_request(preflight, request)

    def test_rejects_nested_authority_laundering_protected_paths_body_text_tooling_and_extra_fields(self):
        preflight = valid_blk153_preflight_package()
        base = valid_metadata_bound_rtm_blk_link_reconciliation_request(preflight)
        cases = [
            ({"operator_identity": "discord:684235178083745819-RTMGenerated"}, "authority-laundering text"),
            ({"request_scope": "REQUEST_AND_COVERAGE_TRUTH"}, "request_scope must be|authority-laundering text"),
            ({"request_package_id": "METADATA-BOUND-RTM-BLK-LINK-RECONCILIATION-REQUEST-154-docs%2525252Frequirements%2525252Factive"}, "authority-laundering text|protected body text"),
            ({"request_package_id": "METADATA-BOUND-RTM-BLK-LINK-RECONCILIATION-REQUEST-154-The%20system%20shall"}, "protected body text"),
            ({"curlWrapper": False}, "unexpected field"),
            ({"operator_attestation": base["operator_attestation"] | {"generateRTM": True}}, "unexpected field"),
        ]
        for patch, message in cases:
            request = copy.deepcopy(base)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_metadata_bound_rtm_blk_link_reconciliation_request(preflight, request)

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
