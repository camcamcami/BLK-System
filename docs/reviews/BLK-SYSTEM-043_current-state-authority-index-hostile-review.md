# BLK-SYSTEM-043 — Current-State Authority Index Hostile Review

**Status:** PASS after remediation
**Date:** 2026-05-09T19:16:32+10:00
**Scope:** BLK-045 evaluation, BLK-046 current-state authority index, deterministic authority-index fixture, active doctrine gates, and non-execution boundary preservation.

---

## 1. Review Questions

1. Does BLK-046 or the fixture accidentally grant live Codex, BLK-pipe dispatch, BLK-test MCP, BEO publication, RTM generation, drift rejection, protected-body access, network/model/cyber/browser/package-manager tooling, or production isolation authority?
2. Does the index distinguish review-ready/fixture-ready from runtime authority?
3. Does BLK-045's supersession of BLK-024 remain clear without weakening BLK-001 through BLK-006?
4. Are all authority surfaces represented exactly once, or can a missing surface hide an unsafe default?
5. Can recursive authority-laundering keys/strings bypass fixture validation?
6. Is the next-step recommendation honest: consolidation now, explicit human approval required before any activation sprint?

---

## 2. Findings

### HR-043-001 — Recursive denied-flag and generic authority keys initially failed open

**Severity:** Blocker
**Status:** Remediated

Initial hostile review found that nested keys such as `live_codex_execution_authorized`, `runtime_authority_granted`, and `execution_authorized` could be placed inside nested surface data without causing validation failure.

Remediation:

- added regression coverage for nested denied flags and generic authority keys;
- added recursive key scanning;
- added strict top-level and per-surface key allowlists;
- rejected unsupported authority-bearing keys such as `approved`, `authorized`, `approval_status`, `runtime_authority`, and `execution_authorized`.

### HR-043-002 — Generic authority values initially failed open

**Severity:** Blocker
**Status:** Remediated

Initial hostile review found that values such as `runtime_authority_granted`, `package_manager_authorized`, and `approved for runtime execution` could pass when placed in nested strings.

Remediation:

- added recursive value scanning;
- added denied-flag value checks;
- added normalized natural-language checks for runtime execution, live Codex, BLK-test MCP, BEO publication, RTM drift rejection, protected-body reads, network tooling, package-manager tooling, and production sandbox claims.

### HR-043-003 — Separator and natural-language variants initially bypassed exact substring checks

**Severity:** Blocker
**Status:** Remediated

Later hostile review found separator variants and natural language such as `runtime-execution-authorized`, `Live Codex execution is authorized`, and `Production sandbox is enforced` could pass exact-string checks.

Remediation:

- added separator-normalized authority text scanning;
- added explicit tests for hyphen/space/underscore variants;
- added tests for `is authorized` / `are authorized` wording across all denied runtime surfaces.

### HR-043-004 — `governing_docs` initially accepted non-doc nested values

**Severity:** Blocker
**Status:** Remediated

Hostile review found that `governing_docs` only required a non-empty list and could accept nested dictionaries or authority strings.

Remediation:

- required every governing document entry to be a strict `BLK-###` string;
- added regression coverage for dictionary and authority-string laundering through `governing_docs`.

### HR-043-005 — Evaluated blocked records preserved true denied flags

**Severity:** Blocker
**Status:** Remediated

Hostile review found that `evaluate_current_state_authority_index()` forced only `runtime_authority_granted` to false and could return a blocked record still carrying another denied flag as `True`.

Remediation:

- forced every denied authority flag to `False` in evaluated output;
- expanded tests so every positive denied flag both fails validation and evaluates to a blocked record with that flag reset to `False`.

---

## 3. Final Verdict

PASS after remediation.

The final fixture is still an advisory/current-state index only. It does not start subprocesses, call Codex, call BLK-pipe, use Git, use network/model/cyber/browser/package-manager tooling, read protected BLK-req bodies, publish BEOs, generate RTMs, perform drift rejection, or claim production isolation.

The final BLK-046 document remains a map of current authority cutlines and not a runtime approval artifact. A future activation sprint still requires separate explicit human approval and a frontier-specific plan.

---

## 4. Verification Evidence

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_current_state_authority_index -q
Ran 11 tests in 0.379s
OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
Ran 64 tests in 0.005s
OK

Expanded hostile probes for natural-language authority claims, governing-doc laundering, and evaluated denied-flag reset
PASS
```
