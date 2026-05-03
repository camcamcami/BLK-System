package gitguard

import (
	"context"
)

// CleanupUnauthorized removes unstaged worktree mutations after allowlisted paths
// have already been explicitly staged. It must only be called after staging the
// complete allowlist, because it reverts all remaining unstaged tracked changes
// and deletes all remaining untracked files/directories, including ignored paths
// and nested Git repositories, in repo.
func CleanupUnauthorized(repo string) error {
	if err := runCleanupGit(repo, "checkout", "--", "."); err != nil {
		return err
	}
	if err := runCleanupGit(repo, "clean", "-ffdx", "-q"); err != nil {
		return err
	}
	return nil
}

func runCleanupGit(repo string, args ...string) error {
	_, err := RunGit(context.Background(), repo, args...)
	return err
}
