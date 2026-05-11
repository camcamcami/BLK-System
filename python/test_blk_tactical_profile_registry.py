import ast
import unittest
from pathlib import Path

from blk_tactical_profile_registry import (
    DENIED_AUTHORITIES,
    LAYER_B_PRINCIPLE_IDS,
    build_profile_selection_record,
    build_tactical_profile_registry,
    evaluate_profile_selection_record,
    evaluate_tactical_profile_registry,
    validate_profile_selection_record,
    validate_tactical_profile_registry,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "blk_tactical_profile_registry.py"

EXPECTED_LAYER_B_PRINCIPLES = [
    "simple_reviewable_control_flow",
    "bounded_iteration",
    "bounded_runtime_state",
    "explicit_lifecycle_management",
    "small_hostile_reviewable_units",
    "boundary_validation",
    "checked_results_and_postconditions",
    "minimal_mutable_scope",
    "no_dynamic_execution_laundering",
    "flat_validated_data_access",
    "zero_warning_intent_under_repository_owned_profiles",
    "no_authority_laundering",
]

EXPECTED_DENIED_AUTHORITIES = [
    "NO_PROFILE_SELECTION_RUNTIME_AUTHORITY",
    "NO_CEB_CEO_EXECUTION_AUTHORITY",
    "NO_TARGET_REPO_SCAN_AUTHORITY",
    "NO_TARGET_REPO_MUTATION_AUTHORITY",
    "NO_KURONODE_MUTATION_AUTHORITY",
    "NO_LIVE_CODEX_EXECUTION_AUTHORITY",
    "NO_BLK_PIPE_EXECUTION_AUTHORITY",
    "NO_PRODUCTION_BLK_TEST_MCP_AUTHORITY",
    "NO_BEO_PUBLICATION_AUTHORITY",
    "NO_RTM_GENERATION_OR_DRIFT_REJECTION_AUTHORITY",
    "NO_PROTECTED_BLK_REQ_BODY_READS",
    "NO_PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING_AUTHORITY",
    "NO_PRODUCTION_SANDBOX_OR_HOST_ISOLATION_CLAIM",
]


class TacticalProfileRegistryTest(unittest.TestCase):
    def test_registry_extracts_layer_b_and_registers_kuronode_profile(self):
        record = build_tactical_profile_registry()

        self.assertEqual(record["registry_id"], "blk_system_tactical_profile_registry")
        self.assertEqual(record["registry_status"], "TACTICAL_PROFILE_REGISTRY_L0_L1_FIXTURE_ONLY")
        self.assertEqual(record["architecture_anchor"], "BLK-078")
        self.assertEqual(record["layer_b_standard_id"], "blk-system-universal-tactical-output-safety")
        self.assertEqual(LAYER_B_PRINCIPLE_IDS, tuple(EXPECTED_LAYER_B_PRINCIPLES))
        self.assertEqual([principle["id"] for principle in record["layer_b_principles"]], EXPECTED_LAYER_B_PRINCIPLES)

        by_profile = {profile["profile_id"]: profile for profile in record["target_profiles"]}
        self.assertEqual(set(by_profile), {"kuronode-typescript"})
        kuronode = by_profile["kuronode-typescript"]
        self.assertEqual(kuronode["profile_source_doc"], "BLK-058")
        self.assertEqual(kuronode["profile_architecture_doc"], "BLK-078")
        self.assertEqual(kuronode["layer"], "Layer C")
        self.assertEqual(kuronode["profile_maturity"], "L0_LAYER_C_SOURCE_ONLY")
        self.assertIn("simple_reviewable_control_flow", kuronode["layer_b_principles"])
        self.assertIn("electron_ipc_boundary", kuronode["layer_c_overlays"])
        self.assertIn("tree_sitter_sysml_wasm_lifecycle", kuronode["layer_c_overlays"])
        self.assertIn("kuronode-power-of-ten-static", kuronode["validation_profiles"])
        self.assertIn("future approved Kuronode TypeScript work only", kuronode["authority_cutline"])
        self.assertEqual(validate_tactical_profile_registry(record), [])

    def test_selection_record_is_review_only_and_forces_denied_authority_flags_false(self):
        selection = build_profile_selection_record()

        self.assertEqual(selection["selection_status"], "PROFILE_SELECTION_RECORD_REVIEW_ONLY_NOT_RUNTIME_AUTHORITY")
        self.assertEqual(selection["selected_profile_id"], "kuronode-typescript")
        self.assertEqual(selection["selected_profile_source_doc"], "BLK-058")
        self.assertEqual(selection["selection_maturity"], "L0_L1_PLANNING_FIXTURE_ONLY")
        self.assertEqual(selection["denied_authorities"], list(EXPECTED_DENIED_AUTHORITIES))
        for flag in [
            "profile_selection_runtime_authority_granted",
            "target_repo_scan_authorized",
            "target_repo_mutation_authorized",
            "live_codex_execution_authorized",
            "blk_pipe_execution_authorized",
            "production_blk_test_mcp_authorized",
            "beo_publication_authorized",
            "rtm_generation_authorized",
            "protected_body_reads_authorized",
            "package_network_model_browser_cyber_tooling_authorized",
            "production_isolation_claimed",
        ]:
            self.assertIs(selection[flag], False, flag)

        evaluated = evaluate_profile_selection_record(selection)
        self.assertEqual(evaluated["evaluation"], "TACTICAL_PROFILE_SELECTION_READY_FOR_REVIEW_NOT_RUNTIME")
        self.assertEqual(validate_profile_selection_record(evaluated), [])

    def test_denied_authority_sets_are_exact(self):
        self.assertEqual(DENIED_AUTHORITIES, tuple(EXPECTED_DENIED_AUTHORITIES))
        bad_sets = [
            EXPECTED_DENIED_AUTHORITIES[:-1],
            EXPECTED_DENIED_AUTHORITIES + ["APPROVED_FOR_LIVE_EXECUTION"],
            EXPECTED_DENIED_AUTHORITIES + [EXPECTED_DENIED_AUTHORITIES[0]],
            EXPECTED_DENIED_AUTHORITIES[:-1] + [{"bad": True}],
        ]

        for bad_set in bad_sets:
            registry = build_tactical_profile_registry()
            registry["denied_authorities"] = list(bad_set)
            registry["target_profiles"][0]["denied_authorities"] = list(bad_set)
            registry_errors = validate_tactical_profile_registry(registry)
            self.assertTrue(any("denied_authorities" in error for error in registry_errors), (bad_set, registry_errors))

            selection = build_profile_selection_record()
            selection["denied_authorities"] = list(bad_set)
            selection_errors = validate_profile_selection_record(selection)
            self.assertTrue(any("denied_authorities" in error for error in selection_errors), (bad_set, selection_errors))

    def test_authority_laundering_fails_closed_in_allowed_strings_and_nested_fields(self):
        phrases = [
            "not runtime approval; APPROVED_FOR_LIVE_EXECUTION",
            "runtime pilot approved by operator; live pilot allowed",
            "Live target scan authorized.",
            "Kuronode mutation is authorized.",
            "BLK-pipe execution authorized by selected profile.",
            "Production BLK-test MCP is authorized.",
            "authoritativeBEOpublication",
            "RTMGeneration",
            "Protected BLK-req body reads are authorized.",
            "Package manager tooling is authorized.",
            "Production sandbox is enforced.",
        ]
        for phrase in phrases:
            registry = build_tactical_profile_registry()
            registry["target_profiles"][0]["authority_cutline"] = phrase
            registry_errors = validate_tactical_profile_registry(registry)
            self.assertTrue(registry_errors, phrase)
            evaluated_registry = evaluate_tactical_profile_registry(registry)
            self.assertEqual(evaluated_registry["evaluation"], "TACTICAL_PROFILE_REGISTRY_BLOCKED")
            self.assertFalse(evaluated_registry["target_repo_scan_authorized"])
            self.assertFalse(evaluated_registry["target_repo_mutation_authorized"])

            selection = build_profile_selection_record()
            selection["selection_summary"] = phrase
            selection_errors = validate_profile_selection_record(selection)
            self.assertTrue(selection_errors, phrase)
            evaluated_selection = evaluate_profile_selection_record(selection)
            self.assertEqual(evaluated_selection["evaluation"], "TACTICAL_PROFILE_SELECTION_BLOCKED")
            self.assertFalse(evaluated_selection["profile_selection_runtime_authority_granted"])
            self.assertFalse(evaluated_selection["target_repo_scan_authorized"])

    def test_command_shaped_validation_profiles_and_unknown_fields_fail_closed(self):
        bad_profile_names = [
            "npm install",
            "curl https://example.invalid/profile",
            "node -e console.log(1)",
            "python scripts/scan.py",
            "go get example.com/tool",
            "bash -lc scan",
            "http://example.invalid/check",
        ]
        for bad_name in bad_profile_names:
            registry = build_tactical_profile_registry()
            registry["target_profiles"][0]["validation_profiles"].append(bad_name)
            errors = validate_tactical_profile_registry(registry)
            self.assertTrue(any("validation_profiles" in error or "forbidden" in error for error in errors), (bad_name, errors))

        registry = build_tactical_profile_registry()
        registry["target_profiles"][0]["live_scan_authorized"] = True
        registry["target_profiles"][0]["nested"] = {"target_repo_mutation_authorized": True}
        errors = validate_tactical_profile_registry(registry)
        self.assertTrue(any("unsupported key" in error for error in errors), errors)
        self.assertTrue(any("target_repo_mutation_authorized" in error for error in errors), errors)

    def test_module_contains_no_live_surface_imports_or_calls(self):
        tree = ast.parse(MODULE.read_text())
        forbidden_imports = {"subprocess", "socket", "requests", "urllib", "http", "git", "os"}
        forbidden_calls = {"eval", "exec", "__import__", "compile", "open", "system", "popen"}
        offenders = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name.split(".")[0] for alias in node.names]
                offenders.extend(name for name in names if name in forbidden_imports)
            if isinstance(node, ast.ImportFrom):
                names = [alias.name.split(".")[0] for alias in node.names]
                if node.module:
                    names.append(node.module.split(".")[0])
                offenders.extend(name for name in names if name in forbidden_imports)
            if isinstance(node, ast.Call):
                func = node.func
                name = ""
                if isinstance(func, ast.Name):
                    name = func.id
                elif isinstance(func, ast.Attribute):
                    name = func.attr
                if name in forbidden_calls:
                    offenders.append(name)

        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
