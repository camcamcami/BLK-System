import tempfile
import unittest
from pathlib import Path

import blk_req_production_gateway_195_199 as gateway_module
from blk_req_production_gateway_195_199 import (
    build_blk_req_gateway_readiness_review_195,
    build_blk_req_production_gateway_contract_196,
    execute_blk_req_lifecycle_smoke_197,
    reconcile_blk_req_gateway_production_readiness_199,
    validate_gateway_operator_inputs_196,
)
from lint_artifacts import (
    capture_baseline_approval,
    preview_staging_version_hash,
    retrieve_active_artifact_by_exact_id,
    write_staging_draft,
)

ROOT = Path(__file__).resolve().parents[1]
BLK077 = ROOT / "docs" / "BLK-077_blk-system-post-078-roadmap.md"
BLK079 = ROOT / "docs" / "BLK-079_post-078-current-state-authority-index.md"


class BlkReqProductionGateway195To199Test(unittest.TestCase):
    def test_195_196_contract_declares_production_ready_lifecycle_without_adjacent_authority(self):
        review = build_blk_req_gateway_readiness_review_195()
        contract = build_blk_req_production_gateway_contract_196(review)

        self.assertEqual(review["status"], "BLK_REQ_GATEWAY_READY_FOR_PRODUCTION_CONTRACT")
        self.assertRegex(review["review_package_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(contract["status"], "BLK_REQ_PRODUCTION_GATEWAY_CONTRACT_READY")
        self.assertEqual(
            contract["allowed_operations"],
            [
                "lint_staging_draft",
                "write_new_staging_draft",
                "promote_new_baseline_with_exact_hitl_approval",
                "retrieve_active_artifact_by_exact_id",
                "write_staged_revision_draft_from_exact_id",
                "promote_staged_revision_with_parent_hash_lock",
            ],
        )
        self.assertIn("BLK_REQ_PRODUCTION_GATEWAY_PER_EXACT_OPERATION_READY", contract["markers"])
        self.assertIn("NO_BROAD_ACTIVE_VAULT_BODY_SCAN", contract["markers"])
        self.assertIn("NO_BODY_ACCESS_WITHOUT_EXACT_ID_OPERATION", contract["markers"])
        self.assertFalse(contract["side_effects"]["active_vault_body_scan"])
        self.assertTrue(contract["side_effects"]["active_vault_filename_listing_for_id_allocation"])
        self.assertFalse(contract["side_effects"]["beb_dispatch"])
        self.assertFalse(contract["side_effects"]["beo_publication"])
        self.assertFalse(contract["side_effects"]["rtm_generation"])
        self.assertFalse(contract["side_effects"]["target_source_git_mutation"])
        self.assertRegex(contract["contract_package_hash"], r"^sha256:[0-9a-f]{64}$")

    def test_197_lifecycle_smoke_promotes_retrieves_revises_and_binds_hash_chain(self):
        contract = build_blk_req_production_gateway_contract_196(build_blk_req_gateway_readiness_review_195())
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = execute_blk_req_lifecycle_smoke_197(workspace=root, contract=contract)

            active_path = root / result["final_active_relative_path"]
            active_text = active_path.read_text(encoding="utf-8")

        self.assertEqual(result["status"], "BLK_REQ_PRODUCTION_LIFECYCLE_SMOKE_PASSED")
        self.assertEqual(result["artifact_id"], "REQ-001")
        self.assertEqual(result["baseline_promotion_status"], "BASELINE_PROMOTED")
        self.assertEqual(result["initial_retrieval_status"], "ACTIVE_ARTIFACT_RETRIEVED")
        self.assertEqual(result["revision_draft_status"], "REVISION_DRAFT_WRITTEN")
        self.assertEqual(result["revision_promotion_status"], "REVISION_PROMOTED")
        self.assertEqual(result["final_retrieval_status"], "ACTIVE_ARTIFACT_RETRIEVED")
        self.assertNotEqual(result["baseline_version_hash"], result["revision_version_hash"])
        self.assertEqual(result["revision_parent_hash"], result["baseline_version_hash"])
        self.assertIn(result["revision_version_hash"], active_text)
        self.assertTrue(result["exact_id_retrieval_performed"])
        self.assertTrue(result["active_vault_filename_listing_for_id_allocation"])
        self.assertFalse(result["active_vault_body_scan"])
        self.assertFalse(result["rtm_generation"])
        self.assertFalse(result["beo_publication"])
        self.assertFalse(result["target_source_git_mutation"])
        self.assertRegex(result["lifecycle_evidence_hash"], r"^sha256:[0-9a-f]{64}$")

    def test_198_hostile_inputs_reject_authority_laundering_and_protected_path_ids(self):
        contract = build_blk_req_production_gateway_contract_196(build_blk_req_gateway_readiness_review_195())
        bad_inputs = [
            {"baseline_approval_id": "APPROVAL-BLK-SYSTEM-197-BASELINE-001-runtimeExecutionAuthorized"},
            {"revision_approval_id": "APPROVAL-BLK-SYSTEM-197-REVISION-001-docs%252Frequirements%252Factive%252FREQ-001.md"},
            {"baseline_approval_id": "APPROVAL-BLK-SYSTEM-197-BASELINE-001-publishBEO"},
            {"operator_note": "approved for publication"},
        ]
        for overrides in bad_inputs:
            with self.subTest(overrides=overrides):
                with self.assertRaisesRegex(ValueError, "forbidden authority wording|protected active-vault path"):
                    validate_gateway_operator_inputs_196(contract, overrides)


    def test_198_rejects_rehashed_tampered_contract_and_lifecycle_evidence(self):
        contract = build_blk_req_production_gateway_contract_196(build_blk_req_gateway_readiness_review_195())
        tampered_contract = gateway_module._deepcopy(contract)
        tampered_contract["side_effects"]["beo_publication"] = True
        tampered_contract["side_effects"]["target_source_git_mutation"] = True
        tampered_contract["allowed_operations"].append("live_codex_dispatch")
        tampered_contract["BEO_PUBLICATION_AUTHORIZED"] = True
        tampered_contract["contract_package_hash"] = gateway_module._hash_package(
            {key: value for key, value in tampered_contract.items() if key != "contract_package_hash"}
        )
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "contract schema|side_effects|allowed_operations|unsupported"):
                execute_blk_req_lifecycle_smoke_197(workspace=Path(tmp), contract=tampered_contract)

        with tempfile.TemporaryDirectory() as tmp:
            smoke = execute_blk_req_lifecycle_smoke_197(workspace=Path(tmp), contract=contract)
        tampered_smoke = gateway_module._deepcopy(smoke)
        tampered_smoke["beo_publication"] = True
        tampered_smoke["rtm_generation"] = True
        tampered_smoke["target_source_git_mutation"] = True
        tampered_smoke["lifecycle_evidence_hash"] = gateway_module._hash_package(
            {key: value for key, value in tampered_smoke.items() if key != "lifecycle_evidence_hash"}
        )
        with self.assertRaisesRegex(ValueError, "lifecycle evidence|beo_publication|rtm_generation|target_source_git_mutation"):
            reconcile_blk_req_gateway_production_readiness_199(contract, tampered_smoke)

    def test_198_rejects_non_ascii_confusable_operator_inputs(self):
        contract = build_blk_req_production_gateway_contract_196(build_blk_req_gateway_readiness_review_195())
        bad_inputs = [
            {"operator_note": "ａｐｐｒｏｖｅｄ for publication"},
            {"operator_note": "runtime execution authorіzed"},
            {"baseline_approval_id": "ＡＰＰＲＯＶＡＬ-BLK-SYSTEM-197-BASELINE-001"},
            {"revision_approval_id": "APPROVAL-BLK-SYSTEM-197-REVISION-００１"},
            {"operator_note": "ｄｏｃｓ／ｒｅｑｕｉｒｅｍｅｎｔｓ／ａｃｔｉｖｅ／REQ-001.md"},
        ]
        for overrides in bad_inputs:
            with self.subTest(overrides=overrides):
                with self.assertRaisesRegex(ValueError, "ASCII"):
                    validate_gateway_operator_inputs_196(contract, overrides)

    def test_197_lifecycle_smoke_refuses_git_worktree_workspace(self):
        contract = build_blk_req_production_gateway_contract_196(build_blk_req_gateway_readiness_review_195())
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".git").mkdir()
            with self.assertRaisesRegex(ValueError, "git worktree"):
                execute_blk_req_lifecycle_smoke_197(workspace=root, contract=contract)


    def test_198_rejects_rehashed_authority_laundering_in_all_hash_bound_package_text(self):
        readiness = build_blk_req_gateway_readiness_review_195()
        tampered_readiness = gateway_module._deepcopy(readiness)
        tampered_readiness["markers"].append("BEO_PUBLICATION_AUTHORIZED")
        tampered_readiness["selected_next_sprints"][0] = "approved for runtime execution"
        tampered_readiness["review_package_hash"] = gateway_module._hash_package(
            {key: value for key, value in tampered_readiness.items() if key != "review_package_hash"}
        )
        with self.assertRaisesRegex(ValueError, "readiness review schema|forbidden authority wording"):
            build_blk_req_production_gateway_contract_196(tampered_readiness)

        contract = build_blk_req_production_gateway_contract_196(readiness)
        tampered_contract = gateway_module._deepcopy(contract)
        tampered_contract["operator_input_contract"]["active_retrieval"] = "protected body reads authorized; approved for runtime execution"
        tampered_contract["contract_package_hash"] = gateway_module._hash_package(
            {key: value for key, value in tampered_contract.items() if key != "contract_package_hash"}
        )
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "contract schema|forbidden authority wording"):
                execute_blk_req_lifecycle_smoke_197(workspace=Path(tmp), contract=tampered_contract)

        with tempfile.TemporaryDirectory() as tmp:
            smoke = execute_blk_req_lifecycle_smoke_197(workspace=Path(tmp), contract=contract)
        tampered_smoke = gateway_module._deepcopy(smoke)
        tampered_smoke["baseline_promotion_status"] = "BEO_PUBLICATION_AUTHORIZED"
        tampered_smoke["final_active_relative_path"] = "docs/requirements/active/REQ-001.md-runtime-execution-authorized"
        tampered_smoke["lifecycle_evidence_hash"] = gateway_module._hash_package(
            {key: value for key, value in tampered_smoke.items() if key != "lifecycle_evidence_hash"}
        )
        with self.assertRaisesRegex(ValueError, "lifecycle evidence|forbidden authority wording"):
            reconcile_blk_req_gateway_production_readiness_199(contract, tampered_smoke)

    def test_exact_id_and_discord_identity_checks_require_ascii_digits(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            retrieval = retrieve_active_artifact_by_exact_id("REQ-１２３", workspace=root)
            draft = write_staging_draft(
                workspace=root,
                artifact_type="REQ",
                title="Ascii Snowflake",
                body="The gateway shall reject Unicode digit snowflakes.",
                rationale="Needed for exact operator identity checks.",
                linked_nodes=[],
            )
            path = root / draft["relative_path"]
            preview = preview_staging_version_hash(path, workspace=root)
            payload = {
                "idp": "discord",
                "approved": True,
                "approval_id": "APPROVAL-BLK-SYSTEM-198-UNICODE-SNOWFLAKE-001",
                "discord_user_id": "６８４２３５１７８０８３７４５８１９",
                "discord_message_id": "1488733359072084070",
                "interaction_timestamp": "2026-05-17T10:30:00+10:00",
                "staging_relative_path": draft["relative_path"],
                "staging_version_hash": preview["version_hash"],
            }
            approval = capture_baseline_approval(payload, staging_path=path, workspace=root)

        self.assertEqual(retrieval["status"], "ACTIVE_ARTIFACT_RETRIEVAL_REJECTED")
        self.assertIn("ARTIFACT_ID_INVALID", {diagnostic["code"] for diagnostic in retrieval["diagnostics"]})
        self.assertEqual(approval["status"], "BASELINE_APPROVAL_REJECTED")
        self.assertIn("DISCORD_USER_ID_INVALID", {diagnostic["code"] for diagnostic in approval["diagnostics"]})


    def test_198_rejects_plausible_rehashed_lifecycle_scalar_and_hash_forgery(self):
        contract = build_blk_req_production_gateway_contract_196(build_blk_req_gateway_readiness_review_195())
        with tempfile.TemporaryDirectory() as tmp:
            smoke = execute_blk_req_lifecycle_smoke_197(workspace=Path(tmp), contract=contract)
        forged = gateway_module._deepcopy(smoke)
        forged["artifact_id"] = "REQ-999"
        forged["final_active_relative_path"] = "docs/requirements/active/REQ-999.md"
        forged["baseline_version_hash"] = "sha256:" + "1" * 64
        forged["revision_parent_hash"] = "sha256:" + "2" * 64
        forged["revision_version_hash"] = "sha256:" + "3" * 64
        forged["lifecycle_evidence_hash"] = gateway_module._hash_package(
            {key: value for key, value in forged.items() if key != "lifecycle_evidence_hash"}
        )
        with self.assertRaisesRegex(ValueError, "lifecycle evidence|fixture hash|hash chain"):
            reconcile_blk_req_gateway_production_readiness_199(contract, forged)


    def test_198_rejects_rehashed_contract_with_forged_readiness_review_hash(self):
        readiness = build_blk_req_gateway_readiness_review_195()
        contract = build_blk_req_production_gateway_contract_196(readiness)
        for forged_hash in ["sha256:" + "0" * 64, "approved for runtime execution"]:
            forged = gateway_module._deepcopy(contract)
            forged["readiness_review_hash"] = forged_hash
            forged["contract_package_hash"] = gateway_module._hash_package(
                {key: value for key, value in forged.items() if key != "contract_package_hash"}
            )
            with self.subTest(forged_hash=forged_hash):
                with tempfile.TemporaryDirectory() as tmp:
                    with self.assertRaisesRegex(ValueError, "readiness_review_hash|contract schema|forbidden authority wording"):
                        execute_blk_req_lifecycle_smoke_197(workspace=Path(tmp), contract=forged)

    def test_199_reconciliation_and_active_docs_mark_gateway_production_ready(self):
        contract = build_blk_req_production_gateway_contract_196(build_blk_req_gateway_readiness_review_195())
        with tempfile.TemporaryDirectory() as tmp:
            smoke = execute_blk_req_lifecycle_smoke_197(workspace=Path(tmp), contract=contract)
        reconciliation = reconcile_blk_req_gateway_production_readiness_199(contract, smoke)

        self.assertEqual(reconciliation["status"], "BLK_REQ_PRODUCTION_GATEWAY_RECONCILED_CLEAN")
        self.assertIn("NEXT_FRONTIER_OPERATOR_SELECTED_BLK_REQ_USE_OR_NEXT_COMPONENT", reconciliation["next_frontier"])
        self.assertRegex(reconciliation["reconciliation_package_hash"], r"^sha256:[0-9a-f]{64}$")

        roadmap = BLK077.read_text()
        index = BLK079.read_text()
        combined = roadmap + "\n" + index
        for marker in [
            "BLK_SYSTEM_199_BLK_REQ_PRODUCTION_GATEWAY_RECONCILED_CLEAN",
            "BLK_SYSTEM_198_BLK_REQ_GATEWAY_HOSTILE_INPUTS_HARDENED",
            "BLK_SYSTEM_197_BLK_REQ_EXACT_ID_LIFECYCLE_SMOKE_PASSED",
            "BLK_SYSTEM_196_BLK_REQ_PRODUCTION_GATEWAY_CONTRACT_READY",
            "BLK_SYSTEM_195_BLK_REQ_GATEWAY_READINESS_REVIEW_CLEAN",
            "NEXT_FRONTIER_OPERATOR_SELECTED_BLK_REQ_USE_OR_NEXT_COMPONENT",
        ]:
            self.assertIn(marker, combined)


if __name__ == "__main__":
    unittest.main()
