import hashlib
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from beo_publication_candidate_fixtures import build_beo_publication_candidate_fixture
from rtm_hash_only_metadata_path_fixtures import build_rtm_hash_only_metadata_path_fixture

ROOT = Path(__file__).resolve().parents[1]
BLK027 = ROOT / "docs" / "BLK-027_rtm-hash-only-metadata-path-boundary.md"
TRACE_ARTIFACTS = [
    {
        "kind": "REQ",
        "id": "REQ-S24-HASH-001",
        "version_hash": "sha256:" + "a" * 64,
    },
    {
        "kind": "UC",
        "id": "UC-S24-HASH-001",
        "version_hash": "sha256:" + "b" * 64,
    },
]


def canonical_fixture_hash(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


class RtmHashOnlyMetadataPathFixtureTest(unittest.TestCase):
    def _draft_beo(self, **overrides):
        draft = {
            "beo_id": "BEO_S24_DRAFT_001",
            "beb_id": "BEB_S24_SYNTHETIC",
            "status": "PASS",
            "source": "blk-test-mcp-first-live-smoke",
            "commit_hash": "synthetic-fixture-no-git-commit",
            "pre_engine_hash": "sha256:" + "c" * 64,
            "trace_artifacts": list(TRACE_ARTIFACTS),
            "live_smoke_replay": {
                "run_id": "BLK-SYSTEM-014-SMOKE-001",
                "tool_name": "run_ast_validation",
                "approval_record_hash": "sha256:" + "d" * 64,
                "authorization_request_hash": "sha256:" + "e" * 64,
                "source_evidence_hash": "sha256:" + "f" * 64,
                "transcript_hash": "sha256:" + "1" * 64,
                "cleanup_status": "CLEANED",
            },
            "beo_publication": "DRAFT_ONLY",
            "rtm_status": "NOT_GENERATED",
            "active_vault_read": False,
        }
        draft.update(overrides)
        return draft

    def _publication_approval(self, draft=None):
        if draft is None:
            draft = self._draft_beo()
        return {
            "approval_record_hash": "sha256:" + "2" * 64,
            "authorization_request_hash": "sha256:" + "3" * 64,
            "operator_identity": "discord:684235178083745819",
            "approval_scope": "BEO_PUBLICATION_CANDIDATE_FIXTURE_ONLY",
            "approval_timestamp": "2026-05-08T07:52:00+10:00",
            "approved_beo_id": draft["beo_id"],
            "approved_beo_hash": canonical_fixture_hash(draft),
            "expired": False,
            "replayed": False,
            "stale": False,
        }

    def _candidate(self, draft=None, **overrides):
        if draft is None:
            draft = self._draft_beo()
        candidate = build_beo_publication_candidate_fixture(
            draft,
            candidate_id="BEO-PUB-CANDIDATE-S24-001",
            publication_approval=self._publication_approval(draft),
            signer_fixture={
                "signer_identity": "fixture-signer:S24",
                "signer_policy_hash": "sha256:" + "4" * 64,
                "key_material_accessed": False,
                "signature_generated": False,
                "kms_called": False,
                "secret_read": False,
            },
            storage_fixture={
                "storage_target_identity": "fixture-storage:S24",
                "storage_policy_hash": "sha256:" + "5" * 64,
                "immutable_storage_written": False,
                "storage_write_attempted": False,
            },
            ledger_fixture={
                "ledger_target_identity": "fixture-ledger:S24",
                "ledger_policy_hash": "sha256:" + "6" * 64,
                "public_ledger_mutated": False,
                "ledger_append_attempted": False,
            },
            rollback_fixture={
                "rollback_policy_hash": "sha256:" + "7" * 64,
                "rollback_fixture_identity": "fixture-rollback:S24",
                "rollback_executed": False,
                "revocation_executed": False,
                "supersession_executed": False,
            },
        )
        candidate.update(overrides)
        return candidate

    def _metadata_records(self, **first_override):
        records = [
            {
                "kind": "REQ",
                "id": "REQ-S24-HASH-001",
                "version_hash": "sha256:" + "a" * 64,
                "metadata_source": "ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY",
                "body_included": False,
                "body_read": False,
            },
            {
                "kind": "UC",
                "id": "UC-S24-HASH-001",
                "version_hash": "sha256:" + "b" * 64,
                "metadata_source": "ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY",
                "body_included": False,
                "body_read": False,
            },
        ]
        records[0].update(first_override)
        return records

    def _approval(self, candidate=None, **overrides):
        if candidate is None:
            candidate = self._candidate()
        approval = {
            "approval_record_hash": "sha256:" + "8" * 64,
            "authorization_request_hash": "sha256:" + "9" * 64,
            "operator_identity": "discord:684235178083745819",
            "approval_scope": "RTM_HASH_METADATA_PATH_FIXTURE_ONLY",
            "approval_timestamp": "2026-05-08T07:53:00+10:00",
            "approved_candidate_id": candidate["candidate_id"],
            "approved_beo_hash": candidate["beo_hash"],
            "expired": False,
            "replayed": False,
            "stale": False,
        }
        approval.update(overrides)
        return approval

    def _path_fixture(self, candidate=None, metadata_records=None, approval=None):
        if candidate is None:
            candidate = self._candidate()
        if metadata_records is None:
            metadata_records = self._metadata_records()
        if approval is None:
            approval = self._approval(candidate)
        return build_rtm_hash_only_metadata_path_fixture(
            candidate,
            hash_metadata_records=metadata_records,
            rtm_metadata_approval=approval,
            path_id="RTM-HASH-PATH-S24-001",
        )

    def test_hash_metadata_path_preserves_candidate_and_metadata_without_rtm_authority(self):
        candidate = self._candidate()
        fixture = self._path_fixture(candidate)

        self.assertEqual(fixture["path_id"], "RTM-HASH-PATH-S24-001")
        self.assertEqual(fixture["path_status"], "RTM_HASH_METADATA_PATH_FIXTURE_ONLY")
        self.assertEqual(fixture["candidate_id"], candidate["candidate_id"])
        self.assertEqual(fixture["beo_id"], candidate["beo_id"])
        self.assertEqual(fixture["beo_hash"], candidate["beo_hash"])
        self.assertEqual(fixture["beo_status"], "PASS")
        self.assertEqual(fixture["trace_artifacts"], TRACE_ARTIFACTS)
        self.assertEqual(fixture["hash_metadata_records"], self._metadata_records())
        self.assertEqual(fixture["comparison_state"], "NOT_EVALUATED_FIXTURE_ONLY")
        self.assertEqual(fixture["rtm_status"], "NOT_GENERATED")
        self.assertEqual(fixture["beo_publication"], "DRAFT_ONLY")
        self.assertFalse(fixture["published"])
        self.assertFalse(fixture["active_vault_read"])
        self.assertFalse(fixture["protected_body_read"])
        self.assertFalse(fixture["rtm_created"])
        self.assertFalse(fixture["matrix_created"])
        self.assertFalse(fixture["drift_decision_made"])
        self.assertEqual(
            fixture["rtm_metadata_approval"]["approval_scope"],
            "RTM_HASH_METADATA_PATH_FIXTURE_ONLY",
        )
        self.assertNotIn("rtm", fixture)
        self.assertNotIn("rtm_id", fixture)
        self.assertNotIn("coverage_matrix", fixture)

    def test_failed_candidate_evidence_stays_non_success_without_rtm_generation(self):
        candidate = self._candidate(self._draft_beo(status="FAIL"))
        fixture = self._path_fixture(candidate)

        self.assertEqual(fixture["beo_status"], "FAIL")
        self.assertEqual(fixture["comparison_state"], "NOT_EVALUATED_FIXTURE_ONLY")
        self.assertFalse(fixture["rtm_created"])
        self.assertFalse(fixture["matrix_created"])

    def test_hash_metadata_path_rejects_authority_bearing_candidate_inputs(self):
        bad_candidates = [
            {"candidate_status": "PUBLISHED"},
            {"beo_publication": "PUBLISHED"},
            {"rtm_status": "GENERATED"},
            {"published": True},
            {"active_vault_read": True},
            {"protected_body_read": True},
            {"rtm": {}},
            {"rtm_id": "RTM-S24-001"},
            {"coverage_matrix": []},
            {"drift_decision": "ACCEPT"},
        ]
        for override in bad_candidates:
            with self.subTest(override=override):
                with self.assertRaises(ValueError):
                    self._path_fixture(self._candidate(**override))

    def test_hash_metadata_path_rejects_body_bearing_or_malformed_metadata(self):
        bad_records = [
            {"version_hash": "not-sha256"},
            {"metadata_source": "LIVE_ACTIVE_VAULT"},
            {"body_included": True},
            {"body_read": True},
            {"id": ""},
            {"body": "protected text"},
            {"text": "protected text"},
            {"content": "protected text"},
            {"requirement_body": "protected text"},
            {"use_case_body": "protected text"},
        ]
        for override in bad_records:
            records = self._metadata_records(**override)
            with self.subTest(override=override):
                with self.assertRaises(ValueError):
                    self._path_fixture(metadata_records=records)

    def test_hash_metadata_path_rejects_bad_rtm_metadata_approval_fixture(self):
        candidate = self._candidate()
        bad_approvals = [
            {"approval_record_hash": "not-sha256"},
            {"authorization_request_hash": "not-sha256"},
            {"approval_scope": "BEO_PUBLICATION_CANDIDATE_FIXTURE_ONLY"},
            {"approved_candidate_id": "OTHER-CANDIDATE"},
            {"approved_beo_hash": "sha256:" + "0" * 64},
            {"expired": True},
            {"replayed": True},
            {"stale": True},
            {"operator_identity": ""},
            {"approval_timestamp": ""},
        ]
        for override in bad_approvals:
            with self.subTest(override=override):
                with self.assertRaises(ValueError):
                    self._path_fixture(candidate, approval=self._approval(candidate, **override))

    def test_hash_metadata_path_does_not_read_protected_vault_paths(self):
        forbidden = ("docs/active", "docs/requirements", "docs/use_cases")

        def fail_forbidden_read(self_path, *args, **kwargs):
            as_text = str(self_path)
            if any(token in as_text for token in forbidden):
                raise AssertionError(f"forbidden active vault read: {as_text}")
            return ""

        with patch.object(Path, "read_text", fail_forbidden_read):
            fixture = self._path_fixture()

        self.assertFalse(fixture["active_vault_read"])
        self.assertFalse(fixture["protected_body_read"])

    def test_hash_metadata_path_boundary_doc_exists_and_preserves_no_authority(self):
        self.assertTrue(BLK027.exists(), "BLK-027 hash-only metadata path boundary missing")
        text = BLK027.read_text()
        required = [
            "RTM hash-only metadata path boundary",
            "Active fixture boundary contract — not RTM generation authority",
            "Track H — BLK-link offline RTM ledger",
            "RTM_HASH_METADATA_PATH_FIXTURE_ONLY",
            'rtm_status: "NOT_GENERATED"',
            "comparison_state: \"NOT_EVALUATED_FIXTURE_ONLY\"",
            "no RTM generation",
            "no RTM drift rejection authority",
            "no protected BLK-req vault body reads",
            "BEO publication candidates are not published BEOs",
            "hash-only metadata records must not contain protected bodies",
            "future RTM generation requires a later explicit sprint and human approval",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-027 missing markers: {missing}")

    def test_hash_metadata_path_module_has_no_live_side_effect_surfaces(self):
        text = (ROOT / "python" / "rtm_hash_only_metadata_path_fixtures.py").read_text()
        forbidden_markers = [
            "subprocess",
            "socket",
            "requests",
            "urllib",
            "http.client",
            "discord",
            "boto3",
            "google.cloud",
            "azure",
            "storage_writer",
            "ledger_writer",
            "publish_authoritative_beo",
            "active_vault_hash_compare",
        ]
        offenders = [marker for marker in forbidden_markers if marker in text]
        self.assertEqual(offenders, [], f"Sprint 024 implementation introduced live markers: {offenders}")


if __name__ == "__main__":
    unittest.main()
