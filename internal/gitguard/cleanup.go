package gitguard

import (
	"context"
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
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
	if err := MakeWorktreeDirsTraversable(repo); err != nil {
		return err
	}
	if err := runCleanupGit(repo, "clean", "-ffdx", "-q"); err != nil {
		return err
	}
	return nil
}

// MakeWorktreeDirsTraversable adds owner rwx bits to worktree directories so
// post-engine audit and cleanup can inspect and remove engine-created unreadable
// residue. It excludes only the repository root .git directory; nested .git
// directories remain ordinary worktree residue and are traversed.
func MakeWorktreeDirsTraversable(repo string) error {
	root, err := filepath.Abs(repo)
	if err != nil {
		return fmt.Errorf("resolve worktree root %q: %w", repo, err)
	}
	rootGit := filepath.Join(root, ".git")
	if err := makeDirTraversable(root); err != nil {
		return err
	}
	return makeDirsTraversable(root, rootGit)
}

func makeDirsTraversable(dir, rootGit string) error {
	entries, err := os.ReadDir(dir)
	if err != nil {
		if errorsIsNotExist(err) {
			return nil
		}
		if chmodErr := makeDirTraversable(dir); chmodErr != nil {
			return chmodErr
		}
		entries, err = os.ReadDir(dir)
		if err != nil {
			return fmt.Errorf("read worktree directory %q: %w", dir, err)
		}
	}
	for _, entry := range entries {
		path := filepath.Join(dir, entry.Name())
		if path == rootGit {
			continue
		}
		info, err := os.Lstat(path)
		if err != nil {
			if errorsIsNotExist(err) {
				continue
			}
			return fmt.Errorf("stat worktree path %q: %w", path, err)
		}
		if !info.IsDir() {
			continue
		}
		if err := chmodDirOwnerRWX(path, info.Mode()); err != nil {
			return err
		}
		if err := makeDirsTraversable(path, rootGit); err != nil {
			return err
		}
	}
	return nil
}

func makeDirTraversable(path string) error {
	info, err := os.Lstat(path)
	if err != nil {
		if errorsIsNotExist(err) {
			return nil
		}
		return fmt.Errorf("stat worktree directory %q: %w", path, err)
	}
	if !info.IsDir() {
		return nil
	}
	return chmodDirOwnerRWX(path, info.Mode())
}

func chmodDirOwnerRWX(path string, mode fs.FileMode) error {
	want := mode | 0o700
	if want == mode {
		return nil
	}
	if err := os.Chmod(path, want); err != nil {
		return fmt.Errorf("chmod worktree directory %q: %w", path, err)
	}
	return nil
}

func errorsIsNotExist(err error) bool {
	return err != nil && (os.IsNotExist(err) || err == fs.ErrNotExist)
}

func runCleanupGit(repo string, args ...string) error {
	_, err := RunGit(context.Background(), repo, args...)
	return err
}
