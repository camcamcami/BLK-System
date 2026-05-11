import copy
import unittest

from authoritative_beo_publication_authority_request import _canonical_hash
from blk_test_kuronode_lifecycle_cleanup_remediation_packet import (
    build_lifecycle_cleanup_remediation_packet,
    default_lifecycle_cleanup_remediation_request,
    load_committed_blk_system_073_evidence,
)
from kuronode_lifecycle_cleanup_patch_approval_envelope import (
    ALLOWED_MODIFIED_FILES,
    EXACT_EXCLUDED_AUTHORITIES,
    PATCH_APPROVAL_READY_STATUS,
    PATCH_FALSE_SIDE_EFFECT_FLAGS,
    RETIRED_BLK_SYSTEM_073_APPROVAL_ID,
    RETIRED_BLK_SYSTEM_073_RUN_ID,
    TARGET_HEAD_SHA,
    build_lifecycle_cleanup_patch_approval_envelope,
    default_lifecycle_cleanup_patch_approval_request,
)


class KuronodeLifecycleCleanupPatchApprovalEnvelopeTest(unittest.TestCase):
    def _packet(self):
        evidence = load_committed_blk_system_073_evidence()
        request = default_lifecycle_cleanup_remediation_request(evidence)
        return build_lifecycle_cleanup_remediation_packet(evidence=evidence, request=request)

    def _envelope(self, packet=None, request=None):
        selected_packet = copy.deepcopy(self._packet() if packet is None else packet)
        selected_request = copy.deepcopy(
            default_lifecycle_cleanup_patch_approval_request(selected_packet) if request is None else request
        )
        return build_lifecycle_cleanup_patch_approval_envelope(
            remediation_packet=selected_packet,
            request=selected_request,
            now="2026-05-11T14:30:00+10:00",
        )

    def test_default_envelope_is_review_ready_not_approved_not_patched(self):
        packet = self._packet()
        envelope = self._envelope(packet=packet)

        self.assertEqual(envelope["envelope_status"], PATCH_APPROVAL_READY_STATUS)
        self.assertEqual(envelope["remediation_packet_hash"], packet["packet_hash"])
        self.assertEqual(envelope["target_repo_path"], "/home/dad/code/Kuronode-v1")
        self.assertEqual(envelope["target_branch"], "main")
        self.assertEqual(envelope["target_head_sha"], TARGET_HEAD_SHA)
        self.assertEqual(envelope["allowed_modified_files"], ALLOWED_MODIFIED_FILES)
        self.assertEqual(envelope["allowed_new_files"], [])
        self.assertEqual(envelope["patch_mechanism"], "BLK_PIPE_EXACT_TARGET_PATCH_PROPOSED_NOT_EXECUTED")
        self.assertEqual(envelope["approval_state"], "READY_FOR_HUMAN_REVIEW_NOT_APPROVED_NOT_PATCHED")
        self.assertFalse(envelope["approval_granted"])
        self.assertFalse(envelope["patch_executed"])
        self.assertFalse(envelope["runtime_validation_executed"])
        self.assertEqual(set(envelope["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        self.assertIn("envelope_hash", envelope)
        for flag in sorted(PATCH_FALSE_SIDE_EFFECT_FLAGS):
            self.assertIn(flag, envelope)
            self.assertIs(envelope[flag], False, flag)

    def test_envelope_contains_required_patch_obligations_and_future_id_policy(self):
        envelope = self._envelope()
        obligations = {item["obligation_id"] for item in envelope["patch_obligations"]}
        self.assertEqual(
            obligations,
            {
                "PATCH_ADD_DETERMINISTIC_LIFECYCLE_TEARDOWN",
                "PATCH_ASSERT_NO_ESCAPED_PROCESS_OR_LISTENER",
                "PATCH_PRESERVE_TIMEOUT_AS_FAILURE",
                "PATCH_ADD_FOCUSED_CLEANUP_REGRESSION",
                "PATCH_RUN_KURONODE_CLOSEOUT_REVIEW_BEFORE_COMPLETION",
                "PATCH_REQUIRE_FRESH_BLK_TEST_RECHECK_IDS_AFTER_PATCH",
            },
        )
        self.assertEqual(envelope["future_patch_approval_id_status"], "FUTURE_CANDIDATE_NOT_CONSUMED")
        self.assertEqual(envelope["future_patch_run_id_status"], "FUTURE_CANDIDATE_NOT_CONSUMED")
        self.assertNotEqual(envelope["future_patch_approval_id"], RETIRED_BLK_SYSTEM_073_APPROVAL_ID)
        self.assertNotEqual(envelope["future_patch_run_id"], RETIRED_BLK_SYSTEM_073_RUN_ID)

    def test_rejects_forged_remediation_packet_hash_and_status(self):
        packet = self._packet()
        packet["packet_hash"] = "sha256:" + "a" * 64
        request = default_lifecycle_cleanup_patch_approval_request(packet)
        with self.assertRaisesRegex(ValueError, "remediation_packet_hash does not match recomputed packet"):
            self._envelope(packet=packet, request=request)

        packet = self._packet()
        packet["packet_status"] = "PATCH_ALREADY_DONE"
        packet["packet_hash"] = _canonical_hash({key: value for key, value in packet.items() if key != "packet_hash"})
        request = default_lifecycle_cleanup_patch_approval_request(packet)
        with self.assertRaisesRegex(ValueError, "remediation packet status"):
            self._envelope(packet=packet, request=request)

    def test_rejects_approval_granted_runtime_or_retired_id_reuse(self):
        packet = self._packet()
        request = default_lifecycle_cleanup_patch_approval_request(packet)
        request["approval_granted"] = True
        with self.assertRaisesRegex(ValueError, "approval_granted must be False"):
            self._envelope(packet=packet, request=request)

        request = default_lifecycle_cleanup_patch_approval_request(packet)
        request["future_patch_approval_id"] = RETIRED_BLK_SYSTEM_073_APPROVAL_ID
        with self.assertRaisesRegex(ValueError, "retired BLK-SYSTEM-073 runtime ID"):
            self._envelope(packet=packet, request=request)

        request = default_lifecycle_cleanup_patch_approval_request(packet)
        request["operator_note"] = "approval granted; run BLK-pipe and patch Kuronode now"
        with self.assertRaisesRegex(ValueError, "authority-laundering text"):
            self._envelope(packet=packet, request=request)

    def test_rejects_target_retargeting_allowlist_drift_and_expired_envelope(self):
        packet = self._packet()
        request = default_lifecycle_cleanup_patch_approval_request(packet)
        request["target_head_sha"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "target_head_sha mismatch"):
            self._envelope(packet=packet, request=request)

        request = default_lifecycle_cleanup_patch_approval_request(packet)
        request["allowed_modified_files"] = ["scripts/other.ts"]
        with self.assertRaisesRegex(ValueError, "allowed_modified_files mismatch"):
            self._envelope(packet=packet, request=request)

        request = default_lifecycle_cleanup_patch_approval_request(packet)
        request["allowed_new_files"] = ["scripts/new_test.ts"]
        with self.assertRaisesRegex(ValueError, "allowed_new_files must be empty"):
            self._envelope(packet=packet, request=request)

        request = default_lifecycle_cleanup_patch_approval_request(packet)
        request["expires_at"] = "2026-05-10T14:30:00+10:00"
        with self.assertRaisesRegex(ValueError, "expires_at must be after requested_at and now"):
            self._envelope(packet=packet, request=request)

    def test_rejects_nested_laundering_protected_path_and_denied_authority_mismatch(self):
        packet = self._packet()
        hostile_notes = [
            {"nested": ["APPROVED_FOR_LIVE_EXECUTION"]},
            "docs%252Factive%252FREQ-001.md",
            "BEO is PUBLISHED and RTM generated",
            "coverage truth established; drift decision made",
            "npm run test:smoke now",
            "read .env secrets",
        ]
        for note in hostile_notes:
            with self.subTest(note=note):
                request = default_lifecycle_cleanup_patch_approval_request(packet)
                request["operator_note"] = note
                with self.assertRaisesRegex(ValueError, "authority-laundering text|protected BLK-req body reference"):
                    self._envelope(packet=packet, request=request)

        request = default_lifecycle_cleanup_patch_approval_request(packet)
        request["excluded_authorities"] = sorted(EXACT_EXCLUDED_AUTHORITIES - {"CODEX_EXECUTION"})
        with self.assertRaisesRegex(ValueError, "excluded_authorities must match exact denied authority set"):
            self._envelope(packet=packet, request=request)

        request = default_lifecycle_cleanup_patch_approval_request(packet)
        request["excluded_authorities"] = sorted(EXACT_EXCLUDED_AUTHORITIES) + ["APPROVED_FOR_LIVE_EXECUTION"]
        with self.assertRaisesRegex(ValueError, "excluded_authorities must match exact denied authority set"):
            self._envelope(packet=packet, request=request)


if __name__ == "__main__":
    unittest.main()
