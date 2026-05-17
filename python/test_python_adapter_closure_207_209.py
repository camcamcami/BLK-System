import copy
import unittest

from python_adapter_closure_207_209 import (
    DEFAULT_207_PACKAGE_HASH,
    DEFAULT_208_PACKAGE_HASH,
    DEFAULT_209_PACKAGE_HASH,
    DENIED_AUTHORITIES,
    NEXT_FRONTIER,
    REQUIRED_FALSE_SIDE_EFFECT_FLAGS,
    build_207_adapter_surface_review_package,
    build_208_adapter_contract_package,
    build_209_adapter_reconciliation_package,
    build_python_adapter_closure_packages,
    canonical_package_hash,
    validate_207_adapter_surface_review_package,
    validate_208_adapter_contract_package,
    validate_209_adapter_reconciliation_package,
)


class PythonAdapterClosure207209Test(unittest.TestCase):
    def test_closure_ladder_builds_three_hash_bound_non_authorizing_packages(self):
        review, contract, reconciliation = build_python_adapter_closure_packages()

        self.assertEqual(review["sprint_id"], "BLK-SYSTEM-207")
        self.assertEqual(review["status"], "PYTHON_ADAPTER_SURFACE_REVIEW_READY_NOT_AUTHORITY")
        self.assertEqual(review["package_hash"], DEFAULT_207_PACKAGE_HASH)
        self.assertEqual(validate_207_adapter_surface_review_package(review), [])
        self.assertIn("python/blk_pipe_adapter.py", review["reviewed_surface_files"])
        self.assertIn("payload_packaging", review["bounded_adapter_surfaces"])

        self.assertEqual(contract["sprint_id"], "BLK-SYSTEM-208")
        self.assertEqual(contract["status"], "PYTHON_ADAPTER_CONTRACT_READY_NOT_DISPATCH_AUTHORITY")
        self.assertEqual(contract["upstream_207_package_hash"], DEFAULT_207_PACKAGE_HASH)
        self.assertEqual(contract["package_hash"], DEFAULT_208_PACKAGE_HASH)
        self.assertEqual(validate_208_adapter_contract_package(contract), [])
        self.assertEqual(contract["authority_grant_fields"], [])
        self.assertEqual(contract["adapter_contract"]["blk_pipe_invocation"], "requires_separate_exact_payload_authority")

        self.assertEqual(reconciliation["sprint_id"], "BLK-SYSTEM-209")
        self.assertEqual(reconciliation["status"], "PYTHON_ADAPTER_RECONCILED_CLEAN")
        self.assertEqual(reconciliation["upstream_207_package_hash"], DEFAULT_207_PACKAGE_HASH)
        self.assertEqual(reconciliation["upstream_208_package_hash"], DEFAULT_208_PACKAGE_HASH)
        self.assertEqual(reconciliation["next_frontier"], NEXT_FRONTIER)
        self.assertEqual(reconciliation["package_hash"], DEFAULT_209_PACKAGE_HASH)
        self.assertEqual(validate_209_adapter_reconciliation_package(reconciliation), [])

    def test_every_package_preserves_exact_denied_authority_set_and_false_flags(self):
        packages = build_python_adapter_closure_packages()
        for package in packages:
            with self.subTest(sprint_id=package["sprint_id"]):
                self.assertEqual(package["denied_authorities"], list(DENIED_AUTHORITIES))
                self.assertEqual(len(package["denied_authorities"]), len(set(package["denied_authorities"])))
                for flag in REQUIRED_FALSE_SIDE_EFFECT_FLAGS:
                    self.assertIs(package[flag], False, flag)

        review = build_207_adapter_surface_review_package()
        missing = copy.deepcopy(review)
        missing["denied_authorities"] = missing["denied_authorities"][:-1]
        missing["package_hash"] = canonical_package_hash(missing)
        self.assertTrue(any("denied_authorities" in error for error in validate_207_adapter_surface_review_package(missing)))

        duplicate = copy.deepcopy(review)
        duplicate["denied_authorities"] = list(DENIED_AUTHORITIES) + [DENIED_AUTHORITIES[0]]
        duplicate["package_hash"] = canonical_package_hash(duplicate)
        self.assertTrue(any("denied_authorities" in error for error in validate_207_adapter_surface_review_package(duplicate)))

        positive_flag = copy.deepcopy(review)
        positive_flag["blk_pipe_dispatch_authorized"] = True
        positive_flag["package_hash"] = canonical_package_hash(positive_flag)
        self.assertTrue(any("blk_pipe_dispatch_authorized" in error for error in validate_207_adapter_surface_review_package(positive_flag)))

    def test_downstream_packages_reject_self_consistent_rehashed_upstream_forgery(self):
        review = build_207_adapter_surface_review_package()
        forged_review = copy.deepcopy(review)
        forged_review["review_findings"].append("CodexApproval inherited from BLK-pipe SUCCESS")
        forged_review["package_hash"] = canonical_package_hash(forged_review)
        self.assertNotEqual(forged_review["package_hash"], DEFAULT_207_PACKAGE_HASH)
        self.assertTrue(validate_207_adapter_surface_review_package(forged_review))
        with self.assertRaisesRegex(ValueError, "exact canonical BLK-SYSTEM-207"):
            build_208_adapter_contract_package(forged_review)

        contract = build_208_adapter_contract_package(review)
        forged_contract = copy.deepcopy(contract)
        forged_contract["adapter_contract"]["blk_pipe_invocation"] = "dispatch_authorized_by_adapter"
        forged_contract["package_hash"] = canonical_package_hash(forged_contract)
        self.assertNotEqual(forged_contract["package_hash"], DEFAULT_208_PACKAGE_HASH)
        self.assertTrue(validate_208_adapter_contract_package(forged_contract))
        with self.assertRaisesRegex(ValueError, "exact canonical 207 and 208"):
            build_209_adapter_reconciliation_package(review, forged_contract)

    def test_caller_controlled_notes_and_refs_reject_authority_and_protected_body_laundering(self):
        review = build_207_adapter_surface_review_package()
        hostile_values = [
            {"operator_notes": ["blkPipeDispatchAuthorized by PASS"]},
            {"operator_notes": ["runtime approval inherited; live Codex execution allowed"]},
            {"operator_notes": ["production isolation is enforced by this adapter"]},
            {"caller_supplied_evidence_refs": {"docs%252Factive": "REQ body text: The system shall..."}},
            {"caller_supplied_evidence_refs": {"docs%252Fuse_cases": "UC body text: The actor shall..."}},
            {"caller_supplied_evidence_refs": {"nested": ["codexApproval", "BLKTestPassApproval"]}},
            {"caller_supplied_evidence_refs": {"secret": "Authorization=Basic abcdef"}},
        ]
        for overrides in hostile_values:
            with self.subTest(overrides=overrides):
                candidate = copy.deepcopy(review)
                candidate.update(overrides)
                candidate["package_hash"] = canonical_package_hash(candidate)
                errors = validate_207_adapter_surface_review_package(candidate)
                self.assertTrue(errors, overrides)
                self.assertTrue(
                    any("authority" in error.lower() or "protected" in error.lower() or "secret" in error.lower() for error in errors),
                    errors,
                )

    def test_adapter_contract_rejects_extra_authority_fields_and_mutated_contract_meaning(self):
        review = build_207_adapter_surface_review_package()
        contract = build_208_adapter_contract_package(review)

        extra = copy.deepcopy(contract)
        extra["dispatch_authority"] = "approved"
        extra["package_hash"] = canonical_package_hash(extra)
        self.assertTrue(any("keys must be exact" in error for error in validate_208_adapter_contract_package(extra)))

        mutated_contract = copy.deepcopy(contract)
        mutated_contract["adapter_contract"]["validation_result_meaning"] = "PASS grants runtime authority"
        mutated_contract["package_hash"] = canonical_package_hash(mutated_contract)
        errors = validate_208_adapter_contract_package(mutated_contract)
        self.assertTrue(errors)
        self.assertTrue(any("adapter_contract" in error or "authority" in error.lower() for error in errors), errors)

    def test_reconciliation_selects_validation_profiles_without_granting_that_surface(self):
        review, contract, reconciliation = build_python_adapter_closure_packages()

        self.assertEqual(reconciliation["next_frontier"], "NEXT_FRONTIER_PYTHON_ADAPTER_CLOSED_VALIDATION_PROFILES_SELECTION_NOT_GRANTED")
        self.assertIn("BLK_SYSTEM_207_PYTHON_ADAPTER_SURFACE_REVIEW_READY", reconciliation["reconciliation_findings"])
        self.assertIn("BLK_SYSTEM_208_PYTHON_ADAPTER_CONTRACT_READY", reconciliation["reconciliation_findings"])
        self.assertIn("validation profiles remain the next selected surface, not granted authority", reconciliation["reconciliation_findings"])
        self.assertFalse(reconciliation["blk_pipe_dispatch_authorized"])
        self.assertFalse(reconciliation["runtime_tooling_authorized"])
        self.assertFalse(reconciliation["target_source_git_mutation_authorized"])


if __name__ == "__main__":
    unittest.main()
