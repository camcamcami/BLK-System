package main

import (
	"context"
	"fmt"
	"io"
	"os"
	"path/filepath"

	"github.com/camcamcami/BLK-System/internal/pipe"
)

func main() {
	os.Exit(run(os.Args[1:], os.Stdin, os.Stdout, os.Stderr))
}

func run(args []string, stdin io.Reader, stdout io.Writer, stderr io.Writer) int {
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
		return pipe.Run(context.Background(), payloadJSON, stdout)
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
		return pipe.Run(context.Background(), payloadJSON, stdout)
	}

	fmt.Fprintln(stderr, "unsupported invocation")
	return pipe.ExitInvalidPayload
}
