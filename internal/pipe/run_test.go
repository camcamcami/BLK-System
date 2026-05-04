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
	"time"

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

func TestRunSuccessAllowedModificationLeavesPhysicalClean(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")

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
	if report.CommitHash == "" || report.CommitHash == beforeHead {
		t.Fatalf("commit hash = %q, before HEAD = %q", report.CommitHash, beforeHead)
	}
	assertStringSlice(t, report.StagedFiles, []string{"README.md"})
	assertStringSlice(t, report.DestroyedFiles, []string{})
	assertPhysicallyClean(t, repo)
}

func TestRunSuccessPreservesPreExistingTrackedFileMode(t *testing.T) {
	if runtime.GOOS == "windows" {
		t.Skip("chmod-based file mode semantics are Unix-specific")
	}
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	readme := filepath.Join(repo, "README.md")
	beforeMode := os.FileMode(0o600)
	if err := os.Chmod(readme, beforeMode); err != nil {
		t.Fatalf("chmod README.md precondition: %v", err)
	}
	t.Cleanup(func() { _ = os.Chmod(readme, 0o644) })

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
	if report.CommitHash == "" || report.CommitHash == beforeHead {
		t.Fatalf("commit hash = %q, before HEAD = %q", report.CommitHash, beforeHead)
	}
	if got := fileModeChmod(t, readme); got != beforeMode {
		t.Fatalf("README.md mode = %s, want %s", got, beforeMode)
	}
	assertStringSlice(t, report.StagedFiles, []string{"README.md"})
	assertStringSlice(t, report.DestroyedFiles, []string{})
	assertPhysicallyClean(t, repo)
}

func TestRunSuccessPreservesPreExistingDirectoryMode(t *testing.T) {
	if runtime.GOOS == "windows" {
		t.Skip("chmod-based directory mode semantics are Unix-specific")
	}
	repo := testutil.NewGitRepo(t)
	testutil.WriteFile(t, repo, "src/file.txt", "tracked\n")
	testutil.RunGit(t, repo, "add", "--", "src/file.txt")
	testutil.RunGit(t, repo, "commit", "-m", "add tracked src")
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	srcDir := filepath.Join(repo, "src")
	beforeMode := os.FileMode(0o500) | os.ModeSticky
	if err := os.Chmod(srcDir, beforeMode); err != nil {
		t.Fatalf("chmod src precondition: %v", err)
	}
	t.Cleanup(func() { _ = os.Chmod(srcDir, 0o755) })

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
	if report.CommitHash == "" || report.CommitHash == beforeHead {
		t.Fatalf("commit hash = %q, before HEAD = %q", report.CommitHash, beforeHead)
	}
	if got := fileModeChmod(t, srcDir); got != beforeMode {
		t.Fatalf("src mode = %s, want %s", got, beforeMode)
	}
	assertStringSlice(t, report.StagedFiles, []string{"README.md"})
	assertStringSlice(t, report.DestroyedFiles, []string{})
	assertPhysicallyClean(t, repo)
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
	if report.TargetBranch != "sprint/ceb-011" || report.BebID != "BEB_011" {
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

func TestRunV47L2PacketDeliveredToEngineStdin(t *testing.T) {
	const expectedPacket = "EXPECTED_PACKET\nfrom V47 l2_packet"
	repo := testutil.NewGitRepo(t)
	payload, err := json.Marshal(map[string]interface{}{
		"action":                 "execute",
		"beb_id":                 "BEB_011",
		"work_dir":               repo,
		"target_branch":          "sprint/ceb-011",
		"engine":                 "sh",
		"engine_args":            []string{"-c", "umask 022; cat > packet.txt; chmod 0644 packet.txt"},
		"l2_packet":              expectedPacket,
		"validation_commands":    []string{"true"},
		"allowed_modified_files": []string{},
		"allowed_new_files":      []string{"packet.txt"},
	})
	if err != nil {
		t.Fatalf("marshal V47 payload: %v", err)
	}

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitSuccess {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitSuccess, report)
	}
	if report.Status != "SUCCESS" {
		t.Fatalf("report status = %q, want SUCCESS", report.Status)
	}
	assertStringSlice(t, report.StagedFiles, []string{"packet.txt"})
	if got := readFile(t, filepath.Join(repo, "packet.txt")); got != expectedPacket {
		t.Fatalf("packet.txt = %q, want %q", got, expectedPacket)
	}
	assertClean(t, repo)
}

func TestRunSuccessReportsTraceArtifacts(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	expected := []contracts.TraceArtifact{
		{Kind: "REQ", ID: "REQ-042", VersionHash: "sha256:0123456789abcdef"},
		{Kind: "UC", ID: "UC-007", VersionHash: "sha256:abcdef0123456789"},
	}
	payload, err := json.Marshal(map[string]interface{}{
		"action":                 "execute",
		"beb_id":                 "BEB_TRACE",
		"work_dir":               repo,
		"engine":                 "sh",
		"engine_args":            []string{"-c", "printf 'after\\n' > README.md"},
		"l2_packet":              "opaque BEB/L2 body remains uninterpreted",
		"validation_commands":    []string{"true"},
		"allowed_modified_files": []string{"README.md"},
		"allowed_new_files":      []string{},
		"trace_artifacts":        expected,
	})
	if err != nil {
		t.Fatalf("marshal V47 payload: %v", err)
	}

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())
	reportJSON := decodeReportMap(t, stdout.Bytes())

	if exitCode != ExitSuccess {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitSuccess, report)
	}
	if report.Status != "SUCCESS" {
		t.Fatalf("report status = %q, want SUCCESS", report.Status)
	}
	assertRunTraceArtifacts(t, report.TraceArtifacts, expected)
	assertReportJSONValue(t, reportJSON, "trace_artifacts", []interface{}{
		map[string]interface{}{"kind": "REQ", "id": "REQ-042", "version_hash": "sha256:0123456789abcdef"},
		map[string]interface{}{"kind": "UC", "id": "UC-007", "version_hash": "sha256:abcdef0123456789"},
	})
	assertClean(t, repo)
}

func TestRunRejectsOversizedPayloadBytesBeforeDecode(t *testing.T) {
	secret := "SECRET_DIRECT_PIPE_RUN_PAYLOAD_SHOULD_NOT_LEAK"
	payload := []byte(strings.Repeat("{", contracts.DefaultMaxPayloadJSONBytes+1) + secret)

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
	if !strings.Contains(report.Error, "payload JSON exceeds maximum size") {
		t.Fatalf("report error = %q, want payload byte cap", report.Error)
	}
	if strings.Contains(stdout.String(), secret) || strings.Contains(stdout.String(), strings.Repeat("{", 64)) {
		t.Fatalf("oversized payload body leaked into report: %s", stdout.String())
	}
	assertStableEmptyReportFields(t, reportJSON, ExitInvalidPayload)
}

func TestRunInvalidPayloadReportsTraceArtifactsWhenDecodedBeforeValidationFailure(t *testing.T) {
	expected := []contracts.TraceArtifact{
		{Kind: "REQ", ID: "REQ-042", VersionHash: "sha256:0123456789abcdef"},
	}
	payload, err := json.Marshal(map[string]interface{}{
		"action":                 "execute",
		"beb_id":                 "BEB_TRACE_INVALID",
		"work_dir":               "relative/repo",
		"engine":                 "sh",
		"engine_args":            []string{"-c", "true"},
		"l2_packet":              "opaque BEB/L2 body remains uninterpreted",
		"validation_commands":    []string{"true"},
		"allowed_modified_files": []string{"README.md"},
		"allowed_new_files":      []string{},
		"trace_artifacts":        expected,
	})
	if err != nil {
		t.Fatalf("marshal V47 payload: %v", err)
	}

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())
	reportJSON := decodeReportMap(t, stdout.Bytes())

	if exitCode != ExitInvalidPayload {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitInvalidPayload, report)
	}
	if report.Status != "INVALID_PAYLOAD" {
		t.Fatalf("report status = %q, want INVALID_PAYLOAD", report.Status)
	}
	assertRunTraceArtifacts(t, report.TraceArtifacts, expected)
	assertReportJSONValue(t, reportJSON, "trace_artifacts", []interface{}{
		map[string]interface{}{"kind": "REQ", "id": "REQ-042", "version_hash": "sha256:0123456789abcdef"},
	})
}

func TestRunInvalidTraceArtifactDoesNotEchoLongHash(t *testing.T) {
	longHash := "sha256:" + strings.Repeat("a", 300)
	payload, err := json.Marshal(map[string]interface{}{
		"action":                 "execute",
		"beb_id":                 "BEB_TRACE_INVALID_LONG",
		"work_dir":               "/absolute/repo",
		"engine":                 "sh",
		"engine_args":            []string{"-c", "true"},
		"validation_commands":    []string{"true"},
		"allowed_modified_files": []string{"README.md"},
		"allowed_new_files":      []string{},
		"trace_artifacts": []contracts.TraceArtifact{
			{Kind: "REQ", ID: "REQ-042", VersionHash: longHash},
		},
	})
	if err != nil {
		t.Fatalf("marshal V47 payload: %v", err)
	}

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())
	reportJSON := decodeReportMap(t, stdout.Bytes())

	if exitCode != ExitInvalidPayload {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitInvalidPayload, report)
	}
	if strings.Contains(string(stdout.Bytes()), longHash) || strings.Contains(report.Error, strings.Repeat("a", 64)) {
		t.Fatalf("invalid trace artifact leaked oversized hash in report: %s", stdout.String())
	}
	assertRunTraceArtifacts(t, report.TraceArtifacts, nil)
	assertReportJSONValue(t, reportJSON, "trace_artifacts", []interface{}{})
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
		"beb_id":                 "BEB_012",
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
	if report.TargetBranch != "sprint/ceb-012" || report.BebID != "BEB_012" {
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
		"beb_id":                 "BEB_013",
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
	if report.TargetBranch != "sprint/ceb-013" || report.BebID != "BEB_013" {
		t.Fatalf("unexpected report V47 metadata: %+v", report)
	}
	assertStableEmptyReportFields(t, reportJSON, ExitInvalidPayload)
}

func TestRunRevertSuccessResetsToVerifiedAncestorAndCleans(t *testing.T) {
	repo, targetHash, secondHash := twoCommitRepo(t)

	payload := payloadJSON(t, contracts.Payload{
		Action:     "revert",
		Workdir:    repo,
		TargetHash: targetHash,
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
	if report.Action != "revert" || report.Workdir != repo {
		t.Fatalf("unexpected action/workdir in report: %+v", report)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != targetHash {
		t.Fatalf("HEAD = %q, want target hash %q", got, targetHash)
	}
	if got := readFile(t, filepath.Join(repo, "README.md")); got != "initial\n" {
		t.Fatalf("README.md = %q, want first commit content", got)
	}
	if report.CommitHash != "" {
		t.Fatalf("CommitHash = %q, want empty because revert must not create a commit", report.CommitHash)
	}
	if targetHash == secondHash {
		t.Fatalf("test setup invalid: targetHash equals secondHash %q", targetHash)
	}
	assertClean(t, repo)
}

func TestRunRevertWithTargetBranchRejectsWrongCurrentBranch(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	targetHash := git(t, repo, "rev-parse", "HEAD")

	testutil.RunGit(t, repo, "checkout", "-b", "sprint/right")
	testutil.WriteFile(t, repo, "README.md", "right branch second\n")
	testutil.RunGit(t, repo, "add", "--", "README.md")
	testutil.RunGit(t, repo, "commit", "-m", "right branch second")

	testutil.RunGit(t, repo, "checkout", "-b", "sprint/wrong")
	testutil.WriteFile(t, repo, "README.md", "wrong branch head\n")
	testutil.RunGit(t, repo, "add", "--", "README.md")
	testutil.RunGit(t, repo, "commit", "-m", "wrong branch head")
	wrongHead := git(t, repo, "rev-parse", "HEAD")

	payload := payloadJSON(t, contracts.Payload{
		Action:       "revert",
		Workdir:      repo,
		TargetHash:   targetHash,
		TargetBranch: "sprint/right",
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitInvalidRevertAnchor {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitInvalidRevertAnchor, report)
	}
	if report.Status != "INVALID_REVERT_ANCHOR" {
		t.Fatalf("report status = %q, want INVALID_REVERT_ANCHOR", report.Status)
	}
	if got := git(t, repo, "rev-parse", "--abbrev-ref", "HEAD"); got != "sprint/wrong" {
		t.Fatalf("current branch = %q, want sprint/wrong", got)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != wrongHead {
		t.Fatalf("HEAD changed from %q to %q", wrongHead, got)
	}
	if got := readFile(t, filepath.Join(repo, "README.md")); got != "wrong branch head\n" {
		t.Fatalf("README.md = %q, want wrong branch content preserved", got)
	}
	assertClean(t, repo)
}

func TestRunRevertWithTargetBranchAcceptsMatchingCurrentBranch(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	targetHash := git(t, repo, "rev-parse", "HEAD")

	testutil.RunGit(t, repo, "checkout", "-b", "sprint/right")
	testutil.WriteFile(t, repo, "README.md", "right branch second\n")
	testutil.RunGit(t, repo, "add", "--", "README.md")
	testutil.RunGit(t, repo, "commit", "-m", "right branch second")

	payload := payloadJSON(t, contracts.Payload{
		Action:       "revert",
		Workdir:      repo,
		TargetHash:   targetHash,
		TargetBranch: "sprint/right",
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
	if got := git(t, repo, "rev-parse", "--abbrev-ref", "HEAD"); got != "sprint/right" {
		t.Fatalf("current branch = %q, want sprint/right", got)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != targetHash {
		t.Fatalf("HEAD = %q, want target hash %q", got, targetHash)
	}
	if got := readFile(t, filepath.Join(repo, "README.md")); got != "initial\n" {
		t.Fatalf("README.md = %q, want first commit content", got)
	}
	assertClean(t, repo)
}

func TestRunRevertWithoutTargetBranchPreservesLegacyCurrentBranchBehavior(t *testing.T) {
	repo, targetHash, _ := twoCommitRepo(t)
	testutil.RunGit(t, repo, "checkout", "-b", "sprint/current")

	payload := payloadJSON(t, contracts.Payload{
		Action:     "revert",
		Workdir:    repo,
		TargetHash: targetHash,
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
	if got := git(t, repo, "rev-parse", "--abbrev-ref", "HEAD"); got != "sprint/current" {
		t.Fatalf("current branch = %q, want sprint/current", got)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != targetHash {
		t.Fatalf("HEAD = %q, want target hash %q", got, targetHash)
	}
	if got := readFile(t, filepath.Join(repo, "README.md")); got != "initial\n" {
		t.Fatalf("README.md = %q, want first commit content", got)
	}
	assertClean(t, repo)
}

func TestRunRevertSHA256RejectsAbbreviatedFortyHexTarget(t *testing.T) {
	repo, targetHash, secondHash := twoCommitSHA256Repo(t)
	abbreviated := targetHash[:40]

	payload := payloadJSON(t, contracts.Payload{
		Action:     "revert",
		Workdir:    repo,
		TargetHash: abbreviated,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitInvalidRevertAnchor {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitInvalidRevertAnchor, report)
	}
	if report.Status != "INVALID_REVERT_ANCHOR" {
		t.Fatalf("report status = %q, want INVALID_REVERT_ANCHOR", report.Status)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != secondHash {
		t.Fatalf("HEAD changed from %q to %q", secondHash, got)
	}
	if got := readFile(t, filepath.Join(repo, "README.md")); got != "second\n" {
		t.Fatalf("README.md = %q, want second commit content preserved", got)
	}
	assertClean(t, repo)
}

func TestRunRevertSHA256AcceptsFullSixtyFourHexTarget(t *testing.T) {
	repo, targetHash, _ := twoCommitSHA256Repo(t)

	payload := payloadJSON(t, contracts.Payload{
		Action:     "revert",
		Workdir:    repo,
		TargetHash: targetHash,
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
	if got := git(t, repo, "rev-parse", "HEAD"); got != targetHash {
		t.Fatalf("HEAD = %q, want target hash %q", got, targetHash)
	}
	if len(targetHash) != 64 {
		t.Fatalf("target hash length = %d, want 64 for SHA-256 repo", len(targetHash))
	}
	assertClean(t, repo)
}

func TestRunRevertPreExistingNestedGitRepositoryExitsSevenBeforeReset(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	targetHash := git(t, repo, "rev-parse", "HEAD")
	sub := filepath.Join(repo, "vendor", "sub")
	if err := os.MkdirAll(sub, 0o755); err != nil {
		t.Fatalf("create nested repo dir: %v", err)
	}
	testutil.RunGit(t, sub, "init")
	testutil.RunGit(t, sub, "config", "--local", "user.name", "BLK Test")
	testutil.RunGit(t, sub, "config", "--local", "user.email", "blk-test@example.invalid")
	testutil.RunGit(t, sub, "config", "--local", "commit.gpgsign", "false")
	testutil.WriteFile(t, sub, "README.md", "nested\n")
	testutil.RunGit(t, sub, "add", "--", "README.md")
	testutil.RunGit(t, sub, "commit", "-m", "nested initial")
	testutil.RunGit(t, repo, "add", "--", "vendor/sub")
	testutil.RunGit(t, repo, "commit", "-m", "add nested git repo")
	beforeHead := git(t, repo, "rev-parse", "HEAD")

	payload := payloadJSON(t, contracts.Payload{
		Action:     "revert",
		Workdir:    repo,
		TargetHash: targetHash,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitGitDirty {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitGitDirty, report)
	}
	if report.Status != "GIT_DIRTY" {
		t.Fatalf("report status = %q, want GIT_DIRTY", report.Status)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	assertGitPathIsDirectory(t, filepath.Join(sub, ".git"))
	if !strings.Contains(report.Error, "vendor/sub/.git/") {
		t.Fatalf("report error = %q, want vendor/sub/.git/", report.Error)
	}
}

func TestRunRevertInvalidAnchorDoesNotReset(t *testing.T) {
	repo, firstHash, secondHash := twoCommitRepo(t)
	mainBranch := git(t, repo, "rev-parse", "--abbrev-ref", "HEAD")
	testutil.RunGit(t, repo, "checkout", "-b", "side", firstHash)
	testutil.WriteFile(t, repo, "side.txt", "side\n")
	testutil.RunGit(t, repo, "add", "--", "side.txt")
	testutil.RunGit(t, repo, "commit", "-m", "side commit")
	sideHash := git(t, repo, "rev-parse", "HEAD")
	testutil.RunGit(t, repo, "checkout", mainBranch)

	payload := payloadJSON(t, contracts.Payload{
		Action:     "revert",
		Workdir:    repo,
		TargetHash: sideHash,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitInvalidRevertAnchor {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitInvalidRevertAnchor, report)
	}
	if report.Status != "INVALID_REVERT_ANCHOR" {
		t.Fatalf("report status = %q, want INVALID_REVERT_ANCHOR", report.Status)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != secondHash {
		t.Fatalf("HEAD changed from %q to %q", secondHash, got)
	}
	if got := readFile(t, filepath.Join(repo, "README.md")); got != "second\n" {
		t.Fatalf("README.md = %q, want second commit content preserved", got)
	}
	assertClean(t, repo)
}

func TestRunRevertPreExistingEmptyUntrackedDirectoryIsPreserved(t *testing.T) {
	repo, targetHash, secondHash := twoCommitRepo(t)
	emptyDir := filepath.Join(repo, "scratch", "empty")
	if err := os.MkdirAll(emptyDir, 0o755); err != nil {
		t.Fatalf("create empty untracked dir: %v", err)
	}

	payload := payloadJSON(t, contracts.Payload{
		Action:     "revert",
		Workdir:    repo,
		TargetHash: targetHash,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitGitDirty {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitGitDirty, report)
	}
	if report.Status != "GIT_DIRTY" {
		t.Fatalf("report status = %q, want GIT_DIRTY", report.Status)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != secondHash {
		t.Fatalf("HEAD changed from %q to %q", secondHash, got)
	}
	if info, err := os.Stat(emptyDir); err != nil || !info.IsDir() {
		t.Fatalf("empty untracked dir was not preserved; info=%v err=%v", info, err)
	}
}

func TestRunRevertDirtyTrackedWorktreeIsPreserved(t *testing.T) {
	repo, targetHash, secondHash := twoCommitRepo(t)
	testutil.WriteFile(t, repo, "README.md", "dirty user work\n")

	payload := payloadJSON(t, contracts.Payload{
		Action:     "revert",
		Workdir:    repo,
		TargetHash: targetHash,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitGitDirty {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitGitDirty, report)
	}
	if report.Status != "GIT_DIRTY" {
		t.Fatalf("report status = %q, want GIT_DIRTY", report.Status)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != secondHash {
		t.Fatalf("HEAD changed from %q to %q", secondHash, got)
	}
	if got := readFile(t, filepath.Join(repo, "README.md")); got != "dirty user work\n" {
		t.Fatalf("README.md = %q, want dirty user work preserved", got)
	}
}

func TestRunRevertPreExistingUntrackedAndIgnoredFilesArePreserved(t *testing.T) {
	tests := []struct {
		name    string
		prepare func(t *testing.T, repo string)
		path    string
		want    string
	}{
		{
			name: "untracked",
			prepare: func(t *testing.T, repo string) {
				testutil.WriteFile(t, repo, "scratch.txt", "scratch\n")
			},
			path: "scratch.txt",
			want: "scratch\n",
		},
		{
			name: "ignored",
			prepare: func(t *testing.T, repo string) {
				testutil.WriteFile(t, repo, ".gitignore", "*.cache\n")
				testutil.RunGit(t, repo, "add", "--", ".gitignore")
				testutil.RunGit(t, repo, "commit", "-m", "ignore cache files")
				testutil.WriteFile(t, repo, "keep.cache", "keep\n")
			},
			path: "keep.cache",
			want: "keep\n",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			repo, targetHash, _ := twoCommitRepo(t)
			tt.prepare(t, repo)
			beforeHead := git(t, repo, "rev-parse", "HEAD")

			payload := payloadJSON(t, contracts.Payload{
				Action:     "revert",
				Workdir:    repo,
				TargetHash: targetHash,
			})

			var stdout bytes.Buffer
			exitCode := Run(context.Background(), payload, &stdout)
			report := decodeReport(t, stdout.Bytes())

			if exitCode != ExitGitDirty {
				t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitGitDirty, report)
			}
			if report.Status != "GIT_DIRTY" {
				t.Fatalf("report status = %q, want GIT_DIRTY", report.Status)
			}
			if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
				t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
			}
			if got := readFile(t, filepath.Join(repo, tt.path)); got != tt.want {
				t.Fatalf("%s = %q, want preserved %q", tt.path, got, tt.want)
			}
		})
	}
}

func TestRunRevertDoesNotRunEngineValidationOrCommit(t *testing.T) {
	repo, targetHash, _ := twoCommitRepo(t)
	engineSentinel := filepath.Join(repo, "engine-ran.txt")
	validationSentinel := filepath.Join(repo, "validation-ran.txt")

	payload := payloadJSON(t, contracts.Payload{
		Action:               "revert",
		Workdir:              repo,
		TargetHash:           targetHash,
		EngineCommand:        []string{"sh", "-c", "printf engine > engine-ran.txt && printf engine > README.md"},
		ValidationCommands:   []string{"printf validation > validation-ran.txt"},
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
	if _, err := os.Stat(engineSentinel); !os.IsNotExist(err) {
		t.Fatalf("engine sentinel exists or stat failed with non-ENOENT: %v", err)
	}
	if _, err := os.Stat(validationSentinel); !os.IsNotExist(err) {
		t.Fatalf("validation sentinel exists or stat failed with non-ENOENT: %v", err)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != targetHash {
		t.Fatalf("HEAD = %q, want target hash %q", got, targetHash)
	}
	if got := git(t, repo, "log", "-1", "--format=%s"); got != "initial commit" {
		t.Fatalf("HEAD commit subject = %q, want initial commit", got)
	}
	if report.CommitHash != "" {
		t.Fatalf("CommitHash = %q, want empty because revert must not commit", report.CommitHash)
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

func TestRunUnauthorizedWarningPrefixUntrackedPathFailsCleansAndDoesNotCommit(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf 'after\\n' > README.md; printf residue > 'warning:evil'"},
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
	assertStringSliceContains(t, report.DestroyedFiles, "warning:evil")
	if _, err := os.Stat(filepath.Join(repo, "warning:evil")); !os.IsNotExist(err) {
		t.Fatalf("warning:evil survived cleanup or stat failed with non-ENOENT: %v", err)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertPhysicallyClean(t, repo)
}

func TestRunUnauthorizedWarningDiagnosticNewlineUntrackedPathFailsCleansAndDoesNotCommit(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	diagnosticLookingPath := "warning: hidden\n"

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf 'after\\n' > README.md; printf residue > \"warning: hidden\n\""},
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
	assertStringSliceContains(t, report.DestroyedFiles, diagnosticLookingPath)
	if _, err := os.Stat(filepath.Join(repo, diagnosticLookingPath)); !os.IsNotExist(err) {
		t.Fatalf("diagnostic-looking newline path survived cleanup or stat failed with non-ENOENT: %v", err)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertPhysicallyClean(t, repo)
}

func TestRunUnauthorizedWarningPrefixTrackedPathFailsRestoresAndDoesNotCommit(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	testutil.WriteFile(t, repo, "warning:tracked", "before\n")
	testutil.RunGit(t, repo, "add", "--", "warning:tracked")
	testutil.RunGit(t, repo, "commit", "-m", "add warning prefix tracked file")
	beforeHead := git(t, repo, "rev-parse", "HEAD")

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf 'after\\n' > README.md; printf changed > 'warning:tracked'"},
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
	assertStringSliceContains(t, report.DestroyedFiles, "warning:tracked")
	if got := readFile(t, filepath.Join(repo, "warning:tracked")); got != "before\n" {
		t.Fatalf("warning:tracked = %q, want restored before contents", got)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertPhysicallyClean(t, repo)
}

func TestRunUnauthorizedEmptyDirectoryFailsAndCleans(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf changed > README.md; mkdir ghostdir"},
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
	assertStringSliceContains(t, report.DestroyedFiles, "ghostdir/")
	if _, err := os.Stat(filepath.Join(repo, "ghostdir")); !os.IsNotExist(err) {
		t.Fatalf("ghostdir survived cleanup or stat failed with non-ENOENT: %v", err)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertPhysicallyClean(t, repo)
}

func TestRunUnauthorizedEmptyNestedGitDirectoryFailsAndCleans(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf changed > README.md; mkdir -p ghost/.git"},
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
	assertStringSliceContains(t, report.DestroyedFiles, "ghost/.git/")
	if _, err := os.Stat(filepath.Join(repo, "ghost")); !os.IsNotExist(err) {
		t.Fatalf("ghost survived cleanup or stat failed with non-ENOENT: %v", err)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertPhysicallyClean(t, repo)
}

func TestRunUnauthorizedNonEmptyNestedGitDirectoryFailsAndCleans(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf 'after\\n' > README.md; mkdir -p ghost/.git; printf x > ghost/.git/config"},
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
	assertStringSliceContains(t, report.DestroyedFiles, "ghost/.git/")
	if stringSliceContains(report.DestroyedFiles, "ghost/") {
		t.Fatalf("destroyed files = %v, want ghost/.git/ without parent ghost/ entry", report.DestroyedFiles)
	}
	if _, err := os.Stat(filepath.Join(repo, "ghost")); !os.IsNotExist(err) {
		t.Fatalf("ghost survived cleanup or stat failed with non-ENOENT: %v", err)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertPhysicallyClean(t, repo)
}

func TestRunUnauthorizedUnreadableDirectoryFailsAndCleans(t *testing.T) {
	if runtime.GOOS == "windows" {
		t.Skip("chmod-based unreadable directory semantics are Unix-specific")
	}
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	noAccessDir := filepath.Join(repo, "noaccess")
	t.Cleanup(func() { _ = os.Chmod(noAccessDir, 0o755) })

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf changed > README.md; mkdir noaccess; chmod 000 noaccess"},
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
	assertStringSliceContains(t, report.DestroyedFiles, "noaccess/")
	if _, err := os.Stat(noAccessDir); !os.IsNotExist(err) {
		t.Fatalf("noaccess survived cleanup or stat failed with non-ENOENT: %v", err)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertPhysicallyClean(t, repo)
}

func TestRunUnauthorizedNonEmptyUnreadableDirectoryFailsAndCleans(t *testing.T) {
	if runtime.GOOS == "windows" {
		t.Skip("chmod-based unreadable directory semantics are Unix-specific")
	}
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	noAccessDir := filepath.Join(repo, "noaccess")
	t.Cleanup(func() { _ = os.Chmod(noAccessDir, 0o755) })

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf changed > README.md; mkdir noaccess; printf residue > noaccess/file; chmod 000 noaccess"},
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
	if !stringSliceContains(report.DestroyedFiles, "noaccess/") && !stringSliceContains(report.DestroyedFiles, "noaccess/file") {
		t.Fatalf("destroyed files = %v, want noaccess/ or noaccess/file", report.DestroyedFiles)
	}
	for _, destroyed := range report.DestroyedFiles {
		if strings.Contains(strings.ToLower(destroyed), "warning:") || strings.Contains(strings.ToLower(destroyed), "permission denied") {
			t.Fatalf("destroyed files include Git warning text as path: %v", report.DestroyedFiles)
		}
	}
	if _, err := os.Stat(noAccessDir); !os.IsNotExist(err) {
		t.Fatalf("noaccess survived cleanup or stat failed with non-ENOENT: %v", err)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertPhysicallyClean(t, repo)
}

func TestRunUnauthorizedPreExistingDirectoryModeMutationFailsRestoresAndCleans(t *testing.T) {
	if runtime.GOOS == "windows" {
		t.Skip("chmod-based directory mode semantics are Unix-specific")
	}
	repo := testutil.NewGitRepo(t)
	testutil.WriteFile(t, repo, "src/file.txt", "tracked\n")
	testutil.RunGit(t, repo, "add", "--", "src/file.txt")
	testutil.RunGit(t, repo, "commit", "-m", "add tracked src")
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	srcDir := filepath.Join(repo, "src")
	beforeMode := fileModePerm(t, srcDir)
	t.Cleanup(func() { _ = os.Chmod(srcDir, beforeMode) })

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf changed > README.md; chmod 000 src"},
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
	assertStringSliceContains(t, report.DestroyedFiles, "src/")
	if got := fileModePerm(t, srcDir); got != beforeMode {
		t.Fatalf("src mode = %03o, want restored %03o", got, beforeMode)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertPhysicallyClean(t, repo)
}

func TestRunUnauthorizedAllowedTrackedFileModeMutationFailsRestoresAndDoesNotCommit(t *testing.T) {
	if runtime.GOOS == "windows" {
		t.Skip("chmod-based file mode semantics are Unix-specific")
	}
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	readme := filepath.Join(repo, "README.md")
	beforeContent := readFile(t, readme)
	beforeMode := os.FileMode(0o644)
	if err := os.Chmod(readme, beforeMode); err != nil {
		t.Fatalf("chmod README.md precondition: %v", err)
	}
	t.Cleanup(func() { _ = os.Chmod(readme, beforeMode) })

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf 'after\\n' > README.md; chmod 600 README.md"},
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
	assertStringSliceContains(t, report.DestroyedFiles, "README.md")
	if got := readFile(t, readme); got != beforeContent {
		t.Fatalf("README.md = %q, want restored %q", got, beforeContent)
	}
	if got := fileModeChmod(t, readme); got != beforeMode {
		t.Fatalf("README.md mode = %s, want restored %s", got, beforeMode)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertPhysicallyClean(t, repo)
}

func TestRunUnauthorizedWorktreeRootPermissionMutationFailsRestoresAndCleans(t *testing.T) {
	if runtime.GOOS == "windows" {
		t.Skip("chmod-based directory mode semantics are Unix-specific")
	}
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	beforeMode := fileModePerm(t, repo)
	t.Cleanup(func() { _ = os.Chmod(repo, beforeMode) })

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf after > README.md; chmod 000 ."},
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
	assertStringSliceContains(t, report.DestroyedFiles, ".")
	if got := fileModePerm(t, repo); got != beforeMode {
		t.Fatalf("repo root mode = %03o, want restored %03o", got, beforeMode)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertPhysicallyClean(t, repo)
}

func TestRunUnauthorizedRootGitPermissionMutationFailsRestoresAndCleans(t *testing.T) {
	if runtime.GOOS == "windows" {
		t.Skip("chmod-based directory mode semantics are Unix-specific")
	}
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	gitDir := filepath.Join(repo, ".git")
	beforeMode := fileModePerm(t, gitDir)
	t.Cleanup(func() { _ = os.Chmod(gitDir, beforeMode) })

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf after > README.md; chmod 000 .git"},
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
	assertStringSliceContains(t, report.DestroyedFiles, ".git/")
	if got := fileModePerm(t, gitDir); got != beforeMode {
		t.Fatalf(".git mode = %03o, want restored %03o", got, beforeMode)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertPhysicallyClean(t, repo)
}

func TestRunUnauthorizedNestedGitPermissionMutationFailsRestoresAndCleans(t *testing.T) {
	if runtime.GOOS == "windows" {
		t.Skip("chmod-based directory mode semantics are Unix-specific")
	}
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	objectsDir := filepath.Join(repo, ".git", "objects")
	beforeMode := fileModeChmod(t, objectsDir)
	t.Cleanup(func() { _ = os.Chmod(objectsDir, beforeMode) })

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf after > README.md; chmod 000 .git/objects"},
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
	assertStringSliceContains(t, report.DestroyedFiles, ".git/objects")
	if got := fileModeChmod(t, objectsDir); got != beforeMode {
		t.Fatalf(".git/objects mode = %s, want restored %s", got, beforeMode)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertPhysicallyClean(t, repo)
}

func TestRunUnauthorizedNestedGitObjectResidueInUnreadableDirectoryCleans(t *testing.T) {
	if runtime.GOOS == "windows" {
		t.Skip("chmod-based directory mode semantics are Unix-specific")
	}
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	objectsDir := filepath.Join(repo, ".git", "objects")
	evilPath := filepath.Join(objectsDir, "zz", "evil")
	beforeMode := fileModeChmod(t, objectsDir)
	t.Cleanup(func() { _ = os.Chmod(objectsDir, beforeMode) })

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf after > README.md; mkdir -p .git/objects/zz; printf evil > .git/objects/zz/evil; chmod 000 .git/objects"},
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
	assertStringSliceContains(t, report.DestroyedFiles, ".git/objects")
	if _, err := os.Stat(evilPath); !os.IsNotExist(err) {
		t.Fatalf(".git/objects/zz/evil survived cleanup or stat failed with non-ENOENT: %v", err)
	}
	if got := fileModeChmod(t, objectsDir); got != beforeMode {
		t.Fatalf(".git/objects mode = %s, want restored %s", got, beforeMode)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertPhysicallyClean(t, repo)
}

func TestRunUnauthorizedNestedGitHookResidueInUnreadableDirectoryCleans(t *testing.T) {
	if runtime.GOOS == "windows" {
		t.Skip("chmod-based directory mode semantics are Unix-specific")
	}
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	hooksDir := filepath.Join(repo, ".git", "hooks")
	evilPath := filepath.Join(hooksDir, "evil")
	beforeMode := fileModeChmod(t, hooksDir)
	t.Cleanup(func() { _ = os.Chmod(hooksDir, beforeMode) })

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf after > README.md; printf evil > .git/hooks/evil; chmod 000 .git/hooks"},
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
	if _, err := os.Stat(evilPath); !os.IsNotExist(err) {
		t.Fatalf(".git/hooks/evil survived cleanup or stat failed with non-ENOENT: %v", err)
	}
	if got := fileModeChmod(t, hooksDir); got != beforeMode {
		t.Fatalf(".git/hooks mode = %s, want restored %s", got, beforeMode)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertPhysicallyClean(t, repo)
}

func TestRunUnauthorizedNonEmptyDirectoryFailsAndCleans(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf changed > README.md; mkdir -p ghostdir && printf residue > ghostdir/file.txt"},
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
	assertStringSliceContains(t, report.DestroyedFiles, "ghostdir/file.txt")
	if _, err := os.Stat(filepath.Join(repo, "ghostdir")); !os.IsNotExist(err) {
		t.Fatalf("ghostdir survived cleanup or stat failed with non-ENOENT: %v", err)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertPhysicallyClean(t, repo)
}

func TestRunUnauthorizedIgnoredFileFailsAndCleans(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	testutil.WriteFile(t, repo, ".gitignore", "*.cache\n")
	testutil.RunGit(t, repo, "add", "--", ".gitignore")
	testutil.RunGit(t, repo, "commit", "-m", "ignore cache files")
	beforeHead := git(t, repo, "rev-parse", "HEAD")

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf changed > README.md; printf residue > ghost.cache"},
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
	assertStringSliceContains(t, report.DestroyedFiles, "ghost.cache")
	if _, err := os.Stat(filepath.Join(repo, "ghost.cache")); !os.IsNotExist(err) {
		t.Fatalf("ghost.cache survived cleanup or stat failed with non-ENOENT: %v", err)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertPhysicallyClean(t, repo)
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

func TestRunUnauthorizedGitDirectorySpecialModePreservedAfterMetadataRestore(t *testing.T) {
	if runtime.GOOS == "windows" {
		t.Skip("chmod-based directory mode semantics are Unix-specific")
	}
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	beforeExclude := readFile(t, filepath.Join(repo, ".git", "info", "exclude"))
	hooksDir := filepath.Join(repo, ".git", "hooks")
	beforeHooksMode := os.FileMode(0o755) | os.ModeSticky
	if err := os.Chmod(hooksDir, beforeHooksMode); err != nil {
		t.Fatalf("chmod .git/hooks precondition: %v", err)
	}
	t.Cleanup(func() { _ = os.Chmod(hooksDir, 0o755) })

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf '# unauthorized\\n' >> .git/info/exclude; printf after > README.md"},
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
	assertStringSliceContains(t, report.DestroyedFiles, ".git/info/exclude")
	if got := readFile(t, filepath.Join(repo, ".git", "info", "exclude")); got != beforeExclude {
		t.Fatalf(".git/info/exclude = %q, want restored %q", got, beforeExclude)
	}
	if got := fileModeChmod(t, hooksDir); got != beforeHooksMode {
		t.Fatalf(".git/hooks mode = %s, want restored %s", got, beforeHooksMode)
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

func TestRunValidationFailureWithGitMutationReportsUnauthorized(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	beforeReadme := readFile(t, filepath.Join(repo, "README.md"))

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf 'after\\n' > README.md"},
		ValidationCommands:   []string{"printf 'validation log before failure\\n'; printf 'malicious hook\\n' > .git/hooks/post-commit; exit 1"},
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
	assertStringSliceContains(t, report.DestroyedFiles, ".git/hooks/post-commit")
	if !strings.Contains(report.ValidationLogs["validation_001"], "validation log before failure") {
		t.Fatalf("validation_001 log = %q, want validation output preserved", report.ValidationLogs["validation_001"])
	}
	if _, err := os.Stat(filepath.Join(repo, ".git", "hooks", "post-commit")); !os.IsNotExist(err) {
		t.Fatalf("post-commit hook still exists or stat failed with non-ENOENT: %v", err)
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

func TestRunValidationFailureWithUnauthorizedWorktreeMutationReportsUnauthorized(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	beforeReadme := readFile(t, filepath.Join(repo, "README.md"))

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf 'after\\n' > README.md"},
		ValidationCommands:   []string{"printf 'validation log before failure\\n'; printf rogue > rogue.txt; exit 1"},
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
	assertStringSliceContains(t, report.DestroyedFiles, "rogue.txt")
	if !strings.Contains(report.ValidationLogs["validation_001"], "validation log before failure") {
		t.Fatalf("validation_001 log = %q, want validation output preserved", report.ValidationLogs["validation_001"])
	}
	if _, err := os.Stat(filepath.Join(repo, "rogue.txt")); !os.IsNotExist(err) {
		t.Fatalf("rogue.txt still exists or stat failed with non-ENOENT: %v", err)
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

func TestRunValidationFailureWithoutMutationStillReportsSyntaxGateFailed(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	beforeReadme := readFile(t, filepath.Join(repo, "README.md"))

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf 'after\\n' > README.md"},
		ValidationCommands:   []string{"printf 'validation failure log\\n'; exit 1"},
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
	if !strings.Contains(report.ValidationLogs["validation_001"], "validation failure log") {
		t.Fatalf("validation_001 log = %q, want validation output preserved", report.ValidationLogs["validation_001"])
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

func TestRunValidationCannotCreateFirstCommitWorthyDiff(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	beforeReadme := readFile(t, filepath.Join(repo, "README.md"))

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf noop"},
		ValidationCommands:   []string{"printf validation > README.md"},
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
	assertStringSliceContains(t, report.DestroyedFiles, "README.md")
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

func TestRunValidationCannotAlterEngineProducedDiff(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	beforeReadme := readFile(t, filepath.Join(repo, "README.md"))

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf engine > README.md"},
		ValidationCommands:   []string{"printf validation > README.md"},
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
	assertStringSliceContains(t, report.DestroyedFiles, "README.md")
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

func TestRunValidationCanReadWithoutMutating(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf engine > README.md"},
		ValidationCommands:   []string{"test \"$(cat README.md)\" = engine"},
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
	if got := readFile(t, filepath.Join(repo, "README.md")); got != "engine" {
		t.Fatalf("README.md = %q, want engine", got)
	}
	assertClean(t, repo)
}

func TestRunValidationMayUseExternalTempWithoutWorktreeMutation(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	externalTemp := t.TempDir()
	scratchPath := filepath.Join(externalTemp, "validation-scratch.txt")

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf engine > README.md"},
		ValidationCommands:   []string{"TMPDIR=" + externalTemp + " sh -c 'printf scratch > \"$TMPDIR/validation-scratch.txt\"'"},
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
	if got := readFile(t, filepath.Join(repo, "README.md")); got != "engine" {
		t.Fatalf("README.md = %q, want engine", got)
	}
	if got := readFile(t, scratchPath); got != "scratch" {
		t.Fatalf("external scratch = %q, want scratch", got)
	}
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

func TestRunValidationEmptyDirectoryFailsAndCleans(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	beforeReadme := readFile(t, filepath.Join(repo, "README.md"))

	payload := payloadJSON(t, contracts.Payload{
		Action:               "execute",
		Workdir:              repo,
		EngineCommand:        []string{"sh", "-c", "printf 'after\\n' > README.md"},
		ValidationCommands:   []string{"mkdir validation-residue"},
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
	assertStringSliceContains(t, report.DestroyedFiles, "validation-residue/")
	if _, err := os.Stat(filepath.Join(repo, "validation-residue")); !os.IsNotExist(err) {
		t.Fatalf("validation-residue survived cleanup or stat failed with non-ENOENT: %v", err)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if got := readFile(t, filepath.Join(repo, "README.md")); got != beforeReadme {
		t.Fatalf("README.md = %q, want restored %q", got, beforeReadme)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertPhysicallyClean(t, repo)
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

func TestRunPreExistingEmptyNestedGitDirectoryExitsSevenBeforeEngine(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	preexistingGitDir := filepath.Join(repo, "preexisting", ".git")
	if err := os.MkdirAll(preexistingGitDir, 0o755); err != nil {
		t.Fatalf("mkdir preexisting nested .git dir: %v", err)
	}

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
		t.Fatalf("report status = %q, want GIT_DIRTY", report.Status)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if _, err := os.Stat(filepath.Join(repo, "engine-ran.txt")); !os.IsNotExist(err) {
		t.Fatalf("engine appears to have run; stat err=%v", err)
	}
	assertGitPathIsDirectory(t, preexistingGitDir)
	if !strings.Contains(report.Error, "preexisting/.git/") {
		t.Fatalf("report error = %q, want preexisting/.git/", report.Error)
	}
}

func TestRunPreExistingNonEmptyNestedGitDirectoryExitsSevenBeforeEngine(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	preexistingGitDir := filepath.Join(repo, "preexisting", ".git")
	preexistingConfig := filepath.Join(preexistingGitDir, "config")
	if err := os.MkdirAll(preexistingGitDir, 0o755); err != nil {
		t.Fatalf("mkdir preexisting nested .git dir: %v", err)
	}
	if err := os.WriteFile(preexistingConfig, []byte("[core]\n"), 0o644); err != nil {
		t.Fatalf("write preexisting nested .git config: %v", err)
	}

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
		t.Fatalf("report status = %q, want GIT_DIRTY", report.Status)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if _, err := os.Stat(filepath.Join(repo, "engine-ran.txt")); !os.IsNotExist(err) {
		t.Fatalf("engine appears to have run; stat err=%v", err)
	}
	assertGitPathIsDirectory(t, preexistingGitDir)
	if got := readFile(t, preexistingConfig); got != "[core]\n" {
		t.Fatalf("preexisting .git/config = %q, want preserved", got)
	}
	if !strings.Contains(report.Error, "preexisting/.git/") {
		t.Fatalf("report error = %q, want preexisting/.git/", report.Error)
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
			name:            "modified active vault artifact",
			allowedModified: []string{"docs/active/REQ-001.md"},
			wantError:       "protected docs/active path",
		},
		{
			name:       "new use case artifact",
			allowedNew: []string{"docs/use_cases/staging/UC-001.md"},
			wantError:  "docs/use_cases",
		},
		{
			name:       "new active vault artifact",
			allowedNew: []string{"docs/active/UC-001.md"},
			wantError:  "protected docs/active path",
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

func TestRunUnauthorizedAllowedNewFileMode0600FailsCleansAndDoesNotCommit(t *testing.T) {
	if runtime.GOOS == "windows" {
		t.Skip("chmod-based file mode semantics are Unix-specific")
	}
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")

	payload := payloadJSON(t, contracts.Payload{
		Action:          "execute",
		Workdir:         repo,
		EngineCommand:   []string{"sh", "-c", "printf 'secret\\n' > new.txt; chmod 600 new.txt"},
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
	if report.Status != "UNAUTHORIZED_FILE_MUTATION" {
		t.Fatalf("report status = %q, want UNAUTHORIZED_FILE_MUTATION", report.Status)
	}
	assertStringSliceContains(t, report.DestroyedFiles, "new.txt")
	if _, err := os.Stat(filepath.Join(repo, "new.txt")); !os.IsNotExist(err) {
		t.Fatalf("new.txt survived cleanup or stat failed with non-ENOENT: %v", err)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertPhysicallyClean(t, repo)
}

func TestRunUnauthorizedAllowedNewExecutableFileMode4755FailsCleansAndDoesNotCommit(t *testing.T) {
	if runtime.GOOS == "windows" {
		t.Skip("chmod-based file mode semantics are Unix-specific")
	}
	repo := testutil.NewGitRepo(t)
	requireChmodModeSupported(t, repo, "setuid-probe", os.ModeSetuid|0o755, false)
	beforeHead := git(t, repo, "rev-parse", "HEAD")

	payload := payloadJSON(t, contracts.Payload{
		Action:          "execute",
		Workdir:         repo,
		EngineCommand:   []string{"sh", "-c", "printf '#!/bin/sh\\nexit 0\\n' > new-exec.sh; chmod 4755 new-exec.sh"},
		AllowedNewFiles: []string{"new-exec.sh"},
		TimeoutSeconds:  5,
		MaxOutputBytes:  4096,
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
	assertStringSliceContains(t, report.DestroyedFiles, "new-exec.sh")
	if _, err := os.Stat(filepath.Join(repo, "new-exec.sh")); !os.IsNotExist(err) {
		t.Fatalf("new-exec.sh survived cleanup or stat failed with non-ENOENT: %v", err)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertPhysicallyClean(t, repo)
}

func TestRunUnauthorizedAllowedNewParentDirectoryMode1777FailsCleansAndDoesNotCommit(t *testing.T) {
	if runtime.GOOS == "windows" {
		t.Skip("chmod-based directory mode semantics are Unix-specific")
	}
	repo := testutil.NewGitRepo(t)
	requireChmodModeSupported(t, repo, "sticky-dir-probe", os.ModeSticky|0o777, true)
	beforeHead := git(t, repo, "rev-parse", "HEAD")

	payload := payloadJSON(t, contracts.Payload{
		Action:          "execute",
		Workdir:         repo,
		EngineCommand:   []string{"sh", "-c", "mkdir -p unsafe-parent; chmod 1777 unsafe-parent; printf 'ok\\n' > unsafe-parent/new.txt; chmod 644 unsafe-parent/new.txt"},
		AllowedNewFiles: []string{"unsafe-parent/new.txt"},
		TimeoutSeconds:  5,
		MaxOutputBytes:  4096,
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
	assertStringSliceContains(t, report.DestroyedFiles, "unsafe-parent/")
	if _, err := os.Stat(filepath.Join(repo, "unsafe-parent")); !os.IsNotExist(err) {
		t.Fatalf("unsafe-parent survived cleanup or stat failed with non-ENOENT: %v", err)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	if report.CommitHash != "" {
		t.Fatalf("commit hash = %q, want empty", report.CommitHash)
	}
	assertStringSlice(t, report.StagedFiles, []string{})
	assertPhysicallyClean(t, repo)
}

func TestRunSuccessAllowedNewFileMode0644Commits(t *testing.T) {
	if runtime.GOOS == "windows" {
		t.Skip("chmod-based file mode semantics are Unix-specific")
	}
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")

	payload := payloadJSON(t, contracts.Payload{
		Action:          "execute",
		Workdir:         repo,
		EngineCommand:   []string{"sh", "-c", "printf 'ok\\n' > new.txt; chmod 644 new.txt"},
		AllowedNewFiles: []string{"new.txt"},
		TimeoutSeconds:  5,
		MaxOutputBytes:  4096,
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
	assertStringSlice(t, report.StagedFiles, []string{"new.txt"})
	if report.CommitHash == "" || report.CommitHash == beforeHead {
		t.Fatalf("commit hash = %q, beforeHead = %q", report.CommitHash, beforeHead)
	}
	if got := fileModeChmod(t, filepath.Join(repo, "new.txt")); got != 0o644 {
		t.Fatalf("new.txt mode = %s, want 0644", got)
	}
	assertClean(t, repo)
}

func TestRunSuccessAllowedNewExecutableFileMode0755Commits(t *testing.T) {
	if runtime.GOOS == "windows" {
		t.Skip("chmod-based file mode semantics are Unix-specific")
	}
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")

	payload := payloadJSON(t, contracts.Payload{
		Action:          "execute",
		Workdir:         repo,
		EngineCommand:   []string{"sh", "-c", "printf '#!/bin/sh\\nexit 0\\n' > new-exec.sh; chmod 755 new-exec.sh"},
		AllowedNewFiles: []string{"new-exec.sh"},
		TimeoutSeconds:  5,
		MaxOutputBytes:  4096,
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
	assertStringSlice(t, report.StagedFiles, []string{"new-exec.sh"})
	if report.CommitHash == "" || report.CommitHash == beforeHead {
		t.Fatalf("commit hash = %q, beforeHead = %q", report.CommitHash, beforeHead)
	}
	if got := fileModeChmod(t, filepath.Join(repo, "new-exec.sh")); got != 0o755 {
		t.Fatalf("new-exec.sh mode = %s, want 0755", got)
	}
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

func TestRunOutputFloodEscapedDescendantCannotMutateAfterReturn(t *testing.T) {
	if runtime.GOOS != "linux" {
		t.Skip("Linux /proc process-tree snapshot is required for redirected escaped descendant cleanup")
	}
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	lateFile := filepath.Join(repo, "late.txt")
	payload := payloadJSON(t, contracts.Payload{
		Action:  "execute",
		Workdir: repo,
		EngineCommand: []string{
			"sh", "-c",
			"setsid sh -c 'sleep 1; printf late > late.txt' >/dev/null 2>&1 & yes flood",
		},
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
	assertFileAbsentFor(t, lateFile, 2*time.Second)
	assertClean(t, repo)
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
}

func TestRunTimeoutEscapedDescendantCannotMutateAfterReturn(t *testing.T) {
	if runtime.GOOS != "linux" {
		t.Skip("Linux /proc pipe-holder discovery is required for escaped descendant cleanup")
	}
	repo := testutil.NewGitRepo(t)
	beforeHead := git(t, repo, "rev-parse", "HEAD")
	lateFile := filepath.Join(repo, "late.txt")
	payload := payloadJSON(t, contracts.Payload{
		Action:  "execute",
		Workdir: repo,
		EngineCommand: []string{
			"sh", "-c",
			"setsid sh -c 'sleep 1; printf late > late.txt' >/dev/null 2>&1 & sleep 10",
		},
		TimeoutSeconds: 5,
		MaxOutputBytes: 4096,
	})

	ctx, cancel := context.WithTimeout(context.Background(), 100*time.Millisecond)
	defer cancel()
	var stdout bytes.Buffer
	exitCode := Run(ctx, payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitEngineTimeout {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitEngineTimeout, report)
	}
	if report.Status != "ENGINE_TIMEOUT" {
		t.Fatalf("report status = %q, want ENGINE_TIMEOUT", report.Status)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
	assertClean(t, repo)
	assertFileAbsentFor(t, lateFile, 2*time.Second)
	assertClean(t, repo)
	if _, err := os.Stat(lateFile); !os.IsNotExist(err) {
		t.Fatalf("late.txt exists or stat failed with non-ENOENT: %v", err)
	}
	if got := git(t, repo, "rev-parse", "HEAD"); got != beforeHead {
		t.Fatalf("HEAD changed from %q to %q", beforeHead, got)
	}
}

func TestRunTargetBranchRejectsDirtyCurrentWorkspaceBeforeCheckout(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	mainBranch := git(t, repo, "rev-parse", "--abbrev-ref", "HEAD")
	testutil.RunGit(t, repo, "checkout", "-b", "feature/dirty-target")
	testutil.WriteFile(t, repo, "target.txt", "target\n")
	testutil.RunGit(t, repo, "add", "--", "target.txt")
	testutil.RunGit(t, repo, "commit", "-m", "target branch commit")
	testutil.RunGit(t, repo, "checkout", mainBranch)
	testutil.WriteFile(t, repo, "README.md", "dirty before branch prep\n")

	payload := payloadJSON(t, contracts.Payload{
		Action:          "execute",
		Workdir:         repo,
		TargetBranch:    "feature/dirty-target",
		EngineCommand:   []string{"sh", "-c", "printf should-not-run > should-not-run.txt"},
		AllowedNewFiles: []string{"should-not-run.txt"},
		TimeoutSeconds:  5,
		MaxOutputBytes:  4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitGitDirty {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitGitDirty, report)
	}
	if report.Status != "GIT_DIRTY" {
		t.Fatalf("report status = %q, want GIT_DIRTY", report.Status)
	}
	if got := git(t, repo, "rev-parse", "--abbrev-ref", "HEAD"); got != mainBranch {
		t.Fatalf("current branch = %q, want %q", got, mainBranch)
	}
	if got := readFile(t, filepath.Join(repo, "README.md")); got != "dirty before branch prep\n" {
		t.Fatalf("README.md = %q, want dirty content preserved", got)
	}
	if _, err := os.Stat(filepath.Join(repo, "should-not-run.txt")); !os.IsNotExist(err) {
		t.Fatalf("engine output exists or stat error = %v, want engine not run", err)
	}
	if report.PreEngineHash != "" {
		t.Fatalf("PreEngineHash = %q, want empty before branch prep failure", report.PreEngineHash)
	}
}

func TestRunTargetBranchExecutesOnExistingLocalBranch(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	mainBranch := git(t, repo, "rev-parse", "--abbrev-ref", "HEAD")
	testutil.RunGit(t, repo, "checkout", "-b", "feature/local-run")
	testutil.WriteFile(t, repo, "branch-base.txt", "local branch base\n")
	testutil.RunGit(t, repo, "add", "--", "branch-base.txt")
	testutil.RunGit(t, repo, "commit", "-m", "local run branch commit")
	branchHead := git(t, repo, "rev-parse", "HEAD")
	testutil.RunGit(t, repo, "checkout", mainBranch)

	payload := payloadJSON(t, contracts.Payload{
		Action:          "execute",
		Workdir:         repo,
		TargetBranch:    "feature/local-run",
		EngineCommand:   []string{"sh", "-c", "printf 'result\\n' > result.txt; chmod 644 result.txt"},
		AllowedNewFiles: []string{"result.txt"},
		TimeoutSeconds:  5,
		MaxOutputBytes:  4096,
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
	if got := git(t, repo, "rev-parse", "--abbrev-ref", "HEAD"); got != "feature/local-run" {
		t.Fatalf("current branch = %q", got)
	}
	if report.PreEngineHash != branchHead {
		t.Fatalf("PreEngineHash = %q, want target branch head %q", report.PreEngineHash, branchHead)
	}
	if got := readFile(t, filepath.Join(repo, "result.txt")); got != "result\n" {
		t.Fatalf("result.txt = %q", got)
	}
	assertStringSlice(t, report.StagedFiles, []string{"result.txt"})
	assertClean(t, repo)
}

func TestRunTargetBranchTracksRemoteBranch(t *testing.T) {
	root := t.TempDir()
	bare := filepath.Join(root, "remote.git")
	testutil.RunGit(t, root, "init", "--bare", bare)

	seed := testutil.NewGitRepo(t)
	defaultBranch := git(t, seed, "rev-parse", "--abbrev-ref", "HEAD")
	testutil.RunGit(t, seed, "remote", "add", "origin", bare)
	testutil.RunGit(t, seed, "push", "origin", defaultBranch)
	testutil.RunGit(t, seed, "checkout", "-b", "feature/remote-run")
	testutil.WriteFile(t, seed, "remote-base.txt", "remote branch base\n")
	testutil.RunGit(t, seed, "add", "--", "remote-base.txt")
	testutil.RunGit(t, seed, "commit", "-m", "remote run branch commit")
	remoteBranchHead := git(t, seed, "rev-parse", "HEAD")
	testutil.RunGit(t, seed, "push", "origin", "feature/remote-run")

	repo := filepath.Join(root, "work")
	testutil.RunGit(t, root, "clone", bare, repo)
	testutil.RunGit(t, repo, "config", "--local", "user.name", "BLK Test")
	testutil.RunGit(t, repo, "config", "--local", "user.email", "blk-test@example.invalid")
	testutil.RunGit(t, repo, "config", "--local", "commit.gpgsign", "false")

	payload := payloadJSON(t, contracts.Payload{
		Action:          "execute",
		Workdir:         repo,
		TargetBranch:    "feature/remote-run",
		EngineCommand:   []string{"sh", "-c", "printf 'remote result\\n' > remote-result.txt; chmod 644 remote-result.txt"},
		AllowedNewFiles: []string{"remote-result.txt"},
		TimeoutSeconds:  5,
		MaxOutputBytes:  4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitSuccess {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitSuccess, report)
	}
	if got := git(t, repo, "rev-parse", "--abbrev-ref", "HEAD"); got != "feature/remote-run" {
		t.Fatalf("current branch = %q", got)
	}
	if got := git(t, repo, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"); got != "origin/feature/remote-run" {
		t.Fatalf("upstream = %q, want origin/feature/remote-run", got)
	}
	if report.PreEngineHash != remoteBranchHead {
		t.Fatalf("PreEngineHash = %q, want remote branch head %q", report.PreEngineHash, remoteBranchHead)
	}
	assertClean(t, repo)
}

func TestRunTargetBranchOrphanInitializesEmptyTreeBeforeEngine(t *testing.T) {
	repo := testutil.NewGitRepo(t)

	payload := payloadJSON(t, contracts.Payload{
		Action:          "execute",
		Workdir:         repo,
		TargetBranch:    "feature/orphan-run",
		EngineCommand:   []string{"sh", "-c", "printf 'created\\n' > created.txt; chmod 644 created.txt"},
		AllowedNewFiles: []string{"created.txt"},
		TimeoutSeconds:  5,
		MaxOutputBytes:  4096,
	})

	var stdout bytes.Buffer
	exitCode := Run(context.Background(), payload, &stdout)
	report := decodeReport(t, stdout.Bytes())

	if exitCode != ExitSuccess {
		t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitSuccess, report)
	}
	if got := git(t, repo, "rev-parse", "--abbrev-ref", "HEAD"); got != "feature/orphan-run" {
		t.Fatalf("current branch = %q", got)
	}
	if report.PreEngineHash == "" || report.CommitHash == "" || report.PreEngineHash == report.CommitHash {
		t.Fatalf("unexpected pre/commit hashes: pre=%q commit=%q", report.PreEngineHash, report.CommitHash)
	}
	if got := git(t, repo, "ls-tree", "-r", "--name-only", report.PreEngineHash); got != "" {
		t.Fatalf("PreEngineHash tree contains %q, want empty tree", got)
	}
	if got := git(t, repo, "log", "--format=%s", "--max-count=2"); got != "blk-pipe: apply bounded engine changes\nInitialize branch" {
		t.Fatalf("last two commit subjects = %q", got)
	}
	if _, err := os.Stat(filepath.Join(repo, "README.md")); !os.IsNotExist(err) {
		t.Fatalf("README.md stat error = %v, want inherited file removed before engine", err)
	}
	if got := readFile(t, filepath.Join(repo, "created.txt")); got != "created\n" {
		t.Fatalf("created.txt = %q", got)
	}
	assertStringSlice(t, report.StagedFiles, []string{"created.txt"})
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
		"beb_id":                 "BEB_011",
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

func twoCommitRepo(t *testing.T) (repo string, firstHash string, secondHash string) {
	t.Helper()
	repo = testutil.NewGitRepo(t)
	firstHash = git(t, repo, "rev-parse", "HEAD")
	testutil.WriteFile(t, repo, "README.md", "second\n")
	testutil.RunGit(t, repo, "add", "--", "README.md")
	testutil.RunGit(t, repo, "commit", "-m", "second commit")
	secondHash = git(t, repo, "rev-parse", "HEAD")
	return repo, firstHash, secondHash
}

func twoCommitSHA256Repo(t *testing.T) (repo string, firstHash string, secondHash string) {
	t.Helper()
	repo = t.TempDir()
	testutil.RunGit(t, repo, "init", "--object-format=sha256")
	testutil.RunGit(t, repo, "config", "--local", "user.name", "BLK Test")
	testutil.RunGit(t, repo, "config", "--local", "user.email", "blk-test@example.invalid")
	testutil.RunGit(t, repo, "config", "--local", "commit.gpgsign", "false")
	testutil.WriteFile(t, repo, "README.md", "initial\n")
	testutil.RunGit(t, repo, "add", "--", "README.md")
	testutil.RunGit(t, repo, "commit", "-m", "initial commit")
	firstHash = git(t, repo, "rev-parse", "HEAD")
	testutil.WriteFile(t, repo, "README.md", "second\n")
	testutil.RunGit(t, repo, "add", "--", "README.md")
	testutil.RunGit(t, repo, "commit", "-m", "second commit")
	secondHash = git(t, repo, "rev-parse", "HEAD")
	return repo, firstHash, secondHash
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

func fileModePerm(t *testing.T, path string) os.FileMode {
	t.Helper()
	info, err := os.Lstat(path)
	if err != nil {
		t.Fatalf("lstat %q: %v", path, err)
	}
	return info.Mode().Perm()
}

func fileModeChmod(t *testing.T, path string) os.FileMode {
	t.Helper()
	info, err := os.Lstat(path)
	if err != nil {
		t.Fatalf("lstat %q: %v", path, err)
	}
	return worktreeDirChmodMode(info.Mode())
}

func requireChmodModeSupported(t *testing.T, repo, rel string, mode os.FileMode, isDir bool) {
	t.Helper()
	path := filepath.Join(repo, filepath.FromSlash(rel))
	if isDir {
		if err := os.MkdirAll(path, 0o755); err != nil {
			t.Fatalf("mkdir chmod mode probe %q: %v", rel, err)
		}
	} else {
		if err := os.WriteFile(path, []byte("probe\n"), 0o644); err != nil {
			t.Fatalf("write chmod mode probe %q: %v", rel, err)
		}
	}
	if err := os.Chmod(path, mode); err != nil {
		_ = os.RemoveAll(path)
		t.Skipf("chmod mode %s is not supported for this filesystem: %v", mode, err)
	}
	got := fileModeChmod(t, path)
	if err := os.RemoveAll(path); err != nil {
		t.Fatalf("remove chmod mode probe %q: %v", rel, err)
	}
	if got != mode {
		t.Skipf("chmod mode %s is not preserved on this filesystem; got %s", mode, got)
	}
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

func assertRunTraceArtifacts(t *testing.T, got []contracts.TraceArtifact, want []contracts.TraceArtifact) {
	t.Helper()
	if len(got) != len(want) {
		t.Fatalf("trace_artifacts length = %d (%v), want %d (%v)", len(got), got, len(want), want)
	}
	for i := range want {
		if got[i] != want[i] {
			t.Fatalf("trace_artifacts[%d] = %#v, want %#v", i, got[i], want[i])
		}
	}
}

func assertStringSliceContains(t *testing.T, got []string, want string) {
	t.Helper()
	if stringSliceContains(got, want) {
		return
	}
	t.Fatalf("slice %v does not contain %q", got, want)
}

func stringSliceContains(got []string, want string) bool {
	for _, item := range got {
		if item == want {
			return true
		}
	}
	return false
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

func assertFileAbsentFor(t *testing.T, path string, duration time.Duration) {
	t.Helper()
	deadline := time.Now().Add(duration)
	for time.Now().Before(deadline) {
		_, err := os.Stat(path)
		if err == nil {
			t.Fatalf("%s exists; escaped descendant mutated after Run returned", path)
		}
		if !os.IsNotExist(err) {
			t.Fatalf("stat %s: %v", path, err)
		}
		time.Sleep(10 * time.Millisecond)
	}
}

func assertPhysicallyClean(t *testing.T, repo string) {
	t.Helper()
	assertClean(t, repo)
	ignored, err := ignoredFileSet(repo)
	if err != nil {
		t.Fatalf("scan ignored files: %v", err)
	}
	if len(ignored) != 0 {
		t.Fatalf("repo has ignored residue: %v", ignored)
	}
	emptyDirs, err := emptyUntrackedDirs(repo)
	if err != nil {
		t.Fatalf("scan empty untracked dirs: %v", err)
	}
	if len(emptyDirs) != 0 {
		t.Fatalf("repo has empty untracked directory residue: %v", emptyDirs)
	}
	nestedGitDirs, err := nestedGitDirs(repo)
	if err != nil {
		t.Fatalf("scan nested .git dirs: %v", err)
	}
	if len(nestedGitDirs) != 0 {
		t.Fatalf("repo has nested .git directory residue: %v", nestedGitDirs)
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
