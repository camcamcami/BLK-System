import copy
import unittest
from pathlib import Path

from blk_system_first_pass_9_9_322 import (
    EXPECTED_322_FIRST_PASS_HASH,
    NEXT_FRONTIER_322,
    build_blk001_006_roadmap_first_pass_done_322,
    validate_blk001_006_roadmap_first_pass_done_322,
)
from blk_system_velocity_to_9_317_321 import (
    OPERATOR_DIRECTIVE_317,
    build_blk_system_development_frontier_317,
    build_exact_no_clock_side_effect_request_318,
    build_blk_system_9_of_10_readiness_matrix_320,
    evaluate_development_authority_laundering_guard_319,
    reconcile_blk_system_development_unblock_321,
)
from blk_system_standing_development_approval_316 import (
    EXPECTED_316_OBSERVED_AT,
    EXPECTED_OPERATOR_DISCORD_ID,
    OPERATOR_STATEMENT_316,
    record_blk_system_standing_development_approval_316,
)

ROOT = Path(__file__).resolve().parents[1]
BLK077 = ROOT / "docs" / "BLK-077_blk-system-post-078-roadmap.md"
ROOT_DOCS = [ROOT / "docs" / f"BLK-00{i}_{name}.md" for i, name in [
    (1, "blk-system-master-architecture"),
    (2, "blk-req-artifact-lifecycle"),
    (3, "blk-pipe-blk-test-orchestration"),
    (4, "blk-pipe-v47-architecture-suite"),
    (5, "blk-req-specification"),
    (6, "blk-req-implementation-brief"),
]]


class BlkSystemFirstPassNineNine322Test(unittest.TestCase):
    def _reconciliation_321(self):
        record_316 = record_blk_system_standing_development_approval_316(
            operator_statement=OPERATOR_STATEMENT_316,
            operator_discord_id=EXPECTED_OPERATOR_DISCORD_ID,
            observed_at=EXPECTED_316_OBSERVED_AT,
        )
        frontier = build_blk_system_development_frontier_317(
            record_316,
            operator_directive=OPERATOR_DIRECTIVE_317,
        )
        request = build_exact_no_clock_side_effect_request_318(frontier)
        guard = evaluate_development_authority_laundering_guard_319(
            request,
            operator_statement=OPERATOR_DIRECTIVE_317,
        )
        matrix = build_blk_system_9_of_10_readiness_matrix_320(guard)
        return reconcile_blk_system_development_unblock_321(matrix)

    def test_322_marks_blk001_to_006_and_roadmap_first_pass_done_for_9_9_not_10(self):
        record = build_blk001_006_roadmap_first_pass_done_322(
            self._reconciliation_321(),
            operator_directive=(
                "plan an execute blk-system sprint for a first pass done of "
                "blk-001 to blk-006 and the blk-system roadmap"
            ),
            target_rating="9.9/10_not_10/10_pending_operator_review_and_verification",
        )

        self.assertEqual(
            record["status"],
            "BLK_SYSTEM_322_ROOT_DOCTRINE_ROADMAP_FIRST_PASS_DONE_FOR_9_9_REVIEW_READY",
        )
        self.assertIn(
            "BLK_SYSTEM_322_ROOT_DOCTRINE_ROADMAP_FIRST_PASS_DONE_FOR_9_9_REVIEW_READY",
            record["markers"],
        )
        self.assertEqual(record["next_frontier"], NEXT_FRONTIER_322)
        self.assertEqual(record["readiness_rating"], "9.9/10_theory_done_pending_review")
        self.assertEqual(
            record["root_doctrine_docs"],
            ["BLK-001", "BLK-002", "BLK-003", "BLK-004", "BLK-005", "BLK-006"],
        )
        self.assertEqual(record["roadmap_doc"], "BLK-077")
        self.assertTrue(record["side_effects"]["root_doctrine_first_pass_done_recorded"])
        self.assertTrue(record["side_effects"]["roadmap_first_pass_done_recorded"])
        self.assertFalse(record["side_effects"]["ten_of_ten_claimed"])
        self.assertFalse(record["side_effects"]["beo_publication"])
        self.assertFalse(record["side_effects"]["rtm_generation"])
        self.assertFalse(record["side_effects"]["production_blk_link"])
        self.assertFalse(record["side_effects"]["protected_body_access"])
        self.assertEqual(record["first_pass_hash"], EXPECTED_322_FIRST_PASS_HASH)
        self.assertEqual(validate_blk001_006_roadmap_first_pass_done_322(record), record)

    def test_322_rejects_10_of_10_and_side_effect_laundering(self):
        reconciliation = self._reconciliation_321()
        with self.assertRaisesRegex(ValueError, "target_rating"):
            build_blk001_006_roadmap_first_pass_done_322(
                reconciliation,
                operator_directive="plan an execute blk-system sprint for a first pass done of blk-001 to blk-006 and the blk-system roadmap",
                target_rating="10/10_final_complete",
            )

        record = build_blk001_006_roadmap_first_pass_done_322(
            reconciliation,
            operator_directive="plan an execute blk-system sprint for a first pass done of blk-001 to blk-006 and the blk-system roadmap",
            target_rating="9.9/10_not_10/10_pending_operator_review_and_verification",
        )
        tampered = copy.deepcopy(record)
        tampered["side_effects"]["beo_publication"] = True
        with self.assertRaisesRegex(ValueError, "side_effects"):
            validate_blk001_006_roadmap_first_pass_done_322(tampered)

        tampered = copy.deepcopy(record)
        tampered["review_gap_register"].append("BEO publication authorized by roadmap")
        tampered["first_pass_hash"] = tampered["first_pass_hash"]
        with self.assertRaisesRegex(ValueError, "canonical hash|authority|review_gap_register"):
            validate_blk001_006_roadmap_first_pass_done_322(tampered)

    def test_322_rejects_rehashed_or_retarged_321_dependency(self):
        reconciliation = self._reconciliation_321()
        tampered = copy.deepcopy(reconciliation)
        tampered["next_frontier"] = "NEXT_FRONTIER_FORGED_9_9_SIDE_EFFECTS_GRANTED"
        with self.assertRaisesRegex(ValueError, "321"):
            build_blk001_006_roadmap_first_pass_done_322(
                tampered,
                operator_directive="plan an execute blk-system sprint for a first pass done of blk-001 to blk-006 and the blk-system roadmap",
                target_rating="9.9/10_not_10/10_pending_operator_review_and_verification",
            )

    def test_322_roadmap_records_first_pass_done_without_patching_root_docs(self):
        roadmap = BLK077.read_text()

        self.assertIn(
            "BLK_SYSTEM_322_ROOT_DOCTRINE_ROADMAP_FIRST_PASS_DONE_FOR_9_9_REVIEW_READY",
            roadmap,
        )
        self.assertIn(NEXT_FRONTIER_322, roadmap)
        self.assertIn(EXPECTED_322_FIRST_PASS_HASH, roadmap)
        self.assertIn("9.9/10 theory done; not 10/10", roadmap)
        self.assertIn("operator review and verification activities remain", roadmap)
        self.assertNotIn("10/10 final", roadmap)
        self.assertIn("no BEO publication", roadmap)
        self.assertIn("no RTM", roadmap)
        self.assertIn("no production `blk-link`", roadmap)

        for path in ROOT_DOCS:
            text = path.read_text()
            self.assertIn("BLK_001_TO_006_FIXED_OVERVIEW_NOT_SPRINT_STATE", text, path.name)
            self.assertNotIn("BLK_SYSTEM_322", text, path.name)
