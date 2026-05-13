package contracts

import (
	"encoding/json"
	"fmt"
	"path"
	"path/filepath"
	"slices"
	"strings"

	"github.com/camcamcami/BLK-System/internal/gitguard"
	"github.com/camcamcami/BLK-System/internal/validationprofiles"
)

const (
	DefaultTimeoutSeconds            = 900
	DefaultMaxOutputBytes            = int64(52428800)
	DefaultMaxPayloadJSONBytes       = 2 * 1024 * 1024
	DefaultMaxValidationCommands     = 16
	DefaultMaxValidationCommandBytes = 4096
	DefaultMaxL2PacketBytes          = 1048576
	maxTraceArtifacts                = 64
	maxTraceArtifactBytes            = 256
	traceVersionHashPrefix           = "sha256:"
	canonicalTraceVersionHashLength  = len(traceVersionHashPrefix) + 64
)

func ValidatePayloadJSONSize(data []byte) error {
	if len(data) > DefaultMaxPayloadJSONBytes {
		return fmt.Errorf("payload JSON exceeds maximum size of %d bytes", DefaultMaxPayloadJSONBytes)
	}
	return nil
}

type TraceArtifact struct {
	Kind        string `json:"kind"`
	ID          string `json:"id"`
	VersionHash string `json:"version_hash"`
}

type Payload struct {
	Action                     string          `json:"action"`
	Workdir                    string          `json:"workdir"`
	WorkDir                    string          `json:"work_dir,omitempty"`
	BebID                      string          `json:"beb_id,omitempty"`
	TargetBranch               string          `json:"target_branch,omitempty"`
	TargetHash                 string          `json:"target_hash,omitempty"`
	EngineCommand              []string        `json:"engine_command"`
	L2Packet                   string          `json:"l2_packet,omitempty"`
	TraceArtifacts             []TraceArtifact `json:"trace_artifacts"`
	ValidationProfiles         []string        `json:"validation_profiles,omitempty"`
	ValidationCommands         []string        `json:"validation_commands"`
	ResolvedValidationCommands []string        `json:"-"`
	AllowedModifiedFiles       []string        `json:"allowed_modified_files"`
	AllowedNewFiles            []string        `json:"allowed_new_files"`
	TimeoutSeconds             int             `json:"timeout_seconds"`
	MaxOutputBytes             int64           `json:"max_output_bytes"`
}

// DecodePayload decodes either the Sprint 001 legacy payload shape or the V47
// execute-compatible shape, normalizes V47 fields into the internal Sprint 001
// execution contract, then validates the normalized payload.
func DecodePayload(data []byte) (Payload, error) {
	if err := ValidatePayloadJSONSize(data); err != nil {
		return Payload{}, err
	}
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
	if err := payload.resolveValidationCommands(); err != nil {
		return payload, err
	}
	return payload, nil
}

type payloadWire struct {
	Action               string          `json:"action"`
	Workdir              string          `json:"workdir"`
	WorkDir              string          `json:"work_dir"`
	BebID                string          `json:"beb_id"`
	TargetBranch         string          `json:"target_branch"`
	TargetHash           string          `json:"target_hash"`
	Engine               string          `json:"engine"`
	EngineArgs           []string        `json:"engine_args"`
	EngineCommand        []string        `json:"engine_command"`
	L2Packet             string          `json:"l2_packet"`
	TraceArtifacts       []TraceArtifact `json:"trace_artifacts"`
	ValidationProfiles   []string        `json:"validation_profiles"`
	ValidationCommands   []string        `json:"validation_commands"`
	AllowedModifiedFiles []string        `json:"allowed_modified_files"`
	AllowedNewFiles      []string        `json:"allowed_new_files"`
	TimeoutSeconds       *int            `json:"timeout_seconds"`
	MaxOutputBytes       *int64          `json:"max_output_bytes"`
}

func (p payloadWire) isV47() bool {
	return p.WorkDir != "" || p.BebID != "" || p.TargetBranch != "" || p.TargetHash != "" || p.Engine != "" || p.EngineArgs != nil || p.L2Packet != "" || p.ValidationProfiles != nil || p.ValidationCommands != nil
}

func (p payloadWire) rawPayload() Payload {
	payload := Payload{
		Action:               p.Action,
		Workdir:              p.Workdir,
		WorkDir:              p.WorkDir,
		BebID:                p.BebID,
		TargetBranch:         p.TargetBranch,
		TargetHash:           p.TargetHash,
		EngineCommand:        append([]string{}, p.EngineCommand...),
		L2Packet:             p.L2Packet,
		TraceArtifacts:       append([]TraceArtifact{}, p.TraceArtifacts...),
		ValidationProfiles:   append([]string{}, p.ValidationProfiles...),
		ValidationCommands:   append([]string{}, p.ValidationCommands...),
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
	if p.ValidationProfiles != nil {
		payload.ValidationProfiles = append([]string{}, p.ValidationProfiles...)
	}
	if p.ValidationCommands != nil {
		payload.ValidationCommands = append([]string{}, p.ValidationCommands...)
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
	if p.Action != "execute" && p.Action != "revert" {
		return fmt.Errorf("action must equal execute or revert")
	}
	if !filepath.IsAbs(p.Workdir) {
		return fmt.Errorf("workdir must be absolute")
	}
	if len(p.L2Packet) > DefaultMaxL2PacketBytes {
		return fmt.Errorf("l2_packet exceeds maximum size of %d bytes", DefaultMaxL2PacketBytes)
	}
	if err := ValidateTraceArtifacts(p.TraceArtifacts); err != nil {
		return err
	}
	if err := validateValidationProfileRequest(p.ValidationProfiles, p.ValidationCommands); err != nil {
		return err
	}
	if p.Action == "revert" {
		return validateRevertTargetHash(p.TargetHash)
	}
	if len(p.TraceArtifacts) == 0 {
		return fmt.Errorf("trace_artifacts must be non-empty for execute payloads")
	}
	if len(p.ValidationProfiles) == 0 && len(p.ValidationCommands) == 0 {
		return fmt.Errorf("validation_profiles or validation_commands required for execute payloads")
	}
	if p.TargetHash != "" {
		if err := validateRevertTargetHash(p.TargetHash); err != nil {
			return err
		}
	}
	if p.TargetBranch != "" {
		if err := gitguard.ValidateBranchName(p.TargetBranch); err != nil {
			return err
		}
	}
	if err := validateEngineCommand(p.EngineCommand); err != nil {
		return err
	}
	if err := validateValidationCommands(p.ValidationCommands); err != nil {
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
	if err := validateAllowlistDisjoint(p.AllowedModifiedFiles, p.AllowedNewFiles); err != nil {
		return err
	}
	return nil
}

// ValidateTraceArtifacts validates opaque BLK-001 trace artifact baton metadata
// without interpreting requirement/use-case semantics or verifying file hashes.

func (p *Payload) resolveValidationCommands() error {
	if p.Action != "execute" {
		p.ResolvedValidationCommands = nil
		return nil
	}
	if len(p.ValidationProfiles) == 0 {
		p.ResolvedValidationCommands = append([]string{}, p.ValidationCommands...)
		return nil
	}
	commands, err := validationprofiles.Resolve(p.ValidationProfiles)
	if err != nil {
		return err
	}
	p.ResolvedValidationCommands = commands
	return nil
}

func ValidateTraceArtifacts(artifacts []TraceArtifact) error {
	if len(artifacts) > maxTraceArtifacts {
		return fmt.Errorf("trace_artifacts must contain at most %d entries", maxTraceArtifacts)
	}
	for i, artifact := range artifacts {
		if strings.TrimSpace(artifact.Kind) == "" {
			return fmt.Errorf("trace_artifacts[%d].kind must be non-empty", i)
		}
		if strings.TrimSpace(artifact.ID) == "" {
			return fmt.Errorf("trace_artifacts[%d].id must be non-empty", i)
		}
		if strings.TrimSpace(artifact.VersionHash) == "" {
			return fmt.Errorf("trace_artifacts[%d].version_hash must be non-empty", i)
		}
		if len(artifact.Kind) > maxTraceArtifactBytes {
			return fmt.Errorf("trace_artifacts[%d].kind exceeds maximum size of %d bytes", i, maxTraceArtifactBytes)
		}
		if len(artifact.ID) > maxTraceArtifactBytes {
			return fmt.Errorf("trace_artifacts[%d].id exceeds maximum size of %d bytes", i, maxTraceArtifactBytes)
		}
		if len(artifact.VersionHash) > maxTraceArtifactBytes {
			return fmt.Errorf("trace_artifacts[%d].version_hash exceeds maximum size of %d bytes", i, maxTraceArtifactBytes)
		}
		if !isCanonicalTraceVersionHash(artifact.VersionHash) {
			return fmt.Errorf("trace_artifacts[%d].version_hash must match sha256:<64-lowercase-hex>", i)
		}
	}
	return nil
}

func isCanonicalTraceVersionHash(value string) bool {
	if len(value) != canonicalTraceVersionHashLength {
		return false
	}
	if !strings.HasPrefix(value, traceVersionHashPrefix) {
		return false
	}
	for _, r := range value[len(traceVersionHashPrefix):] {
		switch {
		case r >= '0' && r <= '9':
		case r >= 'a' && r <= 'f':
		default:
			return false
		}
	}
	return true
}

func validateRevertTargetHash(targetHash string) error {
	if !isFullHexObjectID(targetHash) {
		return fmt.Errorf("target_hash must be a full hexadecimal commit object ID")
	}
	return nil
}

func isFullHexObjectID(value string) bool {
	if len(value) != 40 && len(value) != 64 {
		return false
	}
	for _, r := range value {
		switch {
		case r >= '0' && r <= '9':
		case r >= 'a' && r <= 'f':
		case r >= 'A' && r <= 'F':
		default:
			return false
		}
	}
	return true
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

func validateValidationProfileRequest(profiles []string, commands []string) error {
	if len(profiles) == 0 {
		return nil
	}
	if len(commands) > 0 {
		return fmt.Errorf("validation_profiles and validation_commands must not both be set")
	}
	return validationprofiles.Validate(profiles)
}

func validateValidationCommands(commands []string) error {
	if len(commands) > DefaultMaxValidationCommands {
		return fmt.Errorf("validation_commands must contain at most %d entries", DefaultMaxValidationCommands)
	}
	for i, command := range commands {
		if strings.TrimSpace(command) == "" {
			return fmt.Errorf("validation_commands entries must not be empty")
		}
		if len(command) > DefaultMaxValidationCommandBytes {
			return fmt.Errorf("validation_commands[%d] exceeds maximum size of %d bytes", i, DefaultMaxValidationCommandBytes)
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
		if IsProtectedDocsPath(entry) {
			return fmt.Errorf("%s entry %q matches protected %s path", field, entry, ProtectedDocsPrefix(entry))
		}
	}
	return nil
}

func validateAllowlistDisjoint(allowedModified []string, allowedNew []string) error {
	modified := make(map[string]struct{}, len(allowedModified))
	for _, entry := range allowedModified {
		modified[entry] = struct{}{}
	}
	for _, entry := range allowedNew {
		if _, ok := modified[entry]; ok {
			return fmt.Errorf("allowed_modified_files and allowed_new_files must not overlap: %s", entry)
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

var protectedDocsRoots = []string{"docs/active", "docs/requirements", "docs/use_cases"}

func IsProtectedDocsPath(entry string) bool {
	for _, root := range protectedDocsRoots {
		if entry == root || strings.HasPrefix(entry, root+"/") {
			return true
		}
	}
	return false
}

func ProtectedDocsPrefix(entry string) string {
	for _, root := range protectedDocsRoots {
		if entry == root || strings.HasPrefix(entry, root+"/") {
			return root
		}
	}
	return "docs"
}

func HasProtectedDocsAllowlistEntry(p Payload) (field string, entry string, prefix string, ok bool) {
	for _, candidate := range p.AllowedModifiedFiles {
		if IsProtectedDocsPath(candidate) {
			return "allowed_modified_files", candidate, ProtectedDocsPrefix(candidate), true
		}
	}
	for _, candidate := range p.AllowedNewFiles {
		if IsProtectedDocsPath(candidate) {
			return "allowed_new_files", candidate, ProtectedDocsPrefix(candidate), true
		}
	}
	return "", "", "", false
}
