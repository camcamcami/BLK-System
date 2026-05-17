import tempfile
import unittest
from pathlib import Path

import kuronode_blk_req_vault_bootstrap_200 as bootstrap_module
from blk_req_production_gateway_195_199 import (
    build_blk_req_gateway_readiness_review_195,
    build_blk_req_production_gateway_contract_196,
    execute_blk_req_lifecycle_smoke_197,
    reconcile_blk_req_gateway_production_readiness_199,
)
from kuronode_blk_req_vault_bootstrap_200 import (
    build_kuronode_blk_req_vault_bootstrap_200,
    materialize_kuronode_blk_req_vault_skeleton_200,
)

ROOT = Path(__file__).resolve().parents[1]
BLK077 = ROOT / "docs" / "BLK-077_blk-system-post-078-roadmap.md"
BLK079 = ROOT / "docs" / "BLK-079_post-078-current-state-authority-index.md"


def upstream_reconciliation():
    contract = build_blk_req_production_gateway_contract_196(build_blk_req_gateway_readiness_review_195())
    with tempfile.TemporaryDirectory() as tmp:
        smoke = execute_blk_req_lifecycle_smoke_197(workspace=Path(tmp), contract=contract)
    return reconcile_blk_req_gateway_production_readiness_199(contract, smoke)


class KuronodeBlkReqVaultBootstrap200Test(unittest.TestCase):
    def test_200_blueprint_selects_sibling_vault_layout_without_kuronode_source_mutation(self):
        package = build_kuronode_blk_req_vault_bootstrap_200(upstream_reconciliation())

        self.assertEqual(package["status"], "KURONODE_BLK_REQ_VAULT_BOOTSTRAP_BLUEPRINT_READY")
        self.assertIn("BLK_SYSTEM_200_KURONODE_BLK_REQ_VAULT_BOOTSTRAP_BLUEPRINT_READY", package["markers"])
        self.assertEqual(package["kuronode_source_root"], "/home/dad/code/Kuronode-v1")
        self.assertEqual(package["vault_root"], "/home/dad/BLK-req-Kuronode")
        self.assertEqual(
            package["directory_layout"],
            [
                "docs/requirements/staging",
                "docs/requirements/active",
                "docs/use_cases/staging",
                "docs/use_cases/active",
                "mappings",
                "exports",
            ],
        )
        self.assertEqual(
            package["bootstrap_files"],
            [
                "docs/.blk_req_baseline_approval_ledger.json",
                "mappings/kuronode-id-map.json",
                "exports/kuronode-requirements.json",
            ],
        )
        self.assertEqual(package["id_mapping_contract"]["kuronode_requirement_ids"], "R-* source IDs map to exact REQ-### BLK-req IDs")
        self.assertFalse(package["authority_boundary"]["kuronode_source_git_mutation"])
        self.assertFalse(package["authority_boundary"]["protected_body_migration"])
        self.assertFalse(package["authority_boundary"]["broad_kuronode_doc_scan"])
        self.assertTrue(package["authority_boundary"]["non_git_sibling_vault_bootstrap"])
        self.assertRegex(package["bootstrap_package_hash"], r"^sha256:[0-9a-f]{64}$")

    def test_200_materializer_creates_only_the_declared_skeleton_in_non_git_workspace(self):
        package = build_kuronode_blk_req_vault_bootstrap_200(upstream_reconciliation())
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "BLK-req-Kuronode"
            result = materialize_kuronode_blk_req_vault_skeleton_200(package, root)
            created_paths = sorted(str(path.relative_to(root)) for path in root.rglob("*") if path.is_file() or path.is_dir())

        self.assertEqual(result["status"], "KURONODE_BLK_REQ_VAULT_SKELETON_MATERIALIZED")
        self.assertEqual(result["vault_root_name"], "BLK-req-Kuronode")
        for expected in package["directory_layout"] + package["bootstrap_files"]:
            self.assertIn(expected, created_paths)
        self.assertFalse(result["kuronode_source_git_mutation"])
        self.assertFalse(result["protected_body_migration"])
        self.assertFalse(result["broad_kuronode_doc_scan"])
        self.assertRegex(result["materialization_hash"], r"^sha256:[0-9a-f]{64}$")

    def test_200_rejects_rehashed_upstream_tampering_git_workspaces_and_laundering(self):
        reconciliation = upstream_reconciliation()
        tampered = bootstrap_module._deepcopy(reconciliation)
        tampered["authority_boundary"]["target_source_git_mutation"] = True
        tampered["next_frontier"] = "Kuronode source mutation approved"
        tampered["reconciliation_package_hash"] = bootstrap_module._hash_package(
            {key: value for key, value in tampered.items() if key != "reconciliation_package_hash"}
        )
        with self.assertRaisesRegex(ValueError, "upstream reconciliation|source mutation|forbidden authority wording"):
            build_kuronode_blk_req_vault_bootstrap_200(tampered)

        for field in ("contract_package_hash", "lifecycle_evidence_hash"):
            forged_upstream = bootstrap_module._deepcopy(reconciliation)
            forged_upstream[field] = "sha256:" + "1" * 64
            forged_upstream["reconciliation_package_hash"] = bootstrap_module._hash_package(
                {key: value for key, value in forged_upstream.items() if key != "reconciliation_package_hash"}
            )
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, f"upstream reconciliation {field} mismatch"):
                    build_kuronode_blk_req_vault_bootstrap_200(forged_upstream)

        package = build_kuronode_blk_req_vault_bootstrap_200(reconciliation)
        forged = bootstrap_module._deepcopy(package)
        forged["vault_root"] = "/home/dad/code/Kuronode-v1/docs/requirements"
        forged["authority_boundary"]["kuronode_source_git_mutation"] = True
        forged["bootstrap_package_hash"] = bootstrap_module._hash_package(
            {key: value for key, value in forged.items() if key != "bootstrap_package_hash"}
        )
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "bootstrap package|Kuronode source|source_git_mutation"):
                materialize_kuronode_blk_req_vault_skeleton_200(forged, Path(tmp) / "BLK-req-Kuronode")

        with tempfile.TemporaryDirectory() as tmp:
            git_root = Path(tmp) / "repo"
            git_root.mkdir()
            (git_root / ".git").mkdir()
            with self.assertRaisesRegex(ValueError, "git worktree"):
                materialize_kuronode_blk_req_vault_skeleton_200(package, git_root / "BLK-req-Kuronode")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "BLK-req-Kuronode"
            outside = Path(tmp) / "outside"
            root.mkdir()
            outside.mkdir()
            (root / "mappings").symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "symlink"):
                materialize_kuronode_blk_req_vault_skeleton_200(package, root)
            self.assertFalse((outside / "kuronode-id-map.json").exists())

    def test_200_active_docs_mark_kuronode_vault_bootstrap_as_current_frontier(self):
        package = build_kuronode_blk_req_vault_bootstrap_200(upstream_reconciliation())
        combined = BLK077.read_text() + "\n" + BLK079.read_text()

        self.assertIn("BLK_SYSTEM_200_KURONODE_BLK_REQ_VAULT_BOOTSTRAP_BLUEPRINT_READY", combined)
        self.assertIn("NEXT_FRONTIER_OPERATOR_SELECTED_BOUNDED_KURONODE_FEATURE_WITH_EXTERNAL_CONTAINMENT_OR_HOST_ADMIN_SANDBOX_REPAIR_NOT_GRANTED", combined)
        self.assertIn(package["bootstrap_package_hash"], combined)
        self.assertNotIn("NEXT_FRONTIER_OPERATOR_SELECTED_BLK_REQ_USE_OR_NEXT_COMPONENT", combined)


if __name__ == "__main__":
    unittest.main()
