import copy
import unittest

from authoritative_beo_publication_authority_request import _canonical_hash
from kuronode_power_of_ten_ceb009_patch_approval_envelope import (
    TARGET_BRANCH,
    TARGET_HEAD_SHA,
    TARGET_PATH,
    TARGET_REPO_IDENTITY,
    build_ceb009_patch_approval_envelope,
    default_ceb009_patch_approval_request,
)
from kuronode_power_of_ten_ceb009_patch_execution_authority_request import (
    build_ceb009_patch_execution_authority_request,
    default_ceb009_patch_execution_authority_request,
)
from kuronode_power_of_ten_ceb009_patch_execution_preflight import (
    build_ceb009_patch_execution_preflight,
    default_ceb009_patch_execution_preflight_request,
)
from kuronode_power_of_ten_ceb009_remediation_packet import (
    build_ceb009_remediation_packet,
    default_ceb009_remediation_request,
)
from kuronode_power_of_ten_ceb009_static_gate_pilot import (
    build_ceb009_static_gate_pilot_report,
    default_ceb009_static_corpus,
    default_ceb009_static_request,
)
from kuronode_power_of_ten_ceb009_patch_execution_approval_capture import (
    APPROVED_READY_STATUS,
    BLOCKED_TARGET_DRIFT_STATUS,
    EXACT_EXCLUDED_ADJACENT_AUTHORITIES,
    build_default_ceb009_patch_execution_authority_chain,
    build_ceb009_patch_execution_approval_capture,
    default_ceb009_patch_execution_approval_capture_request,
)


class CEB009PatchExecutionApprovalCaptureTest(unittest.TestCase):
    def _authority_request(self):
        corpus = default_ceb009_static_corpus()
        source_report = build_ceb009_static_gate_pilot_report(
            corpus=corpus,
            request=default_ceb009_static_request(corpus),
        )
        remediation_packet = build_ceb009_remediation_packet(
            source_report=source_report,
            request=default_ceb009_remediation_request(source_report),
        )
        envelope = build_ceb009_patch_approval_envelope(
            remediation_packet=remediation_packet,
            request=default_ceb009_patch_approval_request(remediation_packet),
        )
        preflight = build_ceb009_patch_execution_preflight(
            envelope=envelope,
            request=default_ceb009_patch_execution_preflight_request(envelope),
        )
        return build_ceb009_patch_execution_authority_request(
            preflight=preflight,
            request=default_ceb009_patch_execution_authority_request(preflight),
        )

    def _capture(self, *, authority_request=None, request=None):
        selected_authority = copy.deepcopy(authority_request or self._authority_request())
        selected_request = copy.deepcopy(
            request or default_ceb009_patch_execution_approval_capture_request(selected_authority)
        )
        return build_ceb009_patch_execution_approval_capture(
            authority_request=selected_authority,
            request=selected_request,
        )

    def test_capture_authorizes_one_exact_blk_pipe_attempt_when_local_and_remote_heads_match(self):
        capture = self._capture()

        self.assertEqual(capture["execution_readiness_status"], APPROVED_READY_STATUS)
        self.assertTrue(capture["approval_captured"])
        self.assertTrue(capture["execution_authorized"])
        self.assertFalse(capture["blk_pipe_invoked"])
        self.assertEqual(capture["target_repo_identity"], TARGET_REPO_IDENTITY)
        self.assertEqual(capture["target_branch"], TARGET_BRANCH)
        self.assertEqual(capture["target_head_sha"], TARGET_HEAD_SHA)
        self.assertEqual(capture["observed_local_head"], TARGET_HEAD_SHA)
        self.assertEqual(capture["observed_origin_main_head"], TARGET_HEAD_SHA)
        self.assertEqual(capture["allowed_modified_files"], [TARGET_PATH])
        self.assertEqual(capture["allowed_new_files"], [])
        self.assertEqual(set(capture["excluded_adjacent_authorities"]), EXACT_EXCLUDED_ADJACENT_AUTHORITIES)
        payload = capture["blk_pipe_payload"]
        self.assertEqual(payload["action"], "execute")
        self.assertEqual(payload["work_dir"], "/home/dad/code/Kuronode-v1")
        self.assertEqual(payload["target_branch"], TARGET_BRANCH)
        self.assertEqual(payload["allowed_modified_files"], [TARGET_PATH])
        self.assertEqual(payload["allowed_new_files"], [])
        self.assertNotIn("codex", " ".join(payload["engine_args"]).lower())
        self.assertNotIn("npm", " ".join(payload.get("validation_commands", [])).lower())

    def test_payload_validates_projection_shape_after_evaluate_returns_to_node_context(self):
        capture = self._capture()
        script = capture["blk_pipe_payload"]["engine_args"][1]

        result_index = script.index("const result = await projectionPromise;")
        validation_index = script.index("if (!isProjectionResult(result))")
        self.assertGreater(validation_index, result_index)
        evaluated_fragment = script[script.index("const projectionPromise"):result_index]
        self.assertNotIn("isProjectionResult(result)", evaluated_fragment)

    def test_capture_blocks_without_blk_pipe_payload_when_remote_head_drift_is_observed(self):
        authority = self._authority_request()
        request = default_ceb009_patch_execution_approval_capture_request(authority)
        request["observed_origin_main_head"] = "70b6062b92cf61c12bf190f92dc6b45ea4dcd438"

        capture = self._capture(authority_request=authority, request=request)

        self.assertEqual(capture["execution_readiness_status"], BLOCKED_TARGET_DRIFT_STATUS)
        self.assertTrue(capture["approval_captured"])
        self.assertFalse(capture["execution_authorized"])
        self.assertFalse(capture["blk_pipe_invoked"])
        self.assertEqual(capture["block_reason"], "TARGET_HEAD_DRIFT_REQUIRES_FRESH_APPROVAL")
        self.assertNotIn("blk_pipe_payload", capture)

    def test_capture_rejects_broadened_allowlists_and_new_files(self):
        authority = self._authority_request()
        request = default_ceb009_patch_execution_approval_capture_request(authority)
        request["allowed_modified_files"] = [TARGET_PATH, "packages/electron/src/main.ts"]
        with self.assertRaisesRegex(ValueError, "allowed_modified_files"):
            self._capture(authority_request=authority, request=request)

        request = default_ceb009_patch_execution_approval_capture_request(authority)
        request["allowed_new_files"] = ["scripts/new_smoke_helper.ts"]
        with self.assertRaisesRegex(ValueError, "allowed_new_files"):
            self._capture(authority_request=authority, request=request)

    def test_capture_recomputes_authority_request_hash_and_rejects_tampering(self):
        authority = self._authority_request()
        authority["target_path"] = "packages/electron/src/main.ts"
        authority["authority_request_hash"] = _canonical_hash(
            {key: value for key, value in authority.items() if key != "authority_request_hash"}
        )
        request = default_ceb009_patch_execution_approval_capture_request(authority)
        with self.assertRaisesRegex(ValueError, "target_path"):
            self._capture(authority_request=authority, request=request)

    def test_capture_rejects_metadata_laundering_and_adjacent_authority(self):
        authority = self._authority_request()
        request = default_ceb009_patch_execution_approval_capture_request(authority)
        request["operator_note"] = "approved for BEO publication and RTM generation after blk pipe success"
        with self.assertRaisesRegex(ValueError, "authority-laundering"):
            self._capture(authority_request=authority, request=request)

    def test_default_chain_builds_ready_fixture_for_synthetic_exact_head_inputs(self):
        capture = build_default_ceb009_patch_execution_authority_chain()
        self.assertEqual(capture["execution_readiness_status"], APPROVED_READY_STATUS)
        self.assertEqual(capture["target_path"], TARGET_PATH)


if __name__ == "__main__":
    unittest.main()
