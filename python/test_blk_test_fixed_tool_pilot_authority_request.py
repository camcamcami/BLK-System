import ast
import unittest
from pathlib import Path

from blk_test_fixed_tool_pilot_authority_request import (
    BLOCKED,
    DISABLED,
    READY,
    build_blk_test_fixed_tool_pilot_authority_request,
    simulate_disabled_blk_test_pilot_adapter,
    validate_blk_test_fixed_tool_pilot_authority_request,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "blk_test_fixed_tool_pilot_authority_request.py"


class BlkTestFixedToolPilotAuthorityRequestTest(unittest.TestCase):
    def _record(self):
        return build_blk_test_fixed_tool_pilot_authority_request(
            request_id="BLK-SYSTEM-044-PILOT-REQUEST-001",
            used_request_ids=set(),
        )

    def test_complete_request_is_ready_for_human_review_not_runtime(self):
        record = self._record()

        self.assertEqual(record["request_status"], "BLK_TEST_FIXED_TOOL_PILOT_AUTHORITY_REQUEST_PACKAGE")
        self.assertEqual(record["review_status"], READY)
        self.assertEqual(record["maturity"], "L0_L1_REQUEST_FIXTURE_ONLY")
        self.assertTrue(record["separate_human_approval_required"])
        self.assertEqual(record["roadmap_source"], "BLK-045")
        self.assertIn("BLK-047", record["governing_docs"])
        self.assertEqual(record["validation_errors"], [])
        for flag in (
            "production_blk_test_mcp_authorized",
            "live_transport_authorized",
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

    def test_required_approval_and_proof_sections_fail_closed(self):
        record = self._record()
        record["separate_human_approval_required"] = False
        record["future_approval_envelope"] = {}
        record["proof_obligations"]["physical_isolation"] = []
        record["hostile_review_checklist"] = []
        record["operator_stop_controls"] = {}

        evaluated = validate_blk_test_fixed_tool_pilot_authority_request(
            record,
            used_request_ids=set(),
        )

        self.assertEqual(evaluated["review_status"], BLOCKED)
        self.assertTrue(any("separate_human_approval_required" in error for error in evaluated["validation_errors"]))
        self.assertTrue(any("future_approval_envelope" in error for error in evaluated["validation_errors"]))
        self.assertTrue(any("physical_isolation" in error for error in evaluated["validation_errors"]))
        self.assertTrue(any("hostile_review_checklist" in error for error in evaluated["validation_errors"]))
        self.assertTrue(any("operator_stop_controls" in error for error in evaluated["validation_errors"]))

    def test_denied_authority_flags_fail_closed_and_are_reset_on_evaluation(self):
        record = self._record()
        record["live_transport_authorized"] = True
        record["fixed_tool_execution_authorized"] = True
        record["beo_publication_authorized"] = True
        record["rtm_generation_authorized"] = True

        evaluated = validate_blk_test_fixed_tool_pilot_authority_request(
            record,
            used_request_ids=set(),
        )

        self.assertEqual(evaluated["review_status"], BLOCKED)
        self.assertTrue(any("live_transport_authorized" in error for error in evaluated["validation_errors"]))
        self.assertTrue(any("fixed_tool_execution_authorized" in error for error in evaluated["validation_errors"]))
        self.assertTrue(any("beo_publication_authorized" in error for error in evaluated["validation_errors"]))
        self.assertTrue(any("rtm_generation_authorized" in error for error in evaluated["validation_errors"]))
        self.assertIs(evaluated["live_transport_authorized"], False)
        self.assertIs(evaluated["fixed_tool_execution_authorized"], False)
        self.assertIs(evaluated["beo_publication_authorized"], False)
        self.assertIs(evaluated["rtm_generation_authorized"], False)

    def test_recursive_authority_laundering_keys_and_strings_fail_closed(self):
        record = self._record()
        record["future_approval_envelope"]["nested"] = {
            "authority": "APPROVED_FOR_LIVE_BLK_TEST",
            "approval_status": "APPROVED",
            "claim": "production sandbox is enforced",
            "transport": {"live_transport_authorized": True},
        }

        evaluated = validate_blk_test_fixed_tool_pilot_authority_request(
            record,
            used_request_ids=set(),
        )

        self.assertEqual(evaluated["review_status"], BLOCKED)
        errors = "\n".join(evaluated["validation_errors"])
        self.assertIn("authority", errors)
        self.assertIn("APPROVED_FOR_LIVE_BLK_TEST", errors)
        self.assertIn("production sandbox is enforced", errors)
        self.assertIn("live_transport_authorized", errors)

    def test_adjacent_approval_reuse_markers_fail_closed(self):
        for marker in (
            "CODEX_LIVE_APPROVAL",
            "BLK_PIPE_EXECUTION_APPROVAL",
            "BLK-SYSTEM-014 / BLK-020 approval reused",
            "BEO_PUBLICATION_APPROVAL",
            "RTM_GENERATION_APPROVAL",
            "DRIFT_REJECTION_AUTHORITY",
        ):
            record = self._record()
            record["future_approval_envelope"]["approval_source"] = marker
            evaluated = validate_blk_test_fixed_tool_pilot_authority_request(
                record,
                used_request_ids=set(),
            )
            self.assertEqual(evaluated["review_status"], BLOCKED, marker)
            self.assertTrue(any(marker in error for error in evaluated["validation_errors"]), marker)

    def test_request_id_replay_blocks_review_readiness(self):
        record = self._record()

        evaluated = validate_blk_test_fixed_tool_pilot_authority_request(
            record,
            used_request_ids={"BLK-SYSTEM-044-PILOT-REQUEST-001"},
        )

        self.assertEqual(evaluated["review_status"], BLOCKED)
        self.assertTrue(any("request replayed" in error for error in evaluated["validation_errors"]))

    def test_generic_runtime_approval_language_in_nested_strings_fails_closed(self):
        record = self._record()
        record["future_approval_envelope"]["grant_text"] = "runtime pilot approved by operator; live pilot allowed"

        evaluated = validate_blk_test_fixed_tool_pilot_authority_request(
            record,
            used_request_ids=set(),
        )

        self.assertEqual(evaluated["review_status"], BLOCKED)
        errors = "\n".join(evaluated["validation_errors"])
        self.assertIn("grant_text", errors)
        self.assertIn("runtime pilot approved", errors)

    def test_excluded_adjacent_authorities_rejects_extra_values(self):
        record = self._record()
        record["excluded_adjacent_authorities"].append("APPROVED_FOR_LIVE_EXECUTION")

        evaluated = validate_blk_test_fixed_tool_pilot_authority_request(
            record,
            used_request_ids=set(),
        )

        self.assertEqual(evaluated["review_status"], BLOCKED)
        self.assertTrue(any("excluded_adjacent_authorities extra" in error for error in evaluated["validation_errors"]), evaluated["validation_errors"])

    def test_proof_obligations_and_fixed_tool_constraints_require_required_content(self):
        record = self._record()
        for section in record["proof_obligations"]:
            record["proof_obligations"][section] = ["ok"]
        record["fixed_tool_registry_constraints"] = ["ok"]

        evaluated = validate_blk_test_fixed_tool_pilot_authority_request(
            record,
            used_request_ids=set(),
        )

        self.assertEqual(evaluated["review_status"], BLOCKED)
        errors = "\n".join(evaluated["validation_errors"])
        self.assertIn("proof_obligations.physical_isolation missing required marker", errors)
        self.assertIn("proof_obligations.source_binding missing required marker", errors)
        self.assertIn("fixed_tool_registry_constraints missing required marker", errors)

    def test_disabled_adapter_has_no_side_effects(self):
        adapter = simulate_disabled_blk_test_pilot_adapter(self._record())

        self.assertEqual(adapter["adapter_result"], DISABLED)
        expected_false = {
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

    def test_source_ast_has_no_live_execution_imports_or_calls(self):
        tree = ast.parse(MODULE.read_text())
        forbidden_imports = {
            "subprocess",
            "socket",
            "requests",
            "urllib",
            "http",
            "ftplib",
            "paramiko",
            "git",
        }
        forbidden_calls = {"eval", "exec", "compile", "open", "__import__"}
        offenders = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] in forbidden_imports:
                        offenders.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.split(".")[0] in forbidden_imports:
                    offenders.append(node.module)
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in forbidden_calls:
                    offenders.append(node.func.id)
                if isinstance(node.func, ast.Attribute) and node.func.attr in {"system", "popen", "Popen", "run"}:
                    offenders.append(node.func.attr)
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
