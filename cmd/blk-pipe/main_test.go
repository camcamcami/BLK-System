//go:build linux || darwin

package main

import (
	"bytes"
	"context"
	"encoding/json"
	"io"
	"os"
	"path/filepath"
	"strings"
	"sync/atomic"
	"syscall"
	"testing"
	"time"

	"github.com/camcamcami/BLK-System/internal/contracts"
	"github.com/camcamcami/BLK-System/internal/pipe"
	"github.com/camcamcami/BLK-System/internal/runtimeguard"
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

	if code != pipe.ExitInvalidPayload {
		t.Fatalf("unsupported invocation exit code = %d, want %d", code, pipe.ExitInvalidPayload)
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

func TestPayloadStdinRejectsOversizedPayload(t *testing.T) {
	const secret = "SECRET_PAYLOAD_BODY"
	oversized := strings.Repeat("x", contracts.DefaultMaxPayloadJSONBytes+1) + secret
	var stdout bytes.Buffer
	var stderr bytes.Buffer

	code := run([]string{"--payload-stdin"}, strings.NewReader(oversized), &stdout, &stderr)

	if code != pipe.ExitInvalidPayload {
		t.Fatalf("payload stdin exit code = %d, want %d", code, pipe.ExitInvalidPayload)
	}
	if got := stdout.String(); got != "" {
		t.Fatalf("oversized stdin stdout = %q, want empty", got)
	}
	if got := stderr.String(); !strings.Contains(got, "payload JSON exceeds maximum size") {
		t.Fatalf("oversized stdin stderr = %q, want size error", got)
	}
	if strings.Contains(stderr.String(), secret) || strings.Contains(stderr.String(), strings.Repeat("x", 64)) {
		t.Fatalf("oversized stdin error leaked payload body: %q", stderr.String())
	}
}

func TestPayloadFileInvalidJSONEmitsPipeReport(t *testing.T) {
	payloadPath := filepath.Join(t.TempDir(), "payload.json")
	if err := os.WriteFile(payloadPath, []byte("{"), 0o600); err != nil {
		t.Fatalf("write payload: %v", err)
	}
	var stdout bytes.Buffer
	var stderr bytes.Buffer

	code := run([]string{"--payload", payloadPath}, strings.NewReader(""), &stdout, &stderr)

	if code != pipe.ExitInvalidPayload {
		t.Fatalf("payload file exit code = %d, want %d; stdout=%q stderr=%q", code, pipe.ExitInvalidPayload, stdout.String(), stderr.String())
	}
	report := decodeReport(t, stdout.Bytes())
	if report.Status != "INVALID_PAYLOAD" {
		t.Fatalf("report status = %q, want INVALID_PAYLOAD", report.Status)
	}
	if report.Error == "" {
		t.Fatalf("expected parse error in report")
	}
	if got := stderr.String(); got != "" {
		t.Fatalf("payload file stderr = %q, want empty", got)
	}
}

func TestPayloadFileInvalidPayloadEmitsPipeReport(t *testing.T) {
	payloadPath := filepath.Join(t.TempDir(), "payload.json")
	if err := os.WriteFile(payloadPath, []byte(`{"action":"execute"}`), 0o600); err != nil {
		t.Fatalf("write payload: %v", err)
	}
	var stdout bytes.Buffer
	var stderr bytes.Buffer

	code := run([]string{"--payload", payloadPath}, strings.NewReader(""), &stdout, &stderr)

	if code != pipe.ExitInvalidPayload {
		t.Fatalf("payload file exit code = %d, want %d; stdout=%q stderr=%q", code, pipe.ExitInvalidPayload, stdout.String(), stderr.String())
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
		t.Fatalf("payload file stderr = %q, want empty", got)
	}
}

func TestPayloadFileRejectsOversizedPayloadBeforePipeRun(t *testing.T) {
	const secret = "SECRET_PAYLOAD_BODY"
	payloadPath := filepath.Join(t.TempDir(), "payload.json")
	oversized := strings.Repeat("x", contracts.DefaultMaxPayloadJSONBytes+1) + secret
	if err := os.WriteFile(payloadPath, []byte(oversized), 0o600); err != nil {
		t.Fatalf("write payload: %v", err)
	}
	var stdout bytes.Buffer
	var stderr bytes.Buffer

	code := run([]string{"--payload", payloadPath}, strings.NewReader(""), &stdout, &stderr)

	if code != pipe.ExitInvalidPayload {
		t.Fatalf("payload file exit code = %d, want %d", code, pipe.ExitInvalidPayload)
	}
	if got := stdout.String(); got != "" {
		t.Fatalf("oversized file stdout = %q, want empty", got)
	}
	if got := stderr.String(); !strings.Contains(got, "payload JSON exceeds maximum size") {
		t.Fatalf("oversized file stderr = %q, want size error", got)
	}
	if strings.Contains(stderr.String(), secret) || strings.Contains(stderr.String(), strings.Repeat("x", 64)) {
		t.Fatalf("oversized file error leaked payload body: %q", stderr.String())
	}
}

func TestPayloadFileRequiresAbsolutePath(t *testing.T) {
	var stdout bytes.Buffer
	var stderr bytes.Buffer

	code := run([]string{"--payload", "relative.json"}, strings.NewReader(""), &stdout, &stderr)

	if code != pipe.ExitInvalidPayload {
		t.Fatalf("relative payload exit code = %d, want %d", code, pipe.ExitInvalidPayload)
	}
	if got := stdout.String(); got != "" {
		t.Fatalf("relative payload stdout = %q, want empty", got)
	}
	if got := stderr.String(); got != "payload path must be absolute\n" {
		t.Fatalf("relative payload stderr = %q, want absolute-path error", got)
	}
}

func TestPayloadFileMissingPathIsInvalidPayload(t *testing.T) {
	payloadPath := filepath.Join(t.TempDir(), "missing.json")
	var stdout bytes.Buffer
	var stderr bytes.Buffer

	code := run([]string{"--payload", payloadPath}, strings.NewReader(""), &stdout, &stderr)

	if code != pipe.ExitInvalidPayload {
		t.Fatalf("missing payload exit code = %d, want %d", code, pipe.ExitInvalidPayload)
	}
	if got := stdout.String(); got != "" {
		t.Fatalf("missing payload stdout = %q, want empty", got)
	}
	if got := stderr.String(); !strings.HasPrefix(got, "read payload file: ") {
		t.Fatalf("missing payload stderr = %q, want read payload file prefix", got)
	}
}

func TestPayloadFlagRequiresPath(t *testing.T) {
	var stdout bytes.Buffer
	var stderr bytes.Buffer

	code := run([]string{"--payload"}, strings.NewReader(""), &stdout, &stderr)

	if code != pipe.ExitInvalidPayload {
		t.Fatalf("payload flag exit code = %d, want %d", code, pipe.ExitInvalidPayload)
	}
	if got := stdout.String(); got != "" {
		t.Fatalf("payload flag stdout = %q, want empty", got)
	}
	if got := stderr.String(); got != "unsupported invocation\n" {
		t.Fatalf("payload flag stderr = %q, want unsupported invocation newline", got)
	}
}

func TestGuardedMainRecoversPanicEmitsSingleFatalReport(t *testing.T) {
	var stdout bytes.Buffer
	var stderr bytes.Buffer

	code := guardedMainWithRunner(
		context.Background(),
		[]string{"--payload-stdin"},
		strings.NewReader("{}"),
		&stdout,
		&stderr,
		func(context.Context, []string, io.Reader, io.Writer, io.Writer) int {
			panic("secret panic detail")
		},
		runtimeguard.Options{ReportWriter: &stdout},
	)

	if code != pipe.ExitFatalSystemPanic {
		t.Fatalf("guarded main code = %d, want %d", code, pipe.ExitFatalSystemPanic)
	}
	report := decodeReport(t, stdout.Bytes())
	if report.Status != "FATAL_SYSTEM_PANIC" {
		t.Fatalf("status = %q, want FATAL_SYSTEM_PANIC", report.Status)
	}
	if report.ExitCode != pipe.ExitFatalSystemPanic {
		t.Fatalf("report exit_code = %d, want %d", report.ExitCode, pipe.ExitFatalSystemPanic)
	}
	if strings.Contains(stdout.String(), "secret") {
		t.Fatalf("fatal report leaked panic details: %s", stdout.String())
	}
	if strings.Count(strings.TrimSpace(stdout.String()), "\n") != 0 {
		t.Fatalf("stdout contains multiple JSON reports: %q", stdout.String())
	}
	if got := stderr.String(); got != "" {
		t.Fatalf("stderr = %q, want empty", got)
	}
}

func TestGuardedMainSignalSuppressesConcurrentNormalReport(t *testing.T) {
	var stdout bytes.Buffer
	var stderr bytes.Buffer
	signals := make(chan os.Signal, 1)
	releaseNormalWrite := make(chan struct{})
	var reaped atomic.Int32

	done := make(chan int, 1)
	go func() {
		done <- guardedMainWithRunner(
			context.Background(),
			[]string{"--payload-stdin"},
			strings.NewReader("{}"),
			&stdout,
			&stderr,
			func(_ context.Context, _ []string, _ io.Reader, stdout io.Writer, _ io.Writer) int {
				<-releaseNormalWrite
				_, _ = io.WriteString(stdout, "{\"status\":\"OK\",\"exit_code\":0}\n")
				return pipe.ExitSuccess
			},
			runtimeguard.Options{
				Signals: signals,
				ReapActive: func() error {
					reaped.Add(1)
					close(releaseNormalWrite)
					return nil
				},
			},
		)
	}()

	signals <- syscall.SIGTERM

	select {
	case code := <-done:
		if code != pipe.ExitFatalSystemPanic {
			t.Fatalf("guarded main code = %d, want %d", code, pipe.ExitFatalSystemPanic)
		}
	case <-time.After(time.Second):
		t.Fatal("guarded main did not return after injected signal")
	}
	if reaped.Load() != 1 {
		t.Fatalf("reap calls = %d, want 1", reaped.Load())
	}
	report := decodeReport(t, stdout.Bytes())
	if report.Status != "FATAL_SYSTEM_PANIC" {
		t.Fatalf("status = %q, want FATAL_SYSTEM_PANIC; stdout=%q", report.Status, stdout.String())
	}
	if strings.Count(strings.TrimSpace(stdout.String()), "\n") != 0 {
		t.Fatalf("stdout contains multiple JSON reports: %q", stdout.String())
	}
	if strings.Contains(stdout.String(), "\"OK\"") {
		t.Fatalf("stdout retained normal report after fatal signal: %q", stdout.String())
	}
	if got := stderr.String(); got != "" {
		t.Fatalf("stderr = %q, want empty", got)
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
