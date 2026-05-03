package engine

import (
	"context"
	"errors"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"testing"
	"time"
)

func engineScript(name string) string {
	return filepath.Join("..", "..", "testdata", "engines", name)
}

func TestRunSuccessScriptExitsZeroAndCapturesBoundedOutput(t *testing.T) {
	ctx := context.Background()

	result, err := Run(ctx, ".", []string{engineScript("success.sh")}, 1024)
	if err != nil {
		t.Fatalf("Run returned error: %v", err)
	}

	if result.ExitCode != 0 {
		t.Fatalf("ExitCode = %d, want 0", result.ExitCode)
	}
	if result.OutputBytes == 0 {
		t.Fatalf("OutputBytes = 0, want captured output to be counted")
	}
	output := string(result.Output)
	if !strings.Contains(output, "success stdout") || !strings.Contains(output, "success stderr") {
		t.Fatalf("Output = %q, want bounded stdout/stderr", output)
	}
	if result.TimedOut {
		t.Fatalf("TimedOut = true, want false")
	}
	if result.Flooded {
		t.Fatalf("Flooded = true, want false")
	}
}

func TestRunPassesStdinToEngine(t *testing.T) {
	const expectedPacket = "EXPECTED_PACKET\nfor engine stdin"
	tempDir := t.TempDir()

	result, err := Run(context.Background(), tempDir, []string{"sh", "-c", "cat > packet.txt"}, 1024, []byte(expectedPacket))
	if err != nil {
		t.Fatalf("Run returned error: %v", err)
	}
	if result.ExitCode != 0 {
		t.Fatalf("ExitCode = %d, want 0; output=%q", result.ExitCode, result.Output)
	}
	got, err := os.ReadFile(filepath.Join(tempDir, "packet.txt"))
	if err != nil {
		t.Fatalf("read packet.txt: %v", err)
	}
	if string(got) != expectedPacket {
		t.Fatalf("packet.txt = %q, want %q", string(got), expectedPacket)
	}
}

func TestRunFailScriptReportsNonZeroExitAndCapturesBoundedOutputWithoutInfrastructureError(t *testing.T) {
	ctx := context.Background()

	result, err := Run(ctx, ".", []string{engineScript("fail.sh")}, 1024)
	if err != nil {
		t.Fatalf("Run returned error for non-zero command exit: %v", err)
	}

	if result.ExitCode == 0 {
		t.Fatalf("ExitCode = 0, want non-zero")
	}
	if result.OutputBytes == 0 {
		t.Fatalf("OutputBytes = 0, want captured output to be counted")
	}
	output := string(result.Output)
	if !strings.Contains(output, "fail stdout") || !strings.Contains(output, "fail stderr") {
		t.Fatalf("Output = %q, want bounded stdout/stderr", output)
	}
	if result.TimedOut {
		t.Fatalf("TimedOut = true, want false")
	}
	if result.Flooded {
		t.Fatalf("Flooded = true, want false")
	}
}

func TestRunTimeoutKillsSleepingProcess(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
	defer cancel()

	start := time.Now()
	result, err := Run(ctx, ".", []string{"sh", "-c", "sleep 5"}, 1024)
	elapsed := time.Since(start)
	if err != nil {
		t.Fatalf("Run returned error for timeout: %v", err)
	}

	if !result.TimedOut {
		t.Fatalf("TimedOut = false, want true")
	}
	if result.Flooded {
		t.Fatalf("Flooded = true, want false")
	}
	if elapsed >= time.Second {
		t.Fatalf("Run took %s, want timeout to kill process promptly", elapsed)
	}
}

func TestRunOutputFloodKillsFloodScript(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()

	result, err := Run(ctx, ".", []string{engineScript("flood.sh")}, 4096)
	if err != nil {
		t.Fatalf("Run returned error for flooded command: %v", err)
	}

	if !result.Flooded {
		t.Fatalf("Flooded = false, want true")
	}
	if result.OutputBytes <= 4096 {
		t.Fatalf("OutputBytes = %d, want more than cap to prove cap was exceeded", result.OutputBytes)
	}
	if len(result.Output) > 4096 {
		t.Fatalf("retained Output length = %d, want <= cap", len(result.Output))
	}
	if result.TimedOut {
		t.Fatalf("TimedOut = true, want false")
	}
}

func TestRunDoesNotHangWhenChildInheritsOutputPipeAfterParentExit(t *testing.T) {
	pidFile := filepath.Join(t.TempDir(), "child.pid")
	t.Cleanup(func() {
		pidBytes, err := os.ReadFile(pidFile)
		if err == nil {
			_ = exec.Command("kill", "-KILL", strings.TrimSpace(string(pidBytes))).Run()
		}
	})

	ctx, cancel := context.WithTimeout(context.Background(), 200*time.Millisecond)
	defer cancel()

	type runResult struct {
		result Result
		err    error
	}
	done := make(chan runResult, 1)
	go func() {
		result, err := Run(ctx, ".", []string{"sh", "-c", "sleep 5 & echo $! > \"$1\"; exit 0", "sh", pidFile}, 4096)
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

func TestRunStartFailureIsInfrastructureError(t *testing.T) {
	ctx := context.Background()

	_, err := Run(ctx, ".", []string{filepath.Join(".", "does-not-exist")}, 1024)
	if err == nil {
		t.Fatalf("Run returned nil error for invalid command path")
	}
	var exitErr *exec.ExitError
	if errors.As(err, &exitErr) {
		t.Fatalf("Run returned process exit error for start failure: %v", err)
	}
}
