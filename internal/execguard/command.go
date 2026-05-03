//go:build linux || darwin

package execguard

import (
	"context"
	"errors"
	"fmt"
	"io"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"sort"
	"strconv"
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

const activeReapWait = 2 * time.Second

type activeCommand struct {
	rootPID    int
	pgid       int
	pipeID     string
	directLive bool
	done       chan struct{}
}

var activeProcessGroups = struct {
	sync.Mutex
	nextID   atomic.Int64
	commands map[int64]*activeCommand
}{commands: map[int64]*activeCommand{}}

// KillActiveProcessGroups sends SIGKILL to every process group, visible
// descendant, and inherited-output pipe holder currently owned by execguard.Run.
// It then waits briefly for active Run calls to finish their cmd.Wait/output-drain
// paths, providing the fatal-system kill/reap behavior without os.Exit racing
// ahead of Wait. It is safe to call concurrently with Run.
func KillActiveProcessGroups() (int, error) {
	return killActiveProcessGroups(true)
}

func killActiveProcessGroups(waitForActive bool) (int, error) {
	commands := activeCommandSnapshot()
	if len(commands) == 0 {
		return 0, nil
	}

	processes := processSnapshot()
	ownPID := os.Getpid()
	ownPGID := syscall.Getpgrp()
	targets := activeCleanupTargets(commands, processes, pipeHolderPIDs, ownPID)
	groups := targets.groups
	pids := targets.pids
	for pid := range pids {
		if info, ok := processes[pid]; ok && info.pgid > 0 {
			groups[info.pgid] = struct{}{}
			continue
		}
		if pgid, err := syscall.Getpgid(pid); err == nil && pgid > 0 {
			groups[pgid] = struct{}{}
		}
	}

	killed := 0
	var errs []error
	for _, pgid := range sortedKeys(groups) {
		if pgid == 0 || pgid == ownPGID {
			continue
		}
		err := syscall.Kill(-pgid, syscall.SIGKILL)
		if err == nil {
			killed++
			continue
		}
		if errors.Is(err, syscall.ESRCH) || errors.Is(err, syscall.EPERM) {
			continue
		}
		errs = append(errs, fmt.Errorf("kill process group %d: %w", pgid, err))
	}
	for _, pid := range sortedKeys(pids) {
		if pid == 0 || pid == os.Getpid() {
			continue
		}
		err := syscall.Kill(pid, syscall.SIGKILL)
		if err == nil {
			killed++
			continue
		}
		if errors.Is(err, syscall.ESRCH) || errors.Is(err, syscall.EPERM) {
			continue
		}
		errs = append(errs, fmt.Errorf("kill process %d: %w", pid, err))
	}

	if !waitForActive {
		return killed, errors.Join(errs...)
	}

	deadline := time.Now().Add(activeReapWait)
	for _, command := range commands {
		remaining := time.Until(deadline)
		if remaining <= 0 {
			break
		}
		select {
		case <-command.done:
		case <-time.After(remaining):
		}
	}
	return killed, errors.Join(errs...)
}

type activeCleanupTargetSet struct {
	groups map[int]struct{}
	pids   map[int]struct{}
}

func activeCleanupTargets(commands []activeCommand, processes map[int]processInfo, pipeHolders func(string) []int, ownPID int) activeCleanupTargetSet {
	targets := activeCleanupTargetSet{
		groups: map[int]struct{}{},
		pids:   map[int]struct{}{},
	}
	for _, command := range commands {
		if command.directLive {
			addActiveCleanupPID(&targets, processes, command.rootPID, ownPID)
			targets.groups[command.pgid] = struct{}{}
			for _, pid := range descendantPIDs(command.rootPID, processes) {
				addActiveCleanupPID(&targets, processes, pid, ownPID)
			}
		}
		for _, pid := range pipeHolders(command.pipeID) {
			if pid == ownPID {
				continue
			}
			addActiveCleanupPID(&targets, processes, pid, ownPID)
			for _, descendantPID := range descendantPIDs(pid, processes) {
				addActiveCleanupPID(&targets, processes, descendantPID, ownPID)
			}
		}
	}
	return targets
}

func addActiveCleanupPID(targets *activeCleanupTargetSet, processes map[int]processInfo, pid, ownPID int) {
	if pid == 0 || pid == ownPID {
		return
	}
	targets.pids[pid] = struct{}{}
	if info, ok := processes[pid]; ok && info.pgid > 0 {
		targets.groups[info.pgid] = struct{}{}
	}
}

func registerActiveProcessGroup(pgid int, pipeID string) (func(), func()) {
	command := &activeCommand{rootPID: pgid, pgid: pgid, pipeID: pipeID, directLive: true, done: make(chan struct{})}
	id := activeProcessGroups.nextID.Add(1)
	activeProcessGroups.Lock()
	activeProcessGroups.commands[id] = command
	activeProcessGroups.Unlock()

	markDirectProcessReaped := func() {
		activeProcessGroups.Lock()
		command.directLive = false
		activeProcessGroups.Unlock()
	}

	var once sync.Once
	unregister := func() {
		once.Do(func() {
			activeProcessGroups.Lock()
			delete(activeProcessGroups.commands, id)
			activeProcessGroups.Unlock()
			close(command.done)
		})
	}
	return markDirectProcessReaped, unregister
}

func reapIfCanceledAfterRegistration(ctx context.Context, reapActive func() (int, error)) {
	select {
	case <-ctx.Done():
		_, _ = reapActive()
	default:
	}
}

func activeCommandSnapshot() []activeCommand {
	activeProcessGroups.Lock()
	defer activeProcessGroups.Unlock()
	commands := make([]activeCommand, 0, len(activeProcessGroups.commands))
	for _, command := range activeProcessGroups.commands {
		commands = append(commands, *command)
	}
	sort.Slice(commands, func(i, j int) bool { return commands[i].rootPID < commands[j].rootPID })
	return commands
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
	pipeID := pipeIdentifier(writer)
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
	markDirectProcessReaped, unregisterActiveProcessGroup := registerActiveProcessGroup(cmd.Process.Pid, pipeID)
	defer unregisterActiveProcessGroup()
	// If runtimeguard canceled between cmd.Start and active registration, its
	// first cleanup may have observed an empty registry. Reap once more now that
	// this command and any inherited-output pipe holders are discoverable.
	reapIfCanceledAfterRegistration(runCtx, func() (int, error) {
		return killActiveProcessGroups(false)
	})
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
	markDirectProcessReaped()
	// A shell can exit while children keep inherited stdout/stderr pipe FDs open.
	// Kill the command's process group after the direct process exits so same-pgid
	// background writers are reaped before the final output drain. Descendants that
	// escaped the group are handled by waiting for pipe EOF, bounded only by
	// context timeout/cancellation, output flood, or fatal active cleanup.
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

type processInfo struct {
	pid   int
	ppid  int
	pgid  int
	state string
}

func processSnapshot() map[int]processInfo {
	if runtime.GOOS == "linux" {
		return linuxProcessSnapshot()
	}
	return psProcessSnapshot()
}

func linuxProcessSnapshot() map[int]processInfo {
	entries, err := os.ReadDir("/proc")
	if err != nil {
		return map[int]processInfo{}
	}
	processes := make(map[int]processInfo, len(entries))
	for _, entry := range entries {
		pid, err := strconv.Atoi(entry.Name())
		if err != nil {
			continue
		}
		data, err := os.ReadFile(filepath.Join("/proc", entry.Name(), "stat"))
		if err != nil {
			continue
		}
		info, ok := parseLinuxStat(pid, string(data))
		if ok {
			processes[pid] = info
		}
	}
	return processes
}

func parseLinuxStat(pid int, stat string) (processInfo, bool) {
	end := strings.LastIndex(stat, ")")
	if end < 0 || end+2 >= len(stat) {
		return processInfo{}, false
	}
	fields := strings.Fields(stat[end+1:])
	if len(fields) < 3 {
		return processInfo{}, false
	}
	ppid, err := strconv.Atoi(fields[1])
	if err != nil {
		return processInfo{}, false
	}
	pgid, err := strconv.Atoi(fields[2])
	if err != nil {
		return processInfo{}, false
	}
	return processInfo{pid: pid, ppid: ppid, pgid: pgid, state: fields[0]}, true
}

func psProcessSnapshot() map[int]processInfo {
	out, err := exec.Command("ps", "-axo", "pid=,ppid=,pgid=,stat=").Output()
	if err != nil {
		return map[int]processInfo{}
	}
	processes := map[int]processInfo{}
	for _, line := range strings.Split(string(out), "\n") {
		fields := strings.Fields(line)
		if len(fields) < 4 {
			continue
		}
		pid, pidErr := strconv.Atoi(fields[0])
		ppid, ppidErr := strconv.Atoi(fields[1])
		pgid, pgidErr := strconv.Atoi(fields[2])
		if pidErr != nil || ppidErr != nil || pgidErr != nil {
			continue
		}
		processes[pid] = processInfo{pid: pid, ppid: ppid, pgid: pgid, state: fields[3]}
	}
	return processes
}

func descendantPIDs(rootPID int, processes map[int]processInfo) []int {
	children := map[int][]int{}
	for pid, info := range processes {
		children[info.ppid] = append(children[info.ppid], pid)
	}
	var descendants []int
	queue := append([]int(nil), children[rootPID]...)
	for len(queue) > 0 {
		pid := queue[0]
		queue = queue[1:]
		descendants = append(descendants, pid)
		queue = append(queue, children[pid]...)
	}
	sort.Ints(descendants)
	return descendants
}

// pipeIdentifier returns the Linux /proc identity for an inherited output pipe.
// Darwin builds intentionally fall back to process-tree/process-group cleanup:
// there is no /proc fd table to scan here, so a double-forked/session-escaped
// descendant that keeps stdout/stderr open but is no longer visible in the PPID
// tree is only covered by Linux pipe-holder discovery.
func pipeIdentifier(file *os.File) string {
	if runtime.GOOS != "linux" || file == nil {
		return ""
	}
	link, err := os.Readlink(filepath.Join("/proc/self/fd", strconv.Itoa(int(file.Fd()))))
	if err != nil || !strings.HasPrefix(link, "pipe:[") {
		return ""
	}
	return link
}

func pipeHolderPIDs(pipeID string) []int {
	if runtime.GOOS != "linux" || pipeID == "" {
		return nil
	}
	entries, err := os.ReadDir("/proc")
	if err != nil {
		return nil
	}
	seen := map[int]struct{}{}
	for _, entry := range entries {
		pid, err := strconv.Atoi(entry.Name())
		if err != nil {
			continue
		}
		fdDir := filepath.Join("/proc", entry.Name(), "fd")
		fds, err := os.ReadDir(fdDir)
		if err != nil {
			continue
		}
		for _, fd := range fds {
			link, err := os.Readlink(filepath.Join(fdDir, fd.Name()))
			if err == nil && link == pipeID {
				seen[pid] = struct{}{}
				break
			}
		}
	}
	return sortedKeys(seen)
}

func sortedKeys(values map[int]struct{}) []int {
	keys := make([]int, 0, len(values))
	for value := range values {
		keys = append(keys, value)
	}
	sort.Ints(keys)
	return keys
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
