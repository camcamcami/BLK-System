import copy
import unittest

import blk_root_doctrine_gap_ladder_237_241 as root_ladder
from blk_req_production_gateway_195_199 import (
    build_blk_req_gateway_readiness_review_195,
    build_blk_req_production_gateway_contract_196,
)

from blk_identity_relay_spine_283_285 import (
    IdentityRelayValidationError,
    build_blk_id_identity_spine_contract_283,
    build_identity_record_283,
    validate_identity_record_283,
    build_blk_relay_envelope_contract_284,
    build_relay_envelope_284,
    validate_relay_envelope_284,
    build_identity_relay_loop_evidence_285,
    validate_identity_relay_loop_evidence_285,
    hash_package,
)


def build_loop_kernel_241():
    selected = root_ladder.build_kuronode_route_selection_237()
    overlay = root_ladder.build_root_doctrine_deviation_overlay_238(selected)
    scope = root_ladder.decide_blk_id_relay_scope_239(overlay)
    gateway_contract = build_blk_req_production_gateway_contract_196(
        build_blk_req_gateway_readiness_review_195()
    )
    gateway = root_ladder.build_hitl_gateway_completion_slice_240(scope, gateway_contract)
    return root_ladder.build_reusable_blk003_loop_kernel_241(gateway)


class BlkIdentityRelaySpine283To285Test(unittest.TestCase):
    def test_283_identity_spine_contract_and_records_are_hash_bound_without_authority(self):
        contract = build_blk_id_identity_spine_contract_283()

        self.assertEqual(contract["status"], "BLK_IDENTITY_SPINE_CONTRACT_READY")
        self.assertIn("BLK_SYSTEM_283_BLK_IDENTITY_SPINE_CONTRACT_READY", contract["markers"])
        self.assertIn("actor", contract["record_kinds"])
        self.assertIn("approval", contract["record_kinds"])
        self.assertFalse(contract["side_effects"]["approval_authority_granted"])
        self.assertFalse(contract["side_effects"]["network_runtime_created"])
        self.assertRegex(contract["identity_contract_hash"], r"^sha256:[0-9a-f]{64}$")

        record = build_identity_record_283(
            contract,
            record_kind="actor",
            record_id="ACTOR-DISCORD-684235178083745819",
            source_system_id="SOURCE-DISCORD",
            subject_hash="sha256:" + "a" * 64,
            created_at="2026-05-20T20:00:00Z",
            metadata={"display_name": "operator", "external_ref": "discord-user-684235178083745819"},
        )

        self.assertEqual(record["record_kind"], "actor")
        self.assertEqual(record["record_id"], "ACTOR-DISCORD-684235178083745819")
        self.assertEqual(record["contract_hash"], contract["identity_contract_hash"])
        self.assertFalse(record["side_effects"]["approval_authority_granted"])
        self.assertFalse(record["side_effects"]["source_git_mutation"])
        self.assertRegex(record["identity_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(validate_identity_record_283(record, contract), record)

    def test_283_rejects_unicode_ids_authority_laundering_and_rehashed_extra_fields(self):
        contract = build_blk_id_identity_spine_contract_283()

        with self.assertRaisesRegex(IdentityRelayValidationError, "ASCII|record_id"):
            build_identity_record_283(
                contract,
                record_kind="run",
                record_id="RUN-BLK-SYSTEM-２８３-001",
                source_system_id="SOURCE-DISCORD",
                subject_hash="sha256:" + "b" * 64,
                created_at="2026-05-20T20:00:00Z",
            )

        with self.assertRaisesRegex(IdentityRelayValidationError, "forbidden authority wording|metadata"):
            build_identity_record_283(
                contract,
                record_kind="approval",
                record_id="APPROVAL-BLK-SYSTEM-283-001",
                source_system_id="SOURCE-DISCORD",
                subject_hash="sha256:" + "c" * 64,
                created_at="2026-05-20T20:00:00Z",
                metadata={"summary": "runtime execution authorized"},
            )

        record = build_identity_record_283(
            contract,
            record_kind="artifact",
            record_id="ARTIFACT-BEB-283",
            source_system_id="SOURCE-LOCAL",
            subject_hash="sha256:" + "d" * 64,
            created_at="2026-05-20T20:00:00Z",
        )
        tampered = copy.deepcopy(record)
        tampered["runtime_authority_granted"] = True
        tampered["identity_hash"] = hash_package({k: v for k, v in tampered.items() if k != "identity_hash"})
        with self.assertRaisesRegex(IdentityRelayValidationError, "identity record|unsupported field|runtime_authority_granted"):
            validate_identity_record_283(tampered, contract)

    def test_284_relay_envelope_consumes_identity_records_without_granting_dispatch(self):
        identity_contract = build_blk_id_identity_spine_contract_283()
        source = build_identity_record_283(
            identity_contract,
            record_kind="actor",
            record_id="ACTOR-DISCORD-684235178083745819",
            source_system_id="SOURCE-DISCORD",
            subject_hash="sha256:" + "e" * 64,
            created_at="2026-05-20T20:00:00Z",
        )
        relay_contract = build_blk_relay_envelope_contract_284(identity_contract)

        self.assertEqual(relay_contract["status"], "BLK_RELAY_ENVELOPE_CONTRACT_READY")
        self.assertIn("BLK_SYSTEM_284_BLK_RELAY_ENVELOPE_CONTRACT_READY", relay_contract["markers"])
        self.assertEqual(relay_contract["identity_contract_hash"], identity_contract["identity_contract_hash"])
        self.assertFalse(relay_contract["side_effects"]["network_runtime_created"])
        self.assertFalse(relay_contract["side_effects"]["message_dispatch_authorized"])

        envelope = build_relay_envelope_284(
            relay_contract,
            source_identity_record=source,
            envelope_id="RELAY-BLK-SYSTEM-284-001",
            message_type="HITL_APPROVAL_SIGNAL",
            target_component="blk-req",
            payload_hash="sha256:" + "f" * 64,
            created_at="2026-05-20T20:01:00Z",
            trace_identity_hashes=[source["identity_hash"]],
            metadata={"summary": "typed signal evidence only"},
        )

        self.assertEqual(envelope["source_identity_hash"], source["identity_hash"])
        self.assertFalse(envelope["side_effects"]["message_dispatch_authorized"])
        self.assertFalse(envelope["side_effects"]["runtime_tooling"])
        self.assertRegex(envelope["relay_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(validate_relay_envelope_284(envelope, relay_contract, source), envelope)

    def test_284_rejects_forged_identity_hash_transport_authority_and_extra_fields(self):
        identity_contract = build_blk_id_identity_spine_contract_283()
        source = build_identity_record_283(
            identity_contract,
            record_kind="actor",
            record_id="ACTOR-DISCORD-684235178083745819",
            source_system_id="SOURCE-DISCORD",
            subject_hash="sha256:" + "1" * 64,
            created_at="2026-05-20T20:00:00Z",
        )
        relay_contract = build_blk_relay_envelope_contract_284(identity_contract)

        forged_source = copy.deepcopy(source)
        forged_source["identity_hash"] = "sha256:" + "2" * 64
        with self.assertRaisesRegex(IdentityRelayValidationError, "identity record|hash mismatch"):
            build_relay_envelope_284(
                relay_contract,
                source_identity_record=forged_source,
                envelope_id="RELAY-BLK-SYSTEM-284-002",
                message_type="STATUS_SIGNAL",
                target_component="blk-pipe",
                payload_hash="sha256:" + "3" * 64,
                created_at="2026-05-20T20:01:00Z",
            )

        with self.assertRaisesRegex(IdentityRelayValidationError, "forbidden authority wording|metadata"):
            build_relay_envelope_284(
                relay_contract,
                source_identity_record=source,
                envelope_id="RELAY-BLK-SYSTEM-284-003",
                message_type="STATUS_SIGNAL",
                target_component="blk-pipe",
                payload_hash="sha256:" + "4" * 64,
                created_at="2026-05-20T20:01:00Z",
                metadata={"summary": "mcp transport enabled"},
            )

        envelope = build_relay_envelope_284(
            relay_contract,
            source_identity_record=source,
            envelope_id="RELAY-BLK-SYSTEM-284-004",
            message_type="STATUS_SIGNAL",
            target_component="blk-pipe",
            payload_hash="sha256:" + "5" * 64,
            created_at="2026-05-20T20:01:00Z",
        )
        tampered = copy.deepcopy(envelope)
        tampered["target_source_git_mutation"] = True
        tampered["relay_hash"] = hash_package({k: v for k, v in tampered.items() if k != "relay_hash"})
        with self.assertRaisesRegex(IdentityRelayValidationError, "relay envelope|unsupported field|target_source_git_mutation"):
            validate_relay_envelope_284(tampered, relay_contract, source)

    def test_285_binds_identity_and_relay_to_blk003_loop_evidence_without_runtime(self):
        identity_contract = build_blk_id_identity_spine_contract_283()
        relay_contract = build_blk_relay_envelope_contract_284(identity_contract)
        loop = build_loop_kernel_241()

        evidence = build_identity_relay_loop_evidence_285(identity_contract, relay_contract, loop)

        self.assertEqual(evidence["status"], "IDENTITY_RELAY_LOOP_EVIDENCE_READY")
        self.assertIn("BLK_SYSTEM_285_IDENTITY_RELAY_LOOP_EVIDENCE_READY", evidence["markers"])
        self.assertEqual(evidence["identity_contract_hash"], identity_contract["identity_contract_hash"])
        self.assertEqual(evidence["relay_contract_hash"], relay_contract["relay_contract_hash"])
        self.assertEqual(evidence["loop_kernel_hash"], loop["loop_kernel_hash"])
        self.assertTrue(evidence["loop_binding"]["per_iteration_identity_required"])
        self.assertTrue(evidence["loop_binding"]["relay_envelope_required_per_signal"])
        self.assertFalse(evidence["side_effects"]["loop_runtime_execution"])
        self.assertFalse(evidence["side_effects"]["approval_authority_granted"])
        self.assertFalse(evidence["side_effects"]["network_runtime_created"])
        self.assertRegex(evidence["loop_evidence_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(validate_identity_relay_loop_evidence_285(evidence, identity_contract, relay_contract, loop), evidence)

    def test_285_rejects_rehashed_upstream_contracts_and_loop_authority_laundering(self):
        identity_contract = build_blk_id_identity_spine_contract_283()
        relay_contract = build_blk_relay_envelope_contract_284(identity_contract)
        loop = build_loop_kernel_241()

        tampered_identity = copy.deepcopy(identity_contract)
        tampered_identity["approval_authority_granted"] = True
        tampered_identity["identity_contract_hash"] = hash_package(
            {k: v for k, v in tampered_identity.items() if k != "identity_contract_hash"}
        )
        with self.assertRaisesRegex(IdentityRelayValidationError, "identity contract|unsupported field|approval_authority_granted"):
            build_identity_relay_loop_evidence_285(tampered_identity, relay_contract, loop)

        tampered_relay = copy.deepcopy(relay_contract)
        tampered_relay["side_effects"]["network_runtime_created"] = True
        tampered_relay["relay_contract_hash"] = hash_package(
            {k: v for k, v in tampered_relay.items() if k != "relay_contract_hash"}
        )
        with self.assertRaisesRegex(IdentityRelayValidationError, "relay contract|network_runtime_created"):
            build_identity_relay_loop_evidence_285(identity_contract, tampered_relay, loop)

        tampered_loop = copy.deepcopy(loop)
        tampered_loop["side_effects"]["loop_runtime_execution"] = True
        tampered_loop["loop_kernel_hash"] = root_ladder._hash_package(
            {k: v for k, v in tampered_loop.items() if k != "loop_kernel_hash"}
        )
        with self.assertRaisesRegex(IdentityRelayValidationError, "loop package|loop_runtime_execution"):
            build_identity_relay_loop_evidence_285(identity_contract, relay_contract, tampered_loop)


if __name__ == "__main__":
    unittest.main()
