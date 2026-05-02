package main

import (
	"context"
	"fmt"
	"io"
	"os"

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

	fmt.Fprintln(stderr, "unsupported invocation")
	return pipe.ExitInvalidPayload
}
