//go:build linux || darwin

package execguard

import (
	"context"
	"errors"
	"fmt"
	"io"
	"os"
	"os/exec"
	"sort"
	"strings"
	"sync"
	"sync/atomic"
	"syscall"
	"time"
)

// CommandResult describes the bounded execution outcome for a command.
type CommandResult struct {
	ExitCode    int
	Output      []byte
	OutputBytes int64
	TimedOut    bool
	Flooded     bool
}

// Options controls bounded command execution.
type Options struct {
	Workdir        string
	Command        []string
	Timeout        time.Duration
	MaxOutputBytes int64
	Env            []string
}

type outputRead struct {
	output []byte
	err    error
}

// Run executes opts.Command in opts.Workdir, capturing combined stdout/stderr up
// to opts.MaxOutputBytes while counting total observed bytes. Runtime is bounded
// by ctx and, when set, opts.Timeout. Timeout/flood cancellation kills the whole
// POSIX process group.
//
// On an otherwise successful/direct command exit, Run waits for inherited
// stdout/stderr pipes to close before returning. That prevents descendants that
// escaped the original process group with inherited output FDs from mutating the
// worktree while callers proceed to cleanup/staging. Portable POSIX process
// groups cannot contain a descendant that both escapes and closes or redirects
// those FDs; timeout, flood, or context cancellation can also force Run to return
// before such descendants exit.
func Run(ctx context.Context, opts Options) (CommandResult, error) {
	if len(opts.Command) == 0 {
		return CommandResult{ExitCode: -1}, errors.New("command is empty")
	}
	if opts.MaxOutputBytes < 0 {
		return CommandResult{ExitCode: -1}, errors.New("max output bytes must be non-negative")
	}

	runCtx := ctx
	var cancel context.CancelFunc
	if opts.Timeout > 0 {
		runCtx, cancel = context.WithTimeout(ctx, opts.Timeout)
		defer cancel()
	}

	cmd := exec.CommandContext(runCtx, opts.Command[0], opts.Command[1:]...)
	cmd.Dir = opts.Workdir
	if opts.Env != nil {
		cmd.Env = opts.Env
	}
	cmd.SysProcAttr = &syscall.SysProcAttr{Setpgid: true}
	cmd.Cancel = func() error {
		return killProcessGroup(cmd)
	}

	reader, writer, err := os.Pipe()
	if err != nil {
		return CommandResult{ExitCode: -1}, fmt.Errorf("create output pipe: %w", err)
	}
	defer reader.Close()
	cmd.Stdout = writer
	cmd.Stderr = writer

	var outputBytes atomic.Int64
	var flooded atomic.Bool
	floodCh := make(chan struct{})
	var floodOnce sync.Once
	markFlooded := func() {
		floodOnce.Do(func() {
			flooded.Store(true)
			close(floodCh)
		})
	}

	readDone := make(chan outputRead, 1)
	go func() {
		output, err := captureOutput(reader, opts.MaxOutputBytes, &outputBytes, markFlooded)
		readDone <- outputRead{output: output, err: err}
	}()

	if err := cmd.Start(); err != nil {
		_ = writer.Close()
		_ = reader.Close()
		<-readDone
		return CommandResult{ExitCode: -1}, fmt.Errorf("start command: %w", err)
	}
	_ = writer.Close()

	waitDone := make(chan struct{})
	go func() {
		select {
		case <-floodCh:
			_ = killProcessGroup(cmd)
		case <-waitDone:
		}
	}()

	waitErr := cmd.Wait()
	// A shell can exit while children keep inherited stdout/stderr pipe FDs open.
	// Kill the command's process group after the direct process exits so same-pgid
	// background writers are reaped before the final output drain. Descendants that
	// escaped the group are handled by waiting for pipe EOF, bounded only by
	// context timeout/cancellation or output flood.
	_ = killProcessGroup(cmd)
	close(waitDone)

	result := CommandResult{
		ExitCode:    -1,
		OutputBytes: outputBytes.Load(),
		TimedOut:    runCtx.Err() != nil,
		Flooded:     flooded.Load(),
	}
	if cmd.ProcessState != nil {
		result.ExitCode = cmd.ProcessState.ExitCode()
	}

	readResult := waitForOutputDrain(readDone, reader, drainControl{
		closeImmediately: result.TimedOut || result.Flooded,
		ctxDone:          runCtx.Done(),
		floodCh:          floodCh,
	})
	if runCtx.Err() != nil {
		result.TimedOut = true
	}
	if readResult.err != nil && !errors.Is(readResult.err, os.ErrClosed) {
		return result, fmt.Errorf("read command output: %w", readResult.err)
	}
	result.Output = readResult.output
	result.OutputBytes = outputBytes.Load()
	result.Flooded = flooded.Load()

	if waitErr == nil {
		return result, nil
	}
	var exitErr *exec.ExitError
	if errors.As(waitErr, &exitErr) {
		return result, nil
	}
	if result.TimedOut || result.Flooded {
		return result, nil
	}

	return result, fmt.Errorf("wait for command: %w", waitErr)
}

type drainControl struct {
	closeImmediately bool
	ctxDone          <-chan struct{}
	floodCh          <-chan struct{}
}

func waitForOutputDrain(readDone <-chan outputRead, reader io.Closer, control drainControl) outputRead {
	if control.closeImmediately {
		_ = reader.Close()
		return <-readDone
	}

	select {
	case readResult := <-readDone:
		return readResult
	case <-control.ctxDone:
		_ = reader.Close()
		return <-readDone
	case <-control.floodCh:
		_ = reader.Close()
		return <-readDone
	}
}

// ScrubbedEnv returns a deterministic process environment with dangerous Git and
// SSH agent state removed. Additional entries are appended after the fixed
// baseline so callers can explicitly opt into narrowly scoped settings.
func ScrubbedEnv(workdir string, extra ...string) []string {
	inherited := make(map[string]string)
	for _, entry := range os.Environ() {
		key, _, ok := strings.Cut(entry, "=")
		if !ok || shouldScrubInherited(key) {
			continue
		}
		inherited[key] = entry
	}

	keys := make([]string, 0, len(inherited))
	for key := range inherited {
		keys = append(keys, key)
	}
	sort.Strings(keys)

	env := make([]string, 0, len(keys)+3+len(extra))
	for _, key := range keys {
		env = append(env, inherited[key])
	}
	env = append(env,
		"GIT_CONFIG_GLOBAL="+os.DevNull,
		"GIT_CONFIG_NOSYSTEM=1",
		"PWD="+workdir,
	)
	return append(env, extra...)
}

func shouldScrubInherited(key string) bool {
	if strings.HasPrefix(key, "GIT_") || key == "PWD" {
		return true
	}
	switch key {
	case "SSH_AUTH_SOCK", "SSH_AGENT_PID", "SSH_ASKPASS":
		return true
	default:
		return false
	}
}

func captureOutput(reader io.Reader, maxOutputBytes int64, outputBytes *atomic.Int64, markFlooded func()) ([]byte, error) {
	retained := make([]byte, 0, retainedOutputCapacity(maxOutputBytes))
	buf := make([]byte, 32*1024)
	for {
		n, err := reader.Read(buf)
		if n > 0 {
			newTotal := outputBytes.Add(int64(n))
			if int64(len(retained)) < maxOutputBytes {
				remaining := int(maxOutputBytes - int64(len(retained)))
				toKeep := n
				if toKeep > remaining {
					toKeep = remaining
				}
				retained = append(retained, buf[:toKeep]...)
			}
			if newTotal > maxOutputBytes {
				markFlooded()
			}
		}
		if err != nil {
			if errors.Is(err, io.EOF) {
				return retained, nil
			}
			return retained, err
		}
	}
}

func retainedOutputCapacity(maxOutputBytes int64) int {
	if maxOutputBytes <= 0 {
		return 0
	}
	const defaultCapacity = 32 * 1024
	if maxOutputBytes < defaultCapacity {
		return int(maxOutputBytes)
	}
	return defaultCapacity
}

func killProcessGroup(cmd *exec.Cmd) error {
	if cmd.Process == nil {
		return os.ErrProcessDone
	}
	err := syscall.Kill(-cmd.Process.Pid, syscall.SIGKILL)
	if errors.Is(err, syscall.ESRCH) {
		return os.ErrProcessDone
	}
	return err
}
