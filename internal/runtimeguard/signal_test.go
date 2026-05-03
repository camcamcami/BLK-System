//go:build linux || darwin

package runtimeguard

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"os"
	"strings"
	"sync/atomic"
	"syscall"
	"testing"
	"time"

	"github.com/camcamcami/BLK-System/internal/contracts"
	"github.com/camcamcami/BLK-System/internal/pipe"
)

func TestRunRecoversPanicEmitsSingleSterileFatalReport(t *testing.T) {
	var stdout bytes.Buffer
	var reaped atomic.Int32

	code := Run(context.Background(), Options{
		ReportWriter: &stdout,
		ReapActive: func() error {
			reaped.Add(1)
			return nil
		},
	}, func(context.Context) int {
		panic("secret token /tmp/private/path")
	})

	if code != pipe.ExitFatalSystemPanic {
		t.Fatalf("exit code = %d, want %d", code, pipe.ExitFatalSystemPanic)
	}
	if reaped.Load() != 1 {
		t.Fatalf("reap calls = %d, want 1", reaped.Load())
	}
	report := decodeFatalReport(t, stdout.Bytes())
	if report.Status != "FATAL_SYSTEM_PANIC" {
		t.Fatalf("status = %q, want FATAL_SYSTEM_PANIC", report.Status)
	}
	if report.ExitCode != pipe.ExitFatalSystemPanic {
		t.Fatalf("report exit_code = %d, want %d", report.ExitCode, pipe.ExitFatalSystemPanic)
	}
	if report.Error == "" {
		t.Fatalf("fatal report error is empty")
	}
	if strings.Contains(stdout.String(), "secret") || strings.Contains(stdout.String(), "/tmp/private/path") {
		t.Fatalf("fatal report leaked panic details: %s", stdout.String())
	}
	assertSingleJSONReport(t, stdout.String())
}

func TestRunHandlesInjectedSignalOnceAndExitsOne(t *testing.T) {
	var stdout bytes.Buffer
	signals := make(chan os.Signal, 2)
	releaseRun := make(chan struct{})
	var reaped atomic.Int32

	done := make(chan int, 1)
	go func() {
		done <- Run(context.Background(), Options{
			ReportWriter: &stdout,
			Signals:      signals,
			ReapActive: func() error {
				reaped.Add(1)
				close(releaseRun)
				return nil
			},
		}, func(context.Context) int {
			<-releaseRun
			return pipe.ExitSuccess
		})
	}()

	signals <- syscall.SIGTERM
	signals <- syscall.SIGINT

	select {
	case code := <-done:
		if code != pipe.ExitFatalSystemPanic {
			t.Fatalf("Run returned %d, want %d", code, pipe.ExitFatalSystemPanic)
		}
	case <-time.After(time.Second):
		t.Fatal("Run did not return after injected signal")
	}
	if reaped.Load() != 1 {
		t.Fatalf("reap calls = %d, want 1", reaped.Load())
	}
	report := decodeFatalReport(t, stdout.Bytes())
	if report.Status != "FATAL_SYSTEM_PANIC" {
		t.Fatalf("status = %q, want FATAL_SYSTEM_PANIC", report.Status)
	}
	if !strings.Contains(report.Error, "signal") {
		t.Fatalf("error = %q, want sanitized signal message", report.Error)
	}
	assertSingleJSONReport(t, stdout.String())
}

func TestRunSignalDropsNormalReportWrittenAfterFatalBegins(t *testing.T) {
	var stdout bytes.Buffer
	signals := make(chan os.Signal, 1)
	releaseNormalWrite := make(chan struct{})
	gate := NewReportGate(&stdout)

	done := make(chan int, 1)
	go func() {
		done <- Run(context.Background(), Options{
			ReportWriter: &stdout,
			ReportGate:   gate,
			Signals:      signals,
			ReapActive: func() error {
				close(releaseNormalWrite)
				return nil
			},
		}, func(context.Context) int {
			<-releaseNormalWrite
			_, _ = gate.Write([]byte("{\"status\":\"OK\",\"exit_code\":0}\n"))
			return pipe.ExitSuccess
		})
	}()

	signals <- syscall.SIGTERM

	select {
	case code := <-done:
		if code != pipe.ExitFatalSystemPanic {
			t.Fatalf("Run returned %d, want %d", code, pipe.ExitFatalSystemPanic)
		}
	case <-time.After(time.Second):
		t.Fatal("Run did not return after injected signal")
	}
	if strings.Contains(stdout.String(), "\"OK\"") {
		t.Fatalf("normal report escaped fatal gate: %q", stdout.String())
	}
	report := decodeFatalReport(t, stdout.Bytes())
	if report.Status != "FATAL_SYSTEM_PANIC" {
		t.Fatalf("status = %q, want FATAL_SYSTEM_PANIC", report.Status)
	}
	assertSingleJSONReport(t, stdout.String())
}

func TestRunStopsSignalNotificationBeforeNormalFlush(t *testing.T) {
	var stopped atomic.Bool
	gate := NewReportGate(stopAwareWriter{stopped: &stopped})

	code := Run(context.Background(), Options{
		ReportGate: gate,
		Notify:     func(chan<- os.Signal, ...os.Signal) {},
		Stop: func(chan<- os.Signal) {
			stopped.Store(true)
		},
	}, func(context.Context) int {
		_, _ = gate.Write([]byte("{\"status\":\"OK\",\"exit_code\":0}\n"))
		return pipe.ExitSuccess
	})

	if code != pipe.ExitSuccess {
		t.Fatalf("Run returned %d, want %d after stopping signals before normal flush", code, pipe.ExitSuccess)
	}
	if !stopped.Load() {
		t.Fatalf("signal notification was not stopped")
	}
}

type stopAwareWriter struct {
	stopped *atomic.Bool
}

func (w stopAwareWriter) Write(p []byte) (int, error) {
	if !w.stopped.Load() {
		return 0, errors.New("normal flush happened while runtimeguard still owned signal notification")
	}
	return len(p), nil
}

func decodeFatalReport(t *testing.T, data []byte) contracts.Report {
	t.Helper()
	var report contracts.Report
	if err := json.Unmarshal(data, &report); err != nil {
		t.Fatalf("decode fatal report %q: %v", data, err)
	}
	return report
}

func assertSingleJSONReport(t *testing.T, output string) {
	t.Helper()
	trimmed := strings.TrimSpace(output)
	if trimmed == "" {
		t.Fatalf("empty JSON output")
	}
	if strings.Count(trimmed, "\n") != 0 {
		t.Fatalf("output contains multiple lines/reports: %q", output)
	}
}
