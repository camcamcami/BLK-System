import unittest

from kuronode_power_of_ten_ceb009_fresh_target_patch_execution import (
    CURRENT_TARGET_HEAD_SHA,
    FRESH_TARGET_READY_STATUS,
    TARGET_PATH,
    build_ceb009_fresh_target_patch_execution_payload,
    default_ceb009_fresh_target_patch_execution_request,
)


class CEB009FreshTargetPatchExecutionTest(unittest.TestCase):
    def test_fresh_target_request_builds_one_exact_blk_pipe_payload(self):
        request = default_ceb009_fresh_target_patch_execution_request()
        payload_record = build_ceb009_fresh_target_patch_execution_payload(request)

        self.assertEqual(payload_record["execution_readiness_status"], FRESH_TARGET_READY_STATUS)
        self.assertEqual(payload_record["target_head_sha"], CURRENT_TARGET_HEAD_SHA)
        self.assertTrue(payload_record["approval_captured"])
        self.assertTrue(payload_record["execution_authorized"])
        self.assertFalse(payload_record["blk_pipe_invoked"])
        self.assertFalse(payload_record["kuronode_remote_pushed"])
        payload = payload_record["blk_pipe_payload"]
        self.assertEqual(payload["action"], "execute")
        self.assertEqual(payload["work_dir"], "/home/dad/code/Kuronode-v1")
        self.assertEqual(payload["target_branch"], "main")
        self.assertEqual(payload["allowed_modified_files"], [TARGET_PATH])
        self.assertEqual(payload["allowed_new_files"], [])
        self.assertEqual(payload["engine"], "python3")
        self.assertNotIn("codex", " ".join(payload["engine_args"]).lower())
        self.assertEqual(payload["validation_commands"], ["git diff --check -- scripts/smoke_test.ts"])

    def test_fresh_target_request_rejects_stale_or_different_target(self):
        request = default_ceb009_fresh_target_patch_execution_request()
        request["target_head_sha"] = "cb09d965c0407612c9ce8fc9cc58c5e62c82e1b2"
        with self.assertRaisesRegex(ValueError, "target_head_sha"):
            build_ceb009_fresh_target_patch_execution_payload(request)

    def test_fresh_target_request_rejects_broadened_allowlists(self):
        request = default_ceb009_fresh_target_patch_execution_request()
        request["allowed_modified_files"] = [TARGET_PATH, "packages/electron/src/main.ts"]
        with self.assertRaisesRegex(ValueError, "allowed_modified_files"):
            build_ceb009_fresh_target_patch_execution_payload(request)

    def test_fresh_target_request_rejects_adjacent_authority_laundering(self):
        request = default_ceb009_fresh_target_patch_execution_request()
        request["operator_note"] = "also run npm test, publish CEO_009, and generate RTM"
        with self.assertRaisesRegex(ValueError, "authority-laundering"):
            build_ceb009_fresh_target_patch_execution_payload(request)


if __name__ == "__main__":
    unittest.main()
