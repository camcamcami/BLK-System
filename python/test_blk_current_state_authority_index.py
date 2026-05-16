import ast
import unittest
from pathlib import Path

from blk_current_state_authority_index import (
    DEFAULT_SURFACES,
    build_current_state_authority_index,
    evaluate_current_state_authority_index,
    validate_current_state_authority_index,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "blk_current_state_authority_index.py"
BLK079 = ROOT / "docs" / "BLK-079_post-078-current-state-authority-index.md"
BLK077 = ROOT / "docs" / "BLK-077_blk-system-post-078-roadmap.md"

EXPECTED_SURFACES = {
    "BLK-req legislative gateway",
    "BLK-pipe blast shield",
    "Python adapter layer",
    "Validation profiles",
    "BLK-test",
    "Operator health / observability",
    "Codex live-dispatch ladder",
    "BEO publication path",
    "RTM / blk-link",
}

DENIED_FLAGS = [
    "runtime_authority_granted",
    "live_codex_execution_authorized",
    "blk_pipe_dispatch_authorized",
    "production_blk_test_mcp_authorized",
    "authoritative_beo_publication_authorized",
    "runtime_rtm_generation_authorized",
    "rtm_drift_rejection_authorized",
    "protected_blk_req_body_reads_authorized",
    "network_model_cyber_browser_tooling_authorized",
    "package_manager_authorized",
    "production_isolation_claimed",
]

CURRENT_REQUIRED_MARKERS = [
    "BLK_SYSTEM_162_POST_TRACE_CLOSURE_REVIEW_COMPLETE",
    "POST-METADATA-TRACE-CLOSURE-REVIEW-162-001",
    "sha256:5d16dd57fefc7028b70e38843b76469a80a9ea3786195000ad49330f27f93ff9",
    "NEXT_FRONTIER_HARDENING_OR_OPERATOR_SELECTED_AUTHORITY_NOT_GRANTED",
]
RTM_REQUIRED_MARKERS = [
    "BLK_SYSTEM_162_POST_TRACE_CLOSURE_REVIEW_COMPLETE",
    "POST-METADATA-TRACE-CLOSURE-REVIEW-162-001",
    "NEXT_FRONTIER_HARDENING_OR_OPERATOR_SELECTED_AUTHORITY_NOT_GRANTED",
]


class CurrentStateAuthorityIndexTest(unittest.TestCase):
    def test_default_index_ready_for_operator_review_not_authority(self):
        record = build_current_state_authority_index()

        self.assertEqual(record["index_id"], "blk_system_current_state_authority_index")
        self.assertEqual(record["index_status"], "BLK_SYSTEM_CURRENT_STATE_AUTHORITY_INDEX")
        self.assertEqual(record["roadmap_source"], "BLK-077")
        self.assertEqual(record["maturity"], "CURRENT_STATE_INDEX_L0_L1_ONLY")

        evaluated = evaluate_current_state_authority_index(record)

        self.assertEqual(evaluated["evaluation"], "CURRENT_STATE_INDEX_READY_FOR_OPERATOR_REVIEW_NOT_AUTHORITY")
        self.assertEqual(evaluated["validation_errors"], [])

    def test_every_current_authority_surface_present_exactly_once_without_sprint_catalog(self):
        record = build_current_state_authority_index()
        names = [surface["surface"] for surface in record["surfaces"]]

        self.assertEqual(set(names), EXPECTED_SURFACES)
        self.assertEqual(len(names), len(set(names)))
        self.assertLessEqual(len(names), 9, "current-state index must not become a historical sprint catalog")

    def test_current_surface_cutlines_are_concise_and_non_authorizing(self):
        record = build_current_state_authority_index()
        by_surface = {surface["surface"]: surface for surface in record["surfaces"]}

        for surface in record["surfaces"]:
            with self.subTest(surface=surface["surface"]):
                self.assertIn("BLK-077", surface["governing_docs"])
                self.assertLessEqual(
                    len(surface["authority_cutline"]),
                    900,
                    f"{surface['surface']} authority cutline is too long for lean current-state use",
                )
                self.assertNotRegex(surface["authority_cutline"], r"BLK_SYSTEM_12[0-9].*BLK_SYSTEM_13[0-9].*BLK_SYSTEM_14[0-9]")

        rtm_link = by_surface["RTM / blk-link"]
        self.assertEqual(rtm_link["state"], "post_metadata_trace_closure_review_162_complete")
        self.assertEqual(rtm_link["maturity"], "L2_METADATA_TRACE_CLOSURE_REVIEW_COMPLETE_NOT_AUTHORITY")
        for marker in RTM_REQUIRED_MARKERS:
            self.assertIn(marker, rtm_link["authority_cutline"])
        self.assertIn("does not grant reusable production `blk-link`", rtm_link["authority_cutline"])
        self.assertIn("no reusable RTM generation", rtm_link["authority_cutline"])

        blk_req = by_surface["BLK-req legislative gateway"]
        self.assertEqual(blk_req["state"], "blk_req_metadata_bound_publication_request_127_complete")
        self.assertEqual(blk_req["maturity"], "L0_L1_METADATA_BOUND_BEO_PUBLICATION_PREREQUISITE_REQUEST_REVIEW_ONLY")
        self.assertIn("Protected bodies remain isolated", blk_req["authority_cutline"])

        beo_path = by_surface["BEO publication path"]
        self.assertEqual(beo_path["state"], "authoritative_beo_publication_finality_152_complete")
        self.assertEqual(beo_path["maturity"], "L3_AUTHORITATIVE_BEO_PUBLICATION_SIGNER_STORAGE_LEDGER_FINALITY_COMPLETE")
        self.assertIn("canonical signer", beo_path["authority_cutline"])
        self.assertIn("immutable-storage", beo_path["authority_cutline"])
        self.assertIn("public-ledger", beo_path["authority_cutline"])
        self.assertIn("no reusable publication authority", beo_path["authority_cutline"])

    def test_human_index_is_lean_current_state_not_historical_ledger(self):
        text = BLK079.read_text()
        lines = text.splitlines()

        self.assertLessEqual(len(lines), 180, "BLK-079 should be an active current-state map, not a ledger")
        self.assertLessEqual(len(text), 20000, "BLK-079 active index is too large for lean documentation")
        self.assertFalse(any(len(line) > 900 for line in lines), "BLK-079 has ledger-style oversized lines")
        self.assertNotIn("Persistent doctrine gate marker: BLK-SYSTEM-079 pins", text)
        self.assertNotIn("BLK-SYSTEM-125 pins metadata-only BEB/BEO handoff completion; BLK-SYSTEM-126", text)
        self.assertNotIn("Historical next sprint selected after", text)
        self.assertIn("LEAN_CURRENT_STATE_INDEX_ACTIVE", text)
        self.assertNotIn("This sprint closeout", text)
        self.assertNotRegex(text, r"docs/outcomes/BLK-SYSTEM-\\d+_sprint-closeout\\.md")
        self.assertIn("docs/outcomes/", text)
        for surface in EXPECTED_SURFACES:
            self.assertIn(surface, text)
        for marker in CURRENT_REQUIRED_MARKERS:
            self.assertIn(marker, text)

    def test_roadmap_remains_occam_hardening_only(self):
        text = BLK077.read_text()
        self.assertIn("ROADMAP_OCCAM_PRODUCTION_ONLY", text)
        self.assertIn("NEXT_FRONTIER_HARDENING_OR_OPERATOR_SELECTED_AUTHORITY_NOT_GRANTED", text)
        self.assertIn("POST_TRACE_CLOSURE_REVIEW_COMPLETE", text)
        self.assertLessEqual(len(text.splitlines()), 130)
        self.assertNotIn("High-Level Roadmap to Complete BLK-System", text)

    def test_runtime_and_adjacent_authorities_are_all_denied(self):
        record = build_current_state_authority_index()

        for flag in DENIED_FLAGS:
            self.assertIs(record[flag], False, flag)

        by_surface = {surface["surface"]: surface for surface in record["surfaces"]}
        self.assertIn("not execution-authorized", by_surface["Codex live-dispatch ladder"]["authority_cutline"])
        self.assertIn("Production MCP remains disabled", by_surface["BLK-test"]["authority_cutline"])
        self.assertIn("no protected-body", by_surface["RTM / blk-link"]["authority_cutline"])
        self.assertIn("no target/source/Git mutation", by_surface["RTM / blk-link"]["authority_cutline"])

    def test_post103_generic_current_state_surfaces_do_not_use_pre100_stale_states(self):
        record = build_current_state_authority_index()
        states = {surface["surface"]: surface["state"] for surface in record["surfaces"]}

        self.assertNotIn("draft_and_fixture_only", states.values())
        self.assertNotIn("offline_fixture_only", states.values())
        self.assertEqual(states["BEO publication path"], "authoritative_beo_publication_finality_152_complete")
        self.assertEqual(states["RTM / blk-link"], "post_metadata_trace_closure_review_162_complete")

        for stale_state in ("draft_and_fixture_only", "offline_fixture_only"):
            stale_record = build_current_state_authority_index()
            stale_record["surfaces"][0]["state"] = stale_state
            errors = validate_current_state_authority_index(stale_record)
            self.assertTrue(any("unsupported state" in error for error in errors), (stale_state, errors))

    def test_unsupported_state_and_maturity_fail_closed(self):
        record = build_current_state_authority_index()
        record["surfaces"][0]["state"] = "LIVE_EXECUTION_ENABLED"
        record["surfaces"][1]["maturity"] = "L5_PRODUCTION_AUTHORITY"

        errors = validate_current_state_authority_index(record)
        evaluated = evaluate_current_state_authority_index(record)

        self.assertTrue(any("unsupported state" in error for error in errors))
        self.assertTrue(any("unsupported maturity" in error for error in errors))
        self.assertEqual(evaluated["evaluation"], "CURRENT_STATE_INDEX_BLOCKED")

    def test_recursive_authority_laundering_keys_and_values_fail_closed(self):
        record = build_current_state_authority_index()
        record["surfaces"][0]["nested"] = {
            "APPROVED_FOR_LIVE_EXECUTION": False,
            "notes": ["authoritative BEO publication approved"],
        }

        errors = validate_current_state_authority_index(record)
        evaluated = evaluate_current_state_authority_index(record)

        self.assertTrue(any("forbidden authority wording" in error for error in errors), errors)
        self.assertEqual(evaluated["evaluation"], "CURRENT_STATE_INDEX_BLOCKED")

    def test_recursive_denied_flags_and_generic_authority_claims_fail_closed(self):
        record = build_current_state_authority_index()
        record["surfaces"][0]["nested"] = {
            "live_codex_execution_authorized": True,
            "execution_authorized": True,
            "authority": "approved for runtime execution",
            "notes": ["runtime_authority_granted"],
        }

        errors = validate_current_state_authority_index(record)
        evaluated = evaluate_current_state_authority_index(record)

        self.assertTrue(any("live_codex_execution_authorized" in error for error in errors), errors)
        self.assertTrue(any("execution_authorized" in error for error in errors), errors)
        self.assertTrue(any("approved for runtime execution" in error for error in errors), errors)
        self.assertTrue(any("runtime_authority_granted" in error for error in errors), errors)
        self.assertEqual(evaluated["evaluation"], "CURRENT_STATE_INDEX_BLOCKED")

    def test_extra_authority_claim_fields_fail_closed(self):
        record = build_current_state_authority_index()
        record["approved_for_runtime_execution"] = True
        record["surfaces"][0]["approved"] = True
        record["surfaces"][0]["authorized"] = True
        record["surfaces"][0]["approval_status"] = "approved"
        record["surfaces"][0]["note"] = "live execution authorized"
        record["surfaces"][1]["authority_cutline"] = "runtime execution authorized"

        errors = validate_current_state_authority_index(record)
        evaluated = evaluate_current_state_authority_index(record)

        for marker in [
            "approved_for_runtime_execution",
            "approved",
            "authorized",
            "approval_status",
            "note",
            "runtime execution authorized",
        ]:
            self.assertTrue(any(marker in error for error in errors), (marker, errors))
        self.assertEqual(evaluated["evaluation"], "CURRENT_STATE_INDEX_BLOCKED")

    def test_natural_language_authority_claims_and_governing_doc_laundering_fail_closed(self):
        phrases = [
            "Live Codex execution is authorized",
            "runtime-execution-authorized",
            "Production BLK-test MCP is authorized",
            "RTM drift rejection is authorized",
            "Production sandbox is enforced",
            "BEO publication authorized",
            "Publication authority granted",
            "approved for publication",
            "greenlit for production",
            "exact-ID retrieval authorized.",
            "stagedRevisionOverwriteIsAuthorized",
            "publicAuthorityLedgerRollbackIsAuthorized",
            "BEO%20publication%20authorized",
            "publish%2542EO",
            "RTMGenerationAuthorized",
            "driftRejectionExecuted",
            "productionBlkLinkEnabled",
            "docs%2525252Frequirements%2525252Factive%2525252FREQ-001.md",
        ]
        for phrase in phrases:
            record = build_current_state_authority_index()
            record["surfaces"][0]["authority_cutline"] = phrase
            errors = validate_current_state_authority_index(record)
            self.assertTrue(errors, phrase)

        for bad_doc in [{"is_authorized": True}, "approved", "runtime authority granted"]:
            record = build_current_state_authority_index()
            record["surfaces"][0]["governing_docs"].append(bad_doc)
            errors = validate_current_state_authority_index(record)
            self.assertTrue(errors, bad_doc)

    def test_default_denial_phrases_do_not_false_positive(self):
        record = build_current_state_authority_index()
        record["surfaces"][0]["authority_cutline"] = (
            "does not capture RTM drift-rejection approval; "
            "does not execute RTM drift rejection; "
            "no protected-body reads or hashing; "
            "no source mutation authorized; "
            "no runtime blk-link trace closure occurred"
        )
        errors = validate_current_state_authority_index(record)
        self.assertFalse(any("rtmdriftrejectionapproval" in error for error in errors), errors)
        self.assertFalse(any("source mutation authorized" in error for error in errors), errors)
        self.assertFalse(any("runtime blk-link trace closure occurred" in error for error in errors), errors)

    def test_default_record_contains_evaluation_and_evaluated_records_validate(self):
        record = build_current_state_authority_index()
        self.assertEqual(record["evaluation"], "CURRENT_STATE_INDEX_READY_FOR_OPERATOR_REVIEW_NOT_AUTHORITY")
        self.assertEqual(record["validation_errors"], [])

        evaluated = evaluate_current_state_authority_index(record)

        self.assertEqual(validate_current_state_authority_index(evaluated), [])

    def test_positive_authority_flags_fail_closed(self):
        for flag in DENIED_FLAGS:
            record = build_current_state_authority_index()
            record[flag] = True

            errors = validate_current_state_authority_index(record)
            evaluated = evaluate_current_state_authority_index(record)

            self.assertTrue(any(flag in error for error in errors), flag)
            self.assertIs(evaluated[flag], False, flag)
            self.assertEqual(evaluated["evaluation"], "CURRENT_STATE_INDEX_BLOCKED")

    def test_module_contains_no_live_surface_imports_or_calls(self):
        tree = ast.parse(MODULE.read_text())
        forbidden_imports = {"subprocess", "socket", "requests", "urllib", "http", "git"}
        forbidden_calls = {"eval", "exec", "__import__", "compile", "open"}
        offenders = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
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
