package gitguard

import (
	"os"
	"path/filepath"
	"reflect"
	"testing"

	"github.com/camcamcami/BLK-System/internal/testutil"
)

func TestCleanupUnauthorized(t *testing.T) {
	t.Run("removes unauthorized mutations while preserving staged allowlist", func(t *testing.T) {
		repo := testutil.NewGitRepo(t)
		testutil.WriteFile(t, repo, "tracked/unauthorized.txt", "original unauthorized\n")
		testutil.WriteFile(t, repo, "allowed/modified.txt", "original allowed\n")
		testutil.RunGit(t, repo, "add", "--", "tracked/unauthorized.txt", "allowed/modified.txt")
		testutil.RunGit(t, repo, "commit", "-m", "add cleanup fixtures")

		testutil.WriteFile(t, repo, "tracked/unauthorized.txt", "changed unauthorized\n")
		testutil.WriteFile(t, repo, "allowed/modified.txt", "changed allowed\n")
		testutil.WriteFile(t, repo, "allowed/new.txt", "new allowed\n")
		testutil.WriteFile(t, repo, "scratch/unauthorized.txt", "delete me\n")
		testutil.WriteFile(t, repo, "scratch/nested/unauthorized.txt", "delete nested\n")

		if err := StageAllowlist(repo, []string{"allowed/modified.txt"}, []string{"allowed/new.txt"}); err != nil {
			t.Fatalf("StageAllowlist() error = %v, want nil", err)
		}
		assertCleanupCachedNames(t, repo, []string{"allowed/modified.txt", "allowed/new.txt"})

		if err := CleanupUnauthorized(repo); err != nil {
			t.Fatalf("CleanupUnauthorized() error = %v, want nil", err)
		}

		assertFileContent(t, repo, "tracked/unauthorized.txt", "original unauthorized\n")
		assertNotExists(t, repo, "scratch/unauthorized.txt")
		assertNotExists(t, repo, "scratch/nested/unauthorized.txt")
		assertNotExists(t, repo, "scratch")
		assertFileContent(t, repo, "allowed/modified.txt", "changed allowed\n")
		assertFileContent(t, repo, "allowed/new.txt", "new allowed\n")
		assertCleanupCachedNames(t, repo, []string{"allowed/modified.txt", "allowed/new.txt"})
	})

	t.Run("removes unauthorized untracked nested git repository", func(t *testing.T) {
		repo := testutil.NewGitRepo(t)
		testutil.WriteFile(t, repo, "allowed/modified.txt", "original allowed\n")
		testutil.RunGit(t, repo, "add", "--", "allowed/modified.txt")
		testutil.RunGit(t, repo, "commit", "-m", "add allowed file")

		testutil.WriteFile(t, repo, "allowed/modified.txt", "changed allowed\n")
		testutil.WriteFile(t, repo, "allowed/new.txt", "new allowed\n")
		evilRepo := filepath.Join(repo, "evil")
		if err := os.MkdirAll(evilRepo, 0o755); err != nil {
			t.Fatalf("create nested git repo dir: %v", err)
		}
		testutil.RunGit(t, evilRepo, "init")
		testutil.WriteFile(t, repo, "evil/unauthorized.txt", "delete nested repo\n")

		if err := StageAllowlist(repo, []string{"allowed/modified.txt"}, []string{"allowed/new.txt"}); err != nil {
			t.Fatalf("StageAllowlist() error = %v, want nil", err)
		}
		assertCleanupCachedNames(t, repo, []string{"allowed/modified.txt", "allowed/new.txt"})

		if err := CleanupUnauthorized(repo); err != nil {
			t.Fatalf("CleanupUnauthorized() error = %v, want nil", err)
		}

		assertNotExists(t, repo, "evil")
		assertFileContent(t, repo, "allowed/modified.txt", "changed allowed\n")
		assertFileContent(t, repo, "allowed/new.txt", "new allowed\n")
		assertCleanupCachedNames(t, repo, []string{"allowed/modified.txt", "allowed/new.txt"})
		assertCleanupUnstagedAndUntrackedClean(t, repo)
	})
}

func assertFileContent(t *testing.T, repo string, rel string, want string) {
	t.Helper()

	got, err := os.ReadFile(filepath.Join(repo, filepath.FromSlash(rel)))
	if err != nil {
		t.Fatalf("read %q: %v", rel, err)
	}
	if string(got) != want {
		t.Fatalf("content of %q = %q, want %q", rel, got, want)
	}
}

func assertNotExists(t *testing.T, repo string, rel string) {
	t.Helper()

	_, err := os.Stat(filepath.Join(repo, filepath.FromSlash(rel)))
	if err == nil {
		t.Fatalf("%q exists, want removed", rel)
	}
	if !os.IsNotExist(err) {
		t.Fatalf("stat %q: %v", rel, err)
	}
}

func assertCleanupCachedNames(t *testing.T, repo string, want []string) {
	t.Helper()

	got := splitGitLines(testutil.RunGit(t, repo, "diff", "--cached", "--name-only"))
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("cached names = %q, want %q", got, want)
	}
}

func assertCleanupUnstagedAndUntrackedClean(t *testing.T, repo string) {
	t.Helper()

	if got := testutil.RunGit(t, repo, "diff", "--name-only"); got != "" {
		t.Fatalf("unstaged diff names = %q, want none", got)
	}
	if got := testutil.RunGit(t, repo, "ls-files", "--others", "--exclude-standard"); got != "" {
		t.Fatalf("untracked names = %q, want none", got)
	}
}
