package pipe

import (
	"bytes"
	"context"
	"encoding/json"
	"io"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"syscall"
	"testing"

	"github.com/camcamcami/BLK-System/internal/contracts"
	"github.com/camcamcami/BLK-System/internal/testutil"
)

func TestRunSuccessCommitsAllowedModification(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	testutil.WriteFile(t, repo, "src/allowed.txt", "before\n")
	testutil.RunGit(t, repo, "add", "--", "src/allowed.txt")
	testutil.RunGit(t, repo, "commit", "-m", "add allowed file")
	beforeHead := git(t, repo, "rev-parse", "HEAD")

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf 'after\\n' > src/allowed.txt"},
		AllowedModifiedFiles: []string{"src/allowed.txt"},
		TimeoutSeconds:       5,
		MaxOutputBytes:       4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitSuccess {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitSuccess, report)
	}
	if report.Status != "SUCCESS" {
		t.Fatalf("report status = %q, want SUCCESS", report.Status)
	}
	if report.Action != "execute" || report.Workdir != repo {
		t.Fatalf("unexpected action/workdir in report: %+v", report)
	}
	if report.EngineExitCode != 0 || report.EngineOutputBytes != 0 || report.Error != "" {
		t.Fatalf("unexpected engine/error fields: %+v", report)
	}
	if report.CommitHash == "" || report.CommitHash == beforeHead {
		t.Fatalf("commit hash = %q, before HEAD = %q", report.CommitHash, beforeHead)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != report.CommitHash {
		t.Fatalf("HEAD = %q, report commit hash = %q", got, report.CommitHash)
	}
	if got := git(t, repo, "log", "-1", "--format=%s"); got != "blk-pipe: apply bounded engine changes" {
		t.Fatalf("commit message = %q", got)
	}
	assertStringSlice(t, report.StagedFiles, []string{"src/allowed.txt"})
	assertStringSlice(t, report.DestroyedFiles, []string{})
	if got := readFile(t, filepath.Join(repo, "src", "allowed.txt")); got != "after\n" {
		t.Fatalf("allowed file content = %q", got)
	}
	assertClean(t, repo)
}

func TestRunV47SuccessNormalizesPayloadAndReportsStableFields(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	payload := v47RunPayloadJSON(t, repo, []string{"-c", "printf 'after\\n' > README.md"}, []string{"README.md"})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())
	reportJSON := decodeReportMap(t, stdout.Bytes())

	if exitCode != ExitSuccess {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitSuccess, report)
	}
	if report.ExitCode != ExitSuccess {
		t.Fatalf("report exit code = %d, want %d", report.ExitCode, ExitSuccess)
	}
	if report.Status != "SUCCESS" {
		t.Fatalf("report status = %q, want SUCCESS", report.Status)
	}
	if report.Action != "execute" || report.Workdir != repo || report.WorkDir != repo {
		t.Fatalf("unexpected action/workdir fields in report: %+v", report)
	}
	if report.TargetBranch != "sprint/ceb-011" || report.CebID != "CEB_011" {
		t.Fatalf("unexpected V47 report fields: %+v", report)
	}
	if report.CommitHash == "" || report.CommitHash == beforeHead {
		t.Fatalf("commit hash = %q, before HEAD = %q", report.CommitHash, beforeHead)
	}
	assertStringSlice(t, report.StagedFiles, []string{"README.md"})
	assertStableReportKeys(t, reportJSON, "exit_code", "pre_engine_hash", "git_diff", "engine_logs", "validation_logs", "diff_summary", "untracked_files", "staged_files", "destroyed_files")
	assertReportJSONValue(t, reportJSON, "exit_code", float64(ExitSuccess))
	assertClean(t, repo)
}

func TestRunReportInvalidPayloadIncludesExitCodeAndStableV47Fields(t *testing.T) {
	payload := []byte(`{"action":"execute","work_dir":"relative/repo","engine":"sh","engine_args":["-c","true"],"allowed_modified_files":[],"allowed_new_files":[]}`)

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())
	reportJSON := decodeReportMap(t, stdout.Bytes())

	if exitCode != ExitInvalidPayload {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitInvalidPayload, report)
	}
	if report.ExitCode != ExitInvalidPayload {
		t.Fatalf("report exit code = %d, want %d", report.ExitCode, ExitInvalidPayload)
	}
	if report.Status != "INVALID_PAYLOAD" {
		t.Fatalf("report status = %q, want INVALID_PAYLOAD", report.Status)
	}
	if report.Action != "execute" || report.WorkDir != "relative/repo" {
		t.Fatalf("unexpected V47 report fields for invalid payload: %+v", report)
	}
	assertStableEmptyReportFields(t, reportJSON, ExitInvalidPayload)
}

func TestRunInvalidPayloadWorkdirConflictPreservesReportMetadata(t *testing.T) {
	payload, err := json.Marshal(map[string]interface{}{
		"action":                 "execute",
		"workdir":                "/legacy/repo",
		"work_dir":               "/v47/repo",
		"target_branch":          "sprint/ceb-012",
		"ceb_id":                 "CEB_012",
		"engine":                 "sh",
		"engine_args":            []string{"-c", "true"},
		"allowed_modified_files": []string{"README.md"},
		"allowed_new_files":      []string{"src/new.md"},
	})
	if err != nil {
		t.Fatalf("marshal payload: %v", err)
	}

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())
	reportJSON := decodeReportMap(t, stdout.Bytes())

	if exitCode != ExitInvalidPayload {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitInvalidPayload, report)
	}
	if report.ExitCode != ExitInvalidPayload {
		t.Fatalf("report exit code = %d, want %d", report.ExitCode, ExitInvalidPayload)
	}
	if report.Status != "INVALID_PAYLOAD" {
		t.Fatalf("report status = %q, want INVALID_PAYLOAD", report.Status)
	}
	if !strings.Contains(report.Error, "workdir") || !strings.Contains(report.Error, "work_dir") {
		t.Fatalf("report error = %q, want workdir/work_dir conflict", report.Error)
	}
	if report.Action != "execute" || report.Workdir != "/legacy/repo" || report.WorkDir != "/v47/repo" {
		t.Fatalf("unexpected report action/workdir metadata: %+v", report)
	}
	if report.TargetBranch != "sprint/ceb-012" || report.CebID != "CEB_012" {
		t.Fatalf("unexpected report V47 metadata: %+v", report)
	}
	assertStableEmptyReportFields(t, reportJSON, ExitInvalidPayload)
}

func TestRunInvalidPayloadEngineConflictPreservesReportMetadata(t *testing.T) {
	payload, err := json.Marshal(map[string]interface{}{
		"action":                 "execute",
		"workdir":                "/absolute/repo",
		"work_dir":               "/absolute/repo",
		"target_branch":          "sprint/ceb-013",
		"ceb_id":                 "CEB_013",
		"engine_command":         []string{"sh", "-c", "printf legacy > README.md"},
		"engine":                 "sh",
		"engine_args":            []string{"-c", "printf v47 > README.md"},
		"allowed_modified_files": []string{"README.md"},
		"allowed_new_files":      []string{"src/new.md"},
		"timeout_seconds":        5,
		"max_output_bytes":       4096,
	})
	if err != nil {
		t.Fatalf("marshal payload: %v", err)
	}

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())
	reportJSON := decodeReportMap(t, stdout.Bytes())

	if exitCode != ExitInvalidPayload {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitInvalidPayload, report)
	}
	if report.ExitCode != ExitInvalidPayload {
		t.Fatalf("report exit code = %d, want %d", report.ExitCode, ExitInvalidPayload)
	}
	if report.Status != "INVALID_PAYLOAD" {
		t.Fatalf("report status = %q, want INVALID_PAYLOAD", report.Status)
	}
	if !strings.Contains(report.Error, "engine_command") || !strings.Contains(report.Error, "engine") {
		t.Fatalf("report error = %q, want engine conflict", report.Error)
	}
	if report.Action != "execute" || report.Workdir != "/absolute/repo" || report.WorkDir != "/absolute/repo" {
		t.Fatalf("unexpected report action/workdir metadata: %+v", report)
	}
	if report.TargetBranch != "sprint/ceb-013" || report.CebID != "CEB_013" {
		t.Fatalf("unexpected report V47 metadata: %+v", report)
	}
	assertStableEmptyReportFields(t, reportJSON, ExitInvalidPayload)
}

func TestRunSuccessDisablesPreExistingGitHooksDuringCommit(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	hookPath := filepath.Join(repo, ".git", "hooks", "post-commit")
	if err := os.WriteFile(hookPath, []byte("#!/bin/sh\nprintf hook-ran > hook-ran.txt\n"), 0o755); err != nil {
		t.Fatalf("write post-commit hook: %v", err)
	}

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf 'after\\n' > README.md"},
		AllowedModifiedFiles: []string{"README.md"},
		TimeoutSeconds:       5,
		MaxOutputBytes:       4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitSuccess {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitSuccess, report)
	}
	if report.Status != "SUCCESS" {
		t.Fatalf("report status = %q, want SUCCESS", report.Status)
	}
	if _, err := os.Stat(filepath.Join(repo, "hook-ran.txt")); !os.IsNotExist(err) {
		t.Fatalf("post-commit hook ran or hook-ran.txt stat failed with non-ENOENT: %v", err)
	}
	assertClean(t, repo)
}

func TestRunUnauthorizedMutationCleansAndExitsThree(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")

	payload := payloadJSON(t, contracts.Payload{
		Action:         "execute",
		Workdir:        repo,
		EngineCommand:  []string{"sh", "-c", "mkdir -p src && printf 'nope\\n' > src/unauthorized.txt"},
		TimeoutSeconds: 5,
		MaxOutputBytes: 4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitUnauthorizedMutation {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitUnauthorizedMutation, report)
	}
	if report.Status != "UNAUTHORIZED_FILE_MUTATION" {
		t.Fatalf("report status = %q", report.Status)
	}
	if _, err := os.Stat(filepath.Join(repo, "src", "unauthorized.txt")); !os.IsNotExist(err) {
		t.Fatalf("unauthorized file still exists or stat failed with non-ENOENT: %v", err)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertStringSlice(t, report.DestroyedFiles, []string{"src/unauthorized.txt"})
	assertClean(t, repo)
}

func TestRunUnauthorizedMutationRemovesNestedGitRepository(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")

	payload := payloadJSON(t, contracts.Payload{
		Action:         "execute",
		Workdir:        repo,
		EngineCommand:  []string{"sh", "-c", "git init -q evil && printf 'nope\\n' > evil/unauthorized.txt"},
		TimeoutSeconds: 5,
		MaxOutputBytes: 4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitUnauthorizedMutation {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitUnauthorizedMutation, report)
	}
	if report.Status != "UNAUTHORIZED_FILE_MUTATION" {
		t.Fatalf("report status = %q, want UNAUTHORIZED_FILE_MUTATION", report.Status)
	}
	assertStringSliceContains(t, report.DestroyedFiles, "evil/")
	if _, err := os.Stat(filepath.Join(repo, "evil")); !os.IsNotExist(err) {
		t.Fatalf("nested git repo still exists or stat failed with non-ENOENT: %v", err)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertClean(t, repo)
}

func TestRunGitExcludeMutationCannotHideUnauthorizedFile(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	beforeExclude := readFile(t, filepath.Join(repo, ".git", "info", "exclude"))

	payload := payloadJSON(t, contracts.Payload{
		Action:         "execute",
		Workdir:        repo,
		EngineCommand:  []string{"sh", "-c", "printf 'secret.txt\\n' >> .git/info/exclude && printf 'secret\\n' > secret.txt"},
		TimeoutSeconds: 5,
		MaxOutputBytes: 4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitUnauthorizedMutation {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitUnauthorizedMutation, report)
	}
	if report.Status != "UNAUTHORIZED_FILE_MUTATION" {
		t.Fatalf("report status = %q, want UNAUTHORIZED_FILE_MUTATION", report.Status)
	}
	assertStringSlice(t, report.DestroyedFiles, []string{".git/info/exclude", "secret.txt"})
	if got := readFile(t, filepath.Join(repo, ".git", "info", "exclude")); got != beforeExclude {
		t.Fatalf(".git/info/exclude = %q, want restored %q", got, beforeExclude)
	}
	if _, err := os.Stat(filepath.Join(repo, "secret.txt")); !os.IsNotExist(err) {
		t.Fatalf("secret.txt still exists or stat failed with non-ENOENT: %v", err)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertClean(t, repo)
}

func TestRunGitRootDeletionIsUnauthorizedAndRecovered(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")

	payload := payloadJSON(t, contracts.Payload{
		Action:         "execute",
		Workdir:        repo,
		EngineCommand:  []string{"sh", "-c", "rm -rf .git && printf unauthorized > unauthorized.txt"},
		TimeoutSeconds: 5,
		MaxOutputBytes: 4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitUnauthorizedMutation {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitUnauthorizedMutation, report)
	}
	if report.Status != "UNAUTHORIZED_FILE_MUTATION" {
		t.Fatalf("report status = %q, want UNAUTHORIZED_FILE_MUTATION", report.Status)
	}
	assertStringSliceContains(t, report.DestroyedFiles, ".git/HEAD")
	assertStringSliceContains(t, report.DestroyedFiles, "unauthorized.txt")
	if _, err := os.Stat(filepath.Join(repo, ".git")); err != nil {
		t.Fatalf(".git was not restored: %v", err)
	}
	if _, err := os.Stat(filepath.Join(repo, "unauthorized.txt")); !os.IsNotExist(err) {
		t.Fatalf("unauthorized.txt still exists or stat failed with non-ENOENT: %v", err)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertClean(t, repo)
}

func TestRunGitHookMutationIsUnauthorizedAndHookDoesNotRun(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	beforeReadme := readFile(t, filepath.Join(repo, "README.md"))

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf '#!/bin/sh\\nprintf hook-ran > hook-ran.txt\\n' > .git/hooks/post-commit && chmod +x .git/hooks/post-commit && printf 'after\\n' > README.md"},
		AllowedModifiedFiles: []string{"README.md"},
		TimeoutSeconds:       5,
		MaxOutputBytes:       4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitUnauthorizedMutation {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitUnauthorizedMutation, report)
	}
	if report.Status != "UNAUTHORIZED_FILE_MUTATION" {
		t.Fatalf("report status = %q, want UNAUTHORIZED_FILE_MUTATION", report.Status)
	}
	assertStringSlice(t, report.DestroyedFiles, []string{".git/hooks/post-commit"})
	if _, err := os.Stat(filepath.Join(repo, ".git", "hooks", "post-commit")); !os.IsNotExist(err) {
		t.Fatalf("post-commit hook still exists or stat failed with non-ENOENT: %v", err)
	}
	if _, err := os.Stat(filepath.Join(repo, "hook-ran.txt")); !os.IsNotExist(err) {
		t.Fatalf("post-commit hook ran or hook-ran.txt stat failed with non-ENOENT: %v", err)
	}
	if got := readFile(t, filepath.Join(repo, "README.md")); got != beforeReadme {
		t.Fatalf("README.md = %q, want restored %q", got, beforeReadme)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertClean(t, repo)
}

func TestRunGitHookMutationBlocksValidationAndRestores(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	beforeReadme := readFile(t, filepath.Join(repo, "README.md"))
	sentinel := filepath.Join(repo, "validation-ran.txt")

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf '#!/bin/sh\\nprintf hook-ran > hook-ran.txt\\n' > .git/hooks/post-commit && chmod +x .git/hooks/post-commit && printf 'after\\n' > README.md"},
		ValidationCommands:   []string{"printf validation-ran > validation-ran.txt"},
		AllowedModifiedFiles: []string{"README.md"},
		TimeoutSeconds:       5,
		MaxOutputBytes:       4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitUnauthorizedMutation {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitUnauthorizedMutation, report)
	}
	if report.Status != "UNAUTHORIZED_FILE_MUTATION" {
		t.Fatalf("report status = %q, want UNAUTHORIZED_FILE_MUTATION", report.Status)
	}
	assertStringSlice(t, report.DestroyedFiles, []string{".git/hooks/post-commit"})
	if len(report.ValidationLogs) != 0 {
		t.Fatalf("ValidationLogs = %v, want empty because validation must not run after .git mutation", report.ValidationLogs)
	}
	if _, err := os.Stat(sentinel); !os.IsNotExist(err) {
		t.Fatalf("validation sentinel exists or stat failed with non-ENOENT: %v", err)
	}
	if _, err := os.Stat(filepath.Join(repo, ".git", "hooks", "post-commit")); !os.IsNotExist(err) {
		t.Fatalf("post-commit hook still exists or stat failed with non-ENOENT: %v", err)
	}
	if got := readFile(t, filepath.Join(repo, "README.md")); got != beforeReadme {
		t.Fatalf("README.md = %q, want restored %q", got, beforeReadme)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	assertClean(t, repo)
}

func TestRunGitUnsupportedEntryMutationIsUnauthorizedRestoredAndDoesNotCommit(t *testing.T) {
	requireFIFOSupport(t)
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	beforeReadme := readFile(t, filepath.Join(repo, "README.md"))
	fifoPath := filepath.Join(repo, ".git", "evilfifo")

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "mkfifo .git/evilfifo && printf 'after\\n' > README.md"},
		AllowedModifiedFiles: []string{"README.md"},
		TimeoutSeconds:       5,
		MaxOutputBytes:       4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitUnauthorizedMutation {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitUnauthorizedMutation, report)
	}
	if report.Status != "UNAUTHORIZED_FILE_MUTATION" {
		t.Fatalf("report status = %q, want UNAUTHORIZED_FILE_MUTATION", report.Status)
	}
	assertStringSlice(t, report.DestroyedFiles, []string{".git/evilfifo"})
	if _, err := os.Stat(fifoPath); !os.IsNotExist(err) {
		t.Fatalf("unsupported .git FIFO still exists or stat failed with non-ENOENT: %v", err)
	}
	if got := readFile(t, filepath.Join(repo, "README.md")); got != beforeReadme {
		t.Fatalf("README.md = %q, want restored %q", got, beforeReadme)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertClean(t, repo)
}

func TestRunGitDirectoryReplacedByUnsupportedEntryIsUnauthorizedRestoredAndDoesNotCommit(t *testing.T) {
	requireFIFOSupport(t)
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	beforeReadme := readFile(t, filepath.Join(repo, "README.md"))
	hooksPath := filepath.Join(repo, ".git", "hooks")

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "rm -rf .git/hooks && mkfifo .git/hooks && printf 'after\\n' > README.md"},
		AllowedModifiedFiles: []string{"README.md"},
		TimeoutSeconds:       5,
		MaxOutputBytes:       4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitUnauthorizedMutation {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitUnauthorizedMutation, report)
	}
	if report.Status != "UNAUTHORIZED_FILE_MUTATION" {
		t.Fatalf("report status = %q, want UNAUTHORIZED_FILE_MUTATION", report.Status)
	}
	assertStringSliceContains(t, report.DestroyedFiles, ".git/hooks")
	assertGitPathIsDirectory(t, hooksPath)
	if got := readFile(t, filepath.Join(repo, "README.md")); got != beforeReadme {
		t.Fatalf("README.md = %q, want restored %q", got, beforeReadme)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertClean(t, repo)
}

func TestRunValidationGitDirectoryReplacedByUnsupportedEntryIsUnauthorizedRestoredAndDoesNotCommit(t *testing.T) {
	requireFIFOSupport(t)
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	beforeReadme := readFile(t, filepath.Join(repo, "README.md"))
	refsPath := filepath.Join(repo, ".git", "refs")

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf 'after\\n' > README.md"},
		ValidationCommands:   []string{"rm -rf .git/refs && mkfifo .git/refs"},
		AllowedModifiedFiles: []string{"README.md"},
		TimeoutSeconds:       5,
		MaxOutputBytes:       4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitUnauthorizedMutation {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitUnauthorizedMutation, report)
	}
	if report.Status != "UNAUTHORIZED_FILE_MUTATION" {
		t.Fatalf("report status = %q, want UNAUTHORIZED_FILE_MUTATION", report.Status)
	}
	assertStringSliceContains(t, report.DestroyedFiles, ".git/refs")
	assertGitPathIsDirectory(t, refsPath)
	if got := readFile(t, filepath.Join(repo, "README.md")); got != beforeReadme {
		t.Fatalf("README.md = %q, want restored %q", got, beforeReadme)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertClean(t, repo)
}

func TestRunValidationFailureAbortsBeforeCommitAndRestores(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	beforeReadme := readFile(t, filepath.Join(repo, "README.md"))
	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf 'after\\n' > README.md"},
		ValidationCommands:   []string{"printf 'validation stdout\\n'; printf 'validation stderr\\n' >&2; exit 9", "printf 'second validation\\n'"},
		AllowedModifiedFiles: []string{"README.md"},
		TimeoutSeconds:       5,
		MaxOutputBytes:       4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitValidationFailed {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitValidationFailed, report)
	}
	if report.Status != "SYNTAX_GATE_FAILED" {
		t.Fatalf("report status = %q, want SYNTAX_GATE_FAILED", report.Status)
	}
	if !strings.Contains(report.ValidationLogs["validation_001"], "validation stdout") || !strings.Contains(report.ValidationLogs["validation_001"], "validation stderr") {
		t.Fatalf("validation_001 log = %q, want stdout and stderr", report.ValidationLogs["validation_001"])
	}
	if report.ValidationLogs["validation_002"] != "second validation\n" {
		t.Fatalf("validation_002 log = %q, want second command output", report.ValidationLogs["validation_002"])
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if got := readFile(t, filepath.Join(repo, "README.md")); got != beforeReadme {
		t.Fatalf("README.md = %q, want restored %q", got, beforeReadme)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertClean(t, repo)
}

func TestRunValidationSuccessAllowsCommitAndReportsLogs(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf 'after\\n' > README.md"},
		ValidationCommands:   []string{"printf 'validation one\\n'", "test -f README.md && printf 'validation two\\n'"},
		AllowedModifiedFiles: []string{"README.md"},
		TimeoutSeconds:       5,
		MaxOutputBytes:       4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitSuccess {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitSuccess, report)
	}
	if report.Status != "SUCCESS" {
		t.Fatalf("report status = %q, want SUCCESS", report.Status)
	}
	if report.CommitHash == "" || report.CommitHash == beforeHead {
		t.Fatalf("commit hash = %q, before HEAD = %q", report.CommitHash, beforeHead)
	}
	assertStringSlice(t, report.StagedFiles, []string{"README.md"})
	if report.ValidationLogs["validation_001"] != "validation one\n" || report.ValidationLogs["validation_002"] != "validation two\n" {
		t.Fatalf("ValidationLogs = %v, want deterministic validation outputs", report.ValidationLogs)
	}
	if got := readFile(t, filepath.Join(repo, "README.md")); got != "after\n" {
		t.Fatalf("README.md = %q, want after", got)
	}
	assertClean(t, repo)
}

func TestRunValidationGitHookMutationIsUnauthorizedRestoredAndDoesNotCommit(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	beforeReadme := readFile(t, filepath.Join(repo, "README.md"))
	hookPath := filepath.Join(repo, ".git", "hooks", "post-commit")

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf 'after\\n' > README.md"},
		ValidationCommands:   []string{"printf '#!/bin/sh\\nprintf hook-ran > hook-ran.txt\\n' > .git/hooks/post-commit && chmod +x .git/hooks/post-commit"},
		AllowedModifiedFiles: []string{"README.md"},
		TimeoutSeconds:       5,
		MaxOutputBytes:       4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitUnauthorizedMutation {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitUnauthorizedMutation, report)
	}
	if report.Status != "UNAUTHORIZED_FILE_MUTATION" {
		t.Fatalf("report status = %q, want UNAUTHORIZED_FILE_MUTATION", report.Status)
	}
	assertStringSlice(t, report.DestroyedFiles, []string{".git/hooks/post-commit"})
	if _, err := os.Stat(hookPath); !os.IsNotExist(err) {
		t.Fatalf("validation-created post-commit hook still exists or stat failed with non-ENOENT: %v", err)
	}
	if _, err := os.Stat(filepath.Join(repo, "hook-ran.txt")); !os.IsNotExist(err) {
		t.Fatalf("validation-created post-commit hook ran or hook-ran.txt stat failed with non-ENOENT: %v", err)
	}
	if got := readFile(t, filepath.Join(repo, "README.md")); got != beforeReadme {
		t.Fatalf("README.md = %q, want restored %q", got, beforeReadme)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertClean(t, repo)
}

func TestRunValidationUnsupportedGitEntryMutationIsUnauthorizedRestoredAndDoesNotCommit(t *testing.T) {
	requireFIFOSupport(t)
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	beforeReadme := readFile(t, filepath.Join(repo, "README.md"))
	fifoPath := filepath.Join(repo, ".git", "evilfifo")

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf 'after\\n' > README.md"},
		ValidationCommands:   []string{"mkfifo .git/evilfifo"},
		AllowedModifiedFiles: []string{"README.md"},
		TimeoutSeconds:       5,
		MaxOutputBytes:       4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitUnauthorizedMutation {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitUnauthorizedMutation, report)
	}
	if report.Status != "UNAUTHORIZED_FILE_MUTATION" {
		t.Fatalf("report status = %q, want UNAUTHORIZED_FILE_MUTATION", report.Status)
	}
	assertStringSlice(t, report.DestroyedFiles, []string{".git/evilfifo"})
	if _, err := os.Stat(fifoPath); !os.IsNotExist(err) {
		t.Fatalf("validation-created unsupported .git FIFO still exists or stat failed with non-ENOENT: %v", err)
	}
	if got := readFile(t, filepath.Join(repo, "README.md")); got != beforeReadme {
		t.Fatalf("README.md = %q, want restored %q", got, beforeReadme)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertClean(t, repo)
}

func TestRunDirtyRepoBeforeEngineExitsSeven(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	testutil.WriteFile(t, repo, "dirty.txt", "dirty\n")

	payload := payloadJSON(t, contracts.Payload{
		Action:         "execute",
		Workdir:        repo,
		EngineCommand:  []string{"sh", "-c", "printf 'engine-ran' > engine-ran.txt"},
		TimeoutSeconds: 5,
		MaxOutputBytes: 4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitGitDirty {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitGitDirty, report)
	}
	if report.Status != "GIT_DIRTY" {
		t.Fatalf("report status = %q", report.Status)
	}
	if _, err := os.Stat(filepath.Join(repo, "engine-ran.txt")); !os.IsNotExist(err) {
		t.Fatalf("engine appears to have run; stat err=%v", err)
	}
	if report.Error == "" {
		t.Fatalf("expected dirty repo error in report")
	}
}

func TestRunPreExistingIgnoredFileExitsSevenBeforeEngine(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	testutil.WriteFile(t, repo, ".gitignore", "*.cache\n")
	testutil.RunGit(t, repo, "add", "--", ".gitignore")
	testutil.RunGit(t, repo, "commit", "-m", "ignore cache files")
	testutil.WriteFile(t, repo, "keep.cache", "keep\n")

	payload := payloadJSON(t, contracts.Payload{
		Action:         "execute",
		Workdir:        repo,
		EngineCommand:  []string{"sh", "-c", "printf 'engine-ran' > engine-ran.txt"},
		TimeoutSeconds: 5,
		MaxOutputBytes: 4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitGitDirty {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitGitDirty, report)
	}
	if report.Status != "GIT_DIRTY" {
		t.Fatalf("report status = %q", report.Status)
	}
	if _, err := os.Stat(filepath.Join(repo, "engine-ran.txt")); !os.IsNotExist(err) {
		t.Fatalf("engine appears to have run; stat err=%v", err)
	}
	if got := readFile(t, filepath.Join(repo, "keep.cache")); got != "keep\n" {
		t.Fatalf("keep.cache = %q, want preserved ignored file", got)
	}
	if report.Error == "" {
		t.Fatalf("expected dirty repo error in report")
	}
}

func TestRunProtectedDocsAllowlistRejectsBeforeEngine(t *testing.T) {
	tests := []struct {
		name            string
		allowedModified []string
		allowedNew      []string
		wantError       string
	}{
		{
			name:            "modified requirements artifact",
			allowedModified: []string{"docs/requirements/active/REQ-001.md"},
			wantError:       "docs/requirements",
		},
		{
			name:       "new use case artifact",
			allowedNew: []string{"docs/use_cases/staging/UC-001.md"},
			wantError:  "docs/use_cases",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			repo := testutil.NewGitRepo(t)
			payload := payloadJSON(t, contracts.Payload{
				Action:               "execute",
				Workdir:              repo,
				EngineCommand:        []string{"sh", "-c", "printf ran > engine-ran.txt"},
				AllowedModifiedFiles: tt.allowedModified,
				AllowedNewFiles:      tt.allowedNew,
				TimeoutSeconds:       5,
				MaxOutputBytes:       4096,
			})

			var stdout bytes.Buffer
			exitCode := Run(context.Background(), payload, &stdout)
			report := decodeReport(t, stdout.Bytes())

			if exitCode != ExitInvalidPayload {
				t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitInvalidPayload, report)
			}
			if report.Status != "INVALID_PAYLOAD" {
				t.Fatalf("report status = %q, want INVALID_PAYLOAD", report.Status)
			}
			if !strings.Contains(report.Error, tt.wantError) {
				t.Fatalf("report error = %q, want substring %q", report.Error, tt.wantError)
			}
			if _, err := os.Stat(filepath.Join(repo, "engine-ran.txt")); !os.IsNotExist(err) {
				t.Fatalf("engine appears to have run; stat err=%v", err)
			}
			assertClean(t, repo)
		})
	}
}

func TestRunEngineFailureRoutesToFatalSystemPanic(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")

	payload := payloadJSON(t, contracts.Payload{
		Action:         "execute",
		Workdir:        repo,
		EngineCommand:  []string{"sh", "-c", "printf oops; exit 42"},
		TimeoutSeconds: 5,
		MaxOutputBytes: 4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitFatalSystemPanic {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitFatalSystemPanic, report)
	}
	if exitCode == ExitInvalidRevertAnchor {
		t.Fatalf("engine failure used invalid-revert-anchor code %d", ExitInvalidRevertAnchor)
	}
	if report.Status != "FATAL_ENGINE_FAILED" {
		t.Fatalf("report status = %q, want FATAL_ENGINE_FAILED", report.Status)
	}
	if report.EngineExitCode != 42 {
		t.Fatalf("engine exit code = %d, want 42", report.EngineExitCode)
	}
	if report.EngineOutputBytes != int64(len("oops")) {
		t.Fatalf("engine output bytes = %d, want %d", report.EngineOutputBytes, len("oops"))
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertClean(t, repo)
}

func TestRunSuccessReportsBoundedEngineLogs(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf 'engine stdout\\n'; printf 'engine stderr\\n' >&2; printf 'after\\n' > README.md"},
		AllowedModifiedFiles: []string{"README.md"},
		TimeoutSeconds:       5,
		MaxOutputBytes:       4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitSuccess {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitSuccess, report)
	}
	if report.Status != "SUCCESS" {
		t.Fatalf("report status = %q, want SUCCESS", report.Status)
	}
	if report.ExitCode != ExitSuccess {
		t.Fatalf("report exit code = %d, want %d", report.ExitCode, ExitSuccess)
	}
	if report.PreEngineHash == "" {
		t.Fatalf("PreEngineHash is empty")
	}
	if report.PreEngineHash != beforeHead {
		t.Fatalf("PreEngineHash = %q, want initial HEAD %q", report.PreEngineHash, beforeHead)
	}
	if report.CommitHash == "" || report.CommitHash == report.PreEngineHash {
		t.Fatalf("CommitHash = %q, PreEngineHash = %q", report.CommitHash, report.PreEngineHash)
	}
	if !strings.Contains(report.GitDiff, "diff --git a/README.md b/README.md") || !strings.Contains(report.GitDiff, "+after") {
		t.Fatalf("GitDiff = %q, want README.md change", report.GitDiff)
	}
	if report.DiffSummary == nil {
		t.Fatalf("DiffSummary is nil")
	}
	if report.DiffSummary.FilesChanged != 1 {
		t.Fatalf("DiffSummary.FilesChanged = %d, want 1; summary=%+v", report.DiffSummary.FilesChanged, report.DiffSummary)
	}
	assertStringSlice(t, report.DiffSummary.Files, []string{"README.md"})
	assertStringSlice(t, report.UntrackedFiles, []string{})
	if !strings.Contains(report.EngineLogs, "engine stdout") || !strings.Contains(report.EngineLogs, "engine stderr") {
		t.Fatalf("EngineLogs = %q, want bounded stdout/stderr", report.EngineLogs)
	}
	if report.EngineOutputBytes != int64(len(report.EngineLogs)) {
		t.Fatalf("EngineOutputBytes = %d, len(EngineLogs) = %d", report.EngineOutputBytes, len(report.EngineLogs))
	}
	assertClean(t, repo)
}

func TestRunSuccessReportUntrackedFilesUsesRogueAuditShape(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	testutil.WriteFile(t, repo, ".gitignore", "*.cache\n")
	testutil.RunGit(t, repo, "add", "--", ".gitignore")
	testutil.RunGit(t, repo, "commit", "-m", "ignore cache files")
	testutil.WriteFile(t, repo, "scratch/nested.txt", "untracked\n")
	testutil.WriteFile(t, repo, "ignored.cache", "ignored\n")

	got, err := untrackedReportFiles(repo)
	if err != nil {
		t.Fatalf("untrackedReportFiles() error = %v", err)
	}
	assertStringSlice(t, got, []string{"scratch/"})
}

func TestRunZeroDiffAfterSuccessfulEngineIsUnauthorizedMutation(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf 'noop engine\\n'"},
		AllowedModifiedFiles: []string{"README.md"},
		TimeoutSeconds:       5,
		MaxOutputBytes:       4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitUnauthorizedMutation {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitUnauthorizedMutation, report)
	}
	if report.ExitCode != ExitUnauthorizedMutation {
		t.Fatalf("report exit code = %d, want %d", report.ExitCode, ExitUnauthorizedMutation)
	}
	if report.Status != "UNAUTHORIZED_FILE_MUTATION" {
		t.Fatalf("report status = %q, want UNAUTHORIZED_FILE_MUTATION", report.Status)
	}
	if report.PreEngineHash != beforeHead {
		t.Fatalf("PreEngineHash = %q, want initial HEAD %q", report.PreEngineHash, beforeHead)
	}
	if report.CommitHash != "" {
		t.Fatalf("CommitHash = %q, want empty", report.CommitHash)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertClean(t, repo)
}

func TestRunMissingAllowedNewAfterSuccessfulEngineIsUnauthorizedMutation(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	payload := payloadJSON(t, contracts.Payload{
		Action:          "execute",
		Workdir:         repo,
		EngineCommand:   []string{"sh", "-c", "printf 'noop engine\\n'"},
		AllowedNewFiles: []string{"new.txt"},
		TimeoutSeconds:  5,
		MaxOutputBytes:  4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitUnauthorizedMutation {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitUnauthorizedMutation, report)
	}
	if report.ExitCode != ExitUnauthorizedMutation {
		t.Fatalf("report exit code = %d, want %d", report.ExitCode, ExitUnauthorizedMutation)
	}
	if report.Status != "UNAUTHORIZED_FILE_MUTATION" {
		t.Fatalf("report status = %q, want UNAUTHORIZED_FILE_MUTATION", report.Status)
	}
	if report.PreEngineHash != beforeHead {
		t.Fatalf("PreEngineHash = %q, want initial HEAD %q", report.PreEngineHash, beforeHead)
	}
	if report.CommitHash != "" {
		t.Fatalf("CommitHash = %q, want empty", report.CommitHash)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if _, err := os.Stat(filepath.Join(repo, "new.txt")); !os.IsNotExist(err) {
		t.Fatalf("new.txt exists or stat failed with non-ENOENT: %v", err)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertClean(t, repo)
}

func TestRunReportGenerationFailureRollsBackCommittedChange(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	beforeReadme := readFile(t, filepath.Join(repo, "README.md"))
	testutil.RunGit(t, repo, "config", "diff.external", "false")
	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf 'after\\n' > README.md"},
		AllowedModifiedFiles: []string{"README.md"},
		TimeoutSeconds:       5,
		MaxOutputBytes:       4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitInternalError {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitInternalError, report)
	}
	if report.Status != "INTERNAL_ERROR" {
		t.Fatalf("report status = %q, want INTERNAL_ERROR", report.Status)
	}
	if !strings.Contains(report.Error, "git diff") {
		t.Fatalf("report error = %q, want git diff failure", report.Error)
	}
	if report.CommitHash != "" {
		t.Fatalf("CommitHash = %q, want empty after rollback", report.CommitHash)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if got := readFile(t, filepath.Join(repo, "README.md")); got != beforeReadme {
		t.Fatalf("README.md = %q, want restored %q", got, beforeReadme)
	}
	assertClean(t, repo)
}

func TestRunEngineFailureReportsBoundedEngineLogs(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	payload := payloadJSON(t, contracts.Payload{
		Action:         "execute",
		Workdir:        repo,
		EngineCommand:  []string{"sh", "-c", "printf 'failing stdout\\n'; printf 'failing stderr\\n' >&2; exit 42"},
		TimeoutSeconds: 5,
		MaxOutputBytes: 4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitFatalSystemPanic {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitFatalSystemPanic, report)
	}
	if report.Status != "FATAL_ENGINE_FAILED" {
		t.Fatalf("report status = %q, want FATAL_ENGINE_FAILED", report.Status)
	}
	if !strings.Contains(report.EngineLogs, "failing stdout") || !strings.Contains(report.EngineLogs, "failing stderr") {
		t.Fatalf("EngineLogs = %q, want bounded stdout/stderr", report.EngineLogs)
	}
	if report.EngineOutputBytes != int64(len(report.EngineLogs)) {
		t.Fatalf("EngineOutputBytes = %d, len(EngineLogs) = %d", report.EngineOutputBytes, len(report.EngineLogs))
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	assertClean(t, repo)
}

func TestRunOutputFloodDoesNotStoreUnboundedEngineLogsAndExitsFatalOutputFlood(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	payload := payloadJSON(t, contracts.Payload{
		Action:         "execute",
		Workdir:        repo,
		EngineCommand:  []string{"sh", "-c", "yes flood"},
		TimeoutSeconds: 5,
		MaxOutputBytes: 4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitOutputFlood {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitOutputFlood, report)
	}
	if report.Status != "FATAL_OUTPUT_FLOOD" {
		t.Fatalf("report status = %q, want FATAL_OUTPUT_FLOOD", report.Status)
	}
	if report.EngineOutputBytes <= 4096 {
		t.Fatalf("EngineOutputBytes = %d, want > 4096", report.EngineOutputBytes)
	}
	if len(report.EngineLogs) > 4096 {
		t.Fatalf("EngineLogs length = %d, want <= 4096", len(report.EngineLogs))
	}
	assertClean(t, repo)
}

func payloadJSON(t *testing.T, payload contracts.Payload) []byte {
	t.Helper()
	data, err := json.Marshal(payload)
	if err != nil {
		t.Fatalf("marshal payload: %v", err)
	}
	return data
}

func v47RunPayloadJSON(t *testing.T, repo string, engineArgs []string, allowedModified []string) []byte {
	t.Helper()
	data, err := json.Marshal(map[string]interface{}{
		"action":                 "execute",
		"ceb_id":                 "CEB_011",
		"work_dir":               repo,
		"target_branch":          "sprint/ceb-011",
		"engine":                 "sh",
		"engine_args":            engineArgs,
		"l2_packet":              "## fake packet",
		"validation_commands":    []string{"true"},
		"allowed_modified_files": allowedModified,
		"allowed_new_files":      []string{},
	})
	if err != nil {
		t.Fatalf("marshal V47 payload: %v", err)
	}
	return data
}

func decodeReport(t *testing.T, data []byte) contracts.Report {
	t.Helper()
	var report contracts.Report
	dec := json.NewDecoder(bytes.NewReader(data))
	dec.DisallowUnknownFields()
	if err := dec.Decode(&report); err != nil {
		t.Fatalf("decode report %q: %v", data, err)
	}
	var extra contracts.Report
	if err := dec.Decode(&extra); err != io.EOF {
		t.Fatalf("expected exactly one JSON report, got extra decode err %v after %q", err, data)
	}
	return report
}

func decodeReportMap(t *testing.T, data []byte) map[string]json.RawMessage {
	t.Helper()
	var got map[string]json.RawMessage
	if err := json.Unmarshal(data, &got); err != nil {
		t.Fatalf("decode report JSON map %q: %v", data, err)
	}
	return got
}

func assertStableEmptyReportFields(t *testing.T, got map[string]json.RawMessage, wantExitCode int) {
	t.Helper()
	assertStableReportKeys(t, got, "exit_code", "git_diff", "engine_logs", "validation_logs", "untracked_files", "staged_files", "destroyed_files")
	assertReportJSONValue(t, got, "exit_code", float64(wantExitCode))
	assertReportJSONValue(t, got, "git_diff", "")
	assertReportJSONValue(t, got, "engine_logs", "")
	assertReportJSONValue(t, got, "validation_logs", map[string]interface{}{})
	assertReportJSONValue(t, got, "untracked_files", []interface{}{})
	assertReportJSONValue(t, got, "destroyed_files", []interface{}{})
}

func assertStableReportKeys(t *testing.T, got map[string]json.RawMessage, keys ...string) {
	t.Helper()
	for _, key := range keys {
		if _, ok := got[key]; !ok {
			t.Fatalf("report JSON missing stable key %q in %v", key, got)
		}
	}
}

func assertReportJSONValue(t *testing.T, got map[string]json.RawMessage, key string, want interface{}) {
	t.Helper()
	var value interface{}
	if err := json.Unmarshal(got[key], &value); err != nil {
		t.Fatalf("json.Unmarshal key %q value %s error = %v", key, got[key], err)
	}
	gotJSON, err := json.Marshal(value)
	if err != nil {
		t.Fatalf("marshal value for key %q: %v", key, err)
	}
	wantJSON, err := json.Marshal(want)
	if err != nil {
		t.Fatalf("marshal wanted value for key %q: %v", key, err)
	}
	if string(gotJSON) != string(wantJSON) {
		t.Fatalf("JSON key %q = %s, want %s", key, gotJSON, wantJSON)
	}
}

func git(t *testing.T, repo string, args ...string) string {
	t.Helper()
	return trimTrailingNewline(testutil.RunGit(t, repo, args...))
}

func trimTrailingNewline(s string) string {
	for len(s) > 0 && (s[len(s)-1] == '\n' || s[len(s)-1] == '\r') {
		s = s[:len(s)-1]
	}
	return s
}

func readFile(t *testing.T, path string) string {
	t.Helper()
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("read %q: %v", path, err)
	}
	return string(data)
}

func assertStringSlice(t *testing.T, got []string, want []string) {
	t.Helper()
	if len(got) != len(want) {
		t.Fatalf("slice length = %d (%v), want %d (%v)", len(got), got, len(want), want)
	}
	for i := range want {
		if got[i] != want[i] {
			t.Fatalf("slice[%d] = %q in %v, want %q in %v", i, got[i], got, want[i], want)
		}
	}
}

func assertStringSliceContains(t *testing.T, got []string, want string) {
	t.Helper()
	for _, item := range got {
		if item == want {
			return
		}
	}
	t.Fatalf("slice %v does not contain %q", got, want)
}

func assertGitPathIsDirectory(t *testing.T, path string) {
	t.Helper()
	info, err := os.Lstat(path)
	if err != nil {
		t.Fatalf("git path %q was not restored: %v", path, err)
	}
	if !info.IsDir() {
		t.Fatalf("git path %q mode = %s, want directory", path, info.Mode())
	}
}

func assertClean(t *testing.T, repo string) {
	t.Helper()
	if got := testutil.RunGit(t, repo, "status", "--porcelain", "--untracked-files=all"); got != "" {
		t.Fatalf("repo not clean:\n%s", got)
	}
}

func requireFIFOSupport(t *testing.T) {
	t.Helper()
	if runtime.GOOS == "windows" {
		t.Skip("FIFOs are not supported on windows")
	}
	path := filepath.Join(t.TempDir(), "fifo")
	if err := syscall.Mkfifo(path, 0o600); err != nil {
		t.Skipf("FIFOs are not supported here: %v", err)
	}
}
