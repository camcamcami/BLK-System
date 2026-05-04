package validation

import (
	"context"
	"errors"
	"fmt"
	"strings"
	"time"

	"github.com/camcamcami/BLK-System/internal/execguard"
)

// CommandOutcome records the bounded execution result for one validation command.
type CommandOutcome struct {
	ExitCode    int
	OutputBytes int64
	TimedOut    bool
	Flooded     bool
}

// Result aggregates validation command logs and failure state. Logs are keyed by
// deterministic validation_NNN names in payload order.
type Result struct {
	Logs       map[string]string
	Outcomes   map[string]CommandOutcome
	HasFailure bool
}

// Run executes validation command strings sequentially in workdir using bounded
// execguard execution and a scrubbed deterministic environment. Command strings
// are interpreted exactly as payload-provided shell commands.
func Run(ctx context.Context, workdir string, commands []string, maxOutputBytes int64, timeout ...time.Duration) (Result, error) {
	if maxOutputBytes < 0 {
		return Result{}, errors.New("max output bytes must be non-negative")
	}
	perCommandTimeout := time.Duration(0)
	if len(timeout) > 0 {
		perCommandTimeout = timeout[0]
	}
	overallCtx := ctx
	var cancel context.CancelFunc
	if perCommandTimeout > 0 {
		overallCtx, cancel = context.WithTimeout(ctx, perCommandTimeout)
		defer cancel()
	}

	result := Result{
		Logs:     make(map[string]string, len(commands)),
		Outcomes: make(map[string]CommandOutcome, len(commands)),
	}
	remainingLogBytes := maxOutputBytes
	for i, command := range commands {
		if strings.TrimSpace(command) == "" {
			return result, fmt.Errorf("validation command %d is empty", i+1)
		}
		key := fmt.Sprintf("validation_%03d", i+1)
		if err := overallCtx.Err(); err != nil {
			if i == 0 {
				return result, err
			}
			result.Outcomes[key] = CommandOutcome{ExitCode: -1, TimedOut: true}
			result.HasFailure = true
			break
		}
		runResult, err := execguard.Run(overallCtx, execguard.Options{
			Workdir:        workdir,
			Command:        []string{"sh", "-c", command},
			Timeout:        perCommandTimeout,
			MaxOutputBytes: maxOutputBytes,
			Env:            execguard.ScrubbedEnv(workdir),
		})
		result.Logs[key] = string(retainOutputWithinBudget(runResult.Output, &remainingLogBytes))
		result.Outcomes[key] = CommandOutcome{
			ExitCode:    runResult.ExitCode,
			OutputBytes: runResult.OutputBytes,
			TimedOut:    runResult.TimedOut,
			Flooded:     runResult.Flooded,
		}
		if err != nil {
			if runResult.TimedOut || runResult.Flooded {
				result.HasFailure = true
				break
			}
			if overallCtx.Err() != nil {
				outcome := result.Outcomes[key]
				outcome.ExitCode = -1
				outcome.TimedOut = true
				result.Outcomes[key] = outcome
				result.HasFailure = true
				break
			}
			return result, fmt.Errorf("run validation command %s: %w", key, err)
		}
		if runResult.ExitCode != 0 || runResult.TimedOut || runResult.Flooded {
			result.HasFailure = true
			if runResult.TimedOut || runResult.Flooded {
				break
			}
		}
	}
	return result, nil
}

func retainOutputWithinBudget(output []byte, remaining *int64) []byte {
	if remaining == nil || *remaining <= 0 || len(output) == 0 {
		return nil
	}
	keep := int64(len(output))
	if keep > *remaining {
		keep = *remaining
	}
	*remaining -= keep
	if keep == 0 {
		return nil
	}
	return output[:keep]
}
