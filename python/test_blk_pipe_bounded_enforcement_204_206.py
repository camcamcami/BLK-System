import copy
import unittest
from pathlib import Path

from blk_pipe_bounded_enforcement_204_206 import (
    BLK203_BRIDGE_RECONCILIATION_HASH,
    DEFAULT_204_PACKAGE_HASH,
    DEFAULT_205_PACKAGE_HASH,
    DEFAULT_206_PACKAGE_HASH,
    DENIED_AUTHORITIES,
    REQUIRED_FALSE_SIDE_EFFECT_FLAGS,
    build_204_surface_review_package,
    build_205_enforcement_contract_package,
    build_206_reconciliation_package,
    build_blk_pipe_closure_packages,
    canonical_package_hash,
    validate_204_surface_review_package,
    validate_205_enforcement_contract_package,
    validate_206_reconciliation_package,
)

ROOT = Path(__file__).resolve().parents[1]
BLK077 = ROOT / "docs" / "BLK-077_blk-system-post-078-roadmap.md"
BLK079 = ROOT / "docs" / "BLK-079_post-078-current-state-authority-index.md"
MODULE = ROOT / "python" / "blk_pipe_bounded_enforcement_204_206.py"


class BlkPipeBoundedEnforcementClosureTest(unittest.TestCase):
    def test_204_review_package_closes_surface_as_evidence_not_authority(self):
        package = build_204_surface_review_package()

        self.assertEqual(package["sprint_id"], "BLK-SYSTEM-204")
        self.assertEqual(package["surface"], "BLK-pipe blast shield")
        self.assertEqual(package["status"], "BLK_PIPE_SURFACE_REVIEW_READY_NOT_AUTHORITY")
        self.assertEqual(package["upstream_blk203_hash"], BLK203_BRIDGE_RECONCILIATION_HASH)
        self.assertEqual(package["package_hash"], DEFAULT_204_PACKAGE_HASH)
        self.assertEqual(package["package_hash"], canonical_package_hash(package))
        self.assertEqual(validate_204_surface_review_package(package), [])
        self.assertIn("internal/contracts/report.go", package["surface_files"])
        self.assertIn("internal/validationprofiles/profiles.go", package["surface_files"])
        self.assertIn("python/blk_pipe_adapter.py", package["surface_files"])
        self.assertIn("validation_profile_argv_evidence_only", package["bounded_evidence_surfaces"])
        self.assertIn("failure_class_denial_route_cleanup_status", package["bounded_evidence_surfaces"])

        for flag in REQUIRED_FALSE_SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(package["denied_authorities"], list(DENIED_AUTHORITIES))

    def test_205_contract_binds_exact_204_hash_and_rejects_self_consistent_rehash(self):
        review = build_204_surface_review_package()
        contract = build_205_enforcement_contract_package(review)

        self.assertEqual(contract["sprint_id"], "BLK-SYSTEM-205")
        self.assertEqual(contract["status"], "BLK_PIPE_BOUNDED_ENFORCEMENT_CONTRACT_READY_NOT_AUTHORITY")
        self.assertEqual(contract["upstream_204_package_hash"], DEFAULT_204_PACKAGE_HASH)
        self.assertEqual(contract["package_hash"], DEFAULT_205_PACKAGE_HASH)
        self.assertEqual(validate_205_enforcement_contract_package(contract), [])

        forged_review = copy.deepcopy(review)
        forged_review["bounded_evidence_surfaces"].append("operator asserted blkPipeSuccess after review")
        forged_review["package_hash"] = canonical_package_hash(forged_review)
        self.assertNotEqual(forged_review["package_hash"], DEFAULT_204_PACKAGE_HASH)
        with self.assertRaises(ValueError):
            build_205_enforcement_contract_package(forged_review)

    def test_206_reconciliation_binds_exact_204_and_205_hashes(self):
        review, contract, reconciliation = build_blk_pipe_closure_packages()

        self.assertEqual(reconciliation["sprint_id"], "BLK-SYSTEM-206")
        self.assertEqual(reconciliation["status"], "BLK_PIPE_BOUNDED_ENFORCEMENT_RECONCILED_CLEAN")
        self.assertEqual(reconciliation["upstream_204_package_hash"], DEFAULT_204_PACKAGE_HASH)
        self.assertEqual(reconciliation["upstream_205_package_hash"], DEFAULT_205_PACKAGE_HASH)
        self.assertEqual(reconciliation["package_hash"], DEFAULT_206_PACKAGE_HASH)
        self.assertEqual(validate_204_surface_review_package(review), [])
        self.assertEqual(validate_205_enforcement_contract_package(contract), [])
        self.assertEqual(validate_206_reconciliation_package(reconciliation), [])

        forged_contract = copy.deepcopy(contract)
        forged_contract["side_effect_obligations"]["production_isolation_claimed"] = True
        forged_contract["package_hash"] = canonical_package_hash(forged_contract)
        with self.assertRaises(ValueError):
            build_206_reconciliation_package(review, forged_contract)

    def test_denied_authority_lists_are_exact_no_duplicates_no_extras(self):
        package = build_204_surface_review_package()

        missing = copy.deepcopy(package)
        missing["denied_authorities"] = missing["denied_authorities"][:-1]
        missing["package_hash"] = canonical_package_hash(missing)
        self.assertIn("denied_authorities must match exact ordered list", "\n".join(validate_204_surface_review_package(missing)))

        duplicate = copy.deepcopy(package)
        duplicate["denied_authorities"] = list(DENIED_AUTHORITIES[:-1]) + [DENIED_AUTHORITIES[0]]
        duplicate["package_hash"] = canonical_package_hash(duplicate)
        self.assertIn("denied_authorities must match exact ordered list", "\n".join(validate_204_surface_review_package(duplicate)))

        extra = copy.deepcopy(package)
        extra["denied_authorities"] = list(DENIED_AUTHORITIES) + ["APPROVED_FOR_LIVE_EXECUTION"]
        extra["package_hash"] = canonical_package_hash(extra)
        self.assertIn("denied_authorities must match exact ordered list", "\n".join(validate_204_surface_review_package(extra)))

    def test_nested_notes_reject_authority_laundering_and_protected_paths(self):
        probes = [
            {"operator_notes": ["runtime pilot approved by operator; live pilot allowed"]},
            {"operator_notes": ["%62lk%50ipe%53uccess proves enforcement authority"]},
            {"caller_supplied_evidence_refs": {"metadata": {"approvalInherited": "yes"}}},
            {"caller_supplied_evidence_refs": {"docs%25252Factive%25252FREQ-001.md": "safe-looking ref"}},
            {"caller_supplied_evidence_refs": {"nested": ["productionIsolationClaimed"]}},
            {"caller_supplied_evidence_refs": {"network": "curl https://example.invalid/probe"}},
            {"operator_notes": ["The system shall expose protected body text"]},
        ]
        for patch in probes:
            package = build_204_surface_review_package()
            package.update(patch)
            package["package_hash"] = canonical_package_hash(package)
            with self.subTest(patch=patch):
                self.assertTrue(validate_204_surface_review_package(package))

    def test_contract_evidence_fields_cannot_be_reinterpreted_as_authority(self):
        contract = build_205_enforcement_contract_package(build_204_surface_review_package())
        self.assertEqual(
            contract["report_evidence_contract"],
            {
                "validation_profile_capabilities": "diagnostic_labels_only",
                "resolved_validation_argv": "repository_owned_structured_argv_evidence_only",
                "failure_class": "denial_taxonomy_not_permission",
                "denial_route": "fail_closed_route_not_permission",
                "cleanup_status": "post_run_evidence_not_production_isolation",
                "diff_summary": "bounded_change_summary_not_mutation_authority",
                "trace_artifacts": "metadata_hashes_only_not_protected_body_access",
            },
        )
        for field in contract["report_evidence_contract"]:
            self.assertNotIn(field, contract["authority_grant_fields"])
        self.assertEqual(contract["authority_grant_fields"], [])

    def test_module_does_not_import_live_execution_or_network_surfaces(self):
        source = MODULE.read_text()
        forbidden_imports = ("subprocess", "socket", "requests", "urllib", "http.client", "webbrowser")
        for token in forbidden_imports:
            self.assertNotIn(f"import {token}", source)
            self.assertNotIn(f"from {token}", source)
        for token in ("shell=True", "Popen(", "os.system", "eval(", "exec("):
            self.assertNotIn(token, source)

    def test_active_docs_record_blk_pipe_closure_without_new_authority(self):
        text077 = BLK077.read_text()
        text079 = BLK079.read_text()
        required = [
            "BLK_SYSTEM_206_BLK_PIPE_BOUNDED_ENFORCEMENT_RECONCILED_CLEAN",
            "BLK_SYSTEM_205_BLK_PIPE_BOUNDED_ENFORCEMENT_CONTRACT_READY",
            "BLK_SYSTEM_204_BLK_PIPE_SURFACE_REVIEW_READY",
            "NEXT_FRONTIER_PYTHON_ADAPTER_CLOSED_VALIDATION_PROFILES_SELECTION_NOT_GRANTED",
            "bounded non-authorizing enforcement surface",
            "no broad dispatch",
            "no production-isolation claim",
        ]
        for marker in required:
            self.assertIn(marker, text077)
            self.assertIn(marker, text079)
        self.assertNotIn("NEXT_FRONTIER_BLK_REQ_CLOSED_NEXT_COMPONENT_SELECTION_NOT_GRANTED", text077)
        self.assertNotIn("NEXT_FRONTIER_BLK_REQ_CLOSED_NEXT_COMPONENT_SELECTION_NOT_GRANTED", text079)

    def test_one_closeout_per_sprint_exists_and_contains_boundary_markers(self):
        for sprint in (204, 205, 206):
            path = ROOT / "docs" / "outcomes" / f"BLK-SYSTEM-{sprint}_sprint-closeout.md"
            self.assertTrue(path.exists(), path)
            text = path.read_text()
            self.assertIn("**Status:** Complete", text)
            self.assertIn("bounded non-authorizing enforcement surface", text)
            self.assertIn("No BLK-pipe runtime beyond separately approved exact payloads", text)
            self.assertIn("No new BLK-### root doc was created", text)
