package contracts

import (
	"encoding/json"
	"testing"
)

func TestReportJSONIncludesStableV47FieldsWhenEmpty(t *testing.T) {
	report := Report{
		Status:   "INVALID_PAYLOAD",
		ExitCode: 2,
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

	assertJSONValue(t, got, "exit_code", float64(2))
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
	data, err := json.Marshal(Report{Status: "INVALID_PAYLOAD", ExitCode: 2})
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
			{Kind: "REQ", ID: "REQ-042", VersionHash: "sha256:0123456789abcdef"},
			{Kind: "UC", ID: "UC-007", VersionHash: "sha256:abcdef0123456789"},
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
