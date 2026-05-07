# BLK-SYSTEM-020 — Task 001 Outcome

**Task:** Add RED gates for validation profile payload contract  
**Status:** Complete — RED gates added and observed  
**Date:** 2026-05-07T20:18:00+10:00

---

## 1. Objective

Prove the current payload/report contract lacks a repository-owned validation profile path and lacks fail-closed checks/evidence for invalid or mixed profile requests.

---

## 2. Files Changed

```text
internal/contracts/payload_test.go
internal/contracts/report_test.go
docs/outcomes/BLK-SYSTEM-020_task-001-outcome.md
```

---

## 3. RED Gates Added

Added focused contract tests for:

1. accepting V47 payloads with `validation_profiles: ["go-full"]` and preserving `Payload.ValidationProfiles`;
2. rejecting unknown profiles such as `curl-production`;
3. rejecting mixed `validation_profiles` and legacy `validation_commands`;
4. rejecting duplicate profile names;
5. preserving legacy `validation_commands` only as trusted-local compatibility, not future less-trusted/autonomous authority;
6. emitting report evidence for profile source, requested profile names, and exact resolved commands.

---

## 4. RED Evidence

Command run:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/contracts -run 'TestDecodePayload.*ValidationProfile|TestReport.*ValidationProfile|TestDecodePayload.*Legacy' -count=1
```

Observed RED output:

```text
# github.com/camcamcami/BLK-System/internal/contracts [github.com/camcamcami/BLK-System/internal/contracts.test]
internal/contracts/payload_test.go:184:27: payload.ValidationProfiles undefined (type Payload has no field or method ValidationProfiles)
internal/contracts/payload_test.go:235:27: payload.ValidationProfiles undefined (type Payload has no field or method ValidationProfiles)
internal/contracts/report_test.go:102:3: unknown field ValidationCommandSource in struct literal of type Report
internal/contracts/report_test.go:103:3: unknown field ValidationProfiles in struct literal of type Report
internal/contracts/report_test.go:104:3: unknown field ResolvedValidationCommands in struct literal of type Report
FAIL	github.com/camcamcami/BLK-System/internal/contracts [build failed]
FAIL
```

The RED failure is expected: the production contract has not yet added the requested fields or validation profile registry.

---

## 5. Verification / Hygiene

`git diff --check` was run before commit for the exact touched paths.

---

## 6. Non-Execution Statement

Task 001 did not invoke Hindsight, Codex, live tactical LLMs, network model services, cyber tooling, BLK-pipe implementation execution, production BLK-test MCP, new live BLK-test smoke runs, arbitrary shell as BLK-test behavior, protected BLK-req vault body reads/copying/parsing/hashing/mutation, authoritative BEO publication, RTM generation, RTM drift rejection authority, public ledger mutation, signer/storage/rollback authority, or source mutation outside exact approved allowlists.

---

## 7. Next Task

Task 002 must implement the repository-owned validation profile registry and payload/report contract until these RED gates pass.
