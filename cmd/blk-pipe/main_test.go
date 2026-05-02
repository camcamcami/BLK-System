package main

import (
	"bytes"
	"encoding/json"
	"strings"
	"testing"

	"github.com/camcamcami/BLK-System/internal/contracts"
	"github.com/camcamcami/BLK-System/internal/pipe"
)

func TestRunHealthPrintsDeterministicJSON(t *testing.T) {
	var stdout bytes.Buffer
	var stderr bytes.Buffer

	code := run([]string{"--health"}, strings.NewReader(""), &stdout, &stderr)

	if code != 0 {
		t.Fatalf("run health exit code = %d, want 0; stderr=%q", code, stderr.String())
	}
	want := "{\"status\":\"OK\",\"component\":\"blk-pipe\"}\n"
	if got := stdout.String(); got != want {
		t.Fatalf("health stdout = %q, want %q", got, want)
	}
	if got := stderr.String(); got != "" {
		t.Fatalf("health stderr = %q, want empty", got)
	}
}

func TestRunUnsupportedInvocationReturnsNonZero(t *testing.T) {
	var stdout bytes.Buffer
	var stderr bytes.Buffer

	code := run([]string{}, strings.NewReader(""), &stdout, &stderr)

	if code != 2 {
		t.Fatalf("unsupported invocation exit code = %d, want 2", code)
	}
	if got := stdout.String(); got != "" {
		t.Fatalf("unsupported invocation stdout = %q, want empty", got)
	}
	if got := stderr.String(); got != "unsupported invocation\n" {
		t.Fatalf("unsupported invocation stderr = %q, want unsupported invocation newline", got)
	}
}

func TestRunPayloadStdinInvalidJSONEmitsPipeReport(t *testing.T) {
	var stdout bytes.Buffer
	var stderr bytes.Buffer

	code := run([]string{"--payload-stdin"}, strings.NewReader("{"), &stdout, &stderr)

	if code != pipe.ExitInvalidPayload {
		t.Fatalf("payload stdin exit code = %d, want %d; stderr=%q", code, pipe.ExitInvalidPayload, stderr.String())
	}
	report := decodeReport(t, stdout.Bytes())
	if report.Status != "INVALID_PAYLOAD" {
		t.Fatalf("report status = %q, want INVALID_PAYLOAD", report.Status)
	}
	if report.Error == "" {
		t.Fatalf("expected parse error in report")
	}
	if got := stderr.String(); got != "" {
		t.Fatalf("payload stdin stderr = %q, want empty", got)
	}
}

func TestRunPayloadStdinInvalidPayloadEmitsPipeReport(t *testing.T) {
	var stdout bytes.Buffer
	var stderr bytes.Buffer

	code := run([]string{"--payload-stdin"}, strings.NewReader(`{"action":"execute"}`), &stdout, &stderr)

	if code != pipe.ExitInvalidPayload {
		t.Fatalf("payload stdin exit code = %d, want %d; stderr=%q", code, pipe.ExitInvalidPayload, stderr.String())
	}
	report := decodeReport(t, stdout.Bytes())
	if report.Status != "INVALID_PAYLOAD" {
		t.Fatalf("report status = %q, want INVALID_PAYLOAD", report.Status)
	}
	if report.Action != "execute" {
		t.Fatalf("report action = %q, want execute", report.Action)
	}
	if report.Error == "" {
		t.Fatalf("expected validation error in report")
	}
	if got := stderr.String(); got != "" {
		t.Fatalf("payload stdin stderr = %q, want empty", got)
	}
}

func decodeReport(t *testing.T, data []byte) contracts.Report {
	t.Helper()
	var report contracts.Report
	if err := json.Unmarshal(data, &report); err != nil {
		t.Fatalf("decode report %q: %v", data, err)
	}
	return report
}
