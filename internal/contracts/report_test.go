package contracts

import (
	"encoding/json"
	"testing"
)

func TestReportJSONIncludesStableV47FieldsWhenEmpty(t *testing.T) {
	report := Report{
		Status:   "INVALID_PAYLOAD",
		ExitCode: 8,
		Action:   "execute",
		Workdir:  "/tmp/blk-pipe-repo",
	}

	data, err := json.Marshal(report)
	if err != nil {
		t.Fatalf("json.Marshal(Report) error = %v", err)
	}

	var got map[string]json.RawMessage
	if err := json.Unmarshal(data, &got); err != nil {
		t.Fatalf("json.Unmarshal(%s) error = %v", data, err)
	}

	wantKeys := []string{
		"exit_code",
		"commit_hash",
		"git_diff",
		"engine_logs",
		"validation_logs",
		"untracked_files",
		"staged_files",
		"destroyed_files",
		"error",
	}
	for _, key := range wantKeys {
		if _, ok := got[key]; !ok {
			t.Fatalf("Report JSON = %s, missing stable key %q", data, key)
		}
	}

	assertJSONValue(t, got, "exit_code", float64(8))
	assertJSONValue(t, got, "commit_hash", "")
	assertJSONValue(t, got, "git_diff", "")
	assertJSONValue(t, got, "engine_logs", "")
	assertJSONValue(t, got, "validation_logs", map[string]interface{}{})
	assertJSONValue(t, got, "untracked_files", []interface{}{})
	assertJSONValue(t, got, "staged_files", []interface{}{})
	assertJSONValue(t, got, "destroyed_files", []interface{}{})
	assertJSONValue(t, got, "error", "")
}

func TestReportMarshalEmitsTraceArtifactsAsStableEmptyList(t *testing.T) {
	data, err := json.Marshal(Report{Status: "INVALID_PAYLOAD", ExitCode: 8})
	if err != nil {
		t.Fatalf("json.Marshal(Report) error = %v", err)
	}

	var got map[string]json.RawMessage
	if err := json.Unmarshal(data, &got); err != nil {
		t.Fatalf("json.Unmarshal(%s) error = %v", data, err)
	}

	if _, ok := got["trace_artifacts"]; !ok {
		t.Fatalf("Report JSON = %s, missing stable key trace_artifacts", data)
	}
	assertJSONValue(t, got, "trace_artifacts", []interface{}{})
}

func TestReportMarshalPreservesTraceArtifacts(t *testing.T) {
	report := Report{
		Status: "SUCCESS",
		TraceArtifacts: []TraceArtifact{
			{Kind: "REQ", ID: "REQ-042", VersionHash: "sha256:0000000000000000000000000000000000000000000000000000000000000000"},
			{Kind: "UC", ID: "UC-007", VersionHash: "sha256:1111111111111111111111111111111111111111111111111111111111111111"},
		},
	}

	data, err := json.Marshal(report)
	if err != nil {
		t.Fatalf("json.Marshal(Report) error = %v", err)
	}

	var got Report
	if err := json.Unmarshal(data, &got); err != nil {
		t.Fatalf("json.Unmarshal(%s) error = %v", data, err)
	}
	if len(got.TraceArtifacts) != len(report.TraceArtifacts) {
		t.Fatalf("TraceArtifacts length = %d (%v), want %d (%v)", len(got.TraceArtifacts), got.TraceArtifacts, len(report.TraceArtifacts), report.TraceArtifacts)
	}
	for i := range report.TraceArtifacts {
		if got.TraceArtifacts[i] != report.TraceArtifacts[i] {
			t.Fatalf("TraceArtifacts[%d] = %#v, want %#v", i, got.TraceArtifacts[i], report.TraceArtifacts[i])
		}
	}
}

func TestReportMarshalIncludesValidationProfileEvidence(t *testing.T) {
	report := Report{
		Status:                     "SUCCESS",
		ValidationCommandSource:    "profile",
		ValidationProfiles:         []string{"go-full"},
		ResolvedValidationCommands: []string{"go test ./...", "go vet ./..."},
	}

	data, err := json.Marshal(report)
	if err != nil {
		t.Fatalf("json.Marshal(Report) error = %v", err)
	}

	var got map[string]json.RawMessage
	if err := json.Unmarshal(data, &got); err != nil {
		t.Fatalf("json.Unmarshal(%s) error = %v", data, err)
	}

	assertJSONValue(t, got, "validation_command_source", "profile")
	assertJSONValue(t, got, "validation_profiles", []interface{}{"go-full"})
	assertJSONValue(t, got, "resolved_validation_commands", []interface{}{"go test ./...", "go vet ./..."})
}

func TestReportMarshalIncludesExecutionBoundaryEvidence(t *testing.T) {
	report := Report{
		Status:               "UNAUTHORIZED_FILE_MUTATION",
		ExitCode:             3,
		Action:               "execute",
		Workdir:              "/tmp/blk-pipe-repo",
		TargetBranch:         "sprint/beb-114",
		TargetHash:           "0123456789abcdef0123456789abcdef01234567",
		TimeoutSeconds:       120,
		MaxOutputBytes:       8192,
		AllowedModifiedFiles: []string{"src/allowed.go"},
		AllowedNewFiles:      []string{"docs/outcome.md"},
		FailureClass:         "unauthorized_file_mutation",
		DenialRoute:          "allowlist_or_residue",
		CleanupStatus:        "worktree_restored_or_destroyed_files_reported",
	}

	data, err := json.Marshal(report)
	if err != nil {
		t.Fatalf("json.Marshal(Report) error = %v", err)
	}
	var got map[string]json.RawMessage
	if err := json.Unmarshal(data, &got); err != nil {
		t.Fatalf("json.Unmarshal(%s) error = %v", data, err)
	}

	assertJSONValue(t, got, "target_hash", "0123456789abcdef0123456789abcdef01234567")
	assertJSONValue(t, got, "timeout_seconds", float64(120))
	assertJSONValue(t, got, "max_output_bytes", float64(8192))
	assertJSONValue(t, got, "allowed_modified_files", []interface{}{"src/allowed.go"})
	assertJSONValue(t, got, "allowed_new_files", []interface{}{"docs/outcome.md"})
	assertJSONValue(t, got, "failure_class", "unauthorized_file_mutation")
	assertJSONValue(t, got, "denial_route", "allowlist_or_residue")
	assertJSONValue(t, got, "cleanup_status", "worktree_restored_or_destroyed_files_reported")
}

func assertJSONValue(t *testing.T, got map[string]json.RawMessage, key string, want interface{}) {
	t.Helper()
	var value interface{}
	if err := json.Unmarshal(got[key], &value); err != nil {
		t.Fatalf("json.Unmarshal key %q value %s error = %v", key, got[key], err)
	}
	if !jsonEqual(value, want) {
		t.Fatalf("JSON key %q = %#v, want %#v", key, value, want)
	}
}

func jsonEqual(got, want interface{}) bool {
	gotJSON, err := json.Marshal(got)
	if err != nil {
		return false
	}
	wantJSON, err := json.Marshal(want)
	if err != nil {
		return false
	}
	return string(gotJSON) == string(wantJSON)
}
