package main

import (
	"bytes"
	"testing"
)

func TestRunHealthPrintsDeterministicJSON(t *testing.T) {
	var stdout bytes.Buffer
	var stderr bytes.Buffer

	code := run([]string{"--health"}, &stdout, &stderr)

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

	code := run([]string{}, &stdout, &stderr)

	if code == 0 {
		t.Fatal("unsupported invocation exit code = 0, want non-zero")
	}
	if got := stdout.String(); got != "" {
		t.Fatalf("unsupported invocation stdout = %q, want empty", got)
	}
}
