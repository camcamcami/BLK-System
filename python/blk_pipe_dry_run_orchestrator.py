"""Deterministic Sprint 004 dry-run BLK-pipe payload fixtures.

This module constructs payload dictionaries only. It does not invoke blk-pipe,
Codex, model services, BLK-test, or any networked service.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


_CODEX_DRY_RUN_ARGS = [
    "exec",
    "-",
    "--json",
    "--isolated",
    "--yes",
    "--deny-read=**/.git/**",
    "--deny-read=**/node_modules/**",
    "--deny-read=**/.env*",
    "--dry-run",
]


@dataclass(frozen=True)
class TraceArtifact:
    kind: str
    id: str
    version_hash: str

    def as_payload(self) -> dict[str, str]:
        return {
            "kind": self.kind,
            "id": self.id,
            "version_hash": self.version_hash,
        }


@dataclass(frozen=True)
class DryRunSprintInput:
    beb_id: str
    profile: str
    work_dir: str
    target_branch: str
    l2_packet: str
    trace_artifacts: list[TraceArtifact]
    allowed_new_files: list[str]
    validation_commands: list[str]


def build_codex_dry_run_payload(input: DryRunSprintInput) -> dict:
    """Build a BLK-004-compatible payload for deterministic dry-run fixtures."""
    if input.profile != "codex-dry-run":
        raise ValueError("dry-run payload fixtures require profile codex-dry-run")
    if not Path(input.work_dir).is_absolute():
        raise ValueError("dry-run payload fixtures require an absolute work_dir")
    if not input.beb_id.strip():
        raise ValueError("dry-run payload fixtures require beb_id")
    if not input.target_branch.strip():
        raise ValueError("dry-run payload fixtures require target_branch")
    if input.l2_packet == "":
        raise ValueError("dry-run payload fixtures require l2_packet")
    if not input.trace_artifacts:
        raise ValueError("dry-run payload fixtures require trace artifacts")

    return {
        "action": "execute",
        "beb_id": input.beb_id,
        "work_dir": input.work_dir,
        "target_branch": input.target_branch,
        "engine": "codex-dry-run",
        "engine_args": list(_CODEX_DRY_RUN_ARGS),
        "l2_packet": input.l2_packet,
        "trace_artifacts": [artifact.as_payload() for artifact in input.trace_artifacts],
        "validation_commands": list(input.validation_commands),
        "allowed_modified_files": [],
        "allowed_new_files": list(input.allowed_new_files),
    }


def load_dry_run_fixture(
    beb_path: Path,
    l2_path: Path,
    work_dir: str,
    profile: str = "codex-dry-run",
) -> DryRunSprintInput:
    """Load the narrow Sprint 004 BEB/L2 fixture pair.

    This is intentionally not a general Markdown/YAML parser. It accepts only the
    handoff fixture frontmatter shape defined by the Sprint 004 plan.
    """
    beb_text = beb_path.read_text()
    l2_text = l2_path.read_text()
    metadata = _parse_beb_frontmatter(beb_text)

    beb_id = _required_scalar(metadata, "beb_id")
    l2_id = _required_scalar(metadata, "l2_id")
    trace_artifacts = _required_trace_artifacts(metadata)

    if f"BEB_ID: {beb_id}" not in l2_text:
        raise ValueError("L2 fixture does not bind to BEB identity")
    if f"L2_ID: {l2_id}" not in l2_text:
        raise ValueError("L2 fixture does not bind to expected L2 identity")

    return DryRunSprintInput(
        beb_id=beb_id,
        profile=profile,
        work_dir=work_dir,
        target_branch="sprint/blk-pipe-004-dry-run",
        l2_packet=l2_text,
        trace_artifacts=trace_artifacts,
        allowed_new_files=["dry_run_output.txt"],
        validation_commands=["test -f dry_run_output.txt"],
    )


def _parse_beb_frontmatter(text: str) -> list[str]:
    if not text.startswith("---\n"):
        raise ValueError("BEB fixture missing frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("BEB fixture missing closing frontmatter fence")
    return text[4:end].splitlines()


def _required_scalar(lines: list[str], key: str) -> str:
    pattern = re.compile(rf"^{re.escape(key)}:\s*\"([^\"]+)\"\s*$")
    for line in lines:
        match = pattern.match(line)
        if match:
            return match.group(1)
    raise ValueError(f"BEB fixture missing {key}")


def _required_trace_artifacts(lines: list[str]) -> list[TraceArtifact]:
    artifacts: list[TraceArtifact] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        match = re.match(r"^\s*-\s+kind:\s*\"([^\"]+)\"\s*$", line)
        if not match:
            index += 1
            continue

        artifact = {"kind": match.group(1)}
        for next_line in lines[index + 1 : index + 3]:
            scalar = re.match(r"^\s+(id|version_hash):\s*\"([^\"]+)\"\s*$", next_line)
            if scalar:
                artifact[scalar.group(1)] = scalar.group(2)
        if not {"kind", "id", "version_hash"}.issubset(artifact):
            raise ValueError("BEB fixture trace artifact is incomplete")
        artifacts.append(
            TraceArtifact(
                kind=artifact["kind"],
                id=artifact["id"],
                version_hash=artifact["version_hash"],
            )
        )
        index += 3

    if not artifacts:
        raise ValueError("BEB fixture missing trace artifacts")
    return artifacts
