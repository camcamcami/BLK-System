package pipe

import (
	"bytes"
	"context"
	"encoding/json"
	"io"
	"os"
	"path/filepath"
	"strings"
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

func payloadJSON(t *testing.T, payload contracts.Payload) []byte {
	t.Helper()
	data, err := json.Marshal(payload)
	if err != nil {
		t.Fatalf("marshal payload: %v", err)
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

func assertClean(t *testing.T, repo string) {
	t.Helper()
	if got := testutil.RunGit(t, repo, "status", "--porcelain", "--untracked-files=all"); got != "" {
		t.Fatalf("repo not clean:\n%s", got)
	}
}
