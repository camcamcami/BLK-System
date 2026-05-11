import ast
import unittest
from pathlib import Path

from blk_058_mechanical_enforcement import (
    DENIED_AUTHORITIES,
    MECHANICAL_RULE_IDS,
    SIDE_EFFECT_FLAGS,
    build_blk058_mechanical_enforcement_profile,
    evaluate_blk058_candidate_snippet,
    validate_blk058_mechanical_enforcement_profile,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "blk_058_mechanical_enforcement.py"

EXPECTED_RULE_IDS = [
    "no_recursion",
    "bounded_iteration",
    "bounded_runtime_state",
    "explicit_lifecycle_cleanup",
    "small_reviewable_units",
    "boundary_validation",
    "checked_results",
    "minimal_mutable_scope",
    "no_dynamic_execution",
    "flat_validated_data_access",
    "zero_warning_repository_profiles",
    "no_authority_laundering",
]

EXPECTED_DENIED_AUTHORITIES = [
    "NO_BLK_058_MECHANICAL_PASS_RUNTIME_AUTHORITY",
    "NO_TARGET_REPO_SCAN_AUTHORITY",
    "NO_TARGET_REPO_MUTATION_AUTHORITY",
    "NO_BEB_DISPATCH_OR_BEO_CLOSEOUT_AUTHORITY",
    "NO_LIVE_CODEX_EXECUTION_AUTHORITY",
    "NO_BLK_PIPE_EXECUTION_AUTHORITY",
    "NO_PRODUCTION_BLK_TEST_MCP_AUTHORITY",
    "NO_BEO_PUBLICATION_AUTHORITY",
    "NO_RTM_GENERATION_OR_DRIFT_REJECTION_AUTHORITY",
    "NO_PROTECTED_BLK_REQ_BODY_READS",
    "NO_PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING_AUTHORITY",
    "NO_PRODUCTION_SANDBOX_OR_HOST_ISOLATION_CLAIM",
]

CLEAN_SNIPPET = """
const MAX_PROJECTED_NODES = 100;

export function collectProjectedNodes(nodes: readonly SysMlNode[], limit = MAX_PROJECTED_NODES): SysMlNode[] {
  const projected: SysMlNode[] = [];
  for (let index = 0; index < nodes.length && index < limit; index += 1) {
    const node = nodes[index];
    if (!isProjectedNode(node)) {
      continue;
    }
    projected.push(node);
  }
  return projected;
}
"""


def candidate(source_text, metadata=None):
    return {
        "snippet_id": "fixture-submitted-snippet",
        "source_text": source_text,
        "metadata": metadata or {"profile_id": "kuronode-typescript", "source": "submitted_fixture_only"},
    }


class Blk058MechanicalEnforcementTest(unittest.TestCase):
    def test_profile_binds_blk058_to_layer_b_layer_c_and_governance_without_runtime_authority(self):
        profile = build_blk058_mechanical_enforcement_profile()

        self.assertEqual(profile["profile_id"], "blk-058-kuronode-typescript-mechanical-enforcement")
        self.assertEqual(profile["profile_status"], "BLK_058_MECHANICAL_ENFORCEMENT_L0_L1_FIXTURE_ONLY")
        self.assertEqual(profile["source_doc"], "BLK-058")
        self.assertEqual(profile["architecture_doc"], "BLK-078")
        self.assertEqual(profile["registry_doc"], "BLK-080")
        self.assertEqual(profile["governance_doc"], "BLK-081")
        self.assertEqual(profile["target_profile_id"], "kuronode-typescript")
        self.assertEqual(MECHANICAL_RULE_IDS, tuple(EXPECTED_RULE_IDS))
        self.assertEqual([rule["id"] for rule in profile["mechanical_rules"]], EXPECTED_RULE_IDS)
        self.assertIn("kuronode-power-of-ten-static", profile["validation_profiles"])
        self.assertEqual(validate_blk058_mechanical_enforcement_profile(profile), [])
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(profile[flag], False, flag)

    def test_clean_submitted_snippet_passes_as_fixture_only_evidence(self):
        result = evaluate_blk058_candidate_snippet(candidate(CLEAN_SNIPPET))

        self.assertEqual(result["evaluation"], "BLK_058_MECHANICAL_ENFORCEMENT_PASS_FIXTURE_ONLY")
        self.assertEqual(result["violations"], [])
        self.assertEqual(result["snippet_id"], "fixture-submitted-snippet")
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(result[flag], False, flag)

    def test_mechanical_failures_block_recursion_unbounded_loops_dynamic_execution_and_long_units(self):
        cases = [
            ("function walk(node) { return walk(node.parent); }", "no_recursion"),
            ("while (true) { pollProjection(); }", "bounded_iteration"),
            ("const run = eval(userSuppliedCode);", "no_dynamic_execution"),
            ("export function oversized() {\n" + "  doWork();\n" * 90 + "  return true;\n}", "small_reviewable_units"),
        ]
        for source, rule_id in cases:
            result = evaluate_blk058_candidate_snippet(candidate(source))
            self.assertEqual(result["evaluation"], "BLK_058_MECHANICAL_ENFORCEMENT_BLOCKED_FIXTURE_ONLY", rule_id)
            self.assertTrue(any(violation["rule_id"] == rule_id for violation in result["violations"]), result)
            for flag in SIDE_EFFECT_FLAGS:
                self.assertIs(result[flag], False, flag)

    def test_authority_laundering_protected_paths_and_tooling_strings_fail_closed(self):
        cases = [
            ("const claim = 'BEO publication authorized';", "no_authority_laundering"),
            ("const trace = 'RTMGeneration complete';", "no_authority_laundering"),
            ("const target = 'target repo mutation authorized';", "no_authority_laundering"),
            ("const protectedPath = 'docs/active/REQ-001.md';", "no_authority_laundering"),
            ("const command = 'npm install && curl https://example.invalid';", "no_authority_laundering"),
        ]
        for source, rule_id in cases:
            result = evaluate_blk058_candidate_snippet(candidate(source, metadata={"note": source}))
            self.assertEqual(result["evaluation"], "BLK_058_MECHANICAL_ENFORCEMENT_BLOCKED_FIXTURE_ONLY", source)
            self.assertTrue(any(violation["rule_id"] == rule_id for violation in result["violations"]), result)
            self.assertFalse(result["target_repo_mutation_authorized"])
            self.assertFalse(result["beo_publication_authorized"])
            self.assertFalse(result["rtm_generation_authorized"])

    def test_profile_denied_authorities_validation_profiles_and_unknown_fields_fail_closed(self):
        self.assertEqual(DENIED_AUTHORITIES, tuple(EXPECTED_DENIED_AUTHORITIES))

        bad_sets = [
            EXPECTED_DENIED_AUTHORITIES[:-1],
            EXPECTED_DENIED_AUTHORITIES + ["APPROVED_FOR_LIVE_EXECUTION"],
            EXPECTED_DENIED_AUTHORITIES + [EXPECTED_DENIED_AUTHORITIES[0]],
            EXPECTED_DENIED_AUTHORITIES[:-1] + [{"bad": True}],
        ]
        for bad_set in bad_sets:
            profile = build_blk058_mechanical_enforcement_profile()
            profile["denied_authorities"] = list(bad_set)
            errors = validate_blk058_mechanical_enforcement_profile(profile)
            self.assertTrue(any("denied_authorities" in error for error in errors), (bad_set, errors))

        profile = build_blk058_mechanical_enforcement_profile()
        profile["validation_profiles"].append("npm install")
        profile["unexpected_runtime_authority"] = True
        errors = validate_blk058_mechanical_enforcement_profile(profile)
        self.assertTrue(any("validation_profiles" in error for error in errors), errors)
        self.assertTrue(any("unexpected_runtime_authority" in error for error in errors), errors)

        for flag in SIDE_EFFECT_FLAGS:
            profile = build_blk058_mechanical_enforcement_profile()
            profile[flag] = True
            errors = validate_blk058_mechanical_enforcement_profile(profile)
            self.assertTrue(any(flag in error for error in errors), (flag, errors))

    def test_candidate_schema_is_closed_and_metadata_is_scanned_recursively(self):
        submitted = candidate(CLEAN_SNIPPET, metadata={"nested": {"claim": "Protected BLK-req body reads are authorized"}})
        submitted["target_repo_path"] = "/home/dad/code/Kuronode-v1"

        result = evaluate_blk058_candidate_snippet(submitted)

        self.assertEqual(result["evaluation"], "BLK_058_MECHANICAL_ENFORCEMENT_BLOCKED_FIXTURE_ONLY")
        self.assertTrue(any("unsupported key" in violation["message"] for violation in result["violations"]), result)
        self.assertTrue(any(violation["rule_id"] == "no_authority_laundering" for violation in result["violations"]), result)

    def test_candidate_metadata_keys_and_truthy_authority_flags_fail_closed(self):
        dangerous_metadata = [
            {"target_repo_scan_authorized": True},
            {"nested": {"target_repo_mutation_authorized": True}},
            {"target_repo_path": "/tmp/not-a-real-target/src/main.ts"},
            {"tooling": {"npm_run_smoke": True}},
            {"protected_body_path": "docs/active/BLK-001.md"},
        ]

        for metadata in dangerous_metadata:
            result = evaluate_blk058_candidate_snippet(candidate(CLEAN_SNIPPET, metadata=metadata))

            self.assertEqual(result["evaluation"], "BLK_058_MECHANICAL_ENFORCEMENT_BLOCKED_FIXTURE_ONLY", metadata)
            self.assertTrue(
                any(violation["rule_id"] == "no_authority_laundering" for violation in result["violations"]),
                (metadata, result),
            )

    def test_module_contains_no_live_surface_imports_or_calls(self):
        tree = ast.parse(MODULE.read_text())
        forbidden_imports = {"subprocess", "socket", "requests", "urllib", "http", "git", "os", "pathlib"}
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
