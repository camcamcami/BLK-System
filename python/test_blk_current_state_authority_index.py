import ast
import unittest
from pathlib import Path

from blk_current_state_authority_index import (
    build_current_state_authority_index,
    evaluate_current_state_authority_index,
    validate_current_state_authority_index,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "blk_current_state_authority_index.py"

EXPECTED_SURFACES = {
    "BLK-req legislative gateway",
    "BLK-pipe blast shield",
    "Python adapter layer",
    "Validation profiles",
    "BLK-test",
    "Operator health / observability",
    "Codex live-dispatch ladder",
    "BEO publication path",
    "RTM / blk-link",
    "BLK-078 tactical standard profile architecture",
    "BLK-080 tactical profile registry / Layer B extraction",
    "BLK-081 target-repo execution governance pattern",
    "BLK-082 BLK-058 mechanical enforcement upgrade",
    "BLK-083 BEO publication decision package / pilot request",
    "BLK-084 post-083 frontier selection gate refresh",
    "BLK-085 BEO publication pilot execution request gate",
    "BLK-058 Kuronode TypeScript tactical profile source",
}

DENIED_FLAGS = [
    "runtime_authority_granted",
    "live_codex_execution_authorized",
    "blk_pipe_dispatch_authorized",
    "production_blk_test_mcp_authorized",
    "authoritative_beo_publication_authorized",
    "runtime_rtm_generation_authorized",
    "rtm_drift_rejection_authorized",
    "protected_blk_req_body_reads_authorized",
    "network_model_cyber_browser_tooling_authorized",
    "package_manager_authorized",
    "production_isolation_claimed",
]


class CurrentStateAuthorityIndexTest(unittest.TestCase):
    def test_default_index_ready_for_operator_review_not_authority(self):
        record = build_current_state_authority_index()

        self.assertEqual(record["index_id"], "blk_system_current_state_authority_index")
        self.assertEqual(record["index_status"], "BLK_SYSTEM_CURRENT_STATE_AUTHORITY_INDEX")
        self.assertEqual(record["roadmap_source"], "BLK-077")
        self.assertEqual(record["maturity"], "CURRENT_STATE_INDEX_L0_L1_ONLY")

        evaluated = evaluate_current_state_authority_index(record)

        self.assertEqual(evaluated["evaluation"], "CURRENT_STATE_INDEX_READY_FOR_OPERATOR_REVIEW_NOT_AUTHORITY")
        self.assertEqual(evaluated["validation_errors"], [])

    def test_every_expected_authority_surface_present_exactly_once(self):
        record = build_current_state_authority_index()
        names = [surface["surface"] for surface in record["surfaces"]]

        self.assertEqual(set(names), EXPECTED_SURFACES)
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(len(names), len(EXPECTED_SURFACES))

    def test_runtime_and_adjacent_authorities_are_all_denied(self):
        record = build_current_state_authority_index()

        for flag in DENIED_FLAGS:
            self.assertIs(record[flag], False, flag)

        by_surface = {surface["surface"]: surface for surface in record["surfaces"]}
        self.assertIn("not execution-authorized", by_surface["Codex live-dispatch ladder"]["authority_cutline"])
        self.assertIn("Production MCP remains disabled", by_surface["BLK-test"]["authority_cutline"])
        self.assertIn("Authoritative publication remains disabled", by_surface["BEO publication path"]["authority_cutline"])
        self.assertIn("Runtime RTM generation and drift rejection remain disabled", by_surface["RTM / blk-link"]["authority_cutline"])
        self.assertIn("Protected bodies remain isolated", by_surface["BLK-req legislative gateway"]["authority_cutline"])
        self.assertIn("profile architecture is doctrine only", by_surface["BLK-078 tactical standard profile architecture"]["authority_cutline"])
        self.assertIn("future approved Kuronode TypeScript work only", by_surface["BLK-058 Kuronode TypeScript tactical profile source"]["authority_cutline"])

    def test_post_078_governing_docs_and_profile_surfaces_are_current(self):
        record = build_current_state_authority_index()
        self.assertEqual(record["roadmap_source"], "BLK-077")
        by_surface = {surface["surface"]: surface for surface in record["surfaces"]}

        for surface in record["surfaces"]:
            self.assertIn("BLK-077", surface["governing_docs"], surface["surface"])

        profile_architecture = by_surface["BLK-078 tactical standard profile architecture"]
        self.assertEqual(profile_architecture["state"], "doctrine_only_profile_architecture")
        self.assertEqual(profile_architecture["maturity"], "L0_ARCHITECTURE_DOCTRINE_ONLY")
        self.assertIn("BLK-078", profile_architecture["governing_docs"])
        self.assertIn("Layer A", profile_architecture["authority_cutline"])
        self.assertIn("Layer B", profile_architecture["authority_cutline"])
        self.assertIn("Layer C", profile_architecture["authority_cutline"])
        self.assertIn("does not authorize scans, mutation, dispatch, BLK-test, BEO, or RTM", profile_architecture["authority_cutline"])

        profile_registry = by_surface["BLK-080 tactical profile registry / Layer B extraction"]
        self.assertEqual(profile_registry["state"], "tactical_profile_registry_l0_l1_fixture_complete")
        self.assertEqual(profile_registry["maturity"], "L0_L1_PROFILE_REGISTRY_FIXTURE_DOCTRINE")
        self.assertIn("BLK-080", profile_registry["governing_docs"])
        self.assertIn("python/blk_tactical_profile_registry.py", profile_registry["authority_cutline"])
        self.assertIn("target-repo execution governance", profile_registry["authority_cutline"])
        self.assertIn("no target-repo mutation", profile_registry["authority_cutline"])

        target_governance = by_surface["BLK-081 target-repo execution governance pattern"]
        self.assertEqual(target_governance["state"], "target_repo_governance_l0_l1_fixture_complete")
        self.assertEqual(target_governance["maturity"], "L0_L1_TARGET_REPO_GOVERNANCE_FIXTURE_DOCTRINE")
        self.assertIn("BLK-081", target_governance["governing_docs"])
        self.assertIn("python/blk_target_repo_execution_governance.py", target_governance["authority_cutline"])
        self.assertIn("BLK-058 mechanical enforcement", target_governance["authority_cutline"])
        self.assertIn("no target-repo scan", target_governance["authority_cutline"])
        self.assertIn("no BEB dispatch or BEO closeout execution", target_governance["authority_cutline"])

        mechanical_enforcement = by_surface["BLK-082 BLK-058 mechanical enforcement upgrade"]
        self.assertEqual(mechanical_enforcement["state"], "blk058_mechanical_enforcement_l0_l1_fixture_complete")
        self.assertEqual(mechanical_enforcement["maturity"], "L0_L1_BLK058_MECHANICAL_ENFORCEMENT_FIXTURE")
        self.assertIn("BLK-082", mechanical_enforcement["governing_docs"])
        self.assertIn("python/blk_058_mechanical_enforcement.py", mechanical_enforcement["authority_cutline"])
        self.assertIn("explicit operator decision", mechanical_enforcement["authority_cutline"])
        self.assertIn("no target-repo scan", mechanical_enforcement["authority_cutline"])
        self.assertIn("no BEO publication", mechanical_enforcement["authority_cutline"])

        beo_decision_package = by_surface["BLK-083 BEO publication decision package / pilot request"]
        self.assertEqual(beo_decision_package["state"], "beo_publication_decision_package_l0_l1_review_fixture_complete")
        self.assertEqual(beo_decision_package["maturity"], "L0_L1_BEO_PUBLICATION_DECISION_PACKAGE_REVIEW_FIXTURE")
        self.assertIn("BLK-083", beo_decision_package["governing_docs"])
        self.assertIn("BLK-060", beo_decision_package["governing_docs"])
        self.assertIn("python/beo_publication_decision_package.py", beo_decision_package["authority_cutline"])
        self.assertIn("future explicit human publication pilot approval", beo_decision_package["authority_cutline"])
        self.assertIn("no publication pilot execution", beo_decision_package["authority_cutline"])
        self.assertIn("no RTM generation", beo_decision_package["authority_cutline"])
        self.assertIn("no protected-body reads", beo_decision_package["authority_cutline"])

        post083_selector = by_surface["BLK-084 post-083 frontier selection gate refresh"]
        self.assertEqual(post083_selector["state"], "post083_frontier_selection_l0_l1_fixture_complete")
        self.assertEqual(post083_selector["maturity"], "L0_L1_POST083_FRONTIER_SELECTION_FIXTURE")
        self.assertIn("BLK-084", post083_selector["governing_docs"])
        self.assertIn("BLK-083", post083_selector["governing_docs"])
        self.assertIn("python/blk_post083_frontier_selection_gate.py", post083_selector["authority_cutline"])
        self.assertIn("next logical sprint is not approval", post083_selector["authority_cutline"])
        self.assertIn("no publication pilot execution", post083_selector["authority_cutline"])
        self.assertIn("no RTM generation", post083_selector["authority_cutline"])
        self.assertIn("no target-repo scan", post083_selector["authority_cutline"])

        pilot_request_gate = by_surface["BLK-085 BEO publication pilot execution request gate"]
        self.assertEqual(pilot_request_gate["state"], "beo_publication_pilot_request_gate_l0_l1_complete")
        self.assertEqual(pilot_request_gate["maturity"], "L0_L1_BEO_PUBLICATION_PILOT_REQUEST_GATE")
        self.assertIn("BLK-085", pilot_request_gate["governing_docs"])
        self.assertIn("BLK-083", pilot_request_gate["governing_docs"])
        self.assertIn("python/beo_publication_pilot_execution_request.py", pilot_request_gate["authority_cutline"])
        self.assertIn("explicit human publication pilot approval is still required", pilot_request_gate["authority_cutline"])
        self.assertIn("no publication approval", pilot_request_gate["authority_cutline"])
        self.assertIn("no publication pilot execution", pilot_request_gate["authority_cutline"])
        self.assertIn("no signer/storage/ledger/rollback", pilot_request_gate["authority_cutline"])
        self.assertIn("no RTM generation", pilot_request_gate["authority_cutline"])
        self.assertIn("no target-repo scan", pilot_request_gate["authority_cutline"])

        kuronode_profile = by_surface["BLK-058 Kuronode TypeScript tactical profile source"]
        self.assertEqual(kuronode_profile["state"], "target_profile_source_not_dispatch_authority")
        self.assertEqual(kuronode_profile["maturity"], "L0_LAYER_C_PROFILE_SOURCE_ONLY")
        self.assertIn("BLK-058", kuronode_profile["governing_docs"])
        self.assertIn("BLK-078", kuronode_profile["governing_docs"])
        self.assertIn("future approved Kuronode TypeScript work only", kuronode_profile["authority_cutline"])
        self.assertIn("no Kuronode mutation", kuronode_profile["authority_cutline"])

    def test_unsupported_state_and_maturity_fail_closed(self):
        record = build_current_state_authority_index()
        record["surfaces"][0]["state"] = "LIVE_EXECUTION_ENABLED"
        record["surfaces"][1]["maturity"] = "L5_PRODUCTION_AUTHORITY"

        errors = validate_current_state_authority_index(record)
        evaluated = evaluate_current_state_authority_index(record)

        self.assertTrue(any("unsupported state" in error for error in errors))
        self.assertTrue(any("unsupported maturity" in error for error in errors))
        self.assertEqual(evaluated["evaluation"], "CURRENT_STATE_INDEX_BLOCKED")

    def test_recursive_authority_laundering_keys_and_values_fail_closed(self):
        record = build_current_state_authority_index()
        record["surfaces"][0]["nested"] = {
            "APPROVED_FOR_LIVE_EXECUTION": False,
            "notes": ["authoritative BEO publication approved"],
        }

        errors = validate_current_state_authority_index(record)
        evaluated = evaluate_current_state_authority_index(record)

        self.assertTrue(any("forbidden authority wording" in error for error in errors), errors)
        self.assertEqual(evaluated["evaluation"], "CURRENT_STATE_INDEX_BLOCKED")

    def test_recursive_denied_flags_and_generic_authority_claims_fail_closed(self):
        record = build_current_state_authority_index()
        record["surfaces"][0]["nested"] = {
            "live_codex_execution_authorized": True,
            "execution_authorized": True,
            "authority": "approved for runtime execution",
            "notes": ["runtime_authority_granted"],
        }

        errors = validate_current_state_authority_index(record)
        evaluated = evaluate_current_state_authority_index(record)

        self.assertTrue(any("live_codex_execution_authorized" in error for error in errors), errors)
        self.assertTrue(any("execution_authorized" in error for error in errors), errors)
        self.assertTrue(any("approved for runtime execution" in error for error in errors), errors)
        self.assertTrue(any("runtime_authority_granted" in error for error in errors), errors)
        self.assertEqual(evaluated["evaluation"], "CURRENT_STATE_INDEX_BLOCKED")

    def test_extra_authority_claim_fields_fail_closed(self):
        record = build_current_state_authority_index()
        record["approved_for_runtime_execution"] = True
        record["surfaces"][0]["approved"] = True
        record["surfaces"][0]["authorized"] = True
        record["surfaces"][0]["approval_status"] = "approved"
        record["surfaces"][0]["note"] = "live execution authorized"
        record["surfaces"][1]["authority_cutline"] = "runtime execution authorized"

        errors = validate_current_state_authority_index(record)
        evaluated = evaluate_current_state_authority_index(record)

        for marker in [
            "approved_for_runtime_execution",
            "approved",
            "authorized",
            "approval_status",
            "note",
            "live execution authorized",
            "runtime execution authorized",
        ]:
            self.assertTrue(any(marker in error for error in errors), (marker, errors))
        self.assertEqual(evaluated["evaluation"], "CURRENT_STATE_INDEX_BLOCKED")

    def test_natural_language_authority_claims_and_governing_doc_laundering_fail_closed(self):
        phrases = [
            "Live Codex execution authorized.",
            "Live Codex execution is authorized.",
            "live Codex execution authority",
            "Runtime execution is authorized.",
            "production BLK-test MCP authority",
            "Production BLK-test MCP is authorized.",
            "authoritative BEO publication authority",
            "Authoritative BEO publication is authorized.",
            "RTM drift rejection authority",
            "RTM drift rejection is authorized.",
            "protected BLK-req body reads authorized",
            "Protected BLK-req body reads are authorized.",
            "network tooling authority",
            "Network tooling is authorized.",
            "package-manager tooling authority",
            "Package manager tooling is authorized.",
            "production sandbox enforced",
            "Production sandbox is enforced.",
            "runtime-execution-authorized",
            "live-execution-authorized",
            "execution authorized",
            "not execution authorized; execution authorized after approval",
            "approvedForRuntimeExecution",
            "approvedforruntimeexecution",
            "approved%20for%20runtime%20execution",
            "liveCodexExecutionAuthorized",
            "networkToolingIsAuthorized",
            "runtimeExecutionIsAuthorized",
            "authoritativeBeoPublicationIsAuthorized",
            "rtmDriftRejectionIsAuthorized",
            "protectedBlkReqBodyReadsAreAuthorized",
            "runtime%45xecution%49s%41uthorized",
            "liveCodexExecutionIsAuthorized",
            "productionBlkTestMcpIsAuthorized",
            "packageManagerToolingIsAuthorized",
            "packageManagerTooling%49s%41uthorized",
            "packageManagerAuthorized",
            "networkModelCyberBrowserToolingAuthorized",
            "networkModelCyberBrowserToolingIsAuthorized",
            "productionIsolationClaimed",
            "packageManagerIsAuthorized",
            "Package manager is authorized.",
            "packageManagersAreAuthorized",
            "networkModelBrowserCyberToolingIsAuthorized",
            "network%4DodelBrowserCyberTooling%49s%41uthorized",
            "modelServiceIsAuthorized",
            "Browser tooling is authorized.",
            "Cyber tooling is authorized.",
            "productionIsolationIsClaimed",
            "Production isolation is claimed.",
            "productionIsolationClaimsAreAuthorized",
            "Git mutation authorized",
            "git commit authorized",
            "git push allowed",
            "staging authorized",
            "autofix allowed",
            "source mutation allowed",
        ]
        for phrase in phrases:
            record = build_current_state_authority_index()
            record["surfaces"][0]["authority_cutline"] = phrase
            errors = validate_current_state_authority_index(record)
            self.assertTrue(errors, phrase)

        for bad_doc in [{"is_authorized": True}, "approved", "runtime authority granted"]:
            record = build_current_state_authority_index()
            record["surfaces"][0]["governing_docs"].append(bad_doc)
            errors = validate_current_state_authority_index(record)
            self.assertTrue(errors, bad_doc)

    def test_default_record_contains_evaluation_and_evaluated_records_validate(self):
        record = build_current_state_authority_index()
        self.assertEqual(record["evaluation"], "CURRENT_STATE_INDEX_READY_FOR_OPERATOR_REVIEW_NOT_AUTHORITY")
        self.assertEqual(record["validation_errors"], [])

        evaluated = evaluate_current_state_authority_index(record)

        self.assertEqual(validate_current_state_authority_index(evaluated), [])

    def test_positive_authority_flags_fail_closed(self):
        for flag in DENIED_FLAGS:
            record = build_current_state_authority_index()
            record[flag] = True

            errors = validate_current_state_authority_index(record)
            evaluated = evaluate_current_state_authority_index(record)

            self.assertTrue(any(flag in error for error in errors), flag)
            self.assertIs(evaluated[flag], False, flag)
            self.assertEqual(evaluated["evaluation"], "CURRENT_STATE_INDEX_BLOCKED")

    def test_module_contains_no_live_surface_imports_or_calls(self):
        tree = ast.parse(MODULE.read_text())
        forbidden_imports = {"subprocess", "socket", "requests", "urllib", "http", "git"}
        forbidden_calls = {"eval", "exec", "__import__", "compile", "open"}
        offenders = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [alias.name.split(".")[0] for alias in node.names]
                if node.module:
                    names.append(node.module.split(".")[0])
                offenders.extend(name for name in names if name in forbidden_imports)
            if isinstance(node, ast.Call):
                func = node.func
                name = ""
                if isinstance(func, ast.Name):
                    name = func.id
                elif isinstance(func, ast.Attribute):
                    name = func.attr
                if name in forbidden_calls:
                    offenders.append(name)

        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
