import ast
import copy
import re
import tomllib
import unittest
from pathlib import Path

from product_codex_config_containment_216 import (
    BLK121_DOC_PATH,
    CODEX_CONFIG_DOC_ID,
    DEFAULT_216_PACKAGE_HASH,
    DENIED_AUTHORITIES,
    NEXT_FRONTIER_216,
    REQUIRED_FALSE_SIDE_EFFECT_FLAGS,
    UPSTREAM_BLK215_PACKAGE_HASH,
    build_216_codex_config_containment_package,
    canonical_package_hash,
    validate_216_codex_config_containment_package,
)

ROOT = Path(__file__).resolve().parents[1]
BLK077 = ROOT / "docs" / "BLK-077_blk-system-post-078-roadmap.md"
BLK079 = ROOT / "docs" / "BLK-079_post-078-current-state-authority-index.md"
MODULE = ROOT / "python" / "product_codex_config_containment_216.py"


class ProductCodexConfigContainment216Test(unittest.TestCase):
    def test_216_records_codex_permission_profile_containment_drill(self):
        package = build_216_codex_config_containment_package()

        self.assertEqual(package["sprint_id"], "BLK-SYSTEM-216")
        self.assertEqual(package["status"], "CODEX_PERMISSION_PROFILE_CONTAINMENT_DRILL_RECORDED")
        self.assertEqual(package["upstream_215_package_hash"], UPSTREAM_BLK215_PACKAGE_HASH)
        self.assertEqual(package["codex_configuration_doc"], CODEX_CONFIG_DOC_ID)
        self.assertEqual(package["codex_configuration_doc_path"], BLK121_DOC_PATH)
        self.assertEqual(package["package_hash"], DEFAULT_216_PACKAGE_HASH)
        self.assertEqual(validate_216_codex_config_containment_package(package), [])

    def test_216_permission_profile_uses_modern_profile_not_legacy_exec_flags(self):
        package = build_216_codex_config_containment_package()
        invocation = package["recommended_codex_invocation"]
        profile = package["permission_profile_contract"]
        joined_args = " ".join(invocation["required_args"] + invocation["forbidden_legacy_args"])

        for required in ["--ephemeral", "--ignore-user-config", "--ignore-rules", "--json", "--output-last-message"]:
            self.assertIn(required, invocation["required_args"])
        for feature in ["hooks", "plugins", "goals"]:
            self.assertIn(feature, invocation["disabled_ambient_features"])
        for legacy in ["--isolated", "--yes", "--dry-run", "--deny-read"]:
            self.assertIn(legacy, invocation["forbidden_legacy_args"])
            self.assertNotIn(legacy, invocation["required_args"])
        self.assertNotIn("--deny-read=", joined_args.replace("--deny-read", ""))
        self.assertEqual(profile["default_permissions"], "blk-kuronode-codex-feature")
        self.assertEqual(profile["filesystem"][":project_roots"]["."], "read")
        self.assertEqual(profile["filesystem"][":project_roots"]["**/.env*"], "none")
        self.assertEqual(profile["filesystem"][":project_roots"]["docs/requirements/**"], "none")
        self.assertEqual(profile["filesystem"][":project_roots"]["docs/use_cases/**"], "none")
        self.assertEqual(profile["filesystem"][":project_roots"]["**/node_modules/**"], "none")
        self.assertFalse(profile["network"]["enabled"])
        self.assertEqual(profile["glob_scan_max_depth"], 4)

    def test_216_host_sandbox_result_fails_closed_to_external_container_fallback(self):
        package = build_216_codex_config_containment_package()
        host = package["host_sandbox_smoke_result"]

        self.assertEqual(host["codex_cli_version"], "codex-cli 0.130.0")
        self.assertEqual(host["native_sandbox_status"], "HOST_NATIVE_CODEX_SANDBOX_UNAVAILABLE_BWRAP_RTM_NEWADDR")
        self.assertIn("bwrap: loopback: Failed RTM_NEWADDR", host["observed_failure"])
        self.assertTrue(host["permission_profile_requires_direct_runtime_enforcement"])
        self.assertTrue(host["legacy_landlock_incompatible"])
        self.assertEqual(host["required_fallback"], "DEVCONTAINER_OR_EXTERNAL_SANDBOX_FOR_DANGER_FULL_ACCESS")
        self.assertFalse(package["native_sandbox_enforced"])
        self.assertFalse(package["production_isolation_claimed"])

    def test_216_preserves_all_denied_authorities_and_rejects_laundering(self):
        package = build_216_codex_config_containment_package()
        self.assertEqual(package["denied_authorities"], list(DENIED_AUTHORITIES))
        self.assertEqual(len(package["denied_authorities"]), len(set(package["denied_authorities"])))
        for flag in REQUIRED_FALSE_SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)

        hostile_values = [
            {"operator_notes": ["Codex approval grants live Codex execution authorized forever"]},
            {"operator_notes": ["permission profile proves production sandbox enforced"]},
            {"caller_supplied_evidence_refs": {"protected": "docs%252Frequirements protected body: The system shall..."}},
            {"caller_supplied_evidence_refs": {"network": "network access true and curl https://example.invalid"}},
            {"caller_supplied_evidence_refs": {"package": "npm install && pip install evil"}},
            {"caller_supplied_evidence_refs": {"beo": "BEO publication greenlit"}},
        ]
        for overrides in hostile_values:
            with self.subTest(overrides=overrides):
                candidate = copy.deepcopy(package)
                candidate.update(overrides)
                candidate["package_hash"] = canonical_package_hash(candidate)
                errors = validate_216_codex_config_containment_package(candidate)
                self.assertTrue(errors, overrides)
                self.assertTrue(
                    any("authority" in error.lower() or "protected" in error.lower() or "tool" in error.lower() for error in errors),
                    errors,
                )

    def test_216_rejects_rehashed_scope_and_sandbox_overclaims(self):
        package = build_216_codex_config_containment_package()

        forged = copy.deepcopy(package)
        forged["upstream_215_package_hash"] = "sha256:" + "0" * 64
        forged["package_hash"] = canonical_package_hash(forged)
        self.assertTrue(any("upstream_215" in error for error in validate_216_codex_config_containment_package(forged)))

        overclaim = copy.deepcopy(package)
        overclaim["native_sandbox_enforced"] = True
        overclaim["package_hash"] = canonical_package_hash(overclaim)
        self.assertTrue(any("native_sandbox_enforced" in error for error in validate_216_codex_config_containment_package(overclaim)))

        weakened = copy.deepcopy(package)
        weakened["permission_profile_contract"]["filesystem"][":project_roots"].pop("**/.env*")
        weakened["package_hash"] = canonical_package_hash(weakened)
        self.assertTrue(any("permission_profile" in error for error in validate_216_codex_config_containment_package(weakened)))

    def test_blk121_codex_configuration_doc_exists_and_pins_current_contract(self):
        path = ROOT / BLK121_DOC_PATH
        text = path.read_text()

        required = [
            "# BLK-121 — Codex Configuration and Containment Contract",
            "CODEX_CONFIGURATION_AND_CONTAINMENT_CONTRACT_ACTIVE",
            "SANDBOX_MODE_AND_APPROVAL_POLICY_ARE_SEPARATE_CONTROLS",
            "PERMISSION_PROFILES_USE_NONE_FOR_DENY_READ",
            "HOST_NATIVE_CODEX_SANDBOX_UNAVAILABLE_BWRAP_RTM_NEWADDR",
            "DEVCONTAINER_OR_EXTERNAL_SANDBOX_FOR_DANGER_FULL_ACCESS",
            "NO_LIVE_CODEX_DISPATCH_AUTHORITY",
            "NO_PRODUCTION_ISOLATION_CLAIM",
            "--ephemeral --ignore-user-config --ignore-rules --json",
            "Do not use legacy `--deny-read`, `--isolated`, `--yes`, or `--dry-run` flags",
        ]
        for marker in required:
            self.assertIn(marker, text)
        self.assertEqual(text.count("```") % 2, 0)

        toml_blocks = re.findall(r"```toml\n(.*?)\n```", text, flags=re.DOTALL)
        self.assertEqual(len(toml_blocks), 1)
        parsed = tomllib.loads(toml_blocks[0])
        profile = parsed["permissions"]["blk-kuronode-codex-feature"]
        self.assertEqual(profile["filesystem"]["glob_scan_max_depth"], 4)
        self.assertEqual(profile["filesystem"][":project_roots"]["."], "read")
        self.assertEqual(profile["filesystem"][":project_roots"]["**/.env*"], "none")
        self.assertEqual(profile["network"]["enabled"], False)

    def test_active_docs_record_216_without_granting_runtime(self):
        combined = BLK077.read_text() + "\n" + BLK079.read_text()
        for marker in [
            "BLK_SYSTEM_216_CODEX_PERMISSION_PROFILE_CONTAINMENT_DRILL_RECORDED",
            "blk216_codex_config_containment_package_hash=",
            "NEXT_FRONTIER_THIRD_BOUNDED_KURONODE_FEATURE_LOOP_AVAILABLE_AFTER_UNDO_CHECK_NOT_GRANTED",
            "BLK-121",
            "no reusable Codex dispatch",
            "no production-isolation claim",
        ]:
            self.assertIn(marker, combined)
        self.assertNotIn("NEXT_FRONTIER_THIRD_BOUNDED_KURONODE_FEATURE_LOOP_OR_OPERATOR_SELECTED_UNDO_NOT_GRANTED", combined)

    def test_module_does_not_import_live_execution_or_network_surfaces(self):
        source_path = MODULE
        tree = ast.parse(source_path.read_text())
        forbidden_imports = {"subprocess", "socket", "requests", "urllib", "http", "ftplib"}
        forbidden_calls = {"system", "popen", "run", "Popen", "call", "check_call", "check_output", "exec", "eval"}
        found = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] in forbidden_imports:
                        found.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = (node.module or "").split(".")[0]
                if module in forbidden_imports:
                    found.append(node.module)
            elif isinstance(node, ast.Call):
                func = node.func
                name = ""
                if isinstance(func, ast.Name):
                    name = func.id
                elif isinstance(func, ast.Attribute):
                    name = func.attr
                if name in forbidden_calls:
                    found.append(name)
        self.assertEqual(found, [])


if __name__ == "__main__":
    unittest.main()
