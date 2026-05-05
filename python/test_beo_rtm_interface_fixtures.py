import unittest
from pathlib import Path
from unittest.mock import patch

from beo_fixture_projection import project_mapped_mcp_response_to_beo
from beo_rtm_interface_fixtures import build_beo_rtm_interface_fixture


TRACE_ARTIFACTS = [
    {
        "kind": "REQ",
        "id": "REQ-DRY-001",
        "version_hash": "sha256:" + "a" * 64,
    }
]
FORBIDDEN_AUTHORITY_FIELDS = {
    "rtm",
    "rtm_id",
    "requirements",
    "coverage_matrix",
    "published_at",
    "approved_by",
}


def draft_beo(**overrides):
    fixture = {
        "beo_id": "BEO_007",
        "beb_id": "BEB_007",
        "status": "PASS",
        "source": "blk-test-mcp-response-shape",
        "commit_hash": "abc123",
        "pre_engine_hash": "def456",
        "trace_artifacts": list(TRACE_ARTIFACTS),
        "test_summary": {"profile": "strict-ci", "checks_passed": 1, "checks_failed": 0},
        "rtm_status": "NOT_GENERATED",
        "beo_publication": "DRAFT_ONLY",
    }
    fixture.update(overrides)
    return fixture


class BeoRtmInterfaceFixtureTest(unittest.TestCase):
    def test_beo_rtm_interface_fixture_preserves_trace_but_generates_no_rtm(self):
        interface = build_beo_rtm_interface_fixture(
            draft_beo(), interface_id="BEO_RTM_IFACE_007"
        )

        self.assertEqual(
            interface,
            {
                "interface_id": "BEO_RTM_IFACE_007",
                "source": "beo-rtm-interface-fixture",
                "beo_id": "BEO_007",
                "beb_id": "BEB_007",
                "beo_status": "PASS",
                "beo_publication": "DRAFT_ONLY",
                "rtm_status": "NOT_GENERATED",
                "rtm_authority": "DISABLED_INTERFACE_ONLY",
                "trace_artifacts": TRACE_ARTIFACTS,
                "active_vault_read": False,
                "requirements_resolved": False,
                "reason": "RTM generation remains disabled; fixture preserves opaque trace metadata only",
            },
        )
        self.assertTrue(FORBIDDEN_AUTHORITY_FIELDS.isdisjoint(interface))

    def test_beo_rtm_interface_accepts_failed_draft_beo_without_promoting_success(self):
        interface = build_beo_rtm_interface_fixture(
            draft_beo(status="FAIL"), interface_id="BEO_RTM_IFACE_007"
        )

        self.assertEqual(interface["beo_status"], "FAIL")
        self.assertEqual(interface["rtm_authority"], "DISABLED_INTERFACE_ONLY")
        self.assertNotIn("coverage_matrix", interface)

    def test_beo_rtm_interface_rejects_authoritative_or_generated_inputs(self):
        invalid_cases = [
            ("beo_publication", draft_beo(beo_publication="PUBLISHED"), "DRAFT_ONLY"),
            ("rtm_status", draft_beo(rtm_status="GENERATED"), "NOT_GENERATED"),
            ("rtm", draft_beo(rtm={}), "generated RTM authority field"),
            ("rtm_id", draft_beo(rtm_id="RTM_007"), "generated RTM authority field"),
            ("requirements", draft_beo(requirements=[]), "generated RTM authority field"),
            (
                "coverage_matrix",
                draft_beo(coverage_matrix={}),
                "generated RTM authority field",
            ),
            ("published_at", draft_beo(published_at="2026-05-05"), "generated RTM authority field"),
            ("approved_by", draft_beo(approved_by="human"), "generated RTM authority field"),
        ]

        for label, beo, error in invalid_cases:
            with self.subTest(label=label):
                with self.assertRaisesRegex(ValueError, error):
                    build_beo_rtm_interface_fixture(beo, interface_id="BEO_RTM_IFACE_007")

    def test_beo_rtm_interface_requires_source_bound_draft_beo_fields(self):
        required_fields = ("beo_id", "beb_id", "status", "pre_engine_hash", "trace_artifacts")

        for field in required_fields:
            beo = draft_beo()
            beo[field] = [] if field == "trace_artifacts" else ""
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, field):
                    build_beo_rtm_interface_fixture(beo, interface_id="BEO_RTM_IFACE_007")

    def test_beo_rtm_interface_requires_non_empty_interface_id(self):
        with self.assertRaisesRegex(ValueError, "interface_id"):
            build_beo_rtm_interface_fixture(draft_beo(), interface_id="")

    def test_beo_rtm_interface_accepts_only_pass_fail_draft_beo_status(self):
        with self.assertRaisesRegex(ValueError, "PASS/FAIL"):
            build_beo_rtm_interface_fixture(
                draft_beo(status="BLOCKED"), interface_id="BEO_RTM_IFACE_007"
            )

    def test_beo_rtm_interface_requires_canonical_trace_artifact_hashes(self):
        beo = draft_beo(
            trace_artifacts=[
                {"kind": "REQ", "id": "REQ-DRY-001", "version_hash": "not-sha256"}
            ]
        )

        with self.assertRaisesRegex(ValueError, "version_hash"):
            build_beo_rtm_interface_fixture(beo, interface_id="BEO_RTM_IFACE_007")

    def test_beo_rtm_interface_does_not_read_active_vault(self):
        forbidden = ("docs/active", "docs/requirements", "docs/use_cases")

        def fail_forbidden_read(self_path, *args, **kwargs):
            as_text = str(self_path)
            if any(token in as_text for token in forbidden):
                raise AssertionError(f"forbidden active vault read: {as_text}")
            return ""

        with patch.object(Path, "read_text", fail_forbidden_read):
            interface = build_beo_rtm_interface_fixture(
                draft_beo(), interface_id="BEO_RTM_IFACE_007"
            )

        self.assertEqual(interface["rtm_status"], "NOT_GENERATED")
        self.assertFalse(interface["active_vault_read"])
        self.assertFalse(interface["requirements_resolved"])

    def test_mapped_mcp_beo_projection_can_feed_rtm_interface_fixture(self):
        mapped = {
            "status": "PASS",
            "source": "blk-test-mcp-response-shape",
            "beb_id": "BEB_007",
            "commit_hash": "abc123",
            "pre_engine_hash": "def456",
            "trace_artifacts": list(TRACE_ARTIFACTS),
            "checks": [
                {
                    "name": "fixture-output-present",
                    "status": "PASS",
                    "summary": "deterministic disabled MCP fixture check",
                }
            ],
        }
        beo = project_mapped_mcp_response_to_beo(mapped, beo_id="BEO_007")
        interface = build_beo_rtm_interface_fixture(
            beo, interface_id="BEO_RTM_IFACE_007"
        )

        self.assertEqual(interface["beo_id"], "BEO_007")
        self.assertEqual(interface["beb_id"], "BEB_007")
        self.assertEqual(interface["beo_status"], "PASS")
        self.assertEqual(interface["trace_artifacts"], TRACE_ARTIFACTS)
        self.assertEqual(interface["rtm_authority"], "DISABLED_INTERFACE_ONLY")


if __name__ == "__main__":
    unittest.main()
