package gitguard

import (
	"context"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"

	"github.com/camcamcami/BLK-System/internal/testutil"
)

func TestRunGitRevParseHeadSucceedsInHermeticRepo(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	want := strings.TrimSpace(testutil.RunGit(t, repo, "rev-parse", "HEAD"))

	got, err := RunGit(context.Background(), repo, "rev-parse", "HEAD")
	if err != nil {
		t.Fatalf("RunGit(rev-parse HEAD) error = %v, want nil", err)
	}
	if strings.TrimSpace(string(got.Stdout)) != want {
		t.Fatalf("RunGit stdout = %q, want %q", got.Stdout, want)
	}
}

func TestRunGitFailureIncludesStderrContext(t *testing.T) {
	repo := testutil.NewGitRepo(t)

	_, err := RunGit(context.Background(), repo, "definitely-not-a-real-git-subcommand")
	if err == nil {
		t.Fatal("RunGit() error = nil, want git failure")
	}
	msg := strings.ToLower(err.Error())
	if !strings.Contains(msg, "git definitely-not-a-real-git-subcommand") {
		t.Fatalf("RunGit() error = %q, want command context", err.Error())
	}
	if !strings.Contains(msg, "not a git command") {
		t.Fatalf("RunGit() error = %q, want stderr context", err.Error())
	}
}

func TestRunGitScrubsInheritedGitAndSSHEnvironment(t *testing.T) {
	repo := t.TempDir()
	git := writeFakeGit(t, "#!/bin/sh\n"+
		"env | sort\n")
	t.Setenv("PATH", filepath.Dir(git)+string(os.PathListSeparator)+os.Getenv("PATH"))
	t.Setenv("GIT_DIR", "/tmp/evil-git-dir")
	t.Setenv("GIT_CONFIG_GLOBAL", "/tmp/evil-gitconfig")
	t.Setenv("GIT_SSH_COMMAND", "ssh -i /tmp/evil-key")
	t.Setenv("SSH_AUTH_SOCK", "/tmp/evil-agent.sock")
	t.Setenv("SSH_AGENT_PID", "12345")
	t.Setenv("SSH_ASKPASS", "/tmp/evil-askpass")
	t.Setenv("PWD", "/tmp/inherited-pwd")

	result, err := RunGit(context.Background(), repo, "status")
	if err != nil {
		t.Fatalf("RunGit() error = %v, want nil", err)
	}
	env := string(result.Stdout)
	for _, forbidden := range []string{
		"GIT_DIR=/tmp/evil-git-dir",
		"GIT_CONFIG_GLOBAL=/tmp/evil-gitconfig",
		"GIT_SSH_COMMAND=ssh -i /tmp/evil-key",
		"SSH_AUTH_SOCK=/tmp/evil-agent.sock",
		"SSH_AGENT_PID=12345",
		"SSH_ASKPASS=/tmp/evil-askpass",
		"PWD=/tmp/inherited-pwd",
	} {
		if strings.Contains(env, forbidden) {
			t.Fatalf("RunGit environment contains scrubbed entry %q in:\n%s", forbidden, env)
		}
	}
	if strings.Contains(env, "SSH_AUTH_SOCK=") {
		t.Fatalf("RunGit environment contains scrubbed SSH_AUTH_SOCK in:\n%s", env)
	}
	for _, required := range []string{
		"GIT_CONFIG_NOSYSTEM=1",
		"GIT_CONFIG_GLOBAL=" + os.DevNull,
		"PWD=" + repo,
	} {
		if !strings.Contains(env, required) {
			t.Fatalf("RunGit environment missing %q in:\n%s", required, env)
		}
	}
}

func TestRunGitOutputFloodIsInfrastructureError(t *testing.T) {
	repo := t.TempDir()
	git := writeFakeGit(t, "#!/bin/sh\n"+
		"printf '0123456789abcdef0123456789abcdef'\n")
	t.Setenv("PATH", filepath.Dir(git)+string(os.PathListSeparator)+os.Getenv("PATH"))

	result, err := RunGitWithLimit(context.Background(), repo, 8, "status")
	if err == nil {
		t.Fatal("RunGitWithLimit() error = nil, want output flood infrastructure error")
	}
	if len(result.Stdout) > 8 {
		t.Fatalf("RunGitWithLimit() retained %d bytes, want <= 8", len(result.Stdout))
	}
	if !strings.Contains(strings.ToLower(err.Error()), "output") || !strings.Contains(strings.ToLower(err.Error()), "exceeded") {
		t.Fatalf("RunGitWithLimit() error = %q, want output flood context", err.Error())
	}
}

func TestRunGitTimeoutIsInfrastructureError(t *testing.T) {
	repo := t.TempDir()
	git := writeFakeGit(t, "#!/bin/sh\n"+
		"sleep 10\n")
	t.Setenv("PATH", filepath.Dir(git)+string(os.PathListSeparator)+os.Getenv("PATH"))
	ctx, cancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
	defer cancel()

	_, err := RunGit(ctx, repo, "status")
	if err == nil {
		t.Fatal("RunGit() error = nil, want timeout infrastructure error")
	}
	if !strings.Contains(strings.ToLower(err.Error()), "timed out") {
		t.Fatalf("RunGit() error = %q, want timeout context", err.Error())
	}
}

func TestRunGitWithEnvAllowsHeadlessSSHForLsRemote(t *testing.T) {
	repo := t.TempDir()
	git := writeFakeGit(t, "#!/bin/sh\n"+
		"if [ \"$1\" = ls-remote ]; then printf '%s' \"$GIT_SSH_COMMAND\"; fi\n")
	t.Setenv("PATH", filepath.Dir(git)+string(os.PathListSeparator)+os.Getenv("PATH"))
	t.Setenv("GIT_SSH_COMMAND", "ssh -i /tmp/evil-key")
	want := "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o BatchMode=yes"

	result, err := RunGitWithEnv(context.Background(), repo, []string{"GIT_SSH_COMMAND=" + want}, "ls-remote", "git@example.invalid:repo.git", "HEAD")
	if err != nil {
		t.Fatalf("RunGitWithEnv(ls-remote) error = %v, want nil", err)
	}
	if string(result.Stdout) != want {
		t.Fatalf("GIT_SSH_COMMAND = %q, want %q", result.Stdout, want)
	}
}

func writeFakeGit(t *testing.T, script string) string {
	t.Helper()
	dir := t.TempDir()
	path := filepath.Join(dir, "git")
	if err := os.WriteFile(path, []byte(script), 0o755); err != nil {
		t.Fatalf("write fake git: %v", err)
	}
	return path
}
