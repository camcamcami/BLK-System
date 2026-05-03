package gitguard

import (
	"context"
)

// DirtyError reports a repository that has tracked or untracked changes.
type DirtyError struct {
	Status string
}

func (e *DirtyError) Error() string {
	return "git worktree is dirty:\n" + e.Status
}

// EnsureClean verifies repo has no tracked or untracked changes according to
// git status --porcelain with an explicit untracked-file mode.
func EnsureClean(repo string) error {
	result, err := RunGit(context.Background(), repo, "status", "--porcelain", "--untracked-files=all")
	if err != nil {
		return err
	}
	out := result.Stdout
	if len(out) == 0 {
		return nil
	}
	return &DirtyError{Status: string(out)}
}
