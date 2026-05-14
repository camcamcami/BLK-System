import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from beo_rtm_interface_fixtures import build_beo_rtm_interface_fixture
from beo_publication_path_decision_gate import (
    DECISION_GATE_READY,
    DECISION_SCOPE,
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY,
    SELECTED_NEXT_RUNG,
    SIDE_EFFECT_FLAGS,
    build_beo_publication_path_decision_gate,
    simulate_disabled_beo_publication_path_activation_adapter,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "beo_publication_path_decision_gate.py"

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
    interface = build_beo_rtm_interface_fixture(draft_beo(**overrides), interface_id="BEO_RTM_IFACE_126")
    return interface


def valid_request(interface=None, **overrides):
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
        "future_request_id_candidate": "BEO-PUBLICATION-PREREQUISITE-REQUEST-127-001",
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
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
        **{flag: False for flag in SIDE_EFFECT_FLAGS},
    }
    request.update(overrides)
    return request


class BeoPublicationPathDecisionGateTest(unittest.TestCase):
    def test_builds_review_only_decision_gate_bound_to_metadata_handoff(self):
        interface = valid_interface()
        request = valid_request(interface)

        gate = build_beo_publication_path_decision_gate(interface, request, used_decision_ids=set())

        self.assertEqual(gate["decision_status"], DECISION_GATE_READY)
        self.assertEqual(gate["decision_scope"], DECISION_SCOPE)
        self.assertEqual(gate["selected_next_rung"], SELECTED_NEXT_RUNG)
        self.assertEqual(gate["next_required_authority"], NEXT_REQUIRED_AUTHORITY)
        self.assertEqual(gate["interface_id"], interface["interface_id"])
        self.assertEqual(gate["interface_hash"], _canonical_hash(interface))
        self.assertEqual(gate["beo_id"], "BEO_126")
        self.assertEqual(gate["beb_id"], "BEB_126")
        self.assertEqual(gate["beo_status"], "PASS")
        self.assertEqual(gate["beo_publication"], "DRAFT_ONLY")
        self.assertEqual(gate["rtm_status"], "NOT_GENERATED")
        self.assertEqual(gate["metadata_handoff_status"], "BLK_REQ_TRACE_METADATA_ONLY")
        self.assertEqual(gate["trace_artifacts"], TRACE_ARTIFACTS)
        self.assertTrue(gate["future_publication_prerequisite_request_required"])
        self.assertFalse(gate["future_publication_prerequisite_request_authorized"])
        self.assertEqual(set(gate["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(gate["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(gate[flag], False, flag)
        self.assertEqual(
            gate["decision_gate_hash"],
            _canonical_hash({key: value for key, value in gate.items() if key != "decision_gate_hash"}),
        )

    def test_rejects_forged_or_non_draft_metadata_interface_even_when_rehashed(self):
        interface = valid_interface()
        request = valid_request(interface, exact_interface_hash="sha256:" + "f" * 64)
        with self.assertRaisesRegex(ValueError, "exact_interface_hash does not match"):
            build_beo_publication_path_decision_gate(interface, request, used_decision_ids=set())

        forged = copy.deepcopy(interface)
        forged["beo_publication"] = "PUBLISHED"
        request = valid_request(forged)
        with self.assertRaisesRegex(ValueError, "beo_publication must remain DRAFT_ONLY"):
            build_beo_publication_path_decision_gate(forged, request, used_decision_ids=set())

        failed = valid_interface(status="FAIL")
        request = valid_request(failed)
        with self.assertRaisesRegex(ValueError, "beo_status must be PASS"):
            build_beo_publication_path_decision_gate(failed, request, used_decision_ids=set())

    def test_rejects_wrong_frontier_replay_positive_flags_and_bad_denied_sets(self):
        interface = valid_interface()
        cases = [
            ({"selected_next_rung": "external_authoritative_beo_publication_execution"}, "selected_next_rung must be"),
            ({"decision_scope": "APPROVE_AND_PUBLISH"}, "decision_scope must be"),
            ({"operator_identity": "not-a-discord-identity"}, "operator_identity must be discord:<snowflake>"),
            ({"future_request_id_candidate": "x"}, "future_request_id_candidate must be exact BEO-PUBLICATION-PREREQUISITE-REQUEST-###-###"),
            ({"future_publication_prerequisite_request_authorized": True}, "future_publication_prerequisite_request_authorized must remain false"),
            ({"beo_publication_authorized": True}, "beo_publication_authorized must remain false"),
            ({"rtm_generation_authorized": True}, "rtm_generation_authorized must remain false"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS) + [sorted(EXACT_PROOF_OBLIGATIONS)[0]]}, "proof_obligations must not contain duplicates"),
            ({"excluded_authorities": ["NOPE"]}, "excluded_authorities must match exact denied authority set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES) + [sorted(EXACT_EXCLUDED_AUTHORITIES)[0]]}, "excluded_authorities must not contain duplicates"),
        ]
        for patch, message in cases:
            with self.subTest(patch=patch):
                request = valid_request(interface, **patch)
                with self.assertRaisesRegex(ValueError, message):
                    build_beo_publication_path_decision_gate(interface, request, used_decision_ids=set())

        request = valid_request(interface)
        with self.assertRaisesRegex(ValueError, "decision replayed"):
            build_beo_publication_path_decision_gate(
                interface,
                request,
                used_decision_ids={"BEO-PUBLICATION-PATH-DECISION-GATE-126-001"},
            )

    def test_rejects_laundered_authority_protected_body_and_secret_variants(self):
        interface = valid_interface()
        hostile_cases = [
            ({"decision_id": "BEO-PUBLICATION-PATH-approvedForPublication"}, "authority-laundering text"),
            ({"decision_id": "BEO-PUBLICATION-PATH-approved%46orPublication"}, "authority-laundering text"),
            ({"operator_identity": "discord:684235178083745819-secret-token"}, "secret-bearing field"),
            ({"future_request_id_candidate": "BEO-PUBLICATION-PREREQUISITE-publishBEO"}, "authority-laundering text"),
            ({"future_request_id_candidate": "BEO-PUBLICATION-PREREQUISITE-docs%252Frequirements%252Factive"}, "authority-laundering text"),
            ({"operator_attestation": {**valid_request(interface)["operator_attestation"], "RTMGeneration": True}}, "forbidden authority field"),
            ({"operator_attestation": {**valid_request(interface)["operator_attestation"], "signerKeyMaterial": "SECRET"}}, "secret-bearing field"),
            ({"operator_attestation": {**valid_request(interface)["operator_attestation"], "notes": "The system shall publish"}}, "forbidden authority field"),
            ({"nested": {"publishBEO": True}}, "unexpected field"),
        ]
        for patch, message in hostile_cases:
            with self.subTest(patch=patch):
                request = valid_request(interface, **patch)
                with self.assertRaisesRegex(ValueError, message):
                    build_beo_publication_path_decision_gate(interface, request, used_decision_ids=set())

    def test_rejects_interface_trace_metadata_drift_from_exact_request(self):
        interface = valid_interface()
        request = valid_request(interface)
        request["exact_trace_identities"] = request["exact_trace_identities"][:-1]
        with self.assertRaisesRegex(ValueError, "exact_trace_identities must match"):
            build_beo_publication_path_decision_gate(interface, request, used_decision_ids=set())

        forged = copy.deepcopy(interface)
        forged["trace_artifacts"][0]["body"] = "The system shall publish"
        request = valid_request(forged)
        with self.assertRaisesRegex(ValueError, "interface trace_artifacts rejects unsupported key|authority-laundering text"):
            build_beo_publication_path_decision_gate(forged, request, used_decision_ids=set())

    def test_rejects_unicode_digits_in_exact_ids_and_identity(self):
        interface = valid_interface()

        forged_interface = copy.deepcopy(interface)
        forged_interface["interface_id"] = "BEO_RTM_IFACE_１２６"
        forged_request = valid_request(forged_interface)
        with self.assertRaisesRegex(ValueError, "interface_id must be exact BEO_RTM_IFACE_###"):
            build_beo_publication_path_decision_gate(forged_interface, forged_request, used_decision_ids=set())

        forged_interface = copy.deepcopy(interface)
        forged_interface["trace_artifacts"][0]["id"] = "REQ-１２６"
        forged_request = valid_request(forged_interface)
        with self.assertRaisesRegex(ValueError, "trace_artifacts.id must be exact REQ-### or UC-###"):
            build_beo_publication_path_decision_gate(forged_interface, forged_request, used_decision_ids=set())

        unicode_cases = [
            ({"decision_id": "BEO-PUBLICATION-PATH-DECISION-GATE-１２６-００１"}, "decision_id must be exact"),
            ({"operator_identity": "discord:１２３４５６７８９０１２３４５６７"}, "operator_identity must be discord:<snowflake>"),
            ({"future_request_id_candidate": "BEO-PUBLICATION-PREREQUISITE-REQUEST-１２７-００１"}, "future_request_id_candidate must be exact"),
            ({"exact_trace_identities": ["REQ:REQ-１２６:sha256:" + "a" * 64]}, "exact_trace_identities id must be exact"),
        ]
        for patch, message in unicode_cases:
            with self.subTest(patch=patch):
                request = valid_request(interface, **patch)
                with self.assertRaisesRegex(ValueError, message):
                    build_beo_publication_path_decision_gate(interface, request, used_decision_ids=set())

    def test_returned_gate_defensively_copies_trace_metadata_before_hashing(self):
        interface = valid_interface()
        request = valid_request(interface)
        gate = build_beo_publication_path_decision_gate(interface, request, used_decision_ids=set())

        interface["trace_artifacts"][0]["id"] = "REQ-999"
        request["operator_attestation"]["metadata_handoff_reviewed"] = False

        self.assertEqual(gate["trace_artifacts"], TRACE_ARTIFACTS)
        self.assertEqual(
            gate["decision_gate_hash"],
            _canonical_hash({key: value for key, value in gate.items() if key != "decision_gate_hash"}),
        )

    def test_disabled_activation_adapter_has_complete_no_side_effect_surface(self):
        interface = valid_interface()
        request = valid_request(interface)
        gate = build_beo_publication_path_decision_gate(interface, request, used_decision_ids=set())

        adapter = simulate_disabled_beo_publication_path_activation_adapter(gate)

        self.assertEqual(adapter["adapter_result"], "BEO_PUBLICATION_PATH_ACTIVATION_DISABLED_NOT_AUTHORIZED")
        self.assertEqual(adapter["selected_next_rung"], SELECTED_NEXT_RUNG)
        forged_adapter = simulate_disabled_beo_publication_path_activation_adapter(
            {"decision_id": gate["decision_id"], "selected_next_rung": "AUTHORITATIVE_BEO_PUBLICATION"}
        )
        self.assertIsNone(forged_adapter["selected_next_rung"])
        self.assertIsNone(forged_adapter["decision_id"])
        for key in {
            "publication_approval_captured",
            "beo_publication_attempted",
            "runtime_published_beo_output",
            "signature_generated",
            "signer_key_material_accessed",
            "immutable_storage_written",
            "public_ledger_mutated",
            "rollback_executed",
            "rtm_generated",
            "drift_rejection_performed",
            "active_vault_hash_comparison_performed",
            "protected_body_read_attempted",
            "protected_body_copy_attempted",
            "blk_pipe_dispatched",
            "blk_test_runtime_started",
            "codex_subprocess_started",
            "target_repo_scanned",
            "target_repo_mutated",
            "source_mutation_attempted",
            "git_mutation_attempted",
            "package_manager_called",
            "network_called",
            "model_service_called",
            "browser_tooling_called",
            "cyber_tooling_called",
            "production_isolation_claimed",
        }:
            self.assertIn(key, adapter)
            self.assertIs(adapter[key], False, key)

    def test_module_contains_no_live_publication_runtime_or_mutation_imports(self):
        tree = ast.parse(MODULE.read_text())
        forbidden_imports = {"subprocess", "socket", "requests", "urllib", "http", "ftplib", "paramiko", "git", "os", "shutil", "pathlib"}
        forbidden_calls = {"eval", "exec", "__import__", "compile", "open", "system", "popen", "Popen", "run", "write", "unlink", "rename"}
        offenders = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                offenders.extend(alias.name for alias in node.names if alias.name.split(".")[0] in forbidden_imports)
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.split(".")[0] in forbidden_imports:
                    offenders.append(node.module)
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in forbidden_calls:
                    offenders.append(node.func.id)
                if isinstance(node.func, ast.Attribute) and node.func.attr in forbidden_calls:
                    offenders.append(node.func.attr)
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
