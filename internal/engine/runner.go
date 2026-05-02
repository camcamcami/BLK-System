package engine

import (
	"context"
	"errors"
	"fmt"
	"io"
	"os"
	"os/exec"
	"sync"
	"sync/atomic"
	"syscall"
)

// Result describes the bounded execution outcome for a local engine command.
type Result struct {
	ExitCode    int
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

	cmd := exec.CommandContext(ctx, command[0], command[1:]...)
	cmd.Dir = workdir
	cmd.SysProcAttr = &syscall.SysProcAttr{Setpgid: true}
	cmd.Cancel = func() error {
		return killProcessGroup(cmd)
	}

	reader, writer, err := os.Pipe()
	if err != nil {
		return Result{}, fmt.Errorf("create output pipe: %w", err)
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

	readDone := make(chan error, 1)
	go func() {
		readDone <- countOutput(reader, maxOutputBytes, &outputBytes, markFlooded)
	}()

	if err := cmd.Start(); err != nil {
		_ = writer.Close()
		_ = reader.Close()
		<-readDone
		return Result{}, fmt.Errorf("start engine command: %w", err)
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
	// Kill the command's process group after the direct process exits so output
	// draining cannot wait forever on orphaned pipe writers.
	_ = killProcessGroup(cmd)
	close(waitDone)

	result := Result{
		ExitCode:    -1,
		OutputBytes: outputBytes.Load(),
		TimedOut:    ctx.Err() != nil,
		Flooded:     flooded.Load(),
	}
	if cmd.ProcessState != nil {
		result.ExitCode = cmd.ProcessState.ExitCode()
	}

	if result.TimedOut || result.Flooded {
		_ = reader.Close()
	}
	if readErr := <-readDone; readErr != nil && !errors.Is(readErr, os.ErrClosed) {
		return result, fmt.Errorf("read engine output: %w", readErr)
	}
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

	return result, fmt.Errorf("wait for engine command: %w", waitErr)
}

func countOutput(reader io.Reader, maxOutputBytes int64, outputBytes *atomic.Int64, markFlooded func()) error {
	buf := make([]byte, 32*1024)
	for {
		n, err := reader.Read(buf)
		if n > 0 {
			if outputBytes.Add(int64(n)) > maxOutputBytes {
				markFlooded()
			}
		}
		if err != nil {
			if errors.Is(err, io.EOF) {
				return nil
			}
			return err
		}
	}
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
