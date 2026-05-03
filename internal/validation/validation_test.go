package validation

import (
	"context"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestRunExecutesCommandsSequentiallyAndCapturesDeterministicLogs(t *testing.T) {
	workdir := t.TempDir()
	commands := []string{
		"printf one; printf 1 >> order.txt",
		"printf two; printf 2 >> order.txt",
		"printf three; printf 3 >> order.txt",
	}

	result, err := Run(context.Background(), workdir, commands, 4096)
	if err != nil {
		t.Fatalf("Run() error = %v, want nil", err)
	}

	if result.HasFailure {
		t.Fatalf("HasFailure = true, want false; result=%+v", result)
	}
	if got := readFile(t, filepath.Join(workdir, "order.txt")); got != "123" {
		t.Fatalf("execution order file = %q, want 123", got)
	}
	assertValidationLogs(t, result.Logs, map[string]string{
		"validation_001": "one",
		"validation_002": "two",
		"validation_003": "three",
	})
}

func TestRunRunsAllCommandsAndRecordsFailingOutput(t *testing.T) {
	workdir := t.TempDir()
	commands := []string{
		"printf before; exit 7",
		"printf after; printf ran > after.txt",
	}

	result, err := Run(context.Background(), workdir, commands, 4096)
	if err != nil {
		t.Fatalf("Run() error = %v, want nil", err)
	}

	if !result.HasFailure {
		t.Fatalf("HasFailure = false, want true; result=%+v", result)
	}
	if got := readFile(t, filepath.Join(workdir, "after.txt")); got != "ran" {
		t.Fatalf("second command did not run after failure, after.txt=%q", got)
	}
	if result.Outcomes["validation_001"].ExitCode != 7 {
		t.Fatalf("validation_001 exit code = %d, want 7", result.Outcomes["validation_001"].ExitCode)
	}
	assertValidationLogs(t, result.Logs, map[string]string{
		"validation_001": "before",
		"validation_002": "after",
	})
}

func TestRunRetainsAggregateLogsWithinMaxOutputBytesAndStillRunsAllCommands(t *testing.T) {
	workdir := t.TempDir()
	commands := []string{
		"printf abcd; printf 1 >> order.txt",
		"printf efgh; printf 2 >> order.txt",
		"printf ijkl; printf 3 >> order.txt; exit 7",
		"printf mnop; printf 4 >> order.txt",
	}

	result, err := Run(context.Background(), workdir, commands, 5)
	if err != nil {
		t.Fatalf("Run() error = %v, want nil", err)
	}

	if !result.HasFailure {
		t.Fatalf("HasFailure = false, want true from validation_003 exit; result=%+v", result)
	}
	if got := readFile(t, filepath.Join(workdir, "order.txt")); got != "1234" {
		t.Fatalf("execution order file = %q, want 1234", got)
	}
	if result.Outcomes["validation_003"].ExitCode != 7 {
		t.Fatalf("validation_003 exit code = %d, want 7", result.Outcomes["validation_003"].ExitCode)
	}
	assertValidationLogs(t, result.Logs, map[string]string{
		"validation_001": "abcd",
		"validation_002": "e",
		"validation_003": "",
		"validation_004": "",
	})
	if got := totalValidationLogBytes(result.Logs); got > 5 {
		t.Fatalf("aggregate retained validation log bytes = %d, want <= 5; logs=%v", got, result.Logs)
	}
}

func TestRunScrubsInheritedDangerousEnvironment(t *testing.T) {
	t.Setenv("GIT_DIR", "/tmp/evil-git-dir")
	t.Setenv("GIT_INDEX_FILE", "/tmp/evil-index")
	t.Setenv("SSH_AUTH_SOCK", "/tmp/agent.sock")
	t.Setenv("SSH_AGENT_PID", "12345")
	t.Setenv("SSH_ASKPASS", "/tmp/askpass")
	workdir := t.TempDir()

	result, err := Run(context.Background(), workdir, []string{"env > env.txt"}, 4096)
	if err != nil {
		t.Fatalf("Run() error = %v, want nil", err)
	}
	if result.HasFailure {
		t.Fatalf("HasFailure = true, want false; result=%+v", result)
	}

	env := readFile(t, filepath.Join(workdir, "env.txt"))
	for _, forbidden := range []string{
		"GIT_DIR=",
		"GIT_INDEX_FILE=",
		"SSH_AUTH_SOCK=",
		"SSH_AGENT_PID=",
		"SSH_ASKPASS=",
	} {
		if strings.Contains(env, forbidden) {
			t.Fatalf("env contains forbidden %q in:\n%s", forbidden, env)
		}
	}
	if !strings.Contains(env, "PWD="+workdir+"\n") {
		t.Fatalf("env missing deterministic PWD=%q in:\n%s", workdir, env)
	}
}

func readFile(t *testing.T, path string) string {
	t.Helper()
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("read %q: %v", path, err)
	}
	return string(data)
}

func assertValidationLogs(t *testing.T, got map[string]string, want map[string]string) {
	t.Helper()
	if len(got) != len(want) {
		t.Fatalf("logs length = %d (%v), want %d (%v)", len(got), got, len(want), want)
	}
	for key, wantValue := range want {
		if got[key] != wantValue {
			t.Fatalf("logs[%q] = %q, want %q; all logs=%v", key, got[key], wantValue, got)
		}
	}
}

func totalValidationLogBytes(logs map[string]string) int {
	total := 0
	for _, log := range logs {
		total += len(log)
	}
	return total
}
