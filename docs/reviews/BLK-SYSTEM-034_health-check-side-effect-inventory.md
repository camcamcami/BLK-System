# BLK-SYSTEM-034 — Health-Check Side-Effect Observation Inventory

**Status:** Complete inventory — not production health-check authority
**Date:** 2026-05-08T19:21:29+10:00
**Sprint:** BLK-SYSTEM-034
**Plan:** `docs/plans/blk-system-034_health-check-sandbox-side-effect-observation-boundary.md`
**Boundary:** `docs/BLK-036_track-i-health-check-sandbox-side-effect-observation-boundary.md`

---

## 1. Purpose

This inventory defines the exact observation surface for BLK-SYSTEM-034. It is an allowlist input to BLK-036 and to the Python runner implementation. It does not authorize new profiles, arbitrary shell, production health-check authority, production sandbox/cgroup/VM/network/host-secret isolation claims, BLK-pipe dispatch, production BLK-test MCP, BEO publication, RTM generation, drift rejection, protected-vault body reads, active-vault scans, Git/source repair, or package-manager execution.

---

## 2. Existing Fixed Profiles Preserved

| Profile ID | Status in BLK-SYSTEM-034 |
| --- | --- |
| `git_status_short_branch` | Preserved from BLK-034/BLK-035 |
| `active_doctrine_gate` | Preserved from BLK-034/BLK-035 |
| `python_unittest_discovery` | Preserved from BLK-035 |
| `go_test_all` | Preserved from BLK-035 |
| `go_vet_all` | Preserved from BLK-035 |

No new profile IDs are part of this sprint.

---

## 3. Authorized Observation Surfaces

| Surface | Mechanism | PASS impact | Authority caveat |
| --- | --- | --- | --- |
| Git workspace status | Before/after `git status --porcelain=v1 --untracked-files=all` with optional locks disabled | Changed status blocks advisory PASS | Absence of change is not proof of no source-byte side effect |
| Repo-local cache artifacts | Before/after repository scan for `__pycache__` directories and `.pyc` files | Appearance/change blocks advisory PASS | Observation is limited to repo-local Python cache artifacts |
| Runner-owned temp/cache directory | Per-run temp directory outside repo; `TMPDIR`, `TMP`, `TEMP`, and `PYTHONPYCACHEPREFIX` point inside it | Failure to remove is reportable evidence | Not a production filesystem sandbox or host-secret boundary |
| Timeout cleanup | Fixed profile subprocess starts a new process group/session; timeout cleanup kills the group | Timeout blocks advisory PASS | Process-group cleanup is local hygiene, not cgroup/VM containment |
| Output bounding | Existing output byte gate and bounded excerpts | Output flood blocks advisory PASS | Does not authorize raw log embedding |
| Redaction | Existing secret-pattern redaction on excerpts | Redaction is advisory evidence hygiene | Does not claim host secret isolation |

---

## 4. Explicit Non-Claims

The runner must not report these as observed/enforced facts unless a later sprint implements them mechanically:

- production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux enforcement;
- network firewall or egress denial enforcement;
- host-secret isolation;
- full source-mutation proof beyond observed Git/cache surfaces;
- protected BLK-req body read detection beyond forbidden profile-text rejection;
- active-vault scan detection beyond forbidden profile-text rejection;
- BEO publication prevention beyond no-authority result vocabulary;
- RTM generation or drift decision prevention beyond no-authority result vocabulary.

Use explicit non-claim values such as `NOT_ENFORCED_BY_PILOT` or `NOT_MEASURED_BY_PILOT` for these surfaces.

---

## 5. Blocking Conditions

A fixed profile result must become `BLOCKED_ADVISORY_ONLY` when any of these happen during the run:

1. timeout;
2. output byte limit exceeded;
3. Git workspace status changed;
4. repo-local `__pycache__` / `.pyc` artifacts appeared or changed;
5. runner-owned temporary directory cleanup failed;
6. subprocess startup fails before producing trustworthy bounded evidence.

---

## 6. Review Questions for Task 3

1. Did the sprint preserve exactly the five BLK-035 profile IDs?
2. Are temp/cache paths outside the repo and runner-owned per run?
3. Can repo-local cache artifact creation block PASS even if Git status observation is under-scoped?
4. Does timeout cleanup target the process group/session?
5. Does result vocabulary avoid production sandbox, network firewall, and host-secret isolation claims?
6. Does PASS remain advisory only?
