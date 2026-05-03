//go:build linux || darwin

package runtimeguard

import (
	"bytes"
	"context"
	"encoding/json"
	"io"
	"os"
	"os/signal"
	"sync"
	"syscall"
	"time"

	"github.com/camcamcami/BLK-System/internal/contracts"
	"github.com/camcamcami/BLK-System/internal/pipe"
)

const defaultFatalWait = 2 * time.Second

// ReportGate serializes normal blk-pipe report output against fatal-system
// output. Normal writes are buffered until Run knows no fatal condition won; a
// fatal signal/panic discards any buffered normal output before writing the one
// sterile fatal report. The buffer is intended for blk-pipe's single bounded JSON
// report; callers should not stream unbounded data through ReportGate.
type ReportGate struct {
	mu           sync.Mutex
	sink         io.Writer
	normal       bytes.Buffer
	fatal        bool
	fatalWritten bool
	flushed      bool
}

// NewReportGate returns a gate that eventually writes to sink.
func NewReportGate(sink io.Writer) *ReportGate {
	if sink == nil {
		sink = io.Discard
	}
	return &ReportGate{sink: sink}
}

// Write buffers normal report output until FlushNormal. Once fatal handling has
// begun, normal output is acknowledged and dropped.
func (g *ReportGate) Write(p []byte) (int, error) {
	g.mu.Lock()
	defer g.mu.Unlock()
	if g.fatal {
		return len(p), nil
	}
	if g.flushed {
		_, err := g.sink.Write(p)
		if err != nil {
			return 0, err
		}
		return len(p), nil
	}
	_, err := g.normal.Write(p)
	if err != nil {
		return 0, err
	}
	return len(p), nil
}

// BeginFatal suppresses future normal writes and discards buffered normal
// output. It does not write the fatal report.
func (g *ReportGate) BeginFatal() {
	g.mu.Lock()
	defer g.mu.Unlock()
	if g.fatal {
		return
	}
	g.fatal = true
	g.normal.Reset()
}

// FlushNormal releases buffered normal output if no fatal condition won.
func (g *ReportGate) FlushNormal() error {
	g.mu.Lock()
	defer g.mu.Unlock()
	if g.fatal || g.flushed {
		return nil
	}
	g.flushed = true
	if g.normal.Len() == 0 {
		return nil
	}
	_, err := g.sink.Write(g.normal.Bytes())
	return err
}

// WriteFatal writes the one sterile fatal report, discarding any normal output.
func (g *ReportGate) WriteFatal(message string) error {
	g.mu.Lock()
	defer g.mu.Unlock()
	if g.fatalWritten {
		return nil
	}
	g.fatal = true
	g.fatalWritten = true
	g.normal.Reset()
	return writeFatalReport(g.sink, message)
}

// Options provides seams for fatal-system handling without forcing tests to use
// process-global signal handlers or os.Exit.
type Options struct {
	ReportWriter io.Writer
	ReportGate   *ReportGate
	Signals      <-chan os.Signal
	Notify       func(chan<- os.Signal, ...os.Signal)
	Stop         func(chan<- os.Signal)
	ReapActive   func() error
	FatalWait    time.Duration
}

// Run executes runner behind the blk-pipe fatal-system guard. Panics and
// SIGINT/SIGTERM produce one sterile JSON report, reap active process groups,
// and return code 1. Signal handling is coordinated in-process so active
// execguard commands can observe cancellation, kill/reap children, and finish
// their Wait paths before Run returns.
func Run(ctx context.Context, opts Options, runner func(context.Context) int) int {
	opts = normalizeOptions(opts)

	runCtx, cancel := context.WithCancel(ctx)
	defer cancel()

	signalCh, stopSignals := signalSource(opts)
	defer stopSignals()

	runDone := make(chan runOutcome, 1)
	go func() {
		outcome := runOutcome{}
		defer func() {
			if recovered := recover(); recovered != nil {
				outcome.panicked = true
				outcome.code = pipe.ExitFatalSystemPanic
			}
			runDone <- outcome
		}()
		outcome.code = runner(runCtx)
	}()

	select {
	case <-signalCh:
		return handleFatalSignal(opts, cancel, runDone)
	case outcome := <-runDone:
		if signalPending(signalCh) {
			return handleFatalSignalAfterRunnerDone(opts, cancel)
		}
		if outcome.panicked {
			return handleFatalPanic(opts, cancel)
		}
		stopSignals()
		if signalPending(signalCh) {
			return handleFatalSignalAfterRunnerDone(opts, cancel)
		}
		if err := opts.ReportGate.FlushNormal(); err != nil {
			return pipe.ExitInternalError
		}
		return outcome.code
	}
}

type runOutcome struct {
	code     int
	panicked bool
}

func handleFatalSignal(opts Options, cancel context.CancelFunc, runDone <-chan runOutcome) int {
	cancel()
	opts.ReportGate.BeginFatal()
	_ = opts.ReapActive()
	waitForRunner(runDone, opts.FatalWait)
	_ = opts.ReportGate.WriteFatal("fatal signal received")
	return pipe.ExitFatalSystemPanic
}

func handleFatalSignalAfterRunnerDone(opts Options, cancel context.CancelFunc) int {
	cancel()
	opts.ReportGate.BeginFatal()
	_ = opts.ReapActive()
	_ = opts.ReportGate.WriteFatal("fatal signal received")
	return pipe.ExitFatalSystemPanic
}

func handleFatalPanic(opts Options, cancel context.CancelFunc) int {
	cancel()
	opts.ReportGate.BeginFatal()
	_ = opts.ReapActive()
	_ = opts.ReportGate.WriteFatal("fatal system panic")
	return pipe.ExitFatalSystemPanic
}

func signalPending(signalCh <-chan os.Signal) bool {
	select {
	case _, ok := <-signalCh:
		return ok
	default:
		return false
	}
}

func waitForRunner(runDone <-chan runOutcome, timeout time.Duration) {
	if timeout <= 0 {
		select {
		case <-runDone:
		default:
		}
		return
	}
	select {
	case <-runDone:
	case <-time.After(timeout):
	}
}

func normalizeOptions(opts Options) Options {
	if opts.ReportWriter == nil {
		opts.ReportWriter = io.Discard
	}
	if opts.ReportGate == nil {
		opts.ReportGate = NewReportGate(opts.ReportWriter)
	}
	if opts.Notify == nil {
		opts.Notify = signal.Notify
	}
	if opts.Stop == nil {
		opts.Stop = signal.Stop
	}
	if opts.ReapActive == nil {
		opts.ReapActive = func() error { return nil }
	}
	if opts.FatalWait == 0 {
		opts.FatalWait = defaultFatalWait
	}
	return opts
}

// signalSource installs SIGINT/SIGTERM notification for Run and returns an
// idempotent stop function. Stopping before a normal flush restores default OS
// signal behavior for any SIGINT/SIGTERM that arrives while the output sink is
// blocked; closing the channel preserves any already queued signal for a final
// nonblocking check.
func signalSource(opts Options) (<-chan os.Signal, func()) {
	if opts.Signals != nil {
		return opts.Signals, func() {}
	}
	signalCh := make(chan os.Signal, 1)
	opts.Notify(signalCh, syscall.SIGINT, syscall.SIGTERM)
	var once sync.Once
	return signalCh, func() {
		once.Do(func() {
			opts.Stop(signalCh)
			close(signalCh)
		})
	}
}

func writeFatalReport(writer io.Writer, message string) error {
	report := contracts.NewReport()
	report.Status = "FATAL_SYSTEM_PANIC"
	report.ExitCode = pipe.ExitFatalSystemPanic
	report.Error = message
	return json.NewEncoder(writer).Encode(report)
}
