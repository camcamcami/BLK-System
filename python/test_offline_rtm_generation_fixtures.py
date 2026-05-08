import hashlib
import json
import unittest
from pathlib import Path

from offline_rtm_generation_fixtures import build_offline_rtm_ledger_fixture

ROOT = Path(__file__).resolve().parents[1]
BLK033 = ROOT / "docs" / "BLK-033_offline-rtm-generation-boundary.md"
IMPLEMENTATION = ROOT / "python" / "offline_rtm_generation_fixtures.py"

HASH_A = "sha256:" + "a" * 64
HASH_B = "sha256:" + "b" * 64
HASH_C = "sha256:" + "c" * 64
HASH_D = "sha256:" + "d" * 64
HASH_E = "sha256:" + "e" * 64
HASH_F = "sha256:" + "f" * 64


def canonical_hash(value: dict) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def approval_hashes(
    *,
    input_id: str = "PBI-030-001",
    beo_hash: str = HASH_A,
    publication_receipt_hash: str = HASH_D,
    backend_manifest_hash: str = HASH_F,
    backend_approval_hash: str = HASH_E,
    output_id: str = "RTM-030-001",
    trace_artifacts: list[dict] | None = None,
    metadata_record_identities: list[dict] | None = None,
    approval_id: str = "RTM-GEN-APPROVAL-030-001",
    operator_identity: str = "camcamcami",
    approval_timestamp: str = "2026-05-08T14:22:54+10:00",
) -> tuple[str, str]:
    trace_artifacts = trace_artifacts or [
        {"kind": "REQ", "id": "REQ-001", "version_hash": HASH_B},
        {"kind": "UC", "id": "UC-001", "version_hash": HASH_C},
    ]
    metadata_record_identities = metadata_record_identities or [
        {"kind": "REQ", "id": "REQ-001", "version_hash": HASH_B},
        {"kind": "UC", "id": "UC-001", "version_hash": HASH_C},
    ]
    request_hash = canonical_hash(
        {
            "approval_scope": "OFFLINE_RTM_GENERATION_APPROVAL_FIXTURE_ONLY",
            "approved_input_id": input_id,
            "approved_beo_hash": beo_hash,
            "publication_receipt_hash": publication_receipt_hash,
            "approved_backend_manifest_hash": backend_manifest_hash,
            "backend_approval_hash": backend_approval_hash,
            "approved_output_id": output_id,
            "trace_artifacts": trace_artifacts,
            "metadata_record_identities": metadata_record_identities,
            "drift_rejection_authorized": False,
        }
    )
    record_hash = canonical_hash(
        {
            "approval_id": approval_id,
            "authorization_request_hash": request_hash,
            "operator_identity": operator_identity,
            "approval_scope": "OFFLINE_RTM_GENERATION_APPROVAL_FIXTURE_ONLY",
            "approval_timestamp": approval_timestamp,
            "generation_authorized": True,
            "drift_rejection_authorized": False,
            "expired": False,
            "replayed": False,
            "stale": False,
        }
    )
    return request_hash, record_hash


def published_input_fixture() -> dict:
    return {
        "input_id": "PBI-030-001",
        "input_status": "PUBLISHED_BEO_INPUT_FIXTURE_ONLY",
        "beo_id": "BEO-030-001",
        "beo_hash": HASH_A,
        "beb_id": "BEB-030-001",
        "beo_status": "PASS",
        "trace_artifacts": [
            {"kind": "REQ", "id": "REQ-001", "version_hash": HASH_B},
            {"kind": "UC", "id": "UC-001", "version_hash": HASH_C},
        ],
        "publication_receipt": {
            "publication_receipt_hash": HASH_D,
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
        "manifest_id": "AVHM-030-001",
        "backend_status": "ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY",
        "backend_manifest_hash": HASH_F,
        "backend_approval": {"approval_record_hash": HASH_E},
        "downstream_hash_metadata_records": [
            {
                "kind": "REQ",
                "id": "REQ-001",
                "version_hash": HASH_B,
                "metadata_source": "ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY",
                "body_included": False,
                "body_read": False,
            },
            {
                "kind": "UC",
                "id": "UC-001",
                "version_hash": HASH_C,
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


def generation_approval(
    *,
    input_id: str = "PBI-030-001",
    output_id: str = "RTM-030-001",
    trace_artifacts: list[dict] | None = None,
    metadata_record_identities: list[dict] | None = None,
    approval_id: str = "RTM-GEN-APPROVAL-030-001",
    operator_identity: str = "camcamcami",
    approval_timestamp: str = "2026-05-08T14:22:54+10:00",
) -> dict:
    authorization_request_hash, approval_record_hash = approval_hashes(
        input_id=input_id,
        output_id=output_id,
        trace_artifacts=trace_artifacts,
        metadata_record_identities=metadata_record_identities,
        approval_id=approval_id,
        operator_identity=operator_identity,
        approval_timestamp=approval_timestamp,
    )
    return {
        "approval_id": approval_id,
        "approval_record_hash": approval_record_hash,
        "authorization_request_hash": authorization_request_hash,
        "operator_identity": operator_identity,
        "approval_scope": "OFFLINE_RTM_GENERATION_APPROVAL_FIXTURE_ONLY",
        "approval_timestamp": approval_timestamp,
        "approved_input_id": input_id,
        "approved_beo_hash": HASH_A,
        "approved_backend_manifest_hash": HASH_F,
        "approved_output_id": output_id,
        "generation_authorized": True,
        "drift_rejection_authorized": False,
        "expired": False,
        "replayed": False,
        "stale": False,
    }


class OfflineRtmGenerationFixtureTest(unittest.TestCase):
    def test_generates_deterministic_offline_rtm_ledger_from_supplied_inputs(self):
        ledger = build_offline_rtm_ledger_fixture(
            published_input_fixture(),
            active_vault_backend_fixture=backend_fixture(),
            generation_approval=generation_approval(),
            rtm_id="RTM-030-001",
        )
        self.assertEqual(ledger["rtm_id"], "RTM-030-001")
        self.assertEqual(ledger["rtm_status"], "OFFLINE_RTM_LEDGER_GENERATED_FIXTURE_ONLY")
        self.assertEqual(ledger["rtm_authority"], "OFFLINE_RTM_GENERATION_APPROVED_NARROW")
        self.assertEqual(ledger["coverage_matrix_status"], "OFFLINE_RTM_COVERAGE_MATRIX_FIXTURE_ONLY")
        self.assertRegex(ledger["rtm_ledger_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(ledger["input_id"], "PBI-030-001")
        self.assertEqual(ledger["beo_id"], "BEO-030-001")
        self.assertEqual(ledger["beo_hash"], HASH_A)
        self.assertEqual(ledger["backend_manifest_hash"], HASH_F)
        self.assertEqual(ledger["approval_scope"], "OFFLINE_RTM_GENERATION_APPROVAL_FIXTURE_ONLY")
        self.assertEqual(
            [record["coverage_state"] for record in ledger["coverage_records"]],
            ["TRACE_HASH_MATCHED", "TRACE_HASH_MATCHED"],
        )
        self.assertFalse(ledger["protected_body_read"])
        self.assertFalse(ledger["active_vault_scanned"])
        self.assertFalse(ledger["beo_publication_performed"])
        self.assertFalse(ledger["signature_generated"])
        self.assertFalse(ledger["immutable_storage_written"])
        self.assertFalse(ledger["public_ledger_mutated"])
        self.assertFalse(ledger["drift_rejection_made"])
        self.assertEqual(ledger["protected_body_boundary"], "PROTECTED_BODY_NOT_READ")
        self.assertEqual(ledger["active_vault_boundary"], "ACTIVE_VAULT_NOT_SCANNED")
        self.assertEqual(ledger["beo_publication_boundary"], "BEO_PUBLICATION_NOT_PERFORMED")
        self.assertEqual(
            ledger["side_effect_boundary"], "NO_SIGNER_STORAGE_OR_PUBLIC_LEDGER_SIDE_EFFECTS"
        )

        reordered_backend = backend_fixture()
        reordered_backend["downstream_hash_metadata_records"] = list(
            reversed(reordered_backend["downstream_hash_metadata_records"])
        )
        second = build_offline_rtm_ledger_fixture(
            published_input_fixture(),
            active_vault_backend_fixture=reordered_backend,
            generation_approval=generation_approval(),
            rtm_id="RTM-030-001",
        )
        self.assertEqual(second["rtm_ledger_hash"], ledger["rtm_ledger_hash"])

    def test_requires_exact_trace_metadata_bijection(self):
        backend = backend_fixture()
        backend["downstream_hash_metadata_records"][1]["version_hash"] = HASH_D
        with self.assertRaisesRegex(ValueError, "metadata version_hash mismatch"):
            build_offline_rtm_ledger_fixture(
                published_input_fixture(),
                active_vault_backend_fixture=backend,
                generation_approval=generation_approval(),
                rtm_id="RTM-030-001",
            )

        backend = backend_fixture()
        backend["downstream_hash_metadata_records"].append(
            {
                "kind": "REQ",
                "id": "REQ-999",
                "version_hash": HASH_D,
                "metadata_source": "ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY",
                "body_included": False,
                "body_read": False,
            }
        )
        with self.assertRaisesRegex(ValueError, "extra hash metadata"):
            build_offline_rtm_ledger_fixture(
                published_input_fixture(),
                active_vault_backend_fixture=backend,
                generation_approval=generation_approval(),
                rtm_id="RTM-030-001",
            )

        backend = backend_fixture()
        backend["downstream_hash_metadata_records"].append(dict(backend["downstream_hash_metadata_records"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate hash metadata"):
            build_offline_rtm_ledger_fixture(
                published_input_fixture(),
                active_vault_backend_fixture=backend,
                generation_approval=generation_approval(),
                rtm_id="RTM-030-001",
            )

        published = published_input_fixture()
        published["trace_artifacts"].append(dict(published["trace_artifacts"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate trace artifact"):
            build_offline_rtm_ledger_fixture(
                published,
                active_vault_backend_fixture=backend_fixture(),
                generation_approval=generation_approval(),
                rtm_id="RTM-030-001",
            )

    def test_rejects_protected_body_path_publication_secret_and_drift_fields(self):
        forbidden_fields = [
            "body",
            "text",
            "content",
            "active_vault_path",
            "protected_path",
            "source_path",
            "signature",
            "key_material",
            "private_key",
            "publication_authority",
            "drift_rejection",
            "drift_decision",
            "secret",
            "token",
        ]
        for field in forbidden_fields:
            with self.subTest(field=field):
                published = published_input_fixture()
                published[field] = "forbidden"
                with self.assertRaisesRegex(ValueError, "rejects forbidden field"):
                    build_offline_rtm_ledger_fixture(
                        published,
                        active_vault_backend_fixture=backend_fixture(),
                        generation_approval=generation_approval(),
                        rtm_id="RTM-030-001",
                    )

    def test_unsupported_context_fields_and_malformed_hashes_fail_closed(self):
        published = published_input_fixture()
        published["runtime_authority"] = "laundered"
        with self.assertRaisesRegex(ValueError, "published_beo_input rejects unsupported field"):
            build_offline_rtm_ledger_fixture(
                published,
                active_vault_backend_fixture=backend_fixture(),
                generation_approval=generation_approval(),
                rtm_id="RTM-030-001",
            )

        backend = backend_fixture()
        backend["backend_manifest_hash"] = "sha256:BAD"
        with self.assertRaisesRegex(ValueError, "backend_manifest_hash must match"):
            build_offline_rtm_ledger_fixture(
                published_input_fixture(),
                active_vault_backend_fixture=backend,
                generation_approval=generation_approval(),
                rtm_id="RTM-030-001",
            )

        approval = generation_approval()
        approval["operator_identity"] = 123
        with self.assertRaisesRegex(ValueError, "operator_identity must be a string"):
            build_offline_rtm_ledger_fixture(
                published_input_fixture(),
                active_vault_backend_fixture=backend_fixture(),
                generation_approval=approval,
                rtm_id="RTM-030-001",
            )

    def test_rejects_inherited_approval_and_drift_rejection_authority(self):
        for container_name, flag in [
            ("published", "publication_performed"),
            ("published", "signature_generated"),
            ("published", "immutable_storage_written"),
            ("published", "public_ledger_mutated"),
            ("published", "protected_body_read"),
            ("backend", "active_vault_scanned"),
            ("backend", "active_vault_read"),
            ("backend", "body_copied"),
            ("backend", "body_hashed"),
            ("backend", "drift_decision_made"),
        ]:
            with self.subTest(container=container_name, flag=flag):
                published = published_input_fixture()
                backend = backend_fixture()
                if container_name == "published":
                    published[flag] = True
                else:
                    backend[flag] = True
                with self.assertRaisesRegex(ValueError, f"{flag} must be false"):
                    build_offline_rtm_ledger_fixture(
                        published,
                        active_vault_backend_fixture=backend,
                        generation_approval=generation_approval(),
                        rtm_id="RTM-030-001",
                    )

        inherited_scopes = [
            "RTM_GENERATION_READINESS_PROPOSAL_FIXTURE_ONLY",
            "PUBLISHED_BEO_INPUT_FIXTURE_ONLY",
            "ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY",
            "BLK_TEST_PASS",
            "BEO_PUBLICATION_APPROVAL",
            "BLK_PIPE_EXECUTION_APPROVAL",
            "CODEX_LIVE_APPROVAL",
        ]
        for scope in inherited_scopes:
            with self.subTest(scope=scope):
                approval = generation_approval()
                approval["approval_scope"] = scope
                with self.assertRaisesRegex(ValueError, "approval_scope must be"):
                    build_offline_rtm_ledger_fixture(
                        published_input_fixture(),
                        active_vault_backend_fixture=backend_fixture(),
                        generation_approval=approval,
                        rtm_id="RTM-030-001",
                    )

        for field in ["drift_rejection_authorized", "expired", "replayed", "stale"]:
            with self.subTest(field=field):
                approval = generation_approval()
                approval[field] = True
                with self.assertRaisesRegex(ValueError, "must be false"):
                    build_offline_rtm_ledger_fixture(
                        published_input_fixture(),
                        active_vault_backend_fixture=backend_fixture(),
                        generation_approval=approval,
                        rtm_id="RTM-030-001",
                    )

    def test_rejects_nested_authority_side_effect_and_unsupported_field_smuggling(self):
        nested_trace_cases = [
            ("approval_scope", "BEO_PUBLICATION_APPROVAL"),
            ("drift_rejection_authorized", True),
            ("protected_path", "docs/active/REQ.md"),
        ]
        for field, value in nested_trace_cases:
            with self.subTest(container="trace_artifacts", field=field):
                published = published_input_fixture()
                published["trace_artifacts"][0][field] = value
                with self.assertRaisesRegex(ValueError, "trace_artifacts rejects"):
                    build_offline_rtm_ledger_fixture(
                        published,
                        active_vault_backend_fixture=backend_fixture(),
                        generation_approval=generation_approval(),
                        rtm_id="RTM-030-001",
                    )

        for field, value in [
            ("publication_performed", True),
            ("approval_scope", "BEO_PUBLICATION_APPROVAL"),
        ]:
            with self.subTest(container="publication_receipt", field=field):
                published = published_input_fixture()
                published["publication_receipt"][field] = value
                with self.assertRaisesRegex(ValueError, "publication_receipt rejects"):
                    build_offline_rtm_ledger_fixture(
                        published,
                        active_vault_backend_fixture=backend_fixture(),
                        generation_approval=generation_approval(),
                        rtm_id="RTM-030-001",
                    )

        for field, value in [
            ("approval_scope", "BEO_PUBLICATION_APPROVAL"),
            ("drift_rejection_authorized", True),
        ]:
            with self.subTest(container="backend_approval", field=field):
                backend = backend_fixture()
                backend["backend_approval"][field] = value
                with self.assertRaisesRegex(ValueError, "backend_approval rejects"):
                    build_offline_rtm_ledger_fixture(
                        published_input_fixture(),
                        active_vault_backend_fixture=backend,
                        generation_approval=generation_approval(),
                        rtm_id="RTM-030-001",
                    )

    def test_rejects_path_like_and_authority_strings_in_identity_fields(self):
        approval = generation_approval(output_id="/home/dad/BLK-System/docs/active/REQ.md")
        with self.assertRaisesRegex(ValueError, "rtm_id rejects forbidden identity"):
            build_offline_rtm_ledger_fixture(
                published_input_fixture(),
                active_vault_backend_fixture=backend_fixture(),
                generation_approval=approval,
                rtm_id="/home/dad/BLK-System/docs/active/REQ.md",
            )

        published = published_input_fixture()
        published["trace_artifacts"][0]["id"] = "docs/requirements/REQ-001.md"
        with self.assertRaisesRegex(ValueError, "trace_artifacts.id rejects forbidden identity"):
            build_offline_rtm_ledger_fixture(
                published,
                active_vault_backend_fixture=backend_fixture(),
                generation_approval=generation_approval(),
                rtm_id="RTM-030-001",
            )

        published = published_input_fixture()
        published["input_id"] = "BEO_PUBLICATION_APPROVAL"
        approval = generation_approval()
        approval["approved_input_id"] = "BEO_PUBLICATION_APPROVAL"
        with self.assertRaisesRegex(ValueError, "input_id rejects forbidden identity"):
            build_offline_rtm_ledger_fixture(
                published,
                active_vault_backend_fixture=backend_fixture(),
                generation_approval=approval,
                rtm_id="RTM-030-001",
            )

    def test_rejects_ignored_top_level_fields_that_can_carry_live_state(self):
        for field, value in [
            ("status", "PUBLISHED"),
            ("source_candidate_status", "BEO_PUBLICATION_APPROVAL"),
            ("candidate_id", "CANDIDATE-030-001"),
            ("published_input_fixture", {"publication_performed": True}),
        ]:
            with self.subTest(field=field):
                published = published_input_fixture()
                published[field] = value
                with self.assertRaisesRegex(ValueError, "published_beo_input rejects unsupported field"):
                    build_offline_rtm_ledger_fixture(
                        published,
                        active_vault_backend_fixture=backend_fixture(),
                        generation_approval=generation_approval(),
                        rtm_id="RTM-030-001",
                    )

    def test_approval_hashes_bind_canonical_request_and_record(self):
        approval = generation_approval()
        approval["authorization_request_hash"] = HASH_A
        with self.assertRaisesRegex(ValueError, "authorization_request_hash does not match"):
            build_offline_rtm_ledger_fixture(
                published_input_fixture(),
                active_vault_backend_fixture=backend_fixture(),
                generation_approval=approval,
                rtm_id="RTM-030-001",
            )

        approval = generation_approval()
        approval["approval_record_hash"] = HASH_A
        with self.assertRaisesRegex(ValueError, "approval_record_hash does not match"):
            build_offline_rtm_ledger_fixture(
                published_input_fixture(),
                active_vault_backend_fixture=backend_fixture(),
                generation_approval=approval,
                rtm_id="RTM-030-001",
            )

    def test_rejects_body_prose_and_encoded_paths_in_identity_fields(self):
        body_like = "RTM-030-001 -- body excerpt: The system shall treat this protected req sentence as an id"
        encoded_path = "RTM-030-001 docs%2Factive%2FREQ-001.md"
        for rtm_id in [body_like, encoded_path, "RTM-030-001 with unbounded prose identity text"]:
            with self.subTest(rtm_id=rtm_id):
                with self.assertRaisesRegex(ValueError, "rtm_id rejects (?:invalid identity format|forbidden identity marker)"):
                    build_offline_rtm_ledger_fixture(
                        published_input_fixture(),
                        active_vault_backend_fixture=backend_fixture(),
                        generation_approval=generation_approval(output_id=rtm_id),
                        rtm_id=rtm_id,
                    )

        published = published_input_fixture()
        published["input_id"] = "PBI-030-001 -- body excerpt: The system shall treat this protected req sentence as an id"
        with self.assertRaisesRegex(ValueError, "input_id rejects (?:invalid identity format|forbidden identity marker)"):
            build_offline_rtm_ledger_fixture(
                published,
                active_vault_backend_fixture=backend_fixture(),
                generation_approval=generation_approval(input_id=published["input_id"]),
                rtm_id="RTM-030-001",
            )

        published = published_input_fixture()
        published["trace_artifacts"][0]["id"] = "REQ-001 -- body excerpt: The system shall treat this protected req sentence as an id"
        backend = backend_fixture()
        backend["downstream_hash_metadata_records"][0]["id"] = published["trace_artifacts"][0]["id"]
        trace_artifacts = [
            {"kind": "REQ", "id": published["trace_artifacts"][0]["id"], "version_hash": HASH_B},
            {"kind": "UC", "id": "UC-001", "version_hash": HASH_C},
        ]
        with self.assertRaisesRegex(ValueError, "trace_artifacts.id rejects (?:invalid identity format|forbidden identity marker)"):
            build_offline_rtm_ledger_fixture(
                published,
                active_vault_backend_fixture=backend,
                generation_approval=generation_approval(
                    trace_artifacts=trace_artifacts,
                    metadata_record_identities=trace_artifacts,
                ),
                rtm_id="RTM-030-001",
            )

    def test_rejects_backend_manifest_records_because_they_can_carry_body_or_live_state(self):
        for manifest_records in [
            {"body": "protected req body text", "protected_path": "docs/active/REQ-001.md"},
            [{"body": "protected req body text"}],
            {"drift_rejection_authorized": True, "approval_scope": "BEO_PUBLICATION_APPROVAL"},
            {"active_vault_scanned": True, "protected_body_read": True, "public_ledger_mutated": True},
        ]:
            with self.subTest(manifest_records=manifest_records):
                backend = backend_fixture()
                backend["manifest_records"] = manifest_records
                with self.assertRaisesRegex(ValueError, "active_vault_backend_fixture rejects unsupported field"):
                    build_offline_rtm_ledger_fixture(
                        published_input_fixture(),
                        active_vault_backend_fixture=backend,
                        generation_approval=generation_approval(),
                        rtm_id="RTM-030-001",
                    )

    def test_rejects_body_prose_encoded_as_valid_looking_identity_tokens(self):
        smuggled_id = "REQ-THE_SYSTEM_SHALL_NOT_READ_BODY_TEXT"
        published = published_input_fixture()
        published["trace_artifacts"][0]["id"] = smuggled_id
        backend = backend_fixture()
        backend["downstream_hash_metadata_records"][0]["id"] = smuggled_id
        trace_artifacts = [
            {"kind": "REQ", "id": smuggled_id, "version_hash": HASH_B},
            {"kind": "UC", "id": "UC-001", "version_hash": HASH_C},
        ]
        with self.assertRaisesRegex(ValueError, "trace_artifacts.id rejects (?:invalid identity format|forbidden identity marker)"):
            build_offline_rtm_ledger_fixture(
                published,
                active_vault_backend_fixture=backend,
                generation_approval=generation_approval(
                    trace_artifacts=trace_artifacts,
                    metadata_record_identities=trace_artifacts,
                ),
                rtm_id="RTM-030-001",
            )

    def test_rejects_separator_variant_authority_markers_in_identity_fields(self):
        for approval_id in [
            "RTM-GEN-APPROVAL-BEO-PUBLICATION-APPROVAL",
            "RTM-GEN-APPROVAL-BLK.TEST.PASS",
        ]:
            with self.subTest(approval_id=approval_id):
                with self.assertRaisesRegex(ValueError, "approval_id rejects forbidden identity authority"):
                    build_offline_rtm_ledger_fixture(
                        published_input_fixture(),
                        active_vault_backend_fixture=backend_fixture(),
                        generation_approval=generation_approval(approval_id=approval_id),
                        rtm_id="RTM-030-001",
                    )

        for operator_identity in ["BEO-PUBLICATION-APPROVAL", "BLK.TEST.PASS"]:
            with self.subTest(operator_identity=operator_identity):
                with self.assertRaisesRegex(ValueError, "operator_identity rejects forbidden identity authority"):
                    build_offline_rtm_ledger_fixture(
                        published_input_fixture(),
                        active_vault_backend_fixture=backend_fixture(),
                        generation_approval=generation_approval(operator_identity=operator_identity),
                        rtm_id="RTM-030-001",
                    )

    def test_rejects_operator_identity_body_or_protected_reference_smuggling(self):
        for operator_identity in [
            "REQ-THE_SYSTEM_SHALL_NOT_READ_BODY_TEXT",
            "BODY_EXCERPT",
            "docs.active.REQ-001.md",
            "docs-2Factive-2FREQ-001.md",
        ]:
            with self.subTest(operator_identity=operator_identity):
                with self.assertRaisesRegex(ValueError, "operator_identity rejects (?:invalid identity format|forbidden identity marker)"):
                    build_offline_rtm_ledger_fixture(
                        published_input_fixture(),
                        active_vault_backend_fixture=backend_fixture(),
                        generation_approval=generation_approval(operator_identity=operator_identity),
                        rtm_id="RTM-030-001",
                    )

    def test_rejects_accepted_but_unbound_publication_event_hash(self):
        published = published_input_fixture()
        published["publication_receipt"]["publication_event_hash"] = "sha256:" + "9" * 64
        with self.assertRaisesRegex(ValueError, "publication_receipt rejects unsupported field"):
            build_offline_rtm_ledger_fixture(
                published,
                active_vault_backend_fixture=backend_fixture(),
                generation_approval=generation_approval(),
                rtm_id="RTM-030-001",
            )

    def test_rejects_normalized_operator_identity_smuggling_variants(self):
        for operator_identity in [
            "body_excerpt",
            "docs_active_req_001_md",
            "docs_2factive_2freq_001_md",
            "docsactivereq001md",
            "docs2factive2freq001md",
            "the_system_shall_not_read_body",
        ]:
            with self.subTest(operator_identity=operator_identity):
                with self.assertRaisesRegex(ValueError, "operator_identity rejects forbidden identity"):
                    build_offline_rtm_ledger_fixture(
                        published_input_fixture(),
                        active_vault_backend_fixture=backend_fixture(),
                        generation_approval=generation_approval(operator_identity=operator_identity),
                        rtm_id="RTM-030-001",
                    )

    def test_rejects_approval_timestamp_smuggling_and_malformed_shape(self):
        for approval_timestamp in [
            "2026-05-08T14:22:54+10:00 BEO-PUBLICATION-APPROVAL docs/active/REQ-001.md REQ-THE_SYSTEM_SHALL_NOT_READ_BODY_TEXT",
            "2026-05-08 14:22:54+10:00",
            "2026-05-08T14:22:54+10:00Z",
        ]:
            with self.subTest(approval_timestamp=approval_timestamp):
                with self.assertRaisesRegex(ValueError, "approval_timestamp rejects invalid timestamp format"):
                    build_offline_rtm_ledger_fixture(
                        published_input_fixture(),
                        active_vault_backend_fixture=backend_fixture(),
                        generation_approval=generation_approval(approval_timestamp=approval_timestamp),
                        rtm_id="RTM-030-001",
                    )

    def test_rejects_compacted_inherited_authority_operator_identity(self):
        for operator_identity in [
            "beopublicationapproval",
            "blktestpass",
            "codexliveapproval",
            "publishedbeoinputfixtureonly",
            "rejectdrift",
        ]:
            with self.subTest(operator_identity=operator_identity):
                with self.assertRaisesRegex(ValueError, "operator_identity rejects forbidden identity authority"):
                    build_offline_rtm_ledger_fixture(
                        published_input_fixture(),
                        active_vault_backend_fixture=backend_fixture(),
                        generation_approval=generation_approval(operator_identity=operator_identity),
                        rtm_id="RTM-030-001",
                    )

    def test_rejects_whitespace_normalization_in_accepted_schema_fields(self):
        published = published_input_fixture()
        published["input_status"] = " PUBLISHED_BEO_INPUT_FIXTURE_ONLY "
        with self.assertRaisesRegex(ValueError, "input_status must be"):
            build_offline_rtm_ledger_fixture(
                published,
                active_vault_backend_fixture=backend_fixture(),
                generation_approval=generation_approval(),
                rtm_id="RTM-030-001",
            )

        published = published_input_fixture()
        published["beo_hash"] = " " + HASH_A + " "
        approval = generation_approval()
        approval["approved_beo_hash"] = " " + HASH_A + " "
        with self.assertRaisesRegex(ValueError, "beo_hash must match"):
            build_offline_rtm_ledger_fixture(
                published,
                active_vault_backend_fixture=backend_fixture(),
                generation_approval=approval,
                rtm_id="RTM-030-001",
            )

        backend = backend_fixture()
        backend["backend_status"] = " ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY "
        with self.assertRaisesRegex(ValueError, "backend_status must be"):
            build_offline_rtm_ledger_fixture(
                published_input_fixture(),
                active_vault_backend_fixture=backend,
                generation_approval=generation_approval(),
                rtm_id="RTM-030-001",
            )

        approval = generation_approval(approval_timestamp=" 2026-05-08T14:22:54+10:00 ")
        with self.assertRaisesRegex(ValueError, "approval_timestamp rejects invalid timestamp format"):
            build_offline_rtm_ledger_fixture(
                published_input_fixture(),
                active_vault_backend_fixture=backend_fixture(),
                generation_approval=approval,
                rtm_id="RTM-030-001",
            )

    def test_approval_identity_mismatches_fail_closed(self):
        for field, value, expected in [
            ("approved_input_id", "PBI-030-999", "approved_input_id does not match"),
            ("approved_beo_hash", HASH_D, "approved_beo_hash does not match"),
            ("approved_backend_manifest_hash", HASH_D, "approved_backend_manifest_hash does not match"),
            ("approved_output_id", "RTM-030-999", "approved_output_id does not match"),
        ]:
            with self.subTest(field=field):
                approval = generation_approval()
                approval[field] = value
                with self.assertRaisesRegex(ValueError, expected):
                    build_offline_rtm_ledger_fixture(
                        published_input_fixture(),
                        active_vault_backend_fixture=backend_fixture(),
                        generation_approval=approval,
                        rtm_id="RTM-030-001",
                    )

    def test_blk033_boundary_doc_and_implementation_have_no_live_surface(self):
        self.assertTrue(BLK033.exists(), "BLK-033 offline RTM generation boundary missing")
        text = BLK033.read_text()
        required = [
            "Offline RTM generation boundary",
            "OFFLINE_RTM_GENERATION_APPROVAL_FIXTURE_ONLY",
            "OFFLINE_RTM_LEDGER_GENERATED_FIXTURE_ONLY",
            "OFFLINE_RTM_COVERAGE_MATRIX_FIXTURE_ONLY",
            "DRIFT_REVIEW_REQUIRED_NOT_REJECTED",
            "PROTECTED_BODY_NOT_READ",
            "ACTIVE_VAULT_NOT_SCANNED",
            "BEO_PUBLICATION_NOT_PERFORMED",
            "NO_SIGNER_STORAGE_OR_PUBLIC_LEDGER_SIDE_EFFECTS",
            "does not read protected BLK-req vault bodies",
            "does not scan active-vault paths",
            "does not publish BEOs",
            "does not reject drift",
            "does not inherit approval",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-033 markers missing: {missing}")

        implementation_text = IMPLEMENTATION.read_text()
        forbidden_live_markers = [
            "import subprocess",
            "from subprocess",
            "import socket",
            "import requests",
            "import urllib",
            "http.client",
            "from pathlib",
            "Path(",
            "read_text",
            "glob(",
            "rglob(",
            "os.system",
            "Popen",
            "shell=True",
            "eval(",
            "exec(",
            "__import__",
            "open(",
            "discord",
            "github",
            "publish_authoritative_beo",
            "active_vault_scanner",
            "protected_vault_body_reader",
            "drift_decision_runtime",
        ]
        offenders = [marker for marker in forbidden_live_markers if marker in implementation_text]
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
