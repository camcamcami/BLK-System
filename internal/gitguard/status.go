package gitguard

import (
	"fmt"
	"os"
	"os/exec"
	"strings"
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
	cmd := exec.Command("git", "status", "--porcelain", "--untracked-files=all")
	cmd.Dir = repo
	cmd.Env = gitEnv()

	out, err := cmd.CombinedOutput()
	if err != nil {
		if msg := strings.TrimSpace(string(out)); msg != "" {
			return fmt.Errorf("git status --porcelain --untracked-files=all in %q: %w: %s", repo, err, msg)
		}
		return fmt.Errorf("git status --porcelain --untracked-files=all in %q: %w", repo, err)
	}
	if len(out) == 0 {
		return nil
	}
	return &DirtyError{Status: string(out)}
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
