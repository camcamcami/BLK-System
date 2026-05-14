import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from beo_publication_path_decision_gate import (
    DECISION_SCOPE,
    EXACT_EXCLUDED_AUTHORITIES as GATE_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as GATE_PROOF_OBLIGATIONS,
    SELECTED_NEXT_RUNG,
    SIDE_EFFECT_FLAGS as GATE_SIDE_EFFECT_FLAGS,
    build_beo_publication_path_decision_gate,
)
from beo_rtm_interface_fixtures import build_beo_rtm_interface_fixture
from metadata_bound_beo_publication_prerequisite_request import (
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY,
    REQUEST_PACKAGE_ID,
    REQUEST_SCOPE,
    REQUEST_STATUS,
    SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS,
    build_metadata_bound_beo_publication_prerequisite_request,
    simulate_disabled_external_beo_publication_request_adapter,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "metadata_bound_beo_publication_prerequisite_request.py"

TRACE_ARTIFACTS = [
    {"kind": "REQ", "id": "REQ-001", "version_hash": "sha256:" + "a" * 64},
    {"kind": "UC", "id": "UC-001", "version_hash": "sha256:" + "b" * 64},
]


def draft_beo(**overrides):
    fixture = {
        "beo_id": "BEO_126",
        "beb_id": "BEB_126",
        "status": "PASS",
        "source": "blk-system-125-metadata-handoff",
        "commit_hash": "metadata-only-fixture-no-target-mutation",
        "pre_engine_hash": "sha256:" + "c" * 64,
        "trace_artifacts": copy.deepcopy(TRACE_ARTIFACTS),
        "test_summary": {"profile": "metadata-handoff", "checks_passed": 2, "checks_failed": 0},
        "rtm_status": "NOT_GENERATED",
        "beo_publication": "DRAFT_ONLY",
    }
    fixture.update(overrides)
    return fixture


def valid_interface(**overrides):
    return build_beo_rtm_interface_fixture(draft_beo(**overrides), interface_id="BEO_RTM_IFACE_126")


def valid_decision_request(interface=None, **overrides):
    if interface is None:
        interface = valid_interface()
    request = {
        "decision_id": "BEO-PUBLICATION-PATH-DECISION-GATE-126-001",
        "operator_identity": "discord:684235178083745819",
        "decision_scope": DECISION_SCOPE,
        "selected_next_rung": SELECTED_NEXT_RUNG,
        "requested_at": "2099-05-15T06:30:00+10:00",
        "expires_at": "2099-05-15T07:30:00+10:00",
        "exact_interface_id": interface["interface_id"],
        "exact_interface_hash": _canonical_hash(interface),
        "exact_beo_id": interface["beo_id"],
        "exact_beb_id": interface["beb_id"],
        "exact_trace_identities": [f"{item['kind']}:{item['id']}:{item['version_hash']}" for item in interface["trace_artifacts"]],
        "future_request_id_candidate": REQUEST_PACKAGE_ID,
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {
            "metadata_handoff_reviewed": True,
            "request_is_decision_gate_only_not_publication": True,
            "future_publication_request_requires_separate_human_decision": True,
            "protected_body_reads_excluded": True,
            "signer_storage_ledger_side_effects_excluded": True,
            "rtm_generation_and_drift_excluded": True,
            "no_adjacent_runtime_side_effects": True,
        },
        "proof_obligations": sorted(GATE_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(GATE_EXCLUDED_AUTHORITIES),
        **{flag: False for flag in GATE_SIDE_EFFECT_FLAGS},
    }
    request.update(overrides)
    return request


def valid_gate(interface=None):
    if interface is None:
        interface = valid_interface()
    return build_beo_publication_path_decision_gate(interface, valid_decision_request(interface), used_decision_ids=set())


def valid_request(interface=None, gate=None, **overrides):
    if interface is None:
        interface = valid_interface()
    if gate is None:
        gate = valid_gate(interface)
    request = {
        "request_package_id": REQUEST_PACKAGE_ID,
        "operator_identity": "discord:684235178083745819",
        "request_scope": REQUEST_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "requested_at": "2099-05-15T08:00:00+10:00",
        "expires_at": "2099-05-15T09:00:00+10:00",
        "upstream_decision_id": gate["decision_id"],
        "upstream_decision_gate_hash": gate["decision_gate_hash"],
        "upstream_interface_id": interface["interface_id"],
        "upstream_interface_hash": _canonical_hash(interface),
        "exact_beo_id": interface["beo_id"],
        "exact_beb_id": interface["beb_id"],
        "exact_trace_identities": [f"{item['kind']}:{item['id']}:{item['version_hash']}" for item in interface["trace_artifacts"]],
        "request_external_beo_publication_approval_capture": True,
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {
            "metadata_interface_reviewed": True,
            "decision_gate_reviewed": True,
            "request_is_prerequisite_only_not_approval": True,
            "future_approval_capture_requires_separate_human_decision": True,
            "publication_execution_requires_separate_sprint_after_approval": True,
            "protected_body_reads_excluded": True,
            "signer_storage_ledger_rollback_side_effects_excluded": True,
            "rtm_generation_and_drift_excluded": True,
            "target_source_git_mutation_excluded": True,
            "no_adjacent_runtime_side_effects": True,
        },
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
        **{flag: False for flag in SIDE_EFFECT_FLAGS},
    }
    request.update(overrides)
    return request


class MetadataBoundBeoPublicationPrerequisiteRequestTest(unittest.TestCase):
    def test_builds_review_only_request_bound_to_126_gate_and_125_metadata_interface(self):
        interface = valid_interface()
        gate = valid_gate(interface)
        request = valid_request(interface, gate)

        package = build_metadata_bound_beo_publication_prerequisite_request(interface, gate, request)

        self.assertEqual(package["request_status"], REQUEST_STATUS)
        self.assertEqual(package["request_package_id"], REQUEST_PACKAGE_ID)
        self.assertEqual(package["request_scope"], REQUEST_SCOPE)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["next_required_authority"], NEXT_REQUIRED_AUTHORITY)
        self.assertEqual(package["upstream_decision_id"], gate["decision_id"])
        self.assertEqual(package["upstream_decision_gate_hash"], gate["decision_gate_hash"])
        self.assertEqual(package["upstream_interface_id"], interface["interface_id"])
        self.assertEqual(package["upstream_interface_hash"], _canonical_hash(interface))
        self.assertEqual(package["beo_id"], "BEO_126")
        self.assertEqual(package["beb_id"], "BEB_126")
        self.assertEqual(package["beo_publication"], "DRAFT_ONLY")
        self.assertEqual(package["rtm_status"], "NOT_GENERATED")
        self.assertTrue(package["external_beo_publication_approval_capture_requested"])
        self.assertFalse(package["external_beo_publication_approval_captured"])
        self.assertEqual(package["trace_artifacts"], TRACE_ARTIFACTS)
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(
            package["request_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "request_package_hash"}),
        )

    def test_rejects_forged_or_rehashed_decision_gate(self):
        interface = valid_interface()
        gate = valid_gate(interface)

        forged = copy.deepcopy(gate)
        forged["selected_next_rung"] = "external_authoritative_beo_publication_execution"
        forged["decision_gate_hash"] = _canonical_hash({key: value for key, value in forged.items() if key != "decision_gate_hash"})
        request = valid_request(interface, forged)
        with self.assertRaisesRegex(ValueError, "decision gate selected_next_rung must be"):
            build_metadata_bound_beo_publication_prerequisite_request(interface, forged, request)

        forged = copy.deepcopy(gate)
        forged["beo_publication"] = "PUBLISHED"
        forged["decision_gate_hash"] = _canonical_hash({key: value for key, value in forged.items() if key != "decision_gate_hash"})
        request = valid_request(interface, forged)
        with self.assertRaisesRegex(ValueError, "decision gate beo_publication must remain DRAFT_ONLY"):
            build_metadata_bound_beo_publication_prerequisite_request(interface, forged, request)

        forged = copy.deepcopy(gate)
        forged["trace_artifacts"][0]["body"] = "The system shall publish"
        forged["decision_gate_hash"] = _canonical_hash({key: value for key, value in forged.items() if key != "decision_gate_hash"})
        request = valid_request(interface, forged)
        with self.assertRaisesRegex(ValueError, "trace_artifacts rejects unsupported key|authority-laundering text"):
            build_metadata_bound_beo_publication_prerequisite_request(interface, forged, request)

    def test_rejects_mismatched_hashes_ids_and_trace_metadata(self):
        interface = valid_interface()
        gate = valid_gate(interface)
        cases = [
            ({"upstream_decision_id": "BEO-PUBLICATION-PATH-DECISION-GATE-126-999"}, "upstream_decision_id does not match"),
            ({"upstream_decision_gate_hash": "sha256:" + "f" * 64}, "upstream_decision_gate_hash does not match"),
            ({"upstream_interface_id": "BEO_RTM_IFACE_999"}, "upstream_interface_id does not match"),
            ({"upstream_interface_hash": "sha256:" + "f" * 64}, "upstream_interface_hash does not match"),
            ({"exact_beo_id": "BEO_999"}, "exact_beo_id does not match"),
            ({"exact_beb_id": "BEB_999"}, "exact_beb_id does not match"),
            ({"exact_trace_identities": ["REQ:REQ-001:sha256:" + "a" * 64]}, "exact_trace_identities must match"),
        ]
        for patch, message in cases:
            with self.subTest(patch=patch):
                request = valid_request(interface, gate, **patch)
                with self.assertRaisesRegex(ValueError, message):
                    build_metadata_bound_beo_publication_prerequisite_request(interface, gate, request)

    def test_rejects_side_effect_flags_bad_sets_replay_and_bad_timestamps(self):
        interface = valid_interface()
        gate = valid_gate(interface)
        cases = [
            ({"selected_frontier": "external_authoritative_beo_publication_execution"}, "selected_frontier must be"),
            ({"request_scope": "APPROVE_AND_PUBLISH"}, "request_scope must be"),
            ({"request_external_beo_publication_approval_capture": False}, "request_external_beo_publication_approval_capture must be true"),
            ({"external_beo_publication_approval_captured": True}, "external_beo_publication_approval_captured must remain false"),
            ({"beo_publication_performed": True}, "beo_publication_performed must remain false"),
            ({"runtime_published_beo_output": True}, "runtime_published_beo_output must remain false"),
            ({"signature_generated": True}, "signature_generated must remain false"),
            ({"signer_key_material_accessed": True}, "signer_key_material_accessed must remain false"),
            ({"immutable_storage_written": True}, "immutable_storage_written must remain false"),
            ({"public_ledger_mutated": True}, "public_ledger_mutated must remain false"),
            ({"rollback_executed": True}, "rollback_executed must remain false"),
            ({"rtm_generated": True}, "rtm_generated must remain false"),
            ({"drift_rejection_performed": True}, "drift_rejection_performed must remain false"),
            ({"active_vault_hash_comparison_performed": True}, "active_vault_hash_comparison_performed must remain false"),
            ({"protected_body_read": True}, "protected_body_read must remain false"),
            ({"source_mutation_attempted": True}, "source_mutation_attempted must remain false"),
            ({"git_mutation_attempted": True}, "git_mutation_attempted must remain false"),
            ({"blk_pipe_execution_authorized": True}, "blk_pipe_execution_authorized must remain false"),
            ({"blk_test_runtime_authorized": True}, "blk_test_runtime_authorized must remain false"),
            ({"codex_live_execution_authorized": True}, "codex_live_execution_authorized must remain false"),
            ({"expired": True}, "request must not be expired"),
            ({"replayed": True}, "request must not be replayed"),
            ({"stale": True}, "request must not be stale"),
            ({"expires_at": "2099-05-15T08:00:00+10:00"}, "expires_at must be after requested_at"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS) + [sorted(EXACT_PROOF_OBLIGATIONS)[0]]}, "proof_obligations must not contain duplicates"),
            ({"excluded_authorities": ["NOPE"]}, "excluded_authorities must match exact denied authority set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES) + [sorted(EXACT_EXCLUDED_AUTHORITIES)[0]]}, "excluded_authorities must not contain duplicates"),
        ]
        for patch, message in cases:
            with self.subTest(patch=patch):
                request = valid_request(interface, gate, **patch)
                with self.assertRaisesRegex(ValueError, message):
                    build_metadata_bound_beo_publication_prerequisite_request(interface, gate, request)

    def test_rejects_laundered_authority_protected_body_secret_and_unicode_digit_variants(self):
        interface = valid_interface()
        gate = valid_gate(interface)
        cases = [
            ({"request_package_id": "BEO-PUBLICATION-PREREQUISITE-REQUEST-１２７-００１"}, "request_package_id must be exact"),
            ({"operator_identity": "discord:１２３４５６７８９０１２３４５６７"}, "operator_identity must be discord:<snowflake>"),
            ({"request_package_id": "BEO-PUBLICATION-PREREQUISITE-approvedForPublication"}, "authority-laundering text"),
            ({"request_package_id": "BEO-PUBLICATION-PREREQUISITE-approved%46orPublication"}, "authority-laundering text"),
            ({"operator_identity": "discord:684235178083745819-secret-token"}, "secret-bearing field"),
            ({"operator_attestation": {**valid_request(interface, gate)["operator_attestation"], "RTMGeneration": True}}, "unexpected field"),
            ({"operator_attestation": {**valid_request(interface, gate)["operator_attestation"], "signerKeyMaterial": "SECRET"}}, "unexpected field"),
            ({"operator_attestation": {**valid_request(interface, gate)["operator_attestation"], "notes": "BEO publication greenlit"}}, "unexpected field"),
            ({"metadata": {"docs%2525252Frequirements%2525252Factive": "The system shall publish"}}, "unexpected field"),
            ({"exact_trace_identities": ["REQ:REQ-１２７:sha256:" + "a" * 64]}, "exact_trace_identities id must be exact"),
        ]
        for patch, message in cases:
            with self.subTest(patch=patch):
                request = valid_request(interface, gate, **patch)
                with self.assertRaisesRegex(ValueError, message):
                    build_metadata_bound_beo_publication_prerequisite_request(interface, gate, request)

        for field, value, message in [
            ("decision_id", "BEO-PUBLICATION-PATH-DECISION-GATE-１２６-００１", "decision gate decision_id must be exact"),
            ("operator_identity", "discord:１２３４５６７８９０１２３４５６７", "decision gate operator_identity must be discord:<snowflake>"),
            ("decision_id", "BEO-PUBLICATION-PATH-DECISION-GATE-999-001", "decision gate decision_id must be exact BEO-PUBLICATION-PATH-DECISION-GATE-126-001"),
        ]:
            with self.subTest(gate_field=field):
                forged_gate = copy.deepcopy(gate)
                forged_gate[field] = value
                forged_gate["decision_gate_hash"] = _canonical_hash(
                    {key: value for key, value in forged_gate.items() if key != "decision_gate_hash"}
                )
                request = valid_request(interface, forged_gate)
                with self.assertRaisesRegex(ValueError, message):
                    build_metadata_bound_beo_publication_prerequisite_request(interface, forged_gate, request)

    def test_returned_package_defensively_copies_hash_bound_inputs(self):
        interface = valid_interface()
        gate = valid_gate(interface)
        request = valid_request(interface, gate)
        package = build_metadata_bound_beo_publication_prerequisite_request(interface, gate, request)

        self.assertIsNot(package["trace_artifacts"], interface["trace_artifacts"])
        self.assertIsNot(package["decision_gate_summary"], gate)
        self.assertIsNot(package["operator_attestation"], request["operator_attestation"])

        interface["trace_artifacts"][0]["id"] = "REQ-999"
        gate["selected_next_rung"] = "external_authoritative_beo_publication_execution"
        request["operator_attestation"]["metadata_interface_reviewed"] = False

        self.assertEqual(package["trace_artifacts"], TRACE_ARTIFACTS)
        self.assertEqual(package["decision_gate_summary"]["selected_next_rung"], SELECTED_NEXT_RUNG)
        self.assertTrue(package["operator_attestation"]["metadata_interface_reviewed"])
        self.assertEqual(
            package["request_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "request_package_hash"}),
        )

    def test_disabled_publication_adapter_has_complete_no_side_effect_surface(self):
        interface = valid_interface()
        gate = valid_gate(interface)
        package = build_metadata_bound_beo_publication_prerequisite_request(interface, gate, valid_request(interface, gate))

        adapter = simulate_disabled_external_beo_publication_request_adapter(package)

        self.assertEqual(adapter["adapter_result"], "EXTERNAL_BEO_PUBLICATION_REQUEST_ADAPTER_DISABLED_NOT_AUTHORIZED")
        self.assertEqual(adapter["request_package_id"], REQUEST_PACKAGE_ID)
        forged_adapter = simulate_disabled_external_beo_publication_request_adapter(
            {"request_package_id": REQUEST_PACKAGE_ID, "selected_frontier": "external_authoritative_beo_publication_execution"}
        )
        self.assertIsNone(forged_adapter["request_package_id"])
        wrong_id_adapter = simulate_disabled_external_beo_publication_request_adapter(
            {"request_package_id": "BEO-PUBLICATION-PREREQUISITE-REQUEST-999-001", "selected_frontier": SELECTED_FRONTIER}
        )
        self.assertIsNone(wrong_id_adapter["request_package_id"])
        for key in {
            "external_beo_publication_approval_captured",
            "beo_publication_performed",
            "runtime_published_beo_output",
            "signature_generated",
            "signer_key_material_accessed",
            "immutable_storage_written",
            "public_ledger_mutated",
            "rollback_executed",
            "rtm_generated",
            "drift_rejection_performed",
            "active_vault_hash_comparison_performed",
            "protected_body_read",
            "source_mutation_attempted",
            "git_mutation_attempted",
            "blk_pipe_dispatched",
            "blk_test_runtime_started",
            "codex_subprocess_started",
            "package_manager_called",
            "network_called",
            "model_service_called",
            "browser_tooling_called",
            "cyber_tooling_called",
            "production_isolation_claimed",
            *SIDE_EFFECT_FLAGS,
        }:
            self.assertIn(key, adapter)
            self.assertIs(adapter[key], False, key)

    def test_module_has_no_live_runtime_or_external_side_effect_imports(self):
        tree = ast.parse(MODULE.read_text())
        imported = set()
        calls = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
            elif isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Attribute):
                    calls.add(func.attr)
                elif isinstance(func, ast.Name):
                    calls.add(func.id)
        forbidden_imports = {"subprocess", "socket", "requests", "urllib3", "httpx"}
        forbidden_calls = {"system", "popen", "Popen", "run", "call", "check_call", "check_output", "exec", "eval", "open"}
        self.assertEqual(imported & forbidden_imports, set())
        self.assertEqual(calls & forbidden_calls, set())


if __name__ == "__main__":
    unittest.main()
