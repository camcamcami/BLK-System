import ast
import unittest
from pathlib import Path

from blk_target_repo_execution_governance import (
    DENIED_AUTHORITIES,
    GOVERNANCE_STAGES,
    SIDE_EFFECT_FLAGS,
    build_target_repo_execution_governance_record,
    evaluate_target_repo_execution_governance_record,
    validate_target_repo_execution_governance_record,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "blk_target_repo_execution_governance.py"

EXPECTED_STAGES = [
    "request_package",
    "profile_selection",
    "approval_envelope",
    "preflight_refusal",
    "approval_capture",
    "blk_pipe_invocation_boundary",
    "validation_evidence",
    "hostile_audit",
    "target_repo_closeout",
]

EXPECTED_DENIED_AUTHORITIES = [
    "NO_GOVERNANCE_RECORD_RUNTIME_AUTHORITY",
    "NO_TARGET_REPO_SCAN_AUTHORITY",
    "NO_TARGET_REPO_MUTATION_AUTHORITY",
    "NO_BEB_DISPATCH_OR_BEO_CLOSEOUT_AUTHORITY",
    "NO_APPROVAL_ENVELOPE_RETARGETING_AUTHORITY",
    "NO_LIVE_CODEX_EXECUTION_AUTHORITY",
    "NO_BLK_PIPE_EXECUTION_AUTHORITY",
    "NO_PRODUCTION_BLK_TEST_MCP_AUTHORITY",
    "NO_BEO_PUBLICATION_AUTHORITY",
    "NO_RTM_GENERATION_OR_DRIFT_REJECTION_AUTHORITY",
    "NO_PROTECTED_BLK_REQ_BODY_READS",
    "NO_PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING_AUTHORITY",
    "NO_PRODUCTION_SANDBOX_OR_HOST_ISOLATION_CLAIM",
]


class TargetRepoExecutionGovernanceTest(unittest.TestCase):
    def test_default_governance_record_is_review_ready_not_runtime(self):
        record = build_target_repo_execution_governance_record()

        self.assertEqual(record["governance_id"], "blk_system_target_repo_execution_governance_pattern")
        self.assertEqual(record["governance_status"], "TARGET_REPO_EXECUTION_GOVERNANCE_L0_L1_FIXTURE_ONLY")
        self.assertEqual(record["governance_maturity"], "L0_L1_DOCTRINE_FIXTURE_ONLY")
        self.assertEqual(record["evaluation"], "TARGET_REPO_GOVERNANCE_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME")
        self.assertEqual(GOVERNANCE_STAGES, tuple(EXPECTED_STAGES))
        self.assertEqual(record["required_stage_order"], EXPECTED_STAGES)

        identity = record["target_identity"]
        self.assertEqual(identity["target_repo_id"], "kuronode-v1-fixture")
        self.assertEqual(identity["target_branch"], "main")
        self.assertTrue(identity["target_repo_absolute_path"].startswith("/"))
        self.assertRegex(identity["target_head_sha"], r"^[0-9a-f]{40}$")
        self.assertEqual(identity["target_head_sha"], identity["observed_remote_head_sha"])

        profile = record["profile_selection_record"]
        self.assertEqual(profile["selection_status"], "PROFILE_SELECTION_RECORD_REVIEW_ONLY_NOT_RUNTIME_AUTHORITY")
        self.assertEqual(profile["selected_profile_id"], "kuronode-typescript")
        self.assertEqual(profile["selected_profile_source_doc"], "BLK-058")
        self.assertEqual(profile["selected_profile_architecture_doc"], "BLK-078")

        self.assertEqual(validate_target_repo_execution_governance_record(record), [])

    def test_approval_envelope_replay_expiry_and_validation_profiles_are_required_metadata_only(self):
        record = build_target_repo_execution_governance_record()
        approval = record["approval_envelope"]

        self.assertEqual(approval["request_id"], "BLK-SYSTEM-081-TARGET-REPO-GOVERNANCE-REQUEST-FIXTURE")
        self.assertEqual(approval["approval_id"], "FUTURE_EXPLICIT_APPROVAL_REQUIRED_NOT_GRANTED")
        self.assertEqual(approval["run_id"], "FUTURE_ONE_RUN_ID_REQUIRED_NOT_CONSUMED")
        self.assertEqual(approval["replay_policy"], "future_run_id_must_be_one_use_and_durably_recorded")
        self.assertRegex(approval["expires_at_utc"], r"^2099-01-01T00:00:00Z$")

        boundaries = record["target_boundaries"]
        self.assertIn("src/**/*.ts", boundaries["source_allowlist"])
        self.assertIn(".git/**", boundaries["protected_denylist"])
        self.assertIn("kuronode-power-of-ten-static", boundaries["validation_profiles"])
        self.assertIn("kuronode-typecheck-strict", boundaries["validation_profiles"])

        for broken_key in ["request_id", "approval_id", "run_id", "expires_at_utc", "replay_policy"]:
            broken = build_target_repo_execution_governance_record()
            broken["approval_envelope"].pop(broken_key)
            errors = validate_target_repo_execution_governance_record(broken)
            self.assertTrue(any(broken_key in error for error in errors), (broken_key, errors))

    def test_target_identity_and_profile_selection_fail_closed_when_stale_or_promoted(self):
        bad_records = []

        relative_path = build_target_repo_execution_governance_record()
        relative_path["target_identity"]["target_repo_absolute_path"] = "relative/Kuronode-v1"
        bad_records.append(("absolute_path", relative_path))

        head_mismatch = build_target_repo_execution_governance_record()
        head_mismatch["target_identity"]["observed_remote_head_sha"] = "b" * 40
        bad_records.append(("observed_remote_head_sha", head_mismatch))

        bad_profile = build_target_repo_execution_governance_record()
        bad_profile["profile_selection_record"]["selection_status"] = "PROFILE_SELECTION_APPROVED_FOR_RUNTIME"
        bad_records.append(("profile_selection_record", bad_profile))

        promoted_profile = build_target_repo_execution_governance_record()
        promoted_profile["profile_selection_record"]["target_repo_scan_authorized"] = True
        bad_records.append(("target_repo_scan_authorized", promoted_profile))

        for marker, record in bad_records:
            errors = validate_target_repo_execution_governance_record(record)
            evaluated = evaluate_target_repo_execution_governance_record(record)
            self.assertTrue(any(marker in error for error in errors), (marker, errors))
            self.assertEqual(evaluated["evaluation"], "TARGET_REPO_GOVERNANCE_BLOCKED")
            for flag in SIDE_EFFECT_FLAGS:
                self.assertIs(evaluated[flag], False, flag)

    def test_denied_authorities_and_side_effect_flags_are_exact(self):
        self.assertEqual(DENIED_AUTHORITIES, tuple(EXPECTED_DENIED_AUTHORITIES))

        bad_sets = [
            EXPECTED_DENIED_AUTHORITIES[:-1],
            EXPECTED_DENIED_AUTHORITIES + ["APPROVED_FOR_LIVE_EXECUTION"],
            EXPECTED_DENIED_AUTHORITIES + [EXPECTED_DENIED_AUTHORITIES[0]],
            EXPECTED_DENIED_AUTHORITIES[:-1] + [{"bad": True}],
        ]
        for bad_set in bad_sets:
            record = build_target_repo_execution_governance_record()
            record["denied_authorities"] = list(bad_set)
            errors = validate_target_repo_execution_governance_record(record)
            self.assertTrue(any("denied_authorities" in error for error in errors), (bad_set, errors))

        for flag in SIDE_EFFECT_FLAGS:
            record = build_target_repo_execution_governance_record()
            record[flag] = True
            errors = validate_target_repo_execution_governance_record(record)
            self.assertTrue(any(flag in error for error in errors), (flag, errors))

    def test_authority_laundering_fails_closed_in_allowed_strings_and_nested_fields(self):
        phrases = [
            "not runtime approval; APPROVED_FOR_LIVE_EXECUTION",
            "profile selection grants runtime authority",
            "approval envelope retargeting is allowed",
            "target repo scan authorized",
            "target repo mutation authorized",
            "BEB dispatch authorized",
            "BEO closeout execution authorized",
            "Live Codex execution authorized",
            "BLK-pipe execution authorized",
            "Production BLK-test MCP is authorized",
            "authoritativeBEOpublication",
            "publishBEO",
            "RTMGeneration",
            "RTM drift rejection authorized",
            "Protected BLK-req body reads are authorized",
            "Package manager tooling is authorized",
            "Production sandbox is enforced",
        ]
        for phrase in phrases:
            record = build_target_repo_execution_governance_record()
            record["hostile_review_checklist"].append(phrase)
            record["target_boundaries"]["notes"] = {"nested": phrase}

            errors = validate_target_repo_execution_governance_record(record)
            evaluated = evaluate_target_repo_execution_governance_record(record)

            self.assertTrue(errors, phrase)
            self.assertEqual(evaluated["evaluation"], "TARGET_REPO_GOVERNANCE_BLOCKED")
            self.assertFalse(evaluated["target_repo_scan_authorized"])
            self.assertFalse(evaluated["target_repo_mutation_authorized"])
            self.assertFalse(evaluated["beo_publication_authorized"])
            self.assertFalse(evaluated["rtm_generation_authorized"])

    def test_command_shaped_validation_profiles_and_unknown_fields_fail_closed(self):
        bad_profile_names = [
            "npm install",
            "curl https://example.invalid/profile",
            "node -e console.log(1)",
            "python scripts/scan.py",
            "go get example.com/tool",
            "bash -lc scan",
            "http://example.invalid/check",
        ]
        for bad_name in bad_profile_names:
            record = build_target_repo_execution_governance_record()
            record["target_boundaries"]["validation_profiles"].append(bad_name)
            errors = validate_target_repo_execution_governance_record(record)
            self.assertTrue(any("validation_profiles" in error for error in errors), (bad_name, errors))

        record = build_target_repo_execution_governance_record()
        record["target_identity"]["live_scan_authorized"] = True
        record["unexpected_runtime_authority"] = True
        errors = validate_target_repo_execution_governance_record(record)
        self.assertTrue(any("unsupported key" in error for error in errors), errors)
        self.assertTrue(any("live_scan_authorized" in error for error in errors), errors)
        self.assertTrue(any("unexpected_runtime_authority" in error for error in errors), errors)

    def test_module_contains_no_live_surface_imports_or_calls(self):
        tree = ast.parse(MODULE.read_text())
        forbidden_imports = {"subprocess", "socket", "requests", "urllib", "http", "git", "os", "pathlib"}
        forbidden_calls = {"eval", "exec", "__import__", "compile", "open", "system", "popen"}
        offenders = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name.split(".")[0] for alias in node.names]
                offenders.extend(name for name in names if name in forbidden_imports)
            if isinstance(node, ast.ImportFrom):
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
