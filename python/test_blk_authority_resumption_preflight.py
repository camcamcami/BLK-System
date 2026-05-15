import unittest

from blk_authority_resumption_preflight import (
    BLOCKED,
    READY,
    build_authority_resumption_preflight,
    evaluate_authority_resumption_preflight,
    validate_authority_resumption_preflight,
)
from blk_current_state_authority_index import DENIED_FLAGS


class AuthorityResumptionPreflightTest(unittest.TestCase):
    def test_default_preflight_is_review_only_and_selects_no_authority_rung(self):
        record = build_authority_resumption_preflight()
        evaluated = evaluate_authority_resumption_preflight(record)

        self.assertEqual(record["preflight_id"], "AUTHORITY-RESUMPTION-PREFLIGHT-150-001")
        self.assertEqual(record["preflight_status"], READY)
        self.assertEqual(record["source_index_evaluation"], "CURRENT_STATE_INDEX_READY_FOR_OPERATOR_REVIEW_NOT_AUTHORITY")
        self.assertEqual(record["current_frontier"], "NEXT_FRONTIER_METADATA_BOUND_RTM_BLK_LINK_RECONCILIATION_DECISION_NOT_GRANTED")
        self.assertIsNone(record["selected_authority_rung"])
        self.assertIs(record["operator_decision_required_before_resumption"], True)
        self.assertGreaterEqual(len(record["candidate_authority_rungs"]), 4)
        self.assertTrue(all(item["status"] == "candidate_not_selected" for item in record["candidate_authority_rungs"]))
        self.assertTrue(record["required_evidence_before_selection"])
        for flag in DENIED_FLAGS:
            self.assertIs(record[flag], False, flag)
        self.assertTrue(all(value is False for value in record["side_effects"].values()))
        self.assertEqual(evaluated["evaluation"], READY)
        self.assertEqual(evaluated["validation_errors"], [])

    def test_preflight_rejects_selection_approval_execution_and_laundering(self):
        record = build_authority_resumption_preflight()
        record["selected_authority_rung"] = "rtm_generation"
        record["candidate_authority_rungs"][0]["status"] = "approved"
        record["side_effects"]["execution_attempted"] = True
        record["runtime_rtm_generation_authorized"] = True
        record["required_evidence_before_selection"].append(
            {"docs%2525252Frequirements%2525252Factive": "The system shall remain hidden."}
        )
        record["operator_note"] = "BEO%20publication%20authorized"

        errors = validate_authority_resumption_preflight(record)
        evaluated = evaluate_authority_resumption_preflight(record)

        for marker in [
            "selected_authority_rung must remain null",
            "candidate_not_selected",
            "execution_attempted must remain false",
            "runtime_rtm_generation_authorized must remain false",
            "docsrequirementsactive",
            "beopublicationauthorized",
            "unsupported top-level key 'operator_note'",
        ]:
            self.assertTrue(any(marker in error for error in errors), (marker, errors))
        self.assertEqual(evaluated["evaluation"], BLOCKED)


if __name__ == "__main__":
    unittest.main()
