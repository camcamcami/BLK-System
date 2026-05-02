package gitguard

import (
	"fmt"
	"os/exec"
	"strings"
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
	if err := runCleanupGit(repo, "clean", "-ffdx"); err != nil {
		return err
	}
	return nil
}

func runCleanupGit(repo string, args ...string) error {
	cmd := exec.Command("git", args...)
	cmd.Dir = repo
	cmd.Env = gitEnv()

	out, err := cmd.CombinedOutput()
	if err != nil {
		if msg := strings.TrimSpace(string(out)); msg != "" {
			return fmt.Errorf("git %s in %q: %w: %s", strings.Join(args, " "), repo, err, msg)
		}
		return fmt.Errorf("git %s in %q: %w", strings.Join(args, " "), repo, err)
	}
	return nil
}
