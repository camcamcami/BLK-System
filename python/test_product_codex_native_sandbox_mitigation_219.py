import ast
import copy
import unittest
from pathlib import Path

from product_codex_native_sandbox_mitigation_219 import (
    DEFAULT_219_PACKAGE_HASH,
    DENIED_AUTHORITIES,
    NEXT_FRONTIER_219,
    REQUIRED_FALSE_SIDE_EFFECT_FLAGS,
    UPSTREAM_BLK218_PACKAGE_HASH,
    build_219_native_sandbox_mitigation_package,
    canonical_package_hash,
    validate_219_native_sandbox_mitigation_package,
)

ROOT = Path(__file__).resolve().parents[1]
BLK077 = ROOT / "docs" / "BLK-077_blk-system-post-078-roadmap.md"
BLK079 = ROOT / "docs" / "BLK-079_post-078-current-state-authority-index.md"
MODULE = ROOT / "python" / "product_codex_native_sandbox_mitigation_219.py"


class ProductCodexNativeSandboxMitigation219Test(unittest.TestCase):
    def test_219_records_reproduced_native_sandbox_failure_and_mitigation(self):
        package = build_219_native_sandbox_mitigation_package()

        self.assertEqual(package["sprint_id"], "BLK-SYSTEM-219")
        self.assertEqual(package["status"], "NATIVE_CODEX_SANDBOX_MITIGATION_RECORDED")
        self.assertEqual(package["upstream_218_package_hash"], UPSTREAM_BLK218_PACKAGE_HASH)
        self.assertEqual(package["package_hash"], DEFAULT_219_PACKAGE_HASH)
        self.assertEqual(validate_219_native_sandbox_mitigation_package(package), [])

        probes = package["host_probe_evidence"]
        self.assertEqual(probes["codex_cli_version"], "codex-cli 0.130.0")
        self.assertEqual(probes["bubblewrap_version"], "bubblewrap 0.9.0")
        self.assertEqual(probes["kernel_unprivileged_userns_clone"], "1")
        self.assertEqual(probes["apparmor_restrict_unprivileged_userns"], "1")
        self.assertIn("write failed /proc/self/uid_map: Operation not permitted", probes["unshare_user_result"])
        self.assertIn("bwrap: setting up uid map: Permission denied", probes["bwrap_userns_result"])
        self.assertIn("bwrap: loopback: Failed RTM_NEWADDR", probes["bwrap_network_result"])
        self.assertIn("bwrap: loopback: Failed RTM_NEWADDR", probes["codex_sandbox_result"])

        mitigation = package["mitigation_decision"]
        self.assertEqual(mitigation["native_sandbox_state"], "HOST_BLOCKED_FAIL_CLOSED")
        self.assertEqual(mitigation["active_codex_mode"], "EXTERNAL_CONTAINMENT_REQUIRED")
        self.assertTrue(mitigation["host_admin_repair_required_before_native_workspace_write"])
        self.assertFalse(package["native_sandbox_enforced"])
        self.assertFalse(package["host_configuration_mutated"])
        self.assertFalse(package["production_isolation_claimed"])

    def test_219_preserves_denied_authorities_and_rejects_laundering(self):
        package = build_219_native_sandbox_mitigation_package()
        self.assertEqual(package["denied_authorities"], list(DENIED_AUTHORITIES))
        self.assertEqual(len(package["denied_authorities"]), len(set(package["denied_authorities"])))
        for flag in REQUIRED_FALSE_SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)

        hostile_values = [
            {"operator_notes": ["Native sandbox is enforced, production isolation claim approved"]},
            {"operator_notes": ["live Codex execution authorized after this mitigation"]},
            {"caller_supplied_evidence_refs": {"body": "docs%252Frequirements protected body The system shall"}},
            {"caller_supplied_evidence_refs": {"tooling": "npm install and curl https://example.invalid now allowed"}},
            {"caller_supplied_evidence_refs": {"publication": "BEO publication authorized by sandbox PASS"}},
        ]
        for overrides in hostile_values:
            with self.subTest(overrides=overrides):
                candidate = copy.deepcopy(package)
                candidate.update(overrides)
                candidate["package_hash"] = canonical_package_hash(candidate)
                errors = validate_219_native_sandbox_mitigation_package(candidate)
                self.assertTrue(errors, overrides)
                self.assertTrue(
                    any("authority" in error.lower() or "protected" in error.lower() or "tool" in error.lower() or "sandbox" in error.lower() for error in errors),
                    errors,
                )

    def test_219_rejects_rehashed_upstream_and_sandbox_overclaims(self):
        package = build_219_native_sandbox_mitigation_package()

        forged = copy.deepcopy(package)
        forged["upstream_218_package_hash"] = "sha256:" + "0" * 64
        forged["package_hash"] = canonical_package_hash(forged)
        self.assertTrue(any("upstream_218" in error for error in validate_219_native_sandbox_mitigation_package(forged)))

        overclaim = copy.deepcopy(package)
        overclaim["native_sandbox_enforced"] = True
        overclaim["mitigation_decision"]["native_sandbox_state"] = "READY"
        overclaim["package_hash"] = canonical_package_hash(overclaim)
        errors = validate_219_native_sandbox_mitigation_package(overclaim)
        self.assertTrue(any("native_sandbox" in error for error in errors), errors)

        mutated_host = copy.deepcopy(package)
        mutated_host["host_configuration_mutated"] = True
        mutated_host["package_hash"] = canonical_package_hash(mutated_host)
        self.assertTrue(any("host_configuration_mutated" in error for error in validate_219_native_sandbox_mitigation_package(mutated_host)))

    def test_219_active_docs_record_mitigation_without_granting_runtime(self):
        combined = BLK077.read_text() + "\n" + BLK079.read_text()
        for marker in [
            "BLK_SYSTEM_219_NATIVE_CODEX_SANDBOX_MITIGATION_RECORDED",
            "blk219_native_codex_sandbox_mitigation_hash=",
            "BLK_SYSTEM_220_NATIVE_CODEX_SANDBOX_REPAIR_RECHECK_RECORDED",
            "workspace-write smoke passed only under runtime host-admin AppArmor userns relaxation",
            "no reusable Codex dispatch",
            "no production-isolation claim",
        ]:
            self.assertIn(marker, combined)
        self.assertNotIn("NEXT_FRONTIER_OPERATOR_SELECTED_BOUNDED_KURONODE_FEATURE_OR_OBSERVED_FAILURE_HARDENING_NOT_GRANTED", combined)

    def test_module_does_not_import_live_execution_or_network_surfaces(self):
        tree = ast.parse(MODULE.read_text())
        forbidden_imports = {"subprocess", "socket", "requests", "urllib", "http", "ftplib", "git"}
        forbidden_calls = {"system", "popen", "run", "Popen", "call", "check_call", "check_output", "exec", "eval", "open"}
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
