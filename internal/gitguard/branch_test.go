package gitguard

import (
	"context"
	"errors"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/camcamcami/BLK-System/internal/testutil"
)

func TestValidateBranchNameAcceptsSafeBranchNames(t *testing.T) {
	for _, name := range []string{
		"feature/local",
		"sprint/ceb-011",
		"release-2026.05",
		"users/alice_task-123",
		"BUGFIX/ABC_123",
	} {
		t.Run(name, func(t *testing.T) {
			if err := ValidateBranchName(name); err != nil {
				t.Fatalf("ValidateBranchName(%q) error = %v, want nil", name, err)
			}
		})
	}
}

func TestValidateBranchNameRejectsUnsafeBranchNames(t *testing.T) {
	tests := []string{
		"",
		"   ",
		"../escape",
		"feature/../escape",
		"feature;rm -rf",
		"HEAD~1",
		"-danger",
		"feature with space",
		"feature\tname",
		"feature\nname",
		"feature:name",
		"feature^{commit}",
		"@{upstream}",
		"feature..main",
		"refs/heads/feature",
	}
	for _, name := range tests {
		t.Run(strings.ReplaceAll(name, "\n", `\n`), func(t *testing.T) {
			if err := ValidateBranchName(name); err == nil {
				t.Fatalf("ValidateBranchName(%q) error = nil, want rejection", name)
			}
		})
	}
}

func TestPrepareTargetBranchRejectsDirtyCurrentWorkspaceBeforeCheckout(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	mainBranch := gitOutput(t, repo, "rev-parse", "--abbrev-ref", "HEAD")
	testutil.RunGit(t, repo, "checkout", "-b", "feature/target")
	testutil.WriteFile(t, repo, "target.txt", "target\n")
	testutil.RunGit(t, repo, "add", "--", "target.txt")
	testutil.RunGit(t, repo, "commit", "-m", "target commit")
	testutil.RunGit(t, repo, "checkout", mainBranch)
	testutil.WriteFile(t, repo, "README.md", "dirty\n")

	_, err := PrepareTargetBranch(context.Background(), repo, "feature/target")
	if err == nil {
		t.Fatalf("PrepareTargetBranch() error = nil, want dirty workspace error")
	}
	var dirty *DirtyError
	if !errors.As(err, &dirty) {
		t.Fatalf("PrepareTargetBranch() error = %T %v, want DirtyError", err, err)
	}
	if got := gitOutput(t, repo, "rev-parse", "--abbrev-ref", "HEAD"); got != mainBranch {
		t.Fatalf("current branch = %q, want %q", got, mainBranch)
	}
	if got := readText(t, filepath.Join(repo, "README.md")); got != "dirty\n" {
		t.Fatalf("README.md = %q, want dirty content preserved", got)
	}
}

func TestPrepareTargetBranchChecksOutExistingLocalBranch(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	mainBranch := gitOutput(t, repo, "rev-parse", "--abbrev-ref", "HEAD")
	testutil.RunGit(t, repo, "checkout", "-b", "feature/local")
	testutil.WriteFile(t, repo, "branch.txt", "local branch\n")
	testutil.RunGit(t, repo, "add", "--", "branch.txt")
	testutil.RunGit(t, repo, "commit", "-m", "local branch commit")
	branchHead := gitOutput(t, repo, "rev-parse", "HEAD")
	testutil.RunGit(t, repo, "checkout", mainBranch)

	info, err := PrepareTargetBranch(context.Background(), repo, "feature/local")
	if err != nil {
		t.Fatalf("PrepareTargetBranch() error = %v", err)
	}
	if info.OrphanCreated {
		t.Fatalf("OrphanCreated = true, want false")
	}
	if got := gitOutput(t, repo, "rev-parse", "--abbrev-ref", "HEAD"); got != "feature/local" {
		t.Fatalf("current branch = %q", got)
	}
	if got := gitOutput(t, repo, "rev-parse", "HEAD"); got != branchHead {
		t.Fatalf("HEAD = %q, want local branch head %q", got, branchHead)
	}
}

func TestPrepareTargetBranchTracksRemoteBranch(t *testing.T) {
	root := t.TempDir()
	bare := filepath.Join(root, "remote.git")
	testutil.RunGit(t, root, "init", "--bare", bare)

	seed := testutil.NewGitRepo(t)
	testutil.RunGit(t, seed, "remote", "add", "origin", bare)
	defaultBranch := gitOutput(t, seed, "rev-parse", "--abbrev-ref", "HEAD")
	testutil.RunGit(t, seed, "push", "origin", defaultBranch)
	testutil.RunGit(t, seed, "checkout", "-b", "feature/remote")
	testutil.WriteFile(t, seed, "remote.txt", "remote branch\n")
	testutil.RunGit(t, seed, "add", "--", "remote.txt")
	testutil.RunGit(t, seed, "commit", "-m", "remote branch commit")
	testutil.RunGit(t, seed, "push", "origin", "feature/remote")

	repo := filepath.Join(root, "work")
	testutil.RunGit(t, root, "clone", bare, repo)
	testutil.RunGit(t, repo, "config", "--local", "user.name", "BLK Test")
	testutil.RunGit(t, repo, "config", "--local", "user.email", "blk-test@example.invalid")
	testutil.RunGit(t, repo, "config", "--local", "commit.gpgsign", "false")

	info, err := PrepareTargetBranch(context.Background(), repo, "feature/remote")
	if err != nil {
		t.Fatalf("PrepareTargetBranch() error = %v", err)
	}
	if info.OrphanCreated {
		t.Fatalf("OrphanCreated = true, want false")
	}
	if got := gitOutput(t, repo, "rev-parse", "--abbrev-ref", "HEAD"); got != "feature/remote" {
		t.Fatalf("current branch = %q", got)
	}
	if got := gitOutput(t, repo, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"); got != "origin/feature/remote" {
		t.Fatalf("upstream = %q, want origin/feature/remote", got)
	}
}

func TestPrepareTargetBranchCreatesEmptyInitializedOrphan(t *testing.T) {
	repo := testutil.NewGitRepo(t)

	info, err := PrepareTargetBranch(context.Background(), repo, "feature/orphan")
	if err != nil {
		t.Fatalf("PrepareTargetBranch() error = %v", err)
	}
	if !info.OrphanCreated {
		t.Fatalf("OrphanCreated = false, want true")
	}
	if got := gitOutput(t, repo, "rev-parse", "--abbrev-ref", "HEAD"); got != "feature/orphan" {
		t.Fatalf("current branch = %q", got)
	}
	if got := gitOutput(t, repo, "log", "-1", "--format=%s"); got != "Initialize branch" {
		t.Fatalf("init commit subject = %q", got)
	}
	if got := gitOutput(t, repo, "ls-tree", "-r", "--name-only", "HEAD"); got != "" {
		t.Fatalf("orphan init tree contains files %q, want empty tree", got)
	}
	if _, err := os.Stat(filepath.Join(repo, "README.md")); err != nil {
		t.Fatalf("inherited README.md should still be present until caller sterilizes workspace: %v", err)
	}
}

func TestPrepareExactTargetBranchSkipsOriginFetchForLocalPinnedBranch(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	mainBranch := gitOutput(t, repo, "rev-parse", "--abbrev-ref", "HEAD")
	testutil.RunGit(t, repo, "checkout", "-b", "feature/exact")
	testutil.WriteFile(t, repo, "exact.txt", "exact branch\n")
	testutil.RunGit(t, repo, "add", "--", "exact.txt")
	testutil.RunGit(t, repo, "commit", "-m", "exact branch commit")
	targetHead := gitOutput(t, repo, "rev-parse", "HEAD")
	testutil.RunGit(t, repo, "checkout", mainBranch)
	testutil.RunGit(t, repo, "remote", "add", "origin", "https://github.com/private/needs-auth.git")

	info, err := PrepareExactTargetBranch(context.Background(), repo, "feature/exact", targetHead)
	if err != nil {
		t.Fatalf("PrepareExactTargetBranch() error = %v, want nil without origin fetch", err)
	}
	if info.OrphanCreated {
		t.Fatalf("OrphanCreated = true, want false")
	}
	if got := gitOutput(t, repo, "rev-parse", "--abbrev-ref", "HEAD"); got != "feature/exact" {
		t.Fatalf("current branch = %q, want feature/exact", got)
	}
	if got := gitOutput(t, repo, "rev-parse", "HEAD"); got != targetHead {
		t.Fatalf("HEAD = %q, want target head %q", got, targetHead)
	}
}

func TestPrepareExactTargetBranchRejectsMissingLocalBranchBeforeRemoteFallback(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	targetHead := gitOutput(t, repo, "rev-parse", "HEAD")
	testutil.RunGit(t, repo, "remote", "add", "origin", "https://github.com/private/needs-auth.git")

	_, err := PrepareExactTargetBranch(context.Background(), repo, "feature/missing", targetHead)
	if err == nil {
		t.Fatal("PrepareExactTargetBranch() error = nil, want target head error")
	}
	var targetErr *TargetHeadError
	if !errors.As(err, &targetErr) {
		t.Fatalf("PrepareExactTargetBranch() error = %T %v, want TargetHeadError", err, err)
	}
	if !strings.Contains(err.Error(), "local branch") {
		t.Fatalf("error = %q, want local branch context", err.Error())
	}
}

func TestPrepareExactTargetBranchRejectsHeadMismatch(t *testing.T) {
	repo := testutil.NewGitRepo(t)
	mainHead := gitOutput(t, repo, "rev-parse", "HEAD")
	testutil.RunGit(t, repo, "checkout", "-b", "feature/exact")
	testutil.WriteFile(t, repo, "exact.txt", "exact branch\n")
	testutil.RunGit(t, repo, "add", "--", "exact.txt")
	testutil.RunGit(t, repo, "commit", "-m", "exact branch commit")

	_, err := PrepareExactTargetBranch(context.Background(), repo, "feature/exact", mainHead)
	if err == nil {
		t.Fatal("PrepareExactTargetBranch() error = nil, want target head mismatch")
	}
	var targetErr *TargetHeadError
	if !errors.As(err, &targetErr) {
		t.Fatalf("PrepareExactTargetBranch() error = %T %v, want TargetHeadError", err, err)
	}
	if !strings.Contains(err.Error(), "target_hash") {
		t.Fatalf("error = %q, want target_hash context", err.Error())
	}
}

func gitOutput(t *testing.T, repo string, args ...string) string {
	t.Helper()
	return strings.TrimSpace(testutil.RunGit(t, repo, args...))
}

func readText(t *testing.T, path string) string {
	t.Helper()
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("read %q: %v", path, err)
	}
	return string(data)
}
