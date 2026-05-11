import hashlib
import json
import unittest

from blk_test_kuronode_workspace_pilot_request import (
    build_kuronode_workspace_pilot_request,
    EXACT_EXCLUDED_AUTHORITIES as REQUEST_EXCLUDED_AUTHORITIES,
    NO_SIDE_EFFECT_FLAGS as REQUEST_NO_SIDE_EFFECT_FLAGS,
)
from blk_test_kuronode_workspace_exact_target_approval_envelope import (
    ENVELOPE_READY_STATUS,
    ENVELOPE_EXCLUDED_AUTHORITIES,
    ENVELOPE_NO_SIDE_EFFECT_FLAGS,
    REQUIRED_ENVELOPE_PROOF_MARKERS,
    build_kuronode_workspace_exact_target_approval_envelope,
)

KURONODE_HEAD = "38e332b188e45edcb484765694112c9041ad1a3b"


class BLKTestKuronodeWorkspaceExactTargetApprovalEnvelopeTest(unittest.TestCase):
    def _target(self, **overrides):
        target = {
            "target_repo_path": "/home/dad/code/Kuronode-v1",
            "target_branch": "main",
            "target_head_sha": KURONODE_HEAD,
            "target_workspace_label": "kuronode-v1-local-workspace",
            "target_scope": "Kuronode workspace read-only BLK-test module pilot request",
            "workspace_status": "main...origin/main [ahead 1]",
        }
        target.update(overrides)
        return target

    def _request_seed(self, **overrides):
        request = {
            "request_id": "BLK-SYSTEM-071-KURONODE-WORKSPACE-PILOT-REQUEST-001",
            "operator_identity": "discord:684235178083745819:camcamcami",
            "requested_at": "2026-05-11T10:55:00+10:00",
            "request_scope": "BLK_TEST_KURONODE_WORKSPACE_READ_ONLY_PILOT_REQUEST_ONLY",
            "blk_test_role_statement": "BLK-test is a BLK-System functional module, not BLK-System's test suite.",
            "fixed_tool": "run_ast_validation",
            "tool_mode": "READ_ONLY_STATIC_AST_VALIDATION_REQUEST_ONLY",
            "proof_markers": [
                "BLK_TEST_MODULE_NOT_BLK_SYSTEM_TEST_SUITE",
                "KURONODE_WORKSPACE_EXACT_TARGET_BOUND",
                "READ_ONLY_FIXED_TOOL_ONLY",
                "NO_CEB009_REUSE",
                "NO_SOURCE_OR_GIT_MUTATION_BY_BLK_TEST",
                "NO_PROTECTED_BODY_READ",
                "BEO_RTM_AND_COVERAGE_AUTHORITY_SEPARATE",
            ],
            "historical_references_only": [
                "Prior local Kuronode patch closeout may be cited as historical target-identity context only",
                "Kuronode local commit 38e332b is a target identity, not reusable patch authority",
            ],
            "consumed_authority_ids_reused": [],
            "excluded_authorities": sorted(REQUEST_EXCLUDED_AUTHORITIES),
            "no_side_effects": {key: False for key in REQUEST_NO_SIDE_EFFECT_FLAGS},
        }
        request.update(overrides)
        return request

    def _request_package(self, **overrides):
        return build_kuronode_workspace_pilot_request(self._target(), self._request_seed(**overrides))

    def _with_recomputed_request_hash(self, package):
        updated = dict(package)
        updated["request_hash"] = "sha256:" + hashlib.sha256(
            json.dumps({k: v for k, v in updated.items() if k != "request_hash"}, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
        ).hexdigest()
        return updated

    def _envelope(self, **overrides):
        envelope = {
            "approval_envelope_id": "BLK-SYSTEM-072-KURONODE-WORKSPACE-APPROVAL-ENVELOPE-001",
            "approval_id": "APPROVAL-BLK-SYSTEM-072-KURONODE-WORKSPACE-001",
            "run_id": "RUN-BLK-SYSTEM-072-KURONODE-WORKSPACE-001",
            "operator_identity": "discord:684235178083745819:camcamcami",
            "requested_at": "2026-05-11T11:45:00+10:00",
            "expires_at": "2026-05-11T12:45:00+10:00",
            "approval_scope": "BLK_TEST_KURONODE_WORKSPACE_EXACT_TARGET_APPROVAL_ENVELOPE_REVIEW_ONLY",
            "blk_test_role_statement": "BLK-test is a BLK-System functional module, not BLK-System's test suite.",
            "target_repo_path": "/home/dad/code/Kuronode-v1",
            "target_branch": "main",
            "target_head_sha": KURONODE_HEAD,
            "workspace_status": "main...origin/main [ahead 1]",
            "fixed_tool": "run_ast_validation",
            "tool_mode": "READ_ONLY_STATIC_AST_VALIDATION_FUTURE_RUNTIME_ONLY",
            "timeout_output_profile": {"timeout_seconds": 30, "max_output_bytes": 4096},
            "replay_policy": {
                "replay_ledger_identity": "BLK-SYSTEM-072-KURONODE-WORKSPACE-REPLAY-LEDGER-REVIEW-ONLY",
                "approval_id_one_use": True,
                "run_id_one_use": True,
                "consumed_ids_rejected": True,
            },
            "operator_stop_control": "operator can stop before any separately approved future runtime begins",
            "proof_markers": sorted(REQUIRED_ENVELOPE_PROOF_MARKERS),
            "excluded_authorities": sorted(ENVELOPE_EXCLUDED_AUTHORITIES),
            "no_side_effects": {key: False for key in ENVELOPE_NO_SIDE_EFFECT_FLAGS},
        }
        envelope.update(overrides)
        return envelope

    def test_complete_envelope_returns_review_ready_not_runtime(self):
        result = build_kuronode_workspace_exact_target_approval_envelope(self._request_package(), self._envelope())

        self.assertEqual(result["status"], ENVELOPE_READY_STATUS)
        self.assertFalse(result["runtime_approved"])
        self.assertFalse(result["blk_test_runtime_executed"])
        self.assertFalse(result["source_mutation_allowed"])
        self.assertFalse(result["git_mutation_allowed"])
        self.assertEqual(result["upstream_request_status"], "BLK_TEST_KURONODE_WORKSPACE_PILOT_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME")
        self.assertEqual(result["target_head_sha"], KURONODE_HEAD)
        self.assertEqual(result["approval_id"], "APPROVAL-BLK-SYSTEM-072-KURONODE-WORKSPACE-001")
        self.assertRegex(result["envelope_hash"], r"^sha256:[0-9a-f]{64}$")

    def test_upstream_request_hash_is_recomputed_and_forgery_blocks(self):
        request = self._request_package()
        forged = dict(request)
        forged["target_head_sha"] = "70b6062b92cf61c12bf190f92dc6b45ea4dcd438"
        with self.assertRaises(ValueError):
            build_kuronode_workspace_exact_target_approval_envelope(forged, self._envelope())

        forged_hash = dict(request)
        forged_hash["request_hash"] = "sha256:" + "0" * 64
        with self.assertRaises(ValueError):
            build_kuronode_workspace_exact_target_approval_envelope(forged_hash, self._envelope())

    def test_upstream_request_schema_is_closed_even_when_attacker_recomputes_hash(self):
        request = self._request_package()
        forged = dict(request)
        forged["selected_frontier"] = "runtime approval: yes"
        forged = self._with_recomputed_request_hash(forged)
        with self.assertRaises(ValueError):
            build_kuronode_workspace_exact_target_approval_envelope(forged, self._envelope())

        forged_nested = dict(request)
        forged_nested["authority_notes"] = {"production_mcp_authority": "live execution authorized"}
        forged_nested = self._with_recomputed_request_hash(forged_nested)
        with self.assertRaises(ValueError):
            build_kuronode_workspace_exact_target_approval_envelope(forged_nested, self._envelope())

    def test_exact_target_and_path_spelling_are_required(self):
        bad = [
            self._envelope(target_repo_path="/home/dad/code/Kuronode-v1/."),
            self._envelope(target_repo_path="/home/dad/code/Kuronode-v1/"),
            self._envelope(target_repo_path="/home/dad/code//Kuronode-v1"),
            self._envelope(target_branch="runtime"),
            self._envelope(target_head_sha="38e332b"),
            self._envelope(workspace_status="main...origin/main"),
            self._envelope(fixed_tool="npm test"),
        ]
        for envelope in bad:
            with self.subTest(envelope=envelope):
                with self.assertRaises(ValueError):
                    build_kuronode_workspace_exact_target_approval_envelope(self._request_package(), envelope)

    def test_approval_and_run_ids_must_be_fresh_blk_system_072_ids(self):
        bad = [
            self._envelope(approval_id="APPROVAL-BLK-SYSTEM-071-KURONODE-WORKSPACE-001"),
            self._envelope(run_id="RUN-BLK-SYSTEM-070-CEB009-001"),
            self._envelope(approval_envelope_id="CEB_009-APPROVAL-ENVELOPE-REUSE"),
            self._envelope(replay_policy={"replay_ledger_identity": "BLK-SYSTEM-051-old-ledger", "approval_id_one_use": True, "run_id_one_use": True, "consumed_ids_rejected": True}),
        ]
        for envelope in bad:
            with self.subTest(envelope=envelope):
                with self.assertRaises(ValueError):
                    build_kuronode_workspace_exact_target_approval_envelope(self._request_package(), envelope)

    def test_exact_denied_authorities_no_side_effects_and_proofs_are_required(self):
        missing_auth = sorted(ENVELOPE_EXCLUDED_AUTHORITIES - {"RUNTIME_APPROVAL"})
        extra_auth = sorted(ENVELOPE_EXCLUDED_AUTHORITIES | {"APPROVED_FOR_LIVE_EXECUTION"})
        duplicate_auth = sorted(ENVELOPE_EXCLUDED_AUTHORITIES) + [sorted(ENVELOPE_EXCLUDED_AUTHORITIES)[0]]
        missing_flags = {key: False for key in ENVELOPE_NO_SIDE_EFFECT_FLAGS if key != "runtime_approved"}
        true_flags = {key: False for key in ENVELOPE_NO_SIDE_EFFECT_FLAGS}
        true_flags["kuronode_source_mutated"] = True
        bad_proofs = sorted(REQUIRED_ENVELOPE_PROOF_MARKERS - {"UPSTREAM_REQUEST_HASH_RECOMPUTED"})
        cases = [
            self._envelope(excluded_authorities=missing_auth),
            self._envelope(excluded_authorities=extra_auth),
            self._envelope(excluded_authorities=duplicate_auth),
            self._envelope(no_side_effects=missing_flags),
            self._envelope(no_side_effects=true_flags),
            self._envelope(proof_markers=bad_proofs),
            self._envelope(proof_markers=["ok"]),
        ]
        for envelope in cases:
            with self.subTest(envelope=envelope):
                with self.assertRaises(ValueError):
                    build_kuronode_workspace_exact_target_approval_envelope(self._request_package(), envelope)

    def test_valid_fields_reject_authority_laundering_and_secret_strings(self):
        bad = [
            self._envelope(operator_stop_control="runtime approved by operator"),
            self._envelope(operator_stop_control="runtime approval: yes"),
            self._envelope(operator_stop_control="runtime-approval: yes"),
            self._envelope(operator_stop_control="runtime.approval = yes"),
            self._envelope(operator_stop_control="runtime authorized by human"),
            self._envelope(operator_stop_control="live-execution authorized"),
            self._envelope(operator_stop_control="approved-for-runtime"),
            self._envelope(operator_stop_control="secondary frontier other_frontier"),
            self._envelope(operator_stop_control="selected.frontier: other_frontier"),
            self._envelope(operator_stop_control="BLK-test validates BLK-System"),
            self._envelope(operator_stop_control="Use BLK-SYSTEM-070 task-002 as executable fixture input"),
            self._envelope(operator_stop_control="BEO is PUBLISHED"),
            self._envelope(operator_stop_control="RTM generated"),
            self._envelope(operator_stop_control="coverage truth established"),
            self._envelope(operator_stop_control="drift decision made"),
            self._envelope(operator_stop_control="read .env secrets"),
            self._envelope(operator_stop_control="SECRET_KEY may be used"),
            self._envelope(replay_policy={"replay_ledger_identity": "docs/active/replay-ledger", "approval_id_one_use": True, "run_id_one_use": True, "consumed_ids_rejected": True}),
            self._envelope(timeout_output_profile={"timeout_seconds": 30, "max_output_bytes": 4096, "notes": "git push allowed"}),
        ]
        for envelope in bad:
            with self.subTest(envelope=envelope):
                with self.assertRaises(ValueError):
                    build_kuronode_workspace_exact_target_approval_envelope(self._request_package(), envelope)

    def test_timestamps_are_timezone_aware_ordered_and_within_review_ttl(self):
        bad = [
            self._envelope(requested_at="2026-05-11T11:45:00", expires_at="2026-05-11T12:45:00+10:00"),
            self._envelope(requested_at="2026-05-11T11:45:00+10:00", expires_at="2026-05-11T11:45:00+10:00"),
            self._envelope(requested_at="2026-05-11T11:45:00+10:00", expires_at="2026-05-11T15:46:00+10:00"),
        ]
        for envelope in bad:
            with self.subTest(envelope=envelope):
                with self.assertRaises(ValueError):
                    build_kuronode_workspace_exact_target_approval_envelope(self._request_package(), envelope)


if __name__ == "__main__":
    unittest.main()
