package pipe

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"io/fs"
	"os"
	"os/exec"
	"path/filepath"
	"sort"
	"strings"
	"time"

	"github.com/camcamcami/BLK-System/internal/contracts"
	"github.com/camcamcami/BLK-System/internal/engine"
	"github.com/camcamcami/BLK-System/internal/gitguard"
)

const engineCommitMessage = "blk-pipe: apply bounded engine changes"

// Run orchestrates one bounded blk-pipe execution and writes exactly one JSON
// report to reportWriter. It returns the process exit code matching the report
// status.
func Run(ctx context.Context, payloadJSON []byte, reportWriter io.Writer) int {
	report := contracts.Report{
		StagedFiles:    []string{},
		DestroyedFiles: []string{},
	}
	exitCode := run(ctx, payloadJSON, &report)
	if err := json.NewEncoder(reportWriter).Encode(report); err != nil {
		return ExitInternalError
	}
	return exitCode
}

func run(ctx context.Context, payloadJSON []byte, report *contracts.Report) int {
	payload, exitCode := parseAndValidatePayload(payloadJSON, report)
	if exitCode != ExitSuccess {
		return exitCode
	}

	if err := gitguard.EnsureClean(payload.Workdir); err != nil {
		report.Error = err.Error()
		var dirty *gitguard.DirtyError
		if errors.As(err, &dirty) {
			report.Status = "GIT_DIRTY"
			return ExitGitDirty
		}
		report.Status = "INTERNAL_ERROR"
		return ExitInternalError
	}

	baselineUntracked, err := untrackedFileSet(payload.Workdir)
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		return ExitInternalError
	}
	if len(baselineUntracked) > 0 {
		report.Status = "GIT_DIRTY"
		report.Error = preExistingUntrackedError(baselineUntracked)
		return ExitGitDirty
	}

	gitBefore, err := snapshotGitDir(payload.Workdir)
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		return ExitInternalError
	}

	engineCtx, cancel := context.WithTimeout(ctx, time.Duration(payload.TimeoutSeconds)*time.Second)
	defer cancel()
	result, err := engine.Run(engineCtx, payload.Workdir, payload.EngineCommand, payload.MaxOutputBytes)
	report.EngineExitCode = result.ExitCode
	report.EngineOutputBytes = result.OutputBytes
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		if cleanupErr := cleanupFailedRun(payload.Workdir, gitBefore); cleanupErr != nil {
			report.Error = cleanupErr.Error()
		}
		return ExitInternalError
	}
	if result.Flooded {
		report.Status = "FATAL_OUTPUT_FLOOD"
		report.Error = "engine output exceeded max_output_bytes"
		if cleanupErr := cleanupFailedRun(payload.Workdir, gitBefore); cleanupErr != nil {
			report.Status = "INTERNAL_ERROR"
			report.Error = cleanupErr.Error()
			return ExitInternalError
		}
		return ExitOutputFlood
	}
	if result.TimedOut {
		report.Status = "ENGINE_TIMEOUT"
		report.Error = "engine timed out"
		if cleanupErr := cleanupFailedRun(payload.Workdir, gitBefore); cleanupErr != nil {
			report.Status = "INTERNAL_ERROR"
			report.Error = cleanupErr.Error()
			return ExitInternalError
		}
		return ExitEngineTimeout
	}
	if result.ExitCode != 0 {
		report.Status = "FATAL_ENGINE_FAILED"
		report.Error = fmt.Sprintf("engine exited with code %d", result.ExitCode)
		if cleanupErr := cleanupFailedRun(payload.Workdir, gitBefore); cleanupErr != nil {
			report.Status = "INTERNAL_ERROR"
			report.Error = cleanupErr.Error()
			return ExitInternalError
		}
		return ExitFatalSystemPanic
	}

	gitMutations, err := gitBefore.ChangedPaths()
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		if cleanupErr := cleanupFailedRun(payload.Workdir, gitBefore); cleanupErr != nil {
			report.Error = cleanupErr.Error()
		}
		return ExitInternalError
	}
	if len(gitMutations) > 0 {
		if err := gitBefore.Restore(); err != nil {
			report.Status = "INTERNAL_ERROR"
			report.Error = err.Error()
			return ExitInternalError
		}
		worktreeMutations, err := unauthorizedWorktreeFiles(payload.Workdir, payload.AllowedModifiedFiles, payload.AllowedNewFiles, baselineUntracked)
		if err != nil {
			report.Status = "INTERNAL_ERROR"
			report.Error = err.Error()
			if cleanupErr := cleanupFailedRun(payload.Workdir, nil); cleanupErr != nil {
				report.Error = cleanupErr.Error()
			}
			return ExitInternalError
		}
		report.Status = "UNAUTHORIZED_FILE_MUTATION"
		report.DestroyedFiles = uniqueSorted(append(gitMutations, worktreeMutations...))
		report.Error = "engine modified files outside the allowlist"
		if err := cleanupFailedRun(payload.Workdir, nil); err != nil {
			report.Status = "INTERNAL_ERROR"
			report.Error = err.Error()
			return ExitInternalError
		}
		return ExitUnauthorizedMutation
	}

	if err := gitguard.StageAllowlist(payload.Workdir, payload.AllowedModifiedFiles, payload.AllowedNewFiles); err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		if cleanupErr := cleanupFailedRun(payload.Workdir, gitBefore); cleanupErr != nil {
			report.Error = cleanupErr.Error()
		}
		return ExitInternalError
	}

	stagedFiles, err := stagedDiffFiles(payload.Workdir)
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		if cleanupErr := cleanupFailedRun(payload.Workdir, gitBefore); cleanupErr != nil {
			report.Error = cleanupErr.Error()
		}
		return ExitInternalError
	}
	report.StagedFiles = stagedFiles

	unauthorizedFiles, err := unauthorizedWorktreeFiles(payload.Workdir, nil, nil, baselineUntracked)
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		if cleanupErr := cleanupFailedRun(payload.Workdir, gitBefore); cleanupErr != nil {
			report.Error = cleanupErr.Error()
		}
		return ExitInternalError
	}
	if len(unauthorizedFiles) > 0 {
		report.Status = "UNAUTHORIZED_FILE_MUTATION"
		report.DestroyedFiles = unauthorizedFiles
		report.Error = "engine modified files outside the allowlist"
		if err := cleanupFailedRun(payload.Workdir, gitBefore); err != nil {
			report.Status = "INTERNAL_ERROR"
			report.Error = err.Error()
			return ExitInternalError
		}
		return ExitUnauthorizedMutation
	}

	if len(stagedFiles) > 0 {
		commitHash, err := commitStaged(payload.Workdir)
		if err != nil {
			report.Status = "INTERNAL_ERROR"
			report.Error = err.Error()
			if cleanupErr := cleanupFailedRun(payload.Workdir, gitBefore); cleanupErr != nil {
				report.Error = cleanupErr.Error()
			}
			return ExitInternalError
		}
		report.CommitHash = commitHash
	}

	report.Status = "SUCCESS"
	return ExitSuccess
}

func parseAndValidatePayload(payloadJSON []byte, report *contracts.Report) (contracts.Payload, int) {
	var payload contracts.Payload
	if err := json.Unmarshal(payloadJSON, &payload); err != nil {
		report.Status = "INVALID_PAYLOAD"
		report.Error = err.Error()
		return contracts.Payload{}, ExitInvalidPayload
	}
	report.Action = payload.Action
	report.Workdir = payload.Workdir
	if err := payload.Validate(); err != nil {
		report.Status = "INVALID_PAYLOAD"
		report.Error = err.Error()
		return contracts.Payload{}, ExitInvalidPayload
	}
	return payload, ExitSuccess
}

func stagedDiffFiles(repo string) ([]string, error) {
	out, err := runGit(repo, "diff", "--cached", "--name-only", "-z")
	if err != nil {
		return nil, err
	}
	return splitNULPaths(out), nil
}

func unauthorizedWorktreeFiles(repo string, allowedModified []string, allowedNew []string, baselineUntracked map[string]struct{}) ([]string, error) {
	unstaged, err := runGit(repo, "diff", "--name-only", "-z")
	if err != nil {
		return nil, err
	}
	untracked, err := runGit(repo, "ls-files", "--others", "-z")
	if err != nil {
		return nil, err
	}
	allowed := pathSet(append(append([]string{}, allowedModified...), allowedNew...))
	seen := map[string]struct{}{}
	for _, rel := range splitNULPaths(unstaged) {
		if _, ok := allowed[rel]; ok {
			continue
		}
		seen[rel] = struct{}{}
	}
	for _, rel := range splitNULPaths(untracked) {
		if _, ok := allowed[rel]; ok {
			continue
		}
		if _, ok := baselineUntracked[rel]; ok {
			continue
		}
		seen[rel] = struct{}{}
	}
	paths := make([]string, 0, len(seen))
	for rel := range seen {
		paths = append(paths, rel)
	}
	sort.Strings(paths)
	return paths, nil
}

func untrackedFileSet(repo string) (map[string]struct{}, error) {
	out, err := runGit(repo, "ls-files", "--others", "-z")
	if err != nil {
		return nil, err
	}
	return pathSet(splitNULPaths(out)), nil
}

func preExistingUntrackedError(paths map[string]struct{}) string {
	items := make([]string, 0, len(paths))
	for path := range paths {
		items = append(items, path)
	}
	sort.Strings(items)
	return "git worktree has pre-existing untracked or ignored files:\n" + strings.Join(items, "\n")
}

func pathSet(paths []string) map[string]struct{} {
	set := make(map[string]struct{}, len(paths))
	for _, path := range paths {
		set[path] = struct{}{}
	}
	return set
}

func uniqueSorted(paths []string) []string {
	set := pathSet(paths)
	out := make([]string, 0, len(set))
	for path := range set {
		out = append(out, path)
	}
	sort.Strings(out)
	return out
}

func commitStaged(repo string) (string, error) {
	if _, err := runGit(repo, "-c", "core.hooksPath=/dev/null", "commit", "-m", engineCommitMessage); err != nil {
		return "", err
	}
	out, err := runGit(repo, "rev-parse", "HEAD")
	if err != nil {
		return "", err
	}
	return strings.TrimSpace(string(out)), nil
}

func cleanupFailedRun(repo string, gitBefore *gitSnapshot) error {
	if gitBefore != nil {
		if err := gitBefore.Restore(); err != nil {
			return fmt.Errorf("restore git metadata: %w", err)
		}
	}
	if err := resetHard(repo); err != nil {
		return err
	}
	if err := gitguard.CleanupUnauthorized(repo); err != nil {
		return err
	}
	return nil
}

func resetHard(repo string) error {
	_, err := runGit(repo, "reset", "--hard", "HEAD")
	return err
}

type gitSnapshot struct {
	root    string
	entries map[string]gitSnapshotEntry
}

type gitSnapshotEntry struct {
	mode  os.FileMode
	data  []byte
	link  string
	isDir bool
}

func snapshotGitDir(repo string) (*gitSnapshot, error) {
	out, err := runGit(repo, "rev-parse", "--absolute-git-dir")
	if err != nil {
		return nil, err
	}
	root := strings.TrimSpace(string(out))
	if root == "" {
		return nil, fmt.Errorf("git rev-parse --absolute-git-dir in %q returned an empty path", repo)
	}
	entries, err := snapshotPathEntries(root)
	if err != nil {
		return nil, err
	}
	return &gitSnapshot{root: root, entries: entries}, nil
}

func (s *gitSnapshot) ChangedPaths() ([]string, error) {
	current, err := snapshotPathEntries(s.root)
	if err != nil {
		if errors.Is(err, fs.ErrNotExist) {
			current = map[string]gitSnapshotEntry{}
		} else {
			return nil, err
		}
	}
	changed := map[string]struct{}{}
	for rel, before := range s.entries {
		after, ok := current[rel]
		if !ok || !before.equal(after) {
			changed[gitReportPath(rel)] = struct{}{}
		}
	}
	for rel := range current {
		if _, ok := s.entries[rel]; !ok {
			changed[gitReportPath(rel)] = struct{}{}
		}
	}
	paths := make([]string, 0, len(changed))
	for path := range changed {
		paths = append(paths, path)
	}
	sort.Strings(paths)
	return paths, nil
}

func (s *gitSnapshot) Restore() error {
	current, err := snapshotPathEntries(s.root)
	if err != nil {
		if errors.Is(err, fs.ErrNotExist) {
			current = map[string]gitSnapshotEntry{}
		} else {
			return err
		}
	}
	if info, err := os.Lstat(s.root); err == nil && !info.IsDir() {
		if err := os.RemoveAll(s.root); err != nil {
			return fmt.Errorf("remove non-directory git root %q: %w", s.root, err)
		}
	} else if err != nil && !errors.Is(err, fs.ErrNotExist) {
		return fmt.Errorf("stat git root %q: %w", s.root, err)
	}
	if err := os.MkdirAll(s.root, 0o755); err != nil {
		return fmt.Errorf("restore git root %q: %w", s.root, err)
	}
	for rel, entry := range current {
		if _, ok := s.entries[rel]; ok || entry.isDir {
			continue
		}
		if err := os.RemoveAll(filepath.Join(s.root, filepath.FromSlash(rel))); err != nil {
			return fmt.Errorf("remove added git file %q: %w", gitReportPath(rel), err)
		}
	}
	addedDirs := make([]string, 0)
	for rel, entry := range current {
		if _, ok := s.entries[rel]; !ok && entry.isDir {
			addedDirs = append(addedDirs, rel)
		}
	}
	sort.Slice(addedDirs, func(i, j int) bool { return len(addedDirs[i]) > len(addedDirs[j]) })
	for _, rel := range addedDirs {
		path := filepath.Join(s.root, filepath.FromSlash(rel))
		if err := os.Remove(path); err != nil && !os.IsNotExist(err) {
			return fmt.Errorf("remove added git directory %q: %w", gitReportPath(rel), err)
		}
	}

	dirs := make([]string, 0)
	files := make([]string, 0)
	for rel, entry := range s.entries {
		if entry.isDir {
			dirs = append(dirs, rel)
			continue
		}
		files = append(files, rel)
	}
	sort.Slice(dirs, func(i, j int) bool { return len(dirs[i]) < len(dirs[j]) })
	for _, rel := range dirs {
		entry := s.entries[rel]
		path := filepath.Join(s.root, filepath.FromSlash(rel))
		if err := os.MkdirAll(path, entry.mode.Perm()); err != nil {
			return fmt.Errorf("restore git directory %q: %w", gitReportPath(rel), err)
		}
		if err := os.Chmod(path, entry.mode.Perm()); err != nil {
			return fmt.Errorf("chmod git directory %q: %w", gitReportPath(rel), err)
		}
	}
	sort.Strings(files)
	for _, rel := range files {
		entry := s.entries[rel]
		path := filepath.Join(s.root, filepath.FromSlash(rel))
		if err := os.MkdirAll(filepath.Dir(path), 0o755); err != nil {
			return fmt.Errorf("restore parent for git file %q: %w", gitReportPath(rel), err)
		}
		if entry.mode&os.ModeSymlink != 0 {
			if err := os.RemoveAll(path); err != nil {
				return fmt.Errorf("replace git symlink %q: %w", gitReportPath(rel), err)
			}
			if err := os.Symlink(entry.link, path); err != nil {
				return fmt.Errorf("restore git symlink %q: %w", gitReportPath(rel), err)
			}
			continue
		}
		if !entry.mode.IsRegular() {
			return fmt.Errorf("cannot restore unsupported git entry %q with mode %s", gitReportPath(rel), entry.mode)
		}
		if err := os.RemoveAll(path); err != nil {
			return fmt.Errorf("replace git file %q: %w", gitReportPath(rel), err)
		}
		if err := os.WriteFile(path, entry.data, entry.mode.Perm()); err != nil {
			return fmt.Errorf("restore git file %q: %w", gitReportPath(rel), err)
		}
	}
	return nil
}

func snapshotPathEntries(root string) (map[string]gitSnapshotEntry, error) {
	entries := map[string]gitSnapshotEntry{}
	if err := filepath.WalkDir(root, func(path string, d fs.DirEntry, walkErr error) error {
		if walkErr != nil {
			return walkErr
		}
		relOS, err := filepath.Rel(root, path)
		if err != nil {
			return err
		}
		if relOS == "." {
			return nil
		}
		rel := filepath.ToSlash(relOS)
		info, err := os.Lstat(path)
		if err != nil {
			return err
		}
		entry := gitSnapshotEntry{mode: info.Mode(), isDir: info.IsDir()}
		switch {
		case info.IsDir():
		case info.Mode()&os.ModeSymlink != 0:
			entry.link, err = os.Readlink(path)
			if err != nil {
				return err
			}
		case info.Mode().IsRegular():
			entry.data, err = os.ReadFile(path)
			if err != nil {
				return err
			}
		default:
			return fmt.Errorf("unsupported git entry %q with mode %s", gitReportPath(rel), info.Mode())
		}
		entries[rel] = entry
		return nil
	}); err != nil {
		return nil, fmt.Errorf("snapshot git directory %q: %w", root, err)
	}
	return entries, nil
}

func (e gitSnapshotEntry) equal(other gitSnapshotEntry) bool {
	return e.mode == other.mode && e.link == other.link && e.isDir == other.isDir && bytes.Equal(e.data, other.data)
}

func gitReportPath(rel string) string {
	return ".git/" + filepath.ToSlash(rel)
}

func splitNULPaths(out []byte) []string {
	if len(out) == 0 {
		return []string{}
	}
	parts := bytes.Split(out, []byte{0})
	paths := make([]string, 0, len(parts))
	for _, part := range parts {
		if len(part) > 0 {
			paths = append(paths, string(part))
		}
	}
	sort.Strings(paths)
	return paths
}

func runGit(repo string, args ...string) ([]byte, error) {
	cmd := exec.Command("git", args...)
	cmd.Dir = repo
	cmd.Env = gitEnv()
	out, err := cmd.CombinedOutput()
	if err != nil {
		if msg := strings.TrimSpace(string(out)); msg != "" {
			return out, fmt.Errorf("git %s in %q: %w: %s", strings.Join(args, " "), repo, err, msg)
		}
		return out, fmt.Errorf("git %s in %q: %w", strings.Join(args, " "), repo, err)
	}
	return out, nil
}

func gitEnv() []string {
	env := make([]string, 0, len(os.Environ())+2)
	for _, entry := range os.Environ() {
		key, _, _ := strings.Cut(entry, "=")
		if strings.HasPrefix(key, "GIT_") {
			continue
		}
		env = append(env, entry)
	}
	return append(env,
		"GIT_CONFIG_GLOBAL="+os.DevNull,
		"GIT_CONFIG_NOSYSTEM=1",
	)
}
