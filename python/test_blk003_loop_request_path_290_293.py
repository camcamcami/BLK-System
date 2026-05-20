import copy
import unittest
from pathlib import Path

from blk_authority_smuggling import scan_for_authority_laundering
import blk_root_doctrine_gap_ladder_237_241 as root_ladder
from blk_req_production_gateway_195_199 import (
    build_blk_req_gateway_readiness_review_195,
    build_blk_req_production_gateway_contract_196,
)
from blk_identity_relay_spine_283_285 import (
    build_blk_id_identity_spine_contract_283,
    build_blk_relay_envelope_contract_284,
    build_identity_relay_loop_evidence_285,
)
from blk_speculative_quarantine_approval_286_289 import (
    build_approval_timing_contract_286,
    build_hitl_interaction_evidence_287,
    build_speculative_quarantine_evidence_288,
    build_promotion_or_purge_gate_289,
    hash_package,
)
from blk003_loop_request_path_290_293 import (
    Blk003LoopRequestPathValidationError,
    build_loop_request_contract_290,
    validate_loop_request_contract_290,
    build_beb_l2_route_request_binding_291,
    validate_beb_l2_route_request_binding_291,
    build_quarantine_gated_request_preflight_292,
    validate_quarantine_gated_request_preflight_292,
    build_loop_request_path_reconciliation_293,
    validate_loop_request_path_reconciliation_293,
)

ROOT = Path(__file__).resolve().parents[1]
BLK124 = ROOT / "docs" / "BLK-124_reusable-blk003-loop-request-path-contract.md"


def build_upstream_packages(decision="APPROVE", gate_decision=None, suffix="001"):
    identity = build_blk_id_identity_spine_contract_283()
    relay = build_blk_relay_envelope_contract_284(identity)
    selection = root_ladder.build_kuronode_route_selection_237()
    overlay = root_ladder.build_root_doctrine_deviation_overlay_238(selection)
    scope = root_ladder.decide_blk_id_relay_scope_239(overlay)
    gateway_contract = build_blk_req_production_gateway_contract_196(
        build_blk_req_gateway_readiness_review_195()
    )
    gateway = root_ladder.build_hitl_gateway_completion_slice_240(scope, gateway_contract)
    loop = root_ladder.build_reusable_blk003_loop_kernel_241(gateway)
    loop_evidence = build_identity_relay_loop_evidence_285(identity, relay, loop)
    approval_contract = build_approval_timing_contract_286(identity, relay, loop_evidence)
    interaction = build_hitl_interaction_evidence_287(
        approval_contract,
        identity,
        relay,
        approval_request_hash="sha256:" + "1" * 64,
        request_id=f"REQUEST-BLK-SYSTEM-290-HITL-{suffix}",
        discord_user_id="684235178083745819",
        discord_message_id="1488733359072084070",
        discord_interaction_id="1488733359072084071",
        component_custom_id=f"BLK-HITL-{decision.replace('_', '-')}-290",
        decision=decision,
        decided_at="2026-05-21T09:30:00+10:00",
        expires_at="2026-05-21T10:30:00+10:00",
    )
    quarantine = build_speculative_quarantine_evidence_288(
        approval_contract,
        interaction,
        run_id=f"RUN-BLK-SYSTEM-290-QUARANTINE-{suffix}",
        execution_timing_mode="speculative_quarantine",
        state="QUARANTINE_COMPLETE_AWAITING_DECISION",
        target_hash_before_quarantine="sha256:" + "2" * 64,
        manifest_hash="sha256:" + "3" * 64,
        result_hash="sha256:" + "4" * 64,
        report_hash="sha256:" + "5" * 64,
        quarantine_workspace_id=f"QUARANTINE-BLK-SYSTEM-290-{suffix}",
        started_at="2026-05-21T09:00:00+10:00",
        completed_at="2026-05-21T09:45:00+10:00",
    )
    gate = build_promotion_or_purge_gate_289(
        approval_contract,
        quarantine,
        interaction,
        decision=gate_decision or decision,
        decided_at="2026-05-21T09:50:00+10:00",
        target_hash_at_decision=quarantine["target_hash_before_quarantine"],
        selected_result_hash=quarantine["result_hash"],
    )
    return {
        "identity": identity,
        "relay": relay,
        "loop": loop,
        "loop_evidence": loop_evidence,
        "approval_contract": approval_contract,
        "interaction": interaction,
        "quarantine": quarantine,
        "gate": gate,
    }


def build_documented_request_path():
    upstream = build_upstream_packages()
    contract = build_loop_request_contract_290(
        upstream["loop"],
        upstream["approval_contract"],
    )
    binding = build_beb_l2_route_request_binding_291(
        contract,
        upstream["approval_contract"],
        upstream["quarantine"],
        upstream["interaction"],
        upstream["gate"],
        request_id="REQUEST-BLK-SYSTEM-291-ROUTE-001",
        beb_hash="sha256:" + "6" * 64,
        l2_packet_hash="sha256:" + "7" * 64,
        manifest_hash=upstream["quarantine"]["manifest_hash"],
        target_hash=upstream["quarantine"]["target_hash_before_quarantine"],
        allowed_modified_files_hash="sha256:" + "8" * 64,
        validation_profile_id="kuronode-worktree-static",
        trusted_root_hash="sha256:" + "9" * 64,
        trusted_workdir_hash="sha256:" + "a" * 64,
        codex_model="gpt-5.4",
    )
    preflight = build_quarantine_gated_request_preflight_292(
        contract,
        binding,
        upstream["approval_contract"],
        upstream["quarantine"],
        upstream["interaction"],
        upstream["gate"],
        observed_target_hash=upstream["quarantine"]["target_hash_before_quarantine"],
        private_bwrap_descriptor_hash="sha256:" + "a" * 64,
        validation_profile_hash="sha256:" + "b" * 64,
    )
    reconciliation = build_loop_request_path_reconciliation_293(
        contract,
        binding,
        preflight,
        upstream["approval_contract"],
        upstream["quarantine"],
        upstream["interaction"],
        upstream["gate"],
    )
    return upstream, contract, binding, preflight, reconciliation


class Blk003LoopRequestPath290To293Test(unittest.TestCase):
    def test_290_contract_binds_loop_kernel_and_quarantine_gate_without_runtime(self):
        upstream = build_upstream_packages()

        contract = build_loop_request_contract_290(
            upstream["loop"],
            upstream["approval_contract"],
        )

        self.assertEqual(contract["status"], "BLK003_LOOP_REQUEST_CONTRACT_READY")
        self.assertIn("BLK_SYSTEM_290_BLK003_LOOP_REQUEST_CONTRACT_READY", contract["markers"])
        self.assertEqual(contract["loop_kernel_hash"], upstream["loop"]["loop_kernel_hash"])
        self.assertEqual(
            contract["approval_timing_contract_hash"],
            upstream["approval_contract"]["approval_timing_contract_hash"],
        )
        self.assertIn("promotion_or_purge_gate_hash", contract["required_request_fields"])
        self.assertIn("target_hash", contract["required_request_fields"])
        self.assertTrue(contract["separate_exact_execution_package_required"])
        self.assertFalse(contract["side_effects"]["blk_pipe_runtime_started"])
        self.assertFalse(contract["side_effects"]["live_codex_dispatch_started"])
        self.assertFalse(contract["side_effects"]["target_source_git_mutation"])
        self.assertEqual(validate_loop_request_contract_290(contract), contract)

        forged_loop = copy.deepcopy(upstream["loop"])
        forged_loop["iteration_contract"]["approval_required_per_iteration"] = False
        forged_loop["loop_kernel_hash"] = hash_package(
            {k: v for k, v in forged_loop.items() if k != "loop_kernel_hash"}
        )
        with self.assertRaisesRegex(Blk003LoopRequestPathValidationError, "loop kernel"):
            build_loop_request_contract_290(forged_loop, upstream["approval_contract"])

    def test_291_binds_exact_beb_l2_route_to_gate_without_dispatch(self):
        upstream = build_upstream_packages()
        contract = build_loop_request_contract_290(
            upstream["loop"],
            upstream["approval_contract"],
        )

        binding = build_beb_l2_route_request_binding_291(
            contract,
            upstream["approval_contract"],
            upstream["quarantine"],
            upstream["interaction"],
            upstream["gate"],
            request_id="REQUEST-BLK-SYSTEM-291-ROUTE-001",
            beb_hash="sha256:" + "6" * 64,
            l2_packet_hash="sha256:" + "7" * 64,
            manifest_hash=upstream["quarantine"]["manifest_hash"],
            target_hash=upstream["quarantine"]["target_hash_before_quarantine"],
            allowed_modified_files_hash="sha256:" + "8" * 64,
            validation_profile_id="kuronode-worktree-static",
            trusted_root_hash="sha256:" + "9" * 64,
            trusted_workdir_hash="sha256:" + "a" * 64,
            codex_model="gpt-5.4",
        )

        self.assertEqual(binding["status"], "BEB_L2_ROUTE_REQUEST_BINDING_READY")
        self.assertIn("BLK_SYSTEM_291_BEB_L2_ROUTE_REQUEST_BINDING_READY", binding["markers"])
        self.assertEqual(binding["promotion_or_purge_gate_hash"], upstream["gate"]["promotion_or_purge_gate_hash"])
        self.assertEqual(binding["gate_outcome_state"], "APPROVED_PROMOTED")
        self.assertTrue(binding["gate_allows_promotion"])
        self.assertFalse(binding["runtime_dispatch_requested"])
        self.assertFalse(binding["side_effects"]["blk_pipe_runtime_started"])
        self.assertFalse(binding["side_effects"]["live_codex_dispatch_started"])
        self.assertFalse(binding["side_effects"]["target_source_git_mutation"])
        self.assertEqual(
            validate_beb_l2_route_request_binding_291(
                binding,
                contract,
                upstream["approval_contract"],
                upstream["quarantine"],
                upstream["interaction"],
                upstream["gate"],
            ),
            binding,
        )

        forged_gate = copy.deepcopy(upstream["gate"])
        forged_gate["outcome_state"] = "APPROVED_PROMOTED"
        forged_gate["promotion_gate_opened"] = True
        forged_gate["durable_target_mutation_performed"] = True
        forged_gate["promotion_or_purge_gate_hash"] = hash_package(
            {k: v for k, v in forged_gate.items() if k != "promotion_or_purge_gate_hash"}
        )
        with self.assertRaisesRegex(Blk003LoopRequestPathValidationError, "promotion/purge gate"):
            build_beb_l2_route_request_binding_291(
                contract,
                upstream["approval_contract"],
                upstream["quarantine"],
                upstream["interaction"],
                forged_gate,
                request_id="REQUEST-BLK-SYSTEM-291-ROUTE-FORGE",
                beb_hash="sha256:" + "6" * 64,
                l2_packet_hash="sha256:" + "7" * 64,
                manifest_hash=upstream["quarantine"]["manifest_hash"],
                target_hash=upstream["quarantine"]["target_hash_before_quarantine"],
                allowed_modified_files_hash="sha256:" + "8" * 64,
                validation_profile_id="kuronode-worktree-static",
                trusted_root_hash="sha256:" + "9" * 64,
                trusted_workdir_hash="sha256:" + "a" * 64,
                codex_model="gpt-5.4",
            )

    def test_292_preflight_passes_only_open_gate_and_blocks_stale_or_rejected_paths(self):
        upstream = build_upstream_packages()
        contract = build_loop_request_contract_290(
            upstream["loop"],
            upstream["approval_contract"],
        )
        binding = build_beb_l2_route_request_binding_291(
            contract,
            upstream["approval_contract"],
            upstream["quarantine"],
            upstream["interaction"],
            upstream["gate"],
            request_id="REQUEST-BLK-SYSTEM-292-ROUTE-001",
            beb_hash="sha256:" + "b" * 64,
            l2_packet_hash="sha256:" + "c" * 64,
            manifest_hash=upstream["quarantine"]["manifest_hash"],
            target_hash=upstream["quarantine"]["target_hash_before_quarantine"],
            allowed_modified_files_hash="sha256:" + "d" * 64,
            validation_profile_id="kuronode-worktree-static",
            trusted_root_hash="sha256:" + "e" * 64,
            trusted_workdir_hash="sha256:" + "f" * 64,
            codex_model="gpt-5.4",
        )

        preflight = build_quarantine_gated_request_preflight_292(
            contract,
            binding,
            upstream["approval_contract"],
            upstream["quarantine"],
            upstream["interaction"],
            upstream["gate"],
            observed_target_hash=upstream["quarantine"]["target_hash_before_quarantine"],
            private_bwrap_descriptor_hash="sha256:" + "a" * 64,
            validation_profile_hash="sha256:" + "b" * 64,
        )

        self.assertEqual(preflight["status"], "QUARANTINE_GATED_REQUEST_PREFLIGHT_READY")
        self.assertIn("BLK_SYSTEM_292_QUARANTINE_GATED_REQUEST_PREFLIGHT_READY", preflight["markers"])
        self.assertEqual(preflight["preflight_result"], "REQUEST_PATH_READY_FOR_SEPARATE_EXACT_EXECUTION")
        self.assertTrue(preflight["request_path_ready"])
        self.assertTrue(preflight["separate_exact_execution_package_required"])
        self.assertFalse(preflight["side_effects"]["blk_pipe_runtime_started"])
        self.assertFalse(preflight["side_effects"]["target_source_git_mutation"])
        self.assertEqual(
            validate_quarantine_gated_request_preflight_292(
                preflight,
                contract,
                binding,
                upstream["approval_contract"],
                upstream["quarantine"],
                upstream["interaction"],
                upstream["gate"],
            ),
            preflight,
        )

        stale = build_quarantine_gated_request_preflight_292(
            contract,
            binding,
            upstream["approval_contract"],
            upstream["quarantine"],
            upstream["interaction"],
            upstream["gate"],
            observed_target_hash="sha256:" + "1" * 64,
            private_bwrap_descriptor_hash="sha256:" + "a" * 64,
            validation_profile_hash="sha256:" + "b" * 64,
        )
        self.assertEqual(stale["preflight_result"], "REQUEST_PATH_BLOCKED_BY_TARGET_HASH_DRIFT")
        self.assertFalse(stale["request_path_ready"])

        rejected_upstream = build_upstream_packages(decision="DENY", suffix="DENY")
        reject_contract = build_loop_request_contract_290(
            rejected_upstream["loop"],
            rejected_upstream["approval_contract"],
        )
        rejected_binding = build_beb_l2_route_request_binding_291(
            reject_contract,
            rejected_upstream["approval_contract"],
            rejected_upstream["quarantine"],
            rejected_upstream["interaction"],
            rejected_upstream["gate"],
            request_id="REQUEST-BLK-SYSTEM-292-ROUTE-DENY",
            beb_hash="sha256:" + "b" * 64,
            l2_packet_hash="sha256:" + "c" * 64,
            manifest_hash=rejected_upstream["quarantine"]["manifest_hash"],
            target_hash=rejected_upstream["quarantine"]["target_hash_before_quarantine"],
            allowed_modified_files_hash="sha256:" + "d" * 64,
            validation_profile_id="kuronode-worktree-static",
            trusted_root_hash="sha256:" + "e" * 64,
            trusted_workdir_hash="sha256:" + "f" * 64,
            codex_model="gpt-5.4",
        )
        rejected_preflight = build_quarantine_gated_request_preflight_292(
            reject_contract,
            rejected_binding,
            rejected_upstream["approval_contract"],
            rejected_upstream["quarantine"],
            rejected_upstream["interaction"],
            rejected_upstream["gate"],
            observed_target_hash=rejected_upstream["quarantine"]["target_hash_before_quarantine"],
            private_bwrap_descriptor_hash="sha256:" + "a" * 64,
            validation_profile_hash="sha256:" + "b" * 64,
        )
        self.assertEqual(rejected_preflight["preflight_result"], "REQUEST_PATH_BLOCKED_BY_QUARANTINE_GATE")
        self.assertTrue(rejected_preflight["purge_required_or_completed"])
        self.assertFalse(rejected_preflight["request_path_ready"])

    def test_292_rejects_running_state_laundering_and_unsafe_route_claims(self):
        upstream = build_upstream_packages()
        contract = build_loop_request_contract_290(
            upstream["loop"],
            upstream["approval_contract"],
        )

        with self.assertRaisesRegex(Blk003LoopRequestPathValidationError, "authority wording|validation_profile_id"):
            build_beb_l2_route_request_binding_291(
                contract,
                upstream["approval_contract"],
                upstream["quarantine"],
                upstream["interaction"],
                upstream["gate"],
                request_id="REQUEST-BLK-SYSTEM-292-ROUTE-BAD",
                beb_hash="sha256:" + "b" * 64,
                l2_packet_hash="sha256:" + "c" * 64,
                manifest_hash=upstream["quarantine"]["manifest_hash"],
                target_hash=upstream["quarantine"]["target_hash_before_quarantine"],
                allowed_modified_files_hash="sha256:" + "d" * 64,
                validation_profile_id="codexApproval",
                trusted_root_hash="sha256:" + "e" * 64,
                trusted_workdir_hash="sha256:" + "f" * 64,
                codex_model="gpt-5.4",
            )

        forged_quarantine = copy.deepcopy(upstream["quarantine"])
        forged_quarantine["state"] = "QUARANTINE_RUNNING"
        forged_quarantine["quarantine_evidence_hash"] = hash_package(
            {k: v for k, v in forged_quarantine.items() if k != "quarantine_evidence_hash"}
        )
        with self.assertRaisesRegex(Blk003LoopRequestPathValidationError, "quarantine evidence"):
            build_beb_l2_route_request_binding_291(
                contract,
                upstream["approval_contract"],
                forged_quarantine,
                upstream["interaction"],
                upstream["gate"],
                request_id="REQUEST-BLK-SYSTEM-292-ROUTE-RUNNING",
                beb_hash="sha256:" + "b" * 64,
                l2_packet_hash="sha256:" + "c" * 64,
                manifest_hash=upstream["quarantine"]["manifest_hash"],
                target_hash=upstream["quarantine"]["target_hash_before_quarantine"],
                allowed_modified_files_hash="sha256:" + "d" * 64,
                validation_profile_id="kuronode-worktree-static",
                trusted_root_hash="sha256:" + "e" * 64,
                trusted_workdir_hash="sha256:" + "f" * 64,
                codex_model="gpt-5.4",
            )

    def test_293_reconciles_request_path_and_names_next_frontier_without_live_authority(self):
        upstream = build_upstream_packages()
        contract = build_loop_request_contract_290(
            upstream["loop"],
            upstream["approval_contract"],
        )
        binding = build_beb_l2_route_request_binding_291(
            contract,
            upstream["approval_contract"],
            upstream["quarantine"],
            upstream["interaction"],
            upstream["gate"],
            request_id="REQUEST-BLK-SYSTEM-293-ROUTE-001",
            beb_hash="sha256:" + "b" * 64,
            l2_packet_hash="sha256:" + "c" * 64,
            manifest_hash=upstream["quarantine"]["manifest_hash"],
            target_hash=upstream["quarantine"]["target_hash_before_quarantine"],
            allowed_modified_files_hash="sha256:" + "d" * 64,
            validation_profile_id="kuronode-worktree-static",
            trusted_root_hash="sha256:" + "e" * 64,
            trusted_workdir_hash="sha256:" + "f" * 64,
            codex_model="gpt-5.4",
        )
        preflight = build_quarantine_gated_request_preflight_292(
            contract,
            binding,
            upstream["approval_contract"],
            upstream["quarantine"],
            upstream["interaction"],
            upstream["gate"],
            observed_target_hash=upstream["quarantine"]["target_hash_before_quarantine"],
            private_bwrap_descriptor_hash="sha256:" + "a" * 64,
            validation_profile_hash="sha256:" + "b" * 64,
        )

        reconciliation = build_loop_request_path_reconciliation_293(
            contract,
            binding,
            preflight,
            upstream["approval_contract"],
            upstream["quarantine"],
            upstream["interaction"],
            upstream["gate"],
        )

        self.assertEqual(reconciliation["status"], "REUSABLE_BLK003_LOOP_REQUEST_PATH_RECONCILED")
        self.assertIn(
            "BLK_SYSTEM_293_REUSABLE_BLK003_LOOP_REQUEST_PATH_RECONCILED",
            reconciliation["markers"],
        )
        self.assertEqual(reconciliation["reconciled_state"], "REQUEST_PATH_READY_EXECUTION_NOT_GRANTED")
        self.assertEqual(
            reconciliation["next_frontier"],
            "NEXT_FRONTIER_EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_PACKAGE_REQUIRED_NOT_GRANTED",
        )
        self.assertTrue(reconciliation["separate_exact_execution_package_required"])
        self.assertFalse(reconciliation["side_effects"]["blk_pipe_runtime_started"])
        self.assertFalse(reconciliation["side_effects"]["live_codex_dispatch_started"])
        self.assertFalse(reconciliation["side_effects"]["target_source_git_mutation"])
        self.assertEqual(
            validate_loop_request_path_reconciliation_293(
                reconciliation,
                contract,
                binding,
                preflight,
                upstream["approval_contract"],
                upstream["quarantine"],
                upstream["interaction"],
                upstream["gate"],
            ),
            reconciliation,
        )

        forged = copy.deepcopy(reconciliation)
        forged["next_frontier"] = "NEXT_FRONTIER_REUSABLE_CODEX_DISPATCH_GRANTED"
        forged["reconciliation_hash"] = hash_package(
            {k: v for k, v in forged.items() if k != "reconciliation_hash"}
        )
        with self.assertRaisesRegex(Blk003LoopRequestPathValidationError, "next_frontier|authority wording"):
            validate_loop_request_path_reconciliation_293(
                forged,
                contract,
                binding,
                preflight,
                upstream["approval_contract"],
                upstream["quarantine"],
                upstream["interaction"],
                upstream["gate"],
            )


    def test_exact_marker_lists_block_nested_authority_marker_laundering(self):
        upstream, contract, binding, preflight, _reconciliation = build_documented_request_path()

        forged_contract = copy.deepcopy(contract)
        forged_contract["markers"].append("REUSABLE_CODEX_DISPATCH_GRANTED")
        forged_contract["loop_request_contract_hash"] = hash_package(
            {k: v for k, v in forged_contract.items() if k != "loop_request_contract_hash"}
        )
        with self.assertRaisesRegex(Blk003LoopRequestPathValidationError, "markers mismatch|authority wording"):
            validate_loop_request_contract_290(forged_contract)

        forged_preflight = copy.deepcopy(preflight)
        forged_preflight["markers"].append("BROAD_BLK_PIPE_DISPATCH_GRANTED")
        forged_preflight["preflight_hash"] = hash_package(
            {k: v for k, v in forged_preflight.items() if k != "preflight_hash"}
        )
        with self.assertRaisesRegex(Blk003LoopRequestPathValidationError, "markers mismatch|authority wording"):
            validate_quarantine_gated_request_preflight_292(
                forged_preflight,
                contract,
                binding,
                upstream["approval_contract"],
                upstream["quarantine"],
                upstream["interaction"],
                upstream["gate"],
            )

    def test_293_revalidates_preflight_instead_of_trusting_self_hashed_ready_flag(self):
        upstream, contract, binding, preflight, _reconciliation = build_documented_request_path()

        forged_preflight = copy.deepcopy(preflight)
        forged_preflight["observed_target_hash"] = "sha256:" + "1" * 64
        forged_preflight["target_hash_rechecked"] = False
        forged_preflight["preflight_result"] = "REQUEST_PATH_READY_FOR_SEPARATE_EXACT_EXECUTION"
        forged_preflight["request_path_ready"] = True
        forged_preflight["preflight_hash"] = hash_package(
            {k: v for k, v in forged_preflight.items() if k != "preflight_hash"}
        )

        with self.assertRaisesRegex(
            Blk003LoopRequestPathValidationError,
            "preflight result mismatch|target hash flag mismatch",
        ):
            build_loop_request_path_reconciliation_293(
                contract,
                binding,
                forged_preflight,
                upstream["approval_contract"],
                upstream["quarantine"],
                upstream["interaction"],
                upstream["gate"],
            )

    def test_blk124_contract_doc_makes_request_path_boundary_review_obvious(self):
        self.assertTrue(BLK124.exists(), "BLK-124 loop request path contract doc is missing")
        text = BLK124.read_text()
        self.assertEqual(scan_for_authority_laundering(text, path=str(BLK124)), [])

        _upstream, contract, binding, preflight, reconciliation = build_documented_request_path()
        for marker in [
            "BLK-124 — Reusable BLK-003 Loop Request Path Contract",
            "BLK_SYSTEM_290_BLK003_LOOP_REQUEST_CONTRACT_READY",
            "BLK_SYSTEM_291_BEB_L2_ROUTE_REQUEST_BINDING_READY",
            "BLK_SYSTEM_292_QUARANTINE_GATED_REQUEST_PREFLIGHT_READY",
            "BLK_SYSTEM_293_REUSABLE_BLK003_LOOP_REQUEST_PATH_RECONCILED",
            "NEXT_FRONTIER_EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_PACKAGE_REQUIRED_NOT_GRANTED",
            "no BLK-pipe runtime",
            "no reusable Codex dispatch",
            "no BEO closeout execution",
            f"blk290_loop_request_contract_hash={contract['loop_request_contract_hash']}",
            f"blk291_route_request_binding_hash={binding['route_request_binding_hash']}",
            f"blk292_preflight_hash={preflight['preflight_hash']}",
            f"blk293_reconciliation_hash={reconciliation['reconciliation_hash']}",
        ]:
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
