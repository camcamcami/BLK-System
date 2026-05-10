package gitguard

import (
	"context"
	"fmt"
	"strings"
	"unicode"
)

const hardenedGitSSHCommand = "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o BatchMode=yes"

// BranchPreparation describes the branch preparation path taken for an execute
// payload target_branch.
type BranchPreparation struct {
	OrphanCreated bool
}

// TargetHeadError marks an exact-target local preparation failure before the
// tactical engine may run. It is distinct from infrastructure failures so
// callers can fail closed without reporting a broken runner.
type TargetHeadError struct {
	Reason string
}

func (e *TargetHeadError) Error() string {
	return e.Reason
}

// ValidateBranchName applies a conservative, git-compatible branch-name policy
// before a target branch is ever passed to Git as argv. It intentionally rejects
// revision syntax, path traversal, pathspec metacharacters, shell metacharacters,
// whitespace/control characters, and option-like names.
func ValidateBranchName(name string) error {
	if name == "" {
		return fmt.Errorf("target_branch must not be empty")
	}
	if strings.TrimSpace(name) != name {
		return fmt.Errorf("target_branch %q must not start or end with whitespace", name)
	}
	if strings.HasPrefix(name, "-") {
		return fmt.Errorf("target_branch %q must not start with -", name)
	}
	if name == "HEAD" || strings.HasPrefix(name, "refs/") {
		return fmt.Errorf("target_branch %q must be a branch name, not a ref or reserved revision", name)
	}
	if strings.HasPrefix(name, "/") || strings.HasSuffix(name, "/") || strings.Contains(name, "//") {
		return fmt.Errorf("target_branch %q must be a clean relative branch name", name)
	}
	if strings.Contains(name, "..") {
		return fmt.Errorf("target_branch %q must not contain path traversal or revision range syntax", name)
	}
	if strings.Contains(name, "@{") || name == "@" {
		return fmt.Errorf("target_branch %q must not contain git reflog syntax", name)
	}
	if strings.HasSuffix(name, ".") {
		return fmt.Errorf("target_branch %q must not end with .", name)
	}
	for _, r := range name {
		if unicode.IsSpace(r) || unicode.IsControl(r) {
			return fmt.Errorf("target_branch %q must not contain whitespace or control characters", name)
		}
		switch r {
		case ';', '&', '|', '$', '`', '<', '>', '(', ')', '{', '}', '[', ']', '*', '?', '!', '#', '\'', '"', '\\', ':', '~', '^':
			return fmt.Errorf("target_branch %q contains unsafe git, shell, or revision metacharacter %q", name, r)
		}
	}
	for _, part := range strings.Split(name, "/") {
		if part == "" || part == "." || part == ".." {
			return fmt.Errorf("target_branch %q must not contain empty, ., or .. path components", name)
		}
		if strings.HasPrefix(part, ".") {
			return fmt.Errorf("target_branch %q must not contain hidden ref path components", name)
		}
		if strings.HasSuffix(part, ".lock") {
			return fmt.Errorf("target_branch %q must not contain .lock ref path components", name)
		}
	}
	return nil
}

// PrepareTargetBranch deterministically prepares repo on targetBranch for an
// execute payload. It rejects a dirty current workspace before switching, fetches
// origin when present, checks out an existing local or remote-tracking branch, or
// creates an initialized empty orphan branch as a final fallback.
func PrepareTargetBranch(ctx context.Context, repo string, targetBranch string) (BranchPreparation, error) {
	if err := ValidateBranchName(targetBranch); err != nil {
		return BranchPreparation{}, err
	}
	if err := EnsureClean(repo); err != nil {
		return BranchPreparation{}, err
	}

	origin := hasOriginRemote(ctx, repo)
	if origin {
		if _, err := RunGit(ctx, repo, "fetch", "origin"); err != nil {
			return BranchPreparation{}, err
		}
	}

	if localBranchExists(ctx, repo, targetBranch) {
		if _, err := RunGit(ctx, repo, "checkout", targetBranch); err != nil {
			return BranchPreparation{}, err
		}
		return BranchPreparation{}, nil
	}

	if origin && remoteBranchAvailable(ctx, repo, targetBranch) {
		if _, err := RunGit(ctx, repo, "checkout", "-t", "origin/"+targetBranch); err != nil {
			return BranchPreparation{}, err
		}
		return BranchPreparation{}, nil
	}

	if _, err := RunGit(ctx, repo, "checkout", "--orphan", targetBranch); err != nil {
		return BranchPreparation{}, err
	}
	if _, err := RunGit(ctx, repo, "read-tree", "--empty"); err != nil {
		return BranchPreparation{}, err
	}
	if _, err := RunGit(ctx, repo, "-c", "core.hooksPath=/dev/null", "commit", "--allow-empty", "-m", "Initialize branch"); err != nil {
		return BranchPreparation{}, err
	}
	return BranchPreparation{OrphanCreated: true}, nil
}

// PrepareExactTargetBranch prepares an already-local target branch for an
// execute payload pinned to targetHash. It intentionally does not fetch, probe
// ls-remote, checkout remote-tracking branches, or create orphan branches: an
// exact target hash cannot be retargeted by network discovery.
func PrepareExactTargetBranch(ctx context.Context, repo string, targetBranch string, targetHash string) (BranchPreparation, error) {
	if err := ValidateBranchName(targetBranch); err != nil {
		return BranchPreparation{}, err
	}
	if err := EnsureClean(repo); err != nil {
		return BranchPreparation{}, err
	}
	if !localBranchExists(ctx, repo, targetBranch) {
		return BranchPreparation{}, &TargetHeadError{Reason: fmt.Sprintf("exact-target local mode requires existing local branch %q; remote fetch/checkout is not permitted", targetBranch)}
	}
	if _, err := RunGit(ctx, repo, "checkout", targetBranch); err != nil {
		return BranchPreparation{}, err
	}
	if err := VerifyCurrentHead(ctx, repo, targetHash); err != nil {
		return BranchPreparation{}, err
	}
	return BranchPreparation{}, nil
}

// VerifyCurrentHead requires the repository HEAD to equal the approval-bound
// target_hash before an exact-target execute payload may start its engine.
func VerifyCurrentHead(ctx context.Context, repo string, targetHash string) error {
	result, err := RunGit(ctx, repo, "rev-parse", "HEAD")
	if err != nil {
		return err
	}
	current := strings.TrimSpace(string(result.Stdout))
	if current != targetHash {
		return &TargetHeadError{Reason: fmt.Sprintf("current HEAD %q does not match target_hash %q", current, targetHash)}
	}
	return nil
}

func hasOriginRemote(ctx context.Context, repo string) bool {
	result, err := RunGit(ctx, repo, "remote")
	if err != nil {
		return false
	}
	for _, remote := range strings.Fields(string(result.Stdout)) {
		if remote == "origin" {
			return true
		}
	}
	return false
}

func localBranchExists(ctx context.Context, repo, branch string) bool {
	_, err := RunGit(ctx, repo, "show-ref", "--verify", "--quiet", "refs/heads/"+branch)
	return err == nil
}

func remoteBranchAvailable(ctx context.Context, repo, branch string) bool {
	if remoteTrackingBranchExists(ctx, repo, branch) {
		return true
	}
	if !lsRemoteBranchExists(ctx, repo, branch) {
		return false
	}
	_, err := RunGit(ctx, repo, "fetch", "origin", "refs/heads/"+branch+":refs/remotes/origin/"+branch)
	if err != nil {
		return false
	}
	return remoteTrackingBranchExists(ctx, repo, branch)
}

func remoteTrackingBranchExists(ctx context.Context, repo, branch string) bool {
	_, err := RunGit(ctx, repo, "show-ref", "--verify", "--quiet", "refs/remotes/origin/"+branch)
	return err == nil
}

func lsRemoteBranchExists(ctx context.Context, repo, branch string) bool {
	result, err := RunGitWithEnv(ctx, repo, []string{"GIT_SSH_COMMAND=" + hardenedGitSSHCommand}, "ls-remote", "--symref", "--heads", "origin", "refs/heads/"+branch)
	if err != nil {
		return false
	}
	return strings.TrimSpace(string(result.Stdout)) != ""
}
