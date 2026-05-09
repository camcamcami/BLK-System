import ast
import unittest
from pathlib import Path

from blk_authority_frontier_selection_gate import (
    BLOCKED,
    DISABLED,
    READY,
    build_authority_frontier_selection_gate,
    simulate_disabled_frontier_activation_adapter,
    validate_authority_frontier_selection_gate,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "blk_authority_frontier_selection_gate.py"


class AuthorityFrontierSelectionGateTest(unittest.TestCase):
    def _record(self, frontier="blk_test_fixed_tool_pilot_l3_l4"):
        return build_authority_frontier_selection_gate(
            selection_id="BLK-SYSTEM-045-FRONTIER-SELECTION-001",
            selected_frontier=frontier,
            used_selection_ids=set(),
        )

    def test_single_frontier_selection_is_ready_for_human_decision_not_runtime(self):
        record = self._record()

        self.assertEqual(record["selection_status"], "BLK_SYSTEM_AUTHORITY_FRONTIER_SELECTION_GATE")
        self.assertEqual(record["review_status"], READY)
        self.assertEqual(record["maturity"], "L0_L1_SELECTION_FIXTURE_ONLY")
        self.assertEqual(record["selected_frontier"], "blk_test_fixed_tool_pilot_l3_l4")
        self.assertIs(record["exactly_one_frontier_selected"], True)
        self.assertIn("BLK-048", record["governing_docs"])
        self.assertEqual(record["validation_errors"], [])
        for flag in (
            "runtime_authority_granted",
            "live_codex_execution_authorized",
            "codex_subprocess_started",
            "blk_pipe_dispatch_authorized",
            "production_blk_test_mcp_authorized",
            "live_blk_test_transport_authorized",
            "fixed_tool_execution_authorized",
            "source_mutation_authorized",
            "git_mutation_authorized",
            "protected_body_read_authorized",
            "protected_body_copy_authorized",
            "protected_body_scan_authorized",
            "beo_publication_authorized",
            "rtm_generation_authorized",
            "drift_rejection_authorized",
            "package_manager_authorized",
            "network_model_cyber_browser_tooling_authorized",
            "production_isolation_claimed",
        ):
            self.assertIs(record[flag], False, flag)

    def test_no_multiple_or_unknown_frontiers_fail_closed(self):
        cases = [None, [], ["codex_live_dispatch_l3_smoke", "blk_test_fixed_tool_pilot_l3_l4"], "beo_publication", "rtm_generation"]
        for frontier in cases:
            record = self._record()
            record["selected_frontier"] = frontier
            evaluated = validate_authority_frontier_selection_gate(record, used_selection_ids=set())
            self.assertEqual(evaluated["review_status"], BLOCKED, frontier)
            self.assertTrue(any("selected_frontier" in error for error in evaluated["validation_errors"]), evaluated["validation_errors"])

    def test_readiness_and_next_sprint_language_cannot_substitute_for_runtime_approval(self):
        forbidden = (
            "next sprint approves runtime pilot",
            "BLK_TEST_PILOT_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME means pilot approved",
            "READY_FOR_AUTHORITY_REVIEW_NOT_EXECUTION means live Codex execution authorized",
            "BEO fixture readiness grants publication approval",
            "RTM fixture readiness grants runtime generation approval",
            "sprint-dispatch approval is runtime approval",
        )
        for phrase in forbidden:
            record = self._record()
            record["decision_evidence"]["operator_phrase"] = phrase
            evaluated = validate_authority_frontier_selection_gate(record, used_selection_ids=set())
            self.assertEqual(evaluated["review_status"], BLOCKED, phrase)
            self.assertTrue(any("forbidden authority wording" in error for error in evaluated["validation_errors"]), evaluated["validation_errors"])

    def test_adjacent_authority_inheritance_fails_closed(self):
        record = self._record()
        record["excluded_adjacent_authorities"].append("APPROVED_FOR_LIVE_EXECUTION")
        record["decision_evidence"]["inherits_from"] = "codex_live_approval and BLK_PIPE_EXECUTION_APPROVAL"

        evaluated = validate_authority_frontier_selection_gate(record, used_selection_ids=set())

        self.assertEqual(evaluated["review_status"], BLOCKED)
        errors = "\n".join(evaluated["validation_errors"])
        self.assertIn("excluded_adjacent_authorities extra", errors)
        self.assertIn("BLK_PIPE_EXECUTION_APPROVAL", errors)

    def test_recursive_generic_authority_laundering_fails_closed(self):
        record = self._record()
        record["decision_evidence"]["nested"] = {
            "authority": "APPROVED_FOR_LIVE_EXECUTION",
            "approval_status": "approved",
            "claim": "production sandbox is enforced",
            "runtime_authority_granted": True,
        }

        evaluated = validate_authority_frontier_selection_gate(record, used_selection_ids=set())

        self.assertEqual(evaluated["review_status"], BLOCKED)
        errors = "\n".join(evaluated["validation_errors"])
        self.assertIn("authority", errors)
        self.assertIn("APPROVED_FOR_LIVE_EXECUTION", errors)
        self.assertIn("production sandbox is enforced", errors)
        self.assertIn("runtime_authority_granted", errors)

    def test_required_decision_fields_cannot_be_replaced_by_placeholders(self):
        record = self._record()
        record["required_future_approval_fields"] = ["ok"]
        record["hostile_review_checklist"] = ["ok"]

        evaluated = validate_authority_frontier_selection_gate(record, used_selection_ids=set())

        self.assertEqual(evaluated["review_status"], BLOCKED)
        errors = "\n".join(evaluated["validation_errors"])
        self.assertIn("required_future_approval_fields missing required marker", errors)
        self.assertIn("hostile_review_checklist missing required marker", errors)

    def test_selection_replay_blocks_readiness(self):
        record = self._record()
        evaluated = validate_authority_frontier_selection_gate(
            record,
            used_selection_ids={"BLK-SYSTEM-045-FRONTIER-SELECTION-001"},
        )
        self.assertEqual(evaluated["review_status"], BLOCKED)
        self.assertTrue(any("selection replayed" in error for error in evaluated["validation_errors"]))

    def test_disabled_activation_adapter_has_complete_no_side_effect_surface(self):
        adapter = simulate_disabled_frontier_activation_adapter(self._record())
        self.assertEqual(adapter["adapter_result"], DISABLED)
        expected_false = {
            "codex_subprocess_started",
            "blk_pipe_dispatched",
            "mcp_server_started",
            "mcp_client_started",
            "fixed_tool_executed",
            "source_mutation_attempted",
            "git_mutation_attempted",
            "protected_body_read_attempted",
            "protected_body_copy_attempted",
            "protected_body_scan_attempted",
            "beo_publication_attempted",
            "rtm_generation_attempted",
            "drift_rejection_attempted",
            "network_called",
            "model_service_called",
            "browser_tooling_called",
            "cyber_tooling_called",
            "package_manager_called",
            "arbitrary_shell_called",
            "production_isolation_claimed",
        }
        self.assertTrue(expected_false.issubset(adapter), sorted(expected_false - set(adapter)))
        for key in expected_false:
            self.assertIs(adapter[key], False, key)

    def test_source_ast_has_no_live_execution_or_mutation_imports(self):
        tree = ast.parse(MODULE.read_text())
        forbidden_imports = {"subprocess", "socket", "requests", "urllib", "http", "ftplib", "paramiko", "git", "os", "shutil", "pathlib"}
        forbidden_calls = {"eval", "exec", "compile", "open", "__import__"}
        offenders = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                offenders.extend(alias.name for alias in node.names if alias.name.split(".")[0] in forbidden_imports)
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.split(".")[0] in forbidden_imports:
                    offenders.append(node.module)
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in forbidden_calls:
                    offenders.append(node.func.id)
                if isinstance(node.func, ast.Attribute) and node.func.attr in {"system", "popen", "Popen", "run", "write", "unlink", "rename"}:
                    offenders.append(node.func.attr)
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
