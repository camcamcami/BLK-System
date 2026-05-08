import unittest
from pathlib import Path

from blk_operator_observability_fixtures import (
    FAILURE_CLASS_ORDER,
    build_health_check_escalation_package,
    build_operator_escalation_package,
    build_operator_status_fixture,
)

ROOT = Path(__file__).resolve().parents[1]
BLK031 = ROOT / "docs" / "BLK-031_operator-ux-observability-runbook-boundary.md"
IMPLEMENTATION = ROOT / "python" / "blk_operator_observability_fixtures.py"

HASH_A = "sha256:" + "a" * 64
HASH_B = "sha256:" + "b" * 64
HASH_C = "sha256:" + "c" * 64


def base_report(failure_class="INVALID_PAYLOAD", **overrides):
    report = {
        "failure_class": failure_class,
        "source_report_id": "REPORT-001",
        "beb_id": "BEB-028-001",
        "trace_artifacts": [
            {"kind": "REQ", "id": "REQ-001", "version_hash": HASH_A},
            {"kind": "UC", "id": "UC-001", "version_hash": HASH_B},
        ],
        "raw_evidence_ref": "operator-supplied:reports/REPORT-001.json",
        "raw_evidence_hash": HASH_C,
        "evidence_excerpt": "payload rejected before execution because validation_profile is missing",
        "retry_count": 1,
        "failure_ceiling": 3,
        "reverted": False,
        "dirty": False,
        "command_executed": False,
        "file_read": False,
        "network_called": False,
        "source_mutated": False,
        "approval_captured": False,
        "beo_published": False,
        "rtm_generated": False,
        "drift_decision_made": False,
        "protected_body_read": False,
        "active_vault_scanned": False,
    }
    report.update(overrides)
    return report


def health_result(profile_id="git_status_short_branch", status="PASS_ADVISORY_ONLY", **overrides):
    argv_by_profile = {
        "git_status_short_branch": ["/usr/bin/git", "status", "--short", "--branch"],
        "active_doctrine_gate": [
            "/usr/bin/python3",
            "-m",
            "unittest",
            "python.test_active_doctrine_review_gates",
        ],
        "python_unittest_discovery": [
            "/usr/bin/python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            "python",
            "-p",
            "test_*.py",
        ],
        "go_test_all": ["/home/dad/.local/bin/go", "test", "./..."],
        "go_vet_all": ["/home/dad/.local/bin/go", "vet", "./..."],
    }
    result = {
        "runner_status": "HEALTH_CHECK_RUNNER_PILOT_ADVISORY_ONLY",
        "execution_status": "HEALTH_CHECK_EXECUTED_LOCAL_FIXED_PROFILE",
        "profile_id": profile_id,
        "classification": "ADVISORY_ONLY",
        "argv": argv_by_profile.get(profile_id, ["/usr/bin/git", "status", "--short", "--branch"]),
        "cwd": "/home/dad/BLK-System",
        "status": status,
        "exit_code": 0 if status == "PASS_ADVISORY_ONLY" else 1,
        "stdout_excerpt": "## main...origin/main",
        "stderr_excerpt": "",
        "evidence_hash": HASH_A,
        "raw_output_embedded": False,
        "redaction_applied": False,
        "health_check_pass_grants_authority": False,
        "shell_used": False,
        "command_executed": True,
        "subprocess_started": True,
        "workspace_mode": "source_repo",
        "execution_workspace": "SOURCE_REPOSITORY",
        "side_effect_observation_scope": "GIT_STATUS_AND_REPO_CACHE_AND_RUNNER_TEMP_ONLY",
        "workspace_status_changed": False,
        "source_repo_status_changed": False,
        "source_repo_cache_artifacts_changed": False,
        "network_called": "NOT_MEASURED_BY_PILOT",
        "package_manager_called": "NOT_MEASURED_BY_PILOT",
        "git_mutated": "NO_WORKSPACE_STATUS_CHANGE_OBSERVED",
        "source_mutated": "NOT_MEASURED_BY_PILOT",
        "approval_captured": False,
        "protected_body_read": "NOT_MEASURED_BY_PILOT",
        "active_vault_scanned": "NOT_MEASURED_BY_PILOT",
        "beo_published": "NOT_MEASURED_BY_PILOT",
        "rtm_generated": "NOT_MEASURED_BY_PILOT",
        "drift_decision_made": "NOT_MEASURED_BY_PILOT",
        "production_sandbox_enforced": "NOT_ENFORCED_BY_PILOT",
        "network_firewall_enforced": "NOT_ENFORCED_BY_PILOT",
        "host_secret_isolation_enforced": "NOT_ENFORCED_BY_PILOT",
        "production_authority_granted": False,
    }
    result.update(overrides)
    return result


class OperatorStatusFixtureTest(unittest.TestCase):
    def test_classifies_each_runbook_failure_surface_with_no_authority(self):
        expected = {
            "INVALID_PAYLOAD": ("BLK-pipe", "Blocked before execution: invalid payload"),
            "UNAUTHORIZED_MUTATION": ("BLK-pipe", "Blocked and reverted: unauthorized mutation"),
            "VALIDATION_FAILED": ("BLK-pipe", "Blocked after mutation: validation failed"),
            "OUTPUT_FLOOD": ("BLK-pipe", "Blocked: output limit exceeded"),
            "INVALID_REVERT_ANCHOR": ("BLK-pipe", "Blocked: revert anchor mismatch"),
            "DIRTY_WORKSPACE": ("BLK-pipe", "Blocked: workspace is dirty"),
            "MISSING_APPROVAL": ("Human gate", "Blocked: missing approval"),
            "STALE_OR_REPLAYED_APPROVAL": ("Human gate", "Blocked: approval stale or replayed"),
            "PROTECTED_VAULT_REQUEST": ("BLK-req", "Blocked: protected BLK-req vault access denied"),
            "DISABLED_BLK_TEST": ("BLK-test", "Blocked: BLK-test transport disabled"),
            "DRAFT_ONLY_BEO": ("BEO", "Advisory only: BEO remains draft-only"),
            "RTM_NOT_GENERATED": ("blk-link", "Advisory only: RTM not generated"),
            "UNKNOWN_OR_MALFORMED_REPORT": ("Observability", "Blocked: report is unknown or malformed"),
        }
        self.assertEqual(FAILURE_CLASS_ORDER, list(expected))
        for failure_class, (domain, phrase) in expected.items():
            with self.subTest(failure_class=failure_class):
                overrides = {}
                if failure_class == "UNAUTHORIZED_MUTATION":
                    overrides["reverted"] = True
                if failure_class == "DIRTY_WORKSPACE":
                    overrides["dirty"] = True
                fixture = build_operator_status_fixture(
                    base_report(failure_class, **overrides), fixture_id=f"OBS-{failure_class}"
                )
                self.assertEqual(fixture["fixture_id"], f"OBS-{failure_class}")
                self.assertEqual(fixture["status_fixture"], "OPERATOR_OBSERVABILITY_FIXTURE_ONLY")
                self.assertEqual(fixture["authority"], "OBSERVABILITY_ONLY_NOT_EXECUTION")
                self.assertEqual(fixture["failure_class"], failure_class)
                self.assertEqual(fixture["owning_domain"], domain)
                self.assertEqual(fixture["concise_status"], phrase)
                self.assertTrue(fixture["human_decision_required"])
                self.assertFalse(fixture["command_executed"])
                self.assertFalse(fixture["file_read"])
                self.assertFalse(fixture["network_called"])
                self.assertFalse(fixture["source_mutated"])
                self.assertFalse(fixture["approval_captured"])
                self.assertFalse(fixture["beo_published"])
                self.assertFalse(fixture["rtm_generated"])
                self.assertFalse(fixture["drift_decision_made"])
                self.assertFalse(fixture["protected_body_read"])
                self.assertFalse(fixture["active_vault_scanned"])

    def test_preserves_trace_and_bounded_evidence_identity_without_raw_log_flood(self):
        report = base_report(
            "OUTPUT_FLOOD",
            evidence_excerpt="X" * 1000,
            raw_evidence_ref="operator-supplied:reports/flood.log",
        )
        fixture = build_operator_status_fixture(report, fixture_id="OBS-FLOOD", excerpt_max_chars=80)

        self.assertEqual(fixture["raw_evidence_ref"], "operator-supplied:reports/flood.log")
        self.assertEqual(fixture["raw_evidence_hash"], HASH_C)
        self.assertEqual(fixture["trace_artifacts"], report["trace_artifacts"])
        self.assertLessEqual(len(fixture["bounded_evidence_excerpt"]), 80)
        self.assertTrue(fixture["bounded_evidence_excerpt"].endswith("..."))
        self.assertEqual(fixture["evidence_inline_bounded"], True)
        self.assertEqual(fixture["raw_evidence_embedded"], False)

    def test_sets_retry_revert_dirty_indicators_explicitly(self):
        fixture = build_operator_status_fixture(
            base_report(
                "UNAUTHORIZED_MUTATION",
                retry_count=2,
                failure_ceiling=3,
                reverted=True,
                dirty=True,
            ),
            fixture_id="OBS-MUTATION",
        )

        self.assertEqual(fixture["retry_count"], 2)
        self.assertEqual(fixture["failure_ceiling"], 3)
        self.assertEqual(fixture["failure_ceiling_remaining"], 1)
        self.assertTrue(fixture["reverted"])
        self.assertTrue(fixture["dirty"])
        self.assertEqual(fixture["next_operator_action"], "inspect workspace before retry")

    def test_builds_escalation_package_from_status_fixtures_without_unbounded_logs(self):
        statuses = [
            build_operator_status_fixture(base_report("INVALID_PAYLOAD"), fixture_id="OBS-001"),
            build_operator_status_fixture(
                base_report("RTM_NOT_GENERATED", raw_evidence_hash=HASH_B), fixture_id="OBS-002"
            ),
        ]
        package = build_operator_escalation_package(statuses, package_id="ESC-028-001")

        self.assertEqual(package["package_id"], "ESC-028-001")
        self.assertEqual(package["package_status"], "OPERATOR_ESCALATION_PACKAGE_FIXTURE_ONLY")
        self.assertEqual(package["authority"], "OBSERVABILITY_ONLY_NOT_EXECUTION")
        self.assertEqual(package["status_count"], 2)
        self.assertEqual(package["failure_classes"], ["INVALID_PAYLOAD", "RTM_NOT_GENERATED"])
        self.assertEqual(package["raw_evidence_hashes"], [HASH_C, HASH_B])
        self.assertTrue(package["human_decision_required"])
        self.assertFalse(package["raw_evidence_embedded"])
        self.assertFalse(package["command_executed"])
        self.assertFalse(package["file_read"])
        self.assertFalse(package["network_called"])
        self.assertFalse(package["source_mutated"])
        self.assertFalse(package["approval_captured"])
        self.assertFalse(package["beo_published"])
        self.assertFalse(package["rtm_generated"])
        self.assertFalse(package["drift_decision_made"])
        self.assertFalse(package["protected_body_read"])
        self.assertFalse(package["active_vault_scanned"])

    def test_rejects_unknown_failure_class_and_unsupported_top_level_fields(self):
        with self.assertRaisesRegex(ValueError, "unsupported failure_class"):
            build_operator_status_fixture(base_report("RUNTIME_RTM_GENERATED"), fixture_id="OBS-BAD")
        with self.assertRaisesRegex(ValueError, "unsupported field: unexpected"):
            build_operator_status_fixture(base_report(unexpected="x"), fixture_id="OBS-BAD")

    def test_rejects_authority_laundering_and_protected_nested_fields(self):
        forbidden_cases = [
            {"rtm": {"id": "RTM-001"}},
            {"rtm_status": "GENERATED"},
            {"runtime_rtm_status": "GENERATED"},
            {"generated_rtm_id": "RTM-001"},
            {"publication": {"status": "PUBLISHED"}},
            {"beo_publication": "PUBLISHED"},
            {"publication_status": "PUBLISHED"},
            {"published_beo": "BEO-001"},
            {"signer": {"key_material": "secret"}},
            {"ledger": {"public_mutation": True}},
            {"drift": {"decision": "REJECT"}},
            {"drift_status": "REJECTED"},
            {"drift_rejection_reason": "stale"},
            {"approval_capture": {"approved": True}},
            {"command": "git status"},
            {"body": "REQ text"},
            {"protected_body": "REQ text"},
            {"protected_body_text": "REQ text"},
            {"body_text": "REQ text"},
            {"requirement_body_text": "REQ text"},
            {"path": "docs/active/REQ-001.md"},
            {"path_hint": "docs/active/REQ-001.md"},
            {"protected_path_ref": "docs/active/REQ-001.md"},
            {"active_vault_path_ref": "docs/active/REQ-001.md"},
            {"secret": "token"},
            {"secret_value": "token"},
            {"token_value": "token"},
            {"private_key_ref": "operator-supplied:key"},
        ]
        for nested in forbidden_cases:
            with self.subTest(nested=nested):
                with self.assertRaisesRegex(ValueError, "rejects forbidden field"):
                    build_operator_status_fixture(
                        base_report(trace_artifacts=[{"kind": "REQ", "id": "REQ-001", "version_hash": HASH_A, "meta": nested}]),
                        fixture_id="OBS-BAD",
                    )

    def test_rejects_side_effect_flags_when_true_or_non_bool(self):
        for flag in [
            "command_executed",
            "file_read",
            "network_called",
            "source_mutated",
            "approval_captured",
            "beo_published",
            "rtm_generated",
            "drift_decision_made",
            "protected_body_read",
            "active_vault_scanned",
        ]:
            with self.subTest(flag=flag):
                with self.assertRaisesRegex(ValueError, f"{flag} must be false"):
                    build_operator_status_fixture(base_report(**{flag: True}), fixture_id="OBS-BAD")
                with self.assertRaisesRegex(ValueError, f"{flag} must be false"):
                    build_operator_status_fixture(base_report(**{flag: "false"}), fixture_id="OBS-BAD")

    def test_rejects_malformed_hashes_traces_and_unbounded_excerpt_settings(self):
        with self.assertRaisesRegex(ValueError, "raw_evidence_hash must be sha256"):
            build_operator_status_fixture(base_report(raw_evidence_hash="sha256:bad"), fixture_id="OBS-BAD")
        with self.assertRaisesRegex(ValueError, "version_hash must be sha256"):
            build_operator_status_fixture(
                base_report(trace_artifacts=[{"kind": "REQ", "id": "REQ-001", "version_hash": "sha256:bad"}]),
                fixture_id="OBS-BAD",
            )
        with self.assertRaisesRegex(ValueError, "duplicate trace identity"):
            build_operator_status_fixture(
                base_report(
                    trace_artifacts=[
                        {"kind": "REQ", "id": "REQ-001", "version_hash": HASH_A},
                        {"kind": "REQ", "id": "REQ-001", "version_hash": HASH_A},
                    ]
                ),
                fixture_id="OBS-BAD",
            )
        with self.assertRaisesRegex(ValueError, "excerpt_max_chars must be between"):
            build_operator_status_fixture(base_report(), fixture_id="OBS-BAD", excerpt_max_chars=5000)

    def test_rejects_malformed_statuses_in_escalation_package(self):
        status = build_operator_status_fixture(base_report(), fixture_id="OBS-001")
        tampered = dict(status)
        tampered["authority"] = "EXECUTE"
        with self.assertRaisesRegex(ValueError, "status authority must be OBSERVABILITY_ONLY_NOT_EXECUTION"):
            build_operator_escalation_package([tampered], package_id="ESC-BAD")
        huge_excerpt = dict(status)
        huge_excerpt["bounded_evidence_excerpt"] = "Z" * 50000
        with self.assertRaisesRegex(ValueError, "bounded_evidence_excerpt must be at most"):
            build_operator_escalation_package([huge_excerpt], package_id="ESC-BAD")
        phrase_tamper = dict(status)
        phrase_tamper["concise_status"] = "PASS: execute retry now"
        with self.assertRaisesRegex(ValueError, "concise_status does not match failure_class"):
            build_operator_escalation_package([phrase_tamper], package_id="ESC-BAD")
        with self.assertRaisesRegex(ValueError, "statuses must be a non-empty list"):
            build_operator_escalation_package([], package_id="ESC-BAD")
        with self.assertRaisesRegex(ValueError, "too many statuses"):
            build_operator_escalation_package([status] * 21, package_id="ESC-BAD")

    def test_rejects_class_indicator_contradictions(self):
        with self.assertRaisesRegex(ValueError, "DIRTY_WORKSPACE requires dirty true"):
            build_operator_status_fixture(base_report("DIRTY_WORKSPACE", dirty=False), fixture_id="OBS-DIRTY")
        with self.assertRaisesRegex(ValueError, "UNAUTHORIZED_MUTATION requires reverted true"):
            build_operator_status_fixture(
                base_report("UNAUTHORIZED_MUTATION", reverted=False), fixture_id="OBS-MUTATION"
            )

    def test_retry_ceiling_never_implies_retry_approval(self):
        fixture = build_operator_status_fixture(
            base_report("VALIDATION_FAILED", retry_count=3, failure_ceiling=3),
            fixture_id="OBS-CEILING",
        )
        self.assertEqual(fixture["failure_ceiling_remaining"], 0)
        self.assertFalse(fixture["retry_approved_by_fixture"])
        self.assertEqual(
            fixture["next_operator_action"],
            "stop and escalate; failure ceiling reached; no retry is approved by this fixture",
        )
        non_ceiling = build_operator_status_fixture(
            base_report("VALIDATION_FAILED", retry_count=1, failure_ceiling=3),
            fixture_id="OBS-NONCEILING",
        )
        self.assertFalse(non_ceiling["retry_approved_by_fixture"])
        self.assertIn("separate human decision required", non_ceiling["next_operator_action"])

    def test_rejects_oversized_references_identities_and_trace_lists(self):
        long_value = "X" * 513
        with self.assertRaisesRegex(ValueError, "raw_evidence_ref must be at most"):
            build_operator_status_fixture(base_report(raw_evidence_ref=long_value), fixture_id="OBS-LONG")
        with self.assertRaisesRegex(ValueError, "fixture_id must be at most"):
            build_operator_status_fixture(base_report(), fixture_id="OBS-" + ("X" * 200))
        with self.assertRaisesRegex(ValueError, "source_report_id must be at most"):
            build_operator_status_fixture(base_report(source_report_id=long_value), fixture_id="OBS-LONG")
        with self.assertRaisesRegex(ValueError, "actor_identity must be at most"):
            build_operator_status_fixture(base_report(actor_identity=long_value), fixture_id="OBS-LONG")
        too_many_traces = [
            {"kind": "REQ", "id": f"REQ-{idx:03d}", "version_hash": HASH_A}
            for idx in range(21)
        ]
        with self.assertRaisesRegex(ValueError, "trace_artifacts must contain at most"):
            build_operator_status_fixture(base_report(trace_artifacts=too_many_traces), fixture_id="OBS-LONG")

    def test_builds_health_check_escalation_package_without_raw_output_or_authority(self):
        package = build_health_check_escalation_package(
            [
                health_result("git_status_short_branch", "PASS_ADVISORY_ONLY", evidence_hash=HASH_A),
                health_result(
                    "go_test_all",
                    "FAIL_ADVISORY_ONLY",
                    evidence_hash=HASH_B,
                    stdout_excerpt="FAIL: TestExample",
                    stderr_excerpt="assertion failed",
                ),
                health_result(
                    "active_doctrine_gate",
                    "BLOCKED_ADVISORY_ONLY",
                    evidence_hash=HASH_C,
                    stdout_excerpt="",
                    stderr_excerpt="output limit exceeded",
                    exit_code=None,
                ),
            ],
            package_id="HC-ESC-037-001",
        )

        self.assertEqual(package["package_id"], "HC-ESC-037-001")
        self.assertEqual(package["package_status"], "HEALTH_CHECK_ESCALATION_PACKAGE_ADVISORY_ONLY")
        self.assertEqual(package["authority"], "HEALTH_CHECK_PASS_GRANTS_NO_AUTHORITY")
        self.assertEqual(
            package["profile_ids"], ["git_status_short_branch", "go_test_all", "active_doctrine_gate"]
        )
        self.assertEqual(
            package["advisory_statuses"],
            ["PASS_ADVISORY_ONLY", "FAIL_ADVISORY_ONLY", "BLOCKED_ADVISORY_ONLY"],
        )
        self.assertEqual(
            package["failure_categories"],
            ["ADVISORY_PASS", "FAILED_VERIFICATION_OR_BROKEN_CODE", "POLICY_OR_ENVIRONMENT_BLOCKED"],
        )
        self.assertEqual(package["evidence_hashes"], [HASH_A, HASH_B, HASH_C])
        self.assertEqual(package["exit_codes"], [0, 1, None])
        self.assertTrue(package["human_decision_required"])
        self.assertEqual(
            package["next_operator_action"],
            "inspect failed or blocked health-check evidence; no retry or authority expansion is approved by this package",
        )
        self.assertFalse(package["raw_evidence_embedded"])
        self.assertFalse(package["health_check_pass_grants_authority"])
        self.assertFalse(package["production_authority_granted"])
        self.assertFalse(package["subprocess_started_by_package_helper"])
        self.assertLessEqual(sum(len(v) for v in package["stdout_excerpts"] + package["stderr_excerpts"]), 4000)

    def test_all_pass_health_check_package_is_advisory_without_human_decision(self):
        package = build_health_check_escalation_package(
            [health_result("git_status_short_branch", "PASS_ADVISORY_ONLY", evidence_hash=HASH_A)],
            package_id="HC-ESC-037-PASS",
        )
        self.assertFalse(package["human_decision_required"])
        self.assertEqual(package["failure_categories"], ["ADVISORY_PASS"])
        self.assertEqual(
            package["next_operator_action"],
            "health-check PASS is advisory only; no execution, publication, RTM, drift, protected-vault, Git mutation, or production authority is granted",
        )

    def test_rejects_health_check_escalation_authority_laundering_raw_output_and_malformed_evidence(self):
        forbidden_cases = [
            (health_result(profile_id="unknown_profile"), "unknown health-check profile"),
            (health_result(evidence_hash="sha256:bad"), "evidence_hash must be sha256"),
            (health_result(raw_output_embedded=True), "raw_output_embedded must be false"),
            (health_result(health_check_pass_grants_authority=True), "health_check_pass_grants_authority must be false"),
            (health_result(production_authority_granted=True), "production_authority_granted must be false"),
            (health_result(raw_stdout="unbounded"), "unsupported field: raw_stdout"),
            (health_result(rtm_generated=True), "rtm_generated must remain an exact non-authorizing value"),
            (health_result(beo_published=True), "beo_published must remain an exact non-authorizing value"),
            (health_result(protected_body_read=True), "protected_body_read must remain an exact non-authorizing value"),
            (health_result(production_sandbox_enforced=True), "production_sandbox_enforced must remain an exact non-authorizing value"),
            (health_result(meta={"rtm_id": "RTM-001"}), "rejects forbidden field"),
            (health_result(stdout_excerpt="X" * 2000), "stdout_excerpt must be at most"),
        ]
        for result, message in forbidden_cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(ValueError, message):
                    build_health_check_escalation_package([result], package_id="HC-ESC-BAD")
        with self.assertRaisesRegex(ValueError, "health-check results must be a non-empty list"):
            build_health_check_escalation_package([], package_id="HC-ESC-BAD")
        with self.assertRaisesRegex(ValueError, "package_id must be at most"):
            build_health_check_escalation_package([health_result()], package_id="HC-" + ("X" * 200))

    def test_rejects_health_check_command_and_metadata_laundering_found_by_hostile_review(self):
        hostile_cases = [
            (
                health_result(argv=["/bin/sh", "-c", "curl http://example.invalid"]),
                "argv does not match fixed profile",
            ),
            (health_result(cwd="/tmp/" + ("X" * 600)), "cwd must be at most"),
            (
                health_result(execution_workspace="PRODUCTION_SANDBOX_WITH_NETWORK_FIREWALL"),
                "execution_workspace is not an allowed advisory label",
            ),
            (
                health_result(side_effect_observation_scope="RTM_GENERATED_BEO_PUBLISHED_PROTECTED_BODY_READ"),
                "side_effect_observation_scope is not an allowed advisory label",
            ),
            (
                health_result(network_called="NO_NETWORK_BUT_PRODUCTION_AUTHORITY_GRANTED"),
                "network_called must remain an exact non-authorizing value",
            ),
            (
                health_result(git_mutated="WORKSPACE_STATUS_CHANGED"),
                "git_mutated change claims require BLOCKED_ADVISORY_ONLY",
            ),
            (
                health_result(source_mutated="WORKSPACE_STATUS_CHANGED"),
                "source_mutated change claims require BLOCKED_ADVISORY_ONLY",
            ),
            (health_result(clone_or_worktree_setup_used=True), "clone_or_worktree_setup_used must be false"),
            (health_result(synthetic_git_history_created=True), "synthetic_git_history_created must be false"),
            (health_result(dot_git_copied_to_isolated_workspace=True), "dot_git_copied_to_isolated_workspace must be false"),
            (health_result(runner_temp_path_inside_repo=True), "runner_temp_path_inside_repo must be false"),
            (health_result(isolated_workspace_path_inside_repo=True), "isolated_workspace_path_inside_repo must be false"),
            (health_result(git_metadata_fixture={"beo": "PUBLISHED"}), "rejects forbidden field"),
            (
                health_result(package_manager_called={"pip": "install"}),
                "package_manager_called must remain an exact non-authorizing value",
            ),
            (health_result(stdout_excerpt="GITHUB_TOKEN=abc123"), "health-check result contains secret-looking value"),
            (health_result(cwd="/protected/vault/path/REQ-001.md"), "cwd contains forbidden authority text"),
            (health_result(cwd="/tmp/GITHUB_TOKEN=abc"), "health-check result contains secret-looking value"),
            (health_result(classification="BEO_PUBLISHED"), "classification is not an allowed advisory label"),
            (health_result(workspace_status_changed=True), "workspace_status_changed change claims require BLOCKED_ADVISORY_ONLY"),
            (health_result(repo_cache_artifacts=["GITHUB_TOKEN=abc"]), "health-check result contains secret-looking value"),
            (
                health_result("go_test_all", argv=["/usr/bin/python3", "test", "./..."]),
                "argv executable does not match fixed profile",
            ),
            (
                health_result(
                    "git_status_short_branch",
                    argv=["/usr/bin/git", "--git-dir", "/tmp/other/.git", "--work-tree", "/tmp/other", "status", "--short", "--branch"],
                ),
                "argv Git-metadata paths do not match BLK-System source repository",
            ),
            (
                health_result(git_metadata_fixture={"safe": "GITHUB_TOKEN=abc"}),
                "health-check result contains secret-looking value",
            ),
        ]
        for result, message in hostile_cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(ValueError, message):
                    build_health_check_escalation_package([result], package_id="HC-ESC-HOSTILE")

    def test_rejects_health_check_package_total_excerpt_flood(self):
        results = [
            health_result("git_status_short_branch", evidence_hash=HASH_A, stdout_excerpt="X" * 1000),
            health_result("go_test_all", evidence_hash=HASH_B, stdout_excerpt="Y" * 1000),
            health_result("go_vet_all", evidence_hash=HASH_C, stdout_excerpt="Z" * 1000),
            health_result("active_doctrine_gate", evidence_hash=HASH_A, stdout_excerpt="A" * 1000),
            health_result("python_unittest_discovery", evidence_hash=HASH_B, stdout_excerpt="B"),
        ]
        with self.assertRaisesRegex(ValueError, "health-check package excerpts exceed total size limit"):
            build_health_check_escalation_package(results, package_id="HC-ESC-FLOOD")

    def test_blk031_boundary_doc_pins_track_i_no_authority_runbook_contract(self):
        self.assertTrue(BLK031.exists(), "BLK-031 operator observability boundary missing")
        text = BLK031.read_text()
        required = [
            "Operator UX / observability runbook boundary",
            "Active fixture/runbook boundary contract — not execution authority",
            "Track I — Operator UX, observability, and escalation",
            "OPERATOR_OBSERVABILITY_FIXTURE_ONLY",
            "OPERATOR_ESCALATION_PACKAGE_FIXTURE_ONLY",
            "OBSERVABILITY_ONLY_NOT_EXECUTION",
            "invalid payload",
            "unauthorized mutation",
            "validation failed",
            "output limit exceeded",
            "revert anchor mismatch",
            "workspace is dirty",
            "missing approval",
            "approval stale or replayed",
            "protected BLK-req vault access denied",
            "BLK-test transport disabled",
            "BEO remains draft-only",
            "RTM not generated",
            "unknown or malformed",
            "does not run live health checks",
            "does not execute commands",
            "does not inspect files",
            "does not read protected BLK-req vault bodies",
            "does not authorize production BLK-test MCP",
            "does not authorize authoritative BEO publication",
            "does not authorize RTM generation",
            "does not authorize RTM drift rejection",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-031 markers missing: {missing}")

    def test_implementation_has_no_live_execution_network_or_file_scan_surface(self):
        text = IMPLEMENTATION.read_text()
        forbidden = [
            "import subprocess",
            "from subprocess",
            "import socket",
            "import requests",
            "import urllib",
            "os.system",
            "Popen",
            "shell=True",
            "eval(",
            "exec(",
            "__import__",
            "open(",
            "Path.read_text",
            "git ",
            "discord",
            "github",
        ]
        offenders = [marker for marker in forbidden if marker in text]
        self.assertEqual(offenders, [], f"implementation exposes live surface markers: {offenders}")


if __name__ == "__main__":
    unittest.main()
