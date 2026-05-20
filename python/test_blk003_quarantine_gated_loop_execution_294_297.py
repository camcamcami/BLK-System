import copy
import unittest
from pathlib import Path

from blk_authority_smuggling import scan_for_authority_laundering
from test_blk003_loop_request_path_290_293 import build_documented_request_path
from blk003_quarantine_gated_loop_execution_294_297 import (
    Blk003LoopExecutionPackageValidationError,
    NEXT_FRONTIER_297,
    build_exact_loop_execution_package_294,
    validate_exact_loop_execution_package_294,
    build_fresh_execution_preflight_295,
    validate_fresh_execution_preflight_295,
    record_quarantine_bounded_loop_execution_296,
    validate_quarantine_bounded_loop_execution_296,
    reconcile_exact_loop_execution_package_297,
    validate_exact_loop_execution_reconciliation_297,
    hash_package,
)

ROOT = Path(__file__).resolve().parents[1]
BLK125 = ROOT / "docs" / "BLK-125_exact-quarantine-gated-blk003-loop-execution-contract.md"

_REQUESTED_AT = "2026-05-21T10:00:00+10:00"
_EXPIRES_AT = "2026-05-21T11:00:00+10:00"
_EVALUATED_AT = "2026-05-21T10:05:00+10:00"
_COMPLETED_AT = "2026-05-21T10:20:00+10:00"
_EXECUTION_PACKAGE_ID = "EXECUTION-PACKAGE-BLK-SYSTEM-294-001"
_RUN_ID = "RUN-BLK-SYSTEM-296-EXACT-LOOP-001"


def _ready_chain():
    upstream, contract, binding, request_preflight, request_reconciliation = build_documented_request_path()
    return upstream, contract, binding, request_preflight, request_reconciliation


def _package_294():
    upstream, contract, binding, request_preflight, request_reconciliation = _ready_chain()
    package = build_exact_loop_execution_package_294(
        contract,
        binding,
        request_preflight,
        request_reconciliation,
        upstream["approval_contract"],
        upstream["quarantine"],
        upstream["interaction"],
        upstream["gate"],
        execution_package_id=_EXECUTION_PACKAGE_ID,
        run_id=_RUN_ID,
        requested_at=_REQUESTED_AT,
        expires_at=_EXPIRES_AT,
    )
    return upstream, contract, binding, request_preflight, request_reconciliation, package


def _preflight_295(package=None):
    if package is None:
        upstream, contract, binding, request_preflight, request_reconciliation, package = _package_294()
    else:
        upstream, contract, binding, request_preflight, request_reconciliation = _ready_chain()
    preflight = build_fresh_execution_preflight_295(
        package,
        contract,
        binding,
        request_preflight,
        request_reconciliation,
        upstream["approval_contract"],
        upstream["quarantine"],
        upstream["interaction"],
        upstream["gate"],
        observed_target_hash=binding["target_hash"],
        observed_trusted_root_hash=binding["trusted_root_hash"],
        observed_trusted_workdir_hash=binding["trusted_workdir_hash"],
        observed_private_bwrap_descriptor_hash=request_preflight["private_bwrap_descriptor_hash"],
        observed_validation_profile_hash=request_preflight["validation_profile_hash"],
        sandbox_profile_state="PRIVATE_BWRAP_DESCRIPTOR_READY",
        worktree_state="CLEAN_EXACT_TARGET_WORKTREE",
        evaluated_at=_EVALUATED_AT,
    )
    return upstream, contract, binding, request_preflight, request_reconciliation, package, preflight


def _runtime_report(**overrides):
    report = {
        "run_id": _RUN_ID,
        "quarantine_workspace_id": "QUARANTINE-BLK-SYSTEM-296-EXACT-LOOP-001",
        "attempts": [
            {
                "attempt": 1,
                "status": "FAILED_RETRYABLE",
                "started_at": "2026-05-21T10:06:00+10:00",
                "completed_at": "2026-05-21T10:10:00+10:00",
                "report_hash": "sha256:" + "1" * 64,
            },
            {
                "attempt": 2,
                "status": "SUCCEEDED",
                "started_at": "2026-05-21T10:11:00+10:00",
                "completed_at": _COMPLETED_AT,
                "report_hash": "sha256:" + "2" * 64,
            },
        ],
        "final_result": "SUCCEEDED",
        "dispatcher_report_hash": "sha256:" + "3" * 64,
        "result_hash": "sha256:" + "4" * 64,
        "post_execution_target_hash": "sha256:" + "2" * 64,
        "cleanup_evidence_hash": "sha256:" + "5" * 64,
        "beo_draft_hash": "sha256:" + "6" * 64,
        "completed_at": _COMPLETED_AT,
        "durable_target_source_git_mutation": False,
        "source_git_commit_created": False,
        "beo_closeout_executed": False,
        "beo_publication_performed": False,
        "rtm_generation_performed": False,
        "production_blk_link_performed": False,
        "package_manager_called": False,
        "network_model_browser_cyber_tooling": False,
        "production_isolation_claim": False,
        "reusable_codex_dispatch": False,
        "broad_blk_pipe_dispatch": False,
        "approval_reuse": False,
        "production_blk_test_mcp": False,
        "relay_network_runtime_created": False,
        "message_dispatch_performed": False,
        "protected_body_access": False,
        "runtime_tooling_performed": False,
        "prior_consumed_run_ids": [],
        "consumed_run_ids": [_RUN_ID],
    }
    report.update(overrides)
    return report


def _execution_record_296():
    upstream, contract, binding, request_preflight, request_reconciliation, package, preflight = _preflight_295()
    report = _runtime_report(post_execution_target_hash=binding["target_hash"])
    record = record_quarantine_bounded_loop_execution_296(
        package,
        preflight,
        contract,
        binding,
        request_preflight,
        request_reconciliation,
        upstream["approval_contract"],
        upstream["quarantine"],
        upstream["interaction"],
        upstream["gate"],
        runtime_report=report,
    )
    return upstream, contract, binding, request_preflight, request_reconciliation, package, preflight, record


class Blk003QuarantineGatedLoopExecution294To297Test(unittest.TestCase):
    def test_294_builds_exact_execution_package_from_revalidated_ready_request_path(self):
        upstream, contract, binding, request_preflight, request_reconciliation, package = _package_294()

        self.assertEqual(package["status"], "EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_PACKAGE_READY")
        self.assertIn(
            "BLK_SYSTEM_294_EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_PACKAGE_READY",
            package["markers"],
        )
        self.assertEqual(package["request_path_reconciliation_hash"], request_reconciliation["reconciliation_hash"])
        self.assertEqual(package["route_request_binding_hash"], binding["route_request_binding_hash"])
        self.assertEqual(package["target_hash"], binding["target_hash"])
        self.assertEqual(package["failure_ceiling"], 3)
        self.assertIn("STOP_AFTER_THREE_FAILED_ATTEMPTS", package["stop_conditions"])
        self.assertTrue(package["beo_draft_required"])
        self.assertFalse(package["beo_closeout_execution_allowed"])
        self.assertFalse(package["side_effects"]["durable_target_source_git_mutation"])
        self.assertFalse(package["side_effects"]["reusable_codex_dispatch"])
        self.assertEqual(
            validate_exact_loop_execution_package_294(
                package,
                contract,
                binding,
                request_preflight,
                request_reconciliation,
                upstream["approval_contract"],
                upstream["quarantine"],
                upstream["interaction"],
                upstream["gate"],
            ),
            package,
        )

        blocked_reconciliation = copy.deepcopy(request_reconciliation)
        blocked_reconciliation["reconciled_state"] = "REQUEST_PATH_BLOCKED_GATE_OR_TARGET_DRIFT"
        blocked_reconciliation["reconciliation_hash"] = hash_package(
            {key: value for key, value in blocked_reconciliation.items() if key != "reconciliation_hash"}
        )
        with self.assertRaisesRegex(Blk003LoopExecutionPackageValidationError, "request path.*ready"):
            build_exact_loop_execution_package_294(
                contract,
                binding,
                request_preflight,
                blocked_reconciliation,
                upstream["approval_contract"],
                upstream["quarantine"],
                upstream["interaction"],
                upstream["gate"],
                execution_package_id="EXECUTION-PACKAGE-BLK-SYSTEM-294-BLOCKED",
                run_id="RUN-BLK-SYSTEM-296-BLOCKED-001",
                requested_at=_REQUESTED_AT,
                expires_at=_EXPIRES_AT,
            )

    def test_295_rechecks_fresh_target_worktree_sandbox_and_blocks_drift_without_dispatch(self):
        upstream, contract, binding, request_preflight, request_reconciliation, package, preflight = _preflight_295()

        self.assertEqual(preflight["status"], "FRESH_TARGET_WORKTREE_SANDBOX_PREFLIGHT_READY")
        self.assertIn("BLK_SYSTEM_295_FRESH_TARGET_WORKTREE_SANDBOX_PREFLIGHT_READY", preflight["markers"])
        self.assertEqual(preflight["preflight_result"], "EXACT_LOOP_EXECUTION_PREFLIGHT_READY")
        self.assertTrue(preflight["execution_allowed"])
        self.assertTrue(preflight["target_hash_rechecked"])
        self.assertTrue(preflight["trusted_workdir_hash_rechecked"])
        self.assertTrue(preflight["sandbox_descriptor_rechecked"])
        self.assertFalse(preflight["runtime_dispatch_performed"])
        self.assertFalse(preflight["side_effects"]["durable_target_source_git_mutation"])
        self.assertEqual(
            validate_fresh_execution_preflight_295(
                preflight,
                package,
                contract,
                binding,
                request_preflight,
                request_reconciliation,
                upstream["approval_contract"],
                upstream["quarantine"],
                upstream["interaction"],
                upstream["gate"],
            ),
            preflight,
        )

        stale = build_fresh_execution_preflight_295(
            package,
            contract,
            binding,
            request_preflight,
            request_reconciliation,
            upstream["approval_contract"],
            upstream["quarantine"],
            upstream["interaction"],
            upstream["gate"],
            observed_target_hash="sha256:" + "f" * 64,
            observed_trusted_root_hash=binding["trusted_root_hash"],
            observed_trusted_workdir_hash=binding["trusted_workdir_hash"],
            observed_private_bwrap_descriptor_hash=request_preflight["private_bwrap_descriptor_hash"],
            observed_validation_profile_hash=request_preflight["validation_profile_hash"],
            sandbox_profile_state="PRIVATE_BWRAP_DESCRIPTOR_READY",
            worktree_state="CLEAN_EXACT_TARGET_WORKTREE",
            evaluated_at=_EVALUATED_AT,
        )
        self.assertEqual(stale["preflight_result"], "EXACT_LOOP_EXECUTION_BLOCKED_BY_TARGET_HASH_DRIFT")
        self.assertFalse(stale["execution_allowed"])

        unsafe_sandbox = build_fresh_execution_preflight_295(
            package,
            contract,
            binding,
            request_preflight,
            request_reconciliation,
            upstream["approval_contract"],
            upstream["quarantine"],
            upstream["interaction"],
            upstream["gate"],
            observed_target_hash=binding["target_hash"],
            observed_trusted_root_hash=binding["trusted_root_hash"],
            observed_trusted_workdir_hash=binding["trusted_workdir_hash"],
            observed_private_bwrap_descriptor_hash=request_preflight["private_bwrap_descriptor_hash"],
            observed_validation_profile_hash=request_preflight["validation_profile_hash"],
            sandbox_profile_state="PRIVATE_BWRAP_DESCRIPTOR_MISSING",
            worktree_state="CLEAN_EXACT_TARGET_WORKTREE",
            evaluated_at=_EVALUATED_AT,
        )
        self.assertEqual(unsafe_sandbox["preflight_result"], "EXACT_LOOP_EXECUTION_BLOCKED_BY_WORKTREE_OR_SANDBOX")
        self.assertFalse(unsafe_sandbox["execution_allowed"])

        with self.assertRaisesRegex(Blk003LoopExecutionPackageValidationError, "evaluated_at must be within"):
            build_fresh_execution_preflight_295(
                package,
                contract,
                binding,
                request_preflight,
                request_reconciliation,
                upstream["approval_contract"],
                upstream["quarantine"],
                upstream["interaction"],
                upstream["gate"],
                observed_target_hash=binding["target_hash"],
                observed_trusted_root_hash=binding["trusted_root_hash"],
                observed_trusted_workdir_hash=binding["trusted_workdir_hash"],
                observed_private_bwrap_descriptor_hash=request_preflight["private_bwrap_descriptor_hash"],
                observed_validation_profile_hash=request_preflight["validation_profile_hash"],
                sandbox_profile_state="PRIVATE_BWRAP_DESCRIPTOR_READY",
                worktree_state="CLEAN_EXACT_TARGET_WORKTREE",
                evaluated_at="2026-05-21T12:00:00+10:00",
            )

    def test_296_records_one_quarantine_bounded_loop_execution_with_failure_ceiling_and_no_durable_mutation(self):
        upstream, contract, binding, request_preflight, request_reconciliation, package, preflight, record = _execution_record_296()

        self.assertEqual(record["status"], "QUARANTINE_BOUNDED_BLK003_LOOP_EXECUTION_RECORDED")
        self.assertIn(
            "BLK_SYSTEM_296_QUARANTINE_BOUNDED_BLK003_LOOP_EXECUTION_RECORDED",
            record["markers"],
        )
        self.assertEqual(record["execution_package_hash"], package["execution_package_hash"])
        self.assertEqual(record["fresh_preflight_hash"], preflight["fresh_preflight_hash"])
        self.assertEqual(record["run_id"], _RUN_ID)
        self.assertEqual(record["attempt_count"], 2)
        self.assertEqual(record["failure_ceiling"], 3)
        self.assertEqual(record["final_result"], "SUCCEEDED")
        self.assertTrue(record["target_hash_preserved"])
        self.assertTrue(record["beo_draft_recorded"])
        self.assertFalse(record["beo_closeout_execution_performed"])
        self.assertTrue(record["side_effects"]["quarantine_workspace_mutation_recorded"])
        self.assertFalse(record["side_effects"]["durable_target_source_git_mutation"])
        self.assertFalse(record["side_effects"]["beo_closeout_execution"])
        self.assertEqual(
            validate_quarantine_bounded_loop_execution_296(
                record,
                package,
                preflight,
                contract,
                binding,
                request_preflight,
                request_reconciliation,
                upstream["approval_contract"],
                upstream["quarantine"],
                upstream["interaction"],
                upstream["gate"],
            ),
            record,
        )

        too_many_attempts = _runtime_report(
            post_execution_target_hash=binding["target_hash"],
            attempts=[
                {
                    "attempt": number,
                    "status": "FAILED_RETRYABLE" if number < 4 else "SUCCEEDED",
                    "started_at": f"2026-05-21T10:1{number}:00+10:00",
                    "completed_at": f"2026-05-21T10:1{number}:30+10:00",
                    "report_hash": "sha256:" + format(number, "x") * 64,
                }
                for number in range(1, 5)
            ],
        )
        with self.assertRaisesRegex(Blk003LoopExecutionPackageValidationError, "failure ceiling"):
            record_quarantine_bounded_loop_execution_296(
                package,
                preflight,
                contract,
                binding,
                request_preflight,
                request_reconciliation,
                upstream["approval_contract"],
                upstream["quarantine"],
                upstream["interaction"],
                upstream["gate"],
                runtime_report=too_many_attempts,
            )

        durable_mutation = _runtime_report(
            post_execution_target_hash=binding["target_hash"],
            durable_target_source_git_mutation=True,
        )
        with self.assertRaisesRegex(Blk003LoopExecutionPackageValidationError, "durable target/source/Git mutation"):
            record_quarantine_bounded_loop_execution_296(
                package,
                preflight,
                contract,
                binding,
                request_preflight,
                request_reconciliation,
                upstream["approval_contract"],
                upstream["quarantine"],
                upstream["interaction"],
                upstream["gate"],
                runtime_report=durable_mutation,
            )

        terminal_then_success = _runtime_report(
            post_execution_target_hash=binding["target_hash"],
            attempts=[
                {
                    "attempt": 1,
                    "status": "FAILED_TERMINAL",
                    "started_at": "2026-05-21T10:06:00+10:00",
                    "completed_at": "2026-05-21T10:07:00+10:00",
                    "report_hash": "sha256:" + "7" * 64,
                },
                {
                    "attempt": 2,
                    "status": "SUCCEEDED",
                    "started_at": "2026-05-21T10:08:00+10:00",
                    "completed_at": "2026-05-21T10:09:00+10:00",
                    "report_hash": "sha256:" + "8" * 64,
                },
            ],
        )
        with self.assertRaisesRegex(Blk003LoopExecutionPackageValidationError, "terminal failure"):
            record_quarantine_bounded_loop_execution_296(
                package,
                preflight,
                contract,
                binding,
                request_preflight,
                request_reconciliation,
                upstream["approval_contract"],
                upstream["quarantine"],
                upstream["interaction"],
                upstream["gate"],
                runtime_report=terminal_then_success,
            )

        reversed_time = _runtime_report(
            post_execution_target_hash=binding["target_hash"],
            attempts=[
                {
                    "attempt": 1,
                    "status": "SUCCEEDED",
                    "started_at": "2026-05-21T10:10:00+10:00",
                    "completed_at": "2026-05-21T10:09:00+10:00",
                    "report_hash": "sha256:" + "9" * 64,
                }
            ],
        )
        with self.assertRaisesRegex(Blk003LoopExecutionPackageValidationError, "completed_at must be after started_at"):
            record_quarantine_bounded_loop_execution_296(
                package,
                preflight,
                contract,
                binding,
                request_preflight,
                request_reconciliation,
                upstream["approval_contract"],
                upstream["quarantine"],
                upstream["interaction"],
                upstream["gate"],
                runtime_report=reversed_time,
            )

        replay = _runtime_report(
            post_execution_target_hash=binding["target_hash"],
            prior_consumed_run_ids=[_RUN_ID],
            consumed_run_ids=[_RUN_ID],
        )
        with self.assertRaisesRegex(Blk003LoopExecutionPackageValidationError, "run_id replay"):
            record_quarantine_bounded_loop_execution_296(
                package,
                preflight,
                contract,
                binding,
                request_preflight,
                request_reconciliation,
                upstream["approval_contract"],
                upstream["quarantine"],
                upstream["interaction"],
                upstream["gate"],
                runtime_report=replay,
            )

    def test_296_rejects_blocked_preflight_and_authority_laundering_runtime_report(self):
        upstream, contract, binding, request_preflight, request_reconciliation, package = _package_294()
        blocked_preflight = build_fresh_execution_preflight_295(
            package,
            contract,
            binding,
            request_preflight,
            request_reconciliation,
            upstream["approval_contract"],
            upstream["quarantine"],
            upstream["interaction"],
            upstream["gate"],
            observed_target_hash="sha256:" + "f" * 64,
            observed_trusted_root_hash=binding["trusted_root_hash"],
            observed_trusted_workdir_hash=binding["trusted_workdir_hash"],
            observed_private_bwrap_descriptor_hash=request_preflight["private_bwrap_descriptor_hash"],
            observed_validation_profile_hash=request_preflight["validation_profile_hash"],
            sandbox_profile_state="PRIVATE_BWRAP_DESCRIPTOR_READY",
            worktree_state="CLEAN_EXACT_TARGET_WORKTREE",
            evaluated_at=_EVALUATED_AT,
        )
        with self.assertRaisesRegex(Blk003LoopExecutionPackageValidationError, "preflight is not ready"):
            record_quarantine_bounded_loop_execution_296(
                package,
                blocked_preflight,
                contract,
                binding,
                request_preflight,
                request_reconciliation,
                upstream["approval_contract"],
                upstream["quarantine"],
                upstream["interaction"],
                upstream["gate"],
                runtime_report=_runtime_report(post_execution_target_hash=binding["target_hash"]),
            )

        _u, _c, _b, _rp, _rr, package, preflight = _preflight_295()
        laundering_report = _runtime_report(
            post_execution_target_hash=binding["target_hash"],
            quarantine_workspace_id="QUARANTINE-BLK-SYSTEM-296-APPROVED-FOR-LIVE-EXECUTION",
        )
        with self.assertRaisesRegex(Blk003LoopExecutionPackageValidationError, "authority wording"):
            record_quarantine_bounded_loop_execution_296(
                package,
                preflight,
                contract,
                binding,
                request_preflight,
                request_reconciliation,
                upstream["approval_contract"],
                upstream["quarantine"],
                upstream["interaction"],
                upstream["gate"],
                runtime_report=laundering_report,
            )

    def test_297_reconciles_exact_loop_execution_and_names_blk_test_verification_frontier(self):
        upstream, contract, binding, request_preflight, request_reconciliation, package, preflight, record = _execution_record_296()

        reconciliation = reconcile_exact_loop_execution_package_297(
            package,
            preflight,
            record,
            contract,
            binding,
            request_preflight,
            request_reconciliation,
            upstream["approval_contract"],
            upstream["quarantine"],
            upstream["interaction"],
            upstream["gate"],
        )

        self.assertEqual(reconciliation["status"], "EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_RECONCILED")
        self.assertIn(
            "BLK_SYSTEM_297_EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_RECONCILED",
            reconciliation["markers"],
        )
        self.assertEqual(reconciliation["execution_record_hash"], record["execution_record_hash"])
        self.assertEqual(reconciliation["final_result"], "SUCCEEDED")
        self.assertEqual(reconciliation["next_frontier"], NEXT_FRONTIER_297)
        self.assertEqual(
            reconciliation["next_frontier"],
            "NEXT_FRONTIER_EXACT_BLK_TEST_ORACLE_VERIFICATION_AFTER_LOOP_EXECUTION_REQUIRED_NOT_GRANTED",
        )
        self.assertFalse(reconciliation["side_effects"]["reusable_codex_dispatch"])
        self.assertFalse(reconciliation["side_effects"]["beo_closeout_execution"])
        self.assertFalse(reconciliation["side_effects"]["rtm_generation"])
        self.assertEqual(
            validate_exact_loop_execution_reconciliation_297(
                reconciliation,
                package,
                preflight,
                record,
                contract,
                binding,
                request_preflight,
                request_reconciliation,
                upstream["approval_contract"],
                upstream["quarantine"],
                upstream["interaction"],
                upstream["gate"],
            ),
            reconciliation,
        )

        forged_record = copy.deepcopy(record)
        forged_record["post_execution_target_hash"] = "sha256:" + "f" * 64
        forged_record["target_hash_preserved"] = True
        forged_record["execution_record_hash"] = hash_package(
            {key: value for key, value in forged_record.items() if key != "execution_record_hash"}
        )
        with self.assertRaisesRegex(Blk003LoopExecutionPackageValidationError, "target hash"):
            reconcile_exact_loop_execution_package_297(
                package,
                preflight,
                forged_record,
                contract,
                binding,
                request_preflight,
                request_reconciliation,
                upstream["approval_contract"],
                upstream["quarantine"],
                upstream["interaction"],
                upstream["gate"],
            )

    def test_exact_marker_lists_block_nested_authority_marker_laundering(self):
        upstream, contract, binding, request_preflight, request_reconciliation, package, preflight, record = _execution_record_296()

        forged = copy.deepcopy(record)
        forged["markers"].append("REUSABLE_CODEX_DISPATCH_GRANTED")
        forged["execution_record_hash"] = hash_package(
            {key: value for key, value in forged.items() if key != "execution_record_hash"}
        )
        with self.assertRaisesRegex(Blk003LoopExecutionPackageValidationError, "markers mismatch|authority wording"):
            validate_quarantine_bounded_loop_execution_296(
                forged,
                package,
                preflight,
                contract,
                binding,
                request_preflight,
                request_reconciliation,
                upstream["approval_contract"],
                upstream["quarantine"],
                upstream["interaction"],
                upstream["gate"],
            )

    def test_blk125_contract_doc_makes_execution_boundary_review_obvious(self):
        self.assertTrue(BLK125.exists(), "BLK-125 loop execution contract doc is missing")
        text = BLK125.read_text()
        self.assertEqual(scan_for_authority_laundering(text, path=str(BLK125)), [])

        _upstream, contract, binding, request_preflight, request_reconciliation, package, preflight, record = _execution_record_296()
        reconciliation = reconcile_exact_loop_execution_package_297(
            package,
            preflight,
            record,
            contract,
            binding,
            request_preflight,
            request_reconciliation,
            _upstream["approval_contract"],
            _upstream["quarantine"],
            _upstream["interaction"],
            _upstream["gate"],
        )
        for marker in [
            "BLK-125 — Exact Quarantine-Gated BLK-003 Loop Execution Contract",
            "BLK_SYSTEM_294_EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_PACKAGE_READY",
            "BLK_SYSTEM_295_FRESH_TARGET_WORKTREE_SANDBOX_PREFLIGHT_READY",
            "BLK_SYSTEM_296_QUARANTINE_BOUNDED_BLK003_LOOP_EXECUTION_RECORDED",
            "BLK_SYSTEM_297_EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_RECONCILED",
            "NEXT_FRONTIER_EXACT_BLK_TEST_ORACLE_VERIFICATION_AFTER_LOOP_EXECUTION_REQUIRED_NOT_GRANTED",
            "no reusable Codex dispatch",
            "no durable target/source/Git mutation",
            "no BEO closeout execution",
            f"blk294_execution_package_hash={package['execution_package_hash']}",
            f"blk295_fresh_preflight_hash={preflight['fresh_preflight_hash']}",
            f"blk296_execution_record_hash={record['execution_record_hash']}",
            f"blk297_reconciliation_hash={reconciliation['reconciliation_hash']}",
        ]:
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
