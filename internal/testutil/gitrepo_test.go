package testutil

import (
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"testing"
)

func TestNewGitRepoIgnoresEnvironmentConfigInjection(t *testing.T) {
	t.Setenv("GIT_CONFIG_COUNT", "1")
	t.Setenv("GIT_CONFIG_KEY_0", "commit.gpgsign")
	t.Setenv("GIT_CONFIG_VALUE_0", "true")

	repo := NewGitRepo(t)

	if got := strings.TrimSpace(RunGit(t, repo, "rev-list", "--count", "HEAD")); got != "1" {
		t.Fatalf("commit count = %q, want 1", got)
	}
	if got := RunGit(t, repo, "status", "--porcelain"); got != "" {
		t.Fatalf("git status --porcelain = %q, want clean", got)
	}
}

func TestNewGitRepoIgnoresGlobalHooksPath(t *testing.T) {
	if runtime.GOOS == "windows" {
		t.Skip("shell hook script requires a POSIX shell")
	}

	hooksDir := t.TempDir()
	preCommit := filepath.Join(hooksDir, "pre-commit")
	if err := os.WriteFile(preCommit, []byte("#!/bin/sh\necho hostile global pre-commit >&2\nexit 1\n"), 0o755); err != nil {
		t.Fatalf("write failing pre-commit hook: %v", err)
	}

	globalConfig := filepath.Join(t.TempDir(), "gitconfig")
	config := "[core]\n\thooksPath = " + hooksDir + "\n"
	if err := os.WriteFile(globalConfig, []byte(config), 0o644); err != nil {
		t.Fatalf("write fake global gitconfig: %v", err)
	}
	t.Setenv("GIT_CONFIG_GLOBAL", globalConfig)

	repo := NewGitRepo(t)

	if got := strings.TrimSpace(RunGit(t, repo, "rev-list", "--count", "HEAD")); got != "1" {
		t.Fatalf("commit count = %q, want 1", got)
	}
	if got := RunGit(t, repo, "status", "--porcelain"); got != "" {
		t.Fatalf("git status --porcelain = %q, want clean", got)
	}
}

func TestNewGitRepoIgnoresTemplateDirHooks(t *testing.T) {
	if runtime.GOOS == "windows" {
		t.Skip("shell hook script requires a POSIX shell")
	}

	templateDir := t.TempDir()
	hooksDir := filepath.Join(templateDir, "hooks")
	if err := os.MkdirAll(hooksDir, 0o755); err != nil {
		t.Fatalf("create template hooks dir: %v", err)
	}
	preCommit := filepath.Join(hooksDir, "pre-commit")
	if err := os.WriteFile(preCommit, []byte("#!/bin/sh\necho hostile template pre-commit >&2\nexit 1\n"), 0o755); err != nil {
		t.Fatalf("write failing template pre-commit hook: %v", err)
	}
	t.Setenv("GIT_TEMPLATE_DIR", templateDir)

	repo := NewGitRepo(t)

	if got := strings.TrimSpace(RunGit(t, repo, "rev-list", "--count", "HEAD")); got != "1" {
		t.Fatalf("commit count = %q, want 1", got)
	}
	if got := RunGit(t, repo, "status", "--porcelain"); got != "" {
		t.Fatalf("git status --porcelain = %q, want clean", got)
	}
}

func TestNewGitRepoIgnoresInheritedGitDir(t *testing.T) {
	externalRepo := t.TempDir()
	RunGit(t, externalRepo, "init")
	t.Setenv("GIT_DIR", filepath.Join(externalRepo, ".git"))

	repo := NewGitRepo(t)

	if repo == externalRepo {
		t.Fatal("NewGitRepo returned external repository path")
	}
	if info, err := os.Stat(filepath.Join(repo, ".git")); err != nil {
		t.Fatalf(".git directory does not exist: %v", err)
	} else if !info.IsDir() {
		t.Fatal(".git path is not a directory")
	}
	if got := strings.TrimSpace(RunGit(t, repo, "rev-list", "--count", "HEAD")); got != "1" {
		t.Fatalf("commit count = %q, want 1", got)
	}
	if got := RunGit(t, repo, "status", "--porcelain"); got != "" {
		t.Fatalf("git status --porcelain = %q, want clean", got)
	}
}

func TestNewGitRepoCreatesCleanRepositoryWithInitialCommit(t *testing.T) {
	repo := NewGitRepo(t)

	if repo == "" {
		t.Fatal("NewGitRepo returned empty path")
	}
	if !filepath.IsAbs(repo) {
		t.Fatalf("NewGitRepo returned %q, want absolute path", repo)
	}
	if info, err := os.Stat(repo); err != nil {
		t.Fatalf("repo path %q does not exist: %v", repo, err)
	} else if !info.IsDir() {
		t.Fatalf("repo path %q is not a directory", repo)
	}
	if info, err := os.Stat(filepath.Join(repo, ".git")); err != nil {
		t.Fatalf(".git directory does not exist: %v", err)
	} else if !info.IsDir() {
		t.Fatal(".git path is not a directory")
	}

	if got := strings.TrimSpace(RunGit(t, repo, "config", "--local", "user.name")); got == "" {
		t.Fatal("local git user.name is empty")
	}
	if got := strings.TrimSpace(RunGit(t, repo, "config", "--local", "user.email")); got == "" {
		t.Fatal("local git user.email is empty")
	}
	if got := strings.TrimSpace(RunGit(t, repo, "rev-list", "--count", "HEAD")); got != "1" {
		t.Fatalf("commit count = %q, want 1", got)
	}
	if got := RunGit(t, repo, "status", "--porcelain"); got != "" {
		t.Fatalf("git status --porcelain = %q, want clean", got)
	}
}

func TestWriteFileCreatesParentsAndRunGitReturnsOutput(t *testing.T) {
	repo := NewGitRepo(t)

	WriteFile(t, repo, "nested/path/file.txt", "hello\n")

	got, err := os.ReadFile(filepath.Join(repo, "nested", "path", "file.txt"))
	if err != nil {
		t.Fatalf("ReadFile() error = %v", err)
	}
	if string(got) != "hello\n" {
		t.Fatalf("file content = %q, want %q", got, "hello\n")
	}

	status := RunGit(t, repo, "status", "--porcelain")
	if !strings.Contains(status, "?? nested/") {
		t.Fatalf("RunGit status output = %q, want untracked nested directory", status)
	}
}
