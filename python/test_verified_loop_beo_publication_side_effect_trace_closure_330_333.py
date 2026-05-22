import copy
import unittest

from test_verified_loop_beo_publication_bounded_execution_kernel_329 import _broad_guard_327
from test_verified_loop_beo_publication_live_challenge_guard_313_315 import (
    _short_approve_guard_314,
)
from blk_system_development_authority_distinction_328 import (
    OPERATOR_CORRECTION_328,
    build_development_authority_distinction_328,
)
from verified_loop_beo_publication_approval_request_306_309 import hash_package
from verified_loop_beo_publication_bounded_execution_kernel_329 import (
    EXPECTED_329_EXECUTION_KERNEL_HASH,
    OPERATOR_DIRECTIVE_329,
    build_verified_loop_beo_publication_bounded_execution_kernel_329,
)
from verified_loop_beo_publication_live_challenge_guard_313_315 import (
    reconcile_verified_loop_beo_publication_live_challenge_guard_315,
)
from verified_loop_beo_publication_side_effect_trace_closure_330_333 import (
    BEO_ID_330,
    NEXT_FRONTIER_333,
    OPERATOR_DIRECTIVE_330,
    RUN_ID_330,
    RTM_TRACE_CLOSURE_ID_332,
    RTM_TRACE_CLOSURE_RUN_ID_332,
    execute_rtm_blk_link_trace_closure_332,
    execute_verified_loop_beo_publication_side_effect_package_330,
    reconcile_verified_loop_beo_publication_finality_331,
    reconcile_verified_loop_rtm_blk_link_trace_closure_333,
    validate_rtm_blk_link_trace_closure_332,
    validate_verified_loop_beo_publication_side_effect_package_330,
)


REQUESTED_AT_330 = "2026-05-22T10:00:00+10:00"
EXECUTED_AT_330 = "2026-05-22T10:02:00+10:00"
EXPIRES_AT_330 = "2026-05-22T10:30:00+10:00"
REQUESTED_AT_332 = "2026-05-22T10:05:00+10:00"
EXECUTED_AT_332 = "2026-05-22T10:07:00+10:00"
EXPIRES_AT_332 = "2026-05-22T10:45:00+10:00"


def _kernel_329():
    reconciliation = reconcile_verified_loop_beo_publication_live_challenge_guard_315(
        _short_approve_guard_314(),
    )
    distinction = build_development_authority_distinction_328(
        _broad_guard_327(),
        operator_correction=OPERATOR_CORRECTION_328,
    )
    return build_verified_loop_beo_publication_bounded_execution_kernel_329(
        reconciliation,
        distinction,
        operator_directive=OPERATOR_DIRECTIVE_329,
    )


def _publication_330():
    return execute_verified_loop_beo_publication_side_effect_package_330(
        _kernel_329(),
        operator_directive=OPERATOR_DIRECTIVE_330,
        requested_at=REQUESTED_AT_330,
        executed_at=EXECUTED_AT_330,
        expires_at=EXPIRES_AT_330,
        used_run_ids=(),
    )


def _reconciliation_331():
    return reconcile_verified_loop_beo_publication_finality_331(_publication_330())


def _trace_closure_332():
    return execute_rtm_blk_link_trace_closure_332(
        _reconciliation_331(),
        requested_at=REQUESTED_AT_332,
        executed_at=EXECUTED_AT_332,
        expires_at=EXPIRES_AT_332,
        used_run_ids=(),
    )


class VerifiedLoopBeoPublicationSideEffectTraceClosure330333Test(unittest.TestCase):
    def test_330_executes_one_exact_beo_metadata_package_with_receipt_chain(self):
        package = _publication_330()

        self.assertEqual(
            package["status"],
            "BLK_SYSTEM_330_VERIFIED_LOOP_BEO_PUBLICATION_SIDE_EFFECT_PACKAGE_EXECUTED",
        )
        self.assertIn(
            "BLK_SYSTEM_330_VERIFIED_LOOP_BEO_PUBLICATION_SIDE_EFFECT_PACKAGE_EXECUTED",
            package["markers"],
        )
        self.assertEqual(package["upstream_execution_kernel_hash"], EXPECTED_329_EXECUTION_KERNEL_HASH)
        self.assertEqual(package["run_id_consumed"], RUN_ID_330)
        self.assertEqual(
            package["run_id_replay_evidence"]["current_run_id"],
            RUN_ID_330,
        )
        self.assertEqual(package["run_id_replay_evidence"]["prior_consumed_run_ids"], [])
        self.assertFalse(package["run_id_replay_evidence"]["replayed"])
        self.assertEqual(package["official_beo_metadata"]["beo_id"], BEO_ID_330)
        self.assertEqual(
            package["official_beo_metadata"]["execution_kernel_hash"],
            EXPECTED_329_EXECUTION_KERNEL_HASH,
        )
        self.assertEqual(
            package["signature_receipt"]["execution_request_hash"],
            package["execution_request_hash"],
        )
        self.assertEqual(
            package["immutable_storage_receipt"]["signature_receipt_hash"],
            package["signature_receipt_hash"],
        )
        self.assertEqual(
            package["public_ledger_entry"]["immutable_storage_receipt_hash"],
            package["immutable_storage_receipt_hash"],
        )
        self.assertEqual(
            package["official_beo_metadata"]["public_ledger_entry_hash"],
            package["public_ledger_entry_hash"],
        )
        self.assertEqual(
            validate_verified_loop_beo_publication_side_effect_package_330(package),
            package,
        )

        side_effects = package["side_effects"]
        self.assertTrue(side_effects["run_id_consumed"])
        self.assertTrue(side_effects["beo_publication"])
        self.assertTrue(side_effects["authoritative_beo_publication"])
        self.assertTrue(side_effects["official_beo_metadata_recorded"])
        self.assertFalse(side_effects["reusable_beo_publication"])
        self.assertFalse(side_effects["signature_generated"])
        self.assertFalse(side_effects["immutable_storage_written"])
        self.assertFalse(side_effects["public_ledger_mutated"])
        self.assertFalse(side_effects["rtm_generation"])
        self.assertFalse(side_effects["production_blk_link"])
        self.assertFalse(side_effects["protected_body_access"])

    def test_330_rejects_kernel_mismatch_replay_and_adjacent_authority_laundering(self):
        kernel = _kernel_329()
        forged_kernel = copy.deepcopy(kernel)
        forged_kernel["execution_kernel_hash"] = hash_package(
            {
                key: value
                for key, value in forged_kernel.items()
                if key != "execution_kernel_hash"
            }
        )
        forged_kernel["execution_prerequisites"]["expired_or_prior_challenge_reuse_allowed"] = True
        with self.assertRaisesRegex(ValueError, "kernel|canonical|prerequisites"):
            execute_verified_loop_beo_publication_side_effect_package_330(
                forged_kernel,
                operator_directive=OPERATOR_DIRECTIVE_330,
                requested_at=REQUESTED_AT_330,
                executed_at=EXECUTED_AT_330,
                expires_at=EXPIRES_AT_330,
                used_run_ids=(),
            )

        with self.assertRaisesRegex(ValueError, "operator_directive|forbidden authority wording|mismatch"):
            execute_verified_loop_beo_publication_side_effect_package_330(
                kernel,
                operator_directive="publishBEO now and RTMGenerated through productionBlkLink",
                requested_at=REQUESTED_AT_330,
                executed_at=EXECUTED_AT_330,
                expires_at=EXPIRES_AT_330,
                used_run_ids=(),
            )

        with self.assertRaisesRegex(ValueError, "replay|already consumed"):
            execute_verified_loop_beo_publication_side_effect_package_330(
                kernel,
                operator_directive=OPERATOR_DIRECTIVE_330,
                requested_at=REQUESTED_AT_330,
                executed_at=EXECUTED_AT_330,
                expires_at=EXPIRES_AT_330,
                used_run_ids=(RUN_ID_330,),
            )

        package = _publication_330()
        tampered = copy.deepcopy(package)
        tampered["side_effects"]["reusable_beo_publication"] = True
        tampered["execution_package_hash"] = hash_package(
            {key: value for key, value in tampered.items() if key != "execution_package_hash"}
        )
        with self.assertRaisesRegex(ValueError, "side_effects"):
            validate_verified_loop_beo_publication_side_effect_package_330(tampered)

        replayed = copy.deepcopy(package)
        replayed["run_id_consumed"] = "RUN-BLK-SYSTEM-330-REPLAYED"
        replayed["execution_package_hash"] = hash_package(
            {key: value for key, value in replayed.items() if key != "execution_package_hash"}
        )
        with self.assertRaisesRegex(ValueError, "run_id|request"):
            validate_verified_loop_beo_publication_side_effect_package_330(replayed)

    def test_331_reconciles_official_beo_metadata_for_downstream_trace_closure(self):
        package = _publication_330()
        reconciliation = reconcile_verified_loop_beo_publication_finality_331(package)

        self.assertEqual(
            reconciliation["status"],
            "BLK_SYSTEM_331_VERIFIED_LOOP_BEO_PUBLICATION_FINALITY_RECONCILED",
        )
        self.assertEqual(reconciliation["execution_package_hash"], package["execution_package_hash"])
        self.assertEqual(reconciliation["official_beo_metadata_hash"], package["official_beo_metadata_hash"])
        self.assertTrue(reconciliation["side_effects"]["rtm_blk_link_trace_closure_input_ready"])
        self.assertFalse(reconciliation["side_effects"]["reusable_beo_publication"])
        self.assertFalse(reconciliation["side_effects"]["rtm_generation"])
        self.assertFalse(reconciliation["side_effects"]["production_blk_link"])

    def test_332_closes_rtm_blk_link_trace_using_only_official_beo_metadata(self):
        reconciliation = _reconciliation_331()
        package = execute_rtm_blk_link_trace_closure_332(
            reconciliation,
            requested_at=REQUESTED_AT_332,
            executed_at=EXECUTED_AT_332,
            expires_at=EXPIRES_AT_332,
            used_run_ids=(),
        )

        self.assertEqual(
            package["status"],
            "BLK_SYSTEM_332_RTM_BLK_LINK_TRACE_CLOSURE_RECORDED_FROM_OFFICIAL_BEO_METADATA",
        )
        self.assertEqual(package["trace_closure_id"], RTM_TRACE_CLOSURE_ID_332)
        self.assertEqual(
            package["run_id_replay_evidence"]["current_run_id"],
            RTM_TRACE_CLOSURE_RUN_ID_332,
        )
        self.assertEqual(package["run_id_replay_evidence"]["prior_consumed_run_ids"], [])
        self.assertFalse(package["run_id_replay_evidence"]["replayed"])
        self.assertEqual(package["official_beo_metadata_hash"], reconciliation["official_beo_metadata_hash"])
        self.assertEqual(
            package["trace_closure_record"]["official_beo_metadata_hash"],
            reconciliation["official_beo_metadata_hash"],
        )
        self.assertEqual(
            package["trace_closure_record"]["beo_finality_record_hash"],
            reconciliation["beo_finality_record_hash"],
        )
        self.assertEqual(
            validate_rtm_blk_link_trace_closure_332(package),
            package,
        )

        side_effects = package["side_effects"]
        self.assertTrue(side_effects["rtm_blk_link_trace_closure_recorded"])
        self.assertTrue(side_effects["traceability_loop_closed"])
        self.assertFalse(side_effects["runtime_rtm_generation"])
        self.assertFalse(side_effects["reusable_rtm_generation"])
        self.assertFalse(side_effects["reusable_production_blk_link"])
        self.assertFalse(side_effects["drift_rejection"])
        self.assertFalse(side_effects["coverage_truth"])
        self.assertFalse(side_effects["active_vault_comparison"])
        self.assertFalse(side_effects["protected_body_access"])

    def test_332_rejects_tampered_publication_metadata_or_forbidden_trace_side_effects(self):
        reconciliation = _reconciliation_331()
        forged_reconciliation = copy.deepcopy(reconciliation)
        forged_reconciliation["official_beo_metadata"]["beo_id"] = "BEO-FORGED"
        forged_reconciliation["reconciliation_hash"] = hash_package(
            {
                key: value
                for key, value in forged_reconciliation.items()
                if key != "reconciliation_hash"
            }
        )
        with self.assertRaisesRegex(ValueError, "reconciliation|metadata|canonical"):
            execute_rtm_blk_link_trace_closure_332(
                forged_reconciliation,
                requested_at=REQUESTED_AT_332,
                executed_at=EXECUTED_AT_332,
                expires_at=EXPIRES_AT_332,
                used_run_ids=(),
            )

        with self.assertRaisesRegex(ValueError, "replay|already consumed"):
            execute_rtm_blk_link_trace_closure_332(
                reconciliation,
                requested_at=REQUESTED_AT_332,
                executed_at=EXECUTED_AT_332,
                expires_at=EXPIRES_AT_332,
                used_run_ids=(RTM_TRACE_CLOSURE_RUN_ID_332,),
            )

        package = _trace_closure_332()
        tampered = copy.deepcopy(package)
        tampered["side_effects"]["runtime_rtm_generation"] = True
        tampered["trace_closure_package_hash"] = hash_package(
            {key: value for key, value in tampered.items() if key != "trace_closure_package_hash"}
        )
        with self.assertRaisesRegex(ValueError, "side_effects"):
            validate_rtm_blk_link_trace_closure_332(tampered)

    def test_333_reconciles_closed_traceability_without_granting_reusable_authority(self):
        trace_package = _trace_closure_332()
        reconciliation = reconcile_verified_loop_rtm_blk_link_trace_closure_333(trace_package)

        self.assertEqual(
            reconciliation["status"],
            "BLK_SYSTEM_333_RTM_BLK_LINK_TRACE_CLOSURE_RECONCILED",
        )
        self.assertEqual(reconciliation["trace_closure_package_hash"], trace_package["trace_closure_package_hash"])
        self.assertEqual(reconciliation["next_frontier"], NEXT_FRONTIER_333)
        self.assertTrue(reconciliation["side_effects"]["traceability_loop_closed"])
        self.assertFalse(reconciliation["side_effects"]["reusable_production_blk_link"])
        self.assertFalse(reconciliation["side_effects"]["runtime_rtm_generation"])
        self.assertFalse(reconciliation["side_effects"]["coverage_truth"])
        self.assertFalse(reconciliation["side_effects"]["protected_body_access"])


if __name__ == "__main__":
    unittest.main()
