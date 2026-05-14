import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

import lint_artifacts as lint_artifacts_module
from lint_artifacts import (
    BLK_REQ_DENIED_AUTHORITIES,
    build_legislative_gateway_contract,
    canonicalize_artifact_text,
    capture_baseline_approval,
    compute_version_hash,
    lint_artifact,
    promote_staged_revision_to_active,
    promote_staging_draft_to_baseline,
    preview_staging_version_hash,
    retrieve_active_artifact_by_exact_id,
    validate_legislative_gateway_contract,
    write_staged_revision_draft,
    write_staging_draft,
)

ROOT = Path(__file__).resolve().parents[1]
BLK116 = ROOT / "docs" / "BLK-116_blk-req-legislative-gateway-contract.md"


class BlkReqLegislativeGatewayContractTest(unittest.TestCase):
    def test_contract_pins_allowed_gateway_slices_without_adjacent_authority(self):
        contract = build_legislative_gateway_contract()

        self.assertEqual(contract["contract_marker"], "BLK_SYSTEM_116_BLK_REQ_LEGISLATIVE_GATEWAY_CONTRACT")
        self.assertEqual(contract["contract_status"], "CONTRACT_READY_NOT_EXECUTION_AUTHORITY")
        self.assertEqual(
            contract["allowed_local_backend_operations"],
            [
                "BLK_SYSTEM_117_STAGING_LINTER",
                "BLK_SYSTEM_118_STAGING_DRAFT_WRITER",
                "BLK_SYSTEM_119_CANONICAL_VERSION_HASH_ENGINE",
            ],
        )
        self.assertEqual(set(contract["denied_authorities"]), BLK_REQ_DENIED_AUTHORITIES)
        self.assertEqual(len(contract["denied_authorities"]), len(BLK_REQ_DENIED_AUTHORITIES))

        for flag, value in contract["side_effect_flags"].items():
            self.assertIs(value, False, flag)

        self.assertEqual(validate_legislative_gateway_contract(contract), [])

    def test_contract_validation_rejects_missing_extra_or_true_denied_authority_surfaces(self):
        base = build_legislative_gateway_contract()

        missing = deepcopy(base)
        missing["denied_authorities"] = missing["denied_authorities"][:-1]
        self.assertIn("denied_authorities must match exact BLK-116 set", validate_legislative_gateway_contract(missing))

        extra = deepcopy(base)
        extra["denied_authorities"].append("APPROVED_FOR_LIVE_EXECUTION")
        self.assertIn("denied_authorities must match exact BLK-116 set", validate_legislative_gateway_contract(extra))

        true_flag = deepcopy(base)
        true_flag["side_effect_flags"]["rtm_generation_performed"] = True
        self.assertIn("side_effect_flags.rtm_generation_performed must remain false", validate_legislative_gateway_contract(true_flag))

    def test_contract_validation_rejects_nested_authority_laundering_wording(self):
        contract = build_legislative_gateway_contract()
        contract["notes"].append({"operator_summary": "runtime execution approved; BEO publication granted"})

        errors = validate_legislative_gateway_contract(contract)

        self.assertTrue(any("runtimeexecutionapproved" in error for error in errors), errors)
        self.assertTrue(any("beopublicationgranted" in error for error in errors), errors)

    def test_blk116_boundary_doc_pins_contract_markers(self):
        self.assertTrue(BLK116.exists(), "BLK-116 boundary record missing")
        text = BLK116.read_text()
        required = [
            "BLK_SYSTEM_116_BLK_REQ_LEGISLATIVE_GATEWAY_CONTRACT",
            "CONTRACT_READY_NOT_EXECUTION_AUTHORITY",
            "ALLOWED_LOCAL_BACKEND_OPERATIONS_117_118_119_ONLY",
            "DENIED_ADJACENT_AUTHORITIES_EXACT_SET_PINNED",
            "NO_HITL_APPROVAL_CAPTURE_OR_ACTIVE_PROMOTION_BY_116",
            "BLK-test is a BLK-System functional module, not BLK-System's test suite",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-116 missing markers: {missing}")


class BlkReqVersionAwareStagingLinterTest(unittest.TestCase):
    def _write_artifact(self, root: Path, rel: str, *, metadata: dict, body: str) -> Path:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = ["---"]
        for key, value in metadata.items():
            if key == "linked_nodes":
                lines.append("linked_nodes:")
                for node in value:
                    lines.append(f'  - "{node}"')
            else:
                lines.append(f'{key}: "{value}"')
        lines.append("---")
        lines.append(body)
        path.write_text("\n".join(lines), encoding="utf-8")
        return path

    def _base_metadata(self, **overrides):
        metadata = {
            "id": "TBD",
            "schema_version": "1.0",
            "parent_hash": "",
            "version_hash": "PENDING",
            "status": "DRAFT",
            "rationale": "Needed to keep BLK-req artifacts mechanically bounded.",
            "linked_nodes": ["[[UC-001]]"],
        }
        metadata.update(overrides)
        return metadata

    def test_requirement_staging_linter_accepts_valid_atomic_draft_with_structured_diagnostics(self):
        with self.subTest("valid requirement"):
            import tempfile

            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                path = self._write_artifact(
                    root,
                    "docs/requirements/staging/req_gateway.md",
                    metadata=self._base_metadata(),
                    body="The gateway shall reject malformed draft metadata.",
                )

                result = lint_artifact(path, workspace=root)

            self.assertTrue(result["ok"], result)
            self.assertEqual(result["artifact_type"], "REQ")
            self.assertEqual(result["schema_version"], "1.0")
            self.assertEqual(result["diagnostics"], [])
            self.assertTrue(result["staging_body_read"])
            self.assertFalse(result["active_vault_read"])
            self.assertFalse(result["protected_active_body_read"])

    def test_requirement_linter_rejects_compound_and_subjective_non_bullet_text(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = self._write_artifact(
                root,
                "docs/requirements/staging/compound.md",
                metadata=self._base_metadata(),
                body="The gateway shall be fast and user-friendly while accepting drafts.\n- Operators may compare before and after notes.",
            )

            result = lint_artifact(path, workspace=root)

        codes = {diagnostic["code"] for diagnostic in result["diagnostics"]}
        self.assertFalse(result["ok"])
        self.assertIn("REQ_ATOMICITY_CONJUNCTION", codes)
        self.assertIn("REQ_SUBJECTIVE_VOCABULARY", codes)

    def test_use_case_linter_allows_narrative_conjunctions_but_enforces_word_bound(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            valid_path = self._write_artifact(
                root,
                "docs/use_cases/staging/uc_gateway.md",
                metadata=self._base_metadata(linked_nodes=["[[REQ-001]]"]),
                body="The operator drafts intent and reviews feedback while Hermes keeps the artifact in staging.",
            )
            long_path = self._write_artifact(
                root,
                "docs/use_cases/staging/uc_long.md",
                metadata=self._base_metadata(linked_nodes=["[[REQ-001]]"]),
                body=" ".join(f"word{i}" for i in range(501)),
            )

            valid = lint_artifact(valid_path, workspace=root)
            long = lint_artifact(long_path, workspace=root)

        self.assertTrue(valid["ok"], valid)
        self.assertFalse(long["ok"])
        self.assertIn("UC_BODY_WORD_LIMIT", {diagnostic["code"] for diagnostic in long["diagnostics"]})

    def test_linter_rejects_schema_metadata_and_link_syntax_errors(self):
        import tempfile

        cases = [
            {"schema_version": "2.0"},
            {"status": "BASELINED"},
            {"version_hash": "sha256:" + "a" * 64},
            {"rationale": ""},
            {"linked_nodes": ["REQ-001"]},
            {"id": "UC-001"},
            {"parent_hash": "sha256:" + "b" * 64},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for index, overrides in enumerate(cases):
                with self.subTest(overrides=overrides):
                    path = self._write_artifact(
                        root,
                        f"docs/requirements/staging/bad_{index}.md",
                        metadata=self._base_metadata(**overrides),
                        body="The gateway shall reject malformed metadata.",
                    )
                    result = lint_artifact(path, workspace=root)
                    self.assertFalse(result["ok"], result)
                    self.assertTrue(result["diagnostics"], result)

    def test_linter_rejects_active_or_non_staging_paths_before_body_read(self):
        import tempfile
        from unittest.mock import patch

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            active = root / "docs" / "requirements" / "active" / "REQ-001.md"
            active.parent.mkdir(parents=True)
            active.write_text("SHOULD NOT BE READ", encoding="utf-8")

            def forbidden_read(self_path, *args, **kwargs):
                raise AssertionError(f"unexpected file read: {self_path}")

            with patch.object(Path, "read_text", forbidden_read):
                result = lint_artifact(active, workspace=root)

        self.assertFalse(result["ok"])
        self.assertFalse(result["staging_body_read"])
        self.assertFalse(result["active_vault_read"])
        self.assertIn("PATH_NOT_STAGING", {diagnostic["code"] for diagnostic in result["diagnostics"]})

    def test_blk117_boundary_doc_pins_linter_markers(self):
        blk117 = ROOT / "docs" / "BLK-117_version-aware-staging-linter.md"
        self.assertTrue(blk117.exists(), "BLK-117 boundary record missing")
        text = blk117.read_text()
        required = [
            "BLK_SYSTEM_117_VERSION_AWARE_STAGING_LINTER",
            "LINTER_ROUTES_REQUIREMENTS_AND_USE_CASES_BY_STAGING_PATH",
            "DRAFT_METADATA_SCHEMA_VERSION_1_0_ENFORCED",
            "ACTIVE_VAULT_BODY_READS_REJECTED_BY_LINTER",
            "STRUCTURED_JSON_DIAGNOSTICS_RETURNED",
            "NO_ACTIVE_PROMOTION_OR_HASH_ASSIGNMENT_BY_117",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-117 missing markers: {missing}")


class BlkReqStagingDraftWriterTest(unittest.TestCase):
    def test_writer_creates_requirement_draft_under_requirements_staging_with_strict_metadata(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = write_staging_draft(
                workspace=root,
                artifact_type="REQ",
                title="Gateway Metadata Validation",
                body="The gateway shall reject malformed draft metadata.",
                rationale="Needed for deterministic BLK-req linting.",
                linked_nodes=["[[UC-001]]"],
            )
            path = root / result["relative_path"]
            text = path.read_text(encoding="utf-8")
            lint = lint_artifact(path, workspace=root)

        self.assertEqual(result["status"], "STAGING_DRAFT_WRITTEN")
        self.assertTrue(result["written"])
        self.assertEqual(result["relative_path"], "docs/requirements/staging/gateway-metadata-validation.md")
        self.assertIn('id: "TBD"', text)
        self.assertIn('schema_version: "1.0"', text)
        self.assertIn('parent_hash: ""', text)
        self.assertIn('version_hash: "PENDING"', text)
        self.assertIn('status: "DRAFT"', text)
        self.assertTrue(lint["ok"], lint)

    def test_writer_creates_use_case_draft_under_use_cases_staging_and_reports_attempt_cap(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = write_staging_draft(
                workspace=root,
                artifact_type="UC",
                title="Gateway Narrative Review",
                body="The operator drafts intent and reviews diagnostics while the gateway keeps the draft isolated.",
                rationale="Needed to validate use-case narrative bounds.",
                linked_nodes=["[[REQ-001]]"],
            )
            path = root / result["relative_path"]
            lint = lint_artifact(path, workspace=root)

        self.assertEqual(result["relative_path"], "docs/use_cases/staging/gateway-narrative-review.md")
        self.assertEqual(result["max_self_remediation_attempts"], 3)
        self.assertTrue(lint["ok"], lint)

    def test_writer_rejects_invalid_draft_without_creating_file(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = write_staging_draft(
                workspace=root,
                artifact_type="REQ",
                title="Invalid Compound Requirement",
                body="The gateway shall be fast and user-friendly while accepting drafts.",
                rationale="Needed to prove invalid drafts fail closed.",
                linked_nodes=["[[UC-001]]"],
            )
            path = root / result["relative_path"]

        self.assertEqual(result["status"], "STAGING_DRAFT_REJECTED")
        self.assertFalse(result["written"])
        self.assertFalse(path.exists())
        self.assertIn("REQ_ATOMICITY_CONJUNCTION", {diagnostic["code"] for diagnostic in result["diagnostics"]})

    def test_writer_rejects_path_traversal_and_existing_draft_overwrite(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(ValueError):
                write_staging_draft(
                    workspace=root,
                    artifact_type="REQ",
                    title="Escape",
                    body="The gateway shall reject traversal.",
                    rationale="Needed to prove path containment.",
                    linked_nodes=[],
                    filename_slug="../active/REQ-001",
                )

            first = write_staging_draft(
                workspace=root,
                artifact_type="REQ",
                title="Existing Draft",
                body="The gateway shall reject duplicate draft filenames.",
                rationale="Needed to prove overwrite protection.",
                linked_nodes=[],
            )
            second = write_staging_draft(
                workspace=root,
                artifact_type="REQ",
                title="Existing Draft",
                body="The gateway shall reject duplicate draft filenames.",
                rationale="Needed to prove overwrite protection.",
                linked_nodes=[],
            )

        self.assertEqual(first["status"], "STAGING_DRAFT_WRITTEN")
        self.assertEqual(second["status"], "STAGING_DRAFT_REJECTED")
        self.assertIn("STAGING_DRAFT_EXISTS", {diagnostic["code"] for diagnostic in second["diagnostics"]})

    def test_writer_rejects_symlinked_staging_filename_before_active_target_write(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            staging = root / "docs" / "requirements" / "staging"
            active_target = root / "docs" / "requirements" / "active" / "REQ-001.md"
            staging.mkdir(parents=True)
            active_target.parent.mkdir(parents=True)
            (staging / "symlinked.md").symlink_to("../active/REQ-001.md")

            result = write_staging_draft(
                workspace=root,
                artifact_type="REQ",
                title="Symlinked",
                body="The gateway shall reject symlinked staging paths.",
                rationale="Needed to prove resolved staging containment.",
                linked_nodes=[],
            )

        self.assertEqual(result["status"], "STAGING_DRAFT_REJECTED")
        self.assertFalse(result["written"])
        self.assertFalse(active_target.exists())
        self.assertIn("STAGING_PATH_SYMLINK", {diagnostic["code"] for diagnostic in result["diagnostics"]})

    def test_writer_does_not_write_active_vault_paths(self):
        import tempfile
        from unittest.mock import patch

        written_paths = []
        original_write_text = Path.write_text

        def guarded_write(self_path, *args, **kwargs):
            written_paths.append(str(self_path))
            if "docs/requirements/active" in str(self_path) or "docs/use_cases/active" in str(self_path):
                raise AssertionError(f"active vault write attempted: {self_path}")
            return original_write_text(self_path, *args, **kwargs)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch.object(Path, "write_text", guarded_write):
                result = write_staging_draft(
                    workspace=root,
                    artifact_type="REQ",
                    title="No Active Write",
                    body="The gateway shall keep drafts in staging.",
                    rationale="Needed to prove active vault write absence.",
                    linked_nodes=[],
                )

        self.assertEqual(result["status"], "STAGING_DRAFT_WRITTEN")
        self.assertTrue(written_paths)
        self.assertTrue(all("/staging/" in path for path in written_paths))

    def test_blk118_boundary_doc_pins_writer_markers(self):
        blk118 = ROOT / "docs" / "BLK-118_staging-intake-draft-writer.md"
        self.assertTrue(blk118.exists(), "BLK-118 boundary record missing")
        text = blk118.read_text()
        required = [
            "BLK_SYSTEM_118_STAGING_DRAFT_WRITER",
            "DRAFT_WRITER_OUTPUTS_ONLY_TO_STAGING_DIRECTORIES",
            "NEW_DRAFT_METADATA_ID_TBD_VERSION_HASH_PENDING",
            "INVALID_DRAFTS_RETURN_DIAGNOSTICS_WITHOUT_WRITING",
            "MAX_SELF_REMEDIATION_ATTEMPTS_THREE_DOCUMENTED",
            "NO_HITL_APPROVAL_CAPTURE_OR_ACTIVE_PROMOTION_BY_118",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-118 missing markers: {missing}")


class BlkReqCanonicalVersionHashEngineTest(unittest.TestCase):
    def _artifact_text(self, *, body="The gateway shall reject malformed draft metadata.", rationale="Needed for deterministic hashing.", linked_nodes=None, status="DRAFT", version_hash="PENDING", parent_hash=""):
        linked_nodes = ["[[UC-001]]"] if linked_nodes is None else linked_nodes
        lines = [
            "---",
            'id: "TBD"',
            'schema_version: "1.0"',
            f'parent_hash: "{parent_hash}"',
            f'version_hash: "{version_hash}"',
            f'status: "{status}"',
            f'rationale: "{rationale}"',
            "linked_nodes:",
        ]
        lines.extend(f'  - "{node}"' for node in linked_nodes)
        lines.append("---")
        lines.append(body)
        return "\n".join(lines) + "\n"

    def test_canonical_serialization_uses_declared_fields_and_exact_body(self):
        import json
        import re

        text = self._artifact_text(body="The gateway shall preserve this exact body.")
        canonical = canonicalize_artifact_text(text)
        payload = json.loads(canonical)
        version_hash = compute_version_hash(text)

        self.assertEqual(
            sorted(payload),
            ["body", "id", "linked_nodes", "rationale", "schema_version", "status"],
        )
        self.assertEqual(payload["body"], "The gateway shall preserve this exact body.\n")
        self.assertNotIn("parent_hash", payload)
        self.assertNotIn("version_hash", payload)
        self.assertRegex(version_hash, r"^sha256:[0-9a-f]{64}$")
        self.assertFalse(re.search(r"[A-F]", version_hash))

    def test_hash_changes_for_semantic_fields_but_ignores_parent_and_existing_version_hash(self):
        base = self._artifact_text()
        base_hash = compute_version_hash(base)
        same_with_existing_hash = self._artifact_text(version_hash="sha256:" + "a" * 64)
        same_with_parent_hash = self._artifact_text(parent_hash="sha256:" + "b" * 64)

        self.assertEqual(base_hash, compute_version_hash(same_with_existing_hash))
        self.assertEqual(base_hash, compute_version_hash(same_with_parent_hash))
        self.assertNotEqual(base_hash, compute_version_hash(self._artifact_text(body="The gateway shall reject altered metadata.")))
        self.assertNotEqual(base_hash, compute_version_hash(self._artifact_text(rationale="Changed rationale.")))
        self.assertNotEqual(base_hash, compute_version_hash(self._artifact_text(linked_nodes=["[[REQ-002]]"])))
        self.assertNotEqual(base_hash, compute_version_hash(self._artifact_text(status="BASELINED")))

    def test_hash_preview_reads_only_staging_paths_and_returns_false_side_effects(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            draft = write_staging_draft(
                workspace=root,
                artifact_type="REQ",
                title="Hash Preview",
                body="The gateway shall preview draft hashes.",
                rationale="Needed for trace preparation.",
                linked_nodes=[],
            )
            path = root / draft["relative_path"]
            preview = preview_staging_version_hash(path, workspace=root)
            text = path.read_text(encoding="utf-8")

        self.assertTrue(preview["ok"], preview)
        self.assertEqual(preview["version_hash"], compute_version_hash(text))
        self.assertTrue(preview["staging_body_read"])
        self.assertFalse(preview["active_vault_read"])
        self.assertFalse(preview["active_vault_write"])
        self.assertFalse(preview["baseline_promotion"])

    def test_hash_preview_rejects_active_paths_before_body_read(self):
        import tempfile
        from unittest.mock import patch

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            active = root / "docs" / "requirements" / "active" / "REQ-001.md"
            active.parent.mkdir(parents=True)
            active.write_text("SHOULD NOT BE READ", encoding="utf-8")

            def forbidden_read(self_path, *args, **kwargs):
                raise AssertionError(f"unexpected active read: {self_path}")

            with patch.object(Path, "read_text", forbidden_read):
                preview = preview_staging_version_hash(active, workspace=root)

        self.assertFalse(preview["ok"])
        self.assertFalse(preview["staging_body_read"])
        self.assertFalse(preview["active_vault_read"])
        self.assertIn("PATH_NOT_STAGING", {diagnostic["code"] for diagnostic in preview["diagnostics"]})

    def test_hash_engine_rejects_unsupported_frontmatter_fields_to_avoid_hash_aliasing(self):
        text = self._artifact_text().replace('status: "DRAFT"\n', 'status: "DRAFT"\nbeo_publication: "PUBLISHED"\n')

        with self.assertRaises(ValueError):
            compute_version_hash(text)

    def test_hash_engine_rejects_malformed_canonical_fields(self):
        for bad_text in [
            "No frontmatter\n",
            self._artifact_text(rationale=""),
            self._artifact_text(linked_nodes=["REQ-001"]),
        ]:
            with self.subTest(bad_text=bad_text[:40]):
                with self.assertRaises(ValueError):
                    compute_version_hash(bad_text)

    def test_blk119_boundary_doc_pins_hash_engine_markers(self):
        blk119 = ROOT / "docs" / "BLK-119_canonical-version-hash-engine.md"
        self.assertTrue(blk119.exists(), "BLK-119 boundary record missing")
        text = blk119.read_text()
        required = [
            "BLK_SYSTEM_119_CANONICAL_VERSION_HASH_ENGINE",
            "CANONICAL_SERIALIZATION_FIELDS_ID_SCHEMA_STATUS_RATIONALE_LINKS_BODY",
            "VERSION_HASH_SHA256_LOWERCASE_HEX",
            "VERSION_HASH_IGNORES_PARENT_HASH_AND_PREEXISTING_VERSION_HASH_FIELD",
            "HASH_PREVIEW_STAGING_ONLY_NO_ACTIVE_VAULT_READ",
            "NO_BASELINE_PROMOTION_OR_DRIFT_DECISION_BY_119",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-119 missing markers: {missing}")


class BlkReqHitlBaselinePromotionTest(unittest.TestCase):
    def _approval_payload(self, *, path: Path, workspace: Path, approval_id="APPROVAL-BLK-SYSTEM-120-REQ-001", approved=True, staging_hash=None):
        preview = preview_staging_version_hash(path, workspace=workspace)
        self.assertTrue(preview["ok"], preview)
        return {
            "idp": "discord",
            "approved": approved,
            "approval_id": approval_id,
            "discord_user_id": "684235178083745819",
            "discord_message_id": "1488733359072084070",
            "interaction_timestamp": "2026-05-14T16:30:00+00:00",
            "staging_relative_path": path.relative_to(workspace).as_posix(),
            "staging_version_hash": staging_hash or preview["version_hash"],
        }

    def test_capture_baseline_approval_binds_discord_identity_timestamp_path_and_hash_without_promotion(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            draft = write_staging_draft(
                workspace=root,
                artifact_type="REQ",
                title="Approval Capture",
                body="The gateway shall capture explicit baseline approval.",
                rationale="Needed to prove HITL approval binding.",
                linked_nodes=[],
            )
            path = root / draft["relative_path"]
            approval = capture_baseline_approval(
                self._approval_payload(path=path, workspace=root),
                staging_path=path,
                workspace=root,
            )

        self.assertEqual(approval["status"], "BASELINE_APPROVAL_CAPTURED")
        self.assertEqual(approval["idp"], "discord")
        self.assertEqual(approval["discord_user_id"], "684235178083745819")
        self.assertEqual(approval["staging_relative_path"], "docs/requirements/staging/approval-capture.md")
        self.assertRegex(approval["approval_record_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertTrue(approval["hitl_approval_capture"])
        self.assertFalse(approval["active_vault_write"])
        self.assertFalse(approval["baseline_promotion"])
        self.assertFalse(approval["exact_id_retrieval"])

    def test_capture_rejects_malformed_discord_identity_values(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            draft = write_staging_draft(
                workspace=root,
                artifact_type="REQ",
                title="Forged Identity",
                body="The gateway shall reject forged Discord identity values.",
                rationale="Needed to prevent approval forgery.",
                linked_nodes=[],
            )
            path = root / draft["relative_path"]
            payload = self._approval_payload(path=path, workspace=root)
            payload["discord_user_id"] = "not-a-snowflake"
            payload["discord_message_id"] = "also-not-a-snowflake"

            approval = capture_baseline_approval(payload, staging_path=path, workspace=root)

        self.assertEqual(approval["status"], "BASELINE_APPROVAL_REJECTED")
        codes = {diagnostic["code"] for diagnostic in approval["diagnostics"]}
        self.assertIn("DISCORD_USER_ID_INVALID", codes)
        self.assertIn("DISCORD_MESSAGE_ID_INVALID", codes)
        self.assertFalse(approval["hitl_approval_capture"])

    def test_promote_new_requirement_draft_assigns_next_id_hash_authorization_and_moves_to_active(self):
        import json
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            existing = root / "docs" / "requirements" / "active" / "REQ-001.md"
            existing.parent.mkdir(parents=True)
            existing.write_text("existing placeholder not read by promotion\n", encoding="utf-8")
            draft = write_staging_draft(
                workspace=root,
                artifact_type="REQ",
                title="Baseline Promotion",
                body="The gateway shall promote approved drafts.",
                rationale="Needed to create immutable requirement baselines.",
                linked_nodes=["[[UC-001]]"],
            )
            staging_path = root / draft["relative_path"]
            approval = self._approval_payload(path=staging_path, workspace=root)

            result = promote_staging_draft_to_baseline(
                staging_path,
                approval_payload=approval,
                workspace=root,
                used_approval_ids=[],
            )
            active_path = root / result["active_relative_path"]
            active_text = active_path.read_text(encoding="utf-8")
            metadata, body, errors = __import__("lint_artifacts").parse_artifact_text(active_text)
            authorization = json.loads(metadata["baseline_authorization"])

        self.assertEqual(result["status"], "BASELINE_PROMOTED")
        self.assertEqual(result["assigned_id"], "REQ-002")
        self.assertEqual(result["active_relative_path"], "docs/requirements/active/REQ-002.md")
        self.assertFalse(staging_path.exists())
        self.assertEqual(errors, [])
        self.assertEqual(metadata["id"], "REQ-002")
        self.assertEqual(metadata["status"], "BASELINED")
        self.assertEqual(metadata["parent_hash"], "")
        self.assertEqual(metadata["version_hash"], result["version_hash"])
        self.assertEqual(result["version_hash"], compute_version_hash(active_text))
        self.assertEqual(body, "The gateway shall promote approved drafts.\n")
        self.assertEqual(authorization["discord_user_id"], "684235178083745819")
        self.assertEqual(authorization["approval_record_hash"], result["approval_record_hash"])
        self.assertTrue(result["active_vault_write"])
        self.assertTrue(result["baseline_promotion"])
        self.assertFalse(result["exact_id_retrieval"])
        self.assertFalse(result["rtm_generation"])
        self.assertFalse(result["beo_publication"])

    def test_promotion_rejects_unapproved_mismatched_hash_or_replayed_approval_before_active_write(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            draft = write_staging_draft(
                workspace=root,
                artifact_type="REQ",
                title="Reject Promotion",
                body="The gateway shall reject invalid approval payloads.",
                rationale="Needed to prevent approval laundering.",
                linked_nodes=[],
            )
            path = root / draft["relative_path"]
            base = self._approval_payload(path=path, workspace=root)
            cases = [
                {**base, "approved": False},
                {**base, "staging_version_hash": "sha256:" + "0" * 64},
                {**base, "staging_relative_path": "docs/requirements/staging/other.md"},
            ]
            results = [
                promote_staging_draft_to_baseline(path, approval_payload=case, workspace=root, used_approval_ids=[])
                for case in cases
            ]
            replay = promote_staging_draft_to_baseline(path, approval_payload=base, workspace=root, used_approval_ids=[base["approval_id"]])
            active_files = list((root / "docs" / "requirements" / "active").glob("*.md")) if (root / "docs" / "requirements" / "active").exists() else []
            staging_still_exists = path.exists()

        for result in [*results, replay]:
            self.assertEqual(result["status"], "BASELINE_PROMOTION_REJECTED")
            self.assertFalse(result["active_vault_write"])
            self.assertFalse(result["baseline_promotion"])
        self.assertTrue(staging_still_exists)
        self.assertEqual(active_files, [])
        self.assertIn("APPROVAL_REPLAY", {diagnostic["code"] for diagnostic in replay["diagnostics"]})

    def test_promotion_rejects_durable_replay_even_without_caller_supplied_used_ids(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = write_staging_draft(
                workspace=root,
                artifact_type="REQ",
                title="Replay Durable",
                body="The gateway shall consume approval identifiers durably.",
                rationale="Needed to prevent approval replay.",
                linked_nodes=[],
            )
            first_path = root / first["relative_path"]
            approval = self._approval_payload(path=first_path, workspace=root)
            promoted = promote_staging_draft_to_baseline(first_path, approval_payload=approval, workspace=root)
            second = write_staging_draft(
                workspace=root,
                artifact_type="REQ",
                title="Replay Durable",
                body="The gateway shall consume approval identifiers durably.",
                rationale="Needed to prevent approval replay.",
                linked_nodes=[],
            )
            second_path = root / second["relative_path"]
            replayed = promote_staging_draft_to_baseline(second_path, approval_payload=approval, workspace=root)

        self.assertEqual(promoted["status"], "BASELINE_PROMOTED")
        self.assertTrue(promoted["approval_replay_ledger_written"])
        self.assertEqual(replayed["status"], "BASELINE_PROMOTION_REJECTED")
        self.assertIn("APPROVAL_REPLAY", {diagnostic["code"] for diagnostic in replayed["diagnostics"]})

    def test_promotion_rejects_publish_race_without_overwriting_existing_active_target(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            draft = write_staging_draft(
                workspace=root,
                artifact_type="REQ",
                title="Publish Race",
                body="The gateway shall not overwrite a raced active baseline target.",
                rationale="Needed to prevent active-vault overwrite races.",
                linked_nodes=[],
            )
            path = root / draft["relative_path"]
            approval = self._approval_payload(path=path, workspace=root)
            active_target = root / "docs" / "requirements" / "active" / "REQ-001.md"
            original_open = lint_artifacts_module.os.open

            def raced_open(file, flags, mode=0o777, *args, **kwargs):
                if Path(file) == active_target and flags & lint_artifacts_module.os.O_EXCL:
                    active_target.write_text("sentinel baseline must survive\n", encoding="utf-8")
                return original_open(file, flags, mode, *args, **kwargs)

            with patch.object(lint_artifacts_module.os, "open", side_effect=raced_open):
                result = promote_staging_draft_to_baseline(path, approval_payload=approval, workspace=root)
            sentinel = active_target.read_text(encoding="utf-8")
            staging_still_exists = path.exists()

        self.assertEqual(result["status"], "BASELINE_PROMOTION_REJECTED")
        self.assertFalse(result["active_vault_write"])
        self.assertFalse(result["baseline_promotion"])
        self.assertTrue(staging_still_exists)
        self.assertEqual(sentinel, "sentinel baseline must survive\n")
        self.assertIn("ACTIVE_TARGET_EXISTS", {diagnostic["code"] for diagnostic in result["diagnostics"]})

    def test_promotion_does_not_consume_replay_ledger_when_active_publish_fails(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            draft = write_staging_draft(
                workspace=root,
                artifact_type="REQ",
                title="Publish Failure",
                body="The gateway shall not consume approval IDs when active publish fails.",
                rationale="Needed to prevent false approval consumption.",
                linked_nodes=[],
            )
            path = root / draft["relative_path"]
            approval = self._approval_payload(path=path, workspace=root)
            with patch.object(lint_artifacts_module.os, "open", side_effect=OSError("publish denied")):
                result = promote_staging_draft_to_baseline(path, approval_payload=approval, workspace=root)
            ledger = root / "docs" / ".blk_req_baseline_approval_ledger.json"
            active_files = list((root / "docs" / "requirements" / "active").glob("*.md")) if (root / "docs" / "requirements" / "active").exists() else []
            staging_still_exists = path.exists()

        self.assertEqual(result["status"], "BASELINE_PROMOTION_REJECTED")
        self.assertFalse(result["active_vault_write"])
        self.assertFalse(result["approval_replay_ledger_written"])
        self.assertFalse(ledger.exists())
        self.assertEqual(active_files, [])
        self.assertTrue(staging_still_exists)
        self.assertIn("ACTIVE_PUBLISH_FAILED", {diagnostic["code"] for diagnostic in result["diagnostics"]})

    def test_promotion_rolls_back_active_when_replay_ledger_persistence_fails(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            draft = write_staging_draft(
                workspace=root,
                artifact_type="REQ",
                title="Ledger Failure",
                body="The gateway shall roll back active publish if replay persistence fails.",
                rationale="Needed to prevent partial promotion side effects.",
                linked_nodes=[],
            )
            path = root / draft["relative_path"]
            approval = self._approval_payload(path=path, workspace=root)
            ledger = root / "docs" / ".blk_req_baseline_approval_ledger.json"
            original_replace = lint_artifacts_module.os.replace

            def fail_ledger_replace(src, dst):
                if Path(dst) == ledger:
                    raise OSError("ledger persistence denied")
                return original_replace(src, dst)

            with patch.object(lint_artifacts_module.os, "replace", side_effect=fail_ledger_replace):
                result = promote_staging_draft_to_baseline(path, approval_payload=approval, workspace=root)
            active_files = list((root / "docs" / "requirements" / "active").glob("*.md")) if (root / "docs" / "requirements" / "active").exists() else []
            staging_still_exists = path.exists()
            ledger_exists = ledger.exists()

        self.assertEqual(result["status"], "BASELINE_PROMOTION_REJECTED")
        self.assertFalse(result["active_vault_write"])
        self.assertFalse(result["approval_replay_ledger_written"])
        self.assertFalse(ledger_exists)
        self.assertEqual(active_files, [])
        self.assertTrue(staging_still_exists)
        self.assertIn("APPROVAL_LEDGER_WRITE_FAILED", {diagnostic["code"] for diagnostic in result["diagnostics"]})

    def test_promotion_rejects_active_symlink_target_before_write(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            draft = write_staging_draft(
                workspace=root,
                artifact_type="REQ",
                title="Symlink Active",
                body="The gateway shall reject active symlink targets.",
                rationale="Needed to protect active-vault writes.",
                linked_nodes=[],
            )
            path = root / draft["relative_path"]
            active = root / "docs" / "requirements" / "active"
            active.mkdir(parents=True)
            (active / "REQ-001.md").symlink_to("../../../../outside.md")
            approval = self._approval_payload(path=path, workspace=root)

            result = promote_staging_draft_to_baseline(path, approval_payload=approval, workspace=root, used_approval_ids=[])

        self.assertEqual(result["status"], "BASELINE_PROMOTION_REJECTED")
        self.assertFalse(result["active_vault_write"])
        self.assertIn("ACTIVE_PATH_SYMLINK", {diagnostic["code"] for diagnostic in result["diagnostics"]})

    def test_blk120_boundary_doc_pins_hitl_baseline_promotion_markers(self):
        blk120 = ROOT / "docs" / "BLK-120_hitl-baseline-promotion.md"
        self.assertTrue(blk120.exists(), "BLK-120 boundary record missing")
        text = blk120.read_text()
        required = [
            "BLK_SYSTEM_120_HITL_BASELINE_PROMOTION",
            "DISCORD_HITL_APPROVAL_CAPTURED_FOR_NEW_BASELINES",
            "NEW_BASELINE_PROMOTION_WRITES_ACTIVE_VAULT_BY_BACKEND_ONLY",
            "BASELINE_VERSION_HASH_ASSIGNED_ON_PROMOTION",
            "ACTIVE_VAULT_WRITE_PATH_REJECTS_SYMLINKS_AND_COLLISIONS",
            "ACTIVE_VAULT_PUBLISH_IS_NO_OVERWRITE_EXCLUSIVE_CREATE",
            "APPROVAL_REPLAY_LEDGER_CONSUMES_BASELINE_APPROVAL_IDS",
            "APPROVAL_REPLAY_LEDGER_NOT_CONSUMED_ON_PUBLISH_FAILURE",
            "DISCORD_IDENTITY_VALUES_MUST_BE_SNOWFLAKE_STRINGS",
            "NO_REVISION_OVERWRITE_OR_EXACT_ID_RETRIEVAL_BY_120",
            "NEXT_FRONTIER_BLK_REQ_STAGED_REVISION_AND_EXACT_ID_RETRIEVAL_PLANNING_NOT_EXECUTION_AUTHORITY",
            "BLK-test is a BLK-System functional module, not BLK-System's test suite",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-120 missing markers: {missing}")


class BlkReqRevisionLifecycle122To124Test(unittest.TestCase):
    def _active_artifact_text(self, artifact_id="REQ-001", *, body="The gateway shall retain exact active artifacts.", rationale="Needed for revision lifecycle tests.", parent_hash="", linked_nodes=None):
        linked_nodes = ["[[UC-001]]"] if linked_nodes is None and artifact_id.startswith("REQ-") else ([] if linked_nodes is None else linked_nodes)

        def render(version_hash):
            lines = [
                "---",
                f'id: "{artifact_id}"',
                'schema_version: "1.0"',
                f'parent_hash: "{parent_hash}"',
                f'version_hash: "{version_hash}"',
                'status: "BASELINED"',
                f'rationale: "{rationale}"',
            ]
            if linked_nodes:
                lines.append("linked_nodes:")
                lines.extend(f'  - "{node}"' for node in linked_nodes)
            else:
                lines.append("linked_nodes: []")
            lines.append("---")
            lines.append(body)
            return "\n".join(lines) + "\n"

        provisional = render("PENDING")
        version_hash = compute_version_hash(provisional)
        return render(version_hash), version_hash

    def _write_active(self, root: Path, artifact_id="REQ-001", **kwargs):
        rel_dir = Path("docs/requirements/active") if artifact_id.startswith("REQ-") else Path("docs/use_cases/active")
        path = root / rel_dir / f"{artifact_id}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        text, version_hash = self._active_artifact_text(artifact_id, **kwargs)
        path.write_text(text, encoding="utf-8")
        return path, text, version_hash

    def _approval_payload(self, *, path: Path, workspace: Path, approval_id="APPROVAL-BLK-SYSTEM-124-REVISION-001"):
        preview = preview_staging_version_hash(path, workspace=workspace)
        self.assertTrue(preview["ok"], preview)
        return {
            "idp": "discord",
            "approved": True,
            "approval_id": approval_id,
            "discord_user_id": "684235178083745819",
            "discord_message_id": "1488733359072084070",
            "interaction_timestamp": "2026-05-14T19:11:27+10:00",
            "staging_relative_path": path.relative_to(workspace).as_posix(),
            "staging_version_hash": preview["version_hash"],
        }

    def test_exact_id_retrieval_reads_one_active_artifact_without_directory_scan(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_active(root, "REQ-001")
            with patch.object(Path, "iterdir", side_effect=AssertionError("broad scan attempted")):
                result = retrieve_active_artifact_by_exact_id("REQ-001", workspace=root)

        self.assertEqual(result["status"], "ACTIVE_ARTIFACT_RETRIEVED")
        self.assertEqual(result["artifact_id"], "REQ-001")
        self.assertEqual(result["artifact_type"], "REQ")
        self.assertEqual(result["active_relative_path"], "docs/requirements/active/REQ-001.md")
        self.assertEqual(result["metadata"]["id"], "REQ-001")
        self.assertTrue(result["exact_id_retrieval"])
        self.assertTrue(result["active_vault_read"])
        self.assertFalse(result["broad_active_vault_scan"])
        self.assertFalse(result["active_vault_write"])
        self.assertFalse(result["rtm_generation"])
        self.assertFalse(result["beo_publication"])

    def test_exact_id_retrieval_rejects_bad_ids_missing_files_symlinks_and_mismatched_metadata(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            malformed = retrieve_active_artifact_by_exact_id("../REQ-001", workspace=root)
            missing = retrieve_active_artifact_by_exact_id("REQ-404", workspace=root)
            active = root / "docs" / "requirements" / "active"
            active.mkdir(parents=True)
            (active / "REQ-002.md").symlink_to("../../../../outside.md")
            symlinked = retrieve_active_artifact_by_exact_id("REQ-002", workspace=root)
            mismatch_text, _ = self._active_artifact_text("REQ-003")
            (active / "REQ-004.md").write_text(mismatch_text, encoding="utf-8")
            mismatch = retrieve_active_artifact_by_exact_id("REQ-004", workspace=root)

        self.assertEqual(malformed["status"], "ACTIVE_ARTIFACT_RETRIEVAL_REJECTED")
        self.assertIn("ARTIFACT_ID_INVALID", {diagnostic["code"] for diagnostic in malformed["diagnostics"]})
        self.assertIn("ACTIVE_ARTIFACT_NOT_FOUND", {diagnostic["code"] for diagnostic in missing["diagnostics"]})
        self.assertIn("ACTIVE_PATH_SYMLINK", {diagnostic["code"] for diagnostic in symlinked["diagnostics"]})
        self.assertIn("ACTIVE_ID_MISMATCH", {diagnostic["code"] for diagnostic in mismatch["diagnostics"]})
        self.assertEqual(mismatch["body"], "")
        self.assertIsNone(mismatch["text"])
        self.assertTrue(mismatch["active_vault_read"])
        self.assertTrue(mismatch["protected_active_body_read"])
        for result in [malformed, missing, symlinked, mismatch]:
            self.assertFalse(result["active_vault_write"])
            self.assertFalse(result["broad_active_vault_scan"])

    def test_revision_draft_writer_binds_parent_hash_and_writes_staging_only(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, _, parent_hash = self._write_active(root, "REQ-001")
            result = write_staged_revision_draft(
                workspace=root,
                artifact_id="REQ-001",
                body="The gateway shall preserve revision concurrency.",
                rationale="Needed to stage exact-ID revisions.",
                linked_nodes=["[[UC-001]]"],
            )
            draft_path = root / result["relative_path"]
            text = draft_path.read_text(encoding="utf-8")
            metadata, body, errors = lint_artifacts_module.parse_artifact_text(text)

        self.assertEqual(result["status"], "REVISION_DRAFT_WRITTEN")
        self.assertEqual(result["relative_path"], "docs/requirements/staging/req-001-revision.md")
        self.assertEqual(errors, [])
        self.assertEqual(metadata["id"], "REQ-001")
        self.assertEqual(metadata["parent_hash"], parent_hash)
        self.assertEqual(metadata["version_hash"], "PENDING")
        self.assertEqual(metadata["status"], "DRAFT")
        self.assertEqual(body, "The gateway shall preserve revision concurrency.\n")
        self.assertTrue(result["exact_id_retrieval"])
        self.assertTrue(result["active_vault_read"])
        self.assertFalse(result["active_vault_write"])
        self.assertFalse(result["revision_promotion"])

    def test_revision_draft_writer_rejects_bad_retrieval_and_symlinked_staging_path(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            malformed = write_staged_revision_draft(
                workspace=root,
                artifact_id="REQ-XYZ",
                body="The gateway shall reject malformed revision IDs.",
                rationale="Needed to keep revision drafts exact-ID bound.",
                linked_nodes=[],
            )
            self._write_active(root, "REQ-001")
            staging = root / "docs" / "requirements" / "staging"
            staging.mkdir(parents=True)
            (staging / "req-001-revision.md").symlink_to("../active/REQ-001.md")
            symlinked = write_staged_revision_draft(
                workspace=root,
                artifact_id="REQ-001",
                body="The gateway shall reject symlinked staging revisions.",
                rationale="Needed to prevent staging path escape.",
                linked_nodes=["[[UC-001]]"],
            )

        self.assertEqual(malformed["status"], "REVISION_DRAFT_REJECTED")
        self.assertIn("ARTIFACT_ID_INVALID", {diagnostic["code"] for diagnostic in malformed["diagnostics"]})
        self.assertEqual(symlinked["status"], "REVISION_DRAFT_REJECTED")
        self.assertIn("STAGING_PATH_SYMLINK", {diagnostic["code"] for diagnostic in symlinked["diagnostics"]})
        self.assertFalse(symlinked["active_vault_write"])

    def test_revision_promotion_replaces_exact_active_artifact_after_hitl_parent_hash_match(self):
        import json
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, _, parent_hash = self._write_active(root, "REQ-001", body="The gateway shall keep old text.")
            draft = write_staged_revision_draft(
                workspace=root,
                artifact_id="REQ-001",
                body="The gateway shall promote approved revisions.",
                rationale="Needed to update exact active requirements.",
                linked_nodes=["[[UC-001]]"],
            )
            staging_path = root / draft["relative_path"]
            result = promote_staged_revision_to_active(
                staging_path,
                approval_payload=self._approval_payload(path=staging_path, workspace=root),
                workspace=root,
            )
            active_path = root / "docs" / "requirements" / "active" / "REQ-001.md"
            active_text = active_path.read_text(encoding="utf-8")
            metadata, body, errors = lint_artifacts_module.parse_artifact_text(active_text)
            authorization = json.loads(metadata["revision_authorization"])

        self.assertEqual(result["status"], "REVISION_PROMOTED")
        self.assertEqual(result["artifact_id"], "REQ-001")
        self.assertEqual(result["active_relative_path"], "docs/requirements/active/REQ-001.md")
        self.assertFalse(staging_path.exists())
        self.assertEqual(errors, [])
        self.assertEqual(metadata["id"], "REQ-001")
        self.assertEqual(metadata["parent_hash"], parent_hash)
        self.assertEqual(metadata["status"], "BASELINED")
        self.assertEqual(metadata["version_hash"], result["version_hash"])
        self.assertEqual(result["version_hash"], compute_version_hash(active_text))
        self.assertEqual(body, "The gateway shall promote approved revisions.\n")
        self.assertEqual(authorization["approval_record_hash"], result["approval_record_hash"])
        self.assertTrue(result["active_vault_write"])
        self.assertTrue(result["revision_promotion"])
        self.assertTrue(result["exact_id_retrieval"])
        self.assertFalse(result["revision_overwrite_without_parent_match"])
        self.assertFalse(result["rtm_generation"])
        self.assertFalse(result["beo_publication"])

    def test_revision_promotion_rejects_stale_parent_hash_without_write_or_ledger_consumption(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_active(root, "REQ-001", body="The gateway shall keep first text.")
            draft = write_staged_revision_draft(
                workspace=root,
                artifact_id="REQ-001",
                body="The gateway shall reject stale revisions.",
                rationale="Needed to prevent stale overwrite.",
                linked_nodes=["[[UC-001]]"],
            )
            staging_path = root / draft["relative_path"]
            approval = self._approval_payload(path=staging_path, workspace=root)
            active_path, current_text, _ = self._write_active(root, "REQ-001", body="The gateway shall keep concurrent text.")
            result = promote_staged_revision_to_active(staging_path, approval_payload=approval, workspace=root)
            ledger = root / "docs" / ".blk_req_baseline_approval_ledger.json"
            active_after = active_path.read_text(encoding="utf-8")
            staging_exists = staging_path.exists()
            ledger_exists = ledger.exists()

        self.assertEqual(result["status"], "REVISION_PROMOTION_REJECTED")
        self.assertIn("REVISION_PARENT_HASH_MISMATCH", {diagnostic["code"] for diagnostic in result["diagnostics"]})
        self.assertEqual(active_after, current_text)
        self.assertTrue(staging_exists)
        self.assertFalse(ledger_exists)
        self.assertFalse(result["active_vault_write"])
        self.assertFalse(result["approval_replay_ledger_written"])
        self.assertTrue(result["revision_overwrite_blocked"])

    def test_revision_promotion_rejects_existing_revision_lock_before_active_write(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            active_path, active_text, _ = self._write_active(root, "REQ-001", body="The gateway shall respect revision locks.")
            draft = write_staged_revision_draft(
                workspace=root,
                artifact_id="REQ-001",
                body="The gateway shall reject locked revision promotion.",
                rationale="Needed to prevent concurrent backend revision writes.",
                linked_nodes=["[[UC-001]]"],
            )
            staging_path = root / draft["relative_path"]
            lock_path = active_path.with_name(f".{active_path.name}.revision.lock")
            lock_path.write_text("held\n", encoding="utf-8")
            result = promote_staged_revision_to_active(
                staging_path,
                approval_payload=self._approval_payload(path=staging_path, workspace=root),
                workspace=root,
            )
            active_after = active_path.read_text(encoding="utf-8")
            ledger = root / "docs" / ".blk_req_baseline_approval_ledger.json"

        self.assertEqual(result["status"], "REVISION_PROMOTION_REJECTED")
        self.assertIn("ACTIVE_REVISION_LOCK_HELD", {diagnostic["code"] for diagnostic in result["diagnostics"]})
        self.assertEqual(active_after, active_text)
        self.assertFalse(ledger.exists())
        self.assertFalse(result["active_vault_write"])

    def test_revision_promotion_rolls_back_active_when_replay_ledger_persistence_fails(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            active_path, original_text, _ = self._write_active(root, "REQ-001", body="The gateway shall survive ledger failure.")
            draft = write_staged_revision_draft(
                workspace=root,
                artifact_id="REQ-001",
                body="The gateway shall roll back failed revision promotions.",
                rationale="Needed to prevent partial revision promotion.",
                linked_nodes=["[[UC-001]]"],
            )
            staging_path = root / draft["relative_path"]
            approval = self._approval_payload(path=staging_path, workspace=root)
            ledger = root / "docs" / ".blk_req_baseline_approval_ledger.json"
            original_replace = lint_artifacts_module.os.replace

            def fail_ledger_replace(src, dst):
                if Path(dst) == ledger:
                    raise OSError("ledger persistence denied")
                return original_replace(src, dst)

            with patch.object(lint_artifacts_module.os, "replace", side_effect=fail_ledger_replace):
                result = promote_staged_revision_to_active(staging_path, approval_payload=approval, workspace=root)
            active_after = active_path.read_text(encoding="utf-8")
            staging_exists = staging_path.exists()

        self.assertEqual(result["status"], "REVISION_PROMOTION_REJECTED")
        self.assertIn("APPROVAL_LEDGER_WRITE_FAILED", {diagnostic["code"] for diagnostic in result["diagnostics"]})
        self.assertEqual(active_after, original_text)
        self.assertTrue(staging_exists)
        self.assertFalse(result["active_vault_write"])
        self.assertFalse(result["approval_replay_ledger_written"])

    def test_revision_promotion_reports_active_side_effect_if_ledger_failure_rollback_fails(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            active_path, original_text, _ = self._write_active(root, "REQ-001", body="The gateway shall report failed rollback truthfully.")
            draft = write_staged_revision_draft(
                workspace=root,
                artifact_id="REQ-001",
                body="The gateway shall expose partial active mutation if rollback fails.",
                rationale="Needed to prevent false no-side-effect reports.",
                linked_nodes=["[[UC-001]]"],
            )
            staging_path = root / draft["relative_path"]
            approval = self._approval_payload(path=staging_path, workspace=root)
            ledger = root / "docs" / ".blk_req_baseline_approval_ledger.json"
            original_replace = lint_artifacts_module.os.replace
            active_replace_count = {"count": 0}

            def fail_ledger_and_rollback_replace(src, dst):
                dst_path = Path(dst)
                if dst_path == ledger:
                    raise OSError("ledger persistence denied")
                if dst_path == active_path:
                    active_replace_count["count"] += 1
                    if active_replace_count["count"] == 2:
                        raise OSError("rollback denied")
                return original_replace(src, dst)

            with patch.object(lint_artifacts_module.os, "replace", side_effect=fail_ledger_and_rollback_replace):
                result = promote_staged_revision_to_active(staging_path, approval_payload=approval, workspace=root)
            active_after = active_path.read_text(encoding="utf-8")

        self.assertEqual(result["status"], "REVISION_PROMOTION_REJECTED")
        self.assertIn("APPROVAL_LEDGER_WRITE_FAILED", {diagnostic["code"] for diagnostic in result["diagnostics"]})
        self.assertIn("REVISION_ROLLBACK_FAILED", {diagnostic["code"] for diagnostic in result["diagnostics"]})
        self.assertNotEqual(active_after, original_text)
        self.assertTrue(result["active_vault_write"])
        self.assertTrue(result["partial_active_mutation"])
        self.assertFalse(result["approval_replay_ledger_written"])


if __name__ == "__main__":
    unittest.main()
