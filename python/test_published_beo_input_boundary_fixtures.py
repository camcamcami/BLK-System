import hashlib
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from beo_publication_candidate_fixtures import build_beo_publication_candidate_fixture
from published_beo_input_boundary_fixtures import build_published_beo_input_boundary_fixture

ROOT = Path(__file__).resolve().parents[1]
BLK028 = ROOT / "docs" / "BLK-028_published-beo-input-boundary.md"
TRACE_ARTIFACTS = [
    {
        "kind": "REQ",
        "id": "REQ-S25-PUBLISHED-001",
        "version_hash": "sha256:" + "a" * 64,
    },
    {
        "kind": "UC",
        "id": "UC-S25-PUBLISHED-001",
        "version_hash": "sha256:" + "b" * 64,
    },
]


def canonical_fixture_hash(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


class PublishedBeoInputBoundaryFixtureTest(unittest.TestCase):
    def _draft_beo(self, **overrides):
        draft = {
            "beo_id": "BEO_S25_DRAFT_001",
            "beb_id": "BEB_S25_SYNTHETIC",
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
            "approval_timestamp": "2026-05-08T08:20:00+10:00",
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
            candidate_id="BEO-PUB-CANDIDATE-S25-001",
            publication_approval=self._publication_approval(draft),
            signer_fixture={
                "signer_identity": "fixture-signer:S25",
                "signer_policy_hash": "sha256:" + "4" * 64,
                "key_material_accessed": False,
                "signature_generated": False,
                "kms_called": False,
                "secret_read": False,
            },
            storage_fixture={
                "storage_target_identity": "fixture-storage:S25",
                "storage_policy_hash": "sha256:" + "5" * 64,
                "immutable_storage_written": False,
                "storage_write_attempted": False,
            },
            ledger_fixture={
                "ledger_target_identity": "fixture-ledger:S25",
                "ledger_policy_hash": "sha256:" + "6" * 64,
                "public_ledger_mutated": False,
                "ledger_append_attempted": False,
            },
            rollback_fixture={
                "rollback_policy_hash": "sha256:" + "7" * 64,
                "rollback_fixture_identity": "fixture-rollback:S25",
                "rollback_executed": False,
                "revocation_executed": False,
                "supersession_executed": False,
            },
        )
        candidate.update(overrides)
        return candidate

    def _receipt(self, candidate=None, **overrides):
        if candidate is None:
            candidate = self._candidate()
        receipt = {
            "receipt_id": "PUB-BEO-INPUT-RECEIPT-S25-001",
            "publication_receipt_hash": "sha256:" + "8" * 64,
            "publication_event_hash": "sha256:" + "9" * 64,
            "published_input_identity": "published-beo-input:S25:001",
            "publication_receipt_scope": "PUBLISHED_BEO_INPUT_FIXTURE_ONLY",
            "approved_candidate_id": candidate["candidate_id"],
            "approved_beo_hash": candidate["beo_hash"],
            "operator_identity": "discord:684235178083745819",
            "signer_identity": "fixture-signer:S25",
            "storage_receipt_hash": "sha256:" + "0" * 64,
            "ledger_receipt_hash": "sha256:" + "a" * 64,
            "published_at": "2026-05-08T08:21:00+10:00",
            "expired": False,
            "replayed": False,
            "stale": False,
            "signature_generated": False,
            "key_material_accessed": False,
            "immutable_storage_written": False,
            "storage_write_attempted": False,
            "public_ledger_mutated": False,
            "ledger_append_attempted": False,
            "rollback_executed": False,
            "revocation_executed": False,
            "supersession_executed": False,
        }
        receipt.update(overrides)
        return receipt

    def _input_fixture(self, candidate=None, receipt=None):
        if candidate is None:
            candidate = self._candidate()
        if receipt is None:
            receipt = self._receipt(candidate)
        return build_published_beo_input_boundary_fixture(
            candidate,
            publication_receipt=receipt,
            input_id="PUBLISHED-BEO-INPUT-S25-001",
        )

    def test_published_beo_input_preserves_candidate_and_receipt_without_side_effects(self):
        candidate = self._candidate()
        fixture = self._input_fixture(candidate)

        self.assertEqual(fixture["input_id"], "PUBLISHED-BEO-INPUT-S25-001")
        self.assertEqual(fixture["input_status"], "PUBLISHED_BEO_INPUT_FIXTURE_ONLY")
        self.assertEqual(fixture["candidate_id"], candidate["candidate_id"])
        self.assertEqual(fixture["beo_id"], candidate["beo_id"])
        self.assertEqual(fixture["beo_hash"], candidate["beo_hash"])
        self.assertEqual(fixture["beb_id"], candidate["beb_id"])
        self.assertEqual(fixture["beo_status"], "PASS")
        self.assertEqual(fixture["trace_artifacts"], TRACE_ARTIFACTS)
        self.assertEqual(fixture["publication_receipt"]["receipt_id"], "PUB-BEO-INPUT-RECEIPT-S25-001")
        self.assertEqual(fixture["publication_receipt_scope"], "PUBLISHED_BEO_INPUT_FIXTURE_ONLY")
        self.assertTrue(fixture["published_input_fixture"])
        self.assertEqual(fixture["beo_publication"], "PUBLISHED_INPUT_FIXTURE_ONLY")
        self.assertEqual(fixture["rtm_status"], "NOT_GENERATED")
        self.assertFalse(fixture["publication_performed"])
        self.assertFalse(fixture["signature_generated"])
        self.assertFalse(fixture["key_material_accessed"])
        self.assertFalse(fixture["immutable_storage_written"])
        self.assertFalse(fixture["public_ledger_mutated"])
        self.assertFalse(fixture["rollback_executed"])
        self.assertFalse(fixture["active_vault_read"])
        self.assertFalse(fixture["protected_body_read"])
        self.assertFalse(fixture["rtm_created"])
        self.assertFalse(fixture["matrix_created"])
        self.assertFalse(fixture["drift_decision_made"])
        self.assertNotIn("rtm", fixture)
        self.assertNotIn("rtm_id", fixture)
        self.assertNotIn("coverage_matrix", fixture)
        self.assertNotIn("signature", fixture)

    def test_failed_candidate_evidence_remains_failed_input_without_success_projection(self):
        candidate = self._candidate(self._draft_beo(status="FAIL"))
        fixture = self._input_fixture(candidate)

        self.assertEqual(fixture["beo_status"], "FAIL")
        self.assertTrue(fixture["published_input_fixture"])
        self.assertFalse(fixture["publication_performed"])
        self.assertFalse(fixture["rtm_created"])

    def test_published_beo_input_rejects_candidate_authority_fields(self):
        bad_candidates = [
            {"candidate_status": "PUBLISHED"},
            {"beo_publication": "PUBLISHED"},
            {"rtm_status": "GENERATED"},
            {"published": True},
            {"active_vault_read": True},
            {"protected_body_read": True},
            {"rtm": {}},
            {"rtm_id": "RTM-S25-001"},
            {"coverage_matrix": []},
            {"coverage_status": "TRACED"},
            {"coverage_claim": "FULL"},
            {"drift": "NONE"},
            {"drift_decision": "ACCEPT"},
            {"body": "protected text"},
            {"content": "protected text"},
            {"requirement_body": "protected text"},
            {"use_case_body": "protected text"},
        ]
        for override in bad_candidates:
            with self.subTest(override=override):
                with self.assertRaises(ValueError):
                    self._input_fixture(self._candidate(**override))

    def test_published_beo_input_rejects_bad_receipt_fixture(self):
        candidate = self._candidate()
        bad_receipts = [
            {"publication_receipt_hash": "not-sha256"},
            {"publication_event_hash": "not-sha256"},
            {"storage_receipt_hash": "not-sha256"},
            {"ledger_receipt_hash": "not-sha256"},
            {"publication_receipt_scope": "AUTHORITATIVE_BEO_PUBLICATION"},
            {"approved_candidate_id": "OTHER-CANDIDATE"},
            {"approved_beo_hash": "sha256:" + "f" * 64},
            {"expired": True},
            {"replayed": True},
            {"stale": True},
            {"operator_identity": ""},
            {"published_input_identity": ""},
            {"published_at": ""},
            {"signature_generated": True},
            {"key_material_accessed": True},
            {"immutable_storage_written": True},
            {"storage_write_attempted": True},
            {"public_ledger_mutated": True},
            {"ledger_append_attempted": True},
            {"rollback_executed": True},
            {"revocation_executed": True},
            {"supersession_executed": True},
            {"body": "protected text"},
            {"markdown": "protected text"},
        ]
        for override in bad_receipts:
            with self.subTest(override=override):
                with self.assertRaises(ValueError):
                    self._input_fixture(candidate, self._receipt(candidate, **override))

    def test_published_beo_input_rejects_candidate_nested_side_effect_descriptors(self):
        cases = [
            {"signer_fixture": {"key_material_accessed": True}},
            {"signer_fixture": {"signature_generated": True}},
            {"signer_fixture": {"kms_called": True}},
            {"signer_fixture": {"secret_read": True}},
            {"storage_fixture": {"immutable_storage_written": True}},
            {"storage_fixture": {"storage_write_attempted": True}},
            {"ledger_fixture": {"public_ledger_mutated": True}},
            {"ledger_fixture": {"ledger_append_attempted": True}},
            {"rollback_fixture": {"rollback_executed": True}},
            {"rollback_fixture": {"revocation_executed": True}},
            {"rollback_fixture": {"supersession_executed": True}},
        ]
        base = self._candidate()
        for patch_case in cases:
            candidate = json.loads(json.dumps(base))
            for key, nested in patch_case.items():
                candidate[key].update(nested)
            with self.subTest(patch_case=patch_case):
                with self.assertRaises(ValueError):
                    self._input_fixture(candidate)

    def test_published_beo_input_does_not_read_protected_vault_paths(self):
        forbidden = ("docs/active", "docs/requirements", "docs/use_cases")

        def guarded_open(path, *args, **kwargs):
            text = str(path)
            if any(marker in text for marker in forbidden):
                raise AssertionError(f"protected vault path read attempted: {path}")
            raise AssertionError(f"unexpected file read attempted: {path}")

        with patch("builtins.open", side_effect=guarded_open):
            fixture = self._input_fixture()

        self.assertEqual(fixture["input_status"], "PUBLISHED_BEO_INPUT_FIXTURE_ONLY")
        self.assertFalse(fixture["protected_body_read"])

    def test_published_beo_input_boundary_doc_exists_and_preserves_no_authority(self):
        self.assertTrue(BLK028.exists(), "BLK-028 published-BEO input boundary missing")
        text = BLK028.read_text()
        required = [
            "Published BEO input boundary",
            "Active fixture boundary contract — not BEO publication authority",
            "Track G — BEO publication path",
            "Track H — BLK-link offline RTM ledger",
            "PUBLISHED_BEO_INPUT_FIXTURE_ONLY",
            'rtm_status: "NOT_GENERATED"',
            "no authoritative BEO publication",
            "no runtime `PUBLISHED` BEO output",
            "no signer key material",
            "no immutable storage writes",
            "no public ledger mutation",
            "no rollback, revocation, or supersession execution",
            "no RTM generation",
            "no RTM drift rejection authority",
            "no protected BLK-req vault body reads",
            "publication candidates are not published-BEO inputs",
            "Missing or malformed publication receipt fails closed",
            "future RTM generation requires a later explicit sprint and human approval",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-028 published input boundary markers missing: {missing}")

    def test_published_beo_input_module_has_no_live_side_effect_surfaces(self):
        text = (ROOT / "python" / "published_beo_input_boundary_fixtures.py").read_text()
        forbidden = [
            "def publish",
            "publish_authoritative_beo",
            "beo_publication = \"PUBLISHED\"",
            "generate_rtm",
            "active_vault_hash_compare",
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
            "rollback_executor",
            "live_blk_test",
        ]
        offenders = [marker for marker in forbidden if marker in text]
        self.assertEqual(offenders, [], f"Sprint 025 implementation introduced live markers: {offenders}")


if __name__ == "__main__":
    unittest.main()
