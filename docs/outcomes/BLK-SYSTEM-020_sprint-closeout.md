# BLK-SYSTEM-020 — Sprint Closeout

**Status:** Complete — pending closeout commit hash until this document lands
**Date:** 2026-05-07T20:47:00+10:00
**Plan:** `docs/plans/blk-system-020_validation-command-profile-tightening.md`
**Review:** `docs/reviews/BLK-SYSTEM-020_post-remediation-hostile-review.md`

---

## 1. Executive Summary

BLK-SYSTEM-020 completed validation command profile tightening from BLK-024 Track D.

The sprint added repository-owned named `validation_profiles`, fail-closed payload validation for unknown/duplicate/mixed profile requests, exact resolved-command report evidence, BLK-pipe execution wiring, Python adapter payload compatibility, and active BLK-004 doctrine gates.

The authority movement is deliberately narrow: validation request ambiguity is reduced for future BLK-native boundaries. The sprint does not grant production BLK-test MCP, live tactical LLM execution, arbitrary shell as BLK-test behavior, protected BLK-req body access, authoritative BEO publication, RTM generation, or drift rejection authority.

---

## 2. Final Commit Table

| Task | Commit | Message | Primary artifact |
| --- | --- | --- | --- |
| 0 | `1fef4ad` | `docs: plan blk-system sprint 020 validation profiles` | Plan + task-000 outcome |
| 1 | `218467f` | `test: add validation profile payload contract gates` | RED contract/report gates |
| 2 | `03af200` | `feat: add validation profile registry and payload contract` | Go registry + payload/report contract |
| 3 | `113c0ac` | `feat: run validation profiles through blk-pipe` | BLK-pipe execution + Python adapter wiring |
| 4 | `29bf178` | `docs: define validation profile authority boundary` | BLK-004 doctrine + persistent gate |
| 5 | pending until this closeout commit lands | `docs: close blk-system sprint 020 validation profiles` | Review + closeout + task-005 outcome |

The final closeout commit cannot contain its own hash without a follow-up metadata commit. Use Git history after push as the source of truth for the Task 5 commit hash.

---

## 3. Task Outcomes

| Task | Outcome doc | Result |
| --- | --- | --- |
| 0 | `docs/outcomes/BLK-SYSTEM-020_task-000-outcome.md` | Plan published to GitHub. |
| 1 | `docs/outcomes/BLK-SYSTEM-020_task-001-outcome.md` | RED gates added and observed. |
| 2 | `docs/outcomes/BLK-SYSTEM-020_task-002-outcome.md` | Profile registry and payload/report contract implemented. |
| 3 | `docs/outcomes/BLK-SYSTEM-020_task-003-outcome.md` | Profiles wired through BLK-pipe and Python adapter. |
| 4 | `docs/outcomes/BLK-SYSTEM-020_task-004-outcome.md` | Doctrine and persistent review gate patched. |
| 5 | `docs/outcomes/BLK-SYSTEM-020_task-005-outcome.md` | Hostile review and closeout created. |

---

## 4. Profile Registry and Payload/Report Evidence

Initial approved profiles:

| Profile | Resolved commands |
| --- | --- |
| `go-test` | `go test ./...` |
| `go-vet` | `go vet ./...` |
| `go-full` | `go test ./...`; `go vet ./...` |
| `python-unittest` | `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'` |
| `docs-doctrine-gates` | `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v` |

Payload/report behavior now includes:

- `validation_profiles` on execute payloads;
- fail-closed rejection of unknown profile names;
- fail-closed rejection of duplicate profile names;
- fail-closed rejection when both `validation_profiles` and `validation_commands` are supplied;
- `validation_command_source` in reports;
- `validation_profiles` in reports;
- `resolved_validation_commands` in reports;
- deterministic `validation_NNN` logs preserved.

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

Observed verification summary before closeout docs were created:

```text
ok      github.com/camcamcami/BLK-System/cmd/blk-pipe    (cached)
ok      github.com/camcamcami/BLK-System/internal/contracts    (cached)
ok      github.com/camcamcami/BLK-System/internal/engine    0.133s
ok      github.com/camcamcami/BLK-System/internal/execguard    9.009s
ok      github.com/camcamcami/BLK-System/internal/gitguard    1.081s
ok      github.com/camcamcami/BLK-System/internal/pipe    7.575s
ok      github.com/camcamcami/BLK-System/internal/runtimeguard    (cached)
ok      github.com/camcamcami/BLK-System/internal/testutil    0.143s
ok      github.com/camcamcami/BLK-System/internal/validation    0.172s
ok      github.com/camcamcami/BLK-System/internal/validationprofiles    (cached)
Ran 316 tests in 6.476s
OK
```

Closeout-doc-only validation is recorded in `docs/outcomes/BLK-SYSTEM-020_task-005-outcome.md`.

---

## 6. Acceptance Criteria Status

| Criterion | Status |
| --- | --- |
| `validation_profiles` supported in Go payload contract | PASS |
| Unknown, duplicate, mixed profile/free-form validation requests fail closed | PASS |
| Repository-owned profile resolution covered by Go tests | PASS |
| Profile execution runs exact resolved commands and reports evidence | PASS |
| Existing validation failure/output/timeout/cleanup/staging behavior remains covered | PASS |
| Python adapter can construct profile payloads and refuses mixed sources | PASS |
| BLK-004 and persistent doctrine gates preserve profile boundary | PASS |
| Full verification passes | PASS |
| Every task has an outcome doc | PASS |
| Hostile self-review and closeout created | PASS |

---

## 7. Non-Execution Statement

BLK-SYSTEM-020 did not invoke Hindsight, Codex, live tactical LLMs, network model services, cyber tooling, production BLK-test MCP, new live BLK-test smoke runs, arbitrary shell as BLK-test behavior, protected BLK-req vault body reads/copying/parsing/hashing/mutation, authoritative BEO publication, RTM generation, RTM drift rejection authority, public ledger mutation, signer/storage/rollback authority, or source mutation outside exact approved allowlists.

---

## 8. No-Authority-Expansion Statement

The sprint only reduced validation-command ambiguity by introducing repository-owned validation profile names and auditable resolved command evidence. Legacy `validation_commands` remain trusted-local compatibility only and are not a grant of future less-trusted/autonomous shell authority.

BLK-test remains evidence-only under existing boundaries. BEO publication and RTM generation remain disabled unless later active doctrine explicitly grants separate authority.

---

## 9. Residual / Next-Sprint Seeds

Recommended follow-up candidates:

1. **BLK-SYSTEM-021 — Python adapter policy-layer hardening** (BLK-024 Track E).
2. BEB generator/profile migration if trusted-local payload producers still emit `validation_commands`.
3. Later explicit removal or stricter gating of legacy free-form validation commands after approved producers migrate.

---

## 10. Final Closeout Thesis

BLK-System now has a mechanically boring validation-profile cage: profile names are repository-owned, invalid requests fail before engine execution, BLK-pipe reports the exact commands it ran, and active doctrine states that Go remains the enforcement authority.
