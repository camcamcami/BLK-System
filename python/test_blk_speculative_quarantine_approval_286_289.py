import copy
import unittest
from pathlib import Path

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
    SpeculativeQuarantineValidationError,
    build_approval_timing_contract_286,
    validate_approval_timing_contract_286,
    build_hitl_interaction_evidence_287,
    validate_hitl_interaction_evidence_287,
    build_speculative_quarantine_evidence_288,
    validate_speculative_quarantine_evidence_288,
    build_promotion_or_purge_gate_289,
    validate_promotion_or_purge_gate_289,
    hash_package,
)


def build_upstream_packages():
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
    return identity, relay, loop_evidence


ROOT = Path(__file__).resolve().parents[1]
BLK123 = ROOT / "docs" / "BLK-123_speculative-quarantine-approval-contract.md"


class BlkSpeculativeQuarantineApproval286To289Test(unittest.TestCase):
    def test_286_contract_names_discord_first_timing_modes_and_denies_adjacent_authority(self):
        identity, relay, loop_evidence = build_upstream_packages()

        contract = build_approval_timing_contract_286(identity, relay, loop_evidence)

        self.assertEqual(contract["status"], "SPECULATIVE_QUARANTINE_APPROVAL_CONTRACT_READY")
        self.assertIn("BLK_SYSTEM_286_SPECULATIVE_QUARANTINE_APPROVAL_CONTRACT_READY", contract["markers"])
        self.assertEqual(contract["primary_ux"], "discord_component_button_selector_first")
        self.assertFalse(contract["fallback_short_challenge"]["long_copy_paste_required"])
        self.assertIn("pre_approval_blocked", contract["execution_timing_modes"])
        self.assertIn("speculative_quarantine", contract["execution_timing_modes"])
        self.assertIn("config_policy_bypass", contract["execution_timing_modes"])
        self.assertIn("QUARANTINE_COMPLETE_AWAITING_DECISION", contract["state_model"])
        self.assertIn("APPROVE", contract["allowed_decisions"])
        self.assertIn("DENY", contract["allowed_decisions"])
        self.assertFalse(contract["side_effects"]["source_git_mutation_before_approval"])
        self.assertFalse(contract["side_effects"]["relay_network_runtime_created"])
        self.assertFalse(contract["side_effects"]["approval_reuse"])
        self.assertRegex(contract["approval_timing_contract_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(validate_approval_timing_contract_286(contract), contract)

    def test_286_rejects_rehashed_upstreams_and_vague_fast_mode(self):
        identity, relay, loop_evidence = build_upstream_packages()
        tampered_identity = copy.deepcopy(identity)
        tampered_identity["markers"].append("FAST_MODE_ENABLED")
        tampered_identity["identity_contract_hash"] = hash_package(
            {k: v for k, v in tampered_identity.items() if k != "identity_contract_hash"}
        )

        with self.assertRaisesRegex(SpeculativeQuarantineValidationError, "canonical BLK-283|relay contract"):
            build_approval_timing_contract_286(tampered_identity, relay, loop_evidence)

        contract = build_approval_timing_contract_286(identity, relay, loop_evidence)
        tampered_contract = copy.deepcopy(contract)
        tampered_contract["execution_timing_modes"].append("fast_mode")
        tampered_contract["approval_timing_contract_hash"] = hash_package(
            {k: v for k, v in tampered_contract.items() if k != "approval_timing_contract_hash"}
        )
        with self.assertRaisesRegex(SpeculativeQuarantineValidationError, "execution_timing_modes"):
            validate_approval_timing_contract_286(tampered_contract)

    def test_287_interaction_binds_actor_approval_identity_and_relay_without_copy_paste_or_transport(self):
        identity, relay, loop_evidence = build_upstream_packages()
        contract = build_approval_timing_contract_286(identity, relay, loop_evidence)

        interaction = build_hitl_interaction_evidence_287(
            contract,
            identity,
            relay,
            approval_request_hash="sha256:" + "1" * 64,
            request_id="REQUEST-BLK-SYSTEM-287-HITL-001",
            discord_user_id="684235178083745819",
            discord_message_id="1488733359072084070",
            discord_interaction_id="1488733359072084071",
            component_custom_id="BLK-HITL-APPROVE-287",
            decision="APPROVE",
            decided_at="2026-05-20T21:30:00+10:00",
            expires_at="2026-05-20T22:00:00+10:00",
        )

        self.assertEqual(interaction["status"], "HITL_INTERACTION_IDENTITY_RELAY_EVIDENCE_READY")
        self.assertIn("BLK_SYSTEM_287_HITL_INTERACTION_IDENTITY_RELAY_EVIDENCE_READY", interaction["markers"])
        self.assertTrue(interaction["discord_component_interaction"])
        self.assertFalse(interaction["long_copy_paste_required"])
        self.assertEqual(interaction["decision"], "APPROVE")
        self.assertRegex(interaction["actor_identity_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertRegex(interaction["approval_identity_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertRegex(interaction["hitl_relay_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertFalse(interaction["side_effects"]["message_dispatch_authorized"])
        self.assertFalse(interaction["side_effects"]["approval_reuse"])
        self.assertFalse(interaction["side_effects"]["target_source_git_mutation"])
        self.assertEqual(validate_hitl_interaction_evidence_287(interaction, contract), interaction)

    def test_287_rejects_unicode_snowflakes_unbound_decisions_and_transport_laundering(self):
        identity, relay, loop_evidence = build_upstream_packages()
        contract = build_approval_timing_contract_286(identity, relay, loop_evidence)

        with self.assertRaisesRegex(SpeculativeQuarantineValidationError, "ASCII decimal Discord snowflake"):
            build_hitl_interaction_evidence_287(
                contract,
                identity,
                relay,
                approval_request_hash="sha256:" + "2" * 64,
                request_id="REQUEST-BLK-SYSTEM-287-HITL-002",
                discord_user_id="６８４２３５１７８０８３７４５８１９",
                discord_message_id="1488733359072084070",
                discord_interaction_id="1488733359072084071",
                component_custom_id="BLK-HITL-APPROVE-287",
                decision="APPROVE",
                decided_at="2026-05-20T21:30:00+10:00",
                expires_at="2026-05-20T22:00:00+10:00",
            )

        with self.assertRaisesRegex(SpeculativeQuarantineValidationError, "decision"):
            build_hitl_interaction_evidence_287(
                contract,
                identity,
                relay,
                approval_request_hash="sha256:" + "3" * 64,
                request_id="REQUEST-BLK-SYSTEM-287-HITL-003",
                discord_user_id="684235178083745819",
                discord_message_id="1488733359072084070",
                discord_interaction_id="1488733359072084071",
                component_custom_id="BLK-HITL-APPROVE-287",
                decision="APPROVED",
                decided_at="2026-05-20T21:30:00+10:00",
                expires_at="2026-05-20T22:00:00+10:00",
            )

        with self.assertRaisesRegex(SpeculativeQuarantineValidationError, "forbidden authority wording|component"):
            build_hitl_interaction_evidence_287(
                contract,
                identity,
                relay,
                approval_request_hash="sha256:" + "4" * 64,
                request_id="REQUEST-BLK-SYSTEM-287-HITL-004",
                discord_user_id="684235178083745819",
                discord_message_id="1488733359072084070",
                discord_interaction_id="1488733359072084071",
                component_custom_id="MCP-TRANSPORT-ENABLED",
                decision="APPROVE",
                decided_at="2026-05-20T21:30:00+10:00",
                expires_at="2026-05-20T22:00:00+10:00",
            )

    def test_288_quarantine_evidence_allows_preapproval_compute_only_without_target_mutation(self):
        identity, relay, loop_evidence = build_upstream_packages()
        contract = build_approval_timing_contract_286(identity, relay, loop_evidence)
        interaction = build_hitl_interaction_evidence_287(
            contract,
            identity,
            relay,
            approval_request_hash="sha256:" + "5" * 64,
            request_id="REQUEST-BLK-SYSTEM-288-HITL-001",
            discord_user_id="684235178083745819",
            discord_message_id="1488733359072084070",
            discord_interaction_id="1488733359072084071",
            component_custom_id="BLK-HITL-APPROVE-288",
            decision="APPROVE",
            decided_at="2026-05-20T21:30:00+10:00",
            expires_at="2026-05-20T22:00:00+10:00",
        )

        quarantine = build_speculative_quarantine_evidence_288(
            contract,
            interaction,
            run_id="RUN-BLK-SYSTEM-288-QUARANTINE-001",
            execution_timing_mode="speculative_quarantine",
            state="QUARANTINE_COMPLETE_AWAITING_DECISION",
            target_hash_before_quarantine="sha256:" + "6" * 64,
            manifest_hash="sha256:" + "7" * 64,
            result_hash="sha256:" + "8" * 64,
            report_hash="sha256:" + "9" * 64,
            quarantine_workspace_id="QUARANTINE-BLK-SYSTEM-288-001",
            started_at="2026-05-20T21:20:00+10:00",
            completed_at="2026-05-20T21:45:00+10:00",
        )

        self.assertEqual(quarantine["status"], "SPECULATIVE_QUARANTINE_EVIDENCE_READY")
        self.assertIn("BLK_SYSTEM_288_SPECULATIVE_QUARANTINE_EVIDENCE_READY", quarantine["markers"])
        self.assertTrue(quarantine["pre_approval_compute_performed"])
        self.assertFalse(quarantine["promotion_performed"])
        self.assertFalse(quarantine["target_repo_mutated"])
        self.assertFalse(quarantine["external_side_effects"]["codex_model_api_called"])
        self.assertFalse(quarantine["external_side_effects"]["network_called"])
        self.assertFalse(quarantine["side_effects"]["target_source_git_mutation"])
        self.assertEqual(validate_speculative_quarantine_evidence_288(quarantine, contract, interaction), quarantine)

    def test_288_rejects_non_quarantine_workspace_and_unrecorded_external_side_effects(self):
        identity, relay, loop_evidence = build_upstream_packages()
        contract = build_approval_timing_contract_286(identity, relay, loop_evidence)
        interaction = build_hitl_interaction_evidence_287(
            contract,
            identity,
            relay,
            approval_request_hash="sha256:" + "a" * 64,
            request_id="REQUEST-BLK-SYSTEM-288-HITL-002",
            discord_user_id="684235178083745819",
            discord_message_id="1488733359072084070",
            discord_interaction_id="1488733359072084071",
            component_custom_id="BLK-HITL-APPROVE-288",
            decision="APPROVE",
            decided_at="2026-05-20T21:30:00+10:00",
            expires_at="2026-05-20T22:00:00+10:00",
        )

        with self.assertRaisesRegex(SpeculativeQuarantineValidationError, "quarantine_workspace_id"):
            build_speculative_quarantine_evidence_288(
                contract,
                interaction,
                run_id="RUN-BLK-SYSTEM-288-QUARANTINE-002",
                execution_timing_mode="speculative_quarantine",
                state="QUARANTINE_COMPLETE_AWAITING_DECISION",
                target_hash_before_quarantine="sha256:" + "b" * 64,
                manifest_hash="sha256:" + "c" * 64,
                result_hash="sha256:" + "d" * 64,
                report_hash="sha256:" + "e" * 64,
                quarantine_workspace_id="/home/dad/Kuronode",
                started_at="2026-05-20T21:20:00+10:00",
                completed_at="2026-05-20T21:45:00+10:00",
            )

        with self.assertRaisesRegex(SpeculativeQuarantineValidationError, "external_side_effects"):
            build_speculative_quarantine_evidence_288(
                contract,
                interaction,
                run_id="RUN-BLK-SYSTEM-288-QUARANTINE-003",
                execution_timing_mode="speculative_quarantine",
                state="QUARANTINE_COMPLETE_AWAITING_DECISION",
                target_hash_before_quarantine="sha256:" + "f" * 64,
                manifest_hash="sha256:" + "1" * 64,
                result_hash="sha256:" + "2" * 64,
                report_hash="sha256:" + "3" * 64,
                quarantine_workspace_id="QUARANTINE-BLK-SYSTEM-288-003",
                started_at="2026-05-20T21:20:00+10:00",
                completed_at="2026-05-20T21:45:00+10:00",
                external_side_effects={"codex_model_api_called": True, "network_called": False, "package_manager_called": False},
            )

    def test_289_gate_opens_only_for_exact_result_and_target_hash_match(self):
        identity, relay, loop_evidence = build_upstream_packages()
        contract = build_approval_timing_contract_286(identity, relay, loop_evidence)
        interaction = build_hitl_interaction_evidence_287(
            contract,
            identity,
            relay,
            approval_request_hash="sha256:" + "4" * 64,
            request_id="REQUEST-BLK-SYSTEM-289-HITL-001",
            discord_user_id="684235178083745819",
            discord_message_id="1488733359072084070",
            discord_interaction_id="1488733359072084071",
            component_custom_id="BLK-HITL-APPROVE-289",
            decision="APPROVE",
            decided_at="2026-05-20T21:30:00+10:00",
            expires_at="2026-05-20T22:00:00+10:00",
        )
        quarantine = build_speculative_quarantine_evidence_288(
            contract,
            interaction,
            run_id="RUN-BLK-SYSTEM-289-QUARANTINE-001",
            execution_timing_mode="speculative_quarantine",
            state="QUARANTINE_COMPLETE_AWAITING_DECISION",
            target_hash_before_quarantine="sha256:" + "5" * 64,
            manifest_hash="sha256:" + "6" * 64,
            result_hash="sha256:" + "7" * 64,
            report_hash="sha256:" + "8" * 64,
            quarantine_workspace_id="QUARANTINE-BLK-SYSTEM-289-001",
            started_at="2026-05-20T21:20:00+10:00",
            completed_at="2026-05-20T21:45:00+10:00",
        )

        gate = build_promotion_or_purge_gate_289(
            contract,
            quarantine,
            interaction,
            decision="APPROVE",
            decided_at="2026-05-20T21:50:00+10:00",
            target_hash_at_decision=quarantine["target_hash_before_quarantine"],
            selected_result_hash=quarantine["result_hash"],
        )

        self.assertEqual(gate["status"], "PROMOTION_PURGE_STALE_GATE_READY")
        self.assertEqual(gate["outcome_state"], "APPROVED_PROMOTED")
        self.assertTrue(gate["promotion_gate_opened"])
        self.assertFalse(gate["purge_performed"])
        self.assertFalse(gate["durable_target_mutation_performed"])
        self.assertEqual(gate["selected_result_hash"], quarantine["result_hash"])
        self.assertFalse(gate["side_effects"]["target_source_git_mutation"])
        self.assertEqual(validate_promotion_or_purge_gate_289(gate, contract, quarantine, interaction), gate)

        with self.assertRaisesRegex(SpeculativeQuarantineValidationError, "precede HITL decision|precede quarantine completion"):
            build_promotion_or_purge_gate_289(
                contract,
                quarantine,
                interaction,
                decision="APPROVE",
                decided_at="2026-05-20T21:00:00+10:00",
                target_hash_at_decision=quarantine["target_hash_before_quarantine"],
                selected_result_hash=quarantine["result_hash"],
            )

    def test_289_rejects_pending_expired_stale_or_result_mismatch_promotion(self):
        identity, relay, loop_evidence = build_upstream_packages()
        contract = build_approval_timing_contract_286(identity, relay, loop_evidence)

        def make_quarantine(decision: str, suffix: str, target_hex: str, result_hex: str):
            interaction = build_hitl_interaction_evidence_287(
                contract,
                identity,
                relay,
                approval_request_hash="sha256:" + target_hex * 64,
                request_id=f"REQUEST-BLK-SYSTEM-289-HITL-{suffix}",
                discord_user_id="684235178083745819",
                discord_message_id="1488733359072084070",
                discord_interaction_id="1488733359072084071",
                component_custom_id=f"BLK-HITL-{decision.replace('_', '-')}-289",
                decision=decision,
                decided_at="2026-05-20T21:30:00+10:00",
                expires_at="2026-05-20T22:00:00+10:00",
            )
            quarantine = build_speculative_quarantine_evidence_288(
                contract,
                interaction,
                run_id=f"RUN-BLK-SYSTEM-289-QUARANTINE-{suffix}",
                execution_timing_mode="speculative_quarantine",
                state="QUARANTINE_COMPLETE_AWAITING_DECISION",
                target_hash_before_quarantine="sha256:" + target_hex * 64,
                manifest_hash="sha256:" + "b" * 64,
                result_hash="sha256:" + result_hex * 64,
                report_hash="sha256:" + "d" * 64,
                quarantine_workspace_id=f"QUARANTINE-BLK-SYSTEM-289-{suffix}",
                started_at="2026-05-20T21:20:00+10:00",
                completed_at="2026-05-20T21:45:00+10:00",
            )
            return interaction, quarantine

        reject_interaction, reject_quarantine = make_quarantine("DENY", "DENY", "a", "c")
        rejected = build_promotion_or_purge_gate_289(
            contract,
            reject_quarantine,
            reject_interaction,
            decision="DENY",
            decided_at="2026-05-20T21:50:00+10:00",
            target_hash_at_decision=reject_quarantine["target_hash_before_quarantine"],
            selected_result_hash=reject_quarantine["result_hash"],
        )
        self.assertEqual(rejected["outcome_state"], "REJECTED_PURGED")
        self.assertFalse(rejected["promotion_gate_opened"])
        self.assertTrue(rejected["purge_performed"])
        self.assertRegex(rejected["purge_receipt_hash"], r"^sha256:[0-9a-f]{64}$")

        approve_interaction, approve_quarantine = make_quarantine("APPROVE", "APPR", "a", "c")
        expired = build_promotion_or_purge_gate_289(
            contract,
            approve_quarantine,
            approve_interaction,
            decision="EXPIRE",
            decided_at="2026-05-20T22:10:00+10:00",
            target_hash_at_decision=approve_quarantine["target_hash_before_quarantine"],
            selected_result_hash=approve_quarantine["result_hash"],
        )
        self.assertEqual(expired["outcome_state"], "EXPIRED_PURGED")
        self.assertTrue(expired["purge_performed"])

        dry_interaction, dry_quarantine = make_quarantine("APPROVE_DRY_RUN_ONLY", "DRYO", "a", "c")
        dry_run_only = build_promotion_or_purge_gate_289(
            contract,
            dry_quarantine,
            dry_interaction,
            decision="APPROVE_DRY_RUN_ONLY",
            decided_at="2026-05-20T21:50:00+10:00",
            target_hash_at_decision=dry_quarantine["target_hash_before_quarantine"],
            selected_result_hash=dry_quarantine["result_hash"],
        )
        self.assertEqual(dry_run_only["outcome_state"], "DRY_RUN_ONLY_PURGED")
        self.assertFalse(dry_run_only["promotion_gate_opened"])
        self.assertTrue(dry_run_only["purge_performed"])

        stale = build_promotion_or_purge_gate_289(
            contract,
            approve_quarantine,
            approve_interaction,
            decision="APPROVE",
            decided_at="2026-05-20T21:50:00+10:00",
            target_hash_at_decision="sha256:" + "e" * 64,
            selected_result_hash=approve_quarantine["result_hash"],
        )
        self.assertEqual(stale["outcome_state"], "STALE_TARGET_HASH_BLOCKED")
        self.assertFalse(stale["promotion_gate_opened"])
        self.assertTrue(stale["purge_performed"])

        with self.assertRaisesRegex(SpeculativeQuarantineValidationError, "selected_result_hash"):
            build_promotion_or_purge_gate_289(
                contract,
                approve_quarantine,
                approve_interaction,
                decision="APPROVE",
                decided_at="2026-05-20T21:50:00+10:00",
                target_hash_at_decision=approve_quarantine["target_hash_before_quarantine"],
                selected_result_hash="sha256:" + "f" * 64,
            )

    def test_289_rejects_gate_decision_mismatch_with_hitl_interaction(self):
        identity, relay, loop_evidence = build_upstream_packages()
        contract = build_approval_timing_contract_286(identity, relay, loop_evidence)
        interaction = build_hitl_interaction_evidence_287(
            contract,
            identity,
            relay,
            approval_request_hash="sha256:" + "1" * 64,
            request_id="REQUEST-BLK-SYSTEM-289-HITL-DENY",
            discord_user_id="684235178083745819",
            discord_message_id="1488733359072084070",
            discord_interaction_id="1488733359072084071",
            component_custom_id="BLK-HITL-DENY-289",
            decision="DENY",
            decided_at="2026-05-20T21:30:00+10:00",
            expires_at="2026-05-20T22:00:00+10:00",
        )
        quarantine = build_speculative_quarantine_evidence_288(
            contract,
            interaction,
            run_id="RUN-BLK-SYSTEM-289-QUARANTINE-DENY",
            execution_timing_mode="speculative_quarantine",
            state="QUARANTINE_COMPLETE_AWAITING_DECISION",
            target_hash_before_quarantine="sha256:" + "2" * 64,
            manifest_hash="sha256:" + "3" * 64,
            result_hash="sha256:" + "4" * 64,
            report_hash="sha256:" + "5" * 64,
            quarantine_workspace_id="QUARANTINE-BLK-SYSTEM-289-DENY",
            started_at="2026-05-20T21:20:00+10:00",
            completed_at="2026-05-20T21:45:00+10:00",
        )

        with self.assertRaisesRegex(SpeculativeQuarantineValidationError, "decision mismatch"):
            build_promotion_or_purge_gate_289(
                contract,
                quarantine,
                interaction,
                decision="APPROVE",
                decided_at="2026-05-20T21:50:00+10:00",
                target_hash_at_decision=quarantine["target_hash_before_quarantine"],
                selected_result_hash=quarantine["result_hash"],
            )

        forged_quarantine = copy.deepcopy(quarantine)
        forged_quarantine["hitl_decision"] = "APPROVE"
        forged_quarantine["hitl_interaction_hash"] = "sha256:" + "a" * 64
        forged_quarantine["quarantine_evidence_hash"] = hash_package(
            {k: v for k, v in forged_quarantine.items() if k != "quarantine_evidence_hash"}
        )
        with self.assertRaisesRegex(SpeculativeQuarantineValidationError, "interaction hash|HITL decision"):
            build_promotion_or_purge_gate_289(
                contract,
                forged_quarantine,
                interaction,
                decision="APPROVE",
                decided_at="2026-05-20T21:50:00+10:00",
                target_hash_at_decision=quarantine["target_hash_before_quarantine"],
                selected_result_hash=quarantine["result_hash"],
            )

    def test_289_validator_recomputes_outcome_and_quarantine_integrity(self):
        identity, relay, loop_evidence = build_upstream_packages()
        contract = build_approval_timing_contract_286(identity, relay, loop_evidence)
        interaction = build_hitl_interaction_evidence_287(
            contract,
            identity,
            relay,
            approval_request_hash="sha256:" + "6" * 64,
            request_id="REQUEST-BLK-SYSTEM-289-HITL-FORGE",
            discord_user_id="684235178083745819",
            discord_message_id="1488733359072084070",
            discord_interaction_id="1488733359072084071",
            component_custom_id="BLK-HITL-APPROVE-289",
            decision="APPROVE",
            decided_at="2026-05-20T21:30:00+10:00",
            expires_at="2026-05-20T22:00:00+10:00",
        )
        quarantine = build_speculative_quarantine_evidence_288(
            contract,
            interaction,
            run_id="RUN-BLK-SYSTEM-289-QUARANTINE-FORGE",
            execution_timing_mode="speculative_quarantine",
            state="QUARANTINE_COMPLETE_AWAITING_DECISION",
            target_hash_before_quarantine="sha256:" + "7" * 64,
            manifest_hash="sha256:" + "8" * 64,
            result_hash="sha256:" + "9" * 64,
            report_hash="sha256:" + "a" * 64,
            quarantine_workspace_id="QUARANTINE-BLK-SYSTEM-289-FORGE",
            started_at="2026-05-20T21:20:00+10:00",
            completed_at="2026-05-20T21:45:00+10:00",
        )
        gate = build_promotion_or_purge_gate_289(
            contract,
            quarantine,
            interaction,
            decision="APPROVE",
            decided_at="2026-05-20T21:50:00+10:00",
            target_hash_at_decision=quarantine["target_hash_before_quarantine"],
            selected_result_hash=quarantine["result_hash"],
        )

        forged_gate = copy.deepcopy(gate)
        forged_gate["outcome_state"] = "REJECTED_PURGED"
        forged_gate["promotion_gate_opened"] = False
        forged_gate["purge_performed"] = True
        forged_gate["purge_receipt_hash"] = hash_package(
            {
                "quarantine_evidence_hash": forged_gate["quarantine_evidence_hash"],
                "outcome_state": forged_gate["outcome_state"],
                "target_hash_at_decision": forged_gate["target_hash_at_decision"],
            }
        )
        forged_gate["promotion_or_purge_gate_hash"] = hash_package(
            {k: v for k, v in forged_gate.items() if k != "promotion_or_purge_gate_hash"}
        )
        with self.assertRaisesRegex(SpeculativeQuarantineValidationError, "outcome|promotion_gate"):
            validate_promotion_or_purge_gate_289(forged_gate, contract, quarantine, interaction)

        forged_quarantine = copy.deepcopy(quarantine)
        forged_quarantine["status"] = "NOT_QUARANTINE_EVIDENCE"
        forged_quarantine["run_id"] = "/tmp/not-an-id"
        forged_quarantine["quarantine_evidence_hash"] = hash_package(
            {k: v for k, v in forged_quarantine.items() if k != "quarantine_evidence_hash"}
        )
        with self.assertRaisesRegex(SpeculativeQuarantineValidationError, "quarantine evidence"):
            build_promotion_or_purge_gate_289(
                contract,
                forged_quarantine,
                interaction,
                decision="APPROVE",
                decided_at="2026-05-20T21:50:00+10:00",
                target_hash_at_decision=quarantine["target_hash_before_quarantine"],
                selected_result_hash=quarantine["result_hash"],
            )

    def test_288_requires_actual_preapproval_timing_for_speculative_compute_claim(self):
        identity, relay, loop_evidence = build_upstream_packages()
        contract = build_approval_timing_contract_286(identity, relay, loop_evidence)
        interaction = build_hitl_interaction_evidence_287(
            contract,
            identity,
            relay,
            approval_request_hash="sha256:" + "b" * 64,
            request_id="REQUEST-BLK-SYSTEM-288-HITL-TIMING",
            discord_user_id="684235178083745819",
            discord_message_id="1488733359072084070",
            discord_interaction_id="1488733359072084071",
            component_custom_id="BLK-HITL-APPROVE-288",
            decision="APPROVE",
            decided_at="2026-05-20T21:30:00+10:00",
            expires_at="2026-05-20T22:00:00+10:00",
        )

        with self.assertRaisesRegex(SpeculativeQuarantineValidationError, "pre-approval"):
            build_speculative_quarantine_evidence_288(
                contract,
                interaction,
                run_id="RUN-BLK-SYSTEM-288-QUARANTINE-TIMING",
                execution_timing_mode="speculative_quarantine",
                state="QUARANTINE_COMPLETE_AWAITING_DECISION",
                target_hash_before_quarantine="sha256:" + "c" * 64,
                manifest_hash="sha256:" + "d" * 64,
                result_hash="sha256:" + "e" * 64,
                report_hash="sha256:" + "f" * 64,
                quarantine_workspace_id="QUARANTINE-BLK-SYSTEM-288-TIMING",
                started_at="2026-05-20T21:31:00+10:00",
                completed_at="2026-05-20T21:45:00+10:00",
            )

        with self.assertRaisesRegex(SpeculativeQuarantineValidationError, "completed quarantine evidence"):
            build_speculative_quarantine_evidence_288(
                contract,
                interaction,
                run_id="RUN-BLK-SYSTEM-288-QUARANTINE-RUNNING",
                execution_timing_mode="speculative_quarantine",
                state="QUARANTINE_RUNNING",
                target_hash_before_quarantine="sha256:" + "5" * 64,
                manifest_hash="sha256:" + "6" * 64,
                result_hash="sha256:" + "7" * 64,
                report_hash="sha256:" + "8" * 64,
                quarantine_workspace_id="QUARANTINE-BLK-SYSTEM-288-RUNNING",
                started_at="2026-05-20T21:20:00+10:00",
                completed_at="2026-05-20T21:45:00+10:00",
            )

        with self.assertRaisesRegex(SpeculativeQuarantineValidationError, "pre-approval blocked"):
            build_speculative_quarantine_evidence_288(
                contract,
                interaction,
                run_id="RUN-BLK-SYSTEM-288-QUARANTINE-BLOCKED-TIMING",
                execution_timing_mode="pre_approval_blocked",
                state="QUARANTINE_COMPLETE_AWAITING_DECISION",
                target_hash_before_quarantine="sha256:" + "1" * 64,
                manifest_hash="sha256:" + "2" * 64,
                result_hash="sha256:" + "3" * 64,
                report_hash="sha256:" + "4" * 64,
                quarantine_workspace_id="QUARANTINE-BLK-SYSTEM-288-BLOCKED-TIMING",
                started_at="2026-05-20T21:20:00+10:00",
                completed_at="2026-05-20T21:45:00+10:00",
            )

    def test_289_config_policy_bypass_requires_typed_policy_evidence(self):
        identity, relay, loop_evidence = build_upstream_packages()
        contract = build_approval_timing_contract_286(identity, relay, loop_evidence)
        interaction = build_hitl_interaction_evidence_287(
            contract,
            identity,
            relay,
            approval_request_hash="sha256:" + "1" * 64,
            request_id="REQUEST-BLK-SYSTEM-289-HITL-POLICY",
            discord_user_id="684235178083745819",
            discord_message_id="1488733359072084070",
            discord_interaction_id="1488733359072084071",
            component_custom_id="BLK-HITL-APPROVE-289",
            decision="APPROVE",
            decided_at="2026-05-20T21:30:00+10:00",
            expires_at="2026-05-20T22:00:00+10:00",
        )
        quarantine = build_speculative_quarantine_evidence_288(
            contract,
            interaction,
            run_id="RUN-BLK-SYSTEM-289-QUARANTINE-POLICY",
            execution_timing_mode="speculative_quarantine",
            state="QUARANTINE_COMPLETE_AWAITING_DECISION",
            target_hash_before_quarantine="sha256:" + "2" * 64,
            manifest_hash="sha256:" + "3" * 64,
            result_hash="sha256:" + "4" * 64,
            report_hash="sha256:" + "5" * 64,
            quarantine_workspace_id="QUARANTINE-BLK-SYSTEM-289-POLICY",
            started_at="2026-05-20T21:20:00+10:00",
            completed_at="2026-05-20T21:45:00+10:00",
        )

        with self.assertRaisesRegex(SpeculativeQuarantineValidationError, "policy"):
            build_promotion_or_purge_gate_289(
                contract,
                quarantine,
                interaction,
                decision="CONFIG_POLICY_BYPASS",
                decided_at="2026-05-20T21:50:00+10:00",
                target_hash_at_decision=quarantine["target_hash_before_quarantine"],
                selected_result_hash=quarantine["result_hash"],
                policy_hash="sha256:" + "6" * 64,
            )

        deny_interaction = build_hitl_interaction_evidence_287(
            contract,
            identity,
            relay,
            approval_request_hash="sha256:" + "7" * 64,
            request_id="REQUEST-BLK-SYSTEM-289-HITL-POLICY-DENY",
            discord_user_id="684235178083745819",
            discord_message_id="1488733359072084070",
            discord_interaction_id="1488733359072084071",
            component_custom_id="BLK-HITL-DENY-289",
            decision="DENY",
            decided_at="2026-05-20T21:30:00+10:00",
            expires_at="2026-05-20T22:00:00+10:00",
        )
        deny_quarantine = build_speculative_quarantine_evidence_288(
            contract,
            deny_interaction,
            run_id="RUN-BLK-SYSTEM-289-QUARANTINE-POLICY-DENY",
            execution_timing_mode="speculative_quarantine",
            state="QUARANTINE_COMPLETE_AWAITING_DECISION",
            target_hash_before_quarantine="sha256:" + "8" * 64,
            manifest_hash="sha256:" + "9" * 64,
            result_hash="sha256:" + "a" * 64,
            report_hash="sha256:" + "b" * 64,
            quarantine_workspace_id="QUARANTINE-BLK-SYSTEM-289-POLICY-DENY",
            started_at="2026-05-20T21:20:00+10:00",
            completed_at="2026-05-20T21:45:00+10:00",
        )
        with self.assertRaisesRegex(SpeculativeQuarantineValidationError, "policy bypass cannot override"):
            build_promotion_or_purge_gate_289(
                contract,
                deny_quarantine,
                deny_interaction,
                decision="CONFIG_POLICY_BYPASS",
                decided_at="2026-05-20T21:50:00+10:00",
                target_hash_at_decision=deny_quarantine["target_hash_before_quarantine"],
                selected_result_hash=deny_quarantine["result_hash"],
                policy_hash="sha256:" + "c" * 64,
                policy_source_id="POLICY-BLK-SYSTEM-289-BYPASS",
                policy_operation_class="doc_only",
                policy_scope_hash="sha256:" + "d" * 64,
            )

    def test_blk123_contract_doc_makes_quarantine_authority_boundary_review_obvious(self):
        self.assertTrue(BLK123.exists(), "BLK-123 durable approval contract doc is missing")
        text = BLK123.read_text()

        for marker in [
            "BLK-123 — Speculative Quarantine Approval Contract",
            "pre-approval execution may compute only in a disposable quarantine",
            "durable promotion",
            "Discord button/selector",
            "long exact-text copy-paste",
            "config_policy_bypass",
            "APPROVED_PROMOTED",
            "DRY_RUN_ONLY_PURGED",
            "REJECTED_PURGED",
            "STALE_TARGET_HASH_BLOCKED",
            "blk286_approval_timing_contract_hash=sha256:24f0cf02e473374a6af4360189bd8271acebf906a263baea541cd6db2d004d0c",
            "blk289_promotion_purge_gate_hash=sha256:eb8001a1fd0de19f96dc1dec8cba33586f7404397396db0bb8ff026b7892abef",
        ]:
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
