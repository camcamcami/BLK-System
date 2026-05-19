import json
import tempfile
import unittest
from pathlib import Path

import kuronode_blk_req_mapping_201_203 as mapping_module
from blk_req_production_gateway_195_199 import (
    build_blk_req_gateway_readiness_review_195,
    build_blk_req_production_gateway_contract_196,
    execute_blk_req_lifecycle_smoke_197,
    reconcile_blk_req_gateway_production_readiness_199,
)
from kuronode_blk_req_vault_bootstrap_200 import build_kuronode_blk_req_vault_bootstrap_200
from kuronode_blk_req_mapping_201_203 import (
    build_kuronode_blk_req_mapping_manifest_201,
    materialize_kuronode_blk_req_mapping_202,
    reconcile_kuronode_blk_req_bridge_203,
)

ROOT = Path(__file__).resolve().parents[1]
BLK077 = ROOT / "docs" / "BLK-077_blk-system-post-078-roadmap.md"
BLK079 = ROOT / "docs" / "BLK-079_post-078-current-state-authority-index.md"


def bootstrap_package_200():
    contract = build_blk_req_production_gateway_contract_196(build_blk_req_gateway_readiness_review_195())
    with tempfile.TemporaryDirectory() as tmp:
        smoke = execute_blk_req_lifecycle_smoke_197(workspace=Path(tmp), contract=contract)
    reconciliation = reconcile_blk_req_gateway_production_readiness_199(contract, smoke)
    return build_kuronode_blk_req_vault_bootstrap_200(reconciliation)


class KuronodeBlkReqMapping201To203Test(unittest.TestCase):
    def test_201_manifest_maps_kuronode_ids_to_exact_blk_req_ids_without_body_or_adjacent_authority(self):
        manifest = build_kuronode_blk_req_mapping_manifest_201(bootstrap_package_200())

        self.assertEqual(manifest["status"], "KURONODE_BLK_REQ_EXACT_ID_MAPPING_MANIFEST_READY")
        self.assertIn("BLK_SYSTEM_201_KURONODE_BLK_REQ_EXACT_ID_MAPPING_MANIFEST_READY", manifest["markers"])
        self.assertEqual(manifest["bootstrap_package_hash"], "sha256:8e0414e4564d7ae6567487e807374497fee337f20ec53eb47a6e7ca9a3958229")
        self.assertEqual(
            manifest["mappings"],
            [
                {"kind": "requirement", "kuronode_id": "R-VIS-001", "blk_req_id": "REQ-001", "label": "Kuronode visualization requirement metadata"},
                {"kind": "requirement", "kuronode_id": "R-ARC-001", "blk_req_id": "REQ-002", "label": "Kuronode architecture requirement metadata"},
                {"kind": "use_case", "kuronode_id": "UC-001", "blk_req_id": "UC-001", "label": "Kuronode primary use-case metadata"},
            ],
        )
        self.assertFalse(manifest["authority_boundary"]["protected_body_migration"])
        self.assertFalse(manifest["authority_boundary"]["body_text_included"])
        self.assertFalse(manifest["authority_boundary"]["broad_kuronode_doc_scan"])
        self.assertFalse(manifest["authority_boundary"]["kuronode_source_git_mutation"])
        self.assertFalse(manifest["authority_boundary"]["rtm_generation"])
        self.assertFalse(manifest["authority_boundary"]["beo_publication"])
        self.assertRegex(manifest["mapping_manifest_hash"], r"^sha256:[0-9a-f]{64}$")

    def test_202_materializes_mapping_and_export_metadata_only_in_sibling_vault(self):
        manifest = build_kuronode_blk_req_mapping_manifest_201(bootstrap_package_200())
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "BLK-req-Kuronode"
            result = materialize_kuronode_blk_req_mapping_202(manifest, root)
            mapping_payload = json.loads((root / "mappings/kuronode-id-map.json").read_text())
            export_payload = json.loads((root / "exports/kuronode-requirements.json").read_text())

        self.assertEqual(result["status"], "KURONODE_BLK_REQ_EXACT_ID_MAPPING_MATERIALIZED")
        self.assertIn("BLK_SYSTEM_202_KURONODE_BLK_REQ_EXACT_ID_MAPPING_MATERIALIZED", result["markers"])
        self.assertEqual(mapping_payload["mappings"], manifest["mappings"])
        self.assertEqual(export_payload["requirements"], [m for m in manifest["mappings"] if m["kind"] == "requirement"])
        self.assertEqual(export_payload["use_cases"], [m for m in manifest["mappings"] if m["kind"] == "use_case"])
        self.assertFalse(mapping_payload["body_text_included"])
        self.assertFalse(export_payload["body_text_included"])
        self.assertFalse(result["protected_body_migration"])
        self.assertFalse(result["broad_kuronode_doc_scan"])
        self.assertFalse(result["kuronode_source_git_mutation"])
        self.assertEqual(result["mapping_file_hash"], mapping_module._hash_package(mapping_payload))
        self.assertEqual(result["export_file_hash"], mapping_module._hash_package(export_payload))
        self.assertRegex(result["materialization_hash"], r"^sha256:[0-9a-f]{64}$")

    def test_203_reconciliation_closes_kuronode_blk_req_bridge_and_active_docs(self):
        manifest = build_kuronode_blk_req_mapping_manifest_201(bootstrap_package_200())
        with tempfile.TemporaryDirectory() as tmp:
            materialized = materialize_kuronode_blk_req_mapping_202(manifest, Path(tmp) / "BLK-req-Kuronode")
        reconciliation = reconcile_kuronode_blk_req_bridge_203(manifest, materialized)

        self.assertEqual(reconciliation["status"], "KURONODE_BLK_REQ_BRIDGE_RECONCILED_CLEAN")
        self.assertIn("BLK_SYSTEM_203_KURONODE_BLK_REQ_BRIDGE_RECONCILED_CLEAN", reconciliation["markers"])
        self.assertEqual(reconciliation["next_frontier"], "NEXT_FRONTIER_BLK_REQ_CLOSED_NEXT_COMPONENT_SELECTION_NOT_GRANTED")
        self.assertFalse(reconciliation["authority_boundary"]["kuronode_source_git_mutation"])
        self.assertFalse(reconciliation["authority_boundary"]["protected_body_migration"])
        self.assertFalse(reconciliation["authority_boundary"]["rtm_generation"])
        self.assertEqual(reconciliation["mapping_file_hash"], materialized["mapping_file_hash"])
        self.assertEqual(reconciliation["export_file_hash"], materialized["export_file_hash"])
        self.assertRegex(reconciliation["reconciliation_hash"], r"^sha256:[0-9a-f]{64}$")

        combined = BLK077.read_text() + "\n" + BLK079.read_text()
        for marker in [
            "BLK_SYSTEM_203_KURONODE_BLK_REQ_BRIDGE_RECONCILED_CLEAN",
            "BLK_SYSTEM_202_KURONODE_BLK_REQ_EXACT_ID_MAPPING_MATERIALIZED",
            "BLK_SYSTEM_201_KURONODE_BLK_REQ_EXACT_ID_MAPPING_MANIFEST_READY",
            "NEXT_FRONTIER_EXACT_BEO_PUBLICATION_RUN_REQUIRED_FOR_RTM_DRIFT_COVERAGE_NOT_GRANTED",
        ]:
            self.assertIn(marker, combined)
        self.assertNotIn("NEXT_FRONTIER_KURONODE_BLK_REQ_EXACT_ID_MAPPING_OR_OPERATOR_USE_NOT_GRANTED", combined)

    def test_201_202_reject_duplicate_confusable_body_text_authority_and_path_escape_inputs(self):
        bootstrap = bootstrap_package_200()
        cases = [
            ([{"kind": "requirement", "kuronode_id": "R-VIS-001", "blk_req_id": "REQ-001", "label": "ok"}, {"kind": "requirement", "kuronode_id": "R-VIS-001", "blk_req_id": "REQ-002", "label": "ok"}], "duplicate kuronode_id"),
            ([{"kind": "requirement", "kuronode_id": "R-VIS-００１", "blk_req_id": "REQ-001", "label": "ok"}], "ASCII"),
            ([{"kind": "requirement", "kuronode_id": "R-VIS-001", "blk_req_id": "REQ-００１", "label": "ok"}], "ASCII"),
            ([{"kind": "requirement", "kuronode_id": "R-VIS-001", "blk_req_id": "REQ-001", "label": "The system shall render nodes"}], "protected body text"),
            ([{"kind": "requirement", "kuronode_id": "R-VIS-001", "blk_req_id": "REQ-001", "label": "approved for publication"}], "forbidden authority wording"),
            ([{"kind": "requirement", "kuronode_id": "R-VIS-001", "blk_req_id": "REQ-001", "label": "docs%252Frequirements%252Factive%252FREQ-001.md"}], "protected active-vault path"),
        ]
        for mappings, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(ValueError, message):
                    build_kuronode_blk_req_mapping_manifest_201(bootstrap, mappings)

        forged = mapping_module._deepcopy(bootstrap)
        forged["directory_layout"].append("docs/requirements/active/live")
        forged["bootstrap_package_hash"] = mapping_module._hash_package(
            {key: value for key, value in forged.items() if key != "bootstrap_package_hash"}
        )
        with self.assertRaisesRegex(ValueError, "bootstrap package .*hash mismatch"):
            build_kuronode_blk_req_mapping_manifest_201(forged)

        manifest = build_kuronode_blk_req_mapping_manifest_201(bootstrap)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "BLK-req-Kuronode"
            outside = Path(tmp) / "outside"
            root.mkdir()
            outside.mkdir()
            (root / "exports").symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "symlink"):
                materialize_kuronode_blk_req_mapping_202(manifest, root)
            self.assertFalse((outside / "kuronode-requirements.json").exists())

    def test_202_rejects_unsafe_existing_scaffold_and_rehashed_manifest_tampering(self):
        manifest = build_kuronode_blk_req_mapping_manifest_201(bootstrap_package_200())

        forged = mapping_module._deepcopy(manifest)
        forged["mappings"][0]["blk_req_id"] = "REQ-999"
        forged["mapping_manifest_hash"] = mapping_module._hash_package(
            {key: value for key, value in forged.items() if key != "mapping_manifest_hash"}
        )
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "mapping manifest canonical"):
                materialize_kuronode_blk_req_mapping_202(forged, Path(tmp) / "BLK-req-Kuronode")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "BLK-req-Kuronode"
            (root / "mappings").mkdir(parents=True)
            (root / "exports").mkdir(parents=True)
            unsafe = {
                "version": 1,
                "mappings": [],
                "body_text_included": False,
                "mapping_contract": {},
                "publication_authorized": True,
                "protected_blk_req_body_reads_authorized": True,
            }
            (root / "mappings/kuronode-id-map.json").write_text(json.dumps(unsafe, sort_keys=True), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unsafe existing mapping output"):
                materialize_kuronode_blk_req_mapping_202(manifest, root)
            self.assertIn("publication_authorized", (root / "mappings/kuronode-id-map.json").read_text())

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "BLK-req-Kuronode"
            (root / "mappings").mkdir(parents=True)
            (root / "exports").mkdir(parents=True)
            unsafe = {
                "version": 1,
                "requirements": [],
                "use_cases": [],
                "body_text_included": False,
                "protected_body_migration": False,
                "rtm_generation": True,
            }
            (root / "exports/kuronode-requirements.json").write_text(json.dumps(unsafe, sort_keys=True), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unsafe existing mapping output"):
                materialize_kuronode_blk_req_mapping_202(manifest, root)
            self.assertIn("rtm_generation", (root / "exports/kuronode-requirements.json").read_text())

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "BLK-req-Kuronode"
            (root / "mappings").mkdir(parents=True)
            (root / "exports").mkdir(parents=True)
            duplicate_key_json = (
                '{"version":1,"mappings":[{"label":"The system shall leak protected body"}],'
                '"body_text_included":false,"mapping_contract":'
                + json.dumps(mapping_module._BOOTSTRAP_EXPECTED_MAPPING_CONTRACT, sort_keys=True)
                + ',"mappings":[]}'
            )
            (root / "mappings/kuronode-id-map.json").write_text(duplicate_key_json, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                materialize_kuronode_blk_req_mapping_202(manifest, root)
            self.assertIn("The system shall leak", (root / "mappings/kuronode-id-map.json").read_text())


if __name__ == "__main__":
    unittest.main()
