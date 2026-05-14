package validation

import (
	"context"
	"errors"
	"fmt"
	"strings"
	"time"

	"github.com/camcamcami/BLK-System/internal/execguard"
	"github.com/camcamcami/BLK-System/internal/validationprofiles"
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

type commandPlan struct {
	Argv []string
	Env  []string
}

// Run executes legacy trusted-local validation command strings sequentially in
// workdir using bounded execguard execution and a scrubbed deterministic
// environment. Legacy command strings are interpreted as shell commands and must
// remain a trusted-local compatibility path, not the repository-profile path.
func Run(ctx context.Context, workdir string, commands []string, maxOutputBytes int64, timeout ...time.Duration) (Result, error) {
	return runPlanned(ctx, workdir, len(commands), maxOutputBytes, timeout, func(i int) (commandPlan, error) {
		command := commands[i]
		if strings.TrimSpace(command) == "" {
			return commandPlan{}, fmt.Errorf("validation command %d is empty", i+1)
		}
		return commandPlan{Argv: []string{"sh", "-c", command}}, nil
	})
}

// RunSpecs executes repository-owned structured validation profile specs without
// shell interpretation. Each CommandSpec argv is passed directly to execguard;
// profile Env entries are appended to the scrubbed deterministic environment.
func RunSpecs(ctx context.Context, workdir string, specs []validationprofiles.CommandSpec, maxOutputBytes int64, timeout ...time.Duration) (Result, error) {
	return runPlanned(ctx, workdir, len(specs), maxOutputBytes, timeout, func(i int) (commandPlan, error) {
		spec := specs[i]
		if len(spec.Argv) == 0 {
			return commandPlan{}, fmt.Errorf("validation profile command %d has empty argv", i+1)
		}
		argv := append([]string{}, spec.Argv...)
		for j, arg := range argv {
			if strings.TrimSpace(arg) == "" {
				return commandPlan{}, fmt.Errorf("validation profile command %d argv[%d] is empty", i+1, j)
			}
		}
		if len(argv) >= 2 && argv[0] == "sh" && argv[1] == "-c" {
			return commandPlan{}, fmt.Errorf("validation profile command %d must not use sh -c shell wrapper", i+1)
		}
		return commandPlan{Argv: argv, Env: append([]string{}, spec.Env...)}, nil
	})
}

func runPlanned(
	ctx context.Context,
	workdir string,
	count int,
	maxOutputBytes int64,
	timeout []time.Duration,
	planCommand func(int) (commandPlan, error),
) (Result, error) {
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
		Logs:     make(map[string]string, count),
		Outcomes: make(map[string]CommandOutcome, count),
	}
	remainingLogBytes := maxOutputBytes
	for i := 0; i < count; i++ {
		key := fmt.Sprintf("validation_%03d", i+1)
		if err := overallCtx.Err(); err != nil {
			if i == 0 {
				return result, err
			}
			result.Outcomes[key] = CommandOutcome{ExitCode: -1, TimedOut: true}
			result.HasFailure = true
			break
		}
		planned, err := planCommand(i)
		if err != nil {
			return result, err
		}
		runResult, err := execguard.Run(overallCtx, execguard.Options{
			Workdir:        workdir,
			Command:        planned.Argv,
			Timeout:        perCommandTimeout,
			MaxOutputBytes: maxOutputBytes,
			Env:            execguard.ScrubbedEnv(workdir, planned.Env...),
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
