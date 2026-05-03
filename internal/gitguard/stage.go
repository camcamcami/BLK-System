package gitguard

import (
	"context"
	"fmt"
	"os"
	"path"
	"path/filepath"
	"strings"
)

// StageAllowlist stages only the explicitly allowlisted modified and new files
// in repo. Each path is added with its own git add -- <path> invocation; broad
// staging forms such as git add . or git add -u are intentionally not used.
func StageAllowlist(repo string, allowedModified []string, allowedNew []string) error {
	for _, rel := range allowedModified {
		if err := stagePath(repo, rel); err != nil {
			return err
		}
	}
	for _, rel := range allowedNew {
		if err := stagePath(repo, rel); err != nil {
			return err
		}
	}
	return nil
}

func stagePath(repo string, rel string) error {
	if err := validateStagePath(rel); err != nil {
		return err
	}
	if err := validateStageWorktreeFile(repo, rel); err != nil {
		return err
	}

	_, err := RunGit(context.Background(), repo, "add", "--", rel)
	return err
}

func validateStageWorktreeFile(repo string, rel string) error {
	fullPath := filepath.Join(repo, filepath.FromSlash(rel))
	info, err := os.Stat(fullPath)
	if err != nil {
		return fmt.Errorf("stage path %q in %q must name an existing file: %w", rel, repo, err)
	}
	if info.IsDir() {
		return fmt.Errorf("stage path %q in %q must name a file, not a directory", rel, repo)
	}
	return nil
}

func validateStagePath(rel string) error {
	if rel == "" || path.Clean(rel) != rel {
		return fmt.Errorf("stage path %q must be a clean relative file path", rel)
	}
	if rel == "." {
		return fmt.Errorf("stage path %q must name an explicit file", rel)
	}
	if filepath.IsAbs(rel) || path.IsAbs(rel) {
		return fmt.Errorf("stage path %q must be relative", rel)
	}
	if strings.HasPrefix(rel, ":") || strings.ContainsAny(rel, "*?[") {
		return fmt.Errorf("stage path %q must not contain git pathspec metacharacters", rel)
	}
	for _, part := range strings.Split(rel, "/") {
		if part == ".." {
			return fmt.Errorf("stage path %q must not contain ..", rel)
		}
	}
	return nil
}
