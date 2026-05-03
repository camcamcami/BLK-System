package execguard

import (
	"context"
	"errors"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
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

func killPIDFromFile(pidFile string) {
	pidBytes, err := os.ReadFile(pidFile)
	if err == nil {
		_ = exec.Command("kill", "-KILL", strings.TrimSpace(string(pidBytes))).Run()
	}
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
