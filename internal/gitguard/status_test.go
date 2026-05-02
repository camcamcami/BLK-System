package gitguard

import (
	"errors"
	"strings"
	"testing"

	"github.com/camcamcami/BLK-System/internal/testutil"
)

func TestCleanRepo(t *testing.T) {
	t.Run("clean repo returns nil", func(t *testing.T) {
		repo := testutil.NewGitRepo(t)

		if err := EnsureClean(repo); err != nil {
			t.Fatalf("EnsureClean() error = %v, want nil", err)
		}
	})

	t.Run("modified tracked file returns dirty error", func(t *testing.T) {
		repo := testutil.NewGitRepo(t)
		testutil.WriteFile(t, repo, "README.md", "changed\n")

		err := EnsureClean(repo)
		var dirty *DirtyError
		if !errors.As(err, &dirty) {
			t.Fatalf("EnsureClean() error = %T %[1]v, want *DirtyError", err)
		}
		if !strings.Contains(dirty.Status, "README.md") {
			t.Fatalf("DirtyError.Status = %q, want status output with README.md", dirty.Status)
		}
	})

	t.Run("untracked file returns dirty error", func(t *testing.T) {
		repo := testutil.NewGitRepo(t)
		testutil.WriteFile(t, repo, "scratch.txt", "untracked\n")

		err := EnsureClean(repo)
		var dirty *DirtyError
		if !errors.As(err, &dirty) {
			t.Fatalf("EnsureClean() error = %T %[1]v, want *DirtyError", err)
		}
		if !strings.Contains(dirty.Status, "scratch.txt") {
			t.Fatalf("DirtyError.Status = %q, want status output with scratch.txt", dirty.Status)
		}
	})

	t.Run("untracked file returns dirty error when local config hides untracked files", func(t *testing.T) {
		repo := testutil.NewGitRepo(t)
		testutil.RunGit(t, repo, "config", "--local", "status.showUntrackedFiles", "no")
		testutil.WriteFile(t, repo, "scratch.txt", "untracked\n")

		err := EnsureClean(repo)
		var dirty *DirtyError
		if !errors.As(err, &dirty) {
			t.Fatalf("EnsureClean() error = %T %[1]v, want *DirtyError", err)
		}
		if !strings.Contains(dirty.Status, "scratch.txt") {
			t.Fatalf("DirtyError.Status = %q, want status output with scratch.txt", dirty.Status)
		}
	})

	t.Run("non git repo error includes git stderr", func(t *testing.T) {
		err := EnsureClean(t.TempDir())
		if err == nil {
			t.Fatal("EnsureClean() error = nil, want git error")
		}
		if !strings.Contains(strings.ToLower(err.Error()), "not a git repository") {
			t.Fatalf("EnsureClean() error = %q, want git stderr with not a git repository", err)
		}
	})
}
