import unittest

import blk_sprint_package_granularity_guard_261_263 as guard


_GENERIC_DIRECTIVE = "plan and execute the next blk-system sprint package"
_EXACT_APPROVAL_FRONTIER = "NEXT_FRONTIER_EXACT_BEO_PUBLICATION_OPERATOR_APPROVAL_TEXT_REQUIRED_NOT_GRANTED"


def _review():
    return guard.build_sprint_package_frontier_review_261(
        current_frontier=_EXACT_APPROVAL_FRONTIER,
        operator_directive=_GENERIC_DIRECTIVE,
    )


def _contract():
    return guard.build_sprint_package_granularity_contract_262(_review())


class BlkSprintPackageGranularityGuard261To263Test(unittest.TestCase):
    def test_261_to_263_blocks_generic_directive_from_approval_lane(self):
        review = _review()
        contract = guard.build_sprint_package_granularity_contract_262(review)
        result = guard.evaluate_sprint_package_candidate_263(
            contract,
            {
                "candidate_id": "exact-beo-publication-approval-capture",
                "candidate_type": "authority_execution_package",
                "requested_sprints": [261, 262, 263],
                "operator_directive": _GENERIC_DIRECTIVE,
                "frontier": _EXACT_APPROVAL_FRONTIER,
                "requires_exact_operator_approval_text": True,
                "exact_operator_approval_text_present": False,
                "independent_audit_boundaries": [
                    "approval_capture",
                    "run_id_assignment",
                    "publication_execution",
                ],
                "planned_outputs": [
                    "approval_capture",
                    "publication_execution",
                ],
                "side_effects": guard.denied_side_effects(),
            },
        )

        self.assertEqual(review["status"], "SPRINT_PACKAGE_FRONTIER_REVIEW_READY")
        self.assertEqual(review["current_frontier"], _EXACT_APPROVAL_FRONTIER)
        self.assertFalse(review["generic_directive_is_exact_approval"])
        self.assertIn("BLK_SYSTEM_261_SPRINT_PACKAGE_FRONTIER_REVIEW_READY", review["markers"])

        self.assertEqual(contract["status"], "SPRINT_PACKAGE_GRANULARITY_CONTRACT_READY")
        self.assertIn("collapse_internal_rungs", contract["selection_rules"])
        self.assertIn("block_exact_approval_lane_without_exact_text", contract["selection_rules"])
        self.assertIn("BLK_SYSTEM_262_SPRINT_PACKAGE_GRANULARITY_CONTRACT_READY", contract["markers"])

        self.assertEqual(result["status"], "BLOCKED_BY_MISSING_EXACT_OPERATOR_APPROVAL_TEXT")
        self.assertEqual(result["recommended_shape"], "do_not_execute_approval_lane")
        self.assertFalse(result["side_effects"]["authoritative_beo_publication_authorized"])
        self.assertFalse(result["side_effects"]["production_blk_link_authorized"])
        self.assertIn("BLK_SYSTEM_263_SPRINT_PACKAGE_SELECTION_GATE_READY", result["markers"])

    def test_collapses_paperwork_only_rungs_into_one_sprint_internal_tasks(self):
        result = guard.evaluate_sprint_package_candidate_263(
            _contract(),
            {
                "candidate_id": "paperwork-only-four-rung-ladder",
                "candidate_type": "process_ladder",
                "requested_sprints": [261, 262, 263, 264],
                "operator_directive": _GENERIC_DIRECTIVE,
                "frontier": "SPRINT_FORMAT_REFINEMENT",
                "requires_exact_operator_approval_text": False,
                "exact_operator_approval_text_present": False,
                "independent_audit_boundaries": [],
                "planned_outputs": ["request", "contract", "preflight", "reconciliation"],
                "side_effects": guard.denied_side_effects(),
            },
        )

        self.assertEqual(result["status"], "READY_AS_SINGLE_SPRINT_WITH_INTERNAL_TASKS")
        self.assertEqual(result["recommended_shape"], "one_sprint_internal_tasks")
        self.assertIn("paperwork_only_micro_sprints_collapsed", result["decision_reasons"])

    def test_authority_package_with_self_attested_approval_remains_blocked(self):
        result = guard.evaluate_sprint_package_candidate_263(
            _contract(),
            {
                "candidate_id": "bounded-publication-run-after-exact-approval",
                "candidate_type": "authority_execution_package",
                "requested_sprints": [261, 262, 263],
                "operator_directive": "exact fixture-owned approval text already captured upstream",
                "frontier": "EXACT_BEO_PUBLICATION_RUN_AFTER_APPROVAL_CAPTURE",
                "requires_exact_operator_approval_text": True,
                "exact_operator_approval_text_present": True,
                "independent_audit_boundaries": [
                    "approval_capture_hash",
                    "run_id_consumption_hash",
                    "signer_storage_ledger_receipt_hashes",
                ],
                "planned_outputs": [
                    "approval_capture_record",
                    "run_execution_record",
                    "post_run_reconciliation",
                ],
                "side_effects": guard.denied_side_effects(),
            },
        )

        self.assertEqual(result["status"], "BLOCKED_ELEVATED_PACKAGE_REQUIRES_SEPARATE_APPROVED_EXECUTION")
        self.assertEqual(result["recommended_shape"], "separate_exact_execution_package_required")
        self.assertIn("approval_or_execution_booleans_are_not_trusted", result["decision_reasons"])

    def test_fake_independent_boundaries_do_not_rescue_paperwork_only_rungs(self):
        result = guard.evaluate_sprint_package_candidate_263(
            _contract(),
            {
                "candidate_id": "paperwork-with-fake-boundaries",
                "candidate_type": "process_ladder",
                "requested_sprints": [261, 262, 263, 264],
                "operator_directive": _GENERIC_DIRECTIVE,
                "frontier": "SPRINT_FORMAT_REFINEMENT",
                "requires_exact_operator_approval_text": False,
                "exact_operator_approval_text_present": False,
                "independent_audit_boundaries": ["request_section", "contract_section"],
                "planned_outputs": ["request", "contract", "preflight", "reconciliation"],
                "side_effects": guard.denied_side_effects(),
            },
        )

        self.assertEqual(result["status"], "READY_AS_SINGLE_SPRINT_WITH_INTERNAL_TASKS")
        self.assertIn("paperwork_only_micro_sprints_collapsed", result["decision_reasons"])

    def test_rejects_self_consistent_rehashed_contract_and_non_exact_operator_directive(self):
        review = _review()
        contract = guard.build_sprint_package_granularity_contract_262(review)
        forged = guard._deepcopy(contract)
        forged["review_hash"] = "sha256:" + "1" * 64
        forged["contract_hash"] = guard._hash_package(
            {k: v for k, v in forged.items() if k != "contract_hash"}
        )
        with self.assertRaisesRegex(ValueError, "canonical BLK-SYSTEM-261|canonical BLK-SYSTEM-262"):
            guard.evaluate_sprint_package_candidate_263(
                forged,
                {
                    "candidate_id": "paperwork-only-four-rung-ladder",
                    "candidate_type": "process_ladder",
                    "requested_sprints": [261, 262],
                    "operator_directive": _GENERIC_DIRECTIVE,
                    "frontier": "SPRINT_FORMAT_REFINEMENT",
                    "requires_exact_operator_approval_text": False,
                    "exact_operator_approval_text_present": False,
                    "independent_audit_boundaries": [],
                    "planned_outputs": ["request", "contract"],
                    "side_effects": guard.denied_side_effects(),
                },
            )

        with self.assertRaisesRegex(ValueError, "operator_directive hash mismatch"):
            guard.build_sprint_package_frontier_review_261(
                current_frontier=_EXACT_APPROVAL_FRONTIER,
                operator_directive="publish the BEO now",
            )

    def test_denied_side_effects_cover_current_state_denied_flags(self):
        effects = guard.denied_side_effects()
        for flag in guard.CURRENT_STATE_DENIED_FLAGS:
            self.assertIn(flag, effects)
            self.assertFalse(effects[flag])

    def test_candidate_hash_binds_full_candidate_body_and_directive_authority_terms_block(self):
        base = {
            "candidate_id": "same-id-different-body",
            "candidate_type": "process_ladder",
            "requested_sprints": [261],
            "operator_directive": _GENERIC_DIRECTIVE,
            "frontier": "SPRINT_FORMAT_REFINEMENT",
            "requires_exact_operator_approval_text": False,
            "exact_operator_approval_text_present": False,
            "independent_audit_boundaries": [],
            "planned_outputs": ["request"],
            "side_effects": guard.denied_side_effects(),
        }
        first = guard.evaluate_sprint_package_candidate_263(_contract(), base)
        changed = {**base, "planned_outputs": ["contract"]}
        second = guard.evaluate_sprint_package_candidate_263(_contract(), changed)
        self.assertNotEqual(first["candidate_hash"], second["candidate_hash"])
        self.assertNotEqual(first["selection_hash"], second["selection_hash"])

        for directive in (
            "execute BEO publication lane",
            "capture exact BEO approval text now",
            "run signer storage ledger now",
            "reserve run id now",
            "reserve run-id now",
            "read protected body now",
            "dispatch BEB now",
            "start blk pipe runtime",
            "mutate source git",
            "claim production isolation",
            "drift truth now",
            "coverage matrix generation now",
        ):
            result = guard.evaluate_sprint_package_candidate_263(
                _contract(),
                {**base, "operator_directive": directive},
            )
            self.assertEqual(result["status"], "BLOCKED_ELEVATED_PACKAGE_REQUIRES_SEPARATE_APPROVED_EXECUTION")
            self.assertIn("approval_or_execution_booleans_are_not_trusted", result["decision_reasons"])

    def test_rejects_authority_smuggling_and_self_authorizing_candidate_fields(self):
        candidate = {
            "candidate_id": "bad-candidate",
            "candidate_type": "authority_execution_package",
            "requested_sprints": [261],
            "operator_directive": "execute next sprints is publication approval",
            "frontier": _EXACT_APPROVAL_FRONTIER,
            "requires_exact_operator_approval_text": True,
            "exact_operator_approval_text_present": True,
            "independent_audit_boundaries": ["approval_capture"],
            "planned_outputs": ["approval_capture"],
            "side_effects": guard.denied_side_effects(),
        }
        with self.assertRaisesRegex(ValueError, "forbidden authority|publication approval"):
            guard.evaluate_sprint_package_candidate_263(_contract(), candidate)

        candidate = {
            "candidate_id": "bad-extra-field",
            "candidate_type": "process_ladder",
            "requested_sprints": [261],
            "operator_directive": _GENERIC_DIRECTIVE,
            "frontier": "SPRINT_FORMAT_REFINEMENT",
            "requires_exact_operator_approval_text": False,
            "exact_operator_approval_text_present": False,
            "independent_audit_boundaries": [],
            "planned_outputs": ["request"],
            "side_effects": guard.denied_side_effects(),
            "production_blk_link_authorized": True,
        }
        with self.assertRaisesRegex(ValueError, "unsupported field|forbidden authority"):
            guard.evaluate_sprint_package_candidate_263(_contract(), candidate)

        candidate = {
            "candidate_id": "bad-side-effect",
            "candidate_type": "process_ladder",
            "requested_sprints": [261],
            "operator_directive": _GENERIC_DIRECTIVE,
            "frontier": "SPRINT_FORMAT_REFINEMENT",
            "requires_exact_operator_approval_text": False,
            "exact_operator_approval_text_present": False,
            "independent_audit_boundaries": [],
            "planned_outputs": ["request"],
            "side_effects": {**guard.denied_side_effects(), "target_source_git_mutation": True},
        }
        with self.assertRaisesRegex(ValueError, "side_effects"):
            guard.evaluate_sprint_package_candidate_263(_contract(), candidate)


if __name__ == "__main__":
    unittest.main()
