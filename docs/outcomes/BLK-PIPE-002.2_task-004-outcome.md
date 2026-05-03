# BLK-pipe Sprint 002.2 — Task 4 Outcome

**Status:** Complete
**Date:** 2026-05-04
**Task:** Deliver V47 `l2_packet` to Engine Stdin
**Implementation Commit:** `1053e57 feat: deliver blk-pipe l2 packet to engine stdin`
**Remote:** pushed to `origin/main`
**Plan:** `docs/plans/BLK-PIPE-002.2_cyber-readiness-remediation.md`

---

## 1. Objective

Task 4 closed the hostile-review finding that V47 `l2_packet` was accepted in payloads but dropped before engine execution.

BLK-pipe now normalizes V47 `l2_packet`, bounds it, and delivers it to the engine through stdin. The packet is transported as input, not echoed into reports by default.

---

## 2. Files Changed

Implementation commit:

```text
1053e57 feat: deliver blk-pipe l2 packet to engine stdin
 internal/contracts/payload.go      | 10 +++++--
 internal/contracts/payload_test.go | 58 ++++++++++++++++++++++++++++++++++++++
 internal/engine/runner.go          | 10 ++++++-
 internal/engine/runner_test.go     | 20 +++++++++++++
 internal/execguard/command.go      |  5 ++++
 internal/execguard/command_test.go | 25 ++++++++++++++++
 internal/pipe/run.go               |  2 +-
 internal/pipe/run_test.go          | 36 +++++++++++++++++++++++
 python/blk_pipe_adapter.py         |  1 +
 python/test_blk_pipe_adapter.py    | 21 ++++++++++++++
 10 files changed, 184 insertions(+), 4 deletions(-)
```

Changed files:

- `internal/contracts/payload.go`
- `internal/contracts/payload_test.go`
- `internal/execguard/command.go`
- `internal/execguard/command_test.go`
- `internal/engine/runner.go`
- `internal/engine/runner_test.go`
- `internal/pipe/run.go`
- `internal/pipe/run_test.go`
- `python/blk_pipe_adapter.py`
- `python/test_blk_pipe_adapter.py`

---

## 3. Behavior Implemented

### 3.1 Payload preservation and bounds

`contracts.Payload` now includes `L2Packet`. V47 `l2_packet` is preserved during decode and normalized into the internal payload.

A maximum packet size is enforced through `DefaultMaxL2PacketBytes = 1048576`. Oversized packets are rejected during payload validation before engine start. Error strings do not echo packet content.

### 3.2 Stdin transport

`execguard.Options` now supports stdin bytes. `engine.Run` forwards optional stdin to `execguard.Run`, and `pipe.Run` passes `payload.L2Packet` into the engine as stdin.

Legacy Sprint 001 payloads continue to work with empty stdin.

### 3.3 Python adapter preservation

The Python adapter continues to accept `l2_packet` and now has test coverage proving the serialized payload includes the packet intact.

---

## 4. TDD Evidence

### 4.1 RED

The implementation subagent added failing tests first. Initial RED behavior included:

```text
TestPayloadDecodePreservesL2Packet: payload.L2Packet was empty
TestPayloadDecodeRejectsOversizedL2Packet: oversized packet was accepted
TestRunWritesConfiguredStdinToCommand: execguard had no stdin support
TestRunPassesStdinToEngine: engine.Run did not forward stdin
TestRunV47L2PacketDeliveredToEngineStdin: committed packet content was empty
Python adapter l2_packet serialization test: needed explicit coverage
```

### 4.2 GREEN

Final focused verification passed:

```text
go test ./internal/contracts -run 'TestPayloadDecode.*L2|TestPayloadDecodeV47|TestPayloadDecodeRejectsOversizedL2Packet' -v
PASS

go test ./internal/execguard -run 'TestRunWritesConfiguredStdin|TestRun.*Timeout|TestRun.*OutputFlood' -v
PASS

go test ./internal/engine -run 'TestRunPassesStdin|TestRun' -v
PASS

go test ./internal/pipe -run 'TestRunV47L2Packet|TestRunSuccess' -v
PASS

python3 -m unittest discover -s python -p 'test_*.py'
PASS

go test ./...
PASS

go vet ./...
PASS

git diff --check
PASS
```

---

## 5. Review Results

Task 4 used the required two-stage review loop.

### 5.1 Spec-compliance review

Final result:

```text
PASS
```

The reviewer confirmed:

- `contracts.Payload` includes `L2Packet`,
- `DecodePayload` preserves `l2_packet`,
- oversized packets are rejected before engine start without echoing the packet body,
- `execguard`, `engine`, and `pipe` deliver stdin correctly,
- empty and legacy payload behavior remains compatible,
- Python adapter preserves `l2_packet`,
- required focused and full tests pass.

### 5.2 Code-quality / security review

Final result:

```text
APPROVED
```

The reviewer confirmed:

- packet body is passed via stdin rather than args or env,
- report schema does not add packet content,
- timeout/flood cleanup remains unaffected,
- Python temp payload cleanup remains intact,
- no blocking security or quality issues were found.

---

## 6. Final Verification Evidence

Controller verification before push:

```text
gofmt -l internal/contracts/payload.go internal/contracts/payload_test.go internal/execguard/command.go internal/execguard/command_test.go internal/engine/runner.go internal/engine/runner_test.go internal/pipe/run.go internal/pipe/run_test.go
# no output

go test ./internal/contracts -run 'TestPayloadDecode.*L2|TestPayloadDecodeV47|TestPayloadDecodeRejectsOversizedL2Packet' -v
PASS

go test ./internal/execguard -run 'TestRunWritesConfiguredStdin|TestRun.*Timeout|TestRun.*OutputFlood' -v
PASS

go test ./internal/engine -run 'TestRunPassesStdin|TestRun' -v
PASS

go test ./internal/pipe -run 'TestRunV47L2Packet|TestRunSuccess' -v
PASS

python3 -m unittest discover -s python -p 'test_*.py'
PASS

go test ./...
PASS

go vet ./...
PASS

git diff --check
PASS

git push origin main
origin/main updated to 1053e57
```

Post-push status:

```text
## main...origin/main
1053e57 (HEAD -> main, origin/main) feat: deliver blk-pipe l2 packet to engine stdin
```

---

## 7. Safety Invariants Preserved

- No production `git add .`.
- No production `git add -u`.
- No live Codex or live LLM integration.
- No offensive cyber behavior.
- Packet content is not logged into reports by default.
- Oversized packet input is rejected rather than truncated.
- Legacy payloads continue to work with empty stdin.

---

## 8. Deviations / Notes

`DefaultMaxL2PacketBytes` is currently 1 MiB. Future doctrine may tune this value, but the important security behavior is already established: packet input is bounded and rejected before engine start if oversized.

---

## 9. Next Task

Proceed to Sprint 002.2 Task 5: document cyber-usability guardrails, strict failure handling, host-secret limitations, and the fact that BLK-pipe is still not a complete sandbox.
