from pathlib import Path
import unittest

from beo_fixture_projection import project_live_smoke_evidence_to_draft_beo

ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / "python"


class BeoPublicationDesignGateTest(unittest.TestCase):
    def _live_smoke_evidence(self, **overrides):
        evidence = {
            "sprint": "BLK-SYSTEM-014",
            "source": "blk-test-mcp-first-live-smoke",
            "run_id": "BLK-SYSTEM-014-SMOKE-001",
            "tool_name": "run_ast_validation",
            "status": "PASS",
            "beb_id": "BEB_S14_SYNTHETIC_SMOKE",
            "commit_hash": "synthetic-fixture-no-git-commit",
            "pre_engine_hash": "sha256:" + "3" * 64,
            "test_profile": "bounded-live-smoke-short",
            "trace_artifacts": [
                {
                    "kind": "REQ",
                    "id": "REQ-S14-SMOKE-001",
                    "version_hash": "sha256:" + "1" * 64,
                }
            ],
            "checks": [
                {
                    "name": "run_ast_validation",
                    "status": "PASS",
                    "summary": "AST validation passed",
                }
            ],
            "approval_record_hash": "sha256:" + "4" * 64,
            "authorization_request_hash": "sha256:" + "5" * 64,
            "source_evidence_hash": "sha256:" + "6" * 64,
            "transcript_hash": "sha256:" + "7" * 64,
            "cleanup_status": "CLEANED",
            "beo_publication": "DRAFT_ONLY",
            "rtm_status": "NOT_GENERATED",
            "active_vault_read": False,
        }
        evidence.update(overrides)
        return evidence

    def test_existing_live_smoke_projection_remains_draft_only(self):
        beo = project_live_smoke_evidence_to_draft_beo(
            self._live_smoke_evidence(),
            beo_id="BEO_S16_GUARD_001",
        )

        self.assertEqual(beo["beo_publication"], "DRAFT_ONLY")
        self.assertEqual(beo["rtm_status"], "NOT_GENERATED")
        self.assertNotIn("published_at", beo)
        self.assertNotIn("signature", beo)
        self.assertNotIn("ledger_id", beo)
        self.assertNotIn("rollback_authority", beo)

    def test_published_runtime_input_still_rejects(self):
        with self.assertRaisesRegex(ValueError, "DRAFT_ONLY"):
            project_live_smoke_evidence_to_draft_beo(
                self._live_smoke_evidence(beo_publication="PUBLISHED"),
                beo_id="BEO_S16_GUARD_002",
            )

    def test_publication_authority_fields_still_reject(self):
        forbidden_fields = (
            "published_at",
            "approved_by",
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
        )
        for field in forbidden_fields:
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, field):
                    project_live_smoke_evidence_to_draft_beo(
                        self._live_smoke_evidence(**{field: "forbidden"}),
                        beo_id="BEO_S16_GUARD_003",
                    )

    def test_rtm_authority_fields_still_reject(self):
        forbidden_fields = (
            "rtm",
            "rtm_id",
            "requirements",
            "coverage_matrix",
            "coverage_status",
            "drift",
            "drift_decision",
        )
        for field in forbidden_fields:
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, field):
                    project_live_smoke_evidence_to_draft_beo(
                        self._live_smoke_evidence(**{field: "forbidden"}),
                        beo_id="BEO_S16_GUARD_004",
                    )

    def test_production_python_does_not_define_beo_publisher(self):
        forbidden = [
            "publish_authoritative_beo",
            "public outcome ledger writer",
            "beo_publication = \"PUBLISHED\"",
            "beo_publication='PUBLISHED'",
        ]
        offenders = []
        for path in PYTHON.glob("*.py"):
            if path.name.startswith("test_"):
                continue
            text = path.read_text()
            for marker in forbidden:
                if marker in text:
                    offenders.append(f"{path.relative_to(ROOT)}: {marker}")
        self.assertEqual(offenders, [], f"Sprint 016 introduced runtime publisher markers: {offenders}")

    def test_active_vault_read_flag_still_rejects(self):
        with self.assertRaisesRegex(ValueError, "active_vault_read"):
            project_live_smoke_evidence_to_draft_beo(
                self._live_smoke_evidence(active_vault_read=True),
                beo_id="BEO_S16_GUARD_005",
            )


if __name__ == "__main__":
    unittest.main()
