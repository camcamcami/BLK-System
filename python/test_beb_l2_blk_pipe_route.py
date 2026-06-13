import contextlib
import hashlib
import io
import json
import os
import shutil
import stat
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

from beb_l2_blk_pipe_route import (
    RouteError,
    archive_k2_route_evidence,
    build_hostile_review_record,
    build_clean_worktree_drop_manifest,
    build_default_clean_worktree_retarget_plan,
    build_ignored_residue_cleanup_plan,
    build_kuronode_codex_engine_args,
    build_route_commit_message,
    derive_matching_beo_id,
    dispatch_inbox_once,
    evaluate_remediation_route_policy,
    load_fallback_authorization_record,
    main as route_main,
    preflight_drop_file,
    prepare_beb_l2_drop_package,
    process_drop_file,
    evaluate_route_closeout_gate,
    scan_final_beo_closeout_placeholders,
    scan_k2_final_closeout_artifacts,
    scan_repo_local_hygiene,
    write_fallback_authorization_record,
)
from blk_pipe_adapter import BlkPipeAdapter


TRACE_ARTIFACTS = [
    {"kind": "REQ", "id": "REQ-222", "version_hash": "sha256:" + "2" * 64},
]
TARGET_HASH = "a" * 40
CALLER_OBJECT_PROFILE = "kuronode-caller-object-control-plane-v1"
RENDERER_PUBLIC_SURFACE_PROFILE = "kuronode-renderer-public-surface-v1"
AGENT_A_PROMOTION_REQUEST_PROFILE = "kuronode-agent-a-promotion-request-v1"
CALLER_OBJECT_REQUIRED_PROBES = (
    "KCP-001",
    "KCP-002",
    "KCP-003",
    "KCP-004",
    "KCP-005",
    "KCP-006",
    "KCP-007",
    "KCP-008",
    "KCP-009",
    "KCP-010",
    "KCP-011",
    "KCP-012",
)
RENDERER_PUBLIC_SURFACE_REQUIRED_PROBES = (
    "KRP-001",
    "KRP-002",
    "KRP-003",
    "KRP-004",
    "KRP-005",
    "KRP-006",
    "KRP-007",
    "KRP-008",
)
AGENT_A_PROMOTION_REQUEST_REQUIRED_PROBES = (
    "KAPR-001",
    "KAPR-002",
    "KAPR-003",
    "KAPR-004",
    "KAPR-005",
    "KAPR-006",
    "KAPR-007",
    "KAPR-008",
    "KAPR-009",
    "KAPR-010",
)


class FakeAdapter:
    def __init__(self):
        self.calls = []

    def execute_sprint(self, **kwargs):
        self.calls.append(kwargs)
        return {"status": "SUCCESS", "commit_hash": "abc123"}


class BebL2BlkPipeRouteTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        self.work_dir = self.root / "workspace" / "kuronode"
        self.work_dir.mkdir(parents=True)
        self.beb_path = self.root / "BEB_222.md"
        self.l2_path = self.root / "L2_222.md"
        self.drop_path = self.root / "drop.json"
        self.beb_path.write_text(
            "---\n"
            "beb_id: \"BEB_222\"\n"
            "l2_id: \"L2_222\"\n"
            "trace_artifacts:\n"
            "  - kind: \"REQ\"\n"
            "    id: \"REQ-222\"\n"
            "    version_hash: \"sha256:2222222222222222222222222222222222222222222222222222222222222222\"\n"
            "---\n"
            "# BEB 222\n"
        )
        self.l2_path.write_text(
            "L2_ID: L2_222\n"
            "BEB_ID: BEB_222\n"
            "MODEL: gpt-5.5\n"
            "Implement the exact bounded Kuronode task through Codex.\n"
        )
        self.write_drop()

    def sha(self, path: Path) -> str:
        return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()

    def route_kwargs(self):
        return {
            "allowed_work_dirs": [self.work_dir],
            "trusted_roots": [self.root],
            "approved_drop_sha256": self.sha(self.drop_path),
        }

    def process(self, adapter):
        return process_drop_file(self.drop_path, adapter=adapter, **self.route_kwargs())

    def successful_route_summary(self, **overrides):
        summary = {
            "status": "SUCCESS",
            "exit_code": 0,
            "beb_id": "BEB-K2-023",
            "beo_id": "BEO-K2-023",
            "l2_id": "L2-K2-023",
            "target_hash": "1" * 40,
            "commit_hash": "2" * 40,
            "drop_manifest_sha256": "sha256:" + "3" * 64,
            "engine_logs_bytes": 128,
            "final_message_bytes": 256,
            "validation_log_count": 1,
        }
        summary.update(overrides)
        if "route_summary_artifact_path" not in summary and "route_summary_artifact_sha256" not in summary:
            artifact_bytes = json.dumps(summary, sort_keys=True, separators=(",", ":")).encode("utf-8")
            artifact_digest = hashlib.sha256(artifact_bytes).hexdigest()
            artifact_dir = self.root / "artifacts" / "route-summaries" / str(summary.get("beo_id") or "unknown")
            artifact_dir.mkdir(parents=True, exist_ok=True)
            artifact_path = artifact_dir / f"{artifact_digest[:16]}.json"
            artifact_path.write_bytes(artifact_bytes)
            summary["route_summary_artifact_path"] = str(artifact_path)
            summary["route_summary_artifact_sha256"] = self.sha(artifact_path)
        return summary

    def root_cause_review_evidence(self, **overrides):
        review_path = self.root / "docs" / "root-cause-review.md"
        review_path.parent.mkdir(parents=True, exist_ok=True)
        review_path.write_text("# Root Cause Review\n\nScope decision: continue with root cause bound.\n")
        evidence = {
            "review_path": str(review_path),
            "review_sha256": self.sha(review_path),
            "scope_decision": "continue_with_root_cause_bound",
        }
        evidence.update(overrides)
        return evidence

    def failed_route_summary(self, **overrides):
        summary = {
            "status": "GIT_DIRTY",
            "exit_code": 7,
            "beb_id": "BEB-K2-024",
            "beo_id": "BEO-K2-024",
            "l2_id": "L2-K2-024",
            "target_hash": "4" * 40,
            "commit_hash": "",
            "drop_manifest_sha256": "sha256:" + "5" * 64,
            "engine_logs_bytes": 0,
            "final_message_bytes": 0,
            "validation_log_count": 0,
        }
        summary.update(overrides)
        return summary

    def valid_fallback_authorization(self, **overrides):
        authorization = {
            "fallback_authorized": True,
            "fallback_auth_id": "FALLBACK-AUTH-K2-024",
            "authorization_scope": "ONE_OFF_EXTERNAL_CODEX_FALLBACK",
            "authorized_by": "operator",
            "authorized_at": "2026-06-13T19:00:00+10:00",
            "reason": "ENGINE_TIMEOUT",
            "route_summary_path": "artifacts/kuronode-v2/BEO-K2-024/route-summary.json",
            "route_summary_sha256": "sha256:" + "6" * 64,
            "route_failure_status": "ENGINE_TIMEOUT",
            "target_hash": "4" * 40,
            "fallback_worktree": "/tmp/blk-system-fallbacks/k2-024",
            "allowed_files": ["src/shared/write-admission.mjs", "tests/write-admission.test.mjs"],
            "denied_authorities": [
                "BEO_PUBLICATION",
                "BROAD_BLK_PIPE_DISPATCH",
                "NEXT_K2_SELECTION",
                "REUSABLE_CODEX_DISPATCH",
                "RTM_GENERATION",
                "SOURCE_CLEANUP",
                "WORKTREE_CREATION",
            ],
            "evidence_required": [
                "final_message",
                "focused_red_green",
                "full_verification",
                "patch_sha256",
                "prompt",
            ],
            "max_remediation_rounds": 2,
            "external_codex_model": "gpt-5.4",
            "evidence_artifacts": {
                "final_message": "sha256:" + "8" * 64,
                "focused_red_green": "sha256:" + "9" * 64,
                "full_verification": "sha256:" + "a" * 64,
                "patch_sha256": "sha256:" + "b" * 64,
                "prompt": "sha256:" + "c" * 64,
            },
            "authorization_record_path": "artifacts/kuronode-v2/BEO-K2-024/FALLBACK-AUTH-K2-024.json",
            "authorization_record_sha256": "sha256:" + "7" * 64,
        }
        authorization.update(overrides)
        return authorization

    def failed_route_summary_with_artifact(self, **overrides):
        summary = self.failed_route_summary(status="ENGINE_TIMEOUT", exit_code=124, **overrides)
        artifact_rel = f"artifacts/kuronode-v2/{summary['beo_id']}/route-summary.json"
        artifact_path = self.root / artifact_rel
        artifact_path.parent.mkdir(parents=True, exist_ok=True)
        artifact_bytes = json.dumps(summary, sort_keys=True, separators=(",", ":")).encode("utf-8")
        artifact_path.write_bytes(artifact_bytes)
        summary["route_summary_path"] = artifact_rel
        summary["route_summary_sha256"] = self.sha(artifact_path)
        return summary

    def materialized_fallback_authorization(self, failed_summary=None, **overrides):
        failed_summary = failed_summary or self.failed_route_summary_with_artifact()
        authorization = self.valid_fallback_authorization(
            fallback_auth_id=f"FALLBACK-AUTH-{failed_summary['beo_id'].removeprefix('BEO-')}",
            route_failure_status=failed_summary["status"],
            route_summary_path=failed_summary["route_summary_path"],
            route_summary_sha256=failed_summary["route_summary_sha256"],
            target_hash=failed_summary["target_hash"],
            **overrides,
        )
        authorization.pop("authorization_record_path", None)
        authorization.pop("authorization_record_sha256", None)
        return write_fallback_authorization_record(
            self.root / "artifacts" / f"{authorization['fallback_auth_id']}.json",
            authorization=authorization,
            trusted_roots=[self.root],
        )

    def init_git_workdir(self, ignored: bool = False) -> str:
        subprocess.run(["git", "init", "-b", "sprint/beb-222"], cwd=self.work_dir, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["git", "config", "user.name", "test"], cwd=self.work_dir, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=self.work_dir, check=True)
        tracked = self.work_dir / "src" / "components" / "CanonicalDataGrid.tsx"
        tracked.parent.mkdir(parents=True, exist_ok=True)
        tracked.write_text("export const marker = 'before';\n")
        if ignored:
            (self.work_dir / ".gitignore").write_text("node_modules/\n")
            ignored_file = self.work_dir / "node_modules" / "left-pad" / "index.js"
            ignored_file.parent.mkdir(parents=True, exist_ok=True)
            ignored_file.write_text("module.exports = {};\n")
        subprocess.run(["git", "add", "."], cwd=self.work_dir, check=True)
        subprocess.run(["git", "commit", "-m", "initial"], cwd=self.work_dir, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.work_dir, check=True, text=True, stdout=subprocess.PIPE).stdout.strip()
        self.write_drop(target_hash=head)
        return head

    def write_drop(self, **overrides):
        manifest = {
            "target_project": "kuronode",
            "beb_id": "BEB_222",
            "l2_id": "L2_222",
            "beb_path": str(self.beb_path),
            "beb_sha256": self.sha(self.beb_path),
            "l2_path": str(self.l2_path),
            "l2_sha256": self.sha(self.l2_path),
            "work_dir": str(self.work_dir),
            "target_branch": "sprint/beb-222",
            "target_hash": TARGET_HASH,
            "allowed_modified_files": ["src/components/CanonicalDataGrid.tsx"],
            "allowed_new_files": [],
            "validation_profiles": ["python-unittest"],
        }
        manifest.update(overrides)
        self.drop_path.write_text(json.dumps(manifest))
        return manifest

    def test_preflight_reports_clean_exact_target_ready_without_invoking_engine(self):
        target_hash = self.init_git_workdir()
        adapter = FakeAdapter()

        report = preflight_drop_file(self.drop_path, **self.route_kwargs())

        self.assertEqual(report["status"], "READY")
        self.assertEqual(report["target_hash"], target_hash)
        self.assertEqual(report["blockers"], [])
        self.assertEqual(report["allowed_modified_files"], ["src/components/CanonicalDataGrid.tsx"])
        self.assertEqual(adapter.calls, [])

    def test_prepare_beb_l2_drop_package_writes_hash_bound_artifacts_ready_for_preflight(self):
        target_hash = self.init_git_workdir()
        package_dir = self.root / "packages" / "BLK-SYSTEM-232"

        package = prepare_beb_l2_drop_package(
            package_dir=package_dir,
            beb_id="BEB_232",
            l2_id="L2_232",
            work_dir=self.work_dir,
            target_branch="sprint/beb-222",
            target_hash=target_hash,
            objective="Add a visible Kuronode UI label through Codex.",
            l2_instructions="Modify only the approved UI file and keep tests passing.",
            allowed_modified_files=["src/components/CanonicalDataGrid.tsx"],
            allowed_new_files=[],
            validation_profiles=["python-unittest"],
            trace_artifacts=TRACE_ARTIFACTS,
        )

        self.assertEqual(package["status"], "BEB_L2_DROP_PACKAGE_READY")
        drop_path = Path(package["drop_path"])
        beb_path = Path(package["beb_path"])
        l2_path = Path(package["l2_path"])
        drop = json.loads(drop_path.read_text())
        self.assertEqual(package["approved_drop_sha256"], self.sha(drop_path))
        self.assertEqual(drop["beb_sha256"], self.sha(beb_path))
        self.assertEqual(drop["l2_sha256"], self.sha(l2_path))
        self.assertNotIn("engine", drop)
        self.assertNotIn("engine_args", drop)
        self.assertIn("BEB_ID: BEB_232", l2_path.read_text())
        self.assertIn("MODEL: gpt-5.5", l2_path.read_text())

        report = preflight_drop_file(
            drop_path,
            allowed_work_dirs=[self.work_dir],
            trusted_roots=[self.root],
            approved_drop_sha256=package["approved_drop_sha256"],
        )
        self.assertEqual(report["status"], "READY")
        self.assertEqual(report["target_hash"], target_hash)

    def test_prepare_beb_l2_drop_package_embeds_caller_object_readiness_profile_for_preflight(self):
        target_hash = self.init_git_workdir()
        package_dir = self.root / "packages" / "BLK-SYSTEM-355"

        package = prepare_beb_l2_drop_package(
            package_dir=package_dir,
            beb_id="BEB-TST-001",
            l2_id="L2-TST-001",
            work_dir=self.work_dir,
            target_branch="sprint/beb-222",
            target_hash=target_hash,
            objective="Add a caller-object control-plane helper through the governed route.",
            l2_instructions="Modify only approved caller-object files and keep validation green.",
            allowed_modified_files=[],
            allowed_new_files=["src/shared/view-intent-parameters.mjs", "tests/view-intent-parameters.test.mjs"],
            validation_profiles=["kuronode-worktree-focused-node"],
            readiness_profiles=[CALLER_OBJECT_PROFILE],
            trace_artifacts=TRACE_ARTIFACTS,
        )

        drop_path = Path(package["drop_path"])
        beb_path = Path(package["beb_path"])
        l2_path = Path(package["l2_path"])
        drop = json.loads(drop_path.read_text())
        self.assertEqual(drop["readiness_profiles"], [CALLER_OBJECT_PROFILE])
        self.assertEqual(package["readiness_profiles"], [CALLER_OBJECT_PROFILE])
        self.assertIn("do not authorize source/Git mutation", beb_path.read_text())
        self.assertIn("do not authorize source/Git mutation", l2_path.read_text())
        for probe_id in CALLER_OBJECT_REQUIRED_PROBES:
            self.assertIn(probe_id, beb_path.read_text())
            self.assertIn(probe_id, l2_path.read_text())

        report = preflight_drop_file(
            drop_path,
            allowed_work_dirs=[self.work_dir],
            trusted_roots=[self.root],
            approved_drop_sha256=package["approved_drop_sha256"],
        )
        self.assertEqual(report["status"], "READY")
        self.assertEqual(report["readiness_profiles"], [CALLER_OBJECT_PROFILE])
        self.assertEqual(report["blockers"], [])

    def test_prepare_beb_l2_drop_package_embeds_renderer_public_surface_profile_for_preflight(self):
        target_hash = self.init_git_workdir()
        package_dir = self.root / "packages" / "BLK-SYSTEM-357"

        package = prepare_beb_l2_drop_package(
            package_dir=package_dir,
            beb_id="BEB-TST-010",
            l2_id="L2-TST-010",
            work_dir=self.work_dir,
            target_branch="sprint/beb-222",
            target_hash=target_hash,
            objective="Expose a renderer-visible projection presentation through a bounded public surface.",
            l2_instructions="Modify only approved renderer presentation files and preserve authority boundaries.",
            allowed_modified_files=["src/renderer/App.tsx", "src/renderer/main.tsx"],
            allowed_new_files=["tests/renderer-projection-panel-presentation.test.mjs"],
            validation_profiles=["kuronode-worktree-focused-node"],
            readiness_profiles=[RENDERER_PUBLIC_SURFACE_PROFILE],
            trace_artifacts=TRACE_ARTIFACTS,
        )

        drop_path = Path(package["drop_path"])
        beb_path = Path(package["beb_path"])
        l2_path = Path(package["l2_path"])
        drop = json.loads(drop_path.read_text())
        self.assertEqual(drop["readiness_profiles"], [RENDERER_PUBLIC_SURFACE_PROFILE])
        self.assertEqual(package["readiness_profiles"], [RENDERER_PUBLIC_SURFACE_PROFILE])
        beb_text = beb_path.read_text()
        l2_text = l2_path.read_text()
        self.assertIn("conditional pre-dispatch evidence", beb_text)
        self.assertIn("does not make this profile mandatory for non-renderer slices", beb_text)
        self.assertIn("does not authorize source/Git mutation", l2_text)
        for probe_id in RENDERER_PUBLIC_SURFACE_REQUIRED_PROBES:
            self.assertIn(probe_id, beb_text)
            self.assertIn(probe_id, l2_text)

        report = preflight_drop_file(
            drop_path,
            allowed_work_dirs=[self.work_dir],
            trusted_roots=[self.root],
            approved_drop_sha256=package["approved_drop_sha256"],
        )
        self.assertEqual(report["status"], "READY")
        self.assertEqual(report["readiness_profiles"], [RENDERER_PUBLIC_SURFACE_PROFILE])
        self.assertEqual(report["blockers"], [])

    def test_prepare_beb_l2_drop_package_embeds_agent_a_promotion_request_profile_for_preflight(self):
        target_hash = self.init_git_workdir()
        package_dir = self.root / "packages" / "BLK-SYSTEM-362"

        package = prepare_beb_l2_drop_package(
            package_dir=package_dir,
            beb_id="BEB-TST-023",
            l2_id="L2-TST-023",
            work_dir=self.work_dir,
            target_branch="sprint/beb-222",
            target_hash=target_hash,
            objective="Create a pure-data Agent A promotion-request/preflight envelope.",
            l2_instructions="Modify only approved Agent A promotion-request files and keep authority boundaries denied.",
            allowed_modified_files=["src/shared/agent-a-promotion-request.mjs", "tests/agent-a-promotion-request.test.mjs"],
            allowed_new_files=[],
            validation_profiles=["kuronode-worktree-focused-node"],
            readiness_profiles=[AGENT_A_PROMOTION_REQUEST_PROFILE],
            trace_artifacts=TRACE_ARTIFACTS,
        )

        drop_path = Path(package["drop_path"])
        beb_path = Path(package["beb_path"])
        l2_path = Path(package["l2_path"])
        drop = json.loads(drop_path.read_text())
        self.assertEqual(drop["readiness_profiles"], [AGENT_A_PROMOTION_REQUEST_PROFILE])
        self.assertEqual(package["readiness_profiles"], [AGENT_A_PROMOTION_REQUEST_PROFILE])
        beb_text = beb_path.read_text()
        l2_text = l2_path.read_text()
        self.assertIn("JSON-like finite evidence graphs", beb_text)
        self.assertIn("NaN/Infinity/null hash-alias probes", l2_text)
        self.assertIn("own enumerable __proto__ evidence", beb_text)
        self.assertIn("does not authorize source/Git mutation", l2_text)
        for probe_id in AGENT_A_PROMOTION_REQUEST_REQUIRED_PROBES:
            self.assertIn(probe_id, beb_text)
            self.assertIn(probe_id, l2_text)

        report = preflight_drop_file(
            drop_path,
            allowed_work_dirs=[self.work_dir],
            trusted_roots=[self.root],
            approved_drop_sha256=package["approved_drop_sha256"],
        )
        self.assertEqual(report["status"], "READY")
        self.assertEqual(report["readiness_profiles"], [AGENT_A_PROMOTION_REQUEST_PROFILE])
        self.assertEqual(report["blockers"], [])

    def test_preflight_blocks_caller_object_profile_when_required_probe_card_is_missing(self):
        target_hash = self.init_git_workdir()
        self.write_drop(target_hash=target_hash, readiness_profiles=[CALLER_OBJECT_PROFILE])

        report = preflight_drop_file(self.drop_path, **self.route_kwargs())

        self.assertEqual(report["status"], "BLOCKED")
        blockers = report["blockers"]
        self.assertIn("MISSING_READINESS_PROBE", {blocker["code"] for blocker in blockers})
        missing = {blocker["probe_id"] for blocker in blockers if blocker["code"] == "MISSING_READINESS_PROBE"}
        self.assertEqual(missing, set(CALLER_OBJECT_REQUIRED_PROBES))
        self.assertEqual(report["readiness_profiles"], [CALLER_OBJECT_PROFILE])

    def test_preflight_blocks_renderer_public_surface_profile_when_required_probe_card_is_missing(self):
        target_hash = self.init_git_workdir()
        self.write_drop(target_hash=target_hash, readiness_profiles=[RENDERER_PUBLIC_SURFACE_PROFILE])

        report = preflight_drop_file(self.drop_path, **self.route_kwargs())

        self.assertEqual(report["status"], "BLOCKED")
        blockers = report["blockers"]
        self.assertIn("MISSING_READINESS_PROBE", {blocker["code"] for blocker in blockers})
        missing = {blocker["probe_id"] for blocker in blockers if blocker["code"] == "MISSING_READINESS_PROBE"}
        self.assertEqual(missing, set(RENDERER_PUBLIC_SURFACE_REQUIRED_PROBES))
        self.assertEqual(report["readiness_profiles"], [RENDERER_PUBLIC_SURFACE_PROFILE])

    def test_preflight_blocks_caller_object_profile_when_probe_card_has_bare_ids_only(self):
        target_hash = self.init_git_workdir()
        bare_probe_ids = "\n".join(f"- [ ] {probe_id}" for probe_id in CALLER_OBJECT_REQUIRED_PROBES)
        self.beb_path.write_text(self.beb_path.read_text() + "\n" + bare_probe_ids + "\n")
        self.l2_path.write_text(self.l2_path.read_text() + "\n" + bare_probe_ids + "\n")
        self.write_drop(target_hash=target_hash, readiness_profiles=[CALLER_OBJECT_PROFILE])

        report = preflight_drop_file(self.drop_path, **self.route_kwargs())

        self.assertEqual(report["status"], "BLOCKED")
        blockers = report["blockers"]
        missing = {blocker["probe_id"] for blocker in blockers if blocker["code"] == "MISSING_READINESS_PROBE"}
        self.assertEqual(missing, set(CALLER_OBJECT_REQUIRED_PROBES))

    def test_preflight_blocks_caller_object_profile_when_required_phrases_are_not_in_probe_card(self):
        target_hash = self.init_git_workdir()
        phrase_only = "\n".join(
            f"Implementation note mentions {probe_id} {description}."
            for probe_id, description in (
                ("KCP-001", "direct accepted ready input"),
                ("KCP-002", "wrapper accepted ready input"),
                ("KCP-003", "top-level denied raw/authority/source/provider/parser/import/export/mutation fail closed"),
                ("KCP-004", "nested denied raw/authority/source/provider/parser/import/export/mutation fail closed"),
                ("KCP-005", "raw marker values fail closed and do not serialize back out"),
                ("KCP-006", "duplicate filters or entries beyond cap fail closed"),
                ("KCP-007", "proxy/getter/callable/symbol inputs fail closed without invoking caller code"),
                ("KCP-008", "public capability/result objects deeply frozen and public getters have no mutable prototype"),
                ("KCP-009", "helper vocabulary confined to owning module/tests"),
                ("KCP-010", "downstream compatibility probe for the paired payload/capability surface"),
                ("KCP-011", "deep hostile object graph hits a bounded circuit breaker without throwing"),
                ("KCP-012", "caller authority/status/trust laundering fields force fail-closed false readiness"),
            )
        )
        self.beb_path.write_text(self.beb_path.read_text() + "\n" + phrase_only + "\n")
        self.l2_path.write_text(self.l2_path.read_text() + "\n" + phrase_only + "\n")
        self.write_drop(target_hash=target_hash, readiness_profiles=[CALLER_OBJECT_PROFILE])

        report = preflight_drop_file(self.drop_path, **self.route_kwargs())

        self.assertEqual(report["status"], "BLOCKED")
        self.assertIn("MISSING_READINESS_PROFILE_CARD", {blocker["code"] for blocker in report["blockers"]})

    def test_process_drop_file_refuses_caller_object_profile_without_required_probe_card(self):
        target_hash = self.init_git_workdir()
        self.write_drop(target_hash=target_hash, readiness_profiles=[CALLER_OBJECT_PROFILE])
        adapter = FakeAdapter()

        with self.assertRaisesRegex(RouteError, "MISSING_READINESS_PROBE"):
            self.process(adapter)
        self.assertEqual(adapter.calls, [])

    def test_unknown_readiness_profile_fails_closed_before_dispatch(self):
        target_hash = self.init_git_workdir()
        self.write_drop(target_hash=target_hash, readiness_profiles=["kuronode-unknown-profile"])

        with self.assertRaisesRegex(RouteError, "readiness_profiles contain unsupported profiles"):
            preflight_drop_file(self.drop_path, **self.route_kwargs())

    def test_caller_object_candidate_without_profile_gets_non_authorizing_advisory_suggestion(self):
        target_hash = self.init_git_workdir()
        self.write_drop(
            target_hash=target_hash,
            allowed_modified_files=[],
            allowed_new_files=["src/shared/view-intent-parameters.mjs", "tests/view-intent-parameters.test.mjs"],
        )

        report = preflight_drop_file(self.drop_path, **self.route_kwargs())

        self.assertEqual(report["status"], "READY")
        suggestion = next(item for item in report["allowlist_suggestions"] if item["kind"] == "readiness_profile_recommended")
        self.assertEqual(suggestion["profile"], CALLER_OBJECT_PROFILE)
        self.assertEqual(suggestion["source_file"], "src/shared/view-intent-parameters.mjs")
        self.assertFalse(suggestion["auto_authorized"])

    def test_renderer_public_surface_candidate_without_profile_gets_non_authorizing_advisory_suggestion(self):
        target_hash = self.init_git_workdir()
        self.write_drop(
            target_hash=target_hash,
            allowed_modified_files=["src/renderer/App.tsx", "src/renderer/main.tsx"],
            allowed_new_files=["tests/renderer-projection-panel-presentation.test.mjs"],
        )

        report = preflight_drop_file(self.drop_path, **self.route_kwargs())

        self.assertEqual(report["status"], "READY")
        suggestion = next(
            item
            for item in report["allowlist_suggestions"]
            if item["kind"] == "readiness_profile_recommended"
            and item["profile"] == RENDERER_PUBLIC_SURFACE_PROFILE
        )
        self.assertEqual(suggestion["source_file"], "src/renderer/App.tsx")
        self.assertIn("conditional", suggestion["message"])
        self.assertFalse(suggestion["auto_authorized"])

    def test_prepare_beb_l2_drop_package_rejects_readiness_profile_manifest_override(self):
        target_hash = self.init_git_workdir()
        package_dir = self.root / "packages" / "BLK-SYSTEM-355-bad"

        with self.assertRaisesRegex(RouteError, "override canonical manifest fields: readiness_profiles"):
            prepare_beb_l2_drop_package(
                package_dir=package_dir,
                beb_id="BEB-TST-001",
                l2_id="L2-TST-001",
                work_dir=self.work_dir,
                target_branch="sprint/beb-222",
                target_hash=target_hash,
                objective="bad package",
                l2_instructions="bad package",
                allowed_modified_files=[],
                allowed_new_files=["src/shared/view-intent-parameters.mjs"],
                validation_profiles=["kuronode-worktree-focused-node"],
                trace_artifacts=TRACE_ARTIFACTS,
                extra_manifest_fields={"readiness_profiles": [CALLER_OBJECT_PROFILE]},
            )

    def test_prepare_synthetic_tst_drop_package_writes_named_artifacts_and_view_only_obsidian_mirrors(self):
        target_hash = self.init_git_workdir()
        package_dir = self.root / "docs" / "kuronode-v2" / "route-packages" / "BEB-TST-001"
        mirror_dir = self.root / "Obsidian Vault" / "Projects" / "Kuronode V2.0" / "03 Implementation" / "Execution Mirrors"

        package = prepare_beb_l2_drop_package(
            package_dir=package_dir,
            beb_id="BEB-TST-001",
            l2_id="L2-TST-001",
            work_dir=self.work_dir,
            target_branch="sprint/beb-222",
            target_hash=target_hash,
            objective="Add provider readiness status display through the governed Kuronode V2 route.",
            l2_instructions="Modify only the approved provider-readiness files and keep validation green.",
            allowed_modified_files=["src/components/CanonicalDataGrid.tsx"],
            allowed_new_files=[],
            validation_profiles=["python-unittest"],
            trace_artifacts=TRACE_ARTIFACTS,
            artifact_slug="Provider_Readiness_Status_Display",
            obsidian_mirror_dir=mirror_dir,
        )

        beb_path = Path(package["beb_path"])
        l2_path = Path(package["l2_path"])
        beo_path = Path(package["beo_path"])
        drop_path = Path(package["drop_path"])
        self.assertEqual(beb_path.name, "BEB-TST-001_Provider_Readiness_Status_Display.md")
        self.assertEqual(l2_path.name, "L2-TST-001_Provider_Readiness_Status_Display.md")
        self.assertEqual(beo_path.name, "BEO-TST-001_Provider_Readiness_Status_Display.md")
        self.assertEqual(drop_path.name, "drop.json")
        self.assertEqual(package["beb_id"], "BEB-TST-001")
        self.assertEqual(package["beo_id"], "BEO-TST-001")
        self.assertEqual(package["l2_id"], "L2-TST-001")

        mirror_paths = {Path(path).name: Path(path) for path in package["obsidian_mirror_paths"]}
        self.assertEqual(
            set(mirror_paths),
            {
                "BEB-TST-001_Provider_Readiness_Status_Display.md",
                "L2-TST-001_Provider_Readiness_Status_Display.md",
                "BEO-TST-001_Provider_Readiness_Status_Display.md",
            },
        )
        for mirror_path in mirror_paths.values():
            mirror_text = mirror_path.read_text()
            self.assertTrue(mirror_text.startswith("> VIEW COPY — DO NOT EDIT\n"))
            self.assertIn("BLK-System consumes the canonical route package, not this Obsidian mirror.", mirror_text)
            self.assertIn("Canonical sha256:", mirror_text)
            self.assertEqual(oct(mirror_path.stat().st_mode & 0o777), "0o444")

        drop = json.loads(drop_path.read_text())
        self.assertEqual(drop["beb_id"], "BEB-TST-001")
        self.assertEqual(drop["beo_id"], "BEO-TST-001")
        self.assertEqual(drop["l2_id"], "L2-TST-001")
        self.assertIn("BEB_ID: BEB-TST-001", l2_path.read_text())
        self.assertIn("BEO_ID: BEO-TST-001", l2_path.read_text())
        self.assertIn("L2_ID: L2-TST-001", l2_path.read_text())

        report = preflight_drop_file(
            drop_path,
            allowed_work_dirs=[self.work_dir],
            trusted_roots=[self.root],
            approved_drop_sha256=package["approved_drop_sha256"],
        )
        self.assertEqual(report["status"], "READY")
        self.assertEqual(report["beb_id"], "BEB-TST-001")
        self.assertEqual(report["beo_id"], "BEO-TST-001")
        self.assertEqual(build_route_commit_message("BEB-TST-001"), "blk-pipe: BEB-TST-001")

    def test_prepare_family_drop_package_includes_matching_beo_artifact(self):
        target_hash = self.init_git_workdir()
        package_dir = self.root / "docs" / "kuronode-v2" / "route-packages" / "BEB-TST-002"
        mirror_dir = self.root / "Obsidian Vault" / "Projects" / "Kuronode V2.0" / "03 Implementation" / "Execution Mirrors"

        package = prepare_beb_l2_drop_package(
            package_dir=package_dir,
            beb_id="BEB-TST-002",
            l2_id="L2-TST-002",
            beo_id="BEO-TST-002",
            work_dir=self.work_dir,
            target_branch="sprint/beb-222",
            target_hash=target_hash,
            objective="Add a synthetic TST-family capability through the governed route.",
            l2_instructions="Modify only approved files and preserve the route boundary.",
            allowed_modified_files=["src/components/CanonicalDataGrid.tsx"],
            allowed_new_files=[],
            validation_profiles=["python-unittest"],
            trace_artifacts=TRACE_ARTIFACTS,
            artifact_slug="Test_Capability",
            obsidian_mirror_dir=mirror_dir,
        )

        self.assertEqual(derive_matching_beo_id("BEB-TST-002"), "BEO-TST-002")
        self.assertEqual(package["beo_id"], "BEO-TST-002")
        beo_path = Path(package["beo_path"])
        self.assertEqual(beo_path.name, "BEO-TST-002_Test_Capability.md")
        beo_text = beo_path.read_text()
        self.assertIn('beo_id: "BEO-TST-002"', beo_text)
        self.assertIn('beb_id: "BEB-TST-002"', beo_text)
        self.assertIn('l2_id: "L2-TST-002"', beo_text)
        self.assertIn("BEO_TEMPLATE_PENDING_EXECUTION_EVIDENCE", beo_text)
        self.assertIn("BEO_ID: BEO-TST-002", Path(package["l2_path"]).read_text())

        drop = json.loads(Path(package["drop_path"]).read_text())
        self.assertEqual(drop["beo_id"], "BEO-TST-002")
        self.assertEqual(drop["beo_sha256"], self.sha(beo_path))
        self.assertEqual(drop["beo_path"], str(beo_path))

        mirror_names = {Path(path).name for path in package["obsidian_mirror_paths"]}
        self.assertIn("BEO-TST-002_Test_Capability.md", mirror_names)

        report = preflight_drop_file(
            package["drop_path"],
            allowed_work_dirs=[self.work_dir],
            trusted_roots=[self.root],
            approved_drop_sha256=package["approved_drop_sha256"],
        )
        self.assertEqual(report["status"], "READY")
        self.assertEqual(report["beo_id"], "BEO-TST-002")

    def test_prepare_family_drop_package_rejects_mismatched_beo_or_l2_family(self):
        target_hash = self.init_git_workdir()
        base_kwargs = {
            "package_dir": self.root / "packages" / "BEB-TST-003",
            "beb_id": "BEB-TST-003",
            "l2_id": "L2-TST-003",
            "work_dir": self.work_dir,
            "target_branch": "sprint/beb-222",
            "target_hash": target_hash,
            "objective": "Add a synthetic TST-family capability through the governed route.",
            "l2_instructions": "Modify only approved files and preserve the route boundary.",
            "allowed_modified_files": ["src/components/CanonicalDataGrid.tsx"],
            "allowed_new_files": [],
            "validation_profiles": ["python-unittest"],
            "trace_artifacts": TRACE_ARTIFACTS,
        }
        with self.assertRaisesRegex(RouteError, "beo_id must match BEB family and sequence"):
            prepare_beb_l2_drop_package(**base_kwargs, beo_id="BEO-ALT-003")
        with self.assertRaisesRegex(RouteError, "l2_id must match BEB family and sequence"):
            prepare_beb_l2_drop_package(**{**base_kwargs, "l2_id": "L2-ALT-003", "beo_id": "BEO-TST-003"})

    def test_preflight_rejects_empty_or_aliased_beo_artifact(self):
        target_hash = self.init_git_workdir()
        package = prepare_beb_l2_drop_package(
            package_dir=self.root / "packages" / "BEB-TST-004",
            beb_id="BEB-TST-004",
            l2_id="L2-TST-004",
            work_dir=self.work_dir,
            target_branch="sprint/beb-222",
            target_hash=target_hash,
            objective="Add a synthetic TST-family capability through the governed route.",
            l2_instructions="Modify only approved files and preserve the route boundary.",
            allowed_modified_files=["src/components/CanonicalDataGrid.tsx"],
            allowed_new_files=[],
            validation_profiles=["python-unittest"],
            trace_artifacts=TRACE_ARTIFACTS,
        )
        drop_path = Path(package["drop_path"])
        drop = json.loads(drop_path.read_text())
        beo_path = Path(drop["beo_path"])
        beo_path.write_text("")
        drop["beo_sha256"] = self.sha(beo_path)
        drop_path.write_text(json.dumps(drop, indent=2, sort_keys=True) + "\n")
        with self.assertRaisesRegex(RouteError, "BEO artifact must not be empty"):
            preflight_drop_file(
                drop_path,
                allowed_work_dirs=[self.work_dir],
                trusted_roots=[self.root],
                approved_drop_sha256=self.sha(drop_path),
            )

        drop["beo_path"] = drop["beb_path"]
        drop["beo_sha256"] = drop["beb_sha256"]
        drop_path.write_text(json.dumps(drop, indent=2, sort_keys=True) + "\n")
        with self.assertRaisesRegex(RouteError, "BEB, L2, and BEO artifact paths must be distinct"):
            preflight_drop_file(
                drop_path,
                allowed_work_dirs=[self.work_dir],
                trusted_roots=[self.root],
                approved_drop_sha256=self.sha(drop_path),
            )

    def test_preflight_rejects_beo_overclaims_and_trace_drift(self):
        target_hash = self.init_git_workdir()
        package = prepare_beb_l2_drop_package(
            package_dir=self.root / "packages" / "BEB-TST-006",
            beb_id="BEB-TST-006",
            l2_id="L2-TST-006",
            work_dir=self.work_dir,
            target_branch="sprint/beb-222",
            target_hash=target_hash,
            objective="Add a synthetic TST-family capability through the governed route.",
            l2_instructions="Modify only approved files and preserve the route boundary.",
            allowed_modified_files=["src/components/CanonicalDataGrid.tsx"],
            allowed_new_files=[],
            validation_profiles=["python-unittest"],
            trace_artifacts=TRACE_ARTIFACTS,
        )
        drop_path = Path(package["drop_path"])
        drop = json.loads(drop_path.read_text())
        beo_path = Path(drop["beo_path"])
        original_beo_text = beo_path.read_text()

        beo_path.write_text(original_beo_text.replace("BEO_TEMPLATE_PENDING_EXECUTION_EVIDENCE", "BEO_PUBLISHED", 1))
        drop["beo_sha256"] = self.sha(beo_path)
        drop_path.write_text(json.dumps(drop, indent=2, sort_keys=True) + "\n")
        with self.assertRaisesRegex(RouteError, "BEO status must be BEO_TEMPLATE_PENDING_EXECUTION_EVIDENCE"):
            preflight_drop_file(
                drop_path,
                allowed_work_dirs=[self.work_dir],
                trusted_roots=[self.root],
                approved_drop_sha256=self.sha(drop_path),
            )

        beo_path.write_text(original_beo_text.replace('id: "REQ-222"', 'id: "REQ-999"'))
        drop["beo_sha256"] = self.sha(beo_path)
        drop_path.write_text(json.dumps(drop, indent=2, sort_keys=True) + "\n")
        with self.assertRaisesRegex(RouteError, "BEO trace_artifacts must match paired BEB trace_artifacts"):
            preflight_drop_file(
                drop_path,
                allowed_work_dirs=[self.work_dir],
                trusted_roots=[self.root],
                approved_drop_sha256=self.sha(drop_path),
            )

    def test_final_beo_placeholder_scanner_blocks_hash_freeze_until_final_metadata_is_bound(self):
        pending_text = """---
beo_id: "BEO-K2-015"
status: "BEO_TEMPLATE_PENDING_EXECUTION_EVIDENCE"
closeout_metadata_commit: "this Kuronode closeout metadata commit (pending)"
---
Pending dispatch and pending-k2-015-closeout.
"""

        blocked = scan_final_beo_closeout_placeholders(pending_text, beo_id="BEO-K2-015")

        self.assertEqual(blocked["status"], "FINAL_BEO_PLACEHOLDER_SCAN_BLOCKED")
        self.assertFalse(blocked["hash_freeze_allowed"])
        self.assertIn("PLACEHOLDER_CLOSEOUT_METADATA_COMMIT", {item["code"] for item in blocked["blockers"]})
        self.assertIn("PENDING_BEO_TEMPLATE_STATUS", {item["code"] for item in blocked["blockers"]})

        draft_text = """---
beo_id: "BEO-K2-015"
status: "draft"
closeout_metadata_commit: "4b83f7ebc026188c48b78eecbc0625f7dffb0db0"
---
Draft text with no placeholder metadata.
"""
        draft = scan_final_beo_closeout_placeholders(draft_text, beo_id="BEO-K2-015")
        self.assertEqual(draft["status"], "FINAL_BEO_PLACEHOLDER_SCAN_BLOCKED")
        self.assertIn("NON_FINAL_BEO_STATUS", {item["code"] for item in draft["blockers"]})

        missing_status_text = """---
beo_id: "BEO-K2-015"
closeout_metadata_commit: "4b83f7ebc026188c48b78eecbc0625f7dffb0db0"
---
Closed-looking prose without a status field.
"""
        missing_status = scan_final_beo_closeout_placeholders(missing_status_text, beo_id="BEO-K2-015")
        self.assertIn("MISSING_FINAL_BEO_STATUS", {item["code"] for item in missing_status["blockers"]})

        duplicate_status_text = """---
beo_id: "BEO-K2-015"
status: "closed"
status: "draft"
closeout_metadata_commit: "4b83f7ebc026188c48b78eecbc0625f7dffb0db0"
---
Ambiguous duplicate status must not pass hash freeze.
"""
        duplicate_status = scan_final_beo_closeout_placeholders(duplicate_status_text, beo_id="BEO-K2-015")
        self.assertIn("DUPLICATE_FINAL_BEO_STATUS", {item["code"] for item in duplicate_status["blockers"]})

        final_text = """---
beo_id: "BEO-K2-015"
status: "closed"
artifact_stage: "final_beo_closeout"
target_hash: "68a9b8c0b9b056a9c8a80d8bae32c093ade4c8e6"
feature_commit: "c4ebb5c82cb0354728f55be9b28bcf107a6cd453"
closeout_metadata_commit: "4b83f7ebc026188c48b78eecbc0625f7dffb0db0"
---
# BEO-K2-015
Final verification complete.
"""
        ready = scan_final_beo_closeout_placeholders(final_text, beo_id="BEO-K2-015")

        self.assertEqual(ready["status"], "FINAL_BEO_PLACEHOLDER_SCAN_PASS")
        self.assertTrue(ready["hash_freeze_allowed"])
        self.assertEqual(ready["blockers"], [])
        self.assertRegex(ready["canonical_sha256"], r"^sha256:[0-9a-f]{64}$")

    def test_route_closeout_gate_blocks_non_executed_route_without_fallback_authorization(self):
        gate = evaluate_route_closeout_gate(route_summaries=[self.failed_route_summary()])

        self.assertEqual(gate["status"], "ROUTE_CLOSEOUT_GATE_BLOCKED")
        self.assertFalse(gate["normal_closeout_allowed"])
        self.assertFalse(gate["fallback_exception_allowed"])
        self.assertFalse(gate["external_codex_fallback_authorized"])
        self.assertEqual(gate["successful_route_count"], 0)
        blocker_codes = {item["code"] for item in gate["blockers"]}
        self.assertIn("NO_SUCCESSFUL_BLK_PIPE_ROUTE_COMMIT", blocker_codes)
        self.assertIn("NON_EXECUTED_ROUTE_EVIDENCE", blocker_codes)
        self.assertEqual(gate["required_action"], "repair_or_reroute_through_blk_pipe")

    def test_route_closeout_gate_passes_successful_blk_pipe_route_commit(self):
        gate = evaluate_route_closeout_gate(route_summaries=[self.successful_route_summary()])

        self.assertEqual(gate["status"], "ROUTE_CLOSEOUT_GATE_PASS")
        self.assertTrue(gate["normal_closeout_allowed"])
        self.assertFalse(gate["fallback_exception_allowed"])
        self.assertFalse(gate["external_codex_fallback_authorized"])
        self.assertEqual(gate["successful_route_count"], 1)
        self.assertEqual(gate["blockers"], [])
        self.assertEqual(gate["required_action"], "normal_closeout_allowed")

    def test_route_closeout_gate_rejects_successful_route_without_verified_artifact(self):
        fabricated_success = self.successful_route_summary()
        fabricated_success.pop("route_summary_artifact_path")
        fabricated_success.pop("route_summary_artifact_sha256")

        gate = evaluate_route_closeout_gate(route_summaries=[fabricated_success])

        self.assertEqual(gate["status"], "ROUTE_CLOSEOUT_GATE_BLOCKED")
        self.assertFalse(gate["normal_closeout_allowed"])
        self.assertIn("ROUTE_SUMMARY_ARTIFACT_UNVERIFIED", {item["code"] for item in gate["blockers"]})

    def test_route_closeout_gate_rejects_malformed_success_shape_instead_of_discarding_blockers(self):
        malformed_success = self.successful_route_summary(
            beb_id="not-a-beb",
            target_hash="not-a-git-hash",
            drop_manifest_sha256="not-a-sha256",
        )

        gate = evaluate_route_closeout_gate(route_summaries=[malformed_success])

        self.assertEqual(gate["status"], "ROUTE_CLOSEOUT_GATE_BLOCKED")
        self.assertFalse(gate["normal_closeout_allowed"])
        blocker_codes = {item["code"] for item in gate["blockers"]}
        self.assertIn("INVALID_ROUTE_TARGET_HASH", blocker_codes)
        self.assertIn("INVALID_ROUTE_SUMMARY_IDENTITY", blocker_codes)

    def test_route_closeout_gate_rejects_bool_numeric_success_fields(self):
        bool_success = self.successful_route_summary(
            exit_code=False,
            engine_logs_bytes=True,
            final_message_bytes=True,
            validation_log_count=True,
        )

        gate = evaluate_route_closeout_gate(route_summaries=[bool_success])

        self.assertEqual(gate["status"], "ROUTE_CLOSEOUT_GATE_BLOCKED")
        self.assertFalse(gate["normal_closeout_allowed"])
        self.assertIn("NO_SUCCESSFUL_BLK_PIPE_ROUTE_COMMIT", {item["code"] for item in gate["blockers"]})

    def test_route_closeout_gate_rejects_mixed_success_when_any_route_summary_is_malformed(self):
        gate = evaluate_route_closeout_gate(
            route_summaries=[
                self.successful_route_summary(),
                self.failed_route_summary(target_hash="not-a-git-hash"),
            ]
        )

        self.assertEqual(gate["status"], "ROUTE_CLOSEOUT_GATE_BLOCKED")
        self.assertFalse(gate["normal_closeout_allowed"])
        self.assertIn("INVALID_ROUTE_TARGET_HASH", {item["code"] for item in gate["blockers"]})

    def test_route_closeout_gate_rejects_fallback_without_valid_failed_route_target_binding(self):
        failed = self.failed_route_summary(status="ENGINE_TIMEOUT", exit_code=124, target_hash="not-a-git-hash")

        gate = evaluate_route_closeout_gate(
            route_summaries=[failed],
            fallback_authorization=self.valid_fallback_authorization(),
            fallback_remediation_rounds=1,
        )

        self.assertEqual(gate["status"], "ROUTE_CLOSEOUT_GATE_BLOCKED")
        self.assertFalse(gate["fallback_exception_allowed"])
        self.assertIn("INVALID_ROUTE_TARGET_HASH", {item["code"] for item in gate["blockers"]})

    def test_route_closeout_gate_rejects_invalid_remediation_rounds_before_fallback_exception(self):
        failed = self.failed_route_summary(status="ENGINE_TIMEOUT", exit_code=124)

        gate = evaluate_route_closeout_gate(
            route_summaries=[failed],
            fallback_authorization=self.valid_fallback_authorization(),
            fallback_remediation_rounds=True,
        )

        self.assertEqual(gate["status"], "ROUTE_CLOSEOUT_GATE_BLOCKED")
        self.assertFalse(gate["fallback_exception_allowed"])
        self.assertIn("INVALID_FALLBACK_REMEDIATION_ROUNDS", {item["code"] for item in gate["blockers"]})

    def test_route_closeout_gate_requires_persisted_fallback_authorization_record_fields(self):
        failed = self.failed_route_summary(status="ENGINE_TIMEOUT", exit_code=124)
        legacy_authorization = self.valid_fallback_authorization()
        for field in (
            "fallback_auth_id",
            "authorized_at",
            "route_summary_path",
            "route_summary_sha256",
            "fallback_worktree",
            "evidence_artifacts",
            "authorization_record_path",
            "authorization_record_sha256",
        ):
            legacy_authorization.pop(field, None)

        gate = evaluate_route_closeout_gate(
            route_summaries=[failed],
            fallback_authorization=legacy_authorization,
            fallback_remediation_rounds=1,
        )

        self.assertEqual(gate["status"], "ROUTE_CLOSEOUT_GATE_BLOCKED")
        self.assertFalse(gate["fallback_exception_allowed"])
        self.assertIn("FALLBACK_AUTHORIZATION_INVALID", {item["code"] for item in gate["blockers"]})

    def test_fallback_authorization_record_round_trips_with_hash_bound_file(self):
        failed = self.failed_route_summary_with_artifact()
        record_path = self.root / "artifacts" / "FALLBACK-AUTH-K2-024.json"
        authorization = self.valid_fallback_authorization(
            route_failure_status=failed["status"],
            route_summary_path=failed["route_summary_path"],
            route_summary_sha256=failed["route_summary_sha256"],
            target_hash=failed["target_hash"],
        )
        authorization.pop("authorization_record_path")
        authorization.pop("authorization_record_sha256")

        written = write_fallback_authorization_record(
            record_path,
            authorization=authorization,
            trusted_roots=[self.root],
        )
        loaded = load_fallback_authorization_record(
            record_path,
            expected_sha256=written["authorization_record_sha256"],
            trusted_roots=[self.root],
        )

        self.assertEqual(written["authorization_record_path"], str(record_path.resolve()))
        self.assertEqual(written["authorization_record_sha256"], self.sha(record_path))
        self.assertEqual(loaded, written)
        gate = evaluate_route_closeout_gate(
            route_summaries=[failed],
            fallback_authorization=loaded,
            fallback_remediation_rounds=1,
            fallback_authorization_trusted_roots=[self.root],
        )
        self.assertEqual(gate["status"], "ROUTE_CLOSEOUT_GATE_FALLBACK_EXCEPTION")
        self.assertFalse(gate["normal_closeout_allowed"])
        self.assertTrue(gate["fallback_exception_allowed"])

    def test_route_closeout_gate_rejects_fabricated_or_unbound_fallback_authorization_records(self):
        failed = self.failed_route_summary_with_artifact()
        fabricated = self.valid_fallback_authorization(
            route_failure_status=failed["status"],
            route_summary_path=failed["route_summary_path"],
            route_summary_sha256=failed["route_summary_sha256"],
            target_hash=failed["target_hash"],
            authorization_record_path=str(self.root / "missing" / "FALLBACK-AUTH-K2-024.json"),
            authorization_record_sha256="sha256:" + "f" * 64,
        )

        missing = evaluate_route_closeout_gate(
            route_summaries=[failed],
            fallback_authorization=fabricated,
            fallback_remediation_rounds=1,
            fallback_authorization_trusted_roots=[self.root],
        )
        self.assertEqual(missing["status"], "ROUTE_CLOSEOUT_GATE_BLOCKED")
        self.assertIn("FALLBACK_AUTHORIZATION_INVALID", {item["code"] for item in missing["blockers"]})

        materialized = self.materialized_fallback_authorization(failed)
        forged_route = dict(failed)
        forged_route["route_summary_sha256"] = "sha256:" + "d" * 64
        mismatched = evaluate_route_closeout_gate(
            route_summaries=[forged_route],
            fallback_authorization=materialized,
            fallback_remediation_rounds=1,
            fallback_authorization_trusted_roots=[self.root],
        )
        self.assertEqual(mismatched["status"], "ROUTE_CLOSEOUT_GATE_BLOCKED")
        self.assertIn("FALLBACK_AUTHORIZATION_INVALID", {item["code"] for item in mismatched["blockers"]})

        missing_route_artifact = dict(failed)
        (self.root / missing_route_artifact["route_summary_path"]).unlink()
        missing_artifact_gate = evaluate_route_closeout_gate(
            route_summaries=[missing_route_artifact],
            fallback_authorization=materialized,
            fallback_remediation_rounds=1,
            fallback_authorization_trusted_roots=[self.root],
        )
        self.assertEqual(missing_artifact_gate["status"], "ROUTE_CLOSEOUT_GATE_BLOCKED")
        self.assertIn("FALLBACK_AUTHORIZATION_INVALID", {item["code"] for item in missing_artifact_gate["blockers"]})

        arbitrary_route_artifact = self.failed_route_summary(status="ENGINE_TIMEOUT", exit_code=124)
        arbitrary_rel = "artifacts/kuronode-v2/BEO-K2-024/not-a-route-summary.txt"
        arbitrary_path = self.root / arbitrary_rel
        arbitrary_path.parent.mkdir(parents=True, exist_ok=True)
        arbitrary_path.write_text("hash-bound but not JSON route summary evidence\n")
        arbitrary_route_artifact["route_summary_path"] = arbitrary_rel
        arbitrary_route_artifact["route_summary_sha256"] = self.sha(arbitrary_path)
        arbitrary_auth = self.materialized_fallback_authorization(arbitrary_route_artifact)
        arbitrary_gate = evaluate_route_closeout_gate(
            route_summaries=[arbitrary_route_artifact],
            fallback_authorization=arbitrary_auth,
            fallback_remediation_rounds=1,
            fallback_authorization_trusted_roots=[self.root],
        )
        self.assertEqual(arbitrary_gate["status"], "ROUTE_CLOSEOUT_GATE_BLOCKED")
        self.assertIn("FALLBACK_AUTHORIZATION_INVALID", {item["code"] for item in arbitrary_gate["blockers"]})

    def test_remediation_route_policy_requires_blk_pipe_route_and_enforces_ceiling(self):
        direct_attempt = {
            "remediation_round": 1,
            "execution_path": "EXTERNAL_CODEX",
            "route_summary": self.successful_route_summary(),
        }
        direct = evaluate_remediation_route_policy(remediation_attempts=[direct_attempt])
        self.assertEqual(direct["status"], "REMEDIATION_ROUTE_POLICY_BLOCKED")
        self.assertIn("REMEDIATION_NOT_ROUTED_THROUGH_BLK_PIPE", {item["code"] for item in direct["blockers"]})

        two_rounds = evaluate_remediation_route_policy(remediation_attempts=[
            {"remediation_round": 1, "execution_path": "BLK_PIPE", "route_summary": self.successful_route_summary(commit_hash="2" * 40)},
            {"remediation_round": 2, "execution_path": "BLK_PIPE", "route_summary": self.successful_route_summary(commit_hash="3" * 40)},
        ])
        self.assertEqual(two_rounds["status"], "REMEDIATION_ROUTE_POLICY_WARNING")
        self.assertTrue(two_rounds["closeout_allowed"])
        self.assertIn("REMEDIATION_SECOND_ROUND_WARNING", {item["code"] for item in two_rounds["warnings"]})

        three_rounds = evaluate_remediation_route_policy(remediation_attempts=[
            {"remediation_round": 1, "execution_path": "BLK_PIPE", "route_summary": self.successful_route_summary(commit_hash="2" * 40)},
            {"remediation_round": 2, "execution_path": "BLK_PIPE", "route_summary": self.successful_route_summary(commit_hash="3" * 40)},
            {"remediation_round": 3, "execution_path": "BLK_PIPE", "route_summary": self.successful_route_summary(commit_hash="4" * 40)},
        ])
        self.assertEqual(three_rounds["status"], "REMEDIATION_ROUTE_POLICY_BLOCKED")
        self.assertIn("REMEDIATION_ROOT_CAUSE_REVIEW_REQUIRED", {item["code"] for item in three_rounds["blockers"]})

        four_rounds = evaluate_remediation_route_policy(remediation_attempts=[
            {"remediation_round": index, "execution_path": "BLK_PIPE", "route_summary": self.successful_route_summary(commit_hash=f"{index}" * 40)}
            for index in range(1, 5)
        ])
        self.assertEqual(four_rounds["status"], "REMEDIATION_ROUTE_POLICY_BLOCKED")
        self.assertIn("REMEDIATION_ROUND_CEILING_EXCEEDED", {item["code"] for item in four_rounds["blockers"]})

    def test_remediation_route_policy_rejects_non_list_sparse_rounds_and_boolean_review(self):
        non_list = evaluate_remediation_route_policy(remediation_attempts={})
        self.assertEqual(non_list["status"], "REMEDIATION_ROUTE_POLICY_BLOCKED")
        self.assertIn("INVALID_REMEDIATION_ATTEMPTS", {item["code"] for item in non_list["blockers"]})

        sparse = evaluate_remediation_route_policy(remediation_attempts=[
            {"remediation_round": 3, "execution_path": "BLK_PIPE", "route_summary": self.successful_route_summary(commit_hash="3" * 40), "root_cause_review": True},
        ])
        self.assertEqual(sparse["status"], "REMEDIATION_ROUTE_POLICY_BLOCKED")
        codes = {item["code"] for item in sparse["blockers"]}
        self.assertIn("NON_CONTIGUOUS_REMEDIATION_ROUNDS", codes)
        self.assertIn("REMEDIATION_ROOT_CAUSE_REVIEW_EVIDENCE_INVALID", codes)

        nonexistent_review = evaluate_remediation_route_policy(remediation_attempts=[
            {"remediation_round": 1, "execution_path": "BLK_PIPE", "route_summary": self.successful_route_summary(commit_hash="1" * 40)},
            {"remediation_round": 2, "execution_path": "BLK_PIPE", "route_summary": self.successful_route_summary(commit_hash="2" * 40)},
            {
                "remediation_round": 3,
                "execution_path": "BLK_PIPE",
                "route_summary": self.successful_route_summary(commit_hash="3" * 40),
                "root_cause_review": {
                    "review_path": str(self.root / "docs" / "missing-root-cause-review.md"),
                    "review_sha256": "sha256:" + "e" * 64,
                    "scope_decision": "continue_with_root_cause_bound",
                },
            },
        ])
        self.assertEqual(nonexistent_review["status"], "REMEDIATION_ROUTE_POLICY_BLOCKED")
        self.assertIn("REMEDIATION_ROOT_CAUSE_REVIEW_EVIDENCE_INVALID", {item["code"] for item in nonexistent_review["blockers"]})

        valid_review = evaluate_remediation_route_policy(remediation_attempts=[
            {"remediation_round": 1, "execution_path": "BLK_PIPE", "route_summary": self.successful_route_summary(commit_hash="1" * 40)},
            {"remediation_round": 2, "execution_path": "BLK_PIPE", "route_summary": self.successful_route_summary(commit_hash="2" * 40)},
            {
                "remediation_round": 3,
                "execution_path": "BLK_PIPE",
                "route_summary": self.successful_route_summary(commit_hash="3" * 40),
                "root_cause_review": self.root_cause_review_evidence(),
            },
        ])
        self.assertEqual(valid_review["status"], "REMEDIATION_ROUTE_POLICY_PASS")
        self.assertTrue(valid_review["closeout_allowed"])

    def test_k2_final_closeout_scan_rejects_primary_route_target_hash_mismatch(self):
        final_text = """---
beo_id: "BEO-K2-024"
status: "closed"
artifact_stage: "final_beo_closeout"
target_hash: "4444444444444444444444444444444444444444"
feature_commit: "2222222222222222222222222222222222222222"
closeout_metadata_commit: "3333333333333333333333333333333333333333"
---
# BEO-K2-024
Final verification complete.
"""
        beo_path = self.root / "BEO-K2-024-route-target-mismatch.md"
        beo_path.write_text(final_text)
        final_sha = self.sha(beo_path)
        roadmap_path = self.root / "K2_implementation-roadmap-route-target-mismatch.md"
        roadmap_path.write_text("first_unconsumed_sequence: null\nclosed: K2-024\n")
        mirror_root = self.root / "Obsidian Vault Route Target" / "Projects" / "Kuronode V2.0" / "04 Execution"
        visible_beo = mirror_root / "BEOs" / "BEO-K2-024.md"
        visible_beo.parent.mkdir(parents=True)
        visible_beo.write_text(
            "> VIEW COPY — DO NOT EDIT\n"
            f"Canonical sha256: {final_sha}\n"
            "Canonical commit: 3333333333333333333333333333333333333333\n"
            "BLK-System consumes the canonical route package, not this Obsidian mirror.\n"
        )

        blocked = scan_k2_final_closeout_artifacts(
            beo_path=beo_path,
            expected_beo_id="BEO-K2-024",
            expected_closeout_metadata_commit="3333333333333333333333333333333333333333",
            expected_final_beo_sha256=final_sha,
            roadmap_paths=[roadmap_path],
            obsidian_execution_root=mirror_root,
            route_summaries=[self.successful_route_summary(
                beb_id="BEB-K2-024",
                beo_id="BEO-K2-024",
                l2_id="L2-K2-024",
                target_hash="9" * 40,
                commit_hash="2" * 40,
            )],
        )

        self.assertEqual(blocked["status"], "K2_FINAL_CLOSEOUT_SCAN_BLOCKED")
        self.assertIn("ROUTE_TARGET_HASH_MISMATCH", {item["code"] for item in blocked["blockers"]})

    def test_k2_final_closeout_scan_rejects_remediation_route_summary_identity_mismatch(self):
        final_text = """---
beo_id: "BEO-K2-024"
status: "closed"
artifact_stage: "final_beo_closeout"
target_hash: "4444444444444444444444444444444444444444"
feature_commit: "2222222222222222222222222222222222222222"
closeout_metadata_commit: "3333333333333333333333333333333333333333"
---
# BEO-K2-024
Final verification complete.
"""
        beo_path = self.root / "BEO-K2-024-remediation-identity.md"
        beo_path.write_text(final_text)
        final_sha = self.sha(beo_path)
        roadmap_path = self.root / "K2_implementation-roadmap-remediation-identity.md"
        roadmap_path.write_text("first_unconsumed_sequence: null\nclosed: K2-024\n")
        mirror_root = self.root / "Obsidian Vault Remediation Identity" / "Projects" / "Kuronode V2.0" / "04 Execution"
        visible_beo = mirror_root / "BEOs" / "BEO-K2-024.md"
        visible_beo.parent.mkdir(parents=True)
        visible_beo.write_text(
            "> VIEW COPY — DO NOT EDIT\n"
            f"Canonical sha256: {final_sha}\n"
            "Canonical commit: 3333333333333333333333333333333333333333\n"
            "BLK-System consumes the canonical route package, not this Obsidian mirror.\n"
        )

        blocked = scan_k2_final_closeout_artifacts(
            beo_path=beo_path,
            expected_beo_id="BEO-K2-024",
            expected_closeout_metadata_commit="3333333333333333333333333333333333333333",
            expected_final_beo_sha256=final_sha,
            roadmap_paths=[roadmap_path],
            obsidian_execution_root=mirror_root,
            route_summaries=[self.successful_route_summary(
                beb_id="BEB-K2-024",
                beo_id="BEO-K2-024",
                l2_id="L2-K2-024",
                target_hash="4" * 40,
                commit_hash="2" * 40,
            )],
            remediation_attempts=[{
                "remediation_round": 1,
                "execution_path": "BLK_PIPE",
                "route_summary": self.successful_route_summary(
                    beb_id="BEB-K2-999",
                    beo_id="BEO-K2-999",
                    l2_id="L2-K2-999",
                    target_hash="9" * 40,
                    commit_hash="3" * 40,
                ),
            }],
        )

        self.assertEqual(blocked["status"], "K2_FINAL_CLOSEOUT_SCAN_BLOCKED")
        self.assertIn("REMEDIATION_ROUTE_POLICY_BLOCKED", {item["code"] for item in blocked["blockers"]})
        self.assertIn("REMEDIATION_ROUTE_SUMMARY_IDENTITY_MISMATCH", {item["code"] for item in blocked["remediation_route_policy"]["blockers"]})

    def test_route_closeout_gate_accepts_only_explicit_one_off_fallback_exception(self):
        failed = self.failed_route_summary_with_artifact()
        generic = self.materialized_fallback_authorization(
            failed,
            authorization_scope="GENERIC_FALLBACK_ALLOWED",
        )
        generic_gate = evaluate_route_closeout_gate(
            route_summaries=[failed],
            fallback_authorization=generic,
            fallback_remediation_rounds=1,
            fallback_authorization_trusted_roots=[self.root],
        )
        self.assertEqual(generic_gate["status"], "ROUTE_CLOSEOUT_GATE_BLOCKED")
        self.assertFalse(generic_gate["fallback_exception_allowed"])
        self.assertIn("FALLBACK_AUTHORIZATION_INVALID", {item["code"] for item in generic_gate["blockers"]})

        valid_gate = evaluate_route_closeout_gate(
            route_summaries=[failed],
            fallback_authorization=self.materialized_fallback_authorization(failed),
            fallback_remediation_rounds=1,
            fallback_authorization_trusted_roots=[self.root],
        )
        self.assertEqual(valid_gate["status"], "ROUTE_CLOSEOUT_GATE_FALLBACK_EXCEPTION")
        self.assertFalse(valid_gate["normal_closeout_allowed"])
        self.assertTrue(valid_gate["fallback_exception_allowed"])
        self.assertTrue(valid_gate["external_codex_fallback_authorized"])
        self.assertEqual(valid_gate["required_action"], "fallback_exception_closeout_only")

        over_ceiling = evaluate_route_closeout_gate(
            route_summaries=[failed],
            fallback_authorization=self.materialized_fallback_authorization(failed, max_remediation_rounds=2),
            fallback_remediation_rounds=3,
            fallback_authorization_trusted_roots=[self.root],
        )
        self.assertEqual(over_ceiling["status"], "ROUTE_CLOSEOUT_GATE_BLOCKED")
        self.assertIn("FALLBACK_REMEDIATION_CEILING_EXCEEDED", {item["code"] for item in over_ceiling["blockers"]})

        missing_denial = self.materialized_fallback_authorization(
            failed,
            denied_authorities=["BEO_PUBLICATION", "RTM_GENERATION"],
        )
        missing_denial_gate = evaluate_route_closeout_gate(
            route_summaries=[failed],
            fallback_authorization=missing_denial,
            fallback_remediation_rounds=1,
            fallback_authorization_trusted_roots=[self.root],
        )
        self.assertIn("FALLBACK_AUTHORIZATION_INVALID", {item["code"] for item in missing_denial_gate["blockers"]})

        malformed_denial = self.materialized_fallback_authorization(
            failed,
            denied_authorities=[{"authority": "BEO_PUBLICATION"}],
        )
        malformed_denial_gate = evaluate_route_closeout_gate(
            route_summaries=[failed],
            fallback_authorization=malformed_denial,
            fallback_remediation_rounds=1,
            fallback_authorization_trusted_roots=[self.root],
        )
        self.assertEqual(malformed_denial_gate["status"], "ROUTE_CLOSEOUT_GATE_BLOCKED")
        self.assertIn("FALLBACK_AUTHORIZATION_INVALID", {item["code"] for item in malformed_denial_gate["blockers"]})

    def test_k2_final_closeout_scan_requires_route_closeout_gate_evidence(self):
        final_text = """---
beo_id: "BEO-K2-024"
status: "closed"
artifact_stage: "final_beo_closeout"
target_hash: "4444444444444444444444444444444444444444"
feature_commit: "2222222222222222222222222222222222222222"
closeout_metadata_commit: "3333333333333333333333333333333333333333"
---
# BEO-K2-024
Final verification complete.
"""
        beo_path = self.root / "BEO-K2-024.md"
        beo_path.write_text(final_text)
        final_sha = self.sha(beo_path)
        roadmap_path = self.root / "K2_implementation-roadmap.md"
        roadmap_path.write_text("first_unconsumed_sequence: null\nclosed: K2-024\n")
        mirror_root = self.root / "Obsidian Vault" / "Projects" / "Kuronode V2.0" / "04 Execution"
        visible_beo = mirror_root / "BEOs" / "BEO-K2-024.md"
        visible_beo.parent.mkdir(parents=True)
        visible_beo.write_text(
            "> VIEW COPY — DO NOT EDIT\n"
            f"Canonical sha256: {final_sha}\n"
            "Canonical commit: 3333333333333333333333333333333333333333\n"
            "BLK-System consumes the canonical route package, not this Obsidian mirror.\n"
        )

        missing_route_gate = scan_k2_final_closeout_artifacts(
            beo_path=beo_path,
            expected_beo_id="BEO-K2-024",
            expected_closeout_metadata_commit="3333333333333333333333333333333333333333",
            expected_final_beo_sha256=final_sha,
            roadmap_paths=[roadmap_path],
            obsidian_execution_root=mirror_root,
        )
        self.assertIn("MISSING_ROUTE_CLOSEOUT_GATE_EVIDENCE", {item["code"] for item in missing_route_gate["blockers"]})

        failed_route_gate = scan_k2_final_closeout_artifacts(
            beo_path=beo_path,
            expected_beo_id="BEO-K2-024",
            expected_closeout_metadata_commit="3333333333333333333333333333333333333333",
            expected_final_beo_sha256=final_sha,
            roadmap_paths=[roadmap_path],
            obsidian_execution_root=mirror_root,
            route_summaries=[self.failed_route_summary()],
        )
        self.assertIn("ROUTE_CLOSEOUT_GATE_BLOCKED", {item["code"] for item in failed_route_gate["blockers"]})

        malformed_fallback_gate = scan_k2_final_closeout_artifacts(
            beo_path=beo_path,
            expected_beo_id="BEO-K2-024",
            expected_closeout_metadata_commit="3333333333333333333333333333333333333333",
            expected_final_beo_sha256=final_sha,
            roadmap_paths=[roadmap_path],
            obsidian_execution_root=mirror_root,
            route_summaries=[
                self.failed_route_summary(status="ENGINE_TIMEOUT", exit_code=124, target_hash="not-a-git-hash")
            ],
            fallback_authorization=self.valid_fallback_authorization(),
            fallback_remediation_rounds=1,
        )
        self.assertIn("ROUTE_CLOSEOUT_GATE_BLOCKED", {item["code"] for item in malformed_fallback_gate["blockers"]})
        self.assertEqual(malformed_fallback_gate["route_closeout_gate"]["status"], "ROUTE_CLOSEOUT_GATE_BLOCKED")

        missing_target_fallback_gate = scan_k2_final_closeout_artifacts(
            beo_path=beo_path,
            expected_beo_id="BEO-K2-024",
            expected_closeout_metadata_commit="3333333333333333333333333333333333333333",
            expected_final_beo_sha256=final_sha,
            roadmap_paths=[roadmap_path],
            obsidian_execution_root=mirror_root,
            route_summaries=[
                self.failed_route_summary(status="ENGINE_TIMEOUT", exit_code=124, target_hash="")
            ],
            fallback_authorization=self.valid_fallback_authorization(),
            fallback_remediation_rounds=1,
        )
        self.assertIn("ROUTE_CLOSEOUT_GATE_BLOCKED", {item["code"] for item in missing_target_fallback_gate["blockers"]})
        self.assertEqual(missing_target_fallback_gate["route_closeout_gate"]["status"], "ROUTE_CLOSEOUT_GATE_BLOCKED")

        wrong_identity_route_gate = scan_k2_final_closeout_artifacts(
            beo_path=beo_path,
            expected_beo_id="BEO-K2-024",
            expected_closeout_metadata_commit="3333333333333333333333333333333333333333",
            expected_final_beo_sha256=final_sha,
            roadmap_paths=[roadmap_path],
            obsidian_execution_root=mirror_root,
            route_summaries=[self.successful_route_summary()],
        )
        self.assertIn("ROUTE_SUMMARY_IDENTITY_MISMATCH", {item["code"] for item in wrong_identity_route_gate["blockers"]})

        passed = scan_k2_final_closeout_artifacts(
            beo_path=beo_path,
            expected_beo_id="BEO-K2-024",
            expected_closeout_metadata_commit="3333333333333333333333333333333333333333",
            expected_final_beo_sha256=final_sha,
            roadmap_paths=[roadmap_path],
            obsidian_execution_root=mirror_root,
            route_summaries=[
                self.successful_route_summary(
                    beb_id="BEB-K2-024",
                    beo_id="BEO-K2-024",
                    l2_id="L2-K2-024",
                    target_hash="4" * 40,
                    commit_hash="2" * 40,
                )
            ],
        )
        self.assertEqual(passed["status"], "K2_FINAL_CLOSEOUT_SCAN_PASS")
        self.assertTrue(passed["route_closeout_gate"]["normal_closeout_allowed"])

    def test_k2_final_closeout_scan_blocks_toxic_fallback_wording_without_route_pass_or_record(self):
        final_text = """---
beo_id: "BEO-K2-024"
status: "closed"
artifact_stage: "final_beo_closeout"
target_hash: "4444444444444444444444444444444444444444"
feature_commit: "2222222222222222222222222222222222222222"
closeout_metadata_commit: "3333333333333333333333333333333333333333"
---
# BEO-K2-024
This closeout mentions supervised external Codex fallback after ENGINE_TIMEOUT and commit_hash: "".
"""
        beo_path = self.root / "BEO-K2-024-toxic.md"
        beo_path.write_text(final_text)
        final_sha = self.sha(beo_path)
        roadmap_path = self.root / "K2_implementation-roadmap-toxic.md"
        roadmap_path.write_text("first_unconsumed_sequence: null\nclosed: K2-024\n")
        mirror_root = self.root / "Obsidian Vault Toxic" / "Projects" / "Kuronode V2.0" / "04 Execution"
        visible_beo = mirror_root / "BEOs" / "BEO-K2-024.md"
        visible_beo.parent.mkdir(parents=True)
        visible_beo.write_text(
            "> VIEW COPY — DO NOT EDIT\n"
            f"Canonical sha256: {final_sha}\n"
            "Canonical commit: 3333333333333333333333333333333333333333\n"
            "BLK-System consumes the canonical route package, not this Obsidian mirror.\n"
        )
        closeout_path = self.root / "K2-024-closeout-toxic.md"
        closeout_path.write_text("fallback-remediation used no route commit\n")

        blocked = scan_k2_final_closeout_artifacts(
            beo_path=beo_path,
            expected_beo_id="BEO-K2-024",
            expected_closeout_metadata_commit="3333333333333333333333333333333333333333",
            expected_final_beo_sha256=final_sha,
            roadmap_paths=[roadmap_path],
            obsidian_execution_root=mirror_root,
            route_summaries=[self.failed_route_summary(status="ENGINE_TIMEOUT", exit_code=124)],
            closeout_paths=[closeout_path],
        )
        blocker_codes = {item["code"] for item in blocked["blockers"]}
        self.assertIn("ROUTE_CLOSEOUT_GATE_BLOCKED", blocker_codes)
        self.assertIn("FALLBACK_WORDING_REQUIRES_ROUTE_GATE_EVIDENCE", blocker_codes)
        self.assertFalse(blocked["fallback_wording_scan"]["fallback_wording_allowed"])

        passed = scan_k2_final_closeout_artifacts(
            beo_path=beo_path,
            expected_beo_id="BEO-K2-024",
            expected_closeout_metadata_commit="3333333333333333333333333333333333333333",
            expected_final_beo_sha256=final_sha,
            roadmap_paths=[roadmap_path],
            obsidian_execution_root=mirror_root,
            route_summaries=[self.successful_route_summary(
                beb_id="BEB-K2-024",
                beo_id="BEO-K2-024",
                l2_id="L2-K2-024",
                target_hash="4" * 40,
                commit_hash="2" * 40,
            )],
            closeout_paths=[closeout_path],
        )
        self.assertEqual(passed["status"], "K2_FINAL_CLOSEOUT_SCAN_PASS")
        self.assertTrue(passed["fallback_wording_scan"]["fallback_wording_allowed"])

    def test_k2_final_closeout_scan_blocks_fallback_wording_variants_and_discovers_closeout_files(self):
        final_text = """---
beo_id: "BEO-K2-024"
status: "closed"
artifact_stage: "final_beo_closeout"
target_hash: "4444444444444444444444444444444444444444"
feature_commit: "2222222222222222222222222222222222222222"
closeout_metadata_commit: "3333333333333333333333333333333333333333"
---
# BEO-K2-024
Engine timeout left the route blocked and the source worktree was git dirty.
"""
        beo_path = self.root / "BEO-K2-024-wording-variants.md"
        beo_path.write_text(final_text)
        final_sha = self.sha(beo_path)
        (self.root / "K2-024_sprint-closeout.md").write_text("external Codex fallback with no-route commit\n")
        roadmap_path = self.root / "K2_implementation-roadmap-wording-variants.md"
        roadmap_path.write_text("first_unconsumed_sequence: null\nclosed: K2-024\n")
        mirror_root = self.root / "Obsidian Vault Wording Variants" / "Projects" / "Kuronode V2.0" / "04 Execution"
        visible_beo = mirror_root / "BEOs" / "BEO-K2-024.md"
        visible_beo.parent.mkdir(parents=True)
        visible_beo.write_text(
            "> VIEW COPY — DO NOT EDIT\n"
            f"Canonical sha256: {final_sha}\n"
            "Canonical commit: 3333333333333333333333333333333333333333\n"
            "BLK-System consumes the canonical route package, not this Obsidian mirror.\n"
        )

        blocked = scan_k2_final_closeout_artifacts(
            beo_path=beo_path,
            expected_beo_id="BEO-K2-024",
            expected_closeout_metadata_commit="3333333333333333333333333333333333333333",
            expected_final_beo_sha256=final_sha,
            roadmap_paths=[roadmap_path],
            obsidian_execution_root=mirror_root,
            route_summaries=[self.failed_route_summary(status="ENGINE_TIMEOUT", exit_code=124)],
        )
        self.assertEqual(blocked["status"], "K2_FINAL_CLOSEOUT_SCAN_BLOCKED")
        blocker_codes = {item["code"] for item in blocked["blockers"]}
        self.assertIn("FALLBACK_WORDING_REQUIRES_ROUTE_GATE_EVIDENCE", blocker_codes)
        markers = {match["marker"] for match in blocked["fallback_wording_scan"]["matches"]}
        self.assertIn("engine timeout", markers)
        self.assertIn("git dirty", markers)
        self.assertIn("external Codex fallback", markers)
        self.assertIn("no-route commit", markers)

    def test_k2_final_closeout_scan_blocks_non_blk_pipe_remediation_attempts(self):
        final_text = """---
beo_id: "BEO-K2-024"
status: "closed"
artifact_stage: "final_beo_closeout"
target_hash: "4444444444444444444444444444444444444444"
feature_commit: "2222222222222222222222222222222222222222"
closeout_metadata_commit: "3333333333333333333333333333333333333333"
---
# BEO-K2-024
Final verification complete.
"""
        beo_path = self.root / "BEO-K2-024-remediation.md"
        beo_path.write_text(final_text)
        final_sha = self.sha(beo_path)
        roadmap_path = self.root / "K2_implementation-roadmap-remediation.md"
        roadmap_path.write_text("first_unconsumed_sequence: null\nclosed: K2-024\n")
        mirror_root = self.root / "Obsidian Vault Remediation" / "Projects" / "Kuronode V2.0" / "04 Execution"
        visible_beo = mirror_root / "BEOs" / "BEO-K2-024.md"
        visible_beo.parent.mkdir(parents=True)
        visible_beo.write_text(
            "> VIEW COPY — DO NOT EDIT\n"
            f"Canonical sha256: {final_sha}\n"
            "Canonical commit: 3333333333333333333333333333333333333333\n"
            "BLK-System consumes the canonical route package, not this Obsidian mirror.\n"
        )

        blocked = scan_k2_final_closeout_artifacts(
            beo_path=beo_path,
            expected_beo_id="BEO-K2-024",
            expected_closeout_metadata_commit="3333333333333333333333333333333333333333",
            expected_final_beo_sha256=final_sha,
            roadmap_paths=[roadmap_path],
            obsidian_execution_root=mirror_root,
            route_summaries=[self.successful_route_summary(
                beb_id="BEB-K2-024",
                beo_id="BEO-K2-024",
                l2_id="L2-K2-024",
                target_hash="4" * 40,
                commit_hash="2" * 40,
            )],
            remediation_attempts=[{
                "remediation_round": 1,
                "execution_path": "EXTERNAL_CODEX",
                "route_summary": self.successful_route_summary(
                    beb_id="BEB-K2-024",
                    beo_id="BEO-K2-024",
                    l2_id="L2-K2-024",
                    target_hash="4" * 40,
                    commit_hash="3" * 40,
                ),
            }],
        )

        self.assertEqual(blocked["status"], "K2_FINAL_CLOSEOUT_SCAN_BLOCKED")
        self.assertIn("REMEDIATION_ROUTE_POLICY_BLOCKED", {item["code"] for item in blocked["blockers"]})
        self.assertEqual(blocked["remediation_route_policy"]["status"], "REMEDIATION_ROUTE_POLICY_BLOCKED")

    def test_k2_final_closeout_scan_checks_beo_hash_roadmap_and_visible_mirrors(self):
        final_text = """---
beo_id: "BEO-K2-023"
status: "closed"
artifact_stage: "final_beo_closeout"
target_hash: "68a9b8c0b9b056a9c8a80d8bae32c093ade4c8e6"
feature_commit: "c4229129560eb3da39f9b4f652f258dcc156f245"
closeout_metadata_commit: "3a22c82a53d8751297f618e05a209a3e232a0203"
---
# BEO-K2-023
Final verification complete.
"""
        beo_path = self.root / "BEO-K2-023.md"
        beo_path.write_text(final_text)
        final_sha = self.sha(beo_path)
        roadmap_path = self.root / "K2_implementation-roadmap.md"
        roadmap_path.write_text("first_unconsumed_sequence: null\nclosed: K2-023\n")
        mirror_root = self.root / "Obsidian Vault" / "Projects" / "Kuronode V2.0" / "04 Execution"
        visible_beo = mirror_root / "BEOs" / "BEO-K2-023.md"
        visible_beo.parent.mkdir(parents=True)
        visible_beo.write_text(
            "> VIEW COPY — DO NOT EDIT\n"
            f"Canonical sha256: {final_sha}\n"
            "Canonical commit: eaa41f07bcf98cf2be962f03aa61fdb67d55757a\n"
            "BLK-System consumes the canonical route package, not this Obsidian mirror.\n"
        )
        bdoc = mirror_root / "BDOCs" / "BDOC-K2-023" / "K2-023_hostile-review-remediation-001-blockers.md"
        bdoc.parent.mkdir(parents=True)
        bdoc.write_text("remediation blocker note; not a visible BEO\n")

        passed = scan_k2_final_closeout_artifacts(
            beo_path=beo_path,
            expected_beo_id="BEO-K2-023",
            expected_closeout_metadata_commit="3a22c82a53d8751297f618e05a209a3e232a0203",
            expected_final_beo_sha256=final_sha,
            roadmap_paths=[roadmap_path],
            obsidian_execution_root=mirror_root,
            route_summaries=[self.successful_route_summary(target_hash="68a9b8c0b9b056a9c8a80d8bae32c093ade4c8e6")],
        )

        self.assertEqual(passed["status"], "K2_FINAL_CLOSEOUT_SCAN_PASS")
        self.assertTrue(passed["hash_reconciliation_allowed"])
        self.assertEqual(passed["final_beo_sha256"], final_sha)
        self.assertEqual(passed["visible_beo_mirror_count"], 1)
        self.assertFalse(passed["beo_publication_authorized"])
        self.assertFalse(passed["rtm_generation_authorized"])
        self.assertFalse(passed["next_k2_selection_authorized"])

        visible_beo.write_text(
            "> VIEW COPY — DO NOT EDIT\n"
            f"Canonical sha256: {final_sha}\n"
            "Canonical commit: \n"
            "BLK-System consumes the canonical route package, not this Obsidian mirror.\n"
        )
        blank_mirror_commit = scan_k2_final_closeout_artifacts(
            beo_path=beo_path,
            expected_beo_id="BEO-K2-023",
            expected_closeout_metadata_commit="3a22c82a53d8751297f618e05a209a3e232a0203",
            expected_final_beo_sha256=final_sha,
            roadmap_paths=[roadmap_path],
            obsidian_execution_root=mirror_root,
        )
        self.assertIn("OBSIDIAN_BEO_MIRROR_COMMIT_MISMATCH", {item["code"] for item in blank_mirror_commit["blockers"]})
        visible_beo.write_text(
            "> VIEW COPY — DO NOT EDIT\n"
            f"Canonical sha256: {final_sha}\n"
            "Canonical commit: eaa41f07bcf98cf2be962f03aa61fdb67d55757a\n"
            "BLK-System consumes the canonical route package, not this Obsidian mirror.\n"
        )

        missing_context = scan_k2_final_closeout_artifacts(
            beo_path=beo_path,
            expected_beo_id="BEO-K2-023",
            expected_closeout_metadata_commit="3a22c82a53d8751297f618e05a209a3e232a0203",
            expected_final_beo_sha256=final_sha,
        )
        self.assertIn("MISSING_ROADMAP_PATHS", {item["code"] for item in missing_context["blockers"]})
        self.assertIn("MISSING_OBSIDIAN_EXECUTION_ROOT", {item["code"] for item in missing_context["blockers"]})

        missing_sha = scan_k2_final_closeout_artifacts(
            beo_path=beo_path,
            expected_beo_id="BEO-K2-023",
            expected_closeout_metadata_commit="3a22c82a53d8751297f618e05a209a3e232a0203",
            roadmap_paths=[roadmap_path],
            obsidian_execution_root=mirror_root,
        )
        self.assertIn("EXPECTED_FINAL_BEO_SHA_REQUIRED", {item["code"] for item in missing_sha["blockers"]})

        roadmap_path.write_text("closed: K2-023\n")
        missing_null = scan_k2_final_closeout_artifacts(
            beo_path=beo_path,
            expected_beo_id="BEO-K2-023",
            expected_closeout_metadata_commit="3a22c82a53d8751297f618e05a209a3e232a0203",
            expected_final_beo_sha256=final_sha,
            roadmap_paths=[roadmap_path],
            obsidian_execution_root=mirror_root,
        )
        self.assertIn("MISSING_FIRST_UNCONSUMED_SEQUENCE_NULL", {item["code"] for item in missing_null["blockers"]})

        roadmap_path.write_text("first_unconsumed_sequence: none\nclosed: K2-023\n")
        none_sequence = scan_k2_final_closeout_artifacts(
            beo_path=beo_path,
            expected_beo_id="BEO-K2-023",
            expected_closeout_metadata_commit="3a22c82a53d8751297f618e05a209a3e232a0203",
            expected_final_beo_sha256=final_sha,
            roadmap_paths=[roadmap_path],
            obsidian_execution_root=mirror_root,
        )
        self.assertIn("NEXT_K2_SEQUENCE_STILL_SELECTED", {item["code"] for item in none_sequence["blockers"]})

        roadmap_path.write_text("first_unconsumed_sequence: # blank is not explicit null\nclosed: K2-023\n")
        blank_sequence = scan_k2_final_closeout_artifacts(
            beo_path=beo_path,
            expected_beo_id="BEO-K2-023",
            expected_closeout_metadata_commit="3a22c82a53d8751297f618e05a209a3e232a0203",
            expected_final_beo_sha256=final_sha,
            roadmap_paths=[roadmap_path],
            obsidian_execution_root=mirror_root,
        )
        self.assertIn("NEXT_K2_SEQUENCE_STILL_SELECTED", {item["code"] for item in blank_sequence["blockers"]})

        roadmap_path.write_text("first_unconsumed_sequence: NULL\nclosed: K2-023\n")
        uppercase_null = scan_k2_final_closeout_artifacts(
            beo_path=beo_path,
            expected_beo_id="BEO-K2-023",
            expected_closeout_metadata_commit="3a22c82a53d8751297f618e05a209a3e232a0203",
            expected_final_beo_sha256=final_sha,
            roadmap_paths=[roadmap_path],
            obsidian_execution_root=mirror_root,
        )
        self.assertIn("NEXT_K2_SEQUENCE_STILL_SELECTED", {item["code"] for item in uppercase_null["blockers"]})

        roadmap_path.write_text("first_unconsumed_sequence: null # comment not exact\nclosed: K2-023\n")
        commented_null = scan_k2_final_closeout_artifacts(
            beo_path=beo_path,
            expected_beo_id="BEO-K2-023",
            expected_closeout_metadata_commit="3a22c82a53d8751297f618e05a209a3e232a0203",
            expected_final_beo_sha256=final_sha,
            roadmap_paths=[roadmap_path],
            obsidian_execution_root=mirror_root,
        )
        self.assertIn("NEXT_K2_SEQUENCE_STILL_SELECTED", {item["code"] for item in commented_null["blockers"]})

        roadmap_path.write_text(" first_unconsumed_sequence: null\nclosed: K2-023\n")
        leading_space_null = scan_k2_final_closeout_artifacts(
            beo_path=beo_path,
            expected_beo_id="BEO-K2-023",
            expected_closeout_metadata_commit="3a22c82a53d8751297f618e05a209a3e232a0203",
            expected_final_beo_sha256=final_sha,
            roadmap_paths=[roadmap_path],
            obsidian_execution_root=mirror_root,
        )
        self.assertIn("NEXT_K2_SEQUENCE_STILL_SELECTED", {item["code"] for item in leading_space_null["blockers"]})

        roadmap_path.write_text("first_unconsumed_sequence: null \nclosed: K2-023\n")
        trailing_space_null = scan_k2_final_closeout_artifacts(
            beo_path=beo_path,
            expected_beo_id="BEO-K2-023",
            expected_closeout_metadata_commit="3a22c82a53d8751297f618e05a209a3e232a0203",
            expected_final_beo_sha256=final_sha,
            roadmap_paths=[roadmap_path],
            obsidian_execution_root=mirror_root,
        )
        self.assertIn("NEXT_K2_SEQUENCE_STILL_SELECTED", {item["code"] for item in trailing_space_null["blockers"]})

        roadmap_path.write_text("first_unconsumed_sequence: null\nFIRST_UNCONSUMED_SEQUENCE: 024\nclosed: K2-023\n")
        uppercase_duplicate = scan_k2_final_closeout_artifacts(
            beo_path=beo_path,
            expected_beo_id="BEO-K2-023",
            expected_closeout_metadata_commit="3a22c82a53d8751297f618e05a209a3e232a0203",
            expected_final_beo_sha256=final_sha,
            roadmap_paths=[roadmap_path],
            obsidian_execution_root=mirror_root,
        )
        self.assertIn("NEXT_K2_SEQUENCE_STILL_SELECTED", {item["code"] for item in uppercase_duplicate["blockers"]})

        visible_beo.write_text(
            "> VIEW COPY — DO NOT EDIT\n"
            "Canonical sha256: \n"
            "Canonical commit: eaa41f07bcf98cf2be962f03aa61fdb67d55757a\n"
            "BLK-System consumes the canonical route package, not this Obsidian mirror.\n"
        )
        blank_mirror_sha = scan_k2_final_closeout_artifacts(
            beo_path=beo_path,
            expected_beo_id="BEO-K2-023",
            expected_closeout_metadata_commit="3a22c82a53d8751297f618e05a209a3e232a0203",
            expected_final_beo_sha256=final_sha,
            roadmap_paths=[roadmap_path],
            obsidian_execution_root=mirror_root,
        )
        self.assertIn("OBSIDIAN_BEO_MIRROR_SHA_MISMATCH", {item["code"] for item in blank_mirror_sha["blockers"]})

        visible_beo.write_text(
            "> VIEW COPY — DO NOT EDIT\n"
            f"Canonical sha256: {final_sha}\n"
            "Canonical commit: eaa41f07bcf98cf2be962f03aa61fdb67d55757a\n"
            "BLK-System consumes the canonical route package, not this Obsidian mirror.\n"
        )
        roadmap_path.write_text("first_unconsumed_sequence: 024\nK2-024 pending dispatch\n")
        extra_visible = mirror_root / "BEOs" / "BEO-K2-023_Hostile_Review_Remediation_001.md"
        extra_visible.write_text(
            "> VIEW COPY — DO NOT EDIT\n"
            f"Canonical sha256: {final_sha}\n"
            "remediation template incorrectly visible as a BEO\n"
        )
        roadmap_path.write_text("first_unconsumed_sequence: 024\nK2-024 pending dispatch\n")
        blocked = scan_k2_final_closeout_artifacts(
            beo_path=beo_path,
            expected_beo_id="BEO-K2-023",
            expected_closeout_metadata_commit="3a22c82a53d8751297f618e05a209a3e232a0203",
            expected_final_beo_sha256=final_sha,
            roadmap_paths=[roadmap_path],
            obsidian_execution_root=mirror_root,
        )
        blocker_codes = {item["code"] for item in blocked["blockers"]}
        self.assertEqual(blocked["status"], "K2_FINAL_CLOSEOUT_SCAN_BLOCKED")
        self.assertIn("VISIBLE_BEO_MIRROR_COUNT", blocker_codes)
        self.assertIn("NEXT_K2_SEQUENCE_STILL_SELECTED", blocker_codes)

    def test_prepare_drop_package_refuses_symlinked_package_dir(self):
        target_hash = self.init_git_workdir()
        real_dir = self.root / "real-package-root"
        real_dir.mkdir()
        symlink_dir = self.root / "symlink-package-root"
        symlink_dir.symlink_to(real_dir, target_is_directory=True)
        with self.assertRaisesRegex(RouteError, "BEB-L2 package_dir must not contain symlinked components"):
            prepare_beb_l2_drop_package(
                package_dir=symlink_dir / "BEB-TST-005",
                beb_id="BEB-TST-005",
                l2_id="L2-TST-005",
                work_dir=self.work_dir,
                target_branch="sprint/beb-222",
                target_hash=target_hash,
                objective="Add a synthetic TST-family capability through the governed route.",
                l2_instructions="Modify only approved files and preserve the route boundary.",
                allowed_modified_files=["src/components/CanonicalDataGrid.tsx"],
                allowed_new_files=[],
                validation_profiles=["python-unittest"],
                trace_artifacts=TRACE_ARTIFACTS,
            )

    def test_obsidian_mirror_refuses_symlinked_roots_and_non_generated_overwrites(self):
        target_hash = self.init_git_workdir()
        package_dir = self.root / "packages" / "BEB-TST-001"
        real_mirror_dir = self.root / "real-obsidian-mirror"
        real_mirror_dir.mkdir()
        symlinked_mirror_dir = self.root / "symlinked-obsidian-mirror"
        symlinked_mirror_dir.symlink_to(real_mirror_dir, target_is_directory=True)

        with self.assertRaisesRegex(RouteError, "Obsidian mirror_dir must not contain symlinked components"):
            prepare_beb_l2_drop_package(
                package_dir=package_dir,
                beb_id="BEB-TST-001",
                l2_id="L2-TST-001",
                work_dir=self.work_dir,
                target_branch="sprint/beb-222",
                target_hash=target_hash,
                objective="Add provider readiness status display through the governed Kuronode V2 route.",
                l2_instructions="Modify only the approved provider-readiness files and keep validation green.",
                allowed_modified_files=["src/components/CanonicalDataGrid.tsx"],
                allowed_new_files=[],
                validation_profiles=["python-unittest"],
                trace_artifacts=TRACE_ARTIFACTS,
                artifact_slug="Provider_Readiness_Status_Display",
                obsidian_mirror_dir=symlinked_mirror_dir,
            )

        mirror_dir = self.root / "Obsidian Vault" / "Projects" / "Kuronode V2.0" / "03 Implementation" / "Execution Mirrors"
        mirror_dir.mkdir(parents=True)
        existing_note = mirror_dir / "BEB-TST-001_Provider_Readiness_Status_Display.md"
        existing_note.write_text("operator-owned note; do not clobber\n")

        with self.assertRaisesRegex(RouteError, "existing Obsidian mirror destination is not a generated view copy"):
            prepare_beb_l2_drop_package(
                package_dir=package_dir,
                beb_id="BEB-TST-001",
                l2_id="L2-TST-001",
                work_dir=self.work_dir,
                target_branch="sprint/beb-222",
                target_hash=target_hash,
                objective="Add provider readiness status display through the governed Kuronode V2 route.",
                l2_instructions="Modify only the approved provider-readiness files and keep validation green.",
                allowed_modified_files=["src/components/CanonicalDataGrid.tsx"],
                allowed_new_files=[],
                validation_profiles=["python-unittest"],
                trace_artifacts=TRACE_ARTIFACTS,
                artifact_slug="Provider_Readiness_Status_Display",
                obsidian_mirror_dir=mirror_dir,
            )
        self.assertEqual(existing_note.read_text(), "operator-owned note; do not clobber\n")

    def test_prepare_beb_l2_drop_package_rejects_caller_controlled_manifest_fields(self):
        target_hash = self.init_git_workdir()

        with self.assertRaisesRegex(RouteError, "caller-controlled"):
            prepare_beb_l2_drop_package(
                package_dir=self.root / "packages" / "bad",
                beb_id="BEB_232",
                l2_id="L2_232",
                work_dir=self.work_dir,
                target_branch="sprint/beb-222",
                target_hash=target_hash,
                objective="bad package",
                l2_instructions="bad package",
                allowed_modified_files=["src/components/CanonicalDataGrid.tsx"],
                allowed_new_files=[],
                validation_profiles=["python-unittest"],
                trace_artifacts=TRACE_ARTIFACTS,
                extra_manifest_fields={"engine": "sh", "l2_packet": "manual bypass"},
            )

    def test_prepare_beb_l2_drop_package_rejects_canonical_manifest_overrides(self):
        target_hash = self.init_git_workdir()
        attacker_l2 = self.root / "attacker-L2.md"
        attacker_l2.write_text("L2_ID: L2_232\nBEB_ID: BEB_232\nMODEL: gpt-5.5\nBypass helper packet.\n")

        with self.assertRaisesRegex(RouteError, "canonical manifest fields"):
            prepare_beb_l2_drop_package(
                package_dir=self.root / "packages" / "bad-canonical",
                beb_id="BEB_232",
                l2_id="L2_232",
                work_dir=self.work_dir,
                target_branch="sprint/beb-222",
                target_hash=target_hash,
                objective="bad package",
                l2_instructions="safe helper packet",
                allowed_modified_files=["src/components/CanonicalDataGrid.tsx"],
                allowed_new_files=[],
                validation_profiles=["python-unittest"],
                trace_artifacts=TRACE_ARTIFACTS,
                extra_manifest_fields={"l2_path": str(attacker_l2), "l2_sha256": self.sha(attacker_l2)},
            )

    def test_preflight_blocks_kuronode_dependency_cache_before_codex(self):
        self.init_git_workdir(ignored=True)

        report = preflight_drop_file(self.drop_path, **self.route_kwargs())

        self.assertEqual(report["status"], "BLOCKED")
        blocker_codes = {blocker["code"] for blocker in report["blockers"]}
        self.assertIn("PREEXISTING_IGNORED_OR_UNTRACKED", blocker_codes)
        self.assertTrue(any("node_modules" in path for blocker in report["blockers"] for path in blocker["paths"]))

    def test_preflight_recommends_default_clean_worktree_when_ignored_residue_blocks_k2_dispatch(self):
        target_hash = self.init_git_workdir(ignored=True)

        report = preflight_drop_file(self.drop_path, **self.route_kwargs())

        self.assertEqual(report["status"], "BLOCKED")
        self.assertTrue(report["clean_worktree_retarget_recommended"])
        self.assertEqual(report["default_clean_worktree_root"], "/tmp/blk-system-clean-worktrees")
        self.assertTrue(report["default_clean_worktree_path"].endswith(f"kuronode-beb-222-{target_hash[:12]}"))
        self.assertFalse(report["source_cleanup_authorized"])
        self.assertFalse(report["worktree_creation_authorized"])
        self.assertFalse(report["dispatch_authorized"])

    def test_preflight_reports_blk_pipe_clean_preflight_parity_for_agent_residue(self):
        self.init_git_workdir()
        subprocess.run(
            ["git", "config", "--local", "status.showUntrackedFiles", "no"],
            cwd=self.work_dir,
            check=True,
        )
        for residue_dir in (".agents", ".codex"):
            residue_file = self.work_dir / residue_dir / "session.jsonl"
            residue_file.parent.mkdir(parents=True, exist_ok=True)
            residue_file.write_text("operator-local residue must block before BLK-pipe\n")

        report = preflight_drop_file(self.drop_path, **self.route_kwargs())

        self.assertEqual(report["status"], "BLOCKED")
        self.assertIn("GIT_DIRTY", {blocker["code"] for blocker in report["blockers"]})
        dirty_paths = {path for blocker in report["blockers"] if blocker["code"] == "GIT_DIRTY" for path in blocker["paths"]}
        self.assertTrue(any(path.startswith(".agents/") for path in dirty_paths), dirty_paths)
        self.assertTrue(any(path.startswith(".codex/") for path in dirty_paths), dirty_paths)
        parity = report["clean_preflight_parity"]
        self.assertEqual(parity["source"], "internal/gitguard.EnsureClean")
        self.assertEqual(parity["gitguard_command"], ["git", "status", "--porcelain", "--untracked-files=all"])
        self.assertTrue(parity["would_blk_pipe_git_dirty"])
        self.assertEqual(parity["recommended_action"], "retarget_to_trusted_sterile_clean_worktree")

    def test_cleanup_plan_reports_dry_run_paths_without_removing_ignored_residue(self):
        self.init_git_workdir(ignored=True)
        ignored_file = self.work_dir / "node_modules" / "left-pad" / "index.js"

        plan = build_ignored_residue_cleanup_plan(self.drop_path, **self.route_kwargs())

        self.assertEqual(plan["status"], "CLEANUP_REQUIRED")
        self.assertFalse(plan["cleanup_authorized"])
        self.assertFalse(plan["mutation_performed"])
        self.assertFalse(plan["dispatch_authorized"])
        self.assertEqual(plan["dry_run_command"], ["git", "clean", "-ndX"])
        self.assertTrue(any("node_modules" in path for path in plan["dry_run_paths"]))
        self.assertTrue(ignored_file.exists(), "cleanup planner must not remove ignored files")

    def test_cleanup_plan_refuses_dirty_or_retargeted_worktrees_before_cleanup_advice(self):
        self.init_git_workdir(ignored=True)
        tracked = self.work_dir / "src" / "components" / "CanonicalDataGrid.tsx"
        tracked.write_text("export const marker = 'dirty';\n")

        plan = build_ignored_residue_cleanup_plan(self.drop_path, **self.route_kwargs())

        self.assertEqual(plan["status"], "BLOCKED_BY_NON_CLEANUP_PREFLIGHT")
        self.assertFalse(plan["cleanup_authorized"])
        self.assertFalse(plan["mutation_performed"])
        self.assertEqual(plan["dry_run_paths"], [])
        self.assertEqual(plan["dry_run_command"], [])
        self.assertIn("GIT_DIRTY", {blocker["code"] for blocker in plan["blockers"]})

    def test_clean_worktree_manifest_retargets_drop_without_authorizing_dispatch_or_mutation(self):
        target_hash = self.init_git_workdir(ignored=True)
        clean_root = self.root / "clean-worktrees"
        clean_work_dir = clean_root / "kuronode-clean"

        plan = build_clean_worktree_drop_manifest(
            self.drop_path,
            clean_work_dir=clean_work_dir,
            clean_worktree_roots=[clean_root],
            **self.route_kwargs(),
        )

        self.assertEqual(plan["status"], "CLEAN_WORKTREE_MANIFEST_READY")
        self.assertEqual(plan["source_work_dir"], str(self.work_dir.resolve()))
        self.assertEqual(plan["clean_work_dir"], str(clean_work_dir.resolve()))
        self.assertEqual(plan["drop_manifest"]["work_dir"], str(clean_work_dir.resolve()))
        self.assertEqual(plan["drop_manifest"]["target_hash"], target_hash)
        self.assertTrue(plan["manifest_approval_required"])
        self.assertFalse(plan["dispatch_authorized"])
        self.assertFalse(plan["source_mutation_authorized"])
        self.assertFalse(plan["worktree_creation_authorized"])

    def test_clean_worktree_manifest_output_writes_exact_compact_canonical_approval_bytes(self):
        target_hash = self.init_git_workdir(ignored=True)
        clean_root = self.root / "clean-worktrees"
        clean_work_dir = clean_root / "kuronode-clean"
        manifest_output_path = self.root / "drop.clean-worktree.json"

        plan = build_clean_worktree_drop_manifest(
            self.drop_path,
            clean_work_dir=clean_work_dir,
            clean_worktree_roots=[clean_root],
            manifest_output_path=manifest_output_path,
            **self.route_kwargs(),
        )

        expected_bytes = json.dumps(plan["drop_manifest"], sort_keys=True, separators=(",", ":")).encode("utf-8")
        pretty_hash = "sha256:" + hashlib.sha256((json.dumps(plan["drop_manifest"], indent=2, sort_keys=True) + "\n").encode("utf-8")).hexdigest()
        self.assertEqual(plan["target_hash"], target_hash)
        self.assertEqual(plan["drop_manifest_path"], str(manifest_output_path.resolve()))
        self.assertEqual(manifest_output_path.read_bytes(), expected_bytes)
        self.assertEqual(plan["drop_manifest_sha256"], self.sha(manifest_output_path))
        self.assertNotEqual(plan["drop_manifest_sha256"], pretty_hash)

    def test_clean_worktree_manifest_rejects_unapproved_or_source_nested_destinations(self):
        self.init_git_workdir(ignored=True)
        clean_root = self.root / "clean-worktrees"
        bad_cases = [
            (self.work_dir / "nested-clean", [self.work_dir], "must not be the source work_dir or inside it"),
            (self.root / "elsewhere" / "kuronode-clean", [clean_root], "clean_work_dir must be under a trusted root"),
        ]

        for clean_work_dir, clean_roots, pattern in bad_cases:
            with self.subTest(clean_work_dir=clean_work_dir):
                with self.assertRaisesRegex(RouteError, pattern):
                    build_clean_worktree_drop_manifest(
                        self.drop_path,
                        clean_work_dir=clean_work_dir,
                        clean_worktree_roots=clean_roots,
                        **self.route_kwargs(),
                    )

    def test_clean_worktree_manifest_can_preflight_ready_in_sterile_clone_while_source_is_blocked(self):
        self.init_git_workdir(ignored=True)
        source_report = preflight_drop_file(self.drop_path, **self.route_kwargs())
        self.assertEqual(source_report["status"], "BLOCKED")

        clean_root = self.root / "clean-worktrees"
        clean_work_dir = clean_root / "kuronode-clean"
        subprocess.run(["git", "clone", "--no-hardlinks", str(self.work_dir), str(clean_work_dir)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        plan = build_clean_worktree_drop_manifest(
            self.drop_path,
            clean_work_dir=clean_work_dir,
            clean_worktree_roots=[clean_root],
            **self.route_kwargs(),
        )
        clean_drop = self.root / "clean-drop.json"
        clean_drop.write_text(json.dumps(plan["drop_manifest"], sort_keys=True))

        report = preflight_drop_file(
            clean_drop,
            allowed_work_dirs=[clean_work_dir],
            trusted_roots=[self.root],
            approved_drop_sha256=self.sha(clean_drop),
        )

        self.assertEqual(report["status"], "READY")
        self.assertEqual(report["work_dir"], str(clean_work_dir.resolve()))
        self.assertEqual(report["blockers"], [])

    def test_default_clean_worktree_retarget_plan_prepares_manifest_candidate_from_dirty_source(self):
        target_hash = self.init_git_workdir(ignored=True)
        manifest_output_path = self.root / "drop.default-clean-worktree.json"

        plan = build_default_clean_worktree_retarget_plan(
            self.drop_path,
            manifest_output_path=manifest_output_path,
            **self.route_kwargs(),
        )

        self.assertEqual(plan["status"], "DEFAULT_CLEAN_WORKTREE_MANIFEST_READY")
        self.assertEqual(plan["source_preflight_report"]["status"], "BLOCKED")
        self.assertTrue(plan["source_preflight_report"]["clean_worktree_retarget_recommended"])
        self.assertEqual(plan["drop_manifest"]["target_hash"], target_hash)
        self.assertEqual(plan["drop_manifest_path"], str(manifest_output_path.resolve()))
        self.assertEqual(plan["drop_manifest_sha256"], self.sha(manifest_output_path))
        self.assertTrue(plan["clean_work_dir"].endswith(f"kuronode-beb-222-{target_hash[:12]}"))
        self.assertTrue(plan["manifest_approval_required"])
        self.assertFalse(plan["fallback_authorized"])
        self.assertFalse(plan["source_cleanup_authorized"])
        self.assertFalse(plan["worktree_creation_authorized"])
        self.assertFalse(plan["dispatch_authorized"])

    def test_clean_worktree_manifest_cli_emits_retargeted_manifest_without_dispatch(self):
        self.init_git_workdir(ignored=True)
        clean_root = self.root / "clean-worktrees"
        clean_work_dir = clean_root / "kuronode-clean"
        manifest_output_path = self.root / "drop.clean-worktree.json"
        adapter = FakeAdapter()

        import io
        import contextlib
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            exit_code = route_main([
                "--drop", str(self.drop_path),
                "--allowed-work-dir", str(self.work_dir),
                "--trusted-root", str(self.root),
                "--approved-drop-sha256", self.sha(self.drop_path),
                "--clean-worktree-manifest",
                "--clean-work-dir", str(clean_work_dir),
                "--clean-worktree-root", str(clean_root),
                "--clean-worktree-manifest-output", str(manifest_output_path),
            ])

        report = json.loads(stdout.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(report["status"], "CLEAN_WORKTREE_MANIFEST_READY")
        self.assertEqual(report["drop_manifest"]["work_dir"], str(clean_work_dir.resolve()))
        self.assertEqual(report["drop_manifest_path"], str(manifest_output_path.resolve()))
        self.assertEqual(report["drop_manifest_sha256"], self.sha(manifest_output_path))
        self.assertFalse(report["dispatch_authorized"])
        self.assertEqual(adapter.calls, [])

    def test_process_drop_file_invokes_blk_pipe_with_real_codex_engine_and_exact_l2_packet(self):
        target_hash = self.init_git_workdir()
        adapter = FakeAdapter()

        result = self.process(adapter)

        self.assertEqual(result["status"], "SUCCESS")
        self.assertEqual(result["commit_hash"], "abc123")
        self.assertIn("route_summary", result)
        self.assertEqual(len(adapter.calls), 1)
        payload = adapter.calls[0]
        self.assertEqual(payload["beb_id"], "BEB_222")
        self.assertEqual(payload["work_dir"], str(self.work_dir.resolve()))
        self.assertEqual(payload["target_branch"], "sprint/beb-222")
        self.assertEqual(payload["target_hash"], target_hash)
        self.assertEqual(payload["engine"], "codex")
        self.assertEqual(payload["l2_packet"], self.l2_path.read_text())
        self.assertEqual(payload["validation_profiles"], ["python-unittest"])
        self.assertNotIn("validation_commands", payload)
        self.assertEqual(payload["trace_artifacts"], TRACE_ARTIFACTS)
        self.assertEqual(payload["engine_args"], build_kuronode_codex_engine_args(beb_id="BEB_222", target_hash=target_hash))

    def test_process_drop_file_returns_authoritative_route_summary_not_codex_self_report(self):
        target_hash = self.init_git_workdir()

        class RouteSummaryAdapter:
            def __init__(self):
                self.calls = []

            def execute_sprint(self, **kwargs):
                self.calls.append(kwargs)
                output_index = kwargs["engine_args"].index("--output-last-message") + 1
                final_message = Path(kwargs["engine_args"][output_index])
                final_message.write_text("Codex self-report: commit failed due read-only .git/index.lock\n")
                return {
                    "status": "SUCCESS",
                    "exit_code": 0,
                    "pre_engine_hash": target_hash,
                    "commit_hash": "b" * 40,
                    "engine_logs": "RAW ENGINE LOGS SHOULD NOT BE EMBEDDED IN SUMMARY",
                    "validation_logs": {"npm test": "RAW VALIDATION LOGS SHOULD NOT BE EMBEDDED IN SUMMARY"},
                    "stderr": "RAW STDERR SHOULD NOT BE EMBEDDED IN SUMMARY",
                    "payload_sha256": "sha256:" + "4" * 64,
                }

        result = self.process(RouteSummaryAdapter())

        summary = result["route_summary"]
        self.assertEqual(summary["status"], "SUCCESS")
        self.assertEqual(summary["commit_hash"], "b" * 40)
        self.assertEqual(summary["target_hash"], target_hash)
        self.assertEqual(summary["drop_manifest_sha256"], self.sha(self.drop_path))
        self.assertFalse(summary["codex_final_message_authoritative"])
        self.assertFalse(summary["raw_logs_embedded"])
        self.assertFalse(summary["reusable_codex_dispatch_authorized"])
        self.assertFalse(summary["beo_publication_authorized"])
        self.assertFalse(summary["rtm_generation_authorized"])
        self.assertRegex(summary["final_message_sha256"], r"^sha256:[0-9a-f]{64}$")
        self.assertRegex(summary["engine_logs_sha256"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(summary["validation_log_count"], 1)
        serialized_summary = json.dumps(summary, sort_keys=True)
        self.assertNotIn("RAW ENGINE LOGS", serialized_summary)
        self.assertNotIn("RAW VALIDATION LOGS", serialized_summary)
        self.assertNotIn("read-only .git/index.lock", serialized_summary)
        summary_artifact = Path(summary["route_summary_artifact_path"])
        self.assertTrue(summary_artifact.is_file())
        self.assertEqual(summary["route_summary_artifact_sha256"], self.sha(summary_artifact))
        artifact_text = summary_artifact.read_text()
        self.assertNotIn("RAW ENGINE LOGS", artifact_text)
        self.assertNotIn("RAW VALIDATION LOGS", artifact_text)
        self.assertNotIn("read-only .git/index.lock", artifact_text)

    def test_archive_k2_route_evidence_materializes_sanitized_index_inside_package(self):
        package_dir = self.root / "artifacts" / "kuronode-v2" / "k2-023"
        summary_path = self.root / "tmp-route-summary.json"
        final_message_path = self.root / "final-message.md"
        final_message_path.write_text("Codex final message: implementation completed; commit failed self-report is advisory.\n")
        route_summary = {
            "status": "SUCCESS",
            "beb_id": "BEB-K2-023",
            "beo_id": "BEO-K2-023",
            "l2_id": "L2-K2-023",
            "target_hash": "a" * 40,
            "commit_hash": "b" * 40,
            "drop_manifest_sha256": "sha256:" + "1" * 64,
            "route_summary_artifact_path": str(summary_path),
            "route_summary_artifact_sha256": "",
            "final_message_artifact_path": str(final_message_path),
            "final_message_sha256": self.sha(final_message_path),
            "raw_logs_embedded": False,
            "beo_publication_authorized": False,
            "rtm_generation_authorized": False,
            "reusable_codex_dispatch_authorized": False,
            "unexpected_safe_field": "must not be copied into the package archive",
        }
        summary_path.write_text(json.dumps(route_summary, sort_keys=True))
        route_summary["route_summary_artifact_sha256"] = self.sha(summary_path)
        summary_path.write_text(json.dumps(route_summary, sort_keys=True))

        archive = archive_k2_route_evidence(
            package_dir=package_dir,
            route_summaries=[route_summary],
        )

        evidence_dir = package_dir / "route-evidence"
        self.assertEqual(archive["status"], "K2_ROUTE_EVIDENCE_ARCHIVE_READY")
        self.assertEqual(archive["evidence_count"], 1)
        self.assertFalse(archive["dispatch_authorized"])
        self.assertFalse(archive["beo_publication_authorized"])
        self.assertFalse(archive["rtm_generation_authorized"])
        self.assertTrue((evidence_dir / "route-summary-001.json").is_file())
        self.assertTrue((evidence_dir / "codex-final-message-001.md").is_file())
        index_path = evidence_dir / "evidence-index.json"
        self.assertEqual(archive["evidence_index_path"], str(index_path.resolve()))
        self.assertEqual(archive["evidence_index_sha256"], self.sha(index_path))
        index = json.loads(index_path.read_text())
        self.assertEqual(index["route_evidence"][0]["beb_id"], "BEB-K2-023")
        self.assertEqual(index["route_evidence"][0]["route_summary_sha256"], self.sha(evidence_dir / "route-summary-001.json"))
        self.assertEqual(index["route_evidence"][0]["codex_final_message_sha256"], self.sha(evidence_dir / "codex-final-message-001.md"))
        archived_summary = json.loads((evidence_dir / "route-summary-001.json").read_text())
        self.assertNotIn("unexpected_safe_field", archived_summary)

        authority_summary = dict(route_summary)
        authority_summary.update({
            "beo_publication_authorized": True,
            "rtm_generation_authorized": True,
            "reusable_codex_dispatch_authorized": True,
            "broad_blk_pipe_dispatch_authorized": True,
            "source_cleanup_authorized": True,
            "worktree_creation_authorized": True,
            "codex_final_message_authoritative": True,
        })
        authority_archive = archive_k2_route_evidence(
            package_dir=package_dir / "authority",
            route_summaries=[authority_summary],
        )
        authority_summary_archived = json.loads(
            (Path(authority_archive["evidence_dir"]) / "route-summary-001.json").read_text()
        )
        for denied_field in (
            "beo_publication_authorized",
            "rtm_generation_authorized",
            "reusable_codex_dispatch_authorized",
            "broad_blk_pipe_dispatch_authorized",
            "source_cleanup_authorized",
            "worktree_creation_authorized",
            "codex_final_message_authoritative",
        ):
            self.assertIs(authority_summary_archived[denied_field], False, denied_field)

        unsafe_summary = dict(route_summary)
        unsafe_summary["raw_logs_embedded"] = True
        unsafe_summary["engine_logs"] = "raw log body must not archive"
        with self.assertRaisesRegex(RouteError, "raw route logs"):
            archive_k2_route_evidence(package_dir=package_dir / "unsafe", route_summaries=[unsafe_summary])

        aliased_raw_summary = dict(route_summary)
        aliased_raw_summary["validation_output"] = "RAW VALIDATION LOG body must not archive under alias"
        with self.assertRaisesRegex(RouteError, "raw route logs"):
            archive_k2_route_evidence(package_dir=package_dir / "unsafe-alias", route_summaries=[aliased_raw_summary])

        missing_final_sha = dict(route_summary)
        missing_final_sha.pop("final_message_sha256")
        with self.assertRaisesRegex(RouteError, "final_message_sha256"):
            archive_k2_route_evidence(package_dir=package_dir / "missing-final-sha", route_summaries=[missing_final_sha])

        raw_final_message = self.root / "raw-final-message.md"
        raw_final_message.write_text("RAW ENGINE LOG: read-only .git/index.lock must not archive\n")
        raw_final_summary = dict(route_summary)
        raw_final_summary["final_message_artifact_path"] = str(raw_final_message)
        raw_final_summary["final_message_sha256"] = self.sha(raw_final_message)
        with self.assertRaisesRegex(RouteError, "raw|authority-laundering"):
            archive_k2_route_evidence(package_dir=package_dir / "unsafe-final-message", route_summaries=[raw_final_summary])

        authority_final_message = self.root / "authority-final-message.md"
        authority_final_message.write_text(
            "BEO publication authorized; RTM generation authorized; production blk-link approved; K2-024 selected\n"
        )
        authority_final_summary = dict(route_summary)
        authority_final_summary["final_message_artifact_path"] = str(authority_final_message)
        authority_final_summary["final_message_sha256"] = self.sha(authority_final_message)
        with self.assertRaisesRegex(RouteError, "authority|authorized|publication|blk-link|K2-024"):
            archive_k2_route_evidence(
                package_dir=package_dir / "unsafe-final-message-authority",
                route_summaries=[authority_final_summary],
            )

        protected_final_message = self.root / "docs" / "active" / "protected.md"
        protected_final_message.parent.mkdir(parents=True)
        protected_final_message.write_text("Safe-looking final message body in a protected path.\n")
        protected_final_summary = dict(route_summary)
        protected_final_summary["final_message_artifact_path"] = str(protected_final_message)
        protected_final_summary["final_message_sha256"] = self.sha(protected_final_message)
        with self.assertRaisesRegex(RouteError, "protected.*final_message_artifact_path|final_message_artifact_path.*protected"):
            archive_k2_route_evidence(
                package_dir=package_dir / "unsafe-final-message-protected-path",
                route_summaries=[protected_final_summary],
            )

        invalid_hash_summary = dict(route_summary)
        invalid_hash_summary["engine_logs_sha256"] = "not-a-sha"
        invalid_hash_summary["validation_logs_sha256"] = "also-not-a-sha"
        with self.assertRaisesRegex(RouteError, "engine_logs_sha256|validation_logs_sha256"):
            archive_k2_route_evidence(package_dir=package_dir / "invalid-hash-fields", route_summaries=[invalid_hash_summary])

        nested_status_summary = dict(route_summary)
        nested_status_summary["status"] = {
            "beo_publication_authorized": True,
            "production_blk_link_authorized": True,
            "next_k2_selection_authorized": "K2-024",
        }
        with self.assertRaisesRegex(RouteError, "status"):
            archive_k2_route_evidence(package_dir=package_dir / "nested-status", route_summaries=[nested_status_summary])

        raw_status_summary = dict(route_summary)
        raw_status_summary["status"] = "engine validation transcript copied without exact marker"
        with self.assertRaisesRegex(RouteError, "status"):
            archive_k2_route_evidence(package_dir=package_dir / "raw-status", route_summaries=[raw_status_summary])

    def test_drop_manifest_cannot_override_engine_or_inject_validation_commands(self):
        adapter = FakeAdapter()
        for forbidden_field, value in {
            "engine": "sh",
            "engine_args": ["-c", "printf bypass"],
            "engine_command": ["sh", "-c", "printf bypass"],
            "validation_commands": ["curl https://example.invalid"],
        }.items():
            with self.subTest(forbidden_field=forbidden_field):
                self.write_drop(**{forbidden_field: value})
                with self.assertRaisesRegex(RouteError, forbidden_field):
                    self.process(adapter)
        self.assertEqual(adapter.calls, [])

    def test_drop_manifest_requires_kuronode_project_and_beb_l2_binding_before_dispatch(self):
        adapter = FakeAdapter()
        bad_cases = [
            {"target_project": "other"},
            {"beb_id": "BEB_OTHER"},
            {"l2_id": "L2_OTHER"},
        ]
        for overrides in bad_cases:
            with self.subTest(overrides=overrides):
                self.write_drop(**overrides)
                with self.assertRaises(RouteError):
                    self.process(adapter)
        self.assertEqual(adapter.calls, [])

    def test_route_requires_trusted_workdir_roots_hashes_and_target_hash(self):
        adapter = FakeAdapter()
        outside = self.root.parent / "not-kuronode"
        outside.mkdir(exist_ok=True)
        cases = [
            ({"work_dir": str(outside)}, r"work_dir.*approved"),
            ({"beb_path": str(outside / "BEB.md"), "beb_sha256": "sha256:" + "1" * 64}, r"beb_path.*trusted root"),
            ({"beb_sha256": "sha256:" + "1" * 64}, r"beb_path sha256"),
            ({"l2_sha256": "sha256:" + "1" * 64}, r"l2_path sha256"),
            ({"target_hash": "main"}, r"target_hash"),
        ]
        for overrides, pattern in cases:
            with self.subTest(overrides=overrides):
                self.write_drop(**overrides)
                with self.assertRaisesRegex(RouteError, pattern):
                    self.process(adapter)
        self.assertEqual(adapter.calls, [])

    def test_route_rejects_protected_beb_or_l2_artifact_paths_before_reading(self):
        target_hash = self.init_git_workdir()
        adapter = FakeAdapter()
        protected_root = self.root / "docs" / "requirements" / "active"
        protected_root.mkdir(parents=True)
        protected_beb = protected_root / "REQ-001.md"
        protected_beb.write_text(self.beb_path.read_text())
        protected_l2 = protected_root / "REQ-001-L2.md"
        protected_l2.write_text(self.l2_path.read_text())

        cases = [
            ({"beb_path": str(protected_beb), "beb_sha256": self.sha(protected_beb)}, "beb_path"),
            ({"l2_path": str(protected_l2), "l2_sha256": self.sha(protected_l2)}, "l2_path"),
        ]
        for overrides, field_name in cases:
            with self.subTest(field_name=field_name):
                self.write_drop(target_hash=target_hash, **overrides)
                with self.assertRaisesRegex(RouteError, f"{field_name}.*protected BLK-req"):
                    self.process(adapter)
        self.assertEqual(adapter.calls, [])

    def test_inbox_dispatch_requires_processed_and_failed_dirs_under_trusted_roots(self):
        self.init_git_workdir()
        inbox = self.root / "inbox"
        inbox.mkdir()
        outside = self.root.parent / f"outside-route-state-{self.root.name}"
        drop = inbox / "BEB_222.drop.json"
        drop.write_text(self.drop_path.read_text())
        adapter = FakeAdapter()
        inbox_kwargs = self.route_kwargs()
        inbox_kwargs["approved_drop_sha256s"] = [inbox_kwargs.pop("approved_drop_sha256")]

        with self.assertRaisesRegex(RouteError, "processed_dir.*trusted root"):
            dispatch_inbox_once(inbox, outside / "processed", self.root / "failed", adapter=adapter, **inbox_kwargs)
        self.assertTrue(drop.exists())
        self.assertFalse((outside / "processed" / drop.name).exists())
        self.assertEqual(adapter.calls, [])

        with self.assertRaisesRegex(RouteError, "failed_dir.*trusted root"):
            dispatch_inbox_once(inbox, self.root / "processed", outside / "failed", adapter=adapter, **inbox_kwargs)
        self.assertTrue(drop.exists())
        self.assertFalse((outside / "failed" / drop.name).exists())
        self.assertEqual(adapter.calls, [])

    def test_route_requires_approved_manifest_hash_from_trusted_config(self):
        adapter = FakeAdapter()
        approved = self.sha(self.drop_path)
        self.write_drop(target_branch="sprint/beb-222-retargeted")

        with self.assertRaisesRegex(RouteError, "drop_path sha256"):
            process_drop_file(
                self.drop_path,
                adapter=adapter,
                allowed_work_dirs=[self.work_dir],
                trusted_roots=[self.root],
                approved_drop_sha256=approved,
            )
        self.assertEqual(adapter.calls, [])

    def test_route_rejects_loose_validation_profiles_and_broad_allowlists(self):
        adapter = FakeAdapter()
        cases = [
            ({"validation_profiles": ["curl https://example.invalid"]}, "validation_profiles"),
            ({"validation_profiles": ["unknown-profile"]}, "validation_profiles"),
            ({"allowed_modified_files": ["."]}, "allowed_modified_files"),
            ({"allowed_modified_files": ["src/**/*.ts"]}, "allowed_modified_files"),
            ({"allowed_modified_files": [":(top)src/index.ts"]}, "allowed_modified_files"),
            ({"allowed_modified_files": ["docs/requirements/active/REQ-001.md"]}, "allowed_modified_files"),
        ]
        for overrides, pattern in cases:
            with self.subTest(overrides=overrides):
                self.write_drop(**overrides)
                with self.assertRaisesRegex(RouteError, pattern):
                    self.process(adapter)
        self.assertEqual(adapter.calls, [])

    def test_route_accepts_kuronode_worktree_static_validation_profile(self):
        target_hash = self.init_git_workdir()
        self.write_drop(target_hash=target_hash, validation_profiles=["kuronode-worktree-static"])
        adapter = FakeAdapter()

        result = self.process(adapter)

        self.assertEqual(result["status"], "SUCCESS")
        self.assertEqual(adapter.calls[0]["validation_profiles"], ["kuronode-worktree-static"])

    def test_process_drop_file_uses_adapter_payload_file_path_with_fake_blk_pipe(self):
        target_hash = self.init_git_workdir()
        capture_dir = self.root / "capture"
        fake_blk_pipe = self.root / "fake-blk-pipe"
        fake_blk_pipe.write_text(
            textwrap.dedent(
                """
                #!/usr/bin/env python3
                import json
                import os
                import sys
                from pathlib import Path

                payload_path = Path(sys.argv[2])
                payload = json.loads(payload_path.read_text())
                capture_dir = Path(os.environ["BLK_ROUTE_CAPTURE_DIR"])
                capture_dir.mkdir()
                (capture_dir / "argv.json").write_text(json.dumps(sys.argv[1:]))
                (capture_dir / "payload.json").write_text(json.dumps(payload))
                print(json.dumps({"status": "SUCCESS", "commit_hash": "route-commit"}))
                """
            ).lstrip()
        )
        fake_blk_pipe.chmod(fake_blk_pipe.stat().st_mode | stat.S_IXUSR)
        adapter = BlkPipeAdapter(binary_path=str(fake_blk_pipe))

        import os
        old_capture = os.environ.get("BLK_ROUTE_CAPTURE_DIR")
        os.environ["BLK_ROUTE_CAPTURE_DIR"] = str(capture_dir)
        try:
            result = self.process(adapter)
        finally:
            if old_capture is None:
                os.environ.pop("BLK_ROUTE_CAPTURE_DIR", None)
            else:
                os.environ["BLK_ROUTE_CAPTURE_DIR"] = old_capture

        payload = json.loads((capture_dir / "payload.json").read_text())
        self.assertEqual(result.status, "SUCCESS")
        self.assertEqual(result.commit_hash, "route-commit")
        self.assertEqual(json.loads((capture_dir / "argv.json").read_text())[0], "--payload")
        self.assertEqual(payload["engine"], "codex")
        self.assertEqual(payload["engine_args"], build_kuronode_codex_engine_args(target_hash=target_hash, beb_id="BEB_222"))
        self.assertEqual(payload["l2_packet"], self.l2_path.read_text())
        self.assertEqual(payload["trace_artifacts"], TRACE_ARTIFACTS)
        self.assertEqual(payload["target_hash"], target_hash)

        output_index = payload["engine_args"].index("--output-last-message") + 1
        final_message_artifact = Path(payload["engine_args"][output_index])
        self.assertTrue(final_message_artifact.is_absolute())
        self.assertFalse(final_message_artifact.is_relative_to(self.work_dir.resolve()))
        self.assertEqual(final_message_artifact.parent.name, target_hash[:12])
        self.assertEqual(final_message_artifact.parent.parent.name, "BEB_222")
        self.assertTrue(final_message_artifact.parent.is_dir())

    def test_route_main_progress_stderr_emits_operator_status_lines(self):
        self.init_git_workdir()
        fake_bin_dir = self.root / "bin"
        fake_bin_dir.mkdir()
        fake_blk_pipe = fake_bin_dir / "blk-pipe"
        fake_blk_pipe.write_text(
            textwrap.dedent(
                """
                #!/usr/bin/env python3
                import json

                print(json.dumps({
                    "status": "SUCCESS",
                    "commit_hash": "route-commit",
                    "validation_logs": {"go test ./...": "PASS"},
                }))
                """
            ).lstrip()
        )
        fake_blk_pipe.chmod(fake_blk_pipe.stat().st_mode | stat.S_IXUSR)

        old_path = os.environ.get("PATH", "")
        os.environ["PATH"] = f"{fake_bin_dir}{os.pathsep}{old_path}"
        stdout = io.StringIO()
        stderr = io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exit_code = route_main([
                    "--drop", str(self.drop_path),
                    "--allowed-work-dir", str(self.work_dir),
                    "--trusted-root", str(self.root),
                    "--approved-drop-sha256", self.sha(self.drop_path),
                    "--progress-stderr",
                ])
        finally:
            os.environ["PATH"] = old_path

        self.assertEqual(exit_code, 0)
        self.assertEqual(json.loads(stdout.getvalue())["status"], "SUCCESS")
        status_lines = [
            line for line in stderr.getvalue().splitlines()
            if line.startswith("[BLK status]")
        ]
        self.assertTrue(any("BEB_222 started" in line for line in status_lines), status_lines)
        self.assertTrue(any("Codex started" in line for line in status_lines), status_lines)
        self.assertTrue(any("Codex completed: SUCCESS" in line for line in status_lines), status_lines)
        self.assertTrue(any("testing completed: SUCCESS" in line for line in status_lines), status_lines)
        self.assertFalse(any("blk_pipe_running" in line for line in status_lines), status_lines)

    def test_process_drop_file_rejects_symlinked_external_codex_artifact_directory(self):
        target_hash = self.init_git_workdir()
        artifact_beb_dir = Path("/tmp/blk-system-beb-l2-codex") / "BEB_222"
        shutil.rmtree(artifact_beb_dir, ignore_errors=True)
        self.addCleanup(lambda: shutil.rmtree(artifact_beb_dir, ignore_errors=True))
        artifact_beb_dir.mkdir(parents=True)
        os.symlink(self.work_dir, artifact_beb_dir / target_hash[:12])
        adapter = FakeAdapter()

        with self.assertRaisesRegex(RouteError, "Codex final-message artifact path"):
            self.process(adapter)

        self.assertEqual(adapter.calls, [])

    def test_inbox_dispatch_moves_successful_drop_after_invocation(self):
        self.init_git_workdir()
        inbox = self.root / "inbox"
        processed = self.root / "processed"
        failed = self.root / "failed"
        inbox.mkdir()
        drop = inbox / "BEB_222.drop.json"
        drop.write_text(self.drop_path.read_text())
        adapter = FakeAdapter()

        inbox_kwargs = self.route_kwargs()
        inbox_kwargs["approved_drop_sha256s"] = [inbox_kwargs.pop("approved_drop_sha256")]
        report = dispatch_inbox_once(inbox, processed, failed, adapter=adapter, **inbox_kwargs)

        self.assertEqual(report["status"], "SUCCESS")
        self.assertFalse(drop.exists())
        self.assertTrue((processed / drop.name).exists())
        self.assertFalse(failed.exists())
        self.assertEqual(len(adapter.calls), 1)


    def test_preflight_reports_non_authorizing_companion_test_suggestions(self):
        self.init_git_workdir()
        companion = self.work_dir / "src" / "components" / "CanonicalDataGrid.test.tsx"
        companion.write_text("test('existing companion', () => {});\n")
        subprocess.run(["git", "add", "src/components/CanonicalDataGrid.test.tsx"], cwd=self.work_dir, check=True)
        subprocess.run(["git", "commit", "-m", "add companion test"], cwd=self.work_dir, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.work_dir, check=True, text=True, stdout=subprocess.PIPE).stdout.strip()
        self.write_drop(target_hash=head)

        report = preflight_drop_file(self.drop_path, **self.route_kwargs())

        self.assertEqual(report["status"], "READY")
        self.assertEqual(report["blockers"], [])
        suggestions = report["allowlist_suggestions"]
        self.assertEqual(suggestions[0]["kind"], "existing_companion_test_not_authorized")
        self.assertEqual(suggestions[0]["source_file"], "src/components/CanonicalDataGrid.tsx")
        self.assertEqual(suggestions[0]["suggested_file"], "src/components/CanonicalDataGrid.test.tsx")
        self.assertFalse(suggestions[0]["auto_authorized"])

    def test_route_commit_message_is_beb_bound_and_newline_safe(self):
        self.assertEqual(build_route_commit_message("BEB_344"), "blk-pipe: BEB_344")
        self.assertEqual(build_route_commit_message("BEB-TST-001"), "blk-pipe: BEB-TST-001")
        with self.assertRaisesRegex(RouteError, "beb_id has invalid format"):
            build_route_commit_message("BEB-TST-000")
        with self.assertRaisesRegex(RouteError, "commit message"):
            build_route_commit_message("BEB_" + "X" * 200)

    def test_process_drop_file_passes_beb_bound_commit_message_to_adapter(self):
        self.init_git_workdir()
        adapter = FakeAdapter()

        self.process(adapter)

        self.assertEqual(adapter.calls[0]["commit_message"], "blk-pipe: BEB_222")

    def test_kuronode_focused_node_profile_is_allowed_by_drop_route(self):
        target_hash = self.init_git_workdir()
        self.write_drop(target_hash=target_hash, validation_profiles=["kuronode-worktree-focused-node"])

        report = preflight_drop_file(self.drop_path, **self.route_kwargs())

        self.assertEqual(report["status"], "READY")
        self.assertEqual(report["validation_profiles"], ["kuronode-worktree-focused-node"])

    def test_hostile_review_record_blocks_closeout_until_pass_and_requires_remediation_hashes(self):
        record = build_hostile_review_record(
            beb_id="BEB_349",
            parent_hash="a" * 40,
            feature_hash="b" * 40,
            verdict="BLOCKED",
            blockers=["raw provider error leaked to logs"],
            allowed_files=["packages/core/src/routes/agentAChat.ts"],
            retry_count=1,
        )

        self.assertEqual(record["state"], "HOSTILE_REVIEW_BLOCKED")
        self.assertEqual(record["next_required_state"], "REMEDIATION_PACKET_REQUIRED")
        self.assertFalse(record["closeout_ready"])
        self.assertFalse(record["remediation_auto_authorized"])
        self.assertFalse(record["beo_publication_authorized"])

        with self.assertRaisesRegex(RouteError, "remediation parent/feature hash"):
            build_hostile_review_record(
                beb_id="BEB_349",
                parent_hash="a" * 40,
                feature_hash="b" * 40,
                verdict="PASS",
                blockers=[],
                allowed_files=["packages/core/src/routes/agentAChat.ts"],
                retry_count=0,
            )

        pass_record = build_hostile_review_record(
            beb_id="BEB_349",
            parent_hash="a" * 40,
            feature_hash="b" * 40,
            verdict="PASS",
            blockers=[],
            allowed_files=["packages/core/src/routes/agentAChat.ts"],
            retry_count=2,
            remediation_parent_hash="b" * 40,
            remediation_feature_hash="c" * 40,
        )

        self.assertEqual(pass_record["state"], "HOSTILE_REVIEW_PASS")
        self.assertTrue(pass_record["closeout_ready"])
        self.assertEqual(pass_record["remediation_parent_hash"], "b" * 40)
        self.assertEqual(pass_record["remediation_feature_hash"], "c" * 40)

    def test_codex_args_are_not_caller_controlled(self):
        args = build_kuronode_codex_engine_args()

        self.assertEqual(args[0], "exec")
        self.assertIn("-", args)
        self.assertIn("--model", args)
        self.assertIn("gpt-5.5", args)
        self.assertIn('model_reasoning_effort="xhigh"', args)
        self.assertNotIn("model_reasoning_effort=high", args)
        self.assertIn("--sandbox", args)
        self.assertEqual(args[args.index("--sandbox") + 1], "workspace-write")
        self.assertNotIn("--ask-for-approval", args)
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", args)
        self.assertNotIn("danger-full-access", args)
        with self.assertRaisesRegex(RouteError, "model"):
            build_kuronode_codex_engine_args(model="gpt-5.4", reasoning_effort="xhigh")
        with self.assertRaisesRegex(RouteError, "reasoning_effort"):
            build_kuronode_codex_engine_args(model="gpt-5.5", reasoning_effort="high")
        with self.assertRaisesRegex(RouteError, "reasoning_effort"):
            build_kuronode_codex_engine_args(model="gpt-5.5", reasoning_effort="low")

    def test_repo_local_hygiene_blocks_pycache_and_pyc_without_mutation(self):
        repo = self.root / "repo"
        pycache = repo / "python" / "__pycache__"
        pycache.mkdir(parents=True)
        pyc = pycache / "module.cpython-312.pyc"
        pyc.write_bytes(b"bytecode")

        blocked = scan_repo_local_hygiene(repo)

        self.assertEqual(blocked["status"], "REPO_LOCAL_HYGIENE_BLOCKED")
        self.assertFalse(blocked["mutation_performed"])
        self.assertFalse(blocked["staging_authorized"])
        self.assertIn("REPO_LOCAL_PYCACHE", {item["code"] for item in blocked["blockers"]})
        self.assertIn("python/__pycache__", blocked["forbidden_paths"])
        self.assertIn("python/__pycache__/module.cpython-312.pyc", blocked["forbidden_paths"])

        shutil.rmtree(pycache)
        passed = scan_repo_local_hygiene(repo)
        self.assertEqual(passed["status"], "REPO_LOCAL_HYGIENE_PASS")
        self.assertEqual(passed["blockers"], [])


if __name__ == "__main__":
    unittest.main()
