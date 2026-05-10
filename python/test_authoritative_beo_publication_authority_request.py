import copy
import unittest

from authoritative_beo_publication_authority_request import (
    AUTHORITY_REQUEST_READY,
    EXACT_EXCLUDED_AUTHORITIES,
    build_authoritative_beo_publication_authority_request,
)


HASH_A = "sha256:" + "a" * 64
HASH_B = "sha256:" + "b" * 64
HASH_C = "sha256:" + "c" * 64
HASH_D = "sha256:" + "d" * 64
HASH_E = "sha256:" + "e" * 64
HASH_F = "sha256:" + "f" * 64


def valid_inputs():
    source_candidate = {
        "candidate_id": "BEO-CANDIDATE-054-001",
        "candidate_status": "PUBLICATION_CANDIDATE_FIXTURE_ONLY",
        "beo_id": "BEO-054-001",
        "beo_hash": HASH_A,
        "beb_id": "BEB-054-001",
        "status": "PASS",
        "source_evidence": {
            "run_id": "RUN-BLK-SYSTEM-052-001",
            "tool_name": "run_ast_validation",
            "source_evidence_hash": HASH_B,
            "cleanup_status": "CLEANED",
        },
        "trace_artifacts": [{"kind": "REQ", "id": "REQ-001", "version_hash": HASH_C}],
        "beo_publication": "DRAFT_ONLY",
        "rtm_status": "NOT_GENERATED",
        "published": False,
        "active_vault_read": False,
        "key_material_accessed": False,
        "immutable_storage_written": False,
        "public_ledger_mutated": False,
        "rollback_executed": False,
    }
    approval_request = {
        "request_id": "AUTH-BEO-PUB-REQ-054-001",
        "operator_identity": "discord:684235178083745819",
        "request_hash": HASH_D,
        "approved_candidate_id": "BEO-CANDIDATE-054-001",
        "approved_beo_id": "BEO-054-001",
        "approved_beo_hash": HASH_A,
        "source_evidence_hash": HASH_B,
        "approval_scope": "AUTHORITATIVE_BEO_PUBLICATION_AUTHORITY_REQUEST_ONLY",
        "requested_at": "2026-05-10T13:00:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    signer_policy = {
        "signer_identity": "fixture-signer-policy-054",
        "signer_policy_hash": HASH_E,
        "key_material_accessed": False,
        "signature_generated": False,
        "secret_read": False,
    }
    storage_policy = {
        "storage_target_identity": "fixture-immutable-storage-policy-054",
        "storage_policy_hash": HASH_F,
        "immutable_storage_written": False,
        "storage_write_attempted": False,
    }
    ledger_policy = {
        "ledger_target_identity": "fixture-public-ledger-policy-054",
        "ledger_policy_hash": HASH_C,
        "public_ledger_mutated": False,
        "ledger_append_attempted": False,
    }
    rollback_policy = {
        "rollback_policy_hash": HASH_D,
        "rollback_fixture_identity": "fixture-rollback-policy-054",
        "rollback_executed": False,
        "revocation_executed": False,
        "supersession_executed": False,
    }
    return source_candidate, approval_request, signer_policy, storage_policy, ledger_policy, rollback_policy


class AuthoritativeBeoPublicationAuthorityRequestTest(unittest.TestCase):
    def _build(self, **overrides):
        args = list(valid_inputs())
        names = ["source_candidate", "approval_request", "signer_policy", "storage_policy", "ledger_policy", "rollback_policy"]
        mapped = dict(zip(names, args))
        mapped.update(overrides)
        return build_authoritative_beo_publication_authority_request(**mapped)

    def test_builds_request_ready_for_human_review_without_publication_side_effects(self):
        request = self._build()

        self.assertEqual(request["request_status"], AUTHORITY_REQUEST_READY)
        self.assertEqual(request["candidate_id"], "BEO-CANDIDATE-054-001")
        self.assertEqual(request["beo_id"], "BEO-054-001")
        self.assertEqual(request["beo_hash"], HASH_A)
        self.assertEqual(request["source_evidence_hash"], HASH_B)
        self.assertEqual(set(request["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        self.assertFalse(request["publication_performed"])
        self.assertFalse(request["live_publication_approval_captured"])
        self.assertFalse(request["signature_generated"])
        self.assertFalse(request["key_material_accessed"])
        self.assertFalse(request["immutable_storage_written"])
        self.assertFalse(request["public_ledger_mutated"])
        self.assertFalse(request["rollback_executed"])
        self.assertFalse(request["revocation_executed"])
        self.assertFalse(request["supersession_executed"])
        self.assertFalse(request["rtm_generated"])
        self.assertFalse(request["drift_decision_made"])
        self.assertFalse(request["protected_body_read"])

    def test_rejects_publication_rtm_protected_body_and_secret_laundering(self):
        candidate, approval, signer, storage, ledger, rollback = valid_inputs()
        hostile_cases = [
            ("candidate publication wording", "source_candidate", {"operator_note": "PASS evidence approved for authoritative BEO publication now"}, "authority-laundering text"),
            ("candidate rtm field", "source_candidate", {"rtm_id": "RTM-001"}, "forbidden authority field"),
            ("candidate protected path", "source_candidate", {"evidence_ref": "docs/active/REQ-001.md"}, "protected BLK-req body reference"),
            ("approval live capture", "approval_request", {"live_publication_approval_captured": True}, "forbidden authority field"),
            ("signer secret", "signer_policy", {"private_key": "SECRET"}, "secret-bearing field"),
            ("storage side effect", "storage_policy", {"immutable_storage_written": True}, "immutable_storage_written must be false"),
            ("ledger side effect", "ledger_policy", {"public_ledger_mutated": True}, "public_ledger_mutated must be false"),
            ("rollback side effect", "rollback_policy", {"rollback_executed": True}, "rollback_executed must be false"),
        ]
        for _label, target, patch, message in hostile_cases:
            values = {
                "source_candidate": copy.deepcopy(candidate),
                "approval_request": copy.deepcopy(approval),
                "signer_policy": copy.deepcopy(signer),
                "storage_policy": copy.deepcopy(storage),
                "ledger_policy": copy.deepcopy(ledger),
                "rollback_policy": copy.deepcopy(rollback),
            }
            values[target].update(patch)
            with self.subTest(_label):
                with self.assertRaisesRegex(ValueError, message):
                    build_authoritative_beo_publication_authority_request(**values)

    def test_rejects_stale_replayed_expired_mismatched_or_bad_excluded_authority_requests(self):
        for flag in ["expired", "replayed", "stale"]:
            candidate, approval, signer, storage, ledger, rollback = valid_inputs()
            approval[flag] = True
            with self.subTest(flag=flag):
                with self.assertRaisesRegex(ValueError, f"approval_request must not be {flag}"):
                    build_authoritative_beo_publication_authority_request(candidate, approval, signer, storage, ledger, rollback)

        candidate, approval, signer, storage, ledger, rollback = valid_inputs()
        approval["approved_beo_hash"] = HASH_F
        with self.assertRaisesRegex(ValueError, "approved_beo_hash does not match source candidate"):
            build_authoritative_beo_publication_authority_request(candidate, approval, signer, storage, ledger, rollback)

        candidate, approval, signer, storage, ledger, rollback = valid_inputs()
        del approval["excluded_authorities"]
        with self.assertRaisesRegex(ValueError, "excluded_authorities must match exact denied authority set"):
            build_authoritative_beo_publication_authority_request(candidate, approval, signer, storage, ledger, rollback)

        candidate, approval, signer, storage, ledger, rollback = valid_inputs()
        approval["excluded_authorities"] = sorted(EXACT_EXCLUDED_AUTHORITIES - {"RTM_GENERATION"})
        with self.assertRaisesRegex(ValueError, "excluded_authorities must match exact denied authority set"):
            build_authoritative_beo_publication_authority_request(candidate, approval, signer, storage, ledger, rollback)

    def test_rejects_open_schema_camelcase_constants_duplicate_exclusions_and_trace_mismatch(self):
        hostile_cases = [
            ("approval camelcase", "approval_request", {"publicationAuthority": True}, "unexpected field"),
            ("candidate runtime state", "source_candidate", {"runtime_state": "PUBLISHED"}, "unexpected field"),
            ("signer privateKey", "signer_policy", {"privateKey": "SECRET"}, "secret-bearing field"),
            ("approval trace mismatch", "approval_request", {"trace_artifacts": [{"kind": "REQ", "id": "REQ-001", "version_hash": HASH_F}]}, "unexpected field"),
            ("candidate source evidence extra", "source_candidate_source_evidence", {"privateKey": "SECRET"}, "unexpected field"),
            ("candidate trace artifact extra", "source_candidate_trace_artifact", {"publicationAuthority": True}, "unexpected field"),
            ("candidate nested camelcase publication", "source_candidate_operator_note", {"publicationAuthority": True}, "forbidden authority field"),
            ("candidate nested camelcase runtime output", "source_candidate_operator_note", {"runtimePublishedBeoOutput": True}, "forbidden authority field"),
            ("candidate nested camelcase signer material", "source_candidate_operator_note", {"signerKeyMaterial": "SECRET"}, "secret-bearing field"),
            ("candidate nested uppercase private key", "source_candidate_operator_note", {"PRIVATEKEY": "SECRET"}, "secret-bearing field"),
            ("candidate nested uppercase api key", "source_candidate_operator_note", {"APIKEY": "SECRET"}, "secret-bearing field"),
            ("candidate nested rtm generation", "source_candidate_operator_note", {"RTMGeneration": True}, "forbidden authority field"),
            ("candidate nested rtm id", "source_candidate_operator_note", {"RTMID": "RTM-054-001"}, "forbidden authority field"),
            ("candidate nested active vault comparison", "source_candidate_operator_note", {"ActiveVaultHashComparison": True}, "forbidden authority field"),
            ("candidate nested signature", "source_candidate_operator_note", {"SignatureGenerated": True}, "forbidden authority field"),
            ("candidate nested cryptographic signing", "source_candidate_operator_note", {"CryptographicSigning": True}, "forbidden authority field"),
            ("candidate nested published marker", "source_candidate_operator_note", {"PUBLISHED": True}, "forbidden authority field"),
            ("candidate nested published at", "source_candidate_operator_note", {"publishedAt": "2026-05-10T00:00:00Z"}, "forbidden authority field"),
            ("candidate nested publication performed", "source_candidate_operator_note", {"publicationPerformed": True}, "forbidden authority field"),
            ("candidate nested public ledger mutated", "source_candidate_operator_note", {"publicLedgerMutated": True}, "forbidden authority field"),
            ("candidate nested immutable storage written", "source_candidate_operator_note", {"immutableStorageWritten": True}, "forbidden authority field"),
            ("candidate nested storage write attempted", "source_candidate_operator_note", {"storageWriteAttempted": True}, "forbidden authority field"),
            ("candidate nested ledger append attempted", "source_candidate_operator_note", {"ledgerAppendAttempted": True}, "forbidden authority field"),
            ("candidate nested rollback executed", "source_candidate_operator_note", {"rollbackExecuted": True}, "forbidden authority field"),
            ("candidate nested revocation executed", "source_candidate_operator_note", {"revocationExecuted": True}, "forbidden authority field"),
            ("candidate nested supersession executed", "source_candidate_operator_note", {"supersessionExecuted": True}, "forbidden authority field"),
            ("candidate nested authoritative compact", "source_candidate_operator_note", {"authoritativeBEOpublication": True}, "forbidden authority field"),
            ("candidate nested authoritative allcaps", "source_candidate_operator_note", {"AUTHORITATIVEBEOPUBLICATION": True}, "forbidden authority field"),
            ("candidate nested beo pub approved", "source_candidate_operator_note", {"beoPubApproved": True}, "forbidden authority field"),
            ("candidate nested abp approved", "source_candidate_operator_note", {"ABPApproved": True}, "forbidden authority field"),
            ("candidate nested approval inherited", "source_candidate_operator_note", {"approvalInherited": True}, "forbidden authority field"),
            ("candidate nested codex approval", "source_candidate_operator_note", {"codexApproval": True}, "forbidden authority field"),
            ("candidate nested blk test pass", "source_candidate_operator_note", {"blkTestPassApproval": True}, "forbidden authority field"),
            ("candidate camelcase text", "source_candidate", {"operator_note": "authoritativeBeoPublication approved"}, "authority-laundering text"),
            ("candidate rtm generation text", "source_candidate", {"operator_note": "RTMGeneration complete"}, "authority-laundering text"),
            ("candidate rtm id text", "source_candidate", {"operator_note": "RTMID RTM-054-001"}, "authority-laundering text"),
            ("candidate active vault text", "source_candidate", {"operator_note": "ActiveVaultHashComparison complete"}, "authority-laundering text"),
            ("candidate signature text", "source_candidate", {"operator_note": "SignatureGenerated true"}, "authority-laundering text"),
            ("candidate cryptographic signing text", "source_candidate", {"operator_note": "CryptographicSigning complete"}, "authority-laundering text"),
            ("candidate beo pub approved text", "source_candidate", {"operator_note": "BEO pub approved"}, "authority-laundering text"),
            ("candidate auth beo pub text", "source_candidate", {"operator_note": "auth BEO pub approved"}, "authority-laundering text"),
            ("candidate abp approved text", "source_candidate", {"operator_note": "ABP approved"}, "authority-laundering text"),
            ("candidate rtpbeo text", "source_candidate", {"operator_note": "RTPBEO output"}, "authority-laundering text"),
            ("candidate compact public ledger text", "source_candidate", {"operator_note": "publicLedgerMutated"}, "authority-laundering text"),
            ("candidate compact immutable storage text", "source_candidate", {"operator_note": "immutableStorageWritten"}, "authority-laundering text"),
            ("candidate publication authorized text", "source_candidate", {"operator_note": "BEO publication authorized"}, "authority-laundering text"),
            ("candidate publication authorization text", "source_candidate", {"operator_note": "BEO publication authorization granted"}, "authority-laundering text"),
            ("candidate publication approval granted text", "source_candidate", {"operator_note": "publication approval granted for BEO-054-001"}, "authority-laundering text"),
            ("candidate publication permitted text", "source_candidate", {"operator_note": "BEO publication permitted by operator"}, "authority-laundering text"),
            ("candidate publication authorised text", "source_candidate", {"operator_note": "BEO publication authorised by operator"}, "authority-laundering text"),
            ("candidate publication authorisation text", "source_candidate", {"operator_note": "BEO publication authorisation granted"}, "authority-laundering text"),
            ("candidate publication authority granted text", "source_candidate", {"operator_note": "publication authority granted for BEO-054-001"}, "authority-laundering text"),
            ("candidate approved for publication text", "source_candidate", {"operator_note": "BEO-054-001 approved for publication"}, "authority-laundering text"),
            ("candidate publication greenlit text", "source_candidate", {"operator_note": "BEO publication greenlit by operator"}, "authority-laundering text"),
            ("candidate publication allowed text", "source_candidate", {"operator_note": "BEO publication allowed by operator"}, "authority-laundering text"),
            ("candidate backslash protected path", "source_candidate", {"evidence_ref": r"docs\\active\\REQ-001.md"}, "protected BLK-req body reference"),
            ("candidate directory protected path", "source_candidate", {"evidence_ref": "docs/active"}, "protected BLK-req body reference"),
            ("candidate encoded protected path", "source_candidate", {"evidence_ref": "docs%2Factive%2FREQ-001.md"}, "protected BLK-req body reference"),
            ("candidate parent protected path", "source_candidate", {"evidence_ref": "../docs/active"}, "protected BLK-req body reference"),
            ("candidate query protected path", "source_candidate", {"evidence_ref": "docs/active?raw=1"}, "protected BLK-req body reference"),
            ("candidate double encoded protected path", "source_candidate", {"evidence_ref": "docs%252Factive%252FREQ-001.md"}, "protected BLK-req body reference"),
            ("candidate url query encoded protected path", "source_candidate", {"evidence_ref": "https://example.invalid/view?file=docs%2Factive%2FREQ-001.md"}, "protected BLK-req body reference"),
            ("candidate url hash encoded protected path", "source_candidate", {"evidence_ref": "https://example.invalid/view#docs%252Factive%252FREQ-001.md"}, "protected BLK-req body reference"),
            ("approval inherited blk-test pass", "approval_request", {"request_id": "BLK-test PASS approval reused"}, "authority-laundering text"),
            ("approval explicit inherited text", "approval_request", {"request_id": "approval inherited from BLK-test PASS"}, "authority-laundering text"),
            ("approval inherit text", "approval_request", {"request_id": "inherit approval from BLK-test PASS"}, "authority-laundering text"),
            ("approval reused as text", "approval_request", {"request_id": "BLK test PASS reused as approval"}, "authority-laundering text"),
            ("approval publication authority granted", "approval_request", {"request_id": "publication authority granted for BEO-054-001"}, "authority-laundering text"),
            ("approval approved for publication", "approval_request", {"request_id": "BEO-054-001 approved for publication"}, "authority-laundering text"),
            ("candidate constant", "source_candidate", {"operator_note": "AUTHORITATIVE_BEO_PUBLICATION approved"}, "authority-laundering text"),
            ("candidate published status text", "source_candidate", {"operator_note": "PUBLISHED"}, "authority-laundering text"),
        ]
        for _label, target, patch, message in hostile_cases:
            values = dict(zip(["source_candidate", "approval_request", "signer_policy", "storage_policy", "ledger_policy", "rollback_policy"], valid_inputs()))
            if target == "source_candidate_source_evidence":
                values["source_candidate"]["source_evidence"].update(patch)
            elif target == "source_candidate_trace_artifact":
                values["source_candidate"]["trace_artifacts"][0].update(patch)
            elif target == "source_candidate_operator_note":
                values["source_candidate"]["operator_note"] = patch
            else:
                values[target].update(patch)
            with self.subTest(_label):
                with self.assertRaisesRegex(ValueError, message):
                    build_authoritative_beo_publication_authority_request(**values)

        candidate, approval, signer, storage, ledger, rollback = valid_inputs()
        approval["excluded_authorities"] = sorted(EXACT_EXCLUDED_AUTHORITIES) + ["RTM_GENERATION"]
        with self.assertRaisesRegex(ValueError, "excluded_authorities must match exact denied authority set"):
            build_authoritative_beo_publication_authority_request(candidate, approval, signer, storage, ledger, rollback)

        candidate, approval, signer, storage, ledger, rollback = valid_inputs()
        approval["excluded_authorities"] = sorted(EXACT_EXCLUDED_AUTHORITIES) + [{"RTM_GENERATION": True}]
        with self.assertRaisesRegex(ValueError, "excluded_authorities must match exact denied authority set"):
            build_authoritative_beo_publication_authority_request(candidate, approval, signer, storage, ledger, rollback)

        candidate, approval, signer, storage, ledger, rollback = valid_inputs()
        self.assertIn("COVERAGE_MATRIX", EXACT_EXCLUDED_AUTHORITIES)
        self.assertIn("COVERAGE_CLAIM", EXACT_EXCLUDED_AUTHORITIES)
        self.assertIn("DRIFT_DECISION", EXACT_EXCLUDED_AUTHORITIES)

    def test_rejects_published_candidates_and_bad_evidence_as_publication_authority(self):
        candidate, approval, signer, storage, ledger, rollback = valid_inputs()
        candidate["beo_publication"] = "PUBLISHED"
        with self.assertRaisesRegex(ValueError, "beo_publication must remain DRAFT_ONLY"):
            build_authoritative_beo_publication_authority_request(candidate, approval, signer, storage, ledger, rollback)

        candidate, approval, signer, storage, ledger, rollback = valid_inputs()
        candidate["status"] = "FAIL"
        with self.assertRaisesRegex(ValueError, "source candidate status must be PASS for publication authority request"):
            build_authoritative_beo_publication_authority_request(candidate, approval, signer, storage, ledger, rollback)

        candidate, approval, signer, storage, ledger, rollback = valid_inputs()
        candidate["status"] = "BLOCKED"
        with self.assertRaisesRegex(ValueError, "source candidate status must be PASS or FAIL"):
            build_authoritative_beo_publication_authority_request(candidate, approval, signer, storage, ledger, rollback)

        candidate, approval, signer, storage, ledger, rollback = valid_inputs()
        candidate["source_evidence"]["cleanup_status"] = "DIRTY"
        with self.assertRaisesRegex(ValueError, "cleanup_status must be CLEANED"):
            build_authoritative_beo_publication_authority_request(candidate, approval, signer, storage, ledger, rollback)


if __name__ == "__main__":
    unittest.main()
