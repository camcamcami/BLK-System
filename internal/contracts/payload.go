package contracts

import (
	"fmt"
	"path"
	"path/filepath"
	"strings"
)

type Payload struct {
	Action               string   `json:"action"`
	Workdir              string   `json:"workdir"`
	EngineCommand        []string `json:"engine_command"`
	AllowedModifiedFiles []string `json:"allowed_modified_files"`
	AllowedNewFiles      []string `json:"allowed_new_files"`
	TimeoutSeconds       int      `json:"timeout_seconds"`
	MaxOutputBytes       int64    `json:"max_output_bytes"`
}

func (p Payload) Validate() error {
	if p.Action != "execute" {
		return fmt.Errorf("action must equal execute")
	}
	if !filepath.IsAbs(p.Workdir) {
		return fmt.Errorf("workdir must be absolute")
	}
	if err := validateEngineCommand(p.EngineCommand); err != nil {
		return err
	}
	if p.TimeoutSeconds <= 0 {
		return fmt.Errorf("timeout_seconds must be greater than 0")
	}
	if p.MaxOutputBytes <= 0 {
		return fmt.Errorf("max_output_bytes must be greater than 0")
	}
	if err := validateAllowlist("allowed_modified_files", p.AllowedModifiedFiles); err != nil {
		return err
	}
	if err := validateAllowlist("allowed_new_files", p.AllowedNewFiles); err != nil {
		return err
	}
	return nil
}

func validateEngineCommand(command []string) error {
	if len(command) == 0 {
		return fmt.Errorf("engine_command must contain at least one element")
	}
	for _, entry := range command {
		if strings.TrimSpace(entry) == "" {
			return fmt.Errorf("engine_command entries must not be empty")
		}
	}
	return nil
}

func validateAllowlist(field string, entries []string) error {
	for _, entry := range entries {
		if filepath.IsAbs(entry) || path.IsAbs(entry) {
			return fmt.Errorf("%s entry %q must be relative", field, entry)
		}
		if entry == "" || path.Clean(entry) != entry {
			return fmt.Errorf("%s entry %q must be a clean path", field, entry)
		}
		if entry == "." {
			return fmt.Errorf("%s entry %q must name an explicit file", field, entry)
		}
		if hasPathspecMeta(entry) {
			return fmt.Errorf("%s entry %q must not contain git pathspec metacharacters", field, entry)
		}
		if containsDotDot(entry) {
			return fmt.Errorf("%s entry %q must not contain ..", field, entry)
		}
		if isProtectedDocsPath(entry) {
			return fmt.Errorf("%s entry %q matches protected %s path", field, entry, protectedDocsPrefix(entry))
		}
	}
	return nil
}

func hasPathspecMeta(entry string) bool {
	return strings.HasPrefix(entry, ":") || strings.ContainsAny(entry, "*?[")
}

func containsDotDot(entry string) bool {
	for _, part := range strings.Split(entry, "/") {
		if part == ".." {
			return true
		}
	}
	return false
}

func isProtectedDocsPath(entry string) bool {
	return strings.HasPrefix(entry, "docs/requirements/") || strings.HasPrefix(entry, "docs/use_cases/")
}

func protectedDocsPrefix(entry string) string {
	if strings.HasPrefix(entry, "docs/requirements/") {
		return "docs/requirements"
	}
	if strings.HasPrefix(entry, "docs/use_cases/") {
		return "docs/use_cases"
	}
	return "docs"
}
