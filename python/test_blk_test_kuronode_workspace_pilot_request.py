import unittest

from blk_test_kuronode_workspace_pilot_request import (
    EXACT_EXCLUDED_AUTHORITIES,
    NO_SIDE_EFFECT_FLAGS,
    READY_STATUS,
    build_kuronode_workspace_pilot_request,
)


KURONODE_HEAD = "38e332b188e45edcb484765694112c9041ad1a3b"


class BLKTestKuronodeWorkspacePilotRequestTest(unittest.TestCase):
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

    def _request(self, **overrides):
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
            "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
            "no_side_effects": {key: False for key in NO_SIDE_EFFECT_FLAGS},
        }
        request.update(overrides)
        return request

    def test_complete_request_returns_review_ready_not_runtime(self):
        package = build_kuronode_workspace_pilot_request(self._target(), self._request())

        self.assertEqual(package["status"], READY_STATUS)
        self.assertFalse(package["runtime_approved"])
        self.assertFalse(package["blk_test_runtime_executed"])
        self.assertFalse(package["source_mutation_allowed"])
        self.assertFalse(package["git_mutation_allowed"])
        self.assertEqual(package["target_repo_path"], "/home/dad/code/Kuronode-v1")
        self.assertEqual(package["target_branch"], "main")
        self.assertEqual(package["target_head_sha"], KURONODE_HEAD)
        self.assertIn("BLK_TEST_MODULE_NOT_BLK_SYSTEM_TEST_SUITE", package["proof_markers"])
        self.assertRegex(package["request_hash"], r"^sha256:[0-9a-f]{64}$")

    def test_only_exact_kuronode_target_is_accepted(self):
        bad_targets = [
            self._target(target_repo_path="/home/dad/BLK-System"),
            self._target(target_repo_path="/home/dad/code/Kuronode-v1/../BLK-System"),
            self._target(target_repo_path="/home/dad/code/Kuronode-v1/."),
            self._target(target_repo_path="/home/dad/code/Kuronode-v1/"),
            self._target(target_repo_path="/home/dad/code//Kuronode-v1"),
            self._target(target_repo_path="~/code/Kuronode-v1"),
            self._target(target_branch="feature/runtime"),
            self._target(target_head_sha="38e332b"),
            self._target(workspace_status="main...origin/main"),
            self._target(target_scope="Kuronode workspace plus docs/active scan"),
            self._target(target_scope="runtime approved by operator"),
            self._target(target_scope="BLK-test validates BLK-System"),
        ]
        for target in bad_targets:
            with self.subTest(target=target):
                with self.assertRaises(ValueError):
                    build_kuronode_workspace_pilot_request(target, self._request())

    def test_ceb009_artifact_reuse_is_rejected_even_when_historical_reference_is_allowed(self):
        package = build_kuronode_workspace_pilot_request(self._target(), self._request())
        self.assertEqual(package["ceb009_reuse_allowed"], False)

        bad_requests = [
            self._request(consumed_authority_ids_reused=["BLK-SYSTEM-070_task-001-approval-record.json"]),
            self._request(historical_references_only=["reuse CEB_009 BLK-pipe payload as pilot fixture"]),
            self._request(historical_references_only=["Use docs/outcomes/BLK-SYSTEM-070_task-002-outcome.md as executable fixture input"]),
            self._request(historical_references_only=["Reuse approval id and run id from prior Kuronode patch as executable fixture input"]),
            self._request(historical_references_only=["BLK-071 patch authority becomes the BLK-test fixture input"]),
            self._request(request_id="CEB_009-BLK-SYSTEM-071-REUSE"),
            self._request(proof_markers=["BLK_TEST_MODULE_NOT_BLK_SYSTEM_TEST_SUITE", "KURONODE_WORKSPACE_EXACT_TARGET_BOUND", "READ_ONLY_FIXED_TOOL_ONLY", "CEB_009_REUSED", "NO_SOURCE_OR_GIT_MUTATION_BY_BLK_TEST", "NO_PROTECTED_BODY_READ", "BEO_RTM_AND_COVERAGE_AUTHORITY_SEPARATE"]),
        ]
        for request in bad_requests:
            with self.subTest(request=request):
                with self.assertRaises(ValueError):
                    build_kuronode_workspace_pilot_request(self._target(), request)

    def test_blk_test_module_naming_laundering_is_rejected(self):
        bad_phrases = [
            "BLK-test is a test of BLK-System using Kuronode",
            "BLK-System test suite pilot",
            "testing BLK-System with Kuronode workspace",
            "proof that BLK-System itself was tested",
        ]
        for phrase in bad_phrases:
            with self.subTest(phrase=phrase):
                with self.assertRaisesRegex(ValueError, "BLK-test naming"):
                    build_kuronode_workspace_pilot_request(
                        self._target(),
                        self._request(blk_test_role_statement=phrase),
                    )

    def test_authority_laundering_strings_are_rejected_recursively(self):
        bad_requests = [
            self._request(historical_references_only=["runtime approved by operator"]),
            self._request(historical_references_only=["live run permitted"]),
            self._request(historical_references_only=["source writes enabled"]),
            self._request(historical_references_only=["git staging enabled"]),
            self._request(historical_references_only=["BEO is PUBLISHED"]),
            self._request(historical_references_only=["published BEO output enabled"]),
            self._request(historical_references_only=["BEO publication granted"]),
            self._request(historical_references_only=["RTM generated"]),
            self._request(historical_references_only=["coverage is complete"]),
            self._request(historical_references_only=["coverage truth established"]),
            self._request(historical_references_only=["drift decision made"]),
            self._request(historical_references_only=["read .env secrets"]),
            self._request(historical_references_only=["use SECRET_KEY from environment"]),
            self._request(historical_references_only=["Authorization: Bearer token may be used"]),
            self._request(operator_note="runtime execution is authorized"),
            self._request(metadata={"nested": "Production BLK-test MCP is authorized"}),
            self._request(runtimeApproval=True),
        ]
        for request in bad_requests:
            with self.subTest(request=request):
                with self.assertRaises(ValueError):
                    build_kuronode_workspace_pilot_request(self._target(), request)

    def test_excluded_authorities_must_match_exact_set(self):
        missing = sorted(EXACT_EXCLUDED_AUTHORITIES - {"RUNTIME_BLK_TEST_EXECUTION_AGAINST_KURONODE"})
        extra = sorted(EXACT_EXCLUDED_AUTHORITIES | {"APPROVED_FOR_LIVE_EXECUTION"})
        duplicate = sorted(EXACT_EXCLUDED_AUTHORITIES) + [sorted(EXACT_EXCLUDED_AUTHORITIES)[0]]
        for authorities in [missing, extra, duplicate, [123]]:
            with self.subTest(authorities=authorities):
                with self.assertRaises(ValueError):
                    build_kuronode_workspace_pilot_request(
                        self._target(),
                        self._request(excluded_authorities=authorities),
                    )

    def test_no_side_effect_flags_must_be_exact_false_set(self):
        missing = {key: False for key in NO_SIDE_EFFECT_FLAGS if key != "kuronode_git_mutated"}
        true_flag = {key: False for key in NO_SIDE_EFFECT_FLAGS}
        true_flag["kuronode_source_mutated"] = True
        extra = {key: False for key in NO_SIDE_EFFECT_FLAGS}
        extra["runtime_started"] = False
        for flags in [missing, true_flag, extra, []]:
            with self.subTest(flags=flags):
                with self.assertRaises(ValueError):
                    build_kuronode_workspace_pilot_request(
                        self._target(),
                        self._request(no_side_effects=flags),
                    )

    def test_required_proof_markers_are_exact_and_not_placeholders(self):
        bad_marker_sets = [
            ["ok"],
            [
                "BLK_TEST_MODULE_NOT_BLK_SYSTEM_TEST_SUITE",
                "KURONODE_WORKSPACE_EXACT_TARGET_BOUND",
                "READ_ONLY_FIXED_TOOL_ONLY",
                "NO_CEB009_REUSE",
                "NO_SOURCE_OR_GIT_MUTATION_BY_BLK_TEST",
                "NO_PROTECTED_BODY_READ",
            ],
            [
                "BLK_TEST_MODULE_NOT_BLK_SYSTEM_TEST_SUITE",
                "KURONODE_WORKSPACE_EXACT_TARGET_BOUND",
                "READ_ONLY_FIXED_TOOL_ONLY",
                "NO_CEB009_REUSE",
                "NO_SOURCE_OR_GIT_MUTATION_BY_BLK_TEST",
                "NO_PROTECTED_BODY_READ",
                "BEO_RTM_AND_COVERAGE_AUTHORITY_SEPARATE",
                "APPROVED_FOR_LIVE_EXECUTION",
            ],
        ]
        for proof_markers in bad_marker_sets:
            with self.subTest(proof_markers=proof_markers):
                with self.assertRaises(ValueError):
                    build_kuronode_workspace_pilot_request(
                        self._target(),
                        self._request(proof_markers=proof_markers),
                    )


if __name__ == "__main__":
    unittest.main()
