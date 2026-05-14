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
	"path"
	"path/filepath"
	"sort"
	"strconv"
	"strings"
	"time"

	"github.com/camcamcami/BLK-System/internal/contracts"
	"github.com/camcamcami/BLK-System/internal/engine"
	"github.com/camcamcami/BLK-System/internal/gitguard"
	"github.com/camcamcami/BLK-System/internal/validation"
)

const engineCommitMessage = "blk-pipe: apply bounded engine changes"

// Run orchestrates one bounded blk-pipe execution and writes exactly one JSON
// report to reportWriter. It returns the process exit code matching the report
// status.
func Run(ctx context.Context, payloadJSON []byte, reportWriter io.Writer) int {
	report := contracts.NewReport()
	exitCode := run(ctx, payloadJSON, &report)
	report.ExitCode = exitCode
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

	if payload.Action == "revert" {
		return runRevert(payload, report)
	}

	baselineUntracked, exitCode := cleanPreflight(payload.Workdir, report)
	if exitCode != ExitSuccess {
		return exitCode
	}
	if payload.TargetBranch != "" {
		if exitCode := prepareExecuteTargetBranch(ctx, payload, report); exitCode != ExitSuccess {
			return exitCode
		}
		baselineUntracked, exitCode = cleanPreflight(payload.Workdir, report)
		if exitCode != ExitSuccess {
			return exitCode
		}
	}
	if payload.TargetHash != "" {
		if exitCode := verifyExecuteTargetHash(ctx, payload, report); exitCode != ExitSuccess {
			return exitCode
		}
	}
	if exitCode := failWrongClassAllowlistPaths(payload, report); exitCode != ExitSuccess {
		return exitCode
	}

	preEngineHash, err := currentHeadHash(payload.Workdir)
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		return ExitInternalError
	}
	report.PreEngineHash = preEngineHash

	gitBefore, err := snapshotGitDir(payload.Workdir)
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		return ExitInternalError
	}
	dirBefore, err := snapshotWorktreeDirModes(payload.Workdir, gitBefore.root)
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		return ExitInternalError
	}
	worktreeBefore, err := snapshotPhysicalWorktree(payload.Workdir, gitBefore.root)
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		return ExitInternalError
	}

	engineCtx, cancel := context.WithTimeout(ctx, time.Duration(payload.TimeoutSeconds)*time.Second)
	defer cancel()
	result, err := engine.Run(engineCtx, payload.Workdir, payload.EngineCommand, payload.MaxOutputBytes, []byte(payload.L2Packet))
	report.EngineExitCode = result.ExitCode
	report.EngineOutputBytes = result.OutputBytes
	report.EngineLogs = string(result.Output)
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		if cleanupErr := cleanupFailedRun(payload.Workdir, gitBefore, dirBefore); cleanupErr != nil {
			report.Error = cleanupErr.Error()
		}
		return ExitInternalError
	}
	if result.Flooded {
		report.Status = "FATAL_OUTPUT_FLOOD"
		report.Error = "engine output exceeded max_output_bytes"
		if cleanupErr := cleanupFailedRun(payload.Workdir, gitBefore, dirBefore); cleanupErr != nil {
			report.Status = "INTERNAL_ERROR"
			report.Error = cleanupErr.Error()
			return ExitInternalError
		}
		return ExitOutputFlood
	}
	if result.TimedOut {
		report.Status = "ENGINE_TIMEOUT"
		report.Error = "engine timed out"
		if cleanupErr := cleanupFailedRun(payload.Workdir, gitBefore, dirBefore); cleanupErr != nil {
			report.Status = "INTERNAL_ERROR"
			report.Error = cleanupErr.Error()
			return ExitInternalError
		}
		return ExitEngineTimeout
	}
	if result.ExitCode != 0 {
		report.Status = "FATAL_ENGINE_FAILED"
		report.Error = fmt.Sprintf("engine exited with code %d", result.ExitCode)
		if cleanupErr := cleanupFailedRun(payload.Workdir, gitBefore, dirBefore); cleanupErr != nil {
			report.Status = "INTERNAL_ERROR"
			report.Error = cleanupErr.Error()
			return ExitInternalError
		}
		return ExitFatalSystemPanic
	}

	if exitCode := failUnauthorizedDirectoryModeMutation(payload.Workdir, dirBefore, gitBefore, report, "engine modified files outside the allowlist"); exitCode != ExitSuccess {
		return exitCode
	}

	gitMutations, err := gitBefore.ChangedPaths()
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		if cleanupErr := cleanupFailedRun(payload.Workdir, gitBefore, dirBefore); cleanupErr != nil {
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
		physicalResidue, err := unauthorizedPhysicalResidue(payload.Workdir, payload.AllowedModifiedFiles, payload.AllowedNewFiles, baselineUntracked)
		if err != nil {
			report.Status = "INTERNAL_ERROR"
			report.Error = err.Error()
			if cleanupErr := cleanupFailedRun(payload.Workdir, nil, dirBefore); cleanupErr != nil {
				report.Error = cleanupErr.Error()
			}
			return ExitInternalError
		}
		report.Status = "UNAUTHORIZED_FILE_MUTATION"
		report.DestroyedFiles = uniqueSorted(append(gitMutations, physicalResidue...))
		report.Error = "engine modified files outside the allowlist"
		if err := cleanupFailedRun(payload.Workdir, nil, dirBefore); err != nil {
			report.Status = "INTERNAL_ERROR"
			report.Error = err.Error()
			return ExitInternalError
		}
		return ExitUnauthorizedMutation
	}

	if exitCode := failUnauthorizedPhysicalResidue(payload.Workdir, payload.AllowedModifiedFiles, payload.AllowedNewFiles, baselineUntracked, gitBefore, dirBefore, report, "engine modified files outside the allowlist"); exitCode != ExitSuccess {
		return exitCode
	}

	if exitCode := failNoEngineCandidateDiff(payload.Workdir, worktreeBefore, gitBefore, dirBefore, report); exitCode != ExitSuccess {
		return exitCode
	}

	postEngineValidationBaseline, err := snapshotValidationBaseline(payload.Workdir)
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		if cleanupErr := cleanupFailedRun(payload.Workdir, gitBefore, dirBefore); cleanupErr != nil {
			report.Error = cleanupErr.Error()
		}
		return ExitInternalError
	}

	validationResult, err := runValidation(ctx, payload)
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.ValidationLogs = validationResult.Logs
		report.Error = err.Error()
		if cleanupErr := cleanupValidationFailedRun(payload.Workdir, gitBefore, preEngineHash, dirBefore); cleanupErr != nil {
			report.Error = cleanupErr.Error()
		}
		return ExitInternalError
	}
	report.ValidationLogs = validationResult.Logs

	if exitCode := failValidationMutationFromBaseline(payload.Workdir, postEngineValidationBaseline, gitBefore, dirBefore, preEngineHash, report); exitCode != ExitSuccess {
		return exitCode
	}

	if exitCode := failUnauthorizedValidationDirectoryModeMutation(payload.Workdir, dirBefore, gitBefore, preEngineHash, report); exitCode != ExitSuccess {
		return exitCode
	}

	postValidationGitMutations, err := gitBefore.ChangedPaths()
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		if cleanupErr := cleanupValidationFailedRun(payload.Workdir, gitBefore, preEngineHash, dirBefore); cleanupErr != nil {
			report.Error = cleanupErr.Error()
		}
		return ExitInternalError
	}
	if len(postValidationGitMutations) > 0 {
		if err := gitBefore.Restore(); err != nil {
			report.Status = "INTERNAL_ERROR"
			report.Error = err.Error()
			return ExitInternalError
		}
		physicalResidue, err := unauthorizedPhysicalResidue(payload.Workdir, payload.AllowedModifiedFiles, payload.AllowedNewFiles, baselineUntracked)
		if err != nil {
			report.Status = "INTERNAL_ERROR"
			report.Error = err.Error()
			if cleanupErr := cleanupValidationFailedRun(payload.Workdir, nil, preEngineHash, dirBefore); cleanupErr != nil {
				report.Error = cleanupErr.Error()
			}
			return ExitInternalError
		}
		report.Status = "UNAUTHORIZED_FILE_MUTATION"
		report.DestroyedFiles = uniqueSorted(append(postValidationGitMutations, physicalResidue...))
		report.Error = "validation modified files outside the allowlist"
		if err := cleanupValidationFailedRun(payload.Workdir, nil, preEngineHash, dirBefore); err != nil {
			report.Status = "INTERNAL_ERROR"
			report.Error = err.Error()
			return ExitInternalError
		}
		return ExitUnauthorizedMutation
	}

	if exitCode := failUnauthorizedValidationResidue(payload.Workdir, payload.AllowedModifiedFiles, payload.AllowedNewFiles, baselineUntracked, gitBefore, dirBefore, preEngineHash, report); exitCode != ExitSuccess {
		return exitCode
	}

	if validationResult.HasFailure {
		report.Status = "SYNTAX_GATE_FAILED"
		report.Error = "validation command failed"
		if cleanupErr := cleanupValidationFailedRun(payload.Workdir, gitBefore, preEngineHash, dirBefore); cleanupErr != nil {
			report.Status = "INTERNAL_ERROR"
			report.Error = cleanupErr.Error()
			return ExitInternalError
		}
		return ExitValidationFailed
	}

	producedAllowedNewFiles, err := existingAllowedNewFiles(payload.Workdir, payload.AllowedNewFiles)
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		if cleanupErr := cleanupFailedRun(payload.Workdir, gitBefore, dirBefore); cleanupErr != nil {
			report.Error = cleanupErr.Error()
		}
		return ExitInternalError
	}
	if exitCode := failUnauthorizedAllowedNewPhysicalModes(payload.Workdir, producedAllowedNewFiles, gitBefore, dirBefore, report); exitCode != ExitSuccess {
		return exitCode
	}

	if err := gitguard.StageAllowlist(payload.Workdir, payload.AllowedModifiedFiles, producedAllowedNewFiles); err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		if cleanupErr := cleanupFailedRun(payload.Workdir, gitBefore, dirBefore); cleanupErr != nil {
			report.Error = cleanupErr.Error()
		}
		return ExitInternalError
	}

	stagedFiles, err := stagedDiffFiles(payload.Workdir)
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		if cleanupErr := cleanupFailedRun(payload.Workdir, gitBefore, dirBefore); cleanupErr != nil {
			report.Error = cleanupErr.Error()
		}
		return ExitInternalError
	}
	report.StagedFiles = stagedFiles

	unauthorizedFiles, err := unauthorizedPhysicalResidue(payload.Workdir, nil, nil, baselineUntracked)
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		if cleanupErr := cleanupFailedRun(payload.Workdir, gitBefore, dirBefore); cleanupErr != nil {
			report.Error = cleanupErr.Error()
		}
		return ExitInternalError
	}
	if len(unauthorizedFiles) > 0 {
		report.Status = "UNAUTHORIZED_FILE_MUTATION"
		report.DestroyedFiles = unauthorizedFiles
		report.Error = "engine modified files outside the allowlist"
		if err := cleanupFailedRun(payload.Workdir, gitBefore, dirBefore); err != nil {
			report.Status = "INTERNAL_ERROR"
			report.Error = err.Error()
			return ExitInternalError
		}
		return ExitUnauthorizedMutation
	}

	if len(stagedFiles) == 0 {
		report.Status = "UNAUTHORIZED_FILE_MUTATION"
		report.Error = "engine produced no staged allowlisted diff"
		if err := cleanupFailedRun(payload.Workdir, gitBefore, dirBefore); err != nil {
			report.Status = "INTERNAL_ERROR"
			report.Error = err.Error()
			return ExitInternalError
		}
		return ExitUnauthorizedMutation
	}

	commitHash, err := commitStaged(payload.Workdir)
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		if cleanupErr := cleanupFailedRun(payload.Workdir, gitBefore, dirBefore); cleanupErr != nil {
			report.Error = cleanupErr.Error()
		}
		return ExitInternalError
	}
	report.CommitHash = commitHash

	gitDiff, err := gitDiffFromPreEngine(payload.Workdir, preEngineHash)
	if err != nil {
		return failPostCommitReportGeneration(payload.Workdir, gitBefore, dirBefore, report, err)
	}
	report.GitDiff = gitDiff

	diffSummary, err := diffSummaryFromPreEngine(payload.Workdir, preEngineHash)
	if err != nil {
		return failPostCommitReportGeneration(payload.Workdir, gitBefore, dirBefore, report, err)
	}
	report.DiffSummary = diffSummary

	untrackedFiles, err := untrackedReportFiles(payload.Workdir)
	if err != nil {
		return failPostCommitReportGeneration(payload.Workdir, gitBefore, dirBefore, report, err)
	}
	report.UntrackedFiles = untrackedFiles

	report.Status = "SUCCESS"
	return ExitSuccess
}

func prepareExecuteTargetBranch(ctx context.Context, payload contracts.Payload, report *contracts.Report) int {
	var err error
	if payload.TargetHash != "" {
		_, err = gitguard.PrepareExactTargetBranch(ctx, payload.Workdir, payload.TargetBranch, payload.TargetHash)
	} else {
		_, err = gitguard.PrepareTargetBranch(ctx, payload.Workdir, payload.TargetBranch)
	}
	if err != nil {
		report.Error = err.Error()
		var dirty *gitguard.DirtyError
		if errors.As(err, &dirty) {
			report.Status = "GIT_DIRTY"
			return ExitGitDirty
		}
		var targetHead *gitguard.TargetHeadError
		if errors.As(err, &targetHead) {
			report.Status = "TARGET_HEAD_MISMATCH"
			return ExitUnauthorizedMutation
		}
		report.Status = "INTERNAL_ERROR"
		return ExitInternalError
	}
	if err := sterilizePreparedWorkspace(payload.Workdir); err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		return ExitInternalError
	}
	return ExitSuccess
}

func verifyExecuteTargetHash(ctx context.Context, payload contracts.Payload, report *contracts.Report) int {
	if err := gitguard.VerifyCurrentHead(ctx, payload.Workdir, payload.TargetHash); err != nil {
		report.Error = err.Error()
		var targetHead *gitguard.TargetHeadError
		if errors.As(err, &targetHead) {
			report.Status = "TARGET_HEAD_MISMATCH"
			return ExitUnauthorizedMutation
		}
		report.Status = "INTERNAL_ERROR"
		return ExitInternalError
	}
	return ExitSuccess
}

func sterilizePreparedWorkspace(repo string) error {
	if err := resetHard(repo); err != nil {
		return err
	}
	_, err := runGit(repo, "clean", "-ffdx", "-q")
	return err
}

func cleanPreflight(repo string, report *contracts.Report) (map[string]struct{}, int) {
	if err := gitguard.EnsureClean(repo); err != nil {
		report.Error = err.Error()
		var dirty *gitguard.DirtyError
		if errors.As(err, &dirty) {
			report.Status = "GIT_DIRTY"
			return nil, ExitGitDirty
		}
		report.Status = "INTERNAL_ERROR"
		return nil, ExitInternalError
	}

	baselineUntracked, err := untrackedFileSet(repo)
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		return nil, ExitInternalError
	}
	ignored, err := ignoredFileSet(repo)
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		return nil, ExitInternalError
	}
	emptyDirs, err := emptyUntrackedDirSet(repo)
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		return nil, ExitInternalError
	}
	nestedGitDirs, err := nestedGitDirSet(repo)
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		return nil, ExitInternalError
	}
	preExisting := mergePathSets(baselineUntracked, ignored, emptyDirs, nestedGitDirs)
	if len(preExisting) > 0 {
		report.Status = "GIT_DIRTY"
		report.Error = preExistingUntrackedError(preExisting)
		return nil, ExitGitDirty
	}
	return baselineUntracked, ExitSuccess
}

func failNoEngineCandidateDiff(repo string, worktreeBefore *physicalWorktreeSnapshot, gitBefore *gitSnapshot, dirBefore *worktreeDirModeSnapshot, report *contracts.Report) int {
	candidatePaths, err := worktreeBefore.ChangedPaths()
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		if cleanupErr := cleanupFailedRun(repo, gitBefore, dirBefore); cleanupErr != nil {
			report.Error = cleanupErr.Error()
		}
		return ExitInternalError
	}
	if len(candidatePaths) > 0 {
		return ExitSuccess
	}
	report.Status = "UNAUTHORIZED_FILE_MUTATION"
	report.Error = "engine produced no candidate diff"
	if err := cleanupFailedRun(repo, gitBefore, dirBefore); err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		return ExitInternalError
	}
	return ExitUnauthorizedMutation
}

func failWrongClassAllowlistPaths(payload contracts.Payload, report *contracts.Report) int {
	for _, rel := range payload.AllowedModifiedFiles {
		directory, err := isExistingDirectoryPath(payload.Workdir, rel)
		if err != nil {
			report.Status = "INTERNAL_ERROR"
			report.Error = err.Error()
			return ExitInternalError
		}
		if directory {
			report.Status = "UNAUTHORIZED_FILE_MUTATION"
			report.Error = "allowed_modified_files path must name an explicit file before engine execution"
			return ExitUnauthorizedMutation
		}
		tracked, err := isTrackedFilePath(payload.Workdir, rel)
		if err != nil {
			report.Status = "INTERNAL_ERROR"
			report.Error = err.Error()
			return ExitInternalError
		}
		if !tracked {
			report.Status = "UNAUTHORIZED_FILE_MUTATION"
			report.Error = "allowed_modified_files path is not tracked as an exact file before engine execution"
			return ExitUnauthorizedMutation
		}
	}
	for _, rel := range payload.AllowedNewFiles {
		directory, err := isExistingDirectoryPath(payload.Workdir, rel)
		if err != nil {
			report.Status = "INTERNAL_ERROR"
			report.Error = err.Error()
			return ExitInternalError
		}
		if directory {
			report.Status = "UNAUTHORIZED_FILE_MUTATION"
			report.Error = "allowed_new_files path must name an explicit file before engine execution"
			return ExitUnauthorizedMutation
		}
		tracked, err := isTrackedFilePath(payload.Workdir, rel)
		if err != nil {
			report.Status = "INTERNAL_ERROR"
			report.Error = err.Error()
			return ExitInternalError
		}
		if tracked {
			report.Status = "UNAUTHORIZED_FILE_MUTATION"
			report.Error = "allowed_new_files path is already tracked as an exact file before engine execution"
			return ExitUnauthorizedMutation
		}
	}
	return ExitSuccess
}

func isTrackedFilePath(repo, rel string) (bool, error) {
	out, err := runGit(repo, "ls-files", "-z", "--", rel)
	if err != nil {
		return false, fmt.Errorf("check tracked state for %q: %w", rel, err)
	}
	for _, entry := range bytes.Split(out, []byte{0}) {
		if string(entry) == rel {
			return true, nil
		}
	}
	return false, nil
}

func isExistingDirectoryPath(repo, rel string) (bool, error) {
	info, err := os.Lstat(filepath.Join(repo, filepath.FromSlash(rel)))
	if err == nil {
		return info.IsDir(), nil
	}
	if os.IsNotExist(err) {
		return false, nil
	}
	return false, fmt.Errorf("check path class for %q: %w", rel, err)
}

func runRevert(payload contracts.Payload, report *contracts.Report) int {
	if payload.TargetBranch != "" {
		if err := verifyRevertCurrentBranch(payload.Workdir, payload.TargetBranch); err != nil {
			report.Status = "INVALID_REVERT_ANCHOR"
			report.Error = err.Error()
			return ExitInvalidRevertAnchor
		}
	}
	if err := verifyRevertTargetCommit(payload.Workdir, payload.TargetHash); err != nil {
		report.Status = "INVALID_REVERT_ANCHOR"
		report.Error = err.Error()
		return ExitInvalidRevertAnchor
	}
	if err := verifyRevertAncestry(payload.Workdir, payload.TargetHash); err != nil {
		report.Status = "INVALID_REVERT_ANCHOR"
		report.Error = err.Error()
		return ExitInvalidRevertAnchor
	}
	if err := resetHardTo(payload.Workdir, payload.TargetHash); err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		return ExitInternalError
	}
	if err := cleanRevertWorkspace(payload.Workdir); err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		return ExitInternalError
	}
	report.Status = "SUCCESS"
	return ExitSuccess
}

func verifyRevertCurrentBranch(repo, targetBranch string) error {
	branch, err := currentBranch(repo)
	if err != nil {
		return fmt.Errorf("verify current branch for revert target_branch %q: %w", targetBranch, err)
	}
	if branch == "HEAD" {
		return fmt.Errorf("revert target_branch %q requires a checked-out branch; current repository state is detached HEAD", targetBranch)
	}
	if branch != targetBranch {
		return fmt.Errorf("revert target_branch %q does not match current branch %q", targetBranch, branch)
	}
	return nil
}

func verifyRevertTargetCommit(repo, targetHash string) error {
	out, err := runGit(repo, "rev-parse", "--verify", targetHash+"^{commit}")
	if err != nil {
		return fmt.Errorf("target_hash %q is not a commit object: %w", targetHash, err)
	}
	resolved := strings.TrimSpace(string(out))
	if !strings.EqualFold(resolved, targetHash) {
		return fmt.Errorf("target_hash %q is not the full commit object ID for this repository; resolved %q", targetHash, resolved)
	}
	return nil
}

func verifyRevertAncestry(repo, targetHash string) error {
	if _, err := runGit(repo, "merge-base", "--is-ancestor", targetHash, "HEAD"); err != nil {
		return fmt.Errorf("target_hash %q is not an ancestor of HEAD: %w", targetHash, err)
	}
	return nil
}

func cleanRevertWorkspace(repo string) error {
	if _, err := runGit(repo, "clean", "-ffdx", "-q"); err != nil {
		return err
	}
	return verifyRevertWorkspaceClean(repo)
}

func verifyRevertWorkspaceClean(repo string) error {
	if err := gitguard.EnsureClean(repo); err != nil {
		return err
	}
	ignored, err := ignoredFileSet(repo)
	if err != nil {
		return err
	}
	if len(ignored) > 0 {
		return errors.New(preExistingUntrackedError(ignored))
	}
	emptyDirs, err := emptyUntrackedDirSet(repo)
	if err != nil {
		return err
	}
	if len(emptyDirs) > 0 {
		return errors.New(preExistingUntrackedError(emptyDirs))
	}
	return nil
}

func parseAndValidatePayload(payloadJSON []byte, report *contracts.Report) (contracts.Payload, int) {
	payload, err := contracts.DecodePayload(payloadJSON)
	report.Action = payload.Action
	report.Workdir = payload.Workdir
	report.WorkDir = payload.WorkDir
	report.TargetBranch = payload.TargetBranch
	report.TargetHash = payload.TargetHash
	report.PayloadTrustBoundary = payload.PayloadTrustBoundary
	report.BebID = payload.BebID
	if contracts.ValidateTraceArtifacts(payload.TraceArtifacts) == nil {
		report.TraceArtifacts = append([]contracts.TraceArtifact{}, payload.TraceArtifacts...)
	}
	report.ValidationProfiles = append([]string{}, payload.ValidationProfiles...)
	report.ValidationProfileCapabilities = append([]string{}, payload.ResolvedValidationProfileCapabilities...)
	report.ResolvedValidationCommands = append([]string{}, payload.ResolvedValidationCommands...)
	report.ResolvedValidationArgv = copyArgv(payload.ResolvedValidationArgv)
	switch {
	case len(payload.ValidationProfiles) > 0:
		report.ValidationCommandSource = "profile"
		report.ValidationTrustBoundary = "repository-profile"
	case len(payload.ValidationCommands) > 0:
		report.ValidationCommandSource = "legacy"
		report.ValidationTrustBoundary = "trusted-local-legacy"
	default:
		report.ValidationCommandSource = "none"
		report.ValidationTrustBoundary = "none"
	}
	if err != nil {
		if field, entry, prefix, ok := contracts.HasProtectedDocsAllowlistEntry(payload); ok {
			report.Status = "UNAUTHORIZED_FILE_MUTATION"
			report.Error = fmt.Sprintf("%s entry %q matches protected %s path", field, entry, prefix)
			return contracts.Payload{}, ExitUnauthorizedMutation
		}
		report.Status = "INVALID_PAYLOAD"
		report.Error = err.Error()
		return contracts.Payload{}, ExitInvalidPayload
	}
	return payload, ExitSuccess
}

func runValidation(ctx context.Context, payload contracts.Payload) (validation.Result, error) {
	timeout := time.Duration(payload.TimeoutSeconds) * time.Second
	if len(payload.ValidationProfiles) > 0 {
		return validation.RunSpecs(ctx, payload.Workdir, payload.ResolvedValidationProfileSpecs, payload.MaxOutputBytes, timeout)
	}
	return validation.Run(ctx, payload.Workdir, payload.ResolvedValidationCommands, payload.MaxOutputBytes, timeout)
}

func copyArgv(argv [][]string) [][]string {
	if argv == nil {
		return nil
	}
	copy := make([][]string, len(argv))
	for i := range argv {
		copy[i] = append([]string{}, argv[i]...)
	}
	return copy
}

func existingAllowedNewFiles(repo string, allowedNew []string) ([]string, error) {
	produced := make([]string, 0, len(allowedNew))
	for _, rel := range allowedNew {
		fullPath := filepath.Join(repo, filepath.FromSlash(rel))
		_, err := os.Stat(fullPath)
		if err != nil {
			if os.IsNotExist(err) {
				continue
			}
			return nil, fmt.Errorf("stat allowed new path %q in %q: %w", rel, repo, err)
		}
		produced = append(produced, rel)
	}
	return produced, nil
}

func failPostCommitReportGeneration(repo string, gitBefore *gitSnapshot, dirBefore *worktreeDirModeSnapshot, report *contracts.Report, err error) int {
	report.Status = "INTERNAL_ERROR"
	report.Error = err.Error()
	report.CommitHash = ""
	if cleanupErr := cleanupFailedRun(repo, gitBefore, dirBefore); cleanupErr != nil {
		report.Error = cleanupErr.Error()
	}
	return ExitInternalError
}

func failUnauthorizedDirectoryModeMutation(repo string, dirBefore *worktreeDirModeSnapshot, gitBefore *gitSnapshot, report *contracts.Report, message string) int {
	mutations, err := dirBefore.ChangedPathsAndRestore()
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		if cleanupErr := cleanupFailedRun(repo, gitBefore, dirBefore); cleanupErr != nil {
			report.Error = cleanupErr.Error()
		}
		return ExitInternalError
	}
	if len(mutations) == 0 {
		return ExitSuccess
	}
	report.Status = "UNAUTHORIZED_FILE_MUTATION"
	report.DestroyedFiles = mutations
	report.Error = message
	if err := cleanupFailedRun(repo, gitBefore, dirBefore); err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		return ExitInternalError
	}
	return ExitUnauthorizedMutation
}

func failUnauthorizedValidationDirectoryModeMutation(repo string, dirBefore *worktreeDirModeSnapshot, gitBefore *gitSnapshot, preEngineHash string, report *contracts.Report) int {
	mutations, err := dirBefore.ChangedPathsAndRestore()
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		if cleanupErr := cleanupValidationFailedRun(repo, gitBefore, preEngineHash, dirBefore); cleanupErr != nil {
			report.Error = cleanupErr.Error()
		}
		return ExitInternalError
	}
	if len(mutations) == 0 {
		return ExitSuccess
	}
	report.Status = "UNAUTHORIZED_FILE_MUTATION"
	report.DestroyedFiles = mutations
	report.Error = "validation modified files outside the allowlist"
	if err := cleanupValidationFailedRun(repo, gitBefore, preEngineHash, dirBefore); err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		return ExitInternalError
	}
	return ExitUnauthorizedMutation
}

func failValidationMutationFromBaseline(repo string, baseline *validationBaseline, gitBefore *gitSnapshot, dirBefore *worktreeDirModeSnapshot, preEngineHash string, report *contracts.Report) int {
	mutations, err := baseline.ChangedPaths()
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		if cleanupErr := cleanupValidationFailedRun(repo, gitBefore, preEngineHash, dirBefore); cleanupErr != nil {
			report.Error = cleanupErr.Error()
		}
		return ExitInternalError
	}
	if len(mutations) == 0 {
		return ExitSuccess
	}
	report.Status = "UNAUTHORIZED_FILE_MUTATION"
	report.DestroyedFiles = mutations
	report.Error = "validation modified engine-produced candidate state"
	if err := cleanupValidationFailedRun(repo, gitBefore, preEngineHash, dirBefore); err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		return ExitInternalError
	}
	return ExitUnauthorizedMutation
}

func failUnauthorizedPhysicalResidue(repo string, allowedModified []string, allowedNew []string, baselineUntracked map[string]struct{}, gitBefore *gitSnapshot, dirBefore *worktreeDirModeSnapshot, report *contracts.Report, message string) int {
	residue, err := unauthorizedPhysicalResidue(repo, allowedModified, allowedNew, baselineUntracked)
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		if cleanupErr := cleanupFailedRun(repo, gitBefore, dirBefore); cleanupErr != nil {
			report.Error = cleanupErr.Error()
		}
		return ExitInternalError
	}
	if len(residue) == 0 {
		return ExitSuccess
	}
	report.Status = "UNAUTHORIZED_FILE_MUTATION"
	report.DestroyedFiles = residue
	report.Error = message
	if err := cleanupFailedRun(repo, gitBefore, dirBefore); err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		return ExitInternalError
	}
	return ExitUnauthorizedMutation
}

func failUnauthorizedAllowedNewPhysicalModes(repo string, producedAllowedNew []string, gitBefore *gitSnapshot, dirBefore *worktreeDirModeSnapshot, report *contracts.Report) int {
	residue, err := allowedNewPhysicalModeResidue(repo, producedAllowedNew, dirBefore)
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		if cleanupErr := cleanupFailedRun(repo, gitBefore, dirBefore); cleanupErr != nil {
			report.Error = cleanupErr.Error()
		}
		return ExitInternalError
	}
	if len(residue) == 0 {
		return ExitSuccess
	}
	report.Status = "UNAUTHORIZED_FILE_MUTATION"
	report.DestroyedFiles = residue
	report.Error = "engine modified files outside the allowlist"
	if err := cleanupFailedRun(repo, gitBefore, dirBefore); err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		return ExitInternalError
	}
	return ExitUnauthorizedMutation
}

func failUnauthorizedValidationResidue(repo string, allowedModified []string, allowedNew []string, baselineUntracked map[string]struct{}, gitBefore *gitSnapshot, dirBefore *worktreeDirModeSnapshot, preEngineHash string, report *contracts.Report) int {
	residue, err := unauthorizedPhysicalResidue(repo, allowedModified, allowedNew, baselineUntracked)
	if err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		if cleanupErr := cleanupValidationFailedRun(repo, gitBefore, preEngineHash, dirBefore); cleanupErr != nil {
			report.Error = cleanupErr.Error()
		}
		return ExitInternalError
	}
	if len(residue) == 0 {
		return ExitSuccess
	}
	report.Status = "UNAUTHORIZED_FILE_MUTATION"
	report.DestroyedFiles = residue
	report.Error = "validation modified files outside the allowlist"
	if err := cleanupValidationFailedRun(repo, gitBefore, preEngineHash, dirBefore); err != nil {
		report.Status = "INTERNAL_ERROR"
		report.Error = err.Error()
		return ExitInternalError
	}
	return ExitUnauthorizedMutation
}

func stagedDiffFiles(repo string) ([]string, error) {
	out, err := runGit(repo, "diff", "--cached", "--name-only", "-z")
	if err != nil {
		return nil, err
	}
	return splitNULPaths(out), nil
}

func currentHeadHash(repo string) (string, error) {
	out, err := runGit(repo, "rev-parse", "HEAD")
	if err != nil {
		return "", err
	}
	return strings.TrimSpace(string(out)), nil
}

func currentBranch(repo string) (string, error) {
	out, err := runGit(repo, "rev-parse", "--abbrev-ref", "HEAD")
	if err != nil {
		return "", err
	}
	branch := strings.TrimSpace(string(out))
	if branch == "" {
		return "", errors.New("git returned empty current branch")
	}
	return branch, nil
}

func gitDiffFromPreEngine(repo, preEngineHash string) (string, error) {
	out, err := runGit(repo, "diff", preEngineHash, "HEAD", "--")
	if err != nil {
		return "", err
	}
	return string(out), nil
}

func diffSummaryFromPreEngine(repo, preEngineHash string) (*contracts.DiffSummary, error) {
	out, err := runGit(repo, "diff", preEngineHash, "HEAD", "--numstat", "--")
	if err != nil {
		return nil, err
	}
	return parseNumstat(out)
}

func parseNumstat(out []byte) (*contracts.DiffSummary, error) {
	summary := &contracts.DiffSummary{Files: []string{}}
	for _, line := range strings.Split(strings.TrimRight(string(out), "\n"), "\n") {
		if line == "" {
			continue
		}
		parts := strings.SplitN(line, "\t", 3)
		if len(parts) != 3 {
			return nil, fmt.Errorf("parse git numstat line %q: expected insertions, deletions, and path", line)
		}
		insertions, err := parseNumstatCount(parts[0])
		if err != nil {
			return nil, fmt.Errorf("parse git numstat insertions for %q: %w", parts[2], err)
		}
		deletions, err := parseNumstatCount(parts[1])
		if err != nil {
			return nil, fmt.Errorf("parse git numstat deletions for %q: %w", parts[2], err)
		}
		summary.FilesChanged++
		summary.Insertions += insertions
		summary.Deletions += deletions
		summary.Files = append(summary.Files, parts[2])
	}
	return summary, nil
}

func parseNumstatCount(value string) (int, error) {
	if value == "-" {
		return 0, nil
	}
	return strconv.Atoi(value)
}

func unauthorizedPhysicalResidue(repo string, allowedModified []string, allowedNew []string, baselineUntracked map[string]struct{}) ([]string, error) {
	emptyDirs, err := emptyUntrackedDirs(repo)
	if err != nil {
		return nil, err
	}
	if len(emptyDirs) > 0 {
		if err := gitguard.MakeWorktreeDirsTraversable(repo); err != nil {
			return nil, err
		}
	}
	nestedGitDirs, err := nestedGitDirs(repo)
	if err != nil {
		return nil, err
	}

	unstaged, err := runGit(repo, "diff", "--name-only", "-z")
	if err != nil {
		return nil, err
	}
	untracked, err := untrackedFiles(repo)
	if err != nil {
		return nil, err
	}
	ignored, err := ignoredFileSet(repo)
	if err != nil {
		return nil, err
	}

	allowed := pathSet(append(append([]string{}, allowedModified...), allowedNew...))
	seen := map[string]struct{}{}
	addUnauthorized := func(rel string, honorBaseline bool) {
		if _, ok := allowed[rel]; ok {
			return
		}
		if honorBaseline {
			if _, ok := baselineUntracked[rel]; ok {
				return
			}
		}
		seen[rel] = struct{}{}
	}
	for _, rel := range splitNULPaths(unstaged) {
		addUnauthorized(rel, false)
	}
	for _, rel := range untracked {
		addUnauthorized(rel, true)
	}
	for rel := range ignored {
		addUnauthorized(rel, false)
	}
	for _, rel := range emptyDirs {
		addUnauthorized(rel, false)
	}
	for _, rel := range nestedGitDirs {
		addUnauthorized(rel, false)
	}
	paths := make([]string, 0, len(seen))
	for rel := range seen {
		paths = append(paths, rel)
	}
	sort.Strings(paths)
	return paths, nil
}

func allowedNewPhysicalModeResidue(repo string, producedAllowedNew []string, dirBefore *worktreeDirModeSnapshot) ([]string, error) {
	seen := map[string]struct{}{}
	for _, rel := range producedAllowedNew {
		fullPath := filepath.Join(repo, filepath.FromSlash(rel))
		info, err := os.Lstat(fullPath)
		if err != nil {
			if errors.Is(err, fs.ErrNotExist) {
				continue
			}
			return nil, fmt.Errorf("stat allowed new path %q in %q: %w", rel, repo, err)
		}
		switch {
		case info.Mode().IsRegular():
			normalizedMode, ok := safeAllowedNewRegularFileMode(info.Mode())
			if !ok {
				seen[rel] = struct{}{}
				break
			}
			if normalizedMode != worktreeDirChmodMode(info.Mode()) {
				if err := os.Chmod(fullPath, normalizedMode); err != nil {
					return nil, fmt.Errorf("normalize allowed new path %q in %q: %w", rel, repo, err)
				}
			}
		case info.Mode()&os.ModeSymlink != 0:
			// Symlinks do not carry hidden chmod bits that Git would discard.
		default:
			seen[rel] = struct{}{}
		}
		for parent := path.Dir(rel); parent != "." && parent != "/"; parent = path.Dir(parent) {
			if dirBefore != nil {
				if _, existedBefore := dirBefore.entries[parent]; existedBefore {
					continue
				}
			}
			parentPath := filepath.Join(repo, filepath.FromSlash(parent))
			parentInfo, err := os.Lstat(parentPath)
			if err != nil {
				if errors.Is(err, fs.ErrNotExist) {
					continue
				}
				return nil, fmt.Errorf("stat allowed new parent directory %q in %q: %w", worktreeModeReportPath(parent, true), repo, err)
			}
			if !parentInfo.IsDir() || worktreeDirChmodMode(parentInfo.Mode()) != 0o755 {
				seen[worktreeModeReportPath(parent, true)] = struct{}{}
			}
		}
	}
	paths := make([]string, 0, len(seen))
	for rel := range seen {
		paths = append(paths, rel)
	}
	sort.Strings(paths)
	return paths, nil
}

func safeAllowedNewRegularFileMode(mode os.FileMode) (os.FileMode, bool) {
	chmodMode := worktreeDirChmodMode(mode)
	if chmodMode&(os.ModeSetuid|os.ModeSetgid|os.ModeSticky) != 0 {
		return 0, false
	}
	switch chmodMode.Perm() {
	case 0o644, 0o664:
		return 0o644, true
	case 0o755:
		return 0o755, true
	default:
		return 0, false
	}
}

func untrackedFileSet(repo string) (map[string]struct{}, error) {
	paths, err := untrackedFiles(repo)
	if err != nil {
		return nil, err
	}
	return pathSet(paths), nil
}

func untrackedFiles(repo string) ([]string, error) {
	out, err := runGit(repo, "ls-files", "--others", "-z")
	if err != nil {
		return nil, err
	}
	return splitNULPaths(out), nil
}

func untrackedReportFiles(repo string) ([]string, error) {
	out, err := runGit(repo, "ls-files", "-z", "--others", "--exclude-standard", "--directory")
	if err != nil {
		return nil, err
	}
	return splitNULPaths(out), nil
}

func ignoredFileSet(repo string) (map[string]struct{}, error) {
	out, err := runGit(repo, "ls-files", "-z", "--others", "--ignored", "--exclude-standard")
	if err != nil {
		return nil, err
	}
	return pathSet(splitNULPaths(out)), nil
}

func emptyUntrackedDirSet(repo string) (map[string]struct{}, error) {
	paths, err := emptyUntrackedDirs(repo)
	if err != nil {
		return nil, err
	}
	return pathSet(paths), nil
}

func emptyUntrackedDirs(repo string) ([]string, error) {
	seen := map[string]struct{}{}
	addDirResidue := func(path string, d fs.DirEntry) (string, bool, error) {
		relOS, err := filepath.Rel(repo, path)
		if err != nil {
			return "", false, err
		}
		if relOS == "." {
			return "", false, nil
		}
		rel := filepath.ToSlash(relOS)
		if rel == ".git" {
			return rel, false, nil
		}

		isDir := false
		known := false
		if d != nil {
			isDir = d.IsDir()
			known = true
		}
		if !isDir {
			info, err := os.Lstat(path)
			if err == nil {
				isDir = info.IsDir()
				known = true
			} else if !errors.Is(err, fs.ErrNotExist) {
				known = false
			}
		}
		if isDir || !known {
			seen[rel+"/"] = struct{}{}
			return rel, true, nil
		}
		return rel, false, nil
	}

	if err := filepath.WalkDir(repo, func(path string, d fs.DirEntry, walkErr error) error {
		if walkErr != nil {
			rel, added, err := addDirResidue(path, d)
			if err != nil {
				return err
			}
			if rel == ".git" {
				return filepath.SkipDir
			}
			if !added {
				return walkErr
			}
			return filepath.SkipDir
		}
		if !d.IsDir() {
			return nil
		}
		relOS, err := filepath.Rel(repo, path)
		if err != nil {
			return err
		}
		if relOS == "." {
			return nil
		}
		rel := filepath.ToSlash(relOS)
		if rel == ".git" {
			return filepath.SkipDir
		}
		entries, err := os.ReadDir(path)
		if err != nil {
			if _, _, addErr := addDirResidue(path, d); addErr != nil {
				return addErr
			}
			return filepath.SkipDir
		}
		if len(entries) == 0 {
			seen[rel+"/"] = struct{}{}
		}
		if d.Name() == ".git" {
			return filepath.SkipDir
		}
		return nil
	}); err != nil {
		return nil, fmt.Errorf("scan empty untracked directories in %q: %w", repo, err)
	}
	paths := make([]string, 0, len(seen))
	for path := range seen {
		paths = append(paths, path)
	}
	sort.Strings(paths)
	return paths, nil
}

func preExistingUntrackedError(paths map[string]struct{}) string {
	items := make([]string, 0, len(paths))
	for path := range paths {
		items = append(items, path)
	}
	sort.Strings(items)
	return "git worktree has pre-existing untracked or ignored files:\n" + strings.Join(items, "\n")
}

func nestedGitDirSet(repo string) (map[string]struct{}, error) {
	paths, err := nestedGitDirs(repo)
	if err != nil {
		return nil, err
	}
	return pathSet(paths), nil
}

func nestedGitDirs(repo string) ([]string, error) {
	root, err := filepath.Abs(repo)
	if err != nil {
		return nil, fmt.Errorf("resolve worktree root %q: %w", repo, err)
	}
	root = filepath.Clean(root)
	rootGit := filepath.Join(root, ".git")
	seen := map[string]struct{}{}

	if err := filepath.WalkDir(root, func(path string, d fs.DirEntry, walkErr error) error {
		if walkErr != nil {
			if filepath.Base(path) == ".git" && filepath.Clean(path) != rootGit {
				relOS, err := filepath.Rel(root, path)
				if err != nil {
					return err
				}
				if relOS != "." && !strings.HasPrefix(relOS, ".."+string(filepath.Separator)) && relOS != ".." {
					seen[filepath.ToSlash(relOS)+"/"] = struct{}{}
				}
			}
			if d != nil && d.IsDir() {
				return filepath.SkipDir
			}
			return nil
		}
		if !d.IsDir() {
			return nil
		}
		cleanPath := filepath.Clean(path)
		if cleanPath == rootGit {
			return filepath.SkipDir
		}
		if d.Name() != ".git" {
			return nil
		}
		relOS, err := filepath.Rel(root, cleanPath)
		if err != nil {
			return err
		}
		if relOS != "." && !strings.HasPrefix(relOS, ".."+string(filepath.Separator)) && relOS != ".." {
			seen[filepath.ToSlash(relOS)+"/"] = struct{}{}
		}
		return filepath.SkipDir
	}); err != nil {
		return nil, fmt.Errorf("scan nested .git directories in %q: %w", repo, err)
	}

	paths := make([]string, 0, len(seen))
	for path := range seen {
		paths = append(paths, path)
	}
	sort.Strings(paths)
	return paths, nil
}

func pathSet(paths []string) map[string]struct{} {
	set := make(map[string]struct{}, len(paths))
	for _, path := range paths {
		set[path] = struct{}{}
	}
	return set
}

func mergePathSets(sets ...map[string]struct{}) map[string]struct{} {
	merged := map[string]struct{}{}
	for _, set := range sets {
		for path := range set {
			merged[path] = struct{}{}
		}
	}
	return merged
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

func cleanupFailedRun(repo string, gitBefore *gitSnapshot, dirBefore ...*worktreeDirModeSnapshot) error {
	dirSnapshot := optionalWorktreeDirModeSnapshot(dirBefore)
	if dirSnapshot != nil {
		if err := dirSnapshot.RestoreExisting(); err != nil {
			return err
		}
	}
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
	if dirSnapshot != nil {
		if err := dirSnapshot.RestoreExisting(); err != nil {
			return err
		}
	}
	return nil
}

func cleanupValidationFailedRun(repo string, gitBefore *gitSnapshot, preEngineHash string, dirBefore ...*worktreeDirModeSnapshot) error {
	dirSnapshot := optionalWorktreeDirModeSnapshot(dirBefore)
	if dirSnapshot != nil {
		if err := dirSnapshot.RestoreExisting(); err != nil {
			return err
		}
	}
	if gitBefore != nil {
		if err := gitBefore.Restore(); err != nil {
			return fmt.Errorf("restore git metadata: %w", err)
		}
	}
	if err := resetHardTo(repo, preEngineHash); err != nil {
		return err
	}
	if err := gitguard.CleanupUnauthorized(repo); err != nil {
		return err
	}
	if dirSnapshot != nil {
		if err := dirSnapshot.RestoreExisting(); err != nil {
			return err
		}
	}
	return nil
}

func optionalWorktreeDirModeSnapshot(snapshots []*worktreeDirModeSnapshot) *worktreeDirModeSnapshot {
	if len(snapshots) == 0 {
		return nil
	}
	return snapshots[0]
}

func resetHard(repo string) error {
	_, err := runGit(repo, "reset", "--hard", "HEAD")
	return err
}

func resetHardTo(repo, ref string) error {
	_, err := runGit(repo, "reset", "--hard", ref)
	return err
}

type validationBaseline struct {
	git      *gitSnapshot
	worktree *physicalWorktreeSnapshot
}

func snapshotValidationBaseline(repo string) (*validationBaseline, error) {
	gitSnapshot, err := snapshotGitDir(repo)
	if err != nil {
		return nil, err
	}
	worktreeSnapshot, err := snapshotPhysicalWorktree(repo, gitSnapshot.root)
	if err != nil {
		return nil, err
	}
	return &validationBaseline{git: gitSnapshot, worktree: worktreeSnapshot}, nil
}

func (b *validationBaseline) ChangedPaths() ([]string, error) {
	if b == nil {
		return []string{}, nil
	}
	changed := []string{}
	if b.git != nil {
		gitPaths, err := b.git.ChangedPaths()
		if err != nil {
			return nil, err
		}
		changed = append(changed, gitPaths...)
	}
	if b.worktree != nil {
		worktreePaths, err := b.worktree.ChangedPaths()
		if err != nil {
			return nil, err
		}
		changed = append(changed, worktreePaths...)
	}
	return uniqueSorted(changed), nil
}

type physicalWorktreeSnapshot struct {
	root    string
	gitRoot string
	entries map[string]gitSnapshotEntry
}

func snapshotPhysicalWorktree(repo, gitRoot string) (*physicalWorktreeSnapshot, error) {
	root, err := filepath.Abs(repo)
	if err != nil {
		return nil, fmt.Errorf("resolve worktree root %q: %w", repo, err)
	}
	root = filepath.Clean(root)
	absGitRoot := ""
	if gitRoot != "" {
		absGitRoot, err = filepath.Abs(gitRoot)
		if err != nil {
			return nil, fmt.Errorf("resolve git root %q: %w", gitRoot, err)
		}
		absGitRoot = filepath.Clean(absGitRoot)
	}
	entries, err := snapshotPhysicalWorktreeEntries(root, absGitRoot)
	if err != nil {
		return nil, err
	}
	return &physicalWorktreeSnapshot{root: root, gitRoot: absGitRoot, entries: entries}, nil
}

func snapshotPhysicalWorktreeEntries(root, gitRoot string) (map[string]gitSnapshotEntry, error) {
	entries := map[string]gitSnapshotEntry{}
	if err := filepath.WalkDir(root, func(entryPath string, d fs.DirEntry, walkErr error) error {
		relOS, relErr := filepath.Rel(root, entryPath)
		if relErr != nil {
			return relErr
		}
		rel := filepath.ToSlash(relOS)
		if relOS == "." {
			info, err := os.Lstat(entryPath)
			if err != nil {
				if walkErr != nil {
					return walkErr
				}
				return err
			}
			entries["."] = gitSnapshotEntry{mode: info.Mode(), isDir: info.IsDir()}
			return walkErr
		}
		if isRootGitMetadataPath(root, gitRoot, entryPath) {
			if d != nil && d.IsDir() {
				return filepath.SkipDir
			}
			return nil
		}
		if walkErr != nil {
			info, err := os.Lstat(entryPath)
			if err != nil {
				return walkErr
			}
			if info.IsDir() {
				entries[rel] = gitSnapshotEntry{mode: info.Mode(), isDir: true}
				return filepath.SkipDir
			}
			return walkErr
		}
		entry, err := physicalSnapshotEntry(entryPath, rel)
		if err != nil {
			return err
		}
		entries[rel] = entry
		return nil
	}); err != nil {
		return nil, fmt.Errorf("snapshot physical worktree %q: %w", root, err)
	}
	return entries, nil
}

func physicalSnapshotEntry(entryPath, rel string) (gitSnapshotEntry, error) {
	info, err := os.Lstat(entryPath)
	if err != nil {
		return gitSnapshotEntry{}, err
	}
	entry := gitSnapshotEntry{mode: info.Mode(), isDir: info.IsDir(), size: info.Size(), modTime: info.ModTime()}
	switch {
	case info.IsDir():
	case info.Mode()&os.ModeSymlink != 0:
		entry.link, err = os.Readlink(entryPath)
		if err != nil {
			return gitSnapshotEntry{}, err
		}
	case info.Mode().IsRegular():
		if contracts.IsProtectedDocsPath(rel) {
			entry.metadataOnly = true
			return entry, nil
		}
		entry.data, err = os.ReadFile(entryPath)
		if err != nil {
			return gitSnapshotEntry{}, err
		}
	default:
		// Preserve kind/mode for unsupported physical residue such as FIFOs so
		// validation-created entries are still detectable without blocking cleanup.
	}
	return entry, nil
}

func isRootGitMetadataPath(root, gitRoot, entryPath string) bool {
	if gitRoot == "" {
		return false
	}
	if rel, ok := relativeWorktreeDir(root, gitRoot); !ok || rel != ".git" {
		return false
	}
	return filepath.Clean(entryPath) == gitRoot
}

func (s *physicalWorktreeSnapshot) ChangedPaths() ([]string, error) {
	if s == nil {
		return []string{}, nil
	}
	current, err := snapshotPhysicalWorktree(s.root, s.gitRoot)
	if err != nil {
		return nil, err
	}
	changed := map[string]struct{}{}
	for rel, before := range s.entries {
		after, ok := current.entries[rel]
		if !ok || !before.equal(after) {
			changed[physicalWorktreeReportPath(rel, before)] = struct{}{}
		}
	}
	for rel, after := range current.entries {
		if _, ok := s.entries[rel]; !ok {
			changed[physicalWorktreeReportPath(rel, after)] = struct{}{}
		}
	}
	paths := make([]string, 0, len(changed))
	for path := range changed {
		paths = append(paths, path)
	}
	sort.Strings(paths)
	return paths, nil
}

func physicalWorktreeReportPath(rel string, entry gitSnapshotEntry) string {
	return worktreeModeReportPath(rel, entry.isDir)
}

type worktreeDirModeSnapshot struct {
	root    string
	entries map[string]worktreeDirModeEntry
}

type worktreeDirModeEntry struct {
	mode  os.FileMode
	isDir bool
}

const worktreeDirChmodModeMask = os.ModePerm | os.ModeSetuid | os.ModeSetgid | os.ModeSticky

func worktreeDirChmodMode(mode os.FileMode) os.FileMode {
	return mode & worktreeDirChmodModeMask
}

func snapshotWorktreeDirModes(repo, gitRoot string) (*worktreeDirModeSnapshot, error) {
	root, err := filepath.Abs(repo)
	if err != nil {
		return nil, fmt.Errorf("resolve worktree root %q: %w", repo, err)
	}
	dirs := map[string]struct{}{".": {}}
	files := map[string]struct{}{}
	if gitRoot != "" {
		absGitRoot, err := filepath.Abs(gitRoot)
		if err != nil {
			return nil, fmt.Errorf("resolve git root %q: %w", gitRoot, err)
		}
		if rel, ok := relativeWorktreeDir(root, absGitRoot); ok && rel == ".git" {
			dirs[rel] = struct{}{}
		}
	}
	tracked, err := runGit(repo, "ls-files", "-z")
	if err != nil {
		return nil, err
	}
	for _, file := range splitNULPaths(tracked) {
		files[file] = struct{}{}
		for dir := path.Dir(file); dir != "." && dir != "/"; dir = path.Dir(dir) {
			dirs[dir] = struct{}{}
		}
	}

	rels := sortedDirModeRels(dirs)
	entries := make(map[string]worktreeDirModeEntry, len(rels)+len(files))
	for _, rel := range rels {
		path := worktreeDirModePath(root, rel)
		info, err := os.Lstat(path)
		if err != nil {
			return nil, fmt.Errorf("snapshot worktree directory mode %q: %w", worktreeModeReportPath(rel, true), err)
		}
		if !info.IsDir() {
			continue
		}
		entries[rel] = worktreeDirModeEntry{mode: worktreeDirChmodMode(info.Mode()), isDir: true}
	}
	for _, rel := range sortedDirModeRels(files) {
		path := worktreeDirModePath(root, rel)
		info, err := os.Lstat(path)
		if err != nil {
			return nil, fmt.Errorf("snapshot tracked file mode %q: %w", worktreeModeReportPath(rel, false), err)
		}
		if !info.Mode().IsRegular() {
			continue
		}
		entries[rel] = worktreeDirModeEntry{mode: worktreeDirChmodMode(info.Mode()), isDir: false}
	}
	return &worktreeDirModeSnapshot{root: root, entries: entries}, nil
}

func relativeWorktreeDir(root, path string) (string, bool) {
	relOS, err := filepath.Rel(root, path)
	if err != nil || relOS == "." || strings.HasPrefix(relOS, ".."+string(filepath.Separator)) || relOS == ".." {
		return "", false
	}
	return filepath.ToSlash(relOS), true
}

func (s *worktreeDirModeSnapshot) ChangedPathsAndRestore() ([]string, error) {
	if s == nil {
		return []string{}, nil
	}
	changed := map[string]struct{}{}
	for _, rel := range sortedDirModeRels(s.entryRelSet()) {
		entry := s.entries[rel]
		path := worktreeDirModePath(s.root, rel)
		info, err := os.Lstat(path)
		if err != nil {
			if errors.Is(err, fs.ErrNotExist) {
				continue
			}
			return nil, fmt.Errorf("stat worktree path %q: %w", worktreeModeReportPath(rel, entry.isDir), err)
		}
		if info.IsDir() != entry.isDir || (!entry.isDir && !info.Mode().IsRegular()) {
			continue
		}
		if worktreeDirChmodMode(info.Mode()) == entry.mode {
			continue
		}
		changed[worktreeModeReportPath(rel, entry.isDir)] = struct{}{}
		if err := os.Chmod(path, entry.mode); err != nil {
			return nil, fmt.Errorf("restore worktree path mode %q: %w", worktreeModeReportPath(rel, entry.isDir), err)
		}
	}
	paths := make([]string, 0, len(changed))
	for path := range changed {
		paths = append(paths, path)
	}
	sort.Strings(paths)
	return paths, nil
}

func (s *worktreeDirModeSnapshot) RestoreExisting() error {
	if s == nil {
		return nil
	}
	for _, rel := range sortedDirModeRels(s.entryRelSet()) {
		entry := s.entries[rel]
		path := worktreeDirModePath(s.root, rel)
		info, err := os.Lstat(path)
		if err != nil {
			if errors.Is(err, fs.ErrNotExist) {
				continue
			}
			return fmt.Errorf("stat worktree path %q: %w", worktreeModeReportPath(rel, entry.isDir), err)
		}
		if info.IsDir() != entry.isDir || (!entry.isDir && !info.Mode().IsRegular()) || worktreeDirChmodMode(info.Mode()) == entry.mode {
			continue
		}
		if err := os.Chmod(path, entry.mode); err != nil {
			return fmt.Errorf("restore worktree path mode %q: %w", worktreeModeReportPath(rel, entry.isDir), err)
		}
	}
	return nil
}

func (s *worktreeDirModeSnapshot) entryRelSet() map[string]struct{} {
	rels := make(map[string]struct{}, len(s.entries))
	for rel := range s.entries {
		rels[rel] = struct{}{}
	}
	return rels
}

func sortedDirModeRels(rels map[string]struct{}) []string {
	out := make([]string, 0, len(rels))
	for rel := range rels {
		out = append(out, rel)
	}
	sort.Slice(out, func(i, j int) bool {
		if dirDepth(out[i]) == dirDepth(out[j]) {
			return out[i] < out[j]
		}
		return dirDepth(out[i]) < dirDepth(out[j])
	})
	return out
}

func dirDepth(rel string) int {
	if rel == "." {
		return 0
	}
	return strings.Count(rel, "/") + 1
}

func worktreeDirModePath(root, rel string) string {
	if rel == "." {
		return root
	}
	return filepath.Join(root, filepath.FromSlash(rel))
}

func worktreeDirModeReportPath(rel string) string {
	return worktreeModeReportPath(rel, true)
}

func worktreeModeReportPath(rel string, isDir bool) string {
	if rel == "." {
		return "."
	}
	if !isDir {
		return rel
	}
	return rel + "/"
}

type gitSnapshot struct {
	root    string
	entries map[string]gitSnapshotEntry
}

type gitSnapshotEntry struct {
	mode         os.FileMode
	data         []byte
	link         string
	isDir        bool
	metadataOnly bool
	size         int64
	modTime      time.Time
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
	entries, err := snapshotPathEntries(root, false)
	if err != nil {
		return nil, err
	}
	return &gitSnapshot{root: root, entries: entries}, nil
}

func (s *gitSnapshot) ChangedPaths() ([]string, error) {
	current, err := snapshotPathEntries(s.root, true)
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
	if err := makeGitDirsTraversable(s.root); err != nil {
		return err
	}
	current, err := snapshotPathEntries(s.root, true)
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
	removePaths := make([]string, 0)
	for rel, currentEntry := range current {
		beforeEntry, existed := s.entries[rel]
		if !existed || !beforeEntry.sameKind(currentEntry) {
			removePaths = append(removePaths, rel)
		}
	}
	sort.Slice(removePaths, func(i, j int) bool { return len(removePaths[i]) > len(removePaths[j]) })
	for _, rel := range removePaths {
		if err := os.RemoveAll(filepath.Join(s.root, filepath.FromSlash(rel))); err != nil {
			return fmt.Errorf("remove replaced git entry %q: %w", gitReportPath(rel), err)
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
		if err := os.Chmod(path, gitChmodMode(entry.mode)); err != nil {
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
		if err := os.Chmod(path, gitChmodMode(entry.mode)); err != nil {
			return fmt.Errorf("chmod git file %q: %w", gitReportPath(rel), err)
		}
	}
	return nil
}

func makeGitDirsTraversable(root string) error {
	info, err := os.Lstat(root)
	if err != nil {
		if errors.Is(err, fs.ErrNotExist) {
			return nil
		}
		return fmt.Errorf("stat git root %q: %w", root, err)
	}
	if !info.IsDir() {
		return nil
	}
	return makeGitDirAndChildrenTraversable(root)
}

func makeGitDirAndChildrenTraversable(dir string) error {
	info, err := os.Lstat(dir)
	if err != nil {
		if errors.Is(err, fs.ErrNotExist) {
			return nil
		}
		return fmt.Errorf("stat git directory %q: %w", dir, err)
	}
	if !info.IsDir() {
		return nil
	}
	if err := chmodGitDirOwnerRWX(dir, info.Mode()); err != nil {
		return err
	}
	entries, err := os.ReadDir(dir)
	if err != nil {
		if errors.Is(err, fs.ErrNotExist) {
			return nil
		}
		return fmt.Errorf("read git directory %q: %w", dir, err)
	}
	for _, entry := range entries {
		path := filepath.Join(dir, entry.Name())
		info, err := os.Lstat(path)
		if err != nil {
			if errors.Is(err, fs.ErrNotExist) {
				continue
			}
			return fmt.Errorf("stat git entry %q: %w", path, err)
		}
		if !info.IsDir() {
			continue
		}
		if err := makeGitDirAndChildrenTraversable(path); err != nil {
			return err
		}
	}
	return nil
}

func chmodGitDirOwnerRWX(path string, mode os.FileMode) error {
	current := gitChmodMode(mode)
	want := current | 0o700
	if want == current {
		return nil
	}
	if err := os.Chmod(path, want); err != nil {
		return fmt.Errorf("chmod git directory %q: %w", path, err)
	}
	return nil
}

func gitChmodMode(mode os.FileMode) os.FileMode {
	return mode & worktreeDirChmodModeMask
}

func snapshotPathEntries(root string, allowUnsupported bool) (map[string]gitSnapshotEntry, error) {
	entries := map[string]gitSnapshotEntry{}
	if err := filepath.WalkDir(root, func(path string, d fs.DirEntry, walkErr error) error {
		relOS, relErr := filepath.Rel(root, path)
		if relErr != nil {
			return relErr
		}
		if relOS == "." {
			return walkErr
		}
		rel := filepath.ToSlash(relOS)
		if walkErr != nil {
			if !allowUnsupported {
				return walkErr
			}
			info, err := os.Lstat(path)
			if err != nil {
				return walkErr
			}
			if !info.IsDir() {
				return walkErr
			}
			entries[rel] = gitSnapshotEntry{mode: info.Mode(), isDir: true}
			return filepath.SkipDir
		}
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
			if allowUnsupported {
				break
			}
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
	if e.metadataOnly || other.metadataOnly {
		return e.mode == other.mode &&
			e.link == other.link &&
			e.isDir == other.isDir &&
			e.metadataOnly == other.metadataOnly &&
			e.size == other.size &&
			e.modTime.Equal(other.modTime)
	}
	return e.mode == other.mode && e.link == other.link && e.isDir == other.isDir && bytes.Equal(e.data, other.data)
}

func (e gitSnapshotEntry) sameKind(other gitSnapshotEntry) bool {
	return e.kind() == other.kind()
}

func (e gitSnapshotEntry) kind() string {
	switch {
	case e.isDir:
		return "dir"
	case e.mode&os.ModeSymlink != 0:
		return "symlink"
	case e.mode.IsRegular():
		return "file"
	default:
		return "unsupported"
	}
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
	result, err := gitguard.RunGit(context.Background(), repo, args...)
	return result.Stdout, err
}
