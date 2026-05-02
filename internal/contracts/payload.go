package contracts

import (
	"encoding/json"
	"fmt"
	"path"
	"path/filepath"
	"slices"
	"strings"
)

const (
	DefaultTimeoutSeconds = 900
	DefaultMaxOutputBytes = int64(52428800)
)

type Payload struct {
	Action               string   `json:"action"`
	Workdir              string   `json:"workdir"`
	WorkDir              string   `json:"work_dir,omitempty"`
	CebID                string   `json:"ceb_id,omitempty"`
	TargetBranch         string   `json:"target_branch,omitempty"`
	EngineCommand        []string `json:"engine_command"`
	AllowedModifiedFiles []string `json:"allowed_modified_files"`
	AllowedNewFiles      []string `json:"allowed_new_files"`
	TimeoutSeconds       int      `json:"timeout_seconds"`
	MaxOutputBytes       int64    `json:"max_output_bytes"`
}

// DecodePayload decodes either the Sprint 001 legacy payload shape or the V47
// execute-compatible shape, normalizes V47 fields into the internal Sprint 001
// execution contract, then validates the normalized payload.
func DecodePayload(data []byte) (Payload, error) {
	var wire payloadWire
	if err := json.Unmarshal(data, &wire); err != nil {
		return Payload{}, err
	}
	var fields map[string]json.RawMessage
	if err := json.Unmarshal(data, &fields); err != nil {
		return Payload{}, err
	}
	payload := wire.rawPayload()
	if err := wire.validateMixedFieldConflicts(fields); err != nil {
		return payload, err
	}
	wire.normalizeV47(&payload)

	if err := payload.Validate(); err != nil {
		return payload, err
	}
	return payload, nil
}

type payloadWire struct {
	Action               string   `json:"action"`
	Workdir              string   `json:"workdir"`
	WorkDir              string   `json:"work_dir"`
	CebID                string   `json:"ceb_id"`
	TargetBranch         string   `json:"target_branch"`
	Engine               string   `json:"engine"`
	EngineArgs           []string `json:"engine_args"`
	EngineCommand        []string `json:"engine_command"`
	L2Packet             string   `json:"l2_packet"`
	ValidationCommands   []string `json:"validation_commands"`
	AllowedModifiedFiles []string `json:"allowed_modified_files"`
	AllowedNewFiles      []string `json:"allowed_new_files"`
	TimeoutSeconds       *int     `json:"timeout_seconds"`
	MaxOutputBytes       *int64   `json:"max_output_bytes"`
}

func (p payloadWire) isV47() bool {
	return p.WorkDir != "" || p.CebID != "" || p.TargetBranch != "" || p.Engine != "" || p.EngineArgs != nil || p.L2Packet != "" || p.ValidationCommands != nil
}

func (p payloadWire) rawPayload() Payload {
	payload := Payload{
		Action:               p.Action,
		Workdir:              p.Workdir,
		WorkDir:              p.WorkDir,
		CebID:                p.CebID,
		TargetBranch:         p.TargetBranch,
		EngineCommand:        append([]string{}, p.EngineCommand...),
		AllowedModifiedFiles: append([]string{}, p.AllowedModifiedFiles...),
		AllowedNewFiles:      append([]string{}, p.AllowedNewFiles...),
	}
	if p.TimeoutSeconds != nil {
		payload.TimeoutSeconds = *p.TimeoutSeconds
	}
	if p.MaxOutputBytes != nil {
		payload.MaxOutputBytes = *p.MaxOutputBytes
	}
	return payload
}

func (p payloadWire) normalizeV47(payload *Payload) {
	if p.WorkDir != "" {
		payload.Workdir = p.WorkDir
	}
	if p.Engine != "" {
		payload.EngineCommand = append([]string{p.Engine}, p.EngineArgs...)
	}
	if p.TimeoutSeconds == nil && p.isV47() {
		payload.TimeoutSeconds = DefaultTimeoutSeconds
	}
	if p.MaxOutputBytes == nil && p.isV47() {
		payload.MaxOutputBytes = DefaultMaxOutputBytes
	}
}

func (p payloadWire) validateMixedFieldConflicts(fields map[string]json.RawMessage) error {
	_, hasLegacyWorkdir := fields["workdir"]
	_, hasV47WorkDir := fields["work_dir"]
	if hasLegacyWorkdir && hasV47WorkDir && p.Workdir != p.WorkDir {
		return fmt.Errorf("conflicting workdir and work_dir fields")
	}

	_, hasLegacyEngineCommand := fields["engine_command"]
	_, hasV47Engine := fields["engine"]
	_, hasV47EngineArgs := fields["engine_args"]
	if hasLegacyEngineCommand && (hasV47Engine || hasV47EngineArgs) && !slices.Equal(p.EngineCommand, p.normalizedV47EngineCommand()) {
		return fmt.Errorf("conflicting engine_command and engine/engine_args fields")
	}

	return nil
}

func (p payloadWire) normalizedV47EngineCommand() []string {
	if p.Engine == "" {
		return nil
	}
	return append([]string{p.Engine}, p.EngineArgs...)
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
