import copy
import unittest

from authoritative_beo_publication_authority_request import _canonical_hash
from kuronode_power_of_ten_ceb009_static_gate_pilot import (
    build_ceb009_static_gate_pilot_report,
    default_ceb009_static_corpus,
    default_ceb009_static_request,
)
from kuronode_power_of_ten_ceb009_remediation_packet import (
    build_ceb009_remediation_packet,
    default_ceb009_remediation_request,
)
from kuronode_power_of_ten_ceb009_patch_approval_envelope import (
    build_ceb009_patch_approval_envelope,
    default_ceb009_patch_approval_request,
)
from kuronode_power_of_ten_ceb009_patch_execution_preflight import (
    BLOCK_REASON,
    EXACT_EXCLUDED_AUTHORITIES,
    PREFLIGHT_STATUS,
    TARGET_HEAD_SHA,
    TARGET_PATH,
    build_ceb009_patch_execution_preflight,
    default_ceb009_patch_execution_preflight_request,
)


class KuronodePowerOfTenCeb009PatchExecutionPreflightTest(unittest.TestCase):
    def _remediation_packet(self):
        corpus = default_ceb009_static_corpus()
        source_report = build_ceb009_static_gate_pilot_report(
            corpus=corpus,
            request=default_ceb009_static_request(corpus),
        )
        return build_ceb009_remediation_packet(
            source_report=source_report,
            request=default_ceb009_remediation_request(source_report),
        )

    def _approval_envelope(self):
        remediation_packet = self._remediation_packet()
        return build_ceb009_patch_approval_envelope(
            remediation_packet=remediation_packet,
            request=default_ceb009_patch_approval_request(remediation_packet),
            now="2026-05-10T21:10:00+10:00",
        )

    def _preflight(self, envelope=None, request=None):
        selected_envelope = copy.deepcopy(self._approval_envelope() if envelope is None else envelope)
        selected_request = copy.deepcopy(
            default_ceb009_patch_execution_preflight_request(selected_envelope) if request is None else request
        )
        return build_ceb009_patch_execution_preflight(envelope=selected_envelope, request=selected_request)

    def test_default_preflight_blocks_execution_pending_explicit_human_patch_approval(self):
        envelope = self._approval_envelope()
        preflight = self._preflight(envelope=envelope)

        self.assertEqual(preflight["preflight_status"], PREFLIGHT_STATUS)
        self.assertEqual(preflight["block_reason"], BLOCK_REASON)
        self.assertTrue(preflight["execution_blocked"])
        self.assertFalse(preflight["explicit_human_patch_approval_present"])
        self.assertFalse(preflight["approval_granted"])
        self.assertFalse(preflight["patch_executed"])
        self.assertFalse(preflight["patch_applied"])
        self.assertFalse(preflight["source_mutation_performed"])
        self.assertFalse(preflight["git_mutation_performed"])
        self.assertFalse(preflight["blk_pipe_invoked"])
        self.assertFalse(preflight["codex_started"])
        self.assertFalse(preflight["blk_test_mcp_started"])
        self.assertFalse(preflight["live_kuronode_scan_performed"])
        self.assertFalse(preflight["live_kuronode_source_validation_performed"])
        self.assertFalse(preflight["electron_launched"])
        self.assertFalse(preflight["smoke_test_executed"])
        self.assertFalse(preflight["typescript_tooling_executed"])
        self.assertFalse(preflight["package_manager_invoked"])
        self.assertFalse(preflight["protected_body_read"])
        self.assertFalse(preflight["beo_published"])
        self.assertFalse(preflight["rtm_generated"])
        self.assertFalse(preflight["coverage_claimed"])
        self.assertFalse(preflight["production_isolation_claimed"])
        self.assertEqual(preflight["envelope_hash"], envelope["envelope_hash"])
        self.assertEqual(preflight["target_path"], TARGET_PATH)
        self.assertEqual(preflight["target_head_sha"], TARGET_HEAD_SHA)
        self.assertEqual(set(preflight["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        self.assertIn("preflight_hash", preflight)

    def test_rejects_stale_envelope_missing_integrity_marker_and_approval_flag_flip(self):
        envelope = self._approval_envelope()
        envelope["target_path"] = "scripts/smoke_test.ts.modified"
        request = default_ceb009_patch_execution_preflight_request(envelope)
        with self.assertRaisesRegex(ValueError, "approval envelope hash mismatch"):
            self._preflight(envelope=envelope, request=request)

        envelope = self._approval_envelope()
        envelope["integrity_hardening_markers"] = []
        envelope["envelope_hash"] = _canonical_hash({key: value for key, value in envelope.items() if key != "envelope_hash"})
        request = default_ceb009_patch_execution_preflight_request(envelope)
        with self.assertRaisesRegex(ValueError, "integrity hardening marker required"):
            self._preflight(envelope=envelope, request=request)

        envelope = self._approval_envelope()
        envelope["approval_granted"] = True
        envelope["envelope_hash"] = _canonical_hash({key: value for key, value in envelope.items() if key != "envelope_hash"})
        request = default_ceb009_patch_execution_preflight_request(envelope)
        with self.assertRaisesRegex(ValueError, "approval_granted must remain false"):
            self._preflight(envelope=envelope, request=request)

    def test_rejects_target_allowlist_and_denied_authority_weakening(self):
        envelope = self._approval_envelope()
        envelope["target_head_sha"] = "f" * 40
        envelope["envelope_hash"] = _canonical_hash({key: value for key, value in envelope.items() if key != "envelope_hash"})
        request = default_ceb009_patch_execution_preflight_request(envelope)
        with self.assertRaisesRegex(ValueError, "target_head_sha must match exact CEB_009 fixture target head"):
            self._preflight(envelope=envelope, request=request)

        envelope = self._approval_envelope()
        envelope["allowed_modified_files"] = [TARGET_PATH, "packages/electron/src/main.ts"]
        envelope["envelope_hash"] = _canonical_hash({key: value for key, value in envelope.items() if key != "envelope_hash"})
        request = default_ceb009_patch_execution_preflight_request(envelope)
        with self.assertRaisesRegex(ValueError, "allowed_modified_files must match exact future patch target"):
            self._preflight(envelope=envelope, request=request)

        envelope = self._approval_envelope()
        envelope["excluded_authorities"] = [item for item in envelope["excluded_authorities"] if item != "LIVE_CODEX_EXECUTION"]
        envelope["envelope_hash"] = _canonical_hash({key: value for key, value in envelope.items() if key != "envelope_hash"})
        request = default_ceb009_patch_execution_preflight_request(envelope)
        with self.assertRaisesRegex(ValueError, "envelope excluded_authorities must match exact denied authority set"):
            self._preflight(envelope=envelope, request=request)

    def test_rejects_request_laundering_and_attempted_patch_authority(self):
        envelope = self._approval_envelope()
        request = default_ceb009_patch_execution_preflight_request(envelope)
        request["operator_note"] = "APPROVED_FOR_LIVE_EXECUTION; patch Kuronode now; npm run test:smoke; RTMGenerated"
        with self.assertRaisesRegex(ValueError, "preflight request rejects authority-laundering text"):
            self._preflight(envelope=envelope, request=request)

        request = default_ceb009_patch_execution_preflight_request(envelope)
        request["evidence_ref"] = "https://example.invalid/docs%252Factive%252FREQ-001.md"
        with self.assertRaisesRegex(ValueError, "preflight request rejects protected BLK-req body reference"):
            self._preflight(envelope=envelope, request=request)

        request = default_ceb009_patch_execution_preflight_request(envelope)
        request["explicit_human_patch_approval_present"] = True
        with self.assertRaisesRegex(ValueError, "explicit human patch approval is not accepted in BLK-SYSTEM-063"):
            self._preflight(envelope=envelope, request=request)

        request = default_ceb009_patch_execution_preflight_request(envelope)
        request["excluded_authorities"].append("PATCH_EXECUTION_APPROVED")
        with self.assertRaisesRegex(ValueError, "excluded_authorities must match exact denied authority set"):
            self._preflight(envelope=envelope, request=request)


if __name__ == "__main__":
    unittest.main()
