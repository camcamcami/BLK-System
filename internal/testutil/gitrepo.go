package testutil

import (
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"testing"
)

// NewGitRepo creates a temporary Git repository with local author identity and
// a single initial commit, returning the repository path.
func NewGitRepo(t testing.TB) string {
	t.Helper()

	repo := t.TempDir()
	RunGit(t, repo, "init")
	RunGit(t, repo, "config", "--local", "user.name", "BLK Test")
	RunGit(t, repo, "config", "--local", "user.email", "blk-test@example.invalid")
	RunGit(t, repo, "config", "--local", "commit.gpgsign", "false")

	WriteFile(t, repo, "README.md", "initial\n")
	RunGit(t, repo, "add", "--", "README.md")
	RunGit(t, repo, "commit", "-m", "initial commit")

	return repo
}

// WriteFile writes content to rel under repo, creating parent directories as
// needed.
func WriteFile(t testing.TB, repo string, rel string, content string) {
	t.Helper()

	path := filepath.Join(repo, rel)
	if err := os.MkdirAll(filepath.Dir(path), 0o755); err != nil {
		t.Fatalf("create parent directories for %q: %v", path, err)
	}
	if err := os.WriteFile(path, []byte(content), 0o644); err != nil {
		t.Fatalf("write %q: %v", path, err)
	}
}

// RunGit runs git with args in repo and returns combined stdout/stderr output.
// It fails the test if git exits non-zero.
func RunGit(t testing.TB, repo string, args ...string) string {
	t.Helper()

	cmd := exec.Command("git", args...)
	cmd.Dir = repo
	cmd.Env = gitEnv()
	out, err := cmd.CombinedOutput()
	if err != nil {
		t.Fatalf("git %v in %q failed: %v\n%s", args, repo, err, out)
	}
	return string(out)
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
