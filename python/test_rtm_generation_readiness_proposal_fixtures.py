import unittest
from pathlib import Path

from rtm_generation_readiness_proposal_fixtures import (
    build_rtm_generation_readiness_proposal_fixture,
)

ROOT = Path(__file__).resolve().parents[1]
VALID_HASH_A = "sha256:" + "a" * 64
VALID_HASH_B = "sha256:" + "b" * 64
VALID_HASH_C = "sha256:" + "c" * 64
VALID_HASH_D = "sha256:" + "d" * 64
VALID_HASH_E = "sha256:" + "e" * 64
VALID_HASH_F = "sha256:" + "f" * 64


def published_input_fixture() -> dict:
    return {
        "input_id": "PBI-001",
        "input_status": "PUBLISHED_BEO_INPUT_FIXTURE_ONLY",
        "beo_id": "BEO-001",
        "beo_hash": VALID_HASH_A,
        "beb_id": "BEB-001",
        "beo_status": "PASS",
        "trace_artifacts": [
            {"kind": "REQ", "id": "REQ-001", "version_hash": VALID_HASH_B},
            {"kind": "UC", "id": "UC-001", "version_hash": VALID_HASH_C},
        ],
        "publication_receipt": {
            "publication_receipt_hash": VALID_HASH_D,
            "publication_event_hash": VALID_HASH_E,
        },
        "publication_receipt_scope": "PUBLISHED_BEO_INPUT_FIXTURE_ONLY",
        "beo_publication": "PUBLISHED_INPUT_FIXTURE_ONLY",
        "rtm_status": "NOT_GENERATED",
        "publication_performed": False,
        "signature_generated": False,
        "key_material_accessed": False,
        "immutable_storage_written": False,
        "public_ledger_mutated": False,
        "rollback_executed": False,
        "active_vault_read": False,
        "protected_body_read": False,
        "rtm_created": False,
        "matrix_created": False,
        "drift_decision_made": False,
    }


def backend_fixture() -> dict:
    return {
        "manifest_id": "AVHM-001",
        "backend_status": "ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY",
        "backend_manifest_hash": VALID_HASH_F,
        "backend_approval": {"approval_record_hash": VALID_HASH_E},
        "downstream_hash_metadata_records": [
            {
                "kind": "REQ",
                "id": "REQ-001",
                "version_hash": VALID_HASH_B,
                "metadata_source": "ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY",
                "body_included": False,
                "body_read": False,
            },
            {
                "kind": "UC",
                "id": "UC-001",
                "version_hash": VALID_HASH_C,
                "metadata_source": "ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY",
                "body_included": False,
                "body_read": False,
            },
        ],
        "rtm_status": "NOT_GENERATED",
        "active_vault_scanned": False,
        "active_vault_read": False,
        "protected_body_read": False,
        "body_copied": False,
        "body_hashed": False,
        "rtm_created": False,
        "matrix_created": False,
        "drift_decision_made": False,
        "publication_performed": False,
        "source_mutated": False,
    }


def proposal_request() -> dict:
    return {
        "proposal_request_hash": VALID_HASH_A,
        "authorization_request_hash": VALID_HASH_B,
        "operator_identity": "camcamcami",
        "request_scope": "RTM_GENERATION_READINESS_PROPOSAL_FIXTURE_ONLY",
        "request_timestamp": "2026-05-08T09:30:00+10:00",
        "approved_input_id": "PBI-001",
        "approved_beo_hash": VALID_HASH_A,
        "approved_backend_manifest_hash": VALID_HASH_F,
        "generation_approval_required": True,
        "rtm_generation_authorized": False,
        "expired": False,
        "replayed": False,
        "stale": False,
    }


class RtmGenerationReadinessProposalFixtureTest(unittest.TestCase):
    def test_happy_path_preserves_identities_and_denies_runtime_rtm(self):
        fixture = build_rtm_generation_readiness_proposal_fixture(
            published_input_fixture(),
            active_vault_backend_fixture=backend_fixture(),
            proposal_request=proposal_request(),
            proposal_id="RTM-PROPOSAL-001",
        )

        self.assertEqual(fixture["proposal_id"], "RTM-PROPOSAL-001")
        self.assertEqual(
            fixture["proposal_status"], "RTM_GENERATION_READINESS_PROPOSAL_FIXTURE_ONLY"
        )
        self.assertEqual(fixture["input_id"], "PBI-001")
        self.assertEqual(fixture["beo_hash"], VALID_HASH_A)
        self.assertEqual(fixture["backend_manifest_hash"], VALID_HASH_F)
        self.assertEqual(fixture["rtm_status"], "NOT_GENERATED")
        self.assertEqual(fixture["rtm_authority"], "PROPOSAL_ONLY_NOT_AUTHORIZED")
        self.assertTrue(fixture["generation_approval_required"])
        self.assertFalse(fixture["rtm_generation_authorized"])
        self.assertFalse(fixture["rtm_created"])
        self.assertFalse(fixture["matrix_created"])
        self.assertFalse(fixture["drift_decision_made"])
        self.assertEqual(
            [record["readiness_state"] for record in fixture["readiness_records"]],
            ["READY_FOR_LATER_RTM_APPROVAL", "READY_FOR_LATER_RTM_APPROVAL"],
        )
        self.assertEqual(
            fixture["metadata_record_identities"],
            [
                {"kind": "REQ", "id": "REQ-001", "version_hash": VALID_HASH_B},
                {"kind": "UC", "id": "UC-001", "version_hash": VALID_HASH_C},
            ],
        )

    def test_mismatched_trace_and_metadata_identity_fails_closed(self):
        backend = backend_fixture()
        backend["downstream_hash_metadata_records"][1]["version_hash"] = VALID_HASH_D
        with self.assertRaisesRegex(ValueError, "metadata version_hash mismatch"):
            build_rtm_generation_readiness_proposal_fixture(
                published_input_fixture(),
                active_vault_backend_fixture=backend,
                proposal_request=proposal_request(),
                proposal_id="RTM-PROPOSAL-001",
            )

    def test_extra_and_duplicate_metadata_identities_fail_closed(self):
        backend = backend_fixture()
        backend["downstream_hash_metadata_records"].append(
            {
                "kind": "REQ",
                "id": "REQ-EXTRA",
                "version_hash": VALID_HASH_D,
                "metadata_source": "ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY",
                "body_included": False,
                "body_read": False,
            }
        )
        with self.assertRaisesRegex(ValueError, "extra hash metadata"):
            build_rtm_generation_readiness_proposal_fixture(
                published_input_fixture(),
                active_vault_backend_fixture=backend,
                proposal_request=proposal_request(),
                proposal_id="RTM-PROPOSAL-001",
            )

        backend = backend_fixture()
        backend["downstream_hash_metadata_records"].append(dict(backend["downstream_hash_metadata_records"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate hash metadata"):
            build_rtm_generation_readiness_proposal_fixture(
                published_input_fixture(),
                active_vault_backend_fixture=backend,
                proposal_request=proposal_request(),
                proposal_id="RTM-PROPOSAL-001",
            )

    def test_duplicate_trace_identities_fail_closed(self):
        published = published_input_fixture()
        published["trace_artifacts"].append(dict(published["trace_artifacts"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate trace artifact"):
            build_rtm_generation_readiness_proposal_fixture(
                published,
                active_vault_backend_fixture=backend_fixture(),
                proposal_request=proposal_request(),
                proposal_id="RTM-PROPOSAL-001",
            )

    def test_rejects_runtime_rtm_coverage_drift_publication_and_body_fields(self):
        forbidden_fields = [
            "rtm",
            "rtm_id",
            "rtm_authority",
            "rtm_ledger",
            "coverage_matrix",
            "coverage_status",
            "drift_decision",
            "signature",
            "body",
            "active_vault_path",
        ]
        for field in forbidden_fields:
            with self.subTest(field=field):
                published = published_input_fixture()
                published[field] = "forbidden"
                with self.assertRaisesRegex(ValueError, "rejects forbidden field"):
                    build_rtm_generation_readiness_proposal_fixture(
                        published,
                        active_vault_backend_fixture=backend_fixture(),
                        proposal_request=proposal_request(),
                        proposal_id="RTM-PROPOSAL-001",
                    )

    def test_unsupported_context_fields_fail_closed(self):
        published = published_input_fixture()
        published["runtime_authority"] = "laundered"
        with self.assertRaisesRegex(ValueError, "published_beo_input rejects unsupported field"):
            build_rtm_generation_readiness_proposal_fixture(
                published,
                active_vault_backend_fixture=backend_fixture(),
                proposal_request=proposal_request(),
                proposal_id="RTM-PROPOSAL-001",
            )

        backend = backend_fixture()
        backend["runtime_authority"] = "laundered"
        with self.assertRaisesRegex(ValueError, "active_vault_backend_fixture rejects unsupported field"):
            build_rtm_generation_readiness_proposal_fixture(
                published_input_fixture(),
                active_vault_backend_fixture=backend,
                proposal_request=proposal_request(),
                proposal_id="RTM-PROPOSAL-001",
            )

        request = proposal_request()
        request["runtime_authority"] = "laundered"
        with self.assertRaisesRegex(ValueError, "proposal_request rejects unsupported field"):
            build_rtm_generation_readiness_proposal_fixture(
                published_input_fixture(),
                active_vault_backend_fixture=backend_fixture(),
                proposal_request=request,
                proposal_id="RTM-PROPOSAL-001",
            )

    def test_rejects_nested_secret_body_and_rtm_fields(self):
        for field in ["secret", "rtm", "rtm_authority", "coverage_matrix", "drift_decision"]:
            with self.subTest(field=field):
                request = proposal_request()
                request["nested"] = {field: "value"}
                with self.assertRaisesRegex(ValueError, f"rejects forbidden field: {field}"):
                    build_rtm_generation_readiness_proposal_fixture(
                        published_input_fixture(),
                        active_vault_backend_fixture=backend_fixture(),
                        proposal_request=request,
                        proposal_id="RTM-PROPOSAL-001",
                    )

    def test_malformed_hashes_missing_ids_and_non_string_identities_fail_closed(self):
        published = published_input_fixture()
        published["beo_hash"] = "sha256:BAD"
        with self.assertRaisesRegex(ValueError, "beo_hash must match"):
            build_rtm_generation_readiness_proposal_fixture(
                published,
                active_vault_backend_fixture=backend_fixture(),
                proposal_request=proposal_request(),
                proposal_id="RTM-PROPOSAL-001",
            )

        backend = backend_fixture()
        backend["backend_manifest_hash"] = ""
        with self.assertRaisesRegex(ValueError, "requires non-empty backend_manifest_hash"):
            build_rtm_generation_readiness_proposal_fixture(
                published_input_fixture(),
                active_vault_backend_fixture=backend,
                proposal_request=proposal_request(),
                proposal_id="RTM-PROPOSAL-001",
            )

        request = proposal_request()
        request["operator_identity"] = 123
        with self.assertRaisesRegex(ValueError, "operator_identity must be a string"):
            build_rtm_generation_readiness_proposal_fixture(
                published_input_fixture(),
                active_vault_backend_fixture=backend_fixture(),
                proposal_request=request,
                proposal_id="RTM-PROPOSAL-001",
            )

    def test_request_identity_mismatches_fail_closed(self):
        for field, value, expected in [
            ("approved_input_id", "PBI-WRONG", "approved_input_id does not match"),
            ("approved_beo_hash", VALID_HASH_D, "approved_beo_hash does not match"),
            (
                "approved_backend_manifest_hash",
                VALID_HASH_D,
                "approved_backend_manifest_hash does not match",
            ),
        ]:
            with self.subTest(field=field):
                request = proposal_request()
                request[field] = value
                with self.assertRaisesRegex(ValueError, expected):
                    build_rtm_generation_readiness_proposal_fixture(
                        published_input_fixture(),
                        active_vault_backend_fixture=backend_fixture(),
                        proposal_request=request,
                        proposal_id="RTM-PROPOSAL-001",
                    )

    def test_request_cannot_authorize_generation_or_be_stale(self):
        for field in ["rtm_generation_authorized", "expired", "replayed", "stale"]:
            with self.subTest(field=field):
                request = proposal_request()
                request[field] = True
                with self.assertRaises(ValueError):
                    build_rtm_generation_readiness_proposal_fixture(
                        published_input_fixture(),
                        active_vault_backend_fixture=backend_fixture(),
                        proposal_request=request,
                        proposal_id="RTM-PROPOSAL-001",
                    )

    def test_side_effect_flags_must_remain_false(self):
        for field in [
            "active_vault_scanned",
            "active_vault_read",
            "protected_body_read",
            "rtm_created",
            "matrix_created",
            "drift_decision_made",
            "publication_performed",
            "source_mutated",
        ]:
            with self.subTest(field=field):
                backend = backend_fixture()
                backend[field] = True
                with self.assertRaisesRegex(ValueError, "must be false"):
                    build_rtm_generation_readiness_proposal_fixture(
                        published_input_fixture(),
                        active_vault_backend_fixture=backend,
                        proposal_request=proposal_request(),
                        proposal_id="RTM-PROPOSAL-001",
                    )

    def test_boundary_document_and_implementation_have_no_live_surface(self):
        boundary = ROOT / "docs" / "BLK-030_rtm-generation-readiness-proposal-boundary.md"
        self.assertTrue(boundary.exists(), "BLK-030 boundary missing")
        text = boundary.read_text()
        for marker in [
            "RTM generation readiness proposal boundary",
            "RTM_GENERATION_READINESS_PROPOSAL_FIXTURE_ONLY",
            "proposal-only fixture",
            "no runtime RTM generation",
            "no coverage matrices",
            "no RTM drift rejection authority",
            "no protected BLK-req vault body reads",
            "future runtime RTM generation requires a later explicit sprint and human approval",
        ]:
            self.assertIn(marker, text)

        implementation_text = (ROOT / "python" / "rtm_generation_readiness_proposal_fixtures.py").read_text()
        forbidden_live_markers = [
            "def generate_rtm",
            "class RtmLedger",
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
            "coverage_matrix_generator",
            "drift_decision_runtime",
            "publish_authoritative_beo",
            "ledger_writer",
            "storage_writer",
        ]
        offenders = [marker for marker in forbidden_live_markers if marker in implementation_text]
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
