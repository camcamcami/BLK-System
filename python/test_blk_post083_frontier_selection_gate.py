import ast
import unittest
from pathlib import Path

from blk_post083_frontier_selection_gate import (
    ALLOWED_FRONTIERS,
    BLOCKED,
    BLOCKED_PENDING_PUBLICATION_PREREQUISITES,
    DENIED_FLAGS,
    DISABLED,
    READY,
    build_post083_frontier_selection_gate,
    simulate_disabled_post083_frontier_activation_adapter,
    validate_post083_frontier_selection_gate,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "blk_post083_frontier_selection_gate.py"

EXPECTED_FRONTIERS = {
    "bounded_blk_test_evidence_refresh",
    "beo_publication_pilot_execution_request",
    "codex_live_dispatch_l3_smoke",
    "rtm_authority_request_after_publication_prerequisites",
    "bounded_consolidation_or_remediation_sprint",
}


class Post083FrontierSelectionGateTest(unittest.TestCase):
    def _record(self, frontier="beo_publication_pilot_execution_request", **kwargs):
        return build_post083_frontier_selection_gate(
            selection_id="BLK-SYSTEM-084-POST083-FRONTIER-SELECTION-001",
            selected_frontier=frontier,
            used_selection_ids=set(),
            **kwargs,
        )

    def test_exact_post083_frontier_selection_is_review_ready_not_authority(self):
        record = self._record()

        self.assertEqual(record["selection_status"], "BLK_SYSTEM_POST_083_FRONTIER_SELECTION_GATE")
        self.assertEqual(record["review_status"], READY)
        self.assertEqual(record["maturity"], "L0_L1_POST_083_SELECTION_FIXTURE_ONLY")
        self.assertEqual(record["roadmap_source"], "BLK-077")
        self.assertEqual(record["current_state_source"], "BLK-079")
        self.assertEqual(record["post083_source"], "BLK-083")
        self.assertEqual(record["selected_frontier"], "beo_publication_pilot_execution_request")
        self.assertIs(record["exactly_one_frontier_selected"], True)
        self.assertIn("BLK-083", record["governing_docs"])
        self.assertIn("BLK-084", record["governing_docs"])
        self.assertEqual(record["validation_errors"], [])
        for flag in DENIED_FLAGS:
            self.assertIs(record[flag], False, flag)

    def test_every_current_candidate_has_frontier_specific_governing_docs(self):
        self.assertEqual(set(ALLOWED_FRONTIERS), EXPECTED_FRONTIERS)
        expectations = {
            "bounded_blk_test_evidence_refresh": {"BLK-017", "BLK-019", "BLK-020", "BLK-074", "BLK-077", "BLK-079", "BLK-084"},
            "beo_publication_pilot_execution_request": {"BLK-022", "BLK-057", "BLK-060", "BLK-083", "BLK-084"},
            "codex_live_dispatch_l3_smoke": {"BLK-040", "BLK-041", "BLK-042", "BLK-043", "BLK-044", "BLK-084"},
            "rtm_authority_request_after_publication_prerequisites": {"BLK-023", "BLK-027", "BLK-029", "BLK-030", "BLK-033", "BLK-083", "BLK-084"},
            "bounded_consolidation_or_remediation_sprint": {"BLK-077", "BLK-079", "BLK-084"},
        }
        for frontier, expected_docs in expectations.items():
            record = self._record(
                frontier,
                publication_prerequisites_satisfied=frontier == "rtm_authority_request_after_publication_prerequisites",
            )
            self.assertTrue(expected_docs.issubset(set(record["governing_docs"])), (frontier, record["governing_docs"]))
            if frontier != "rtm_authority_request_after_publication_prerequisites":
                self.assertEqual(record["review_status"], READY, frontier)

    def test_next_logical_and_generic_names_do_not_select_higher_authority(self):
        cases = [
            None,
            [],
            ["beo_publication_pilot_execution_request", "codex_live_dispatch_l3_smoke"],
            "next logical",
            "next sprint",
            "beo_publication",
            "publication_pilot",
            "rtm_generation",
            "blk_test_refresh",
        ]
        for frontier in cases:
            record = self._record()
            record["selected_frontier"] = frontier
            evaluated = validate_post083_frontier_selection_gate(record, used_selection_ids=set())
            self.assertEqual(evaluated["review_status"], BLOCKED, frontier)
            self.assertTrue(any("selected_frontier" in error for error in evaluated["validation_errors"]), evaluated["validation_errors"])

    def test_nested_compact_encoded_and_stale_frontier_mentions_fail_closed(self):
        cases = [
            "codex live dispatch l3 smoke",
            "codexLiveDispatchL3Smoke",
            "codex%20live%20dispatch%20l3%20smoke",
            "beoPublicationPilotExecutionRequest",
            "bounded BLK-test evidence refresh",
            "blk test fixed tool pilot l3 l4",
            "blkTestFixedToolPilotL3L4",
            "blk_test_fixed_tool_pilot_l3_l4",
        ]
        for phrase in cases:
            record = self._record()
            record["decision_evidence"]["notes"] = phrase
            evaluated = validate_post083_frontier_selection_gate(record, used_selection_ids=set())
            self.assertEqual(evaluated["review_status"], BLOCKED, phrase)
            self.assertTrue(
                any("frontier" in error.casefold() or "stale" in error.casefold() for error in evaluated["validation_errors"]),
                evaluated["validation_errors"],
            )

    def test_whitelisted_lists_still_scan_extra_frontier_and_authority_laundering(self):
        cases = [
            ("frontier_prerequisites", "codexLiveDispatchL3Smoke"),
            ("required_future_approval_fields", "approved%20for%20runtime%20execution"),
            ("hostile_review_checklist", "blkTestFixedToolPilotL3L4"),
            ("governing_docs", "codex%20live%20dispatch%20l3%20smoke"),
        ]
        for field, phrase in cases:
            record = self._record()
            record[field].append(phrase)
            evaluated = validate_post083_frontier_selection_gate(record, used_selection_ids=set())
            self.assertEqual(evaluated["review_status"], BLOCKED, (field, phrase, evaluated["validation_errors"]))
            self.assertTrue(
                any(phrase in error or "governing_docs" in error for error in evaluated["validation_errors"]),
                evaluated["validation_errors"],
            )

    def test_nested_side_effect_boolean_keys_fail_closed(self):
        record = self._record()
        record["decision_evidence"]["side_effects"] = {
            "packageManagerCalled": True,
            "networkCalled": True,
            "modelServiceCalled": True,
            "browserToolingCalled": True,
            "cyberToolingCalled": True,
            "signerKeyAccessed": True,
            "storageWritten": True,
            "ledgerAppended": True,
            "CodexSubprocessStarted": True,
            "sourceMutationAttempted": True,
            "gitMutationAttempted": True,
        }

        evaluated = validate_post083_frontier_selection_gate(record, used_selection_ids=set())

        self.assertEqual(evaluated["review_status"], BLOCKED)
        errors = "\n".join(evaluated["validation_errors"])
        for marker in [
            "packageManagerCalled",
            "networkCalled",
            "modelServiceCalled",
            "browserToolingCalled",
            "cyberToolingCalled",
            "signerKeyAccessed",
            "storageWritten",
            "ledgerAppended",
            "CodexSubprocessStarted",
            "sourceMutationAttempted",
            "gitMutationAttempted",
        ]:
            self.assertIn(marker, errors)

    def test_rtm_authority_request_blocks_until_publication_prerequisites_exist(self):
        record = self._record("rtm_authority_request_after_publication_prerequisites")

        self.assertEqual(record["review_status"], BLOCKED_PENDING_PUBLICATION_PREREQUISITES)
        self.assertTrue(any("publication prerequisites" in error for error in record["validation_errors"]), record["validation_errors"])
        self.assertIs(record["runtime_rtm_generation_authorized"], False)
        self.assertIs(record["rtm_generated"], False)

        caller_claimed_ready = self._record(
            "rtm_authority_request_after_publication_prerequisites",
            publication_prerequisites_satisfied=True,
        )
        self.assertEqual(caller_claimed_ready["review_status"], BLOCKED_PENDING_PUBLICATION_PREREQUISITES)
        self.assertTrue(
            any("later authority-specific sprint" in error for error in caller_claimed_ready["validation_errors"]),
            caller_claimed_ready["validation_errors"],
        )

    def test_authority_laundering_keys_values_and_percent_encoding_fail_closed(self):
        record = self._record()
        record["decision_evidence"]["operator_phrase"] = "approved for publication"
        record["decision_evidence"]["nested"] = {
            "publication_authorized": True,
            "encoded_publication": "%42EO publication authorized",
            "double_encoded_protected": "docs%252Factive/REQ-001.md",
            "compact_rtm": "RTMGeneration greenlit",
            "signer": "SIGNERKEYMATERIAL available",
            "targetRepoMutation": "allowed",
        }

        evaluated = validate_post083_frontier_selection_gate(record, used_selection_ids=set())

        self.assertEqual(evaluated["review_status"], BLOCKED)
        errors = "\n".join(evaluated["validation_errors"])
        for marker in [
            "approved for publication",
            "publication_authorized",
            "%42EO publication authorized",
            "docs%252Factive/REQ-001.md",
            "RTMGeneration greenlit",
            "SIGNERKEYMATERIAL",
            "targetRepoMutation",
        ]:
            self.assertIn(marker, errors)

    def test_tooling_and_isolation_camel_compact_claims_fail_closed(self):
        phrases = [
            "packageManagerIsAuthorized",
            "packageManagerToolingIsAuthorized",
            "packageManagersAreAuthorized",
            "Package manager is authorized.",
            "networkToolingIsAuthorized",
            "networkModelCyberBrowserToolingAuthorized",
            "networkModelCyberBrowserToolingIsAuthorized",
            "networkModelBrowserCyberToolingIsAuthorized",
            "networkModelBrowserCyberTooling%49s%41uthorized",
            "Network tooling is authorized.",
            "modelServiceIsAuthorized",
            "Model service is authorized.",
            "browserToolingIsAuthorized",
            "Browser tooling is authorized.",
            "cyberToolingIsAuthorized",
            "Cyber tooling is authorized.",
            "productionIsolationClaimed",
            "productionIsolationIsClaimed",
            "productionIsolationClaimsAreAuthorized",
            "productionIsolation%49s%43laimed",
            "Production isolation is claimed.",
            "Production isolation claims are authorized.",
        ]
        for phrase in phrases:
            record = self._record()
            record["decision_evidence"]["notes"] = phrase
            evaluated = validate_post083_frontier_selection_gate(record, used_selection_ids=set())
            self.assertEqual(evaluated["review_status"], BLOCKED, phrase)
            self.assertTrue(evaluated["validation_errors"], phrase)

    def test_approval_noun_and_incidental_negative_clause_authority_claims_fail_closed(self):
        phrases = [
            "next logical sprint is approval",
            "next sprint is approval",
            "BLK-083 decision package is publication approval",
            "BLK-083 decision-package readiness is publication approval",
            "Package managers are allowed; no separate ticket recorded",
            "package managers allowed; no separate ticket recorded",
            "packageManagerIsAllowed; no separate ticket recorded",
            "Network tooling is allowed; no separate ticket recorded",
            "network is allowed; no separate ticket recorded",
            "network allowed; no separate ticket recorded",
            "model service allowed; no separate ticket recorded",
            "browser tooling allowed; no separate ticket recorded",
            "cyber tooling allowed; no separate ticket recorded",
            "Production isolation is allowed; no separate ticket recorded",
            "production isolation claim allowed; no separate ticket recorded",
        ]
        for phrase in phrases:
            record = self._record()
            record["decision_evidence"]["notes"] = phrase
            evaluated = validate_post083_frontier_selection_gate(record, used_selection_ids=set())
            self.assertEqual(evaluated["review_status"], BLOCKED, phrase)
            self.assertTrue(evaluated["validation_errors"], phrase)

    def test_structured_key_value_approval_noun_laundering_fails_closed(self):
        cases = [
            ("next_sprint", "approval"),
            ("next logical sprint", "approval"),
            ("next_sprint", "is_approval"),
            ("future sprint", "publication approval"),
            ("next_sprint", ["approval"]),
            ("next_sprint", {"state": "approval"}),
            ("next logical sprint", ["approval"]),
            ("future sprint", ["publication approval"]),
        ]
        for key, value in cases:
            record = self._record()
            record["decision_evidence"][key] = value
            evaluated = validate_post083_frontier_selection_gate(record, used_selection_ids=set())
            self.assertEqual(evaluated["review_status"], BLOCKED, (key, value))
            self.assertTrue(evaluated["validation_errors"], (key, value))

    def test_source_git_mutation_alias_authority_claims_fail_closed(self):
        phrases = [
            "git commit authorized",
            "git push allowed",
            "staging authorized",
            "autofix allowed",
            "source mutation allowed",
            "gitCommitAuthorized",
            "gitPushAllowed",
            "staging%20authorized",
            "autofix%20allowed",
        ]
        for phrase in phrases:
            record = self._record()
            record["decision_evidence"]["notes"] = phrase
            evaluated = validate_post083_frontier_selection_gate(record, used_selection_ids=set())
            self.assertEqual(evaluated["review_status"], BLOCKED, phrase)
            self.assertTrue(evaluated["validation_errors"], phrase)

    def test_required_denied_authority_set_and_side_effect_flags_are_exact(self):
        record = self._record()
        record["excluded_adjacent_authorities"] = record["excluded_adjacent_authorities"][:-1]
        record["excluded_adjacent_authorities"].append("APPROVED_FOR_LIVE_EXECUTION")
        record["publication_pilot_executed"] = True

        evaluated = validate_post083_frontier_selection_gate(record, used_selection_ids=set())

        self.assertEqual(evaluated["review_status"], BLOCKED)
        errors = "\n".join(evaluated["validation_errors"])
        self.assertIn("excluded_adjacent_authorities missing", errors)
        self.assertIn("excluded_adjacent_authorities extra APPROVED_FOR_LIVE_EXECUTION", errors)
        self.assertIn("publication_pilot_executed must be false", errors)
        self.assertIs(evaluated["publication_pilot_executed"], False)

        duplicate = self._record()
        duplicate["excluded_adjacent_authorities"].append(duplicate["excluded_adjacent_authorities"][0])
        evaluated_duplicate = validate_post083_frontier_selection_gate(duplicate, used_selection_ids=set())
        self.assertEqual(evaluated_duplicate["review_status"], BLOCKED)
        self.assertTrue(any("duplicate" in error for error in evaluated_duplicate["validation_errors"]), evaluated_duplicate["validation_errors"])

    def test_selection_replay_blocks_readiness(self):
        record = self._record()
        evaluated = validate_post083_frontier_selection_gate(
            record,
            used_selection_ids={"BLK-SYSTEM-084-POST083-FRONTIER-SELECTION-001"},
        )
        self.assertEqual(evaluated["review_status"], BLOCKED)
        self.assertTrue(any("selection replayed" in error for error in evaluated["validation_errors"]))

    def test_disabled_activation_adapter_has_complete_no_side_effect_surface(self):
        adapter = simulate_disabled_post083_frontier_activation_adapter(self._record())
        self.assertEqual(adapter["adapter_result"], DISABLED)
        expected_false = {
            "publication_approval_captured",
            "publication_pilot_executed",
            "beo_published",
            "signer_key_material_accessed",
            "cryptographic_signing_performed",
            "immutable_storage_written",
            "public_ledger_mutated",
            "rollback_executed",
            "rtm_generated",
            "drift_rejection_performed",
            "blk_test_runtime_started",
            "codex_subprocess_started",
            "blk_pipe_dispatched",
            "target_repo_scanned",
            "target_repo_mutated",
            "source_mutation_attempted",
            "git_mutation_attempted",
            "protected_body_read_attempted",
            "protected_body_copy_attempted",
            "protected_body_scan_attempted",
            "package_manager_called",
            "network_called",
            "model_service_called",
            "browser_tooling_called",
            "cyber_tooling_called",
            "production_isolation_claimed",
        }
        self.assertTrue(expected_false.issubset(adapter), sorted(expected_false - set(adapter)))
        for key in expected_false:
            self.assertIs(adapter[key], False, key)
        for key in DENIED_FLAGS:
            self.assertIn(key, adapter, key)
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
