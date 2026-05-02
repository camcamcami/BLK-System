package main

import (
	"fmt"
	"io"
	"os"

	"github.com/camcamcami/BLK-System/internal/pipe"
)

func main() {
	os.Exit(run(os.Args[1:], os.Stdout, os.Stderr))
}

func run(args []string, stdout io.Writer, stderr io.Writer) int {
	if len(args) == 1 && args[0] == "--health" {
		fmt.Fprintln(stdout, "{\"status\":\"OK\",\"component\":\"blk-pipe\"}")
		return pipe.ExitSuccess
	}

	fmt.Fprintln(stderr, "unsupported invocation")
	return pipe.ExitInvalidPayload
}
