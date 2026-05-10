import copy
import unittest

from authoritative_beo_publication_authority_request import (
    EXACT_EXCLUDED_AUTHORITIES as REQUEST_EXCLUDED_AUTHORITIES,
    _canonical_hash,
    build_authoritative_beo_publication_authority_request,
)
from test_authoritative_beo_publication_authority_request import HASH_A, HASH_B, HASH_C, HASH_D, HASH_E, HASH_F, valid_inputs

from authoritative_beo_publication_approval_envelope import (
    APPROVAL_ENVELOPE_READY,
    EXACT_EXCLUDED_AUTHORITIES,
    build_authoritative_beo_publication_approval_envelope,
)

HASH_G = "sha256:" + "1" * 64
HASH_H = "sha256:" + "2" * 64
HASH_I = "sha256:" + "3" * 64


def valid_envelope_inputs():
    request = build_authoritative_beo_publication_authority_request(*valid_inputs())
    publication_target = {
        "target_id": "BEO-PUBLICATION-TARGET-055-001",
        "target_kind": "FIXTURE_PUBLICATION_TARGET_ONLY",
        "target_ref": "fixture://beo-publication-targets/055/001",
        "beo_id": request["beo_id"],
        "beo_hash": request["beo_hash"],
        "candidate_id": request["candidate_id"],
        "source_evidence_hash": request["source_evidence_hash"],
        "immutable_storage_written": False,
        "public_ledger_mutated": False,
        "publication_performed": False,
        "operator_note": "exact target envelope fixture only",
    }
    approval_envelope = {
        "envelope_id": "BEO-PUB-APPROVAL-ENVELOPE-055-001",
        "operator_identity": "discord:684235178083745819",
        "approval_scope": "AUTHORITATIVE_BEO_PUBLICATION_APPROVAL_ENVELOPE_ONLY_NOT_PUBLICATION",
        "approved_request_id": request["request_id"],
        "approved_request_hash": request["request_hash"],
        "approved_target_id": publication_target["target_id"],
        "approved_beo_id": request["beo_id"],
        "approved_beo_hash": request["beo_hash"],
        "source_evidence_hash": request["source_evidence_hash"],
        "pilot_id": "BEO-PUBLICATION-PILOT-055-001",
        "run_id": "RUN-BLK-SYSTEM-055-PUBLICATION-PILOT-001",
        "approval_id": "APPROVAL-BLK-SYSTEM-055-BEO-PUBLICATION-001",
        "requested_at": "2099-05-10T15:30:00+10:00",
        "expires_at": "2099-05-10T16:30:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    signer_policy = {
        "signer_identity": "fixture-signer-policy-055",
        "signer_policy_hash": HASH_E,
        "key_material_accessed": False,
        "signature_generated": False,
        "secret_read": False,
    }
    storage_policy = {
        "storage_target_identity": "fixture-immutable-storage-policy-055",
        "storage_policy_hash": HASH_F,
        "immutable_storage_written": False,
        "storage_write_attempted": False,
    }
    ledger_policy = {
        "ledger_target_identity": "fixture-public-ledger-policy-055",
        "ledger_policy_hash": HASH_G,
        "public_ledger_mutated": False,
        "ledger_append_attempted": False,
    }
    rollback_policy = {
        "rollback_policy_hash": HASH_H,
        "rollback_fixture_identity": "fixture-rollback-policy-055",
        "rollback_executed": False,
        "revocation_executed": False,
        "supersession_executed": False,
    }
    audit_bundle = {
        "audit_bundle_id": "AUDIT-BEO-PUB-055-001",
        "audit_bundle_hash": HASH_I,
        "request_hash": request["request_hash"],
        "beo_hash": request["beo_hash"],
        "source_evidence_hash": request["source_evidence_hash"],
        "protected_body_read": False,
        "rtm_generated": False,
        "drift_decision_made": False,
    }
    pilot_controls = {
        "operator_stop_control": "discord-stop-required-before-runtime",
        "max_output_bytes": 20000,
        "timeout_seconds": 300,
        "single_run_only": True,
        "replay_protection": "fresh-approval-and-run-id-required",
        "publication_performed": False,
        "signature_generated": False,
        "immutable_storage_written": False,
        "public_ledger_mutated": False,
        "rollback_executed": False,
        "rtm_generated": False,
        "protected_body_read": False,
    }
    return (
        request,
        publication_target,
        approval_envelope,
        signer_policy,
        storage_policy,
        ledger_policy,
        rollback_policy,
        audit_bundle,
        pilot_controls,
    )


class AuthoritativeBeoPublicationApprovalEnvelopeTest(unittest.TestCase):
    def _build(self, **overrides):
        names = [
            "authority_request_package",
            "publication_target",
            "approval_envelope",
            "signer_policy",
            "storage_policy",
            "ledger_policy",
            "rollback_policy",
            "audit_bundle",
            "pilot_controls",
        ]
        mapped = dict(zip(names, valid_envelope_inputs()))
        mapped.update(overrides)
        return build_authoritative_beo_publication_approval_envelope(**mapped)

    def test_builds_approval_envelope_ready_for_human_review_without_publication_side_effects(self):
        envelope = self._build()

        self.assertEqual(envelope["envelope_status"], APPROVAL_ENVELOPE_READY)
        self.assertEqual(envelope["beo_id"], "BEO-054-001")
        self.assertEqual(envelope["pilot_id"], "BEO-PUBLICATION-PILOT-055-001")
        self.assertEqual(envelope["requested_at"], "2099-05-10T15:30:00+10:00")
        self.assertEqual(envelope["expires_at"], "2099-05-10T16:30:00+10:00")
        self.assertEqual(set(envelope["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        self.assertFalse(envelope["publication_performed"])
        self.assertFalse(envelope["runtime_published_beo_output"])
        self.assertFalse(envelope["live_publication_approval_captured"])
        self.assertFalse(envelope["signature_generated"])
        self.assertFalse(envelope["key_material_accessed"])
        self.assertFalse(envelope["immutable_storage_written"])
        self.assertFalse(envelope["public_ledger_mutated"])
        self.assertFalse(envelope["rollback_executed"])
        self.assertFalse(envelope["revocation_executed"])
        self.assertFalse(envelope["supersession_executed"])
        self.assertFalse(envelope["rtm_generated"])
        self.assertFalse(envelope["drift_decision_made"])
        self.assertFalse(envelope["protected_body_read"])
        self.assertIn("envelope_hash", envelope)

    def test_rejects_mismatched_upstream_request_target_and_evidence_identity(self):
        cases = [
            ("bad request status", "authority_request_package", {"request_status": "PUBLISHED"}, "authority request package must be BLK-057 request-ready"),
            ("bad request exclusions", "authority_request_package", {"excluded_authorities": sorted(REQUEST_EXCLUDED_AUTHORITIES - {"RTM_GENERATION"})}, "authority_request_package excluded_authorities must match BLK-057 denied authority set"),
            ("bad request trace", "authority_request_package", {"trace_artifacts": [{"kind": "REQ", "id": "REQ-001", "version_hash": "bad"}]}, "version_hash must be a sha256 hash"),
            ("bad target beo", "publication_target", {"beo_id": "BEO-OTHER"}, "publication target beo_id does not match request"),
            ("bad target hash", "publication_target", {"beo_hash": HASH_F}, "publication target beo_hash does not match request"),
            ("bad approval request hash", "approval_envelope", {"approved_request_hash": HASH_F}, "approved_request_hash does not match request"),
            ("bad approval evidence", "approval_envelope", {"source_evidence_hash": HASH_F}, "approval source_evidence_hash does not match request"),
            ("bad audit evidence", "audit_bundle", {"source_evidence_hash": HASH_F}, "audit_bundle source_evidence_hash does not match request"),
        ]
        for label, target, patch, message in cases:
            mapped = dict(zip([
                "authority_request_package", "publication_target", "approval_envelope", "signer_policy", "storage_policy", "ledger_policy", "rollback_policy", "audit_bundle", "pilot_controls"
            ], valid_envelope_inputs()))
            mapped[target] = copy.deepcopy(mapped[target])
            mapped[target].update(patch)
            with self.subTest(label):
                with self.assertRaisesRegex(ValueError, message):
                    build_authoritative_beo_publication_approval_envelope(**mapped)

    def test_rejects_forged_or_laundered_upstream_authority_request_packages(self):
        inputs = list(valid_envelope_inputs())
        request = copy.deepcopy(inputs[0])
        request["candidate_id"] = "BEO-CANDIDATE-FORGED-055"
        request["request_hash"] = HASH_G
        target = copy.deepcopy(inputs[1])
        target["candidate_id"] = request["candidate_id"]
        approval = copy.deepcopy(inputs[2])
        approval["approved_request_hash"] = request["request_hash"]
        audit = copy.deepcopy(inputs[7])
        audit["request_hash"] = request["request_hash"]
        inputs[0], inputs[1], inputs[2], inputs[7] = request, target, approval, audit
        with self.assertRaisesRegex(ValueError, "request_hash does not match canonical authority request package"):
            build_authoritative_beo_publication_approval_envelope(*inputs)

        inputs = list(valid_envelope_inputs())
        request = copy.deepcopy(inputs[0])
        request["signer_policy"] = copy.deepcopy(request["signer_policy"])
        request["signer_policy"]["secret_read"] = True
        request["request_hash"] = _canonical_hash({k: v for k, v in request.items() if k != "request_hash"})
        approval = copy.deepcopy(inputs[2])
        approval["approved_request_hash"] = request["request_hash"]
        audit = copy.deepcopy(inputs[7])
        audit["request_hash"] = request["request_hash"]
        inputs[0], inputs[2], inputs[7] = request, approval, audit
        with self.assertRaisesRegex(ValueError, "secret_read must be false"):
            build_authoritative_beo_publication_approval_envelope(*inputs)

        for label, trace_patch, message in [
            ("protected path", {"id": "docs/active/REQ-001.md"}, "protected BLK-req body reference"),
            ("rtm kind", {"kind": "RTMGeneration"}, "authority-laundering text"),
            ("arbitrary kind", {"kind": "ARBITRARY"}, "trace artifact kind must be REQ, UC, BEB, BEO, BLK, or EVIDENCE"),
        ]:
            inputs = list(valid_envelope_inputs())
            request = copy.deepcopy(inputs[0])
            request["trace_artifacts"] = [dict(request["trace_artifacts"][0], **trace_patch)]
            request["request_hash"] = _canonical_hash({k: v for k, v in request.items() if k != "request_hash"})
            approval = copy.deepcopy(inputs[2])
            approval["approved_request_hash"] = request["request_hash"]
            audit = copy.deepcopy(inputs[7])
            audit["request_hash"] = request["request_hash"]
            inputs[0], inputs[2], inputs[7] = request, approval, audit
            with self.subTest(label=label):
                with self.assertRaisesRegex(ValueError, message):
                    build_authoritative_beo_publication_approval_envelope(*inputs)

    def test_rejects_missing_policy_bindings_and_malformed_or_expired_timestamps(self):
        for target, removed_key, message in [
            ("signer_policy", "signer_policy_hash", "signer_policy missing required field: signer_policy_hash"),
            ("storage_policy", "storage_policy_hash", "storage_policy missing required field: storage_policy_hash"),
            ("ledger_policy", "ledger_append_attempted", "ledger_policy missing required field: ledger_append_attempted"),
            ("rollback_policy", "revocation_executed", "rollback_policy missing required field: revocation_executed"),
        ]:
            names = [
                "authority_request_package", "publication_target", "approval_envelope", "signer_policy", "storage_policy", "ledger_policy", "rollback_policy", "audit_bundle", "pilot_controls"
            ]
            mapped = dict(zip(names, valid_envelope_inputs()))
            mapped[target] = copy.deepcopy(mapped[target])
            del mapped[target][removed_key]
            with self.subTest(target=target, removed_key=removed_key):
                with self.assertRaisesRegex(ValueError, message):
                    build_authoritative_beo_publication_approval_envelope(**mapped)

        timestamp_cases = [
            ({"requested_at": "not-a-time"}, "requested_at must be an ISO-8601 timestamp with timezone"),
            ({"expires_at": "not-a-time"}, "expires_at must be an ISO-8601 timestamp with timezone"),
            ({"requested_at": "2099-05-10T17:30:00+10:00", "expires_at": "2099-05-10T16:30:00+10:00"}, "expires_at must be after requested_at"),
            ({"requested_at": "2020-01-01T00:00:00+00:00", "expires_at": "2020-01-01T01:00:00+00:00"}, "expires_at must be in the future"),
        ]
        for patch, message in timestamp_cases:
            inputs = list(valid_envelope_inputs())
            approval = copy.deepcopy(inputs[2])
            approval.update(patch)
            inputs[2] = approval
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_authoritative_beo_publication_approval_envelope(*inputs)

    def test_rejects_stale_replayed_expired_or_bad_excluded_authority_envelopes(self):
        for flag in ["expired", "replayed", "stale"]:
            inputs = list(valid_envelope_inputs())
            approval = copy.deepcopy(inputs[2])
            approval[flag] = True
            inputs[2] = approval
            with self.subTest(flag=flag):
                with self.assertRaisesRegex(ValueError, f"approval_envelope must not be {flag}"):
                    build_authoritative_beo_publication_approval_envelope(*inputs)

        inputs = list(valid_envelope_inputs())
        approval = copy.deepcopy(inputs[2])
        approval["excluded_authorities"] = sorted(EXACT_EXCLUDED_AUTHORITIES - {"RTM_GENERATION"})
        inputs[2] = approval
        with self.assertRaisesRegex(ValueError, "excluded_authorities must match exact denied authority set"):
            build_authoritative_beo_publication_approval_envelope(*inputs)

        inputs = list(valid_envelope_inputs())
        approval = copy.deepcopy(inputs[2])
        approval["excluded_authorities"] = sorted(EXACT_EXCLUDED_AUTHORITIES) + ["RTM_GENERATION"]
        inputs[2] = approval
        with self.assertRaisesRegex(ValueError, "excluded_authorities must match exact denied authority set"):
            build_authoritative_beo_publication_approval_envelope(*inputs)

    def test_rejects_publication_side_effects_secrets_rtm_and_protected_path_laundering(self):
        cases = [
            ("target performs publication", "publication_target", {"publication_performed": True}, "publication_performed must be false"),
            ("signer key", "signer_policy", {"privateKey": "SECRET"}, "secret-bearing field"),
            ("storage write", "storage_policy", {"immutable_storage_written": True}, "immutable_storage_written must be false"),
            ("ledger append", "ledger_policy", {"ledger_append_attempted": True}, "ledger_append_attempted must be false"),
            ("rollback execute", "rollback_policy", {"rollback_executed": True}, "rollback_executed must be false"),
            ("audit rtm", "audit_bundle", {"RTMGeneration": True}, "forbidden authority field"),
            ("pilot signature", "pilot_controls", {"signature_generated": True}, "signature_generated must be false"),
            ("target protected path", "publication_target", {"target_ref": "docs%252Factive%252FREQ-001.md"}, "protected BLK-req body reference"),
        ]
        for label, target, patch, message in cases:
            mapped = dict(zip([
                "authority_request_package", "publication_target", "approval_envelope", "signer_policy", "storage_policy", "ledger_policy", "rollback_policy", "audit_bundle", "pilot_controls"
            ], valid_envelope_inputs()))
            mapped[target] = copy.deepcopy(mapped[target])
            mapped[target].update(patch)
            with self.subTest(label):
                with self.assertRaisesRegex(ValueError, message):
                    build_authoritative_beo_publication_approval_envelope(**mapped)

    def test_rejects_inherited_approval_and_compact_authority_laundering_text(self):
        hostile_texts = [
            "BLK-test PASS approval inherited; publishBEO allowed",
            "BLK-pipe success means BEO publication authorized",
            "Codex approval greenlit authoritativeBEOpublication",
            "publication authority granted for BEO-054-001",
            "approved for publication by prior request",
            "runtimePublishedBEOOutput permitted",
            "SignatureGenerated and publicLedgerMutated after pilot",
            "ActiveVaultHashComparison and RTMGeneration complete",
        ]
        for text in hostile_texts:
            inputs = list(valid_envelope_inputs())
            approval = copy.deepcopy(inputs[2])
            approval["approval_id"] = text
            inputs[2] = approval
            with self.subTest(text=text):
                with self.assertRaisesRegex(ValueError, "authority-laundering text"):
                    build_authoritative_beo_publication_approval_envelope(*inputs)

    def test_request_excluded_authority_set_remains_separate_from_publication_envelope_set(self):
        self.assertIn("AUTHORITATIVE_BEO_PUBLICATION", REQUEST_EXCLUDED_AUTHORITIES)
        self.assertIn("ACTUAL_AUTHORITATIVE_BEO_PUBLICATION", EXACT_EXCLUDED_AUTHORITIES)
        self.assertIn("LIVE_PUBLICATION_APPROVAL_CAPTURE", EXACT_EXCLUDED_AUTHORITIES)
        self.assertIn("PUBLIC_LEDGER_APPEND_OR_MUTATION", EXACT_EXCLUDED_AUTHORITIES)
        self.assertIn("GENERIC_BLK_TEST_MCP", EXACT_EXCLUDED_AUTHORITIES)
        self.assertIn("REUSABLE_BLK_TEST_SERVICE_STARTUP", EXACT_EXCLUDED_AUTHORITIES)
        self.assertIn("ARBITRARY_SHELL_OR_CALLER_SUPPLIED_COMMANDS", EXACT_EXCLUDED_AUTHORITIES)
        self.assertIn("PACKAGE_MANAGER_NETWORK_MODEL_BROWSER_OR_CYBER_TOOLING", EXACT_EXCLUDED_AUTHORITIES)
        self.assertIn("PRODUCTION_SANDBOX_OR_HOST_SECRET_ISOLATION_CLAIM", EXACT_EXCLUDED_AUTHORITIES)


if __name__ == "__main__":
    unittest.main()
