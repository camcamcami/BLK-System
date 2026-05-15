import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from test_post_rtm_generation_reconciliation import valid_blk143_execution_package, valid_reconciliation_context
from post_rtm_generation_reconciliation import build_post_rtm_generation_reconciliation

from authority_ladder_hardening_policy import (
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    HARDENING_CONTEXT_ID,
    HARDENING_MODE,
    NEXT_FRONTIER,
    POLICY_PACKAGE_ID,
    POLICY_SCOPE,
    POLICY_STATUS,
    SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS,
    build_authority_ladder_hardening_policy,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "authority_ladder_hardening_policy.py"


def valid_blk144_reconciliation_package():
    execution = valid_blk143_execution_package()
    context = valid_reconciliation_context(execution)
    return build_post_rtm_generation_reconciliation(execution, context)


def valid_hardening_context(reconciliation=None, **overrides):
    if reconciliation is None:
        reconciliation = valid_blk144_reconciliation_package()
    context = {
        "hardening_context_id": HARDENING_CONTEXT_ID,
        "operator_identity": reconciliation["operator_identity"],
        "hardening_mode": HARDENING_MODE,
        "policy_scope": POLICY_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_reconciliation_package_id": reconciliation["reconciliation_package_id"],
        "upstream_reconciliation_package_hash": reconciliation["reconciliation_package_hash"],
        "upstream_reconciliation_context_hash": reconciliation["reconciliation_context_hash"],
        "upstream_execution_package_id": reconciliation["upstream_execution_package_id"],
        "upstream_execution_package_hash": reconciliation["upstream_execution_package_hash"],
        "upstream_rtm_record_id": reconciliation["upstream_rtm_record_id"],
        "upstream_rtm_record_hash": reconciliation["upstream_rtm_record_hash"],
        "hardening_reason": "STOP_AND_HARDEN_ONLY_AFTER_CLEAN_POST_RTM_RECONCILIATION",
        "authority_rung_selected": False,
        "authority_decision_requested": False,
        "execution_requested": False,
        "hardened_at": "2099-05-15T16:00:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {
            "exact_blk144_reconciliation_reviewed": True,
            "hardening_only_mode_selected": True,
            "no_authority_rung_selected": True,
            "no_authority_decision_requested": True,
            "no_execution_requested": True,
            "reconciliation_evidence_is_not_authority": True,
            "no_active_vault_filesystem_read": True,
            "no_protected_body_reads": True,
            "no_drift_rejection_or_coverage_truth": True,
            "no_reusable_blk_link_authority": True,
            "no_beb_dispatch_or_beo_closeout": True,
            "no_signer_storage_ledger_side_effects": True,
            "no_target_source_git_mutation": True,
            "no_blk_pipe_blk_test_codex_tooling": True,
            "no_production_isolation_claim": True,
        },
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        context[flag] = False
    context.update(overrides)
    return context


def rehash_reconciliation_package(package):
    package["reconciliation_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "reconciliation_package_hash"}
    )
    return package


class AuthorityLadderHardeningPolicyTest(unittest.TestCase):
    def test_builds_hardening_only_policy_without_selecting_or_requesting_next_authority(self):
        reconciliation = valid_blk144_reconciliation_package()
        context = valid_hardening_context(reconciliation)

        package = build_authority_ladder_hardening_policy(reconciliation, context)

        self.assertEqual(package["policy_status"], POLICY_STATUS)
        self.assertEqual(package["policy_package_id"], POLICY_PACKAGE_ID)
        self.assertEqual(package["policy_scope"], POLICY_SCOPE)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["upstream_reconciliation_package_id"], reconciliation["reconciliation_package_id"])
        self.assertEqual(package["upstream_reconciliation_package_hash"], reconciliation["reconciliation_package_hash"])
        self.assertEqual(package["hardening_context_hash"], _canonical_hash(context))
        self.assertEqual(package["next_frontier"], NEXT_FRONTIER)
        self.assertFalse(package["authority_rung_selected"])
        self.assertFalse(package["authority_decision_requested"])
        self.assertFalse(package["execution_requested"])
        self.assertTrue(package["reconciliation_evidence_is_authority" ] is False)
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(
            package["policy_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "policy_package_hash"}),
        )

    def test_rejects_forged_rehashed_or_authority_claiming_blk144_reconciliation(self):
        reconciliation = valid_blk144_reconciliation_package()
        context = valid_hardening_context(reconciliation)

        forged = copy.deepcopy(reconciliation)
        forged["reconciliation_package_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "reconciliation_package_hash does not match submitted BLK-144 package"):
            build_authority_ladder_hardening_policy(forged, context)

        forged = copy.deepcopy(reconciliation)
        forged["reconciliation_package_id"] = "POST-RTM-GENERATION-RECONCILIATION-１４５-001"
        rehash_reconciliation_package(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-144 reconciliation package required"):
            build_authority_ladder_hardening_policy(forged, valid_hardening_context(forged))

        forged = copy.deepcopy(reconciliation)
        forged["next_frontier_granted"] = True
        rehash_reconciliation_package(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-144 reconciliation package required|next_frontier_granted must remain false"):
            build_authority_ladder_hardening_policy(forged, valid_hardening_context(forged))

    def test_rejects_any_attempt_to_select_request_or_execute_a_next_authority_rung(self):
        reconciliation = valid_blk144_reconciliation_package()
        base_context = valid_hardening_context(reconciliation)
        cases = [
            ({"authority_rung_selected": True}, "authority_rung_selected must remain false"),
            ({"authority_decision_requested": True}, "authority_decision_requested must remain false"),
            ({"execution_requested": True}, "execution_requested must remain false"),
            ({"hardening_mode": "REQUEST_NEXT_AUTHORITY_DECISION"}, "hardening_mode must match exact hardening-only value|authority-laundering text"),
            ({"selected_frontier": "postRtmAuthorityDecision"}, "selected_frontier must match exact hardening-only value|authority-laundering text"),
            ({"reusable_blk_link_authority_granted": True}, "reusable_blk_link_authority_granted must remain false"),
            ({"rtm_drift_rejection_authorized": True}, "rtm_drift_rejection_authorized must remain false"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS) + [sorted(EXACT_PROOF_OBLIGATIONS)[0]]}, "proof_obligations must not contain duplicates"),
            ({"excluded_authorities": ["NOPE"]}, "excluded_authorities must match exact denied authority set"),
        ]
        for patch, message in cases:
            candidate = copy.deepcopy(base_context)
            candidate.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_authority_ladder_hardening_policy(reconciliation, candidate)

    def test_rejects_authority_laundering_protected_paths_tooling_and_extra_fields(self):
        reconciliation = valid_blk144_reconciliation_package()
        context = valid_hardening_context(reconciliation)
        cases = [
            ({"hardening_context_id": "AUTHORITY-LADDER-HARDENING-145-docs%2525252Frequirements%2525252Factive"}, "protected body text"),
            ({"operator_identity": "discord:684235178083745819-approvedForProduction"}, "authority-laundering text"),
            ({"hardening_reason": "greenlit for publication after hardening"}, "authority-laundering text"),
            ({"policy_scope": "HARDEN_AND_ESTABLISH_COVERAGE_TRUTH"}, "policy_scope must match exact hardening-only value|authority-laundering text"),
            ({"curlWrapper": False}, "unexpected field"),
            ({"operator_attestation": context["operator_attestation"] | {"publishBEO": True}}, "unexpected field"),
        ]
        for patch, message in cases:
            candidate = copy.deepcopy(context)
            candidate.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_authority_ladder_hardening_policy(reconciliation, candidate)

    def test_context_is_hash_bound_and_returned_inputs_are_defensively_copied(self):
        reconciliation = valid_blk144_reconciliation_package()
        base_context = valid_hardening_context(reconciliation)
        alt_context = valid_hardening_context(reconciliation, hardened_at="2099-05-15T16:10:00+10:00")

        base_package = build_authority_ladder_hardening_policy(reconciliation, base_context)
        alt_package = build_authority_ladder_hardening_policy(reconciliation, alt_context)

        self.assertEqual(base_package["hardening_context_hash"], _canonical_hash(base_context))
        self.assertEqual(alt_package["hardening_context_hash"], _canonical_hash(alt_context))
        self.assertNotEqual(base_package["hardening_context_hash"], alt_package["hardening_context_hash"])
        self.assertNotEqual(base_package["policy_package_hash"], alt_package["policy_package_hash"])
        base_context["operator_attestation"]["no_drift_rejection_or_coverage_truth"] = "mutated"
        self.assertIs(base_package["operator_attestation"]["no_drift_rejection_or_coverage_truth"], True)

    def test_module_has_no_live_runtime_tooling_or_protected_body_file_access(self):
        tree = ast.parse(MODULE.read_text())
        imported = set()
        calls = set()
        forbidden_imports = {"subprocess", "socket", "requests", "urllib3", "httpx", "shutil", "pathlib", "os"}
        forbidden_calls = {"system", "popen", "Popen", "run", "call", "check_call", "check_output", "exec", "eval", "open", "read_text", "urlopen", "request", "__import__"}
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
        self.assertEqual(imported & forbidden_imports, set())
        self.assertEqual(calls & forbidden_calls, set())


if __name__ == "__main__":
    unittest.main()
