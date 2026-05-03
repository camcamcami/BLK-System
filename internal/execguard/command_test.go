//go:build linux || darwin

package execguard

import (
	"context"
	"errors"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"sync/atomic"
	"syscall"
	"testing"
	"time"
)

func TestScrubbedEnvRemovesInheritedGitAndSSHKeys(t *testing.T) {
	t.Setenv("GIT_DIR", "/tmp/evil-git-dir")
	t.Setenv("GIT_CONFIG_GLOBAL", "/tmp/evil-gitconfig")
	t.Setenv("GIT_SSH_COMMAND", "ssh -i /tmp/evil-key")
	t.Setenv("SSH_AUTH_SOCK", "/tmp/agent.sock")
	t.Setenv("SSH_AGENT_PID", "12345")
	t.Setenv("SSH_ASKPASS", "/tmp/askpass")
	t.Setenv("PWD", "/tmp/inherited-pwd")
	t.Setenv("BLK_KEEP_ME", "kept")

	env := ScrubbedEnv("/safe/workdir", "EXTRA_ONE=1", "GIT_SSH_COMMAND=ssh -F /dev/null")

	if got := envValue(t, env, "BLK_KEEP_ME"); got != "kept" {
		t.Fatalf("BLK_KEEP_ME = %q, want kept", got)
	}
	for _, key := range []string{"GIT_DIR", "SSH_AUTH_SOCK", "SSH_AGENT_PID", "SSH_ASKPASS"} {
		if envHasKey(env, key) {
			t.Fatalf("ScrubbedEnv retained inherited %s in %v", key, env)
		}
	}
	if got := envValue(t, env, "GIT_CONFIG_GLOBAL"); got != os.DevNull {
		t.Fatalf("GIT_CONFIG_GLOBAL = %q, want %q", got, os.DevNull)
	}
	if got := envValue(t, env, "GIT_CONFIG_NOSYSTEM"); got != "1" {
		t.Fatalf("GIT_CONFIG_NOSYSTEM = %q, want 1", got)
	}
	if got := envValue(t, env, "PWD"); got != "/safe/workdir" {
		t.Fatalf("PWD = %q, want deterministic workdir", got)
	}
	if count := envKeyCount(env, "PWD"); count != 1 {
		t.Fatalf("PWD appears %d times in %v, want exactly once", count, env)
	}
	if got := env[len(env)-2:]; got[0] != "EXTRA_ONE=1" || got[1] != "GIT_SSH_COMMAND=ssh -F /dev/null" {
		t.Fatalf("extra env entries not preserved/appended at end: tail=%v env=%v", got, env)
	}
}

func TestRunSuccessCapturesBoundedCombinedOutput(t *testing.T) {
	result, err := Run(context.Background(), Options{
		Workdir:        ".",
		Command:        []string{"sh", "-c", "printf out; printf err >&2"},
		MaxOutputBytes: 1024,
	})
	if err != nil {
		t.Fatalf("Run returned error: %v", err)
	}
	if result.ExitCode != 0 {
		t.Fatalf("ExitCode = %d, want 0", result.ExitCode)
	}
	if got := string(result.Output); got != "outerr" {
		t.Fatalf("Output = %q, want combined stdout/stderr", got)
	}
	if result.OutputBytes != int64(len("outerr")) {
		t.Fatalf("OutputBytes = %d, want %d", result.OutputBytes, len("outerr"))
	}
	if result.TimedOut || result.Flooded {
		t.Fatalf("unexpected timeout/flood flags: %+v", result)
	}
}

func TestRunNonZeroExitReturnsExitCodeAndBoundedOutputWithoutInfrastructureError(t *testing.T) {
	result, err := Run(context.Background(), Options{
		Workdir:        ".",
		Command:        []string{"sh", "-c", "printf failure; exit 42"},
		MaxOutputBytes: 1024,
	})
	if err != nil {
		t.Fatalf("Run returned error for non-zero command exit: %v", err)
	}
	if result.ExitCode != 42 {
		t.Fatalf("ExitCode = %d, want 42", result.ExitCode)
	}
	if got := string(result.Output); got != "failure" {
		t.Fatalf("Output = %q, want failure", got)
	}
	if result.OutputBytes != int64(len("failure")) {
		t.Fatalf("OutputBytes = %d, want %d", result.OutputBytes, len("failure"))
	}
	if result.TimedOut || result.Flooded {
		t.Fatalf("unexpected timeout/flood flags: %+v", result)
	}
}

func TestRunTimeoutKillsProcessGroupPromptly(t *testing.T) {
	start := time.Now()
	result, err := Run(context.Background(), Options{
		Workdir:        ".",
		Command:        []string{"sh", "-c", "sleep 5"},
		Timeout:        50 * time.Millisecond,
		MaxOutputBytes: 1024,
	})
	elapsed := time.Since(start)
	if err != nil {
		t.Fatalf("Run returned error for timeout: %v", err)
	}
	if !result.TimedOut {
		t.Fatalf("TimedOut = false, want true; result=%+v", result)
	}
	if result.Flooded {
		t.Fatalf("Flooded = true, want false")
	}
	if elapsed >= time.Second {
		t.Fatalf("Run took %s, want prompt process-group kill", elapsed)
	}
}

func TestRunOutputFloodKillsProcessGroupAndKeepsOnlyBoundedOutput(t *testing.T) {
	result, err := Run(context.Background(), Options{
		Workdir:        ".",
		Command:        []string{"sh", "-c", "yes flood"},
		Timeout:        2 * time.Second,
		MaxOutputBytes: 4096,
	})
	if err != nil {
		t.Fatalf("Run returned error for flooded command: %v", err)
	}
	if !result.Flooded {
		t.Fatalf("Flooded = false, want true; result=%+v", result)
	}
	if result.OutputBytes <= 4096 {
		t.Fatalf("OutputBytes = %d, want more than cap to prove flood", result.OutputBytes)
	}
	if len(result.Output) > 4096 {
		t.Fatalf("retained output length = %d, want <= cap", len(result.Output))
	}
	if result.TimedOut {
		t.Fatalf("TimedOut = true, want false")
	}
}

func TestRunDoesNotHangWhenChildInheritsOutputPipeAfterParentExit(t *testing.T) {
	pidFile := filepath.Join(t.TempDir(), "child.pid")
	t.Cleanup(func() {
		killPIDFromFile(pidFile)
	})

	type runResult struct {
		result CommandResult
		err    error
	}
	done := make(chan runResult, 1)
	go func() {
		result, err := Run(context.Background(), Options{
			Workdir:        ".",
			Command:        []string{"sh", "-c", "sleep 5 & echo $! > \"$1\"; exit 0", "sh", pidFile},
			Timeout:        200 * time.Millisecond,
			MaxOutputBytes: 4096,
		})
		done <- runResult{result: result, err: err}
	}()

	select {
	case got := <-done:
		if got.err != nil {
			t.Fatalf("Run returned error: %v", got.err)
		}
		if got.result.ExitCode != 0 {
			t.Fatalf("ExitCode = %d, want 0", got.result.ExitCode)
		}
		if got.result.TimedOut {
			t.Fatalf("TimedOut = true, want false")
		}
		if got.result.Flooded {
			t.Fatalf("Flooded = true, want false")
		}
	case <-time.After(time.Second):
		t.Fatalf("Run did not return after direct process exited while child held output pipe open")
	}
}

func TestRunContextCancellationBoundsEscapedDescendantHoldingOutputPipe(t *testing.T) {
	tempDir := t.TempDir()
	readyFile := filepath.Join(tempDir, "escaped-child.ready")
	markerFile := filepath.Join(tempDir, "escaped-child.mutated")
	pidFile := filepath.Join(tempDir, "escaped-child.pid")
	t.Cleanup(func() {
		killPIDFromFile(pidFile)
	})

	start := time.Now()
	result, err := Run(context.Background(), Options{
		Workdir: ".",
		Command: []string{
			"sh", "-c",
			"EXECGUARD_HELPER_ESCAPED_PIPE_HOLDER=1 \"$1\" -test.run=TestHelperEscapedPipeHolder -- \"$2\" \"$3\" \"$4\" & i=0; while [ ! -s \"$2\" ] && [ \"$i\" -lt 100 ]; do i=$((i+1)); sleep 0.01; done; [ -s \"$2\" ] || exit 2; exit 0",
			"sh", os.Args[0], readyFile, markerFile, pidFile,
		},
		Timeout:        100 * time.Millisecond,
		MaxOutputBytes: 4096,
	})
	elapsed := time.Since(start)
	if err != nil {
		t.Fatalf("Run returned error: %v", err)
	}
	if result.ExitCode != 0 {
		t.Fatalf("ExitCode = %d, want 0", result.ExitCode)
	}
	if !result.TimedOut {
		t.Fatalf("TimedOut = false, want true after context timed out while draining escaped descendant output")
	}
	if result.Flooded {
		t.Fatalf("Flooded = true, want false")
	}
	if elapsed >= time.Second {
		t.Fatalf("Run took %s, want context timeout to bound output drain", elapsed)
	}
}

func TestRunWaitsForEscapedDescendantToCloseInheritedOutputPipeBeforeReturning(t *testing.T) {
	tempDir := t.TempDir()
	readyFile := filepath.Join(tempDir, "escaped-child.ready")
	markerFile := filepath.Join(tempDir, "escaped-child.mutated")
	pidFile := filepath.Join(tempDir, "escaped-child.pid")
	t.Cleanup(func() {
		killPIDFromFile(pidFile)
	})

	type runResult struct {
		result CommandResult
		err    error
	}
	done := make(chan runResult, 1)
	start := time.Now()
	go func() {
		result, err := Run(context.Background(), Options{
			Workdir: ".",
			Command: []string{
				"sh", "-c",
				"EXECGUARD_HELPER_ESCAPED_PIPE_HOLDER=1 \"$1\" -test.run=TestHelperEscapedPipeHolder -- \"$2\" \"$3\" \"$4\" & i=0; while [ ! -s \"$2\" ] && [ \"$i\" -lt 100 ]; do i=$((i+1)); sleep 0.01; done; [ -s \"$2\" ] || exit 2; exit 0",
				"sh", os.Args[0], readyFile, markerFile, pidFile,
			},
			MaxOutputBytes: 4096,
		})
		done <- runResult{result: result, err: err}
	}()

	var got runResult
	select {
	case got = <-done:
	case <-time.After(2 * time.Second):
		killPIDFromFile(pidFile)
		t.Fatalf("Run did not return after escaped descendant had enough time to close inherited output pipe")
	}

	elapsed := time.Since(start)
	if got.err != nil {
		t.Fatalf("Run returned error: %v", got.err)
	}
	if got.result.ExitCode != 0 {
		t.Fatalf("ExitCode = %d, want 0", got.result.ExitCode)
	}
	if got.result.TimedOut {
		t.Fatalf("TimedOut = true, want false")
	}
	if got.result.Flooded {
		t.Fatalf("Flooded = true, want false")
	}
	if _, err := os.Stat(markerFile); err != nil {
		t.Fatalf("Run returned before escaped descendant closed inherited output and wrote marker after %s: %v", elapsed, err)
	}
}

func TestKillActiveProcessGroupsKillsRunningCommand(t *testing.T) {
	tempDir := t.TempDir()
	pidFile := filepath.Join(tempDir, "active.pid")

	type runResult struct {
		result CommandResult
		err    error
	}
	done := make(chan runResult, 1)
	go func() {
		result, err := Run(context.Background(), Options{
			Workdir: ".",
			Command: []string{
				"sh", "-c",
				"echo $$ > \"$1\"; sleep 30",
				"sh", pidFile,
			},
			MaxOutputBytes: 1024,
		})
		done <- runResult{result: result, err: err}
	}()

	pid := waitForPIDFile(t, pidFile)
	t.Cleanup(func() {
		_ = syscall.Kill(-pid, syscall.SIGKILL)
		_ = syscall.Kill(pid, syscall.SIGKILL)
	})

	killed, err := KillActiveProcessGroups()
	if err != nil {
		t.Fatalf("KillActiveProcessGroups returned error: %v", err)
	}
	if killed < 1 {
		t.Fatalf("KillActiveProcessGroups killed %d groups, want at least 1", killed)
	}

	select {
	case got := <-done:
		if got.err != nil {
			t.Fatalf("Run returned infrastructure error after active kill: %v", got.err)
		}
		if got.result.ExitCode == 0 {
			t.Fatalf("ExitCode = 0, want non-zero after active process group kill")
		}
	case <-time.After(2 * time.Second):
		t.Fatalf("Run did not return after active process group kill")
	}

	assertProcessGone(t, pid)
}

func TestKillActiveProcessGroupsKillsEscapedDescendant(t *testing.T) {
	tempDir := t.TempDir()
	rootPIDFile := filepath.Join(tempDir, "root.pid")
	escapedPIDFile := filepath.Join(tempDir, "escaped.pid")
	readyFile := filepath.Join(tempDir, "escaped.ready")
	t.Cleanup(func() {
		killPIDFromFile(escapedPIDFile)
		killPIDFromFile(rootPIDFile)
	})

	type runResult struct {
		result CommandResult
		err    error
	}
	done := make(chan runResult, 1)
	go func() {
		result, err := Run(context.Background(), Options{
			Workdir: ".",
			Command: []string{
				"sh", "-c",
				"echo $$ > \"$2\"; EXECGUARD_HELPER_ESCAPED_SLEEPER=1 \"$1\" -test.run=TestHelperEscapedSleeper -- \"$3\" \"$4\" & i=0; while [ ! -s \"$4\" ] && [ \"$i\" -lt 100 ]; do i=$((i+1)); sleep 0.01; done; sleep 30",
				"sh", os.Args[0], rootPIDFile, escapedPIDFile, readyFile,
			},
			MaxOutputBytes: 1024,
		})
		done <- runResult{result: result, err: err}
	}()

	escapedPID := waitForPIDFile(t, escapedPIDFile)
	killed, err := KillActiveProcessGroups()
	if err != nil {
		t.Fatalf("KillActiveProcessGroups returned error: %v", err)
	}
	if killed < 1 {
		t.Fatalf("KillActiveProcessGroups killed %d targets, want at least 1", killed)
	}

	select {
	case got := <-done:
		if got.err != nil {
			t.Fatalf("Run returned infrastructure error after active kill: %v", got.err)
		}
	case <-time.After(2 * time.Second):
		t.Fatalf("Run did not return after active kill of escaped descendant")
	}
	assertProcessGone(t, escapedPID)
}

func TestActiveRegistryAllowsRepeatedRootPIDUntilEachRunUnregisters(t *testing.T) {
	const reusedRootPID = 424242
	_, unregisterFirst := registerActiveProcessGroup(reusedRootPID, "pipe:[first]")
	t.Cleanup(unregisterFirst)
	_, unregisterSecond := registerActiveProcessGroup(reusedRootPID, "pipe:[second]")
	t.Cleanup(unregisterSecond)

	commands := activeCommandSnapshot()
	seenFirst := false
	seenSecond := false
	for _, command := range commands {
		if command.rootPID != reusedRootPID {
			continue
		}
		switch command.pipeID {
		case "pipe:[first]":
			seenFirst = true
		case "pipe:[second]":
			seenSecond = true
		}
	}
	if !seenFirst || !seenSecond {
		t.Fatalf("active registry for repeated root PID captured first=%t second=%t in snapshot %#v, want both runs registered independently", seenFirst, seenSecond, commands)
	}
}

func TestActiveCleanupTargetsIgnoreReapedDirectPIDAndKeepPipeHolder(t *testing.T) {
	const (
		rootPID       = 101
		rootPGID      = 202
		descendantPID = 303
		pipeHolderPID = 404
		ownPID        = 505
	)
	commands := []activeCommand{{
		rootPID:    rootPID,
		pgid:       rootPGID,
		pipeID:     "pipe:[stale-direct]",
		directLive: false,
		done:       make(chan struct{}),
	}}
	processes := map[int]processInfo{
		descendantPID: {pid: descendantPID, ppid: rootPID, pgid: rootPGID},
		pipeHolderPID: {pid: pipeHolderPID, ppid: 1, pgid: 606},
	}

	targets := activeCleanupTargets(commands, processes, func(pipeID string) []int {
		if pipeID != "pipe:[stale-direct]" {
			t.Fatalf("pipeHolders called with %q, want registered pipe ID", pipeID)
		}
		return []int{pipeHolderPID, ownPID}
	}, ownPID)

	if _, ok := targets.pids[rootPID]; ok {
		t.Fatalf("cleanup targets included reaped root PID %d in %#v", rootPID, targets.pids)
	}
	if _, ok := targets.groups[rootPGID]; ok {
		t.Fatalf("cleanup targets included stale root PGID %d in %#v", rootPGID, targets.groups)
	}
	if _, ok := targets.pids[descendantPID]; ok {
		t.Fatalf("cleanup targets included descendant traversal from reaped root PID %d in %#v", descendantPID, targets.pids)
	}
	if _, ok := targets.pids[pipeHolderPID]; !ok {
		t.Fatalf("cleanup targets omitted pipe holder PID %d in %#v", pipeHolderPID, targets.pids)
	}
	if _, ok := targets.pids[ownPID]; ok {
		t.Fatalf("cleanup targets included own PID %d in %#v", ownPID, targets.pids)
	}
}

func TestActiveCleanupTargetsIncludePipeHolderDescendantsAfterDirectReaped(t *testing.T) {
	const (
		rootPID             = 111
		rootPGID            = 222
		staleRootChildPID   = 333
		pipeHolderPID       = 444
		pipeHolderPGID      = 555
		pipeHolderChildPID  = 666
		pipeHolderChildPGID = 777
		grandchildPID       = 888
		grandchildPGID      = 999
		ownPID              = 1001
	)
	commands := []activeCommand{{
		rootPID:    rootPID,
		pgid:       rootPGID,
		pipeID:     "pipe:[held-output]",
		directLive: false,
		done:       make(chan struct{}),
	}}
	processes := map[int]processInfo{
		staleRootChildPID:  {pid: staleRootChildPID, ppid: rootPID, pgid: rootPGID},
		pipeHolderPID:      {pid: pipeHolderPID, ppid: 1, pgid: pipeHolderPGID},
		pipeHolderChildPID: {pid: pipeHolderChildPID, ppid: pipeHolderPID, pgid: pipeHolderChildPGID},
		grandchildPID:      {pid: grandchildPID, ppid: pipeHolderChildPID, pgid: grandchildPGID},
		ownPID:             {pid: ownPID, ppid: pipeHolderPID, pgid: 1002},
	}

	targets := activeCleanupTargets(commands, processes, func(pipeID string) []int {
		if pipeID != "pipe:[held-output]" {
			t.Fatalf("pipeHolders called with %q, want registered pipe ID", pipeID)
		}
		return []int{pipeHolderPID}
	}, ownPID)

	for _, pid := range []int{pipeHolderPID, pipeHolderChildPID, grandchildPID} {
		if _, ok := targets.pids[pid]; !ok {
			t.Fatalf("cleanup targets omitted pipe-holder descendant PID %d in %#v", pid, targets.pids)
		}
	}
	for _, pgid := range []int{pipeHolderPGID, pipeHolderChildPGID, grandchildPGID} {
		if _, ok := targets.groups[pgid]; !ok {
			t.Fatalf("cleanup targets omitted pipe-holder descendant PGID %d in %#v", pgid, targets.groups)
		}
	}
	if _, ok := targets.pids[rootPID]; ok {
		t.Fatalf("cleanup targets included reaped root PID %d in %#v", rootPID, targets.pids)
	}
	if _, ok := targets.groups[rootPGID]; ok {
		t.Fatalf("cleanup targets included stale root PGID %d in %#v", rootPGID, targets.groups)
	}
	if _, ok := targets.pids[staleRootChildPID]; ok {
		t.Fatalf("cleanup targets traversed from reaped root PID %d in %#v", staleRootChildPID, targets.pids)
	}
	if _, ok := targets.pids[ownPID]; ok {
		t.Fatalf("cleanup targets included own PID %d in %#v", ownPID, targets.pids)
	}
}

func TestActiveCleanupTargetsDoNotTraverseOwnPipeHolderDescendantsAfterDirectReaped(t *testing.T) {
	const (
		rootPID                 = 121
		rootPGID                = 232
		staleRootChildPID       = 343
		ownPID                  = 454
		ownChildPID             = 565
		ownGrandchildPID        = 676
		pipeHolderPID           = 787
		pipeHolderPGID          = 898
		pipeHolderChildPID      = 909
		pipeHolderChildPGID     = 1010
		pipeHolderGrandchildPID = 1111
		pipeHolderGrandPGID     = 1212
	)
	commands := []activeCommand{{
		rootPID:    rootPID,
		pgid:       rootPGID,
		pipeID:     "pipe:[own-and-external-holder]",
		directLive: false,
		done:       make(chan struct{}),
	}}
	processes := map[int]processInfo{
		staleRootChildPID:       {pid: staleRootChildPID, ppid: rootPID, pgid: rootPGID},
		ownPID:                  {pid: ownPID, ppid: 1, pgid: 455},
		ownChildPID:             {pid: ownChildPID, ppid: ownPID, pgid: 566},
		ownGrandchildPID:        {pid: ownGrandchildPID, ppid: ownChildPID, pgid: 677},
		pipeHolderPID:           {pid: pipeHolderPID, ppid: 1, pgid: pipeHolderPGID},
		pipeHolderChildPID:      {pid: pipeHolderChildPID, ppid: pipeHolderPID, pgid: pipeHolderChildPGID},
		pipeHolderGrandchildPID: {pid: pipeHolderGrandchildPID, ppid: pipeHolderChildPID, pgid: pipeHolderGrandPGID},
	}

	targets := activeCleanupTargets(commands, processes, func(pipeID string) []int {
		if pipeID != "pipe:[own-and-external-holder]" {
			t.Fatalf("pipeHolders called with %q, want registered pipe ID", pipeID)
		}
		return []int{ownPID, pipeHolderPID}
	}, ownPID)

	for _, pid := range []int{pipeHolderPID, pipeHolderChildPID, pipeHolderGrandchildPID} {
		if _, ok := targets.pids[pid]; !ok {
			t.Fatalf("cleanup targets omitted external pipe-holder PID/descendant %d in %#v", pid, targets.pids)
		}
	}
	for _, pgid := range []int{pipeHolderPGID, pipeHolderChildPGID, pipeHolderGrandPGID} {
		if _, ok := targets.groups[pgid]; !ok {
			t.Fatalf("cleanup targets omitted external pipe-holder PGID/descendant PGID %d in %#v", pgid, targets.groups)
		}
	}
	for _, pid := range []int{ownPID, ownChildPID, ownGrandchildPID, rootPID, staleRootChildPID} {
		if _, ok := targets.pids[pid]; ok {
			t.Fatalf("cleanup targets included excluded PID %d in %#v", pid, targets.pids)
		}
	}
	for _, pgid := range []int{rootPGID, 455, 566, 677} {
		if _, ok := targets.groups[pgid]; ok {
			t.Fatalf("cleanup targets included excluded PGID %d in %#v", pgid, targets.groups)
		}
	}
}

func TestRegisterActiveProcessGroupMarksDirectProcessReapedButKeepsRegisteredPipe(t *testing.T) {
	const rootPID = 515151
	markDirectProcessReaped, unregister := registerActiveProcessGroup(rootPID, "pipe:[mark-reaped]")
	t.Cleanup(unregister)

	markDirectProcessReaped()
	commands := activeCommandSnapshot()
	for _, command := range commands {
		if command.rootPID != rootPID || command.pipeID != "pipe:[mark-reaped]" {
			continue
		}
		if command.directLive {
			t.Fatalf("directLive = true after markDirectProcessReaped for snapshot %#v", commands)
		}
		return
	}
	t.Fatalf("marked active command root PID %d pipeID %q missing from snapshot %#v", rootPID, "pipe:[mark-reaped]", commands)
}

func TestReapIfCanceledAfterRegistrationReapsCanceledContext(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	var calls atomic.Int32

	reapIfCanceledAfterRegistration(ctx, func() (int, error) {
		calls.Add(1)
		return 0, nil
	})

	if calls.Load() != 1 {
		t.Fatalf("reap calls = %d, want 1 for canceled context after active registration", calls.Load())
	}
}

func TestReapIfCanceledAfterRegistrationSkipsLiveContext(t *testing.T) {
	var calls atomic.Int32

	reapIfCanceledAfterRegistration(context.Background(), func() (int, error) {
		calls.Add(1)
		return 0, nil
	})

	if calls.Load() != 0 {
		t.Fatalf("reap calls = %d, want 0 for live context", calls.Load())
	}
}

func TestRegistryStaysActiveWhileEscapedDescendantHoldsOutputPipe(t *testing.T) {
	tempDir := t.TempDir()
	escapedPIDFile := filepath.Join(tempDir, "escaped.pid")
	readyFile := filepath.Join(tempDir, "escaped.ready")
	t.Cleanup(func() {
		killPIDFromFile(escapedPIDFile)
	})

	type runResult struct {
		result CommandResult
		err    error
	}
	done := make(chan runResult, 1)
	go func() {
		result, err := Run(context.Background(), Options{
			Workdir: ".",
			Command: []string{
				"sh", "-c",
				"EXECGUARD_HELPER_ESCAPED_SLEEPER=1 \"$1\" -test.run=TestHelperEscapedSleeper -- \"$2\" \"$3\" & i=0; while [ ! -s \"$3\" ] && [ \"$i\" -lt 100 ]; do i=$((i+1)); sleep 0.01; done; [ -s \"$3\" ] || exit 2; exit 0",
				"sh", os.Args[0], escapedPIDFile, readyFile,
			},
			MaxOutputBytes: 1024,
		})
		done <- runResult{result: result, err: err}
	}()

	escapedPID := waitForPIDFile(t, escapedPIDFile)
	killed, err := KillActiveProcessGroups()
	if err != nil {
		t.Fatalf("KillActiveProcessGroups returned error: %v", err)
	}
	if killed < 1 {
		t.Fatalf("KillActiveProcessGroups killed %d targets, want registry to stay active until output drain", killed)
	}

	select {
	case got := <-done:
		if got.err != nil {
			t.Fatalf("Run returned infrastructure error after active kill: %v", got.err)
		}
	case <-time.After(2 * time.Second):
		t.Fatalf("Run did not return after escaped pipe holder was killed")
	}
	assertProcessGone(t, escapedPID)
}

func TestHelperEscapedPipeHolder(t *testing.T) {
	if os.Getenv("EXECGUARD_HELPER_ESCAPED_PIPE_HOLDER") != "1" {
		return
	}
	if len(os.Args) < 6 {
		os.Exit(2)
	}
	readyFile := os.Args[len(os.Args)-3]
	markerFile := os.Args[len(os.Args)-2]
	pidFile := os.Args[len(os.Args)-1]
	if _, err := syscall.Setsid(); err != nil {
		os.Exit(3)
	}
	if err := os.WriteFile(pidFile, []byte(fmt.Sprintf("%d", os.Getpid())), 0o600); err != nil {
		os.Exit(4)
	}
	if err := os.WriteFile(readyFile, []byte("ready"), 0o600); err != nil {
		os.Exit(5)
	}
	time.Sleep(700 * time.Millisecond)
	if err := os.WriteFile(markerFile, []byte("mutated"), 0o600); err != nil {
		os.Exit(6)
	}
	os.Exit(0)
}

func TestHelperEscapedSleeper(t *testing.T) {
	if os.Getenv("EXECGUARD_HELPER_ESCAPED_SLEEPER") != "1" {
		return
	}
	if len(os.Args) < 5 {
		os.Exit(2)
	}
	pidFile := os.Args[len(os.Args)-2]
	readyFile := os.Args[len(os.Args)-1]
	if _, err := syscall.Setsid(); err != nil {
		os.Exit(3)
	}
	if err := os.WriteFile(pidFile, []byte(fmt.Sprintf("%d", os.Getpid())), 0o600); err != nil {
		os.Exit(4)
	}
	if err := os.WriteFile(readyFile, []byte("ready"), 0o600); err != nil {
		os.Exit(5)
	}
	time.Sleep(30 * time.Second)
	os.Exit(0)
}

func killPIDFromFile(pidFile string) {
	pidBytes, err := os.ReadFile(pidFile)
	if err == nil {
		_ = exec.Command("kill", "-KILL", strings.TrimSpace(string(pidBytes))).Run()
	}
}

func waitForPIDFile(t *testing.T, pidFile string) int {
	t.Helper()
	deadline := time.Now().Add(time.Second)
	for time.Now().Before(deadline) {
		pidBytes, err := os.ReadFile(pidFile)
		if err == nil && strings.TrimSpace(string(pidBytes)) != "" {
			var pid int
			if _, scanErr := fmt.Sscanf(strings.TrimSpace(string(pidBytes)), "%d", &pid); scanErr != nil {
				t.Fatalf("parse pid file %q: %v", string(pidBytes), scanErr)
			}
			return pid
		}
		time.Sleep(10 * time.Millisecond)
	}
	t.Fatalf("pid file %s was not created", pidFile)
	return 0
}

func assertProcessGone(t *testing.T, pid int) {
	t.Helper()
	deadline := time.Now().Add(time.Second)
	for time.Now().Before(deadline) {
		err := syscall.Kill(pid, 0)
		if errors.Is(err, syscall.ESRCH) {
			return
		}
		time.Sleep(10 * time.Millisecond)
	}
	t.Fatalf("process %d still exists after active process group kill", pid)
}

func TestRunStartFailureIsInfrastructureError(t *testing.T) {
	_, err := Run(context.Background(), Options{
		Workdir:        ".",
		Command:        []string{filepath.Join(".", "does-not-exist")},
		MaxOutputBytes: 1024,
	})
	if err == nil {
		t.Fatalf("Run returned nil error for invalid command path")
	}
	var exitErr *exec.ExitError
	if errors.As(err, &exitErr) {
		t.Fatalf("Run returned process exit error for start failure: %v", err)
	}
}

func envValue(t *testing.T, env []string, key string) string {
	t.Helper()
	prefix := key + "="
	for i := len(env) - 1; i >= 0; i-- {
		if strings.HasPrefix(env[i], prefix) {
			return strings.TrimPrefix(env[i], prefix)
		}
	}
	t.Fatalf("env missing key %q in %v", key, env)
	return ""
}

func envHasKey(env []string, key string) bool {
	return envKeyCount(env, key) > 0
}

func envKeyCount(env []string, key string) int {
	prefix := key + "="
	count := 0
	for _, entry := range env {
		if strings.HasPrefix(entry, prefix) {
			count++
		}
	}
	return count
}
