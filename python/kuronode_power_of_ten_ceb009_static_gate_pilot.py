"""CEB_009 static Power-of-Ten gate pilot fixture.

This module evaluates BLK-System-owned CEB_009 TypeScript fixture material. It
returns deterministic static findings only. It does not scan a live Kuronode
checkout, launch Electron, run the smoke test, execute TypeScript tooling, invoke
package managers, start Codex or BLK-test MCP, mutate source/Git, publish BEOs,
generate RTM, or read protected BLK-req bodies.
"""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from typing import Any
from urllib.parse import unquote

from authoritative_beo_publication_authority_request import _canonical_hash, _required_hash, _required_string
from kuronode_power_of_ten_static_profile import (
    EXACT_EXCLUDED_AUTHORITIES as STATIC_PROFILE_EXCLUDED_AUTHORITIES,
    PROFILE_NAME as STATIC_PROFILE_NAME,
    REQUEST_STATUS as STATIC_PROFILE_REQUEST_STATUS,
    evaluate_kuronode_power_of_ten_static_profile,
)

READY_STATUS = "KURONODE_POWER_OF_TEN_CEB009_STATIC_GATE_PILOT_FINDINGS_READY_NOT_RUNTIME"
REQUEST_STATUS = "KURONODE_POWER_OF_TEN_CEB009_STATIC_GATE_PILOT_FIXTURE_ONLY"
KURONODE_HEAD = "cb09d965c0407612c9ce8fc9cc58c5e62c82e1b2"
SOURCE_CORPUS_ID = "BLK-SYSTEM-059-CEB009-STATIC-CORPUS"

EXACT_EXCLUDED_AUTHORITIES = {
    "LIVE_KURONODE_REPOSITORY_SCAN",
    "LIVE_KURONODE_SOURCE_VALIDATION",
    "ELECTRON_OR_SMOKE_TEST_EXECUTION",
    "WALL_CLOCK_TIMEOUT_WAIT",
    "TYPESCRIPT_TOOLING_EXECUTION",
    "PACKAGE_MANAGER_INVOCATION",
    "NETWORK_ACCESS",
    "MODEL_SERVICE_ACCESS",
    "BROWSER_OR_CYBER_TOOLING",
    "SOURCE_OR_GIT_MUTATION_BY_GATE",
    "LIVE_CODEX_EXECUTION",
    "LIVE_TACTICAL_LLM_DISPATCH",
    "PRODUCTION_BLK_TEST_MCP",
    "GENERIC_BLK_TEST_MCP",
    "REUSABLE_BLK_TEST_SERVICE_STARTUP",
    "ARBITRARY_SHELL_OR_CALLER_SUPPLIED_COMMANDS",
    "PROTECTED_BLK_REQ_BODY_READ",
    "AUTHORITATIVE_BEO_PUBLICATION",
    "RUNTIME_PUBLISHED_BEO_OUTPUT",
    "LIVE_PUBLICATION_APPROVAL_CAPTURE",
    "SIGNER_KEY_MATERIAL_ACCESS",
    "CRYPTOGRAPHIC_SIGNING",
    "IMMUTABLE_STORAGE_WRITE",
    "PUBLIC_LEDGER_APPEND_OR_MUTATION",
    "ROLLBACK_REVOCATION_SUPERSESSION_EXECUTION",
    "RUNTIME_RTM_GENERATION",
    "RTM_DRIFT_REJECTION",
    "ACTIVE_VAULT_HASH_COMPARISON",
    "COVERAGE_MATRIX_OR_CLAIM",
    "PRODUCTION_SANDBOX_OR_HOST_SECRET_ISOLATION_CLAIM",
}

_REQUEST_KEYS = {
    "request_status",
    "request_id",
    "operator_identity",
    "source_corpus_id",
    "source_corpus_hash",
    "kuronode_head",
    "excluded_authorities",
    "operator_note",
}

_LAUNDERING_RE = re.compile(
    r"approved[_\s-]*for[_\s-]*live[_\s-]*execution|runtime[_\s-]*pilot[_\s-]*approved|"
    r"live[_\s-]*(?:scan|validation)[_\s-]*(?:allowed|authorized|authorised|approved)|"
    r"run[_\s-]*(?:npm|npx|pnpm|yarn|bun)|npm[_\s-]*run[_\s-]*test:?smoke|test:?smoke|"
    r"electron[_\s-]*(?:launch|started|executed)|smoke[_\s-]*test[_\s-]*(?:executed|passed|started)|"
    r"\b(?:tsc|eslint|prettier|npm|npx|pnpm|yarn|bun|curl|wget|ssh|scp|rsync|docker|deno)\b|"
    r"codex|blk[-_\s]*test[_\s-]*mcp|beo[_\s-]*publication|authoritative[_\s-]*beo|"
    r"rtm(?:id|generation|generated)?|drift[_\s-]*rejection|coverage[_\s-]*(?:matrix|claim)|"
    r"active[_\s-]*vault[_\s-]*hash[_\s-]*comparison|source[_\s-]*mutation|git[_\s-]*mutation|"
    r"protected[_\s-]*blk[-_\s]*req[_\s-]*body|private[_\s-]*key|api[_\s-]*key|bearer",
    re.IGNORECASE,
)
_PROTECTED_RE = re.compile(r"docs[\\/]+(?:active|requirements|use_cases)[\\/]+|protected[_\s-]*blk[-_\s]*req[_\s-]*body", re.IGNORECASE)


def default_ceb009_static_corpus() -> list[dict[str, str]]:
    """Return the BLK-System-owned CEB_009 TypeScript fixture descriptor."""

    return [
        {
            "path": "scripts/smoke_test.ts",
            "language": "typescript",
            "content": _CEB009_SMOKE_TEST_TS,
        }
    ]


def default_ceb009_static_request(corpus: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Return a valid static-pilot request for the supplied corpus."""

    selected = default_ceb009_static_corpus() if corpus is None else corpus
    return {
        "request_status": REQUEST_STATUS,
        "request_id": "BLK-SYSTEM-059-CEB009-STATIC-GATE-PILOT-001",
        "operator_identity": "discord:684235178083745819",
        "source_corpus_id": SOURCE_CORPUS_ID,
        "source_corpus_hash": _corpus_hash(selected),
        "kuronode_head": KURONODE_HEAD,
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
        "operator_note": "static CEB_009 fixture material only",
    }


def build_ceb009_static_gate_pilot_report(*, corpus: list[dict[str, Any]], request: dict[str, Any]) -> dict[str, Any]:
    """Build deterministic CEB_009 static findings without runtime side effects."""

    validated_request = _validate_request(request, corpus)
    static_profile_report = evaluate_kuronode_power_of_ten_static_profile(
        files=deepcopy(corpus),
        request=_static_profile_request(validated_request, corpus),
    )
    ceb009_findings = _scan_ceb009_semantics(corpus)
    report = {
        "report_status": READY_STATUS,
        "pilot_scope": "CEB_009_STATIC_FIXTURE_ONLY_NOT_RUNTIME",
        "request_id": validated_request["request_id"],
        "operator_identity": validated_request["operator_identity"],
        "source_corpus_identity": {
            "source_corpus_id": validated_request["source_corpus_id"],
            "source_corpus_hash": validated_request["source_corpus_hash"],
            "ceb_id": "CEB_009",
            "l2_packet_id": "CEB_009_L2_packet",
            "kuronode_head": validated_request["kuronode_head"],
        },
        "source_file_count": len(corpus),
        "static_profile_report": static_profile_report,
        "ceb009_findings": ceb009_findings,
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
        "live_kuronode_scan_performed": False,
        "electron_launched": False,
        "smoke_test_executed": False,
        "timeout_path_waited": False,
        "typescript_tooling_executed": False,
        "package_manager_invoked": False,
        "network_accessed": False,
        "source_mutation_performed": False,
        "git_mutation_performed": False,
        "codex_started": False,
        "blk_test_mcp_started": False,
        "protected_body_read": False,
        "beo_published": False,
        "rtm_generated": False,
        "coverage_claimed": False,
        "production_isolation_claimed": False,
    }
    report["report_hash"] = _canonical_hash({key: value for key, value in report.items() if key != "report_hash"})
    return report


def _validate_request(request: dict[str, Any], corpus: list[dict[str, Any]]) -> dict[str, str]:
    if not isinstance(request, dict):
        raise ValueError("request must be a dictionary")
    _enforce_keys(request, _REQUEST_KEYS, "request")
    _reject_laundering({key: value for key, value in request.items() if key != "excluded_authorities"}, "request")
    if _required_string(request.get("request_status"), "request_status") != REQUEST_STATUS:
        raise ValueError("request_status must be KURONODE_POWER_OF_TEN_CEB009_STATIC_GATE_PILOT_FIXTURE_ONLY")
    _validate_excluded_authorities(request.get("excluded_authorities"))
    source_corpus_hash = _required_hash(request.get("source_corpus_hash"), "source_corpus_hash")
    if source_corpus_hash != _corpus_hash(corpus):
        raise ValueError("source_corpus_hash does not match submitted corpus")
    if _required_string(request.get("kuronode_head"), "kuronode_head") != KURONODE_HEAD:
        raise ValueError("kuronode_head must match the planned CEB_009 fixture HEAD")
    return {
        "request_id": _required_string(request.get("request_id"), "request_id"),
        "operator_identity": _required_string(request.get("operator_identity"), "operator_identity"),
        "source_corpus_id": _required_string(request.get("source_corpus_id"), "source_corpus_id"),
        "source_corpus_hash": source_corpus_hash,
        "kuronode_head": KURONODE_HEAD,
    }


def _static_profile_request(validated_request: dict[str, str], corpus: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "profile_name": STATIC_PROFILE_NAME,
        "request_status": STATIC_PROFILE_REQUEST_STATUS,
        "request_id": validated_request["request_id"],
        "operator_identity": validated_request["operator_identity"],
        "trace_artifacts": [{"kind": "BLK", "id": "BLK-058", "version_hash": "sha256:" + "5" * 64}],
        "source_bundle_id": validated_request["source_corpus_id"],
        "source_bundle_hash": _corpus_hash(corpus),
        "excluded_authorities": sorted(STATIC_PROFILE_EXCLUDED_AUTHORITIES),
        "operator_note": "fixture-only static profile descriptors",
    }


def _scan_ceb009_semantics(corpus: list[dict[str, Any]]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for file_desc in corpus:
        path = _required_string(file_desc.get("path"), "path")
        content = _required_string(file_desc.get("content"), "content")
        if "streamId: 'timeout'" in content and "[PASS]" in content and "process.exit(0)" in content and "streamId === 'timeout'" not in content:
            findings.append(_finding(path, _line_of(content, "[PASS]"), "CEB009_TIMEOUT_FALSE_PASS_RISK", "risk"))
        if "setTimeout" in content and "30000" in content:
            findings.append(_finding(path, _line_of(content, "setTimeout"), "CEB009_TIMEOUT_BOUND_RECORDED", "positive", {"timeout_ms": 30000, "executed": False}))
        if ".ast" not in content:
            findings.append(_finding(path, _line_of(content, "const result = await projectionPromise"), "CEB009_RESULT_SHAPE_VALIDATION_MISSING", "risk"))
        if "@ts-ignore" in content or "as any" in content:
            findings.append(_finding(path, _line_of(content, "@ts-ignore") or _line_of(content, "as any"), "CEB009_UNSAFE_ANY_OR_TS_IGNORE_RECORDED", "risk"))
        if "finally" in content and "electronApp.close()" in content and "unsub()" in content:
            findings.append(_finding(path, _line_of(content, "finally"), "CEB009_CLEANUP_PATH_RECORDED", "positive", {"executed": False}))
    return findings


def _corpus_hash(corpus: list[dict[str, Any]]) -> str:
    stable = json.dumps(deepcopy(corpus), sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(stable).hexdigest()


def _validate_excluded_authorities(excluded: Any) -> None:
    if (
        not isinstance(excluded, list)
        or not all(isinstance(item, str) for item in excluded)
        or set(excluded) != EXACT_EXCLUDED_AUTHORITIES
        or len(excluded) != len(EXACT_EXCLUDED_AUTHORITIES)
    ):
        raise ValueError("excluded_authorities must match exact denied authority set")


def _enforce_keys(value: dict[str, Any], allowed: set[str], label: str) -> None:
    extra = sorted(set(value) - allowed)
    if extra:
        raise ValueError(f"{label} contains unexpected field(s): {extra}")


def _reject_laundering(value: Any, label: str) -> None:
    if isinstance(value, dict):
        for item in value.values():
            _reject_laundering(item, label)
    elif isinstance(value, list):
        for item in value:
            _reject_laundering(item, label)
    elif isinstance(value, str):
        normalized = _normalize_text(value)
        if _PROTECTED_RE.search(normalized):
            raise ValueError(f"{label} rejects protected BLK-req body reference")
        if _LAUNDERING_RE.search(normalized):
            raise ValueError(f"{label} rejects authority-laundering text")


def _normalize_text(value: str) -> str:
    decoded = value
    for _ in range(3):
        next_decoded = unquote(decoded)
        if next_decoded == decoded:
            break
        decoded = next_decoded
    return decoded.replace("\\", "/")


def _line_of(content: str, needle: str) -> int:
    index = content.find(needle)
    if index < 0:
        return 1
    return content[:index].count("\n") + 1


def _finding(path: str, line: int, rule: str, polarity: str, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    finding = {"path": path, "line": line, "rule": rule, "polarity": polarity}
    if extra:
        finding.update(extra)
    return finding


_CEB009_SMOKE_TEST_TS = """import { _electron as electron } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';

(async () => {
  let electronApp;
  try {
    console.log('[SMOKE] Launching Electron...');
    electronApp = await electron.launch({
      cwd: path.resolve(process.cwd(), 'packages/electron'),
      args: ['.', '--disable-gpu', '--no-sandbox', '--no-zygote', '--disable-gpu-compositing', '--ozone-platform=x11'],
      env: {
        ...process.env,
        DISPLAY: process.env.DISPLAY || ':99',
        ELECTRON_OZONE_PLATFORM_HINT: 'x11',
      },
    });

    const window = await electronApp.firstWindow();
    console.log('[SMOKE] Window captured. Waiting for renderer bootstrap (#root)...');
    await window.waitForSelector('#root', { timeout: 10000 });

    // Pre-flight check: see if the scaffold text exists
    const bodyText = await window.innerText('body');
    if (!bodyText.includes('Electron scaffold verified')) {
      throw new Error('Renderer scaffold verification failed');
    }

    // Trigger path observation:
    // We observe the IPC push instead of DOM if .joint-cell isn't ready.
    console.log('[SMOKE] Listening for kur:projection-result...');
    const projectionPromise = window.evaluate(() => {
      return new Promise((resolve) => {
        // @ts-ignore
        const unsub = window.KuronodeAPI.onProjectionResult((result) => {
          unsub();
          resolve(result);
        });
        // Timeout guard — pipeline must respond within 30s
        setTimeout(() => resolve({ streamId: 'timeout', _type: 'timeout' }), 30000);
      });
    });

    // Trigger the pipeline via IntentTrigger (Preload API)
    console.log('[SMOKE] Triggering pipeline via intentTrigger...');
    await window.evaluate(() => {
      // @ts-ignore
      window.KuronodeAPI.intentTrigger({ anchors: ['Drone'], scope: 'structural' });
    });

    const result = await projectionPromise;
    console.log('[SMOKE] Received projection result:', (result as any).streamId);

    console.log('[PASS] Headless Pipeline Smoke Test Succeeded.');
    process.exit(0);
  } catch (error) {
    console.error('[FAIL] Smoke test failed:', error);
    process.exit(1);
  } finally {
    if (electronApp) {
      await electronApp.close();
    }
  }
})();"""
