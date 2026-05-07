import unittest
from pathlib import Path
from unittest.mock import patch

from active_vault_hash_metadata_backend_fixtures import (
    build_active_vault_hash_metadata_backend_fixture,
)

ROOT = Path(__file__).resolve().parents[1]
BLK029 = ROOT / "docs" / "BLK-029_active-vault-hash-metadata-backend-boundary.md"


class ActiveVaultHashMetadataBackendFixtureTest(unittest.TestCase):
    def _records(self, **first_override):
        records = [
            {
                "kind": "REQ",
                "id": "REQ-S26-HASH-001",
                "version_hash": "sha256:" + "a" * 64,
                "manifest_record_id": "AVHM-S26-REQ-001",
                "backend_manifest_hash": "sha256:" + "b" * 64,
                "metadata_source": "ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY",
                "downstream_metadata_source": "ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY",
                "body_included": False,
                "body_read": False,
                "body_copied": False,
                "body_hashed": False,
                "active_vault_read": False,
                "active_vault_scanned": False,
                "protected_path_accessed": False,
            },
            {
                "kind": "UC",
                "id": "UC-S26-HASH-001",
                "version_hash": "sha256:" + "c" * 64,
                "manifest_record_id": "AVHM-S26-UC-001",
                "backend_manifest_hash": "sha256:" + "b" * 64,
                "metadata_source": "ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY",
                "downstream_metadata_source": "ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY",
                "body_included": False,
                "body_read": False,
                "body_copied": False,
                "body_hashed": False,
                "active_vault_read": False,
                "active_vault_scanned": False,
                "protected_path_accessed": False,
            },
        ]
        records[0].update(first_override)
        return records

    def _approval(self, **overrides):
        approval = {
            "approval_record_hash": "sha256:" + "d" * 64,
            "authorization_request_hash": "sha256:" + "e" * 64,
            "operator_identity": "discord:684235178083745819",
            "approval_scope": "ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY",
            "approval_timestamp": "2026-05-08T08:48:00+10:00",
            "approved_manifest_hash": "sha256:" + "b" * 64,
            "expired": False,
            "replayed": False,
            "stale": False,
        }
        approval.update(overrides)
        return approval

    def _fixture(self, records=None, approval=None, manifest_id="AVHM-MANIFEST-S26-001"):
        return build_active_vault_hash_metadata_backend_fixture(
            self._records() if records is None else records,
            backend_approval=self._approval() if approval is None else approval,
            manifest_id=manifest_id,
        )

    def test_backend_fixture_preserves_manifest_hashes_without_body_or_rtm_authority(self):
        fixture = self._fixture()

        self.assertEqual(fixture["manifest_id"], "AVHM-MANIFEST-S26-001")
        self.assertEqual(fixture["backend_status"], "ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY")
        self.assertEqual(fixture["rtm_status"], "NOT_GENERATED")
        self.assertEqual(fixture["backend_manifest_hash"], "sha256:" + "b" * 64)
        self.assertEqual(fixture["backend_approval"]["approval_scope"], "ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY")
        self.assertFalse(fixture["active_vault_scanned"])
        self.assertFalse(fixture["active_vault_read"])
        self.assertFalse(fixture["protected_body_read"])
        self.assertFalse(fixture["body_copied"])
        self.assertFalse(fixture["body_hashed"])
        self.assertFalse(fixture["rtm_created"])
        self.assertFalse(fixture["matrix_created"])
        self.assertFalse(fixture["drift_decision_made"])
        self.assertFalse(fixture["publication_performed"])
        self.assertFalse(fixture["source_mutated"])
        self.assertEqual(len(fixture["manifest_records"]), 2)
        self.assertEqual(
            fixture["manifest_records"][0]["metadata_source"],
            "ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY",
        )
        self.assertEqual(
            fixture["downstream_hash_metadata_records"][0],
            {
                "kind": "REQ",
                "id": "REQ-S26-HASH-001",
                "version_hash": "sha256:" + "a" * 64,
                "metadata_source": "ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY",
                "body_included": False,
                "body_read": False,
            },
        )
        self.assertNotIn("rtm", fixture)
        self.assertNotIn("rtm_id", fixture)
        self.assertNotIn("coverage_matrix", fixture)

    def test_backend_fixture_rejects_malformed_hashes_missing_ids_and_non_string_identity(self):
        bad_records = [
            {"version_hash": "not-sha256"},
            {"backend_manifest_hash": "not-sha256"},
            {"kind": ""},
            {"id": ""},
            {"manifest_record_id": 123},
            {"metadata_source": "ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY"},
            {"downstream_metadata_source": "OTHER"},
        ]
        for override in bad_records:
            with self.subTest(override=override):
                with self.assertRaises(ValueError):
                    self._fixture(records=self._records(**override))
        with self.assertRaises(ValueError):
            self._fixture(manifest_id=123)

    def test_backend_fixture_rejects_protected_path_and_body_bearing_fields(self):
        for field in [
            "active_vault_path",
            "protected_path",
            "requirements_path",
            "use_cases_path",
            "source_path",
            "file_path",
            "path",
            "body",
            "text",
            "content",
            "markdown",
            "requirement_body",
            "use_case_body",
            "body_excerpt",
            "body_hash_input",
            "raw_artifact",
            "artifact_text",
        ]:
            with self.subTest(field=field):
                with self.assertRaises(ValueError):
                    self._fixture(records=self._records(**{field: "forbidden"}))

    def test_backend_fixture_rejects_promotion_rtm_publication_and_side_effect_fields(self):
        for override in [
            {"promote": True},
            {"promotion_performed": True},
            {"baseline_authorization": {}},
            {"revision_applied": True},
            {"parent_hash_checked": True},
            {"active_vault_written": True},
            {"rtm": {}},
            {"rtm_id": "RTM-S26-001"},
            {"coverage_matrix": []},
            {"coverage_status": "TRACED"},
            {"drift_decision": "ACCEPT"},
            {"published_at": "now"},
            {"signature": "sig"},
            {"ledger_id": "ledger"},
            {"publication_authority": "LIVE"},
            {"beo_publication": "PUBLISHED"},
            {"active_vault_read": True},
            {"active_vault_scanned": True},
            {"protected_path_accessed": True},
            {"body_read": True},
            {"body_copied": True},
            {"body_hashed": True},
            {"rtm_created": True},
            {"matrix_created": True},
            {"drift_decision_made": True},
            {"publication_performed": True},
            {"source_mutated": True},
        ]:
            with self.subTest(override=override):
                with self.assertRaises(ValueError):
                    self._fixture(records=self._records(**override))

    def test_backend_fixture_rejects_bad_backend_approval_fixture(self):
        for override in [
            {"approval_record_hash": "not-sha256"},
            {"authorization_request_hash": "not-sha256"},
            {"operator_identity": ""},
            {"operator_identity": 123},
            {"approval_scope": "RTM_HASH_METADATA_PATH_FIXTURE_ONLY"},
            {"approval_timestamp": ""},
            {"approved_manifest_hash": "sha256:" + "0" * 64},
            {"expired": True},
            {"replayed": True},
            {"stale": True},
        ]:
            with self.subTest(override=override):
                with self.assertRaises(ValueError):
                    self._fixture(approval=self._approval(**override))

    def test_backend_fixture_does_not_read_protected_vault_paths(self):
        forbidden = ("docs/active", "docs/requirements", "docs/use_cases")

        def fail_forbidden_read(self_path, *args, **kwargs):
            as_text = str(self_path)
            if any(token in as_text for token in forbidden):
                raise AssertionError(f"forbidden active vault read: {as_text}")
            return ""

        with patch.object(Path, "read_text", fail_forbidden_read):
            fixture = self._fixture()

        self.assertFalse(fixture["active_vault_scanned"])
        self.assertFalse(fixture["active_vault_read"])
        self.assertFalse(fixture["protected_body_read"])

    def test_backend_boundary_doc_exists_and_preserves_no_authority(self):
        self.assertTrue(BLK029.exists(), "BLK-029 active-vault hash metadata backend boundary missing")
        text = BLK029.read_text()
        required = [
            "Active-vault hash metadata backend boundary",
            "Active fixture boundary contract — not active-vault read authority and not RTM generation authority",
            "Track B — BLK-req legislative gateway",
            "Track H — BLK-link offline RTM ledger",
            "ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY",
            "ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY",
            'rtm_status: "NOT_GENERATED"',
            "no active-vault filesystem scanning",
            "no protected BLK-req vault body reads",
            "does not authorize RTM generation",
            "does not authorize RTM drift rejection authority",
            "future RTM generation requires a later explicit sprint and human approval",
            "Missing or malformed backend manifest metadata fails closed",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-029 missing markers: {missing}")

    def test_backend_module_has_no_live_side_effect_surfaces(self):
        text = (ROOT / "python" / "active_vault_hash_metadata_backend_fixtures.py").read_text()
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
            "open(",
            "Path(",
            "read_text",
            "glob(",
            "rglob(",
            "active_vault_scanner",
            "generate_rtm",
            "coverage_matrix_generator",
            "drift_decision_runtime",
            "publish_authoritative_beo",
        ]
        offenders = [marker for marker in forbidden_markers if marker in text]
        self.assertEqual(offenders, [], f"Sprint 026 implementation introduced live markers: {offenders}")


if __name__ == "__main__":
    unittest.main()
