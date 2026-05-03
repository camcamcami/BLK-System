package gitguard

import (
	"context"
	"fmt"
	"strings"
	"time"

	"github.com/camcamcami/BLK-System/internal/execguard"
)

const (
	defaultGitTimeout        = 30 * time.Second
	defaultGitMaxOutputBytes = 4 * 1024 * 1024
)

// GitResult describes the bounded output from a Git command.
type GitResult struct {
	Stdout []byte
}

// RunGit runs git in repo with a short deterministic timeout, scrubbed Git/SSH
// environment, process-group cleanup, and bounded combined stdout/stderr output.
func RunGit(ctx context.Context, repo string, args ...string) (GitResult, error) {
	return runGit(ctx, repo, defaultGitMaxOutputBytes, nil, args...)
}

// RunGitWithLimit is RunGit with an explicit combined stdout/stderr output cap.
func RunGitWithLimit(ctx context.Context, repo string, maxOutputBytes int64, args ...string) (GitResult, error) {
	return runGit(ctx, repo, maxOutputBytes, nil, args...)
}

// RunGitWithEnv is RunGit with explicit environment entries appended after the
// scrubbed baseline. This is intended for narrowly scoped Git settings such as
// headless ls-remote SSH hardening.
func RunGitWithEnv(ctx context.Context, repo string, extraEnv []string, args ...string) (GitResult, error) {
	return runGit(ctx, repo, defaultGitMaxOutputBytes, extraEnv, args...)
}

func runGit(ctx context.Context, repo string, maxOutputBytes int64, extraEnv []string, args ...string) (GitResult, error) {
	if ctx == nil {
		ctx = context.Background()
	}
	if maxOutputBytes < 0 {
		return GitResult{}, fmt.Errorf("git %s in %q: max output bytes must be non-negative", strings.Join(args, " "), repo)
	}

	command := append([]string{"git"}, args...)
	result, err := execguard.Run(ctx, execguard.Options{
		Workdir:        repo,
		Command:        command,
		Timeout:        defaultGitTimeout,
		MaxOutputBytes: maxOutputBytes,
		Env:            execguard.ScrubbedEnv(repo, extraEnv...),
	})
	gitResult := GitResult{Stdout: result.Output}
	if err != nil {
		return gitResult, fmt.Errorf("git %s in %q: infrastructure error: %w", strings.Join(args, " "), repo, err)
	}
	if result.Flooded {
		return gitResult, fmt.Errorf("git %s in %q: infrastructure error: output exceeded max output bytes (%d > %d)", strings.Join(args, " "), repo, result.OutputBytes, maxOutputBytes)
	}
	if result.TimedOut {
		return gitResult, fmt.Errorf("git %s in %q: infrastructure error: timed out", strings.Join(args, " "), repo)
	}
	if result.ExitCode != 0 {
		if msg := strings.TrimSpace(string(result.Output)); msg != "" {
			return gitResult, fmt.Errorf("git %s in %q exited with code %d: %s", strings.Join(args, " "), repo, result.ExitCode, msg)
		}
		return gitResult, fmt.Errorf("git %s in %q exited with code %d", strings.Join(args, " "), repo, result.ExitCode)
	}
	return gitResult, nil
}
