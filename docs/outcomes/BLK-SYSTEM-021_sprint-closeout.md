# BLK-SYSTEM-021 — Sprint Closeout

**Status:** Complete — pending closeout commit hash until this document lands
**Date:** 2026-05-07T21:38:00+10:00
**Plan:** `docs/plans/blk-system-021_python-adapter-policy-layer-hardening.md`
**Review:** `docs/reviews/BLK-SYSTEM-021_post-remediation-hostile-review.md`

---

## 1. Executive Summary

BLK-SYSTEM-021 completed Python adapter policy-layer hardening from BLK-024 Track E.

The sprint added fail-fast Python adapter preflight for canonical `trace_artifacts`, absolute work directories, empty execute fields, protected BLK-req allowlist paths, validation-profile hygiene, bounded trusted-local validation commands, scrubbed subprocess environment handling, raw report preservation tests, and active BLK-004 doctrine gates.

The authority movement is deliberately narrow: Python reduces local operator/orchestrator mistakes before subprocess invocation. Go `blk-pipe` remains the final deterministic enforcement authority.

---

## 2. Final Commit Table

| Task | Commit | Message | Primary artifact |
| --- | --- | --- | --- |
| 0 | `bb8dbef` | `docs: plan blk-system sprint 021 python adapter policy` | Plan + task-000 outcome |
| 1 | `b9c3d91` | `test: add python adapter policy preflight gates` | RED adapter policy gates |
| 2 | `9c7544a` | `feat: add python adapter payload policy preflight` | Adapter payload preflight helpers |
| 3 | `2aced4e` | `feat: scrub python adapter subprocess environment` | Subprocess env + report preservation |
| 4 | `25c0409` | `docs: define python adapter policy boundary` | BLK-004 doctrine + persistent gate |
| 5 | pending until this closeout commit lands | `docs: close blk-system sprint 021 python adapter policy` | Review + closeout + task-005 outcome + final remediation |

The final closeout commit cannot contain its own hash without a follow-up metadata commit. Use Git history after push as the source of truth for the Task 5 commit hash.

---

## 3. Task Outcomes

| Task | Outcome doc | Result |
| --- | --- | --- |
| 0 | `docs/outcomes/BLK-SYSTEM-021_task-000-outcome.md` | Plan published to GitHub. |
| 1 | `docs/outcomes/BLK-SYSTEM-021_task-001-outcome.md` | RED gates added and observed. |
| 2 | `docs/outcomes/BLK-SYSTEM-021_task-002-outcome.md` | Adapter execute payload preflight implemented. |
| 3 | `docs/outcomes/BLK-SYSTEM-021_task-003-outcome.md` | Subprocess env and report preservation hardened. |
| 4 | `docs/outcomes/BLK-SYSTEM-021_task-004-outcome.md` | Doctrine and persistent review gate patched. |
| 5 | `docs/outcomes/BLK-SYSTEM-021_task-005-outcome.md` | Hostile review, final remediation, and closeout created. |

---

## 4. Implemented Behavior

Python adapter now rejects before subprocess invocation:

- missing or empty execute `trace_artifacts`;
- malformed trace artifact entries;
- non-canonical trace hashes outside `sha256:<64-lowercase-hex>`;
- non-absolute `work_dir`;
- empty `beb_id`, `target_branch`, `engine`, or `l2_packet`;
- absolute/traversing/non-string allowlist paths;
- protected BLK-req allowlist paths under `docs/active/`, `docs/requirements/`, or `docs/use_cases/`;
- duplicate, empty, or non-string `validation_profiles`;
- empty, non-string, too many, or oversized trusted-local `validation_commands`.

Python adapter subprocess handling now:

- uses shell-free list argv for payload invocation and health check;
- scrubs `SSH_AUTH_SOCK`, `SSH_AGENT_PID`, and `SSH_ASKPASS`;
- sets `PWD` to payload `work_dir` when invoking payloads;
- preserves raw Go report evidence and stderr.

---

## 5. Final Verification Output

Commands run:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./...
go vet ./...
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
git diff --check
git status --short --branch
```

Observed verification summary before closeout docs were staged:

```text
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/contracts	(cached)
ok  	github.com/camcamcami/BLK-System/internal/engine	(cached)
ok  	github.com/camcamcami/BLK-System/internal/execguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/gitguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/pipe	7.388s
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/testutil	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validation	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validationprofiles	(cached)
Ran 328 tests in 6.457s
OK
```

Closeout-doc-only validation is recorded in `docs/outcomes/BLK-SYSTEM-021_task-005-outcome.md`.

---

## 6. Acceptance Criteria Status

| Criterion | Status |
| --- | --- |
| Execute payloads require non-empty canonical `trace_artifacts` | PASS |
| Empty critical fields and non-absolute `work_dir` rejected | PASS |
| Protected BLK-req allowlist paths rejected early | PASS |
| Validation profile policy preserved | PASS |
| Payload and health subprocess invocations scrub high-risk SSH/askpass env | PASS |
| Raw Go report evidence and non-success status preserved | PASS |
| Revert payload remains separate from execute-only fields | PASS |
| BLK-004 and persistent doctrine gates preserve adapter boundary | PASS |
| Full verification passes | PASS |
| Every task has an outcome doc | PASS |
| Hostile self-review and closeout created | PASS |

---

## 7. Non-Execution Statement

BLK-SYSTEM-021 did not invoke Hindsight, Codex, live tactical LLMs, network model services, cyber tooling, production BLK-test MCP, new live BLK-test smoke runs, arbitrary shell as BLK-test behavior, protected BLK-req vault body reads/copying/parsing/hashing/mutation, authoritative BEO publication, RTM generation, RTM drift rejection authority, public ledger mutation, signer/storage/rollback authority, or source mutation outside exact approved allowlists.

---

## 8. No-Authority-Expansion Statement

The sprint only reduced Python adapter/orchestrator misuse risk. Python adapter checks are fail-fast convenience only and are not the final authority.

Go `blk-pipe` remains the final deterministic authority for payload validation, protected-path classification, validation profile resolution, execution, cleanup, Git routing, and report evidence.

BLK-test remains evidence-only under existing boundaries. BEO publication and RTM generation remain disabled unless later active doctrine explicitly grants separate authority.

---

## 9. Residual / Next-Sprint Seeds

Recommended follow-up candidates:

1. BEB generator/profile migration if trusted-local payload producers still emit `validation_commands`.
2. Later explicit removal or stricter gating of legacy free-form validation commands after approved producers migrate.
3. BLK-test pilot design review only after profile/adapter hardening remains stable under hostile review.

---

## 10. Final Closeout Thesis

BLK-System now has a safer Python adapter policy layer: malformed BLK-native payloads fail earlier and more readably, subprocess environment handling is less leaky, and raw Go report evidence remains intact. The authority boundary stayed intact: Python helps the operator avoid mistakes; Go `blk-pipe` still enforces the law.
