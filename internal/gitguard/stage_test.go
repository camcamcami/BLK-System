package gitguard

import (
	"os"
	"path/filepath"
	"reflect"
	"strings"
	"testing"

	"github.com/camcamcami/BLK-System/internal/testutil"
)

func TestStageAllowlist(t *testing.T) {
	t.Run("stages modified allowlisted file", func(t *testing.T) {
		repo := testutil.NewGitRepo(t)
		testutil.WriteFile(t, repo, "README.md", "changed\n")

		if err := StageAllowlist(repo, []string{"README.md"}, nil); err != nil {
			t.Fatalf("StageAllowlist() error = %v, want nil", err)
		}

		assertCachedNames(t, repo, []string{"README.md"})
	})

	t.Run("stages new allowlisted file", func(t *testing.T) {
		repo := testutil.NewGitRepo(t)
		testutil.WriteFile(t, repo, "docs/new.md", "new\n")

		if err := StageAllowlist(repo, nil, []string{"docs/new.md"}); err != nil {
			t.Fatalf("StageAllowlist() error = %v, want nil", err)
		}

		assertCachedNames(t, repo, []string{"docs/new.md"})
	})

	t.Run("does not stage unallowlisted modified or new files", func(t *testing.T) {
		repo := testutil.NewGitRepo(t)
		testutil.WriteFile(t, repo, "README.md", "allowed modified\n")
		testutil.WriteFile(t, repo, "allowed/new.txt", "allowed new\n")
		testutil.WriteFile(t, repo, "unallowed/modified.txt", "initial unallowed\n")
		testutil.RunGit(t, repo, "add", "--", "unallowed/modified.txt")
		testutil.RunGit(t, repo, "commit", "-m", "add unallowed tracked file")
		testutil.WriteFile(t, repo, "unallowed/modified.txt", "changed unallowed\n")
		testutil.WriteFile(t, repo, "unallowed/new-a.txt", "unallowed new a\n")
		testutil.WriteFile(t, repo, "unallowed/nested/new-b.txt", "unallowed new b\n")

		if err := StageAllowlist(repo, []string{"README.md"}, []string{"allowed/new.txt"}); err != nil {
			t.Fatalf("StageAllowlist() error = %v, want nil", err)
		}

		assertCachedNames(t, repo, []string{"README.md", "allowed/new.txt"})
	})

	t.Run("uses pathspec terminator for dash prefixed paths", func(t *testing.T) {
		repo := testutil.NewGitRepo(t)
		testutil.WriteFile(t, repo, "-allowed.txt", "new\n")

		if err := StageAllowlist(repo, nil, []string{"-allowed.txt"}); err != nil {
			t.Fatalf("StageAllowlist() error = %v, want nil", err)
		}

		assertCachedNames(t, repo, []string{"-allowed.txt"})
	})

	t.Run("rejects directory allowlist entry without staging children", func(t *testing.T) {
		repo := testutil.NewGitRepo(t)
		testutil.WriteFile(t, repo, "safe/a.txt", "new a\n")
		testutil.WriteFile(t, repo, "safe/nested/b.txt", "new b\n")

		err := StageAllowlist(repo, nil, []string{"safe"})
		if err == nil {
			t.Fatal("StageAllowlist() error = nil, want error for directory")
		}

		assertCachedNames(t, repo, nil)
	})

	t.Run("rejects deleted allowlisted file without staging deletion", func(t *testing.T) {
		repo := testutil.NewGitRepo(t)
		testutil.WriteFile(t, repo, "delete-me.txt", "tracked\n")
		testutil.RunGit(t, repo, "add", "--", "delete-me.txt")
		testutil.RunGit(t, repo, "commit", "-m", "add tracked file")
		if err := os.Remove(filepath.Join(repo, "delete-me.txt")); err != nil {
			t.Fatalf("remove tracked file: %v", err)
		}

		err := StageAllowlist(repo, []string{"delete-me.txt"}, nil)
		if err == nil {
			t.Fatal("StageAllowlist() error = nil, want error for deleted file")
		}

		assertCachedNames(t, repo, nil)
	})

	t.Run("rejects unsafe path and pathspec inputs before git can widen scope", func(t *testing.T) {
		cases := []struct {
			name  string
			rel   string
			setup func(t *testing.T, repo string)
		}{
			{name: "parent traversal", rel: "../x"},
			{name: "cleaned traversal", rel: "safe/../x"},
			{name: "dot", rel: "."},
			{name: "wildcard", rel: "*"},
			{name: "magic glob pathspec", rel: ":(glob)**"},
			{
				name: "directory",
				rel:  "safe",
				setup: func(t *testing.T, repo string) {
					t.Helper()
					testutil.WriteFile(t, repo, "safe/a.txt", "new a\n")
					testutil.WriteFile(t, repo, "safe/b.txt", "new b\n")
				},
			},
		}

		for _, tc := range cases {
			t.Run(tc.name, func(t *testing.T) {
				repo := testutil.NewGitRepo(t)
				if tc.setup != nil {
					tc.setup(t, repo)
				}

				err := StageAllowlist(repo, nil, []string{tc.rel})
				if err == nil {
					t.Fatalf("StageAllowlist(%q) error = nil, want error", tc.rel)
				}

				assertCachedNames(t, repo, nil)
			})
		}
	})
}

func assertCachedNames(t *testing.T, repo string, want []string) {
	t.Helper()

	got := splitGitLines(testutil.RunGit(t, repo, "diff", "--cached", "--name-only"))
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("cached names = %q, want %q", got, want)
	}
}

func splitGitLines(out string) []string {
	out = strings.TrimSuffix(out, "\n")
	if out == "" {
		return nil
	}
	return strings.Split(out, "\n")
}
