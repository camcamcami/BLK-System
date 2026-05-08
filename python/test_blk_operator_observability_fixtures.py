import unittest
from pathlib import Path

from blk_operator_observability_fixtures import (
    FAILURE_CLASS_ORDER,
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
                fixture = build_operator_status_fixture(
                    base_report(failure_class), fixture_id=f"OBS-{failure_class}"
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
            {"publication": {"status": "PUBLISHED"}},
            {"signer": {"key_material": "secret"}},
            {"ledger": {"public_mutation": True}},
            {"drift": {"decision": "REJECT"}},
            {"approval_capture": {"approved": True}},
            {"command": "git status"},
            {"body": "REQ text"},
            {"path": "docs/active/REQ-001.md"},
            {"secret": "token"},
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
        with self.assertRaisesRegex(ValueError, "statuses must be a non-empty list"):
            build_operator_escalation_package([], package_id="ESC-BAD")

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
