//go:build linux || darwin

package main

import (
	"context"
	"fmt"
	"io"
	"os"
	"path/filepath"

	"github.com/camcamcami/BLK-System/internal/execguard"
	"github.com/camcamcami/BLK-System/internal/pipe"
	"github.com/camcamcami/BLK-System/internal/runtimeguard"
)

type pipeRunner func(context.Context, []string, io.Reader, io.Writer, io.Writer) int

func main() {
	os.Exit(guardedMain(context.Background(), os.Args[1:], os.Stdin, os.Stdout, os.Stderr))
}

func guardedMain(ctx context.Context, args []string, stdin io.Reader, stdout io.Writer, stderr io.Writer) int {
	return guardedMainWithRunner(ctx, args, stdin, stdout, stderr, runWithContext, runtimeguard.Options{})
}

func guardedMainWithRunner(ctx context.Context, args []string, stdin io.Reader, stdout io.Writer, stderr io.Writer, runner pipeRunner, guard runtimeguard.Options) int {
	if guard.ReportWriter == nil {
		guard.ReportWriter = stdout
	}
	if guard.ReportGate == nil {
		guard.ReportGate = runtimeguard.NewReportGate(guard.ReportWriter)
	}
	if guard.ReapActive == nil {
		guard.ReapActive = func() error {
			_, err := execguard.KillActiveProcessGroups()
			return err
		}
	}
	return runtimeguard.Run(ctx, guard, func(runCtx context.Context) int {
		return runner(runCtx, args, stdin, guard.ReportGate, stderr)
	})
}

func run(args []string, stdin io.Reader, stdout io.Writer, stderr io.Writer) int {
	return runWithContext(context.Background(), args, stdin, stdout, stderr)
}

func runWithContext(ctx context.Context, args []string, stdin io.Reader, stdout io.Writer, stderr io.Writer) int {
	if len(args) == 1 && args[0] == "--health" {
		fmt.Fprintln(stdout, "{\"status\":\"OK\",\"component\":\"blk-pipe\"}")
		return pipe.ExitSuccess
	}
	if len(args) == 1 && args[0] == "--payload-stdin" {
		payloadJSON, err := io.ReadAll(stdin)
		if err != nil {
			fmt.Fprintf(stderr, "read payload stdin: %v\n", err)
			return pipe.ExitInternalError
		}
		return pipe.Run(ctx, payloadJSON, stdout)
	}
	if len(args) == 2 && args[0] == "--payload" {
		if !filepath.IsAbs(args[1]) {
			fmt.Fprintln(stderr, "payload path must be absolute")
			return pipe.ExitInvalidPayload
		}
		payloadJSON, err := os.ReadFile(args[1])
		if err != nil {
			fmt.Fprintf(stderr, "read payload file: %v\n", err)
			return pipe.ExitInvalidPayload
		}
		return pipe.Run(ctx, payloadJSON, stdout)
	}

	fmt.Fprintln(stderr, "unsupported invocation")
	return pipe.ExitInvalidPayload
}
