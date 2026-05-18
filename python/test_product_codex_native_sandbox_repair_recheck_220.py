import ast
import copy
import unittest
from pathlib import Path

from product_codex_native_sandbox_repair_recheck_220 import (
    DEFAULT_220_PACKAGE_HASH,
    DENIED_AUTHORITIES,
    NEXT_FRONTIER_220,
    REQUIRED_FALSE_SIDE_EFFECT_FLAGS,
    UPSTREAM_BLK219_PACKAGE_HASH,
    build_220_native_sandbox_repair_recheck_package,
    canonical_package_hash,
    validate_220_native_sandbox_repair_recheck_package,
)

ROOT = Path(__file__).resolve().parents[1]
BLK077 = ROOT / "docs" / "BLK-077_blk-system-post-078-roadmap.md"
BLK079 = ROOT / "docs" / "BLK-079_post-078-current-state-authority-index.md"
MODULE = ROOT / "python" / "product_codex_native_sandbox_repair_recheck_220.py"


class ProductCodexNativeSandboxRepairRecheck220Test(unittest.TestCase):
    def test_220_records_admin_repair_recheck_without_overclaiming_persistence(self):
        package = build_220_native_sandbox_repair_recheck_package()

        self.assertEqual(package["sprint_id"], "BLK-SYSTEM-220")
        self.assertEqual(package["status"], "NATIVE_CODEX_SANDBOX_REPAIR_RECHECK_RECORDED")
        self.assertEqual(package["upstream_219_package_hash"], UPSTREAM_BLK219_PACKAGE_HASH)
        self.assertEqual(package["package_hash"], DEFAULT_220_PACKAGE_HASH)
        self.assertEqual(validate_220_native_sandbox_repair_recheck_package(package), [])

        pre = package["pre_repair_evidence"]
        self.assertEqual(pre["newuidmap"], "missing")
        self.assertEqual(pre["apparmor_restrict_unprivileged_userns"], "1")
        self.assertIn("uid_map: Operation not permitted", pre["unshare_result"])
        self.assertIn("Failed RTM_NEWADDR", pre["codex_sandbox_result"])

        repair = package["host_admin_repair_evidence"]
        self.assertEqual(repair["uidmap_installed"], True)
        self.assertEqual(repair["newuidmap_mode"], "4755 root:root")
        self.assertEqual(repair["runtime_apparmor_restrict_unprivileged_userns"], "0")
        self.assertEqual(repair["persisted_sysctl_change"], False)
        self.assertEqual(repair["restored_apparmor_restrict_unprivileged_userns_after_test"], "1")

        smoke = package["passing_smoke_evidence"]
        self.assertEqual(smoke["unshare_map_current_rc"], 0)
        self.assertEqual(smoke["bwrap_full_rc"], 0)
        self.assertEqual(smoke["codex_exec_workspace_write_rc"], 0)
        self.assertEqual(smoke["codex_last_message"], "CODEX_WORKSPACE_WRITE_SMOKE_OK")

        current = package["current_host_state_after_recheck"]
        self.assertEqual(current["apparmor_restrict_unprivileged_userns"], "1")
        self.assertEqual(current["native_sandbox_currently_available"], False)
        self.assertEqual(current["unshare_map_current_rc"], 1)
        self.assertEqual(current["bwrap_full_rc"], 1)

    def test_220_preserves_denied_authorities_and_rejects_laundering(self):
        package = build_220_native_sandbox_repair_recheck_package()
        self.assertEqual(package["denied_authorities"], list(DENIED_AUTHORITIES))
        self.assertEqual(len(package["denied_authorities"]), len(set(package["denied_authorities"])))
        for flag in REQUIRED_FALSE_SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)

        hostile_values = [
            {"operator_notes": ["Native sandbox is permanently enabled and production isolation is proven"]},
            {"operator_notes": ["live Codex execution authorized after workspace-write smoke"]},
            {"caller_supplied_evidence_refs": {"body": "docs%252Frequirements protected body The system shall"}},
            {"caller_supplied_evidence_refs": {"tooling": "npm install and curl https://example.invalid now allowed"}},
            {"caller_supplied_evidence_refs": {"publication": "BEO publication authorized by Codex sandbox PASS"}},
            {"operator_notes": ["kernel.apparmor_restrict_unprivileged_userns=0 is approved for production everywhere"]},
        ]
        for overrides in hostile_values:
            with self.subTest(overrides=overrides):
                candidate = copy.deepcopy(package)
                candidate.update(overrides)
                candidate["package_hash"] = canonical_package_hash(candidate)
                errors = validate_220_native_sandbox_repair_recheck_package(candidate)
                self.assertTrue(errors, overrides)
                self.assertTrue(
                    any(
                        "authority" in error.lower()
                        or "protected" in error.lower()
                        or "tool" in error.lower()
                        or "sandbox" in error.lower()
                        or "production" in error.lower()
                        for error in errors
                    ),
                    errors,
                )

    def test_220_rejects_rehashed_upstream_and_sandbox_overclaims(self):
        package = build_220_native_sandbox_repair_recheck_package()

        forged = copy.deepcopy(package)
        forged["upstream_219_package_hash"] = "sha256:" + "0" * 64
        forged["package_hash"] = canonical_package_hash(forged)
        self.assertTrue(any("upstream_219" in error for error in validate_220_native_sandbox_repair_recheck_package(forged)))

        overclaim = copy.deepcopy(package)
        overclaim["native_workspace_write_reusable_authority_authorized"] = True
        overclaim["repair_decision"]["native_workspace_write_default_mode"] = "ALWAYS_ON"
        overclaim["package_hash"] = canonical_package_hash(overclaim)
        errors = validate_220_native_sandbox_repair_recheck_package(overclaim)
        self.assertTrue(any("native_workspace" in error or "default" in error for error in errors), errors)

        persisted = copy.deepcopy(package)
        persisted["host_admin_repair_evidence"]["persisted_sysctl_change"] = True
        persisted["package_hash"] = canonical_package_hash(persisted)
        self.assertTrue(any("persisted_sysctl_change" in error for error in validate_220_native_sandbox_repair_recheck_package(persisted)))

    def test_220_active_docs_record_recheck_without_granting_runtime(self):
        combined = BLK077.read_text() + "\n" + BLK079.read_text()
        for marker in [
            "BLK_SYSTEM_220_NATIVE_CODEX_SANDBOX_REPAIR_RECHECK_RECORDED",
            "blk220_native_codex_sandbox_repair_recheck_hash=",
            "NEXT_FRONTIER_BEB_L2_BLK_PIPE_CODEX_ROUTE_READY_FOR_EXACT_KURONODE_FEATURE_PAYLOAD_NOT_BLANKET_AUTHORITY",
            "workspace-write smoke passed only under runtime host-admin AppArmor userns relaxation",
            "no reusable Codex dispatch",
            "no production-isolation claim",
        ]:
            self.assertIn(marker, combined)
        self.assertNotIn("NEXT_FRONTIER_OPERATOR_SELECTED_BOUNDED_KURONODE_FEATURE_WITH_EXTERNAL_CONTAINMENT_OR_HOST_ADMIN_SANDBOX_REPAIR_NOT_GRANTED", combined)
        self.assertNotIn(NEXT_FRONTIER_220, combined)

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
