import unittest
from copy import deepcopy
from pathlib import Path

from lint_artifacts import (
    BLK_REQ_DENIED_AUTHORITIES,
    build_legislative_gateway_contract,
    lint_artifact,
    validate_legislative_gateway_contract,
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


if __name__ == "__main__":
    unittest.main()
