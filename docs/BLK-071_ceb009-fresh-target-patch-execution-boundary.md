# BLK-071 — CEB_009 Fresh-Target Patch Execution Boundary

**Status:** Active exact-target execution boundary — one BLK-pipe-mediated local Kuronode patch commit is authorized for `70b6062b92cf61c12bf190f92dc6b45ea4dcd438`; remote push and adjacent authorities remain unauthorized
**Date:** 2026-05-11T08:45:00+10:00
**Purpose:** Define the BLK-SYSTEM-066 boundary for using the user's fresh approval to patch CEB_009 against the current observed Kuronode `origin/main` target.
**Scope:** One local BLK-pipe-mediated patch attempt against `/home/dad/code/Kuronode-v1` after local checkout synchronization to the approved SHA. Only `scripts/smoke_test.ts` may be source-mutated. This boundary does not authorize Kuronode remote push, live Codex, BLK-test MCP, Electron/smoke runtime, TypeScript/package-manager tooling, BEO/CEO publication, RTM, protected reads, coverage/drift claims, or production isolation claims.

---

## 0. Boundary Markers

```text
KURONODE_POWER_OF_TEN_CEB009_FRESH_TARGET_PATCH_EXECUTION_BOUNDARY
KURONODE_POWER_OF_TEN_CEB009_FRESH_TARGET_PATCH_EXECUTION_READY_FOR_BLK_PIPE
KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_BLK_PIPE_COMMITTED_NOT_PUSHED
PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_066_CEB009_FRESH_TARGET_PATCH_EXECUTION
```

Fresh approval targets only:

```text
70b6062b92cf61c12bf190f92dc6b45ea4dcd438
```

Local checkout synchronization to this SHA is permitted only to prepare the approved target. It is not authority to patch any other SHA.

---

## 1. Authorized Scope

BLK-SYSTEM-066 may:

1. capture the user's fresh `I approve` response as approval for the displayed current SHA `70b6062b92cf61c12bf190f92dc6b45ea4dcd438`;
2. fetch Kuronode `origin` and reset local `main` to exactly that SHA;
3. verify local HEAD and observed `origin/main` both equal that SHA;
4. build one BLK-pipe payload with:
   - `work_dir=/home/dad/code/Kuronode-v1`;
   - `target_branch=main`;
   - `allowed_modified_files=[scripts/smoke_test.ts]`;
   - `allowed_new_files=[]`;
   - `engine=python3`;
   - validation command `git diff --check -- scripts/smoke_test.ts` only;
5. invoke Go `blk-pipe` at most once;
6. accept a local BLK-pipe-created Kuronode commit if and only if the report status is `SUCCESS` and staged/committed files are exactly allowlisted;
7. record the raw BLK-pipe report and hostile-review outcome in BLK-System docs.

---

## 2. Exact Patch Intent

The only authorized source mutation is CEB_009 remediation of `scripts/smoke_test.ts`:

1. remove `@ts-ignore` and unsafe `any` projection-result access;
2. add typed preload API and projection-result guard logic;
3. fail on timeout sentinel before PASS logging;
4. fail on missing AST payload before PASS logging;
5. preserve listener unsubscribe cleanup;
6. preserve Electron close cleanup in `finally`.

---

## 3. Explicit Non-Authority

No Kuronode remote push.

No source or Git mutation outside exact BLK-pipe allowlists.

No retargeting to any SHA other than `70b6062b92cf61c12bf190f92dc6b45ea4dcd438`.

No live Codex execution.

No production BLK-test MCP authority.

No generic BLK-test MCP authority.

No reusable BLK-test service startup.

No arbitrary shell as BLK-test behavior.

No Electron launch, no headless smoke-test execution, and no wall-clock timeout wait.

No TypeScript tooling, typechecker, linter, formatter, or package-manager execution.

No package-manager, network, model-service, browser, or cyber tooling authority.

No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison.

No authoritative BEO publication.

No CEO_009 publication.

No runtime `PUBLISHED` BEO output.

No signer key material access.

No cryptographic signing.

No immutable storage writes.

No public ledger append or mutation.

No runtime RTM generation or RTM drift rejection.

No active-vault hash comparison, coverage matrix, coverage claim, or drift decision.

No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim.

---

## 4. Success Interpretation

If BLK-pipe succeeds, the sprint may return:

```text
KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_BLK_PIPE_COMMITTED_NOT_PUSHED
```

That state means only a local BLK-pipe-enforced Kuronode commit exists. It is not remote publication, not BEO/CEO publication, not BLK-test PASS evidence, not runtime smoke evidence, and not RTM trace closure.
