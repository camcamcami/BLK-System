import hashlib
import json
import unittest
from pathlib import Path

from beo_publication_candidate_fixtures import build_beo_publication_candidate_fixture

ROOT = Path(__file__).resolve().parents[1]
TRACE_ARTIFACTS = [
    {
        "kind": "REQ",
        "id": "REQ-S23-CANDIDATE-001",
        "version_hash": "sha256:" + "a" * 64,
    }
]


def canonical_fixture_hash(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


class BeoPublicationCandidateFixtureTest(unittest.TestCase):
    def _draft_beo(self, **overrides):
        draft = {
            "beo_id": "BEO_S23_DRAFT_001",
            "beb_id": "BEB_S23_SYNTHETIC",
            "status": "PASS",
            "source": "blk-test-mcp-first-live-smoke",
            "commit_hash": "synthetic-fixture-no-git-commit",
            "pre_engine_hash": "sha256:" + "b" * 64,
            "trace_artifacts": list(TRACE_ARTIFACTS),
            "test_summary": {
                "profile": "bounded-live-smoke-short",
                "checks_passed": 1,
                "checks_failed": 0,
            },
            "live_smoke_replay": {
                "run_id": "BLK-SYSTEM-014-SMOKE-001",
                "tool_name": "run_ast_validation",
                "approval_record_hash": "sha256:" + "c" * 64,
                "authorization_request_hash": "sha256:" + "d" * 64,
                "source_evidence_hash": "sha256:" + "e" * 64,
                "transcript_hash": "sha256:" + "f" * 64,
                "cleanup_status": "CLEANED",
            },
            "beo_publication": "DRAFT_ONLY",
            "rtm_status": "NOT_GENERATED",
            "active_vault_read": False,
        }
        draft.update(overrides)
        return draft

    def _approval(self, draft=None, **overrides):
        if draft is None:
            draft = self._draft_beo()
        approval = {
            "approval_record_hash": "sha256:" + "1" * 64,
            "authorization_request_hash": "sha256:" + "2" * 64,
            "operator_identity": "discord:684235178083745819",
            "approval_scope": "BEO_PUBLICATION_CANDIDATE_FIXTURE_ONLY",
            "approval_timestamp": "2026-05-08T07:10:00+10:00",
            "approved_beo_id": draft["beo_id"],
            "approved_beo_hash": canonical_fixture_hash(draft),
            "expired": False,
            "replayed": False,
            "stale": False,
        }
        approval.update(overrides)
        return approval

    def _signer(self, **overrides):
        signer = {
            "signer_identity": "fixture-signer:S23",
            "signer_policy_hash": "sha256:" + "3" * 64,
            "key_material_accessed": False,
            "signature_generated": False,
            "kms_called": False,
            "secret_read": False,
        }
        signer.update(overrides)
        return signer

    def _storage(self, **overrides):
        storage = {
            "storage_target_identity": "fixture-storage:S23",
            "storage_policy_hash": "sha256:" + "4" * 64,
            "immutable_storage_written": False,
            "storage_write_attempted": False,
        }
        storage.update(overrides)
        return storage

    def _ledger(self, **overrides):
        ledger = {
            "ledger_target_identity": "fixture-ledger:S23",
            "ledger_policy_hash": "sha256:" + "5" * 64,
            "public_ledger_mutated": False,
            "ledger_append_attempted": False,
        }
        ledger.update(overrides)
        return ledger

    def _rollback(self, **overrides):
        rollback = {
            "rollback_policy_hash": "sha256:" + "6" * 64,
            "rollback_fixture_identity": "fixture-rollback:S23",
            "rollback_executed": False,
            "revocation_executed": False,
            "supersession_executed": False,
        }
        rollback.update(overrides)
        return rollback

    def _candidate(self, draft=None, **overrides):
        if draft is None:
            draft = self._draft_beo()
        return build_beo_publication_candidate_fixture(
            draft,
            candidate_id=overrides.pop("candidate_id", "BEO-PUB-CANDIDATE-S23-001"),
            publication_approval=overrides.pop("publication_approval", self._approval(draft)),
            signer_fixture=overrides.pop("signer_fixture", self._signer()),
            storage_fixture=overrides.pop("storage_fixture", self._storage()),
            ledger_fixture=overrides.pop("ledger_fixture", self._ledger()),
            rollback_fixture=overrides.pop("rollback_fixture", self._rollback()),
        )

    def test_candidate_fixture_preserves_source_binding_and_denies_side_effects(self):
        draft = self._draft_beo()
        candidate = self._candidate(draft)

        self.assertEqual(candidate["candidate_status"], "PUBLICATION_CANDIDATE_FIXTURE_ONLY")
        self.assertEqual(candidate["candidate_id"], "BEO-PUB-CANDIDATE-S23-001")
        self.assertEqual(candidate["beo_id"], draft["beo_id"])
        self.assertEqual(candidate["beo_hash"], canonical_fixture_hash(draft))
        self.assertEqual(candidate["beb_id"], draft["beb_id"])
        self.assertEqual(candidate["status"], "PASS")
        self.assertEqual(candidate["commit_hash"], draft["commit_hash"])
        self.assertEqual(candidate["pre_engine_hash"], draft["pre_engine_hash"])
        self.assertEqual(candidate["trace_artifacts"], draft["trace_artifacts"])
        self.assertEqual(candidate["beo_publication"], "DRAFT_ONLY")
        self.assertEqual(candidate["rtm_status"], "NOT_GENERATED")
        self.assertFalse(candidate["published"])
        self.assertFalse(candidate["active_vault_read"])
        self.assertFalse(candidate["key_material_accessed"])
        self.assertFalse(candidate["immutable_storage_written"])
        self.assertFalse(candidate["public_ledger_mutated"])
        self.assertFalse(candidate["rollback_executed"])
        self.assertEqual(candidate["publication_approval"]["approval_scope"], "BEO_PUBLICATION_CANDIDATE_FIXTURE_ONLY")
        self.assertEqual(candidate["publication_approval"]["operator_identity"], "discord:684235178083745819")
        self.assertEqual(candidate["signer_fixture"]["signer_identity"], "fixture-signer:S23")
        self.assertEqual(candidate["storage_fixture"]["storage_target_identity"], "fixture-storage:S23")
        self.assertEqual(candidate["ledger_fixture"]["ledger_target_identity"], "fixture-ledger:S23")
        self.assertEqual(candidate["rollback_fixture"]["rollback_fixture_identity"], "fixture-rollback:S23")
        self.assertNotIn("published_at", candidate)
        self.assertNotIn("signature", candidate)
        self.assertNotIn("rtm", candidate)
        self.assertNotIn("coverage_matrix", candidate)

    def test_candidate_fixture_accepts_failed_draft_without_promoting_success(self):
        draft = self._draft_beo(
            status="FAIL",
            test_summary={"profile": "bounded-live-smoke-short", "checks_passed": 0, "checks_failed": 1},
        )
        candidate = self._candidate(draft)

        self.assertEqual(candidate["status"], "FAIL")
        self.assertEqual(candidate["candidate_status"], "PUBLICATION_CANDIDATE_FIXTURE_ONLY")
        self.assertFalse(candidate["published"])

    def test_candidate_fixture_rejects_publication_and_rtm_authority_fields(self):
        forbidden_cases = [
            {"beo_publication": "PUBLISHED"},
            {"rtm_status": "GENERATED"},
            {"rtm": {"id": "RTM-001"}},
            {"rtm_id": "RTM-001"},
            {"requirements": []},
            {"coverage_matrix": []},
            {"coverage_status": "TRACED"},
            {"drift": "NONE"},
            {"drift_decision": "ACCEPT"},
            {"published_at": "2026-05-08T07:10:00+10:00"},
            {"signature": "forbidden"},
            {"ledger_id": "ledger-row"},
            {"publication_authority": True},
        ]
        for override in forbidden_cases:
            with self.subTest(override=override):
                with self.assertRaises(ValueError):
                    self._candidate(self._draft_beo(**override))

    def test_candidate_fixture_rejects_bad_approval_fixture(self):
        draft = self._draft_beo()
        bad_approval_cases = [
            {"approval_record_hash": "not-sha256"},
            {"authorization_request_hash": "not-sha256"},
            {"approval_scope": "CODEX_LIVE"},
            {"approved_beo_id": "OTHER-BEO"},
            {"approved_beo_hash": "sha256:" + "9" * 64},
            {"expired": True},
            {"replayed": True},
            {"stale": True},
            {"operator_identity": ""},
            {"approval_timestamp": ""},
        ]
        for override in bad_approval_cases:
            with self.subTest(override=override):
                with self.assertRaises(ValueError):
                    self._candidate(draft, publication_approval=self._approval(draft, **override))

    def test_candidate_fixture_rejects_side_effect_descriptors(self):
        cases = [
            {"signer_fixture": self._signer(key_material_accessed=True)},
            {"signer_fixture": self._signer(signature_generated=True)},
            {"signer_fixture": self._signer(kms_called=True)},
            {"signer_fixture": self._signer(secret_read=True)},
            {"signer_fixture": self._signer(private_key="forbidden")},
            {"storage_fixture": self._storage(immutable_storage_written=True)},
            {"storage_fixture": self._storage(storage_write_attempted=True)},
            {"ledger_fixture": self._ledger(public_ledger_mutated=True)},
            {"ledger_fixture": self._ledger(ledger_append_attempted=True)},
            {"rollback_fixture": self._rollback(rollback_executed=True)},
            {"rollback_fixture": self._rollback(revocation_executed=True)},
            {"rollback_fixture": self._rollback(supersession_executed=True)},
        ]
        for kwargs in cases:
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):
                    self._candidate(**kwargs)

    def test_candidate_fixture_rejects_non_publishable_evidence_statuses(self):
        for status in [
            "BLOCKED",
            "FATAL_TIMEOUT",
            "FATAL_OUTPUT_FLOOD",
            "TRANSPORT_ERROR",
            "OPERATOR_INTERRUPTED",
            "UNKNOWN",
            "",
        ]:
            with self.subTest(status=status):
                with self.assertRaises(ValueError):
                    self._candidate(self._draft_beo(status=status))

    def test_candidate_fixture_rejects_active_vault_read_and_malformed_hashes(self):
        for override in [
            {"active_vault_read": True},
            {"pre_engine_hash": "not-sha256"},
            {"trace_artifacts": []},
            {"trace_artifacts": [{"kind": "REQ", "id": "REQ-1", "version_hash": "not-sha256"}]},
        ]:
            with self.subTest(override=override):
                with self.assertRaises(ValueError):
                    self._candidate(self._draft_beo(**override))

    def test_candidate_fixture_rejects_malformed_source_evidence_identity(self):
        malformed_replay_cases = [
            {"source_evidence_hash": "not-sha256"},
            {"approval_record_hash": "not-sha256"},
            {"authorization_request_hash": "not-sha256"},
            {"transcript_hash": "not-sha256"},
            {"run_id": ""},
            {"tool_name": ""},
            {"cleanup_status": "DIRTY"},
            {"expired": True},
            {"replayed": True},
            {"stale": True},
        ]
        for replay_override in malformed_replay_cases:
            with self.subTest(replay_override=replay_override):
                draft = self._draft_beo()
                replay = dict(draft["live_smoke_replay"])
                replay.update(replay_override)
                with self.assertRaises(ValueError):
                    self._candidate(self._draft_beo(live_smoke_replay=replay))

    def test_candidate_module_does_not_reference_live_side_effect_surfaces(self):
        source = (ROOT / "python" / "beo_publication_candidate_fixtures.py").read_text()
        forbidden_markers = [
            "subprocess",
            "socket",
            "requests",
            "urllib",
            "http.client",
            "discord",
            "kms",
            "boto3",
            "google.cloud",
            "azure",
            "publish_authoritative_beo",
            "public outcome ledger writer",
            "generate_rtm",
            "coverage_matrix =",
            "beo_publication = \"PUBLISHED\"",
            "beo_publication='PUBLISHED'",
            "private_key",
        ]
        offenders = [marker for marker in forbidden_markers if marker in source]
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
