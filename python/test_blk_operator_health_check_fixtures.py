import unittest
from pathlib import Path

from blk_operator_health_check_fixtures import (
    ALLOWED_HEALTH_CHECK_CANDIDATES,
    build_health_check_escalation_fixture,
    build_health_check_profile_fixture,
    build_health_check_result_fixture,
)

ROOT = Path(__file__).resolve().parents[1]
BLK032 = ROOT / "docs" / "BLK-032_track-i-live-health-check-boundary.md"
IMPLEMENTATION = ROOT / "python" / "blk_operator_health_check_fixtures.py"

HASH_A = "sha256:" + "a" * 64
HASH_B = "sha256:" + "b" * 64

SIDE_EFFECT_FLAGS = [
    "command_executed",
    "subprocess_started",
    "network_called",
    "file_read",
    "git_called",
    "package_manager_called",
    "source_mutated",
    "approval_captured",
    "protected_body_read",
    "active_vault_scanned",
    "beo_published",
    "rtm_generated",
    "drift_decision_made",
]


def base_profile(**overrides):
    profile = {
        "check_id": "GO-TEST",
        "category": "go_toolchain_readiness",
        "classification": "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED",
        "argv": ["go", "test", "./..."],
        "description": "Go unit tests candidate; inert metadata only",
        "expected_evidence_ref": "operator-supplied:future-health/go-test.json",
        "network_denied": True,
        "package_manager_denied": True,
        "protected_vault_denied": True,
        "approval_required_for_execution": True,
    }
    profile.update(overrides)
    return profile


def base_result(**overrides):
    result = {
        "check_id": "GO-TEST",
        "classification": "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED",
        "status": "BLOCKED_NOT_EXECUTED",
        "evidence_ref": "operator-supplied:future-health/go-test.json",
        "evidence_hash": HASH_A,
        "stdout_excerpt": "not executed; profile boundary only",
        "stderr_excerpt": "",
        "exit_code": None,
        "redaction_applied": True,
        "health_check_pass_grants_authority": False,
        "command_executed": False,
        "subprocess_started": False,
        "network_called": False,
        "file_read": False,
        "git_called": False,
        "package_manager_called": False,
        "source_mutated": False,
        "approval_captured": False,
        "protected_body_read": False,
        "active_vault_scanned": False,
        "beo_published": False,
        "rtm_generated": False,
        "drift_decision_made": False,
    }
    result.update(overrides)
    return result


class HealthCheckProfileFixtureTest(unittest.TestCase):
    def test_normalizes_allowed_fixed_argv_candidates_without_execution_authority(self):
        expected = [
            (["go", "test", "./..."], "go_toolchain_readiness", "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED"),
            (["go", "vet", "./..."], "go_vet_readiness", "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED"),
            (
                ["python3", "-m", "unittest", "discover", "python", "test_*.py"],
                "python_unittest_readiness",
                "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED",
            ),
            (
                ["python3", "-m", "unittest", "python.test_active_doctrine_review_gates"],
                "active_doctrine_gate_readiness",
                "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED",
            ),
            (["git", "status", "--short", "--branch"], "git_clean_state_advisory", "ADVISORY_ONLY"),
        ]
        self.assertEqual(ALLOWED_HEALTH_CHECK_CANDIDATES, [item[0] for item in expected])
        for argv, category, classification in expected:
            with self.subTest(argv=argv):
                fixture = build_health_check_profile_fixture(
                    base_profile(argv=argv, category=category, classification=classification),
                    fixture_id=f"HCP-{category}",
                )
                self.assertEqual(fixture["fixture_id"], f"HCP-{category}")
                self.assertEqual(fixture["profile_fixture"], "HEALTH_CHECK_PROFILE_FIXTURE_ONLY")
                self.assertEqual(fixture["boundary_fixture"], "HEALTH_CHECK_BOUNDARY_FIXTURE_ONLY")
                self.assertEqual(fixture["authority"], "HEALTH_CHECK_AUTHORITY_NOT_GRANTED")
                self.assertEqual(fixture["execution_status"], "HEALTH_CHECKS_NOT_EXECUTED")
                self.assertEqual(fixture["argv"], argv)
                self.assertEqual(fixture["classification"], classification)
                self.assertTrue(fixture["approval_required_for_execution"])
                self.assertFalse(fixture["health_check_pass_grants_authority"])
                for flag in SIDE_EFFECT_FLAGS:
                    self.assertFalse(fixture[flag], flag)

    def test_rejects_shell_strings_wrappers_network_package_git_mutation_and_protected_scans(self):
        forbidden_profiles = [
            {"argv": "go test ./..."},
            {"argv": ["bash", "-lc", "go test ./..."]},
            {"argv": ["python3", "-c", "print('health')"]},
            {"argv": ["node", "-e", "console.log('health')"]},
            {"argv": ["curl", "https://example.invalid"]},
            {"argv": ["wget", "https://example.invalid"]},
            {"argv": ["ssh", "host", "true"]},
            {"argv": ["npm", "install"]},
            {"argv": ["pip", "install", "requests"]},
            {"argv": ["uv", "pip", "install", "requests"]},
            {"argv": ["go", "get", "example.invalid/mod"]},
            {"argv": ["git", "commit", "-m", "x"], "category": "git_clean_state_advisory", "classification": "ADVISORY_ONLY"},
            {"argv": ["git", "push"], "category": "git_clean_state_advisory", "classification": "ADVISORY_ONLY"},
            {"argv": ["python3", "-m", "unittest", "discover", "docs/active", "test_*.py"]},
        ]
        for override in forbidden_profiles:
            with self.subTest(override=override):
                with self.assertRaises(ValueError):
                    build_health_check_profile_fixture(base_profile(**override), fixture_id="HCP-BAD")

    def test_rejects_profile_authority_laundering_fields_and_side_effect_claims(self):
        forbidden_nested = [
            {"rtm": {"id": "RTM-001"}},
            {"coverage_matrix": []},
            {"drift_decision": "REJECT"},
            {"publication_status": "PUBLISHED"},
            {"protected_body_text": "REQ body"},
            {"active_vault_path_ref": "docs/active/REQ.md"},
            {"secret_value": "[REDACTED]"},
            {"github_token": "[REDACTED]"},
        ]
        for nested in forbidden_nested:
            with self.subTest(nested=nested):
                with self.assertRaisesRegex(ValueError, "rejects forbidden field"):
                    build_health_check_profile_fixture(base_profile(metadata=nested), fixture_id="HCP-BAD")
        for flag in SIDE_EFFECT_FLAGS:
            with self.subTest(flag=flag):
                with self.assertRaisesRegex(ValueError, f"{flag} must be false"):
                    build_health_check_profile_fixture(base_profile(**{flag: True}), fixture_id="HCP-BAD")


class HealthCheckResultFixtureTest(unittest.TestCase):
    def test_normalizes_bounded_result_without_pass_or_runtime_authority(self):
        fixture = build_health_check_result_fixture(
            base_result(status="PASS_SUPPLIED_BY_CALLER", stdout_excerpt="safe bounded PASS text"),
            fixture_id="HCR-001",
            excerpt_max_chars=24,
        )
        self.assertEqual(fixture["fixture_id"], "HCR-001")
        self.assertEqual(fixture["result_fixture"], "HEALTH_CHECK_RESULT_FIXTURE_ONLY")
        self.assertEqual(fixture["boundary_fixture"], "HEALTH_CHECK_BOUNDARY_FIXTURE_ONLY")
        self.assertEqual(fixture["authority"], "HEALTH_CHECK_AUTHORITY_NOT_GRANTED")
        self.assertEqual(fixture["execution_status"], "HEALTH_CHECKS_NOT_EXECUTED")
        self.assertEqual(fixture["status"], "PASS_SUPPLIED_BY_CALLER")
        self.assertLessEqual(len(fixture["stdout_excerpt"]), 24)
        self.assertEqual(fixture["raw_output_embedded"], False)
        self.assertEqual(fixture["redaction_applied"], True)
        self.assertFalse(fixture["health_check_pass_grants_authority"])
        for flag in SIDE_EFFECT_FLAGS:
            self.assertFalse(fixture[flag], flag)

    def test_rejects_unbounded_output_secrets_unsupported_statuses_and_side_effects(self):
        with self.assertRaisesRegex(ValueError, "excerpt_max_chars"):
            build_health_check_result_fixture(base_result(), fixture_id="HCR-BAD", excerpt_max_chars=4096)
        with self.assertRaisesRegex(ValueError, "stdout_excerpt exceeds"):
            build_health_check_result_fixture(base_result(stdout_excerpt="X" * 5000), fixture_id="HCR-BAD")
        with self.assertRaisesRegex(ValueError, "stderr_excerpt exceeds"):
            build_health_check_result_fixture(base_result(stderr_excerpt="X" * 5000), fixture_id="HCR-BAD")
        for leak in [
            "GITHUB_TOKEN=[REDACTED]",
            "Authorization: Bearer [REDACTED]",
            "Authorization: Basic [REDACTED]",
            "API_KEY=[REDACTED]",
            "apikey=[REDACTED]",
            "api-key: [REDACTED]",
            "AWS_ACCESS_KEY_ID=[REDACTED]",
            "ghp_REDACTEDTOKEN",
            "github_pat_REDACTEDTOKEN",
            "password=[REDACTED]",
            "SECRET=[REDACTED]",
            "SSH_AUTH_SOCK=/tmp/agent.sock",
            ".env contains values",
        ]:
            with self.subTest(leak=leak):
                with self.assertRaisesRegex(ValueError, "secret or environment leakage"):
                    build_health_check_result_fixture(base_result(stdout_excerpt=leak), fixture_id="HCR-BAD")
        with self.assertRaisesRegex(ValueError, "unsupported status"):
            build_health_check_result_fixture(base_result(status="MAYBE_NOT_EXECUTED"), fixture_id="HCR-BAD")
        with self.assertRaisesRegex(ValueError, "health_check_pass_grants_authority must be false"):
            build_health_check_result_fixture(
                base_result(health_check_pass_grants_authority=True), fixture_id="HCR-BAD"
            )
        for flag in SIDE_EFFECT_FLAGS:
            with self.subTest(flag=flag):
                with self.assertRaisesRegex(ValueError, f"{flag} must be false"):
                    build_health_check_result_fixture(base_result(**{flag: True}), fixture_id="HCR-BAD")

    def test_rejects_protected_refs_hidden_commands_and_pass_as_authority_text(self):
        for override in [
            {"expected_evidence_ref": "operator-supplied:docs/active/protected-vault/body.md"},
            {"description": "alias hc='curl https://example.invalid'; go test"},
            {"description": "wrapper runs pip install requests before health"},
            {"metadata": {"alias": "wget https://example.invalid"}},
            {"metadata": {"wrapper": "uv pip install requests"}},
            {"description": "PASS approves publish_authoritative_beo and generate_rtm"},
        ]:
            with self.subTest(profile_override=override):
                with self.assertRaisesRegex(ValueError, "forbidden string content"):
                    build_health_check_profile_fixture(base_profile(**override), fixture_id="HCP-BAD")
        for override in [
            {"evidence_ref": "operator-supplied:docs/active/protected-vault/body.md"},
            {"evidence_ref": "operator-supplied:generate_rtm/result.json"},
            {"stdout_excerpt": "PASS: approved to publish BEO, generate RTM, reject drift"},
        ]:
            with self.subTest(result_override=override):
                with self.assertRaisesRegex(ValueError, "forbidden string content"):
                    build_health_check_result_fixture(base_result(**override), fixture_id="HCR-BAD")

    def test_builds_escalation_fixture_from_results_without_raw_log_flood(self):
        results = [
            build_health_check_result_fixture(base_result(), fixture_id="HCR-001"),
            build_health_check_result_fixture(
                base_result(check_id="PY-UNIT", evidence_hash=HASH_B, stdout_excerpt="python evidence"),
                fixture_id="HCR-002",
            ),
        ]
        package = build_health_check_escalation_fixture(results, package_id="HCE-029-001")
        self.assertEqual(package["package_id"], "HCE-029-001")
        self.assertEqual(package["package_fixture"], "HEALTH_CHECK_ESCALATION_FIXTURE_ONLY")
        self.assertEqual(package["boundary_fixture"], "HEALTH_CHECK_BOUNDARY_FIXTURE_ONLY")
        self.assertEqual(package["authority"], "HEALTH_CHECK_AUTHORITY_NOT_GRANTED")
        self.assertEqual(package["execution_status"], "HEALTH_CHECKS_NOT_EXECUTED")
        self.assertEqual(package["result_count"], 2)
        self.assertEqual(package["result_ids"], ["HCR-001", "HCR-002"])
        self.assertEqual(package["evidence_hashes"], [HASH_A, HASH_B])
        self.assertFalse(package["raw_output_embedded"])
        self.assertFalse(package["health_check_pass_grants_authority"])
        for flag in SIDE_EFFECT_FLAGS:
            self.assertFalse(package[flag], flag)

    def test_rejects_tampered_escalation_results(self):
        result = build_health_check_result_fixture(base_result(), fixture_id="HCR-001")
        tampered = dict(result)
        tampered["authority"] = "EXECUTE_HEALTH_CHECKS"
        with self.assertRaisesRegex(ValueError, "result authority"):
            build_health_check_escalation_fixture([tampered], package_id="HCE-BAD")
        huge = dict(result)
        huge["stdout_excerpt"] = "X" * 5000
        with self.assertRaisesRegex(ValueError, "bounded excerpt"):
            build_health_check_escalation_fixture([huge], package_id="HCE-BAD")


class HealthCheckBoundaryDoctrineTest(unittest.TestCase):
    def test_blk032_boundary_doc_pins_no_live_health_check_authority(self):
        self.assertTrue(BLK032.exists(), "BLK-032 health-check boundary missing")
        text = BLK032.read_text()
        required = [
            "Track I live health-check boundary",
            "Boundary contract — not live health-check authority",
            "HEALTH_CHECK_BOUNDARY_FIXTURE_ONLY",
            "HEALTH_CHECK_PROFILE_FIXTURE_ONLY",
            "HEALTH_CHECK_RESULT_FIXTURE_ONLY",
            "HEALTH_CHECK_ESCALATION_FIXTURE_ONLY",
            "HEALTH_CHECKS_NOT_EXECUTED",
            "HEALTH_CHECK_AUTHORITY_NOT_GRANTED",
            "fixed argv arrays only",
            "does not execute commands",
            "does not start subprocesses",
            "does not call network services",
            "does not run package managers",
            "does not inspect files",
            "does not read protected BLK-req vault bodies",
            "does not scan active-vault paths",
            "does not mutate Git or source state",
            "does not authorize production BLK-test MCP",
            "does not authorize authoritative BEO publication",
            "does not authorize RTM generation",
            "does not authorize RTM drift rejection",
            "health-check PASS remains advisory",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-032 markers missing: {missing}")

    def test_implementation_has_no_live_execution_network_file_or_api_surface(self):
        text = IMPLEMENTATION.read_text()
        forbidden = [
            "import subprocess",
            "from subprocess",
            "import socket",
            "import requests",
            "import urllib",
            "http.client",
            "from pathlib",
            "Path(",
            "read_text",
            "glob(",
            "rglob(",
            "os.system",
            "Popen",
            "shell=True",
            "eval(",
            "exec(",
            "__import__",
            "open(",
            "discord",
            "github",
            "publish_authoritative_beo",
            "generate_rtm",
            "coverage_matrix_generator",
            "drift_decision_runtime",
            "active_vault_scanner",
            "protected_vault_body_reader",
        ]
        offenders = [marker for marker in forbidden if marker in text]
        self.assertEqual(offenders, [], f"health-check implementation introduced live markers: {offenders}")


if __name__ == "__main__":
    unittest.main()
