package engine

import (
	"context"
	"errors"
	"fmt"

	"github.com/camcamcami/BLK-System/internal/execguard"
)

// Result describes the bounded execution outcome for a local engine command.
type Result struct {
	ExitCode    int
	Output      []byte
	OutputBytes int64
	TimedOut    bool
	Flooded     bool
}

// Run executes command in workdir while bounding combined stdout/stderr bytes.
func Run(ctx context.Context, workdir string, command []string, maxOutputBytes int64) (Result, error) {
	if len(command) == 0 {
		return Result{}, errors.New("engine command is empty")
	}
	if maxOutputBytes < 0 {
		return Result{}, errors.New("max output bytes must be non-negative")
	}

	result, err := execguard.Run(ctx, execguard.Options{
		Workdir:        workdir,
		Command:        command,
		MaxOutputBytes: maxOutputBytes,
		Env:            execguard.ScrubbedEnv(workdir),
	})
	engineResult := Result{
		ExitCode:    result.ExitCode,
		Output:      result.Output,
		OutputBytes: result.OutputBytes,
		TimedOut:    result.TimedOut,
		Flooded:     result.Flooded,
	}
	if err != nil {
		return engineResult, fmt.Errorf("run engine command: %w", err)
	}
	return engineResult, nil
}
