import unittest
from pathlib import Path
from unittest.mock import patch

from beo_fixture_projection import project_mapped_mcp_response_to_beo
from beo_rtm_interface_fixtures import build_beo_rtm_interface_fixture


TRACE_ARTIFACTS = [
    {
        "kind": "REQ",
        "id": "REQ-001",
        "version_hash": "sha256:" + "a" * 64,
    },
    {
        "kind": "UC",
        "id": "UC-001",
        "version_hash": "sha256:" + "b" * 64,
    },
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
                "metadata_handoff_status": "BLK_REQ_TRACE_METADATA_ONLY",
                "active_vault_read": False,
                "requirements_resolved": False,
                "protected_body_copied": False,
                "beb_dispatch_executed": False,
                "beo_closeout_executed": False,
                "beo_publication_attempted": False,
                "rtm_generation_executed": False,
                "drift_decision_executed": False,
                "signer_storage_ledger_touched": False,
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

    def test_beo_rtm_interface_rejects_top_level_side_effect_laundering_inputs(self):
        side_effect_fields = [
            "active_vault_read",
            "requirements_resolved",
            "protected_body_copied",
            "beb_dispatch_executed",
            "beo_closeout_executed",
            "beo_publication_attempted",
            "rtm_generation_executed",
            "drift_decision_executed",
            "signer_storage_ledger_touched",
            "publication_authority_granted",
            "signature",
            "signer",
            "signer_identity",
            "storage_uri",
            "storage_location",
            "ledger_id",
            "public_ledger_mutation",
            "rollback_plan",
            "rollback_authority",
            "publication_authority",
            "publicLedgerMutation",
            "publicationAuthority",
            "signerIdentity",
            "rtmGenerationExecuted",
            "beoPublicationAttempted",
            "approvedBy",
            "approved%5Fby",
            "coverageMatrix",
            "publishedAt",
            "publishBEO",
            "beoPublicationAuthorized",
            "approvedForPublication",
            "activeVaultHashComparison",
            "generateRTM",
            "protectedBody",
            "protectedBLKReqBody",
            "bodyExcerpt",
            "docsRequirementsActive",
            "docs%2Frequirements%2Factive",
            "activeVaultPath",
            "protectedBodyPath",
            "beoPublication",
            "beopublication",
            "beo%5Fpublication",
            "rtmStatus",
            "rtmstatus",
            "rtm%5Fstatus",
            "publication_status",
            "drift_status",
            "body_text",
            "reqBody",
        ]
        for field in side_effect_fields:
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, "authority field|side-effect field|unsupported"):
                    build_beo_rtm_interface_fixture(
                        draft_beo(**{field: True}), interface_id="BEO_RTM_IFACE_007"
                    )

    def test_beo_rtm_interface_rejects_nested_authority_laundering_inputs(self):
        invalid_cases = [
            {"notes": "approved for publication"},
            {"test_summary": {"operator_note": "BEO publication authorized"}},
            {"evidence": [{"claim": "greenlit signer storage ledger"}]},
            {"metadata": {"rtm": {}}},
            {"metadata": {"approved_by": "human"}},
            {"metadata": {"protectedBody": "The system shall..."}},
            {"driftRejectionExecuted": True},
            {"metadata": {"drift_rejection_executed": True}},
            {"metadata": {"beoPublication": "PUBLISHED"}},
            {"metadata": {"rtmStatus": "GENERATED"}},
            {"blkReqBody": "The system shall do X"},
            {"blk_req_body": "The system shall do X"},
            {"metadata": {"requirementBody": "The system shall do X"}},
            {"metadata": {"body": "The system shall do X"}},
        ]
        for overrides in invalid_cases:
            with self.subTest(overrides=overrides):
                with self.assertRaisesRegex(ValueError, "authority|side-effect|protected"):
                    build_beo_rtm_interface_fixture(
                        draft_beo(**overrides), interface_id="BEO_RTM_IFACE_007"
                    )

    def test_beo_rtm_interface_rejects_laundered_interface_id(self):
        invalid_ids = [
            "publishBEO",
            "approvedForPublication",
            "generateRTM",
            "protectedBody",
            "docs%2Frequirements%2Factive",
            "docs%2525252Frequirements%2525252Factive",
        ]
        for interface_id in invalid_ids:
            with self.subTest(interface_id=interface_id):
                with self.assertRaisesRegex(ValueError, "authority or protected marker"):
                    build_beo_rtm_interface_fixture(
                        draft_beo(), interface_id=interface_id
                    )

    def test_beo_rtm_interface_rejects_body_text_in_output_identifiers(self):
        invalid_cases = [
            {"interface_id": "The%20system%20shall%20do%20X"},
            {"beo_id": "The system shall do X"},
            {"beb_id": "The system shall do X"},
        ]
        for case in invalid_cases:
            fixture = draft_beo(
                beo_id=case.get("beo_id", "BEO_007"),
                beb_id=case.get("beb_id", "BEB_007"),
            )
            with self.subTest(case=case):
                with self.assertRaisesRegex(ValueError, "authority or protected marker"):
                    build_beo_rtm_interface_fixture(
                        fixture,
                        interface_id=case.get("interface_id", "BEO_RTM_IFACE_007"),
                    )

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
                {"kind": "REQ", "id": "REQ-001", "version_hash": "not-sha256"}
            ]
        )

        with self.assertRaisesRegex(ValueError, "version_hash"):
            build_beo_rtm_interface_fixture(beo, interface_id="BEO_RTM_IFACE_007")

    def test_beo_rtm_interface_requires_exact_blk_req_trace_metadata(self):
        invalid_cases = [
            (
                "legacy dry-run id",
                {"kind": "REQ", "id": "REQ-DRY-001", "version_hash": "sha256:" + "a" * 64},
                "trace_artifacts.id must be exact REQ-### or UC-###",
            ),
            (
                "short id",
                {"kind": "REQ", "id": "REQ-1", "version_hash": "sha256:" + "a" * 64},
                "trace_artifacts.id must be exact REQ-### or UC-###",
            ),
            (
                "unsupported kind",
                {"kind": "FEATURE", "id": "REQ-001", "version_hash": "sha256:" + "a" * 64},
                "trace_artifacts.kind must be REQ or UC",
            ),
            (
                "kind id mismatch",
                {"kind": "REQ", "id": "UC-001", "version_hash": "sha256:" + "a" * 64},
                "trace_artifacts.kind must match id prefix",
            ),
            (
                "extra body key",
                {"kind": "REQ", "id": "REQ-001", "version_hash": "sha256:" + "a" * 64, "body": "The protected requirement body."},
                "trace_artifacts rejects unsupported key",
            ),
            (
                "protected path string",
                {"kind": "REQ", "id": "docs/requirements/active/REQ-001.md", "version_hash": "sha256:" + "a" * 64},
                "trace_artifacts.id rejects protected path or body marker",
            ),
            (
                "authority marker string",
                {"kind": "REQ", "id": "REQ-001 publishBEO", "version_hash": "sha256:" + "a" * 64},
                "trace_artifacts.id rejects authority marker",
            ),
        ]

        for label, artifact, error in invalid_cases:
            with self.subTest(label=label):
                with self.assertRaisesRegex(ValueError, error):
                    build_beo_rtm_interface_fixture(
                        draft_beo(trace_artifacts=[artifact]), interface_id="BEO_RTM_IFACE_007"
                    )

    def test_beo_rtm_interface_rejects_duplicate_trace_identity_and_copies_metadata(self):
        source_trace = [
            {"kind": "REQ", "id": "REQ-001", "version_hash": "sha256:" + "a" * 64},
            {"kind": "REQ", "id": "REQ-001", "version_hash": "sha256:" + "b" * 64},
        ]
        with self.assertRaisesRegex(ValueError, "duplicate trace_artifacts identity"):
            build_beo_rtm_interface_fixture(
                draft_beo(trace_artifacts=source_trace), interface_id="BEO_RTM_IFACE_007"
            )

        mutable_trace = [{"kind": "REQ", "id": "REQ-001", "version_hash": "sha256:" + "a" * 64}]
        interface = build_beo_rtm_interface_fixture(
            draft_beo(trace_artifacts=mutable_trace), interface_id="BEO_RTM_IFACE_007"
        )
        mutable_trace[0]["id"] = "UC-001"
        self.assertEqual(interface["trace_artifacts"][0]["id"], "REQ-001")
        self.assertEqual(interface["metadata_handoff_status"], "BLK_REQ_TRACE_METADATA_ONLY")
        self.assertFalse(interface["beo_publication_attempted"])
        self.assertFalse(interface["rtm_generation_executed"])

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
