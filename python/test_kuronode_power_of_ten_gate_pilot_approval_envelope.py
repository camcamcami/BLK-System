import copy
import hashlib
import unittest

from kuronode_power_of_ten_gate_pilot_approval_envelope import (
    EXACT_EXCLUDED_AUTHORITIES,
    PROFILE_COMMAND,
    PROFILE_NAME,
    READY_STATUS,
    build_kuronode_power_of_ten_gate_pilot_approval_envelope,
)


def sha(value):
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def valid_inputs():
    target_package = {
        "target_repo_identity": "KURONODE-V1-EXACT-TARGET-FUTURE-PILOT",
        "target_branch": "main",
        "target_head_sha": "a" * 40,
        "target_workspace_identity": "KURONODE-P10-GATE-WORKSPACE-BLK-SYSTEM-058",
        "target_scope": "KURONODE_TYPESCRIPT_POWER_OF_TEN_GATE_PILOT_EXACT_TARGET_ONLY",
        "operator_note": "future exact target envelope only",
    }
    readiness_evidence = {
        "static_profile_boundary_marker": "KURONODE_TYPESCRIPT_POWER_OF_TEN_STATIC_PROFILE_BOUNDARY",
        "validation_profile_boundary_marker": "KURONODE_POWER_OF_TEN_VALIDATION_PROFILE_REGISTRY_BOUNDARY",
        "static_profile_status": "KURONODE_POWER_OF_TEN_STATIC_PROFILE_PASS_FIXTURE_ONLY",
        "fixture_profile_marker": "KURONODE_POWER_OF_TEN_STATIC_FIXTURE_SELFTEST_PROFILE_REGISTERED",
        "profile_name": PROFILE_NAME,
        "profile_command_hash": sha(PROFILE_COMMAND),
        "source_bundle_hash": sha("submitted fixture source bundle descriptors"),
        "evidence_hash": sha("blk-system-056-057-evidence"),
    }
    approval_package = {
        "approval_id": "BLK-SYSTEM-058-KURONODE-GATE-APPROVAL-001",
        "run_id": "BLK-SYSTEM-058-KURONODE-GATE-RUN-001",
        "operator_identity": "discord:684235178083745819",
        "approval_scope": "KURONODE_POWER_OF_TEN_GATE_PILOT_APPROVAL_ENVELOPE_ONLY",
        "requested_at": "2026-05-10T20:00:00+10:00",
        "expires_at": "2026-05-10T21:00:00+10:00",
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    pilot_controls = {
        "timeout_seconds": 120,
        "max_output_bytes": 200000,
        "replay_ledger_identity": "BLK-SYSTEM-058-KURONODE-GATE-REPLAY-LEDGER-FUTURE",
        "operator_stop_required": True,
        "cleanup_required": True,
        "proof_markers": [
            "EXACT_TARGET_BOUND",
            "REPLAY_PROTECTION_REQUIRED",
            "OUTPUT_BOUND_REQUIRED",
            "OPERATOR_STOP_REQUIRED",
            "NO_SOURCE_MUTATION_REQUIRED",
            "NO_PROTECTED_BODY_READ_REQUIRED",
        ],
    }
    return target_package, readiness_evidence, approval_package, pilot_controls


class KuronodePowerOfTenGatePilotApprovalEnvelopeTest(unittest.TestCase):
    def _build(self, mutate=None):
        inputs = [copy.deepcopy(item) for item in valid_inputs()]
        if mutate:
            mutate(*inputs)
        return build_kuronode_power_of_ten_gate_pilot_approval_envelope(*inputs, now="2026-05-10T20:30:00+10:00")

    def test_builds_ready_envelope_without_runtime_side_effects(self):
        envelope = self._build()

        self.assertEqual(envelope["envelope_status"], READY_STATUS)
        self.assertEqual(envelope["profile_name"], PROFILE_NAME)
        self.assertEqual(envelope["target_head_sha"], "a" * 40)
        self.assertEqual(set(envelope["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        self.assertFalse(envelope["live_kuronode_scan_performed"])
        self.assertFalse(envelope["typescript_tooling_executed"])
        self.assertFalse(envelope["package_manager_invoked"])
        self.assertFalse(envelope["source_mutation_performed"])
        self.assertFalse(envelope["git_mutation_performed"])
        self.assertFalse(envelope["codex_started"])
        self.assertFalse(envelope["blk_test_mcp_started"])
        self.assertFalse(envelope["protected_body_read"])
        self.assertFalse(envelope["beo_published"])
        self.assertFalse(envelope["rtm_generated"])
        self.assertIn("envelope_hash", envelope)

    def test_rejects_timestamp_expiry_and_malformed_target_hash(self):
        with self.assertRaisesRegex(ValueError, "expires_at must be after requested_at"):
            self._build(lambda _target, _evidence, approval, _controls: approval.update({"expires_at": "2026-05-10T19:59:59+10:00"}))
        with self.assertRaisesRegex(ValueError, "approval envelope is expired"):
            self._build(lambda _target, _evidence, approval, _controls: approval.update({"expires_at": "2026-05-10T20:10:00+10:00"}))
        with self.assertRaisesRegex(ValueError, "target_head_sha must be a 40-character hex commit"):
            self._build(lambda target, _evidence, _approval, _controls: target.update({"target_head_sha": "not-a-sha"}))

    def test_rejects_profile_and_denied_authority_mismatch(self):
        with self.assertRaisesRegex(ValueError, "profile_command_hash does not match exact fixture command"):
            self._build(lambda _target, evidence, _approval, _controls: evidence.update({"profile_command_hash": sha("npm install && tsc")}))
        with self.assertRaisesRegex(ValueError, "profile_name must be kuronode-power-of-ten-static-fixture"):
            self._build(lambda _target, evidence, _approval, _controls: evidence.update({"profile_name": "kuronode-power-of-ten-static"}))
        with self.assertRaisesRegex(ValueError, "excluded_authorities must match exact denied authority set"):
            self._build(lambda _target, _evidence, approval, _controls: approval.update({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES - {"LIVE_CODEX_EXECUTION"})}))
        with self.assertRaisesRegex(ValueError, "excluded_authorities must match exact denied authority set"):
            self._build(lambda _target, _evidence, approval, _controls: approval.update({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES) + ["LIVE_CODEX_EXECUTION"]}))

    def test_rejects_laundered_runtime_authority_and_protected_paths(self):
        cases = [
            ("target", {"operator_note": "runtime pilot approved by operator; live scan allowed"}),
            ("target", {"operator_note": "scan docs%252Factive%252FREQ-001.md before validation"}),
            ("evidence", {"extra": "BEO publication authorized; RTMGeneration complete"}),
            ("approval", {"approval_scope": "APPROVED_FOR_LIVE_EXECUTION"}),
            ("controls", {"replay_ledger_identity": "curl https://example.invalid then npm install"}),
        ]
        for section, patch in cases:
            with self.subTest(section=section, patch=patch):
                def mutate(target, evidence, approval, controls):
                    {"target": target, "evidence": evidence, "approval": approval, "controls": controls}[section].update(patch)
                with self.assertRaisesRegex(ValueError, "authority-laundering text|unexpected field|protected BLK-req body reference"):
                    self._build(mutate)

    def test_rejects_weak_controls_and_side_effect_flags(self):
        with self.assertRaisesRegex(ValueError, "approval_id must bind to BLK-SYSTEM-058"):
            self._build(lambda _target, _evidence, approval, _controls: approval.update({"approval_id": "BLK-SYSTEM-057-KURONODE-GATE-APPROVAL-001"}))
        with self.assertRaisesRegex(ValueError, "run_id must bind to BLK-SYSTEM-058"):
            self._build(lambda _target, _evidence, approval, _controls: approval.update({"run_id": "BLK-SYSTEM-057-KURONODE-GATE-RUN-001"}))
        with self.assertRaisesRegex(ValueError, "proof_markers must include exact pilot safety markers"):
            self._build(lambda _target, _evidence, _approval, controls: controls.update({"proof_markers": ["ok"]}))
        with self.assertRaisesRegex(ValueError, "operator_stop_required must be true"):
            self._build(lambda _target, _evidence, _approval, controls: controls.update({"operator_stop_required": False}))
        with self.assertRaisesRegex(ValueError, "unsupported keys"):
            self._build(lambda _target, _evidence, _approval, controls: controls.update({"live_kuronode_scan_performed": True}))


if __name__ == "__main__":
    unittest.main()
