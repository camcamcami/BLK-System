package contracts

import (
	"encoding/json"
	"strings"
	"testing"
)

func validPayload() Payload {
	return Payload{
		Action:               "execute",
		Workdir:              "/tmp/blk-pipe-repo",
		EngineCommand:        []string{"/tmp/fake-engine.sh"},
		TraceArtifacts:       canonicalTraceArtifacts(),
		ValidationCommands:   []string{"go test ./...", "go vet ./..."},
		AllowedModifiedFiles: []string{"src/allowed.txt"},
		AllowedNewFiles:      []string{"src/new.txt"},
		TimeoutSeconds:       60,
		MaxOutputBytes:       52428800,
	}
}

func canonicalTraceArtifacts() []TraceArtifact {
	return []TraceArtifact{{Kind: "REQ", ID: "REQ-DRY-001", VersionHash: "sha256:" + strings.Repeat("a", 64)}}
}

func TestPayloadValidateAcceptsValidPayload(t *testing.T) {
	if err := validPayload().Validate(); err != nil {
		t.Fatalf("Validate() error = %v, want nil", err)
	}
}

func TestPayloadValidateRejectsExecuteWithoutTraceArtifacts(t *testing.T) {
	payload := Payload{
		Action:               "execute",
		Workdir:              "/tmp/blk-pipe-repo",
		EngineCommand:        []string{"/tmp/fake-engine.sh"},
		ValidationCommands:   []string{"true"},
		AllowedModifiedFiles: []string{"README.md"},
		TimeoutSeconds:       60,
		MaxOutputBytes:       4096,
	}

	err := payload.Validate()
	if err == nil {
		t.Fatal("Validate() error = nil, want trace_artifacts rejection")
	}
	if !strings.Contains(err.Error(), "trace_artifacts") || !strings.Contains(err.Error(), "non-empty") {
		t.Fatalf("Validate() error = %q, want non-empty trace_artifacts", err.Error())
	}
}

func TestPayloadValidateRejectsExecuteWithoutValidation(t *testing.T) {
	payload := validPayload()
	payload.ValidationCommands = nil
	payload.ValidationProfiles = nil

	err := payload.Validate()
	if err == nil {
		t.Fatal("Validate() error = nil, want validation required rejection")
	}
	if !strings.Contains(err.Error(), "validation_profiles") || !strings.Contains(err.Error(), "validation_commands") || !strings.Contains(err.Error(), "required") {
		t.Fatalf("Validate() error = %q, want validation required", err.Error())
	}
}

func TestPayloadValidateRevertDoesNotRequireTraceArtifacts(t *testing.T) {
	payload := Payload{
		Action:     "revert",
		Workdir:    "/tmp/blk-pipe-repo",
		TargetHash: "0123456789abcdef0123456789abcdef01234567",
	}

	if err := payload.Validate(); err != nil {
		t.Fatalf("Validate() error = %v, want nil", err)
	}
}

func TestPayloadValidateRejectsOverlappingModifiedAndNewAllowlists(t *testing.T) {
	payload := validPayload()
	payload.AllowedModifiedFiles = []string{"README.md"}
	payload.AllowedNewFiles = []string{"README.md"}

	err := payload.Validate()
	if err == nil {
		t.Fatal("Validate() error = nil, want allowlist overlap rejection")
	}
	if !strings.Contains(err.Error(), "allowed_modified_files") || !strings.Contains(err.Error(), "allowed_new_files") {
		t.Fatalf("Validate() error = %q, want both allowlist names", err.Error())
	}
}

func TestPayloadValidateRejectsTooManyValidationCommands(t *testing.T) {
	payload := validPayload()
	payload.ValidationCommands = make([]string, DefaultMaxValidationCommands+1)
	for i := range payload.ValidationCommands {
		payload.ValidationCommands[i] = "true"
	}

	err := payload.Validate()
	if err == nil {
		t.Fatal("Validate() error = nil, want non-nil")
	}
	if !strings.Contains(err.Error(), "validation_commands") || !strings.Contains(err.Error(), "16") {
		t.Fatalf("Validate() error = %q, want validation_commands limit", err.Error())
	}
}

func TestPayloadValidateRejectsValidationCommandTooLong(t *testing.T) {
	longCommand := strings.Repeat("x", DefaultMaxValidationCommandBytes+1)
	payload := validPayload()
	payload.ValidationCommands = []string{longCommand}

	err := payload.Validate()
	if err == nil {
		t.Fatal("Validate() error = nil, want non-nil")
	}
	if !strings.Contains(err.Error(), "validation_commands[0]") || !strings.Contains(err.Error(), "4096") {
		t.Fatalf("Validate() error = %q, want validation command byte limit", err.Error())
	}
	if strings.Contains(err.Error(), longCommand) || strings.Contains(err.Error(), strings.Repeat("x", 64)) {
		t.Fatalf("Validate() error echoed oversized validation command: %q", err.Error())
	}
}

func TestPayloadDecodeLegacyPayloadStillValidates(t *testing.T) {
	data := []byte(`{"action":"execute","workdir":"/absolute/repo","engine_command":["sh","-c","printf legacy > README.md"],"trace_artifacts":[{"kind":"REQ","id":"REQ-DRY-001","version_hash":"sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}],"validation_commands":["true"],"allowed_modified_files":["README.md"],"allowed_new_files":[],"timeout_seconds":5,"max_output_bytes":4096}`)

	payload, err := DecodePayload(data)
	if err != nil {
		t.Fatalf("DecodePayload() error = %v, want nil", err)
	}

	if payload.Action != "execute" {
		t.Fatalf("Action = %q, want execute", payload.Action)
	}
	if payload.Workdir != "/absolute/repo" {
		t.Fatalf("Workdir = %q, want /absolute/repo", payload.Workdir)
	}
	assertStrings(t, payload.EngineCommand, []string{"sh", "-c", "printf legacy > README.md"})
	assertStrings(t, payload.ValidationCommands, []string{"true"})
	assertStrings(t, payload.AllowedModifiedFiles, []string{"README.md"})
	assertStrings(t, payload.AllowedNewFiles, []string{})
	if payload.TimeoutSeconds != 5 {
		t.Fatalf("TimeoutSeconds = %d, want 5", payload.TimeoutSeconds)
	}
	if payload.MaxOutputBytes != 4096 {
		t.Fatalf("MaxOutputBytes = %d, want 4096", payload.MaxOutputBytes)
	}
}

func TestDecodePayloadRejectsOversizedPayloadBytes(t *testing.T) {
	secret := "SECRET_PAYLOAD_BODY_SHOULD_NOT_LEAK"
	data := []byte(strings.Repeat("{", DefaultMaxPayloadJSONBytes+1) + secret)

	_, err := DecodePayload(data)
	if err == nil {
		t.Fatal("DecodePayload() error = nil, want oversized payload rejection")
	}
	if !strings.Contains(err.Error(), "payload JSON exceeds maximum size") || !strings.Contains(err.Error(), "2097152") {
		t.Fatalf("DecodePayload() error = %q, want payload byte cap", err.Error())
	}
	if strings.Contains(err.Error(), secret) || strings.Contains(err.Error(), strings.Repeat("{", 64)) {
		t.Fatalf("DecodePayload() error echoed oversized payload body: %q", err.Error())
	}
}

func TestDecodePayloadAcceptsBEBID(t *testing.T) {
	payload, err := DecodePayload(v47PayloadJSON(`"beb_id":"BEB_011"`))
	if err != nil {
		t.Fatalf("DecodePayload() error = %v, want nil", err)
	}

	if payload.BebID != "BEB_011" {
		t.Fatalf("BebID = %q, want BEB_011", payload.BebID)
	}
}

func TestDecodePayloadDoesNotRequireLegacyCEBID(t *testing.T) {
	payload, err := DecodePayload([]byte(`{"action":"execute","beb_id":"BEB_011","work_dir":"/absolute/repo","target_branch":"sprint/beb-011","engine":"sh","engine_args":["-c","printf after > README.md"],"l2_packet":"## fake packet","trace_artifacts":[{"kind":"REQ","id":"REQ-DRY-001","version_hash":"sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}],"validation_commands":["go test ./..."],"allowed_modified_files":["README.md"],"allowed_new_files":["docs/new.md"]}`))
	if err != nil {
		t.Fatalf("DecodePayload() error = %v, want nil", err)
	}

	if payload.BebID != "BEB_011" {
		t.Fatalf("BebID = %q, want BEB_011", payload.BebID)
	}
}

func TestDecodePayloadAcceptsValidationProfiles(t *testing.T) {
	payload, err := DecodePayload(validationProfilePayloadJSON(t, map[string]interface{}{
		"validation_profiles": []string{"go-full"},
	}))
	if err != nil {
		t.Fatalf("DecodePayload() error = %v, want nil", err)
	}

	assertStrings(t, payload.ValidationProfiles, []string{"go-full"})
}

func TestDecodePayloadRejectsUnknownValidationProfile(t *testing.T) {
	_, err := DecodePayload(validationProfilePayloadJSON(t, map[string]interface{}{
		"validation_profiles": []string{"curl-production"},
	}))
	if err == nil {
		t.Fatal("DecodePayload() error = nil, want unknown validation profile rejection")
	}
	if !strings.Contains(err.Error(), "validation_profiles") || !strings.Contains(err.Error(), "curl-production") {
		t.Fatalf("DecodePayload() error = %q, want validation_profiles unknown profile", err.Error())
	}
}

func TestDecodePayloadRejectsMixedValidationProfilesAndCommands(t *testing.T) {
	_, err := DecodePayload(validationProfilePayloadJSON(t, map[string]interface{}{
		"validation_profiles": []string{"go-full"},
		"validation_commands": []string{"go test ./..."},
	}))
	if err == nil {
		t.Fatal("DecodePayload() error = nil, want mixed validation source rejection")
	}
	if !strings.Contains(err.Error(), "validation_profiles") || !strings.Contains(err.Error(), "validation_commands") {
		t.Fatalf("DecodePayload() error = %q, want validation_profiles/validation_commands rejection", err.Error())
	}
}

func TestDecodePayloadRejectsDuplicateValidationProfile(t *testing.T) {
	_, err := DecodePayload(validationProfilePayloadJSON(t, map[string]interface{}{
		"validation_profiles": []string{"go-test", "go-test"},
	}))
	if err == nil {
		t.Fatal("DecodePayload() error = nil, want duplicate validation profile rejection")
	}
	if !strings.Contains(err.Error(), "validation_profiles") || !strings.Contains(err.Error(), "duplicate") || !strings.Contains(err.Error(), "go-test") {
		t.Fatalf("DecodePayload() error = %q, want duplicate validation_profiles rejection", err.Error())
	}
}

func TestDecodePayloadLegacyValidationCommandsAreTrustedLocalCompatibilityOnly(t *testing.T) {
	// Legacy validation_commands remain accepted only for trusted-local compatibility.
	// Less-trusted/autonomous boundaries must use repository-owned validation_profiles.
	payload, err := DecodePayload(validationProfilePayloadJSON(t, map[string]interface{}{
		"validation_commands": []string{"go test ./..."},
	}))
	if err != nil {
		t.Fatalf("DecodePayload() error = %v, want legacy trusted-local compatibility", err)
	}

	assertStrings(t, payload.ValidationCommands, []string{"go test ./..."})
	assertStrings(t, payload.ValidationProfiles, nil)
}

func TestPayloadDecodeV47WorkDirMapsToWorkdir(t *testing.T) {
	payload, err := DecodePayload(v47PayloadJSON(`"work_dir":"/absolute/repo"`))
	if err != nil {
		t.Fatalf("DecodePayload() error = %v, want nil", err)
	}

	if payload.Workdir != "/absolute/repo" {
		t.Fatalf("Workdir = %q, want /absolute/repo", payload.Workdir)
	}
}

func TestPayloadDecodeV47EngineArgsNormalizeEngineCommand(t *testing.T) {
	payload, err := DecodePayload(v47PayloadJSON(`"engine":"sh","engine_args":["-c","printf after > README.md"]`))
	if err != nil {
		t.Fatalf("DecodePayload() error = %v, want nil", err)
	}

	assertStrings(t, payload.EngineCommand, []string{"sh", "-c", "printf after > README.md"})
}

func TestPayloadDecodePreservesL2Packet(t *testing.T) {
	const expectedPacket = "EXPECTED_PACKET\nwith exact bytes"
	data, err := json.Marshal(map[string]interface{}{
		"action":                 "execute",
		"beb_id":                 "BEB_011",
		"work_dir":               "/absolute/repo",
		"target_branch":          "sprint/ceb-011",
		"engine":                 "sh",
		"engine_args":            []string{"-c", "true"},
		"l2_packet":              expectedPacket,
		"trace_artifacts":        canonicalTraceArtifacts(),
		"validation_commands":    []string{"true"},
		"allowed_modified_files": []string{"README.md"},
		"allowed_new_files":      []string{},
	})
	if err != nil {
		t.Fatalf("marshal payload: %v", err)
	}

	payload, err := DecodePayload(data)
	if err != nil {
		t.Fatalf("DecodePayload() error = %v, want nil", err)
	}

	if payload.L2Packet != expectedPacket {
		t.Fatalf("L2Packet = %q, want %q", payload.L2Packet, expectedPacket)
	}
}

func TestPayloadDecodePreservesTraceArtifacts(t *testing.T) {
	expected := []TraceArtifact{
		{Kind: "REQ", ID: "REQ-042", VersionHash: "sha256:0000000000000000000000000000000000000000000000000000000000000000"},
		{Kind: "UC", ID: "UC-007", VersionHash: "sha256:1111111111111111111111111111111111111111111111111111111111111111"},
	}

	payload, err := DecodePayload(tracePayloadJSON(t, expected))
	if err != nil {
		t.Fatalf("DecodePayload() error = %v, want nil", err)
	}

	assertTraceArtifacts(t, payload.TraceArtifacts, expected)
}

func TestPayloadDecodeRejectsTooManyTraceArtifacts(t *testing.T) {
	artifacts := make([]TraceArtifact, 65)
	for i := range artifacts {
		artifacts[i] = TraceArtifact{Kind: "REQ", ID: "REQ-042", VersionHash: "sha256:0000000000000000000000000000000000000000000000000000000000000000"}
	}

	_, err := DecodePayload(tracePayloadJSON(t, artifacts))
	if err == nil {
		t.Fatal("DecodePayload() error = nil, want non-nil")
	}
	if !strings.Contains(err.Error(), "trace_artifacts") || !strings.Contains(err.Error(), "64") {
		t.Fatalf("DecodePayload() error = %q, want trace_artifacts limit", err.Error())
	}
}

func TestPayloadDecodeRejectsTraceArtifactMissingFields(t *testing.T) {
	tests := []struct {
		name     string
		artifact TraceArtifact
		want     string
	}{
		{
			name:     "missing kind",
			artifact: TraceArtifact{ID: "REQ-042", VersionHash: "sha256:0000000000000000000000000000000000000000000000000000000000000000"},
			want:     "kind",
		},
		{
			name:     "missing id",
			artifact: TraceArtifact{Kind: "REQ", VersionHash: "sha256:0000000000000000000000000000000000000000000000000000000000000000"},
			want:     "id",
		},
		{
			name:     "missing version hash",
			artifact: TraceArtifact{Kind: "REQ", ID: "REQ-042"},
			want:     "version_hash",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			_, err := DecodePayload(tracePayloadJSON(t, []TraceArtifact{tt.artifact}))
			if err == nil {
				t.Fatal("DecodePayload() error = nil, want non-nil")
			}
			if !strings.Contains(err.Error(), "trace_artifacts") || !strings.Contains(err.Error(), tt.want) {
				t.Fatalf("DecodePayload() error = %q, want trace_artifacts/%s", err.Error(), tt.want)
			}
		})
	}
}

func TestPayloadDecodeRejectsTraceArtifactWithoutSHA256Prefix(t *testing.T) {
	artifact := TraceArtifact{Kind: "REQ", ID: "REQ-042", VersionHash: "blake3:0123456789abcdef"}

	_, err := DecodePayload(tracePayloadJSON(t, []TraceArtifact{artifact}))
	if err == nil {
		t.Fatal("DecodePayload() error = nil, want non-nil")
	}
	if !strings.Contains(err.Error(), "version_hash") || !strings.Contains(err.Error(), "sha256:") {
		t.Fatalf("DecodePayload() error = %q, want version_hash sha256 prefix", err.Error())
	}
}

func TestPayloadDecodeRejectsTraceArtifactShortSHA256Hash(t *testing.T) {
	artifact := TraceArtifact{Kind: "REQ", ID: "REQ-042", VersionHash: "sha256:0123456789abcdef"}

	_, err := DecodePayload(tracePayloadJSON(t, []TraceArtifact{artifact}))
	if err == nil {
		t.Fatal("DecodePayload() error = nil, want non-nil")
	}
	if !strings.Contains(err.Error(), "version_hash") || !strings.Contains(err.Error(), "sha256") {
		t.Fatalf("DecodePayload() error = %q, want canonical sha256 version_hash", err.Error())
	}
}

func TestPayloadDecodeRejectsTraceArtifactUppercaseSHA256Hash(t *testing.T) {
	artifact := TraceArtifact{Kind: "REQ", ID: "REQ-042", VersionHash: "sha256:" + strings.Repeat("A", 64)}

	_, err := DecodePayload(tracePayloadJSON(t, []TraceArtifact{artifact}))
	if err == nil {
		t.Fatal("DecodePayload() error = nil, want non-nil")
	}
	if !strings.Contains(err.Error(), "version_hash") || !strings.Contains(err.Error(), "sha256") {
		t.Fatalf("DecodePayload() error = %q, want canonical sha256 version_hash", err.Error())
	}
}

func TestPayloadDecodeRejectsTraceArtifactNonHexSHA256Hash(t *testing.T) {
	artifact := TraceArtifact{Kind: "REQ", ID: "REQ-042", VersionHash: "sha256:" + strings.Repeat("g", 64)}

	_, err := DecodePayload(tracePayloadJSON(t, []TraceArtifact{artifact}))
	if err == nil {
		t.Fatal("DecodePayload() error = nil, want non-nil")
	}
	if !strings.Contains(err.Error(), "version_hash") || !strings.Contains(err.Error(), "sha256") {
		t.Fatalf("DecodePayload() error = %q, want canonical sha256 version_hash", err.Error())
	}
}

func TestPayloadDecodeTraceArtifactErrorDoesNotEchoLongHash(t *testing.T) {
	longHash := "sha256:" + strings.Repeat("a", 300)
	artifact := TraceArtifact{Kind: "REQ", ID: "REQ-042", VersionHash: longHash}

	_, err := DecodePayload(tracePayloadJSON(t, []TraceArtifact{artifact}))
	if err == nil {
		t.Fatal("DecodePayload() error = nil, want non-nil")
	}
	if strings.Contains(err.Error(), longHash) || strings.Contains(err.Error(), strings.Repeat("a", 64)) {
		t.Fatalf("DecodePayload() error echoed oversized version_hash: %q", err.Error())
	}
}

func TestPayloadDecodeRejectsOversizedL2Packet(t *testing.T) {
	packet := strings.Repeat("X", DefaultMaxL2PacketBytes+1)
	data, err := json.Marshal(map[string]interface{}{
		"action":                 "execute",
		"beb_id":                 "BEB_011",
		"work_dir":               "/absolute/repo",
		"target_branch":          "sprint/ceb-011",
		"engine":                 "sh",
		"engine_args":            []string{"-c", "true"},
		"l2_packet":              packet,
		"validation_commands":    []string{"true"},
		"allowed_modified_files": []string{"README.md"},
		"allowed_new_files":      []string{},
	})
	if err != nil {
		t.Fatalf("marshal payload: %v", err)
	}

	_, err = DecodePayload(data)
	if err == nil {
		t.Fatal("DecodePayload() error = nil, want non-nil")
	}
	if !strings.Contains(err.Error(), "l2_packet") {
		t.Fatalf("DecodePayload() error = %q, want l2_packet", err.Error())
	}
	if strings.Contains(err.Error(), packet) {
		t.Fatalf("DecodePayload() error echoed full l2_packet body")
	}
}

func TestPayloadDecodeRejectsMixedWorkdirConflict(t *testing.T) {
	data := []byte(`{"action":"execute","workdir":"/legacy/repo","work_dir":"/v47/repo","engine":"sh","engine_args":["-c","true"],"allowed_modified_files":["README.md"],"allowed_new_files":[],"timeout_seconds":5,"max_output_bytes":4096}`)

	_, err := DecodePayload(data)
	if err == nil {
		t.Fatal("DecodePayload() error = nil, want non-nil")
	}
	if !strings.Contains(err.Error(), "workdir") || !strings.Contains(err.Error(), "work_dir") {
		t.Fatalf("DecodePayload() error = %q, want conflict mentioning workdir and work_dir", err.Error())
	}
}

func TestPayloadDecodeRejectsMixedEngineCommandConflict(t *testing.T) {
	data := []byte(`{"action":"execute","workdir":"/absolute/repo","work_dir":"/absolute/repo","engine_command":["sh","-c","printf legacy > README.md"],"engine":"sh","engine_args":["-c","printf v47 > README.md"],"allowed_modified_files":["README.md"],"allowed_new_files":[],"timeout_seconds":5,"max_output_bytes":4096}`)

	_, err := DecodePayload(data)
	if err == nil {
		t.Fatal("DecodePayload() error = nil, want non-nil")
	}
	if !strings.Contains(err.Error(), "engine_command") || !strings.Contains(err.Error(), "engine") {
		t.Fatalf("DecodePayload() error = %q, want conflict mentioning engine_command and engine", err.Error())
	}
}

func TestPayloadDecodeCleanV47PayloadValidates(t *testing.T) {
	data := []byte(`{"action":"execute","beb_id":"BEB_011","work_dir":"/absolute/repo","target_branch":"sprint/ceb-011","engine":"sh","engine_args":["-c","printf after > README.md"],"l2_packet":"## fake packet","trace_artifacts":[{"kind":"REQ","id":"REQ-DRY-001","version_hash":"sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}],"validation_commands":["go test ./..."],"allowed_modified_files":["README.md"],"allowed_new_files":["docs/new.md"]}`)

	payload, err := DecodePayload(data)
	if err != nil {
		t.Fatalf("DecodePayload() error = %v, want nil", err)
	}

	if payload.Action != "execute" {
		t.Fatalf("Action = %q, want execute", payload.Action)
	}
	if payload.Workdir != "/absolute/repo" {
		t.Fatalf("Workdir = %q, want /absolute/repo", payload.Workdir)
	}
	assertStrings(t, payload.EngineCommand, []string{"sh", "-c", "printf after > README.md"})
	assertStrings(t, payload.ValidationCommands, []string{"go test ./..."})
	assertStrings(t, payload.AllowedModifiedFiles, []string{"README.md"})
	assertStrings(t, payload.AllowedNewFiles, []string{"docs/new.md"})
	if payload.TimeoutSeconds != DefaultTimeoutSeconds {
		t.Fatalf("TimeoutSeconds = %d, want %d", payload.TimeoutSeconds, DefaultTimeoutSeconds)
	}
	if payload.MaxOutputBytes != DefaultMaxOutputBytes {
		t.Fatalf("MaxOutputBytes = %d, want %d", payload.MaxOutputBytes, DefaultMaxOutputBytes)
	}
}

func TestPayloadDecodeV47MissingLimitsUseDeterministicDefaults(t *testing.T) {
	payload, err := DecodePayload(v47PayloadJSON(``))
	if err != nil {
		t.Fatalf("DecodePayload() error = %v, want nil", err)
	}

	if payload.TimeoutSeconds != DefaultTimeoutSeconds {
		t.Fatalf("TimeoutSeconds = %d, want %d", payload.TimeoutSeconds, DefaultTimeoutSeconds)
	}
	if payload.MaxOutputBytes != DefaultMaxOutputBytes {
		t.Fatalf("MaxOutputBytes = %d, want %d", payload.MaxOutputBytes, DefaultMaxOutputBytes)
	}
}

func TestPayloadDecodeV47RelativeWorkDirFails(t *testing.T) {
	_, err := DecodePayload(v47PayloadJSON(`"work_dir":"relative/repo"`))
	if err == nil {
		t.Fatal("DecodePayload() error = nil, want non-nil")
	}
	if !strings.Contains(err.Error(), "workdir") {
		t.Fatalf("DecodePayload() error = %q, want substring workdir", err.Error())
	}
}

func TestPayloadValidateExecuteAcceptsOptionalFullTargetHash(t *testing.T) {
	payload := Payload{
		Action:               "execute",
		Workdir:              "/tmp/blk-pipe-repo",
		TargetHash:           "0123456789abcdef0123456789abcdef01234567",
		EngineCommand:        []string{"sh", "-c", "true"},
		TraceArtifacts:       canonicalTraceArtifacts(),
		ValidationCommands:   []string{"true"},
		AllowedModifiedFiles: []string{"README.md"},
		AllowedNewFiles:      []string{},
		TimeoutSeconds:       5,
		MaxOutputBytes:       4096,
	}

	if err := payload.Validate(); err != nil {
		t.Fatalf("Validate() error = %v, want nil", err)
	}
}

func TestPayloadValidateExecuteRejectsUnsafeTargetHashWhenProvided(t *testing.T) {
	for _, targetHash := range []string{"HEAD~1", "main", "0123456789abcdef", ":(glob)**"} {
		t.Run(targetHash, func(t *testing.T) {
			payload := Payload{
				Action:               "execute",
				Workdir:              "/tmp/blk-pipe-repo",
				TargetHash:           targetHash,
				EngineCommand:        []string{"sh", "-c", "true"},
				TraceArtifacts:       canonicalTraceArtifacts(),
				ValidationCommands:   []string{"true"},
				AllowedModifiedFiles: []string{"README.md"},
				AllowedNewFiles:      []string{},
				TimeoutSeconds:       5,
				MaxOutputBytes:       4096,
			}

			err := payload.Validate()
			if err == nil {
				t.Fatal("Validate() error = nil, want target_hash rejection")
			}
			if !strings.Contains(err.Error(), "target_hash") {
				t.Fatalf("Validate() error = %q, want target_hash substring", err.Error())
			}
		})
	}
}

func TestPayloadValidateRevertAcceptsAbsoluteWorkdirAndFullTargetHash(t *testing.T) {
	payload := Payload{
		Action:     "revert",
		Workdir:    "/tmp/blk-pipe-repo",
		TargetHash: "0123456789abcdef0123456789abcdef01234567",
	}

	if err := payload.Validate(); err != nil {
		t.Fatalf("Validate() error = %v, want nil", err)
	}
}

func TestPayloadDecodeRevertV47WorkDirAndTargetHash(t *testing.T) {
	data := []byte(`{"action":"revert","work_dir":"/absolute/repo","target_hash":"0123456789abcdef0123456789abcdef01234567"}`)

	payload, err := DecodePayload(data)
	if err != nil {
		t.Fatalf("DecodePayload() error = %v, want nil", err)
	}

	if payload.Action != "revert" {
		t.Fatalf("Action = %q, want revert", payload.Action)
	}
	if payload.Workdir != "/absolute/repo" {
		t.Fatalf("Workdir = %q, want /absolute/repo", payload.Workdir)
	}
	if payload.TargetHash != "0123456789abcdef0123456789abcdef01234567" {
		t.Fatalf("TargetHash = %q", payload.TargetHash)
	}
}

func TestPayloadValidateRevertRejectsMissingOrUnsafeTargetHash(t *testing.T) {
	tests := []struct {
		name       string
		targetHash string
		want       string
	}{
		{name: "missing target hash", targetHash: "", want: "target_hash"},
		{name: "relative HEAD ancestry", targetHash: "HEAD~1", want: "target_hash"},
		{name: "relative HEAD parent", targetHash: "HEAD^", want: "target_hash"},
		{name: "reflog selector", targetHash: "@{1}", want: "target_hash"},
		{name: "branch name", targetHash: "main", want: "target_hash"},
		{name: "tag name", targetHash: "v1.2.3", want: "target_hash"},
		{name: "short hex", targetHash: "0123456789abcdef", want: "target_hash"},
		{name: "pathspec-ish", targetHash: ":(glob)**", want: "target_hash"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			payload := Payload{
				Action:     "revert",
				Workdir:    "/tmp/blk-pipe-repo",
				TargetHash: tt.targetHash,
			}

			err := payload.Validate()
			if err == nil {
				t.Fatal("Validate() error = nil, want non-nil")
			}
			if !strings.Contains(err.Error(), tt.want) {
				t.Fatalf("Validate() error = %q, want substring %q", err.Error(), tt.want)
			}
		})
	}
}

func TestPayloadValidateRevertRequiresAbsoluteWorkdir(t *testing.T) {
	payload := Payload{
		Action:     "revert",
		Workdir:    "relative/repo",
		TargetHash: "0123456789abcdef0123456789abcdef01234567",
	}

	err := payload.Validate()
	if err == nil {
		t.Fatal("Validate() error = nil, want non-nil")
	}
	if !strings.Contains(err.Error(), "workdir") {
		t.Fatalf("Validate() error = %q, want substring workdir", err.Error())
	}
}

func TestPayloadDecodeProtectedPathsStillFailForLegacyAndV47Allowlists(t *testing.T) {
	tests := []struct {
		name string
		data []byte
		want string
	}{
		{
			name: "legacy allowed_modified_files requirements path",
			data: []byte(`{"action":"execute","workdir":"/absolute/repo","engine_command":["sh","-c","true"],"trace_artifacts":[{"kind":"REQ","id":"REQ-DRY-001","version_hash":"sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}],"validation_commands":["true"],"allowed_modified_files":["docs/requirements/active/REQ-001.md"],"allowed_new_files":[],"timeout_seconds":5,"max_output_bytes":4096}`),
			want: "docs/requirements",
		},
		{
			name: "legacy allowed_modified_files active vault path",
			data: []byte(`{"action":"execute","workdir":"/absolute/repo","engine_command":["sh","-c","true"],"trace_artifacts":[{"kind":"REQ","id":"REQ-DRY-001","version_hash":"sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}],"validation_commands":["true"],"allowed_modified_files":["docs/active/REQ-001.md"],"allowed_new_files":[],"timeout_seconds":5,"max_output_bytes":4096}`),
			want: "protected docs/active path",
		},
		{
			name: "legacy allowed_new_files use case path",
			data: []byte(`{"action":"execute","workdir":"/absolute/repo","engine_command":["sh","-c","true"],"trace_artifacts":[{"kind":"REQ","id":"REQ-DRY-001","version_hash":"sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}],"validation_commands":["true"],"allowed_modified_files":[],"allowed_new_files":["docs/use_cases/staging/UC-001.md"],"timeout_seconds":5,"max_output_bytes":4096}`),
			want: "docs/use_cases",
		},
		{
			name: "legacy allowed_new_files active vault path",
			data: []byte(`{"action":"execute","workdir":"/absolute/repo","engine_command":["sh","-c","true"],"trace_artifacts":[{"kind":"REQ","id":"REQ-DRY-001","version_hash":"sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}],"validation_commands":["true"],"allowed_modified_files":[],"allowed_new_files":["docs/active/UC-001.md"],"timeout_seconds":5,"max_output_bytes":4096}`),
			want: "protected docs/active path",
		},
		{
			name: "v47 allowed_modified_files requirements path",
			data: v47PayloadJSON(`"allowed_modified_files":["docs/requirements/active/REQ-001.md"]`),
			want: "docs/requirements",
		},
		{
			name: "v47 allowed_modified_files active vault path",
			data: v47PayloadJSON(`"allowed_modified_files":["docs/active/REQ-001.md"]`),
			want: "protected docs/active path",
		},
		{
			name: "v47 allowed_new_files use case path",
			data: v47PayloadJSON(`"allowed_new_files":["docs/use_cases/staging/UC-001.md"]`),
			want: "docs/use_cases",
		},
		{
			name: "v47 allowed_new_files active vault path",
			data: v47PayloadJSON(`"allowed_new_files":["docs/active/UC-001.md"]`),
			want: "protected docs/active path",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			_, err := DecodePayload(tt.data)
			if err == nil {
				t.Fatal("DecodePayload() error = nil, want non-nil")
			}
			if !strings.Contains(err.Error(), tt.want) {
				t.Fatalf("DecodePayload() error = %q, want substring %q", err.Error(), tt.want)
			}
		})
	}
}

func TestPayloadValidateRejectsInvalidPayloads(t *testing.T) {
	tests := []struct {
		name string
		edit func(*Payload)
		want string
	}{
		{
			name: "non execute action",
			edit: func(p *Payload) { p.Action = "plan" },
			want: "action",
		},
		{
			name: "relative workdir",
			edit: func(p *Payload) { p.Workdir = "relative/repo" },
			want: "workdir",
		},
		{
			name: "empty engine command",
			edit: func(p *Payload) { p.EngineCommand = nil },
			want: "engine_command",
		},
		{
			name: "blank engine command element",
			edit: func(p *Payload) { p.EngineCommand = []string{""} },
			want: "engine_command",
		},
		{
			name: "whitespace engine command element",
			edit: func(p *Payload) { p.EngineCommand = []string{"   "} },
			want: "engine_command",
		},
		{
			name: "blank validation command",
			edit: func(p *Payload) { p.ValidationCommands = []string{"go test ./...", ""} },
			want: "validation_commands",
		},
		{
			name: "whitespace validation command",
			edit: func(p *Payload) { p.ValidationCommands = []string{"   "} },
			want: "validation_commands",
		},
		{
			name: "dot path in allowlist",
			edit: func(p *Payload) { p.AllowedModifiedFiles = []string{"."} },
			want: "allowed_modified_files",
		},
		{
			name: "glob star path in allowlist",
			edit: func(p *Payload) { p.AllowedModifiedFiles = []string{"*"} },
			want: "allowed_modified_files",
		},
		{
			name: "nested glob path in allowlist",
			edit: func(p *Payload) { p.AllowedModifiedFiles = []string{"src/*"} },
			want: "allowed_modified_files",
		},
		{
			name: "git pathspec magic in allowlist",
			edit: func(p *Payload) { p.AllowedModifiedFiles = []string{":(glob)**"} },
			want: "allowed_modified_files",
		},
		{
			name: "escape path in modified allowlist",
			edit: func(p *Payload) { p.AllowedModifiedFiles = []string{"../escape.txt"} },
			want: "allowed_modified_files",
		},
		{
			name: "escape path in new allowlist",
			edit: func(p *Payload) { p.AllowedNewFiles = []string{"safe/../escape.txt"} },
			want: "allowed_new_files",
		},
		{
			name: "absolute path in allowlist",
			edit: func(p *Payload) { p.AllowedModifiedFiles = []string{"/tmp/escape.txt"} },
			want: "allowed_modified_files",
		},
		{
			name: "unclean path in allowlist",
			edit: func(p *Payload) { p.AllowedModifiedFiles = []string{"src//allowed.txt"} },
			want: "allowed_modified_files",
		},
		{
			name: "protected BLK-req requirements artifact path",
			edit: func(p *Payload) { p.AllowedModifiedFiles = []string{"docs/requirements/active/REQ-001.md"} },
			want: "docs/requirements",
		},
		{
			name: "protected BLK-req active vault modified path",
			edit: func(p *Payload) { p.AllowedModifiedFiles = []string{"docs/active/REQ-001.md"} },
			want: "protected docs/active path",
		},
		{
			name: "protected BLK-req use case artifact path",
			edit: func(p *Payload) { p.AllowedNewFiles = []string{"docs/use_cases/staging/UC-001.md"} },
			want: "docs/use_cases",
		},
		{
			name: "protected BLK-req active vault new path",
			edit: func(p *Payload) { p.AllowedNewFiles = []string{"docs/active/UC-001.md"} },
			want: "protected docs/active path",
		},
		{
			name: "zero timeout",
			edit: func(p *Payload) { p.TimeoutSeconds = 0 },
			want: "timeout_seconds",
		},
		{
			name: "zero max output bytes",
			edit: func(p *Payload) { p.MaxOutputBytes = 0 },
			want: "max_output_bytes",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			payload := validPayload()
			tt.edit(&payload)

			err := payload.Validate()
			if err == nil {
				t.Fatal("Validate() error = nil, want non-nil")
			}
			if !strings.Contains(err.Error(), tt.want) {
				t.Fatalf("Validate() error = %q, want substring %q", err.Error(), tt.want)
			}
		})
	}
}

func TestPayloadValidateAllowsNonProtectedDocsPaths(t *testing.T) {
	payload := validPayload()
	payload.AllowedModifiedFiles = []string{"docs/plans/BLK-PIPE-003_integration-readiness-and-capability-profiles.md"}
	payload.AllowedNewFiles = []string{"docs/outcomes/BLK-PIPE-003_task-001-outcome.md"}

	if err := payload.Validate(); err != nil {
		t.Fatalf("Validate() error = %v, want nil for non-protected docs paths", err)
	}
}

func TestPayloadJSONTags(t *testing.T) {
	payload := validPayload()
	got, err := json.Marshal(payload)
	if err != nil {
		t.Fatalf("json.Marshal(Payload) error = %v", err)
	}

	wantFragments := []string{
		`"action":"execute"`,
		`"workdir":"/tmp/blk-pipe-repo"`,
		`"engine_command":["/tmp/fake-engine.sh"]`,
		`"validation_commands":["go test ./...","go vet ./..."]`,
		`"allowed_modified_files":["src/allowed.txt"]`,
		`"allowed_new_files":["src/new.txt"]`,
		`"timeout_seconds":60`,
		`"max_output_bytes":52428800`,
	}
	for _, fragment := range wantFragments {
		if !strings.Contains(string(got), fragment) {
			t.Fatalf("marshaled Payload = %s, want fragment %s", got, fragment)
		}
	}
}

func v47PayloadJSON(extra string) []byte {
	fields := []string{
		`"action":"execute"`,
		`"beb_id":"BEB_011"`,
		`"work_dir":"/absolute/repo"`,
		`"target_branch":"sprint/ceb-011"`,
		`"engine":"sh"`,
		`"engine_args":["-c","printf after > README.md"]`,
		`"l2_packet":"## fake packet"`,
		`"trace_artifacts":[{"kind":"REQ","id":"REQ-DRY-001","version_hash":"sha256:` + strings.Repeat("a", 64) + `"}]`,
		`"validation_commands":["go test ./..."]`,
		`"allowed_modified_files":["README.md"]`,
		`"allowed_new_files":[]`,
	}
	if extra != "" {
		fields = append(fields, extra)
	}
	return []byte(`{` + strings.Join(fields, `,`) + `}`)
}

func validationProfilePayloadJSON(t *testing.T, overrides map[string]interface{}) []byte {
	t.Helper()
	payload := map[string]interface{}{
		"action":                 "execute",
		"beb_id":                 "BEB_PROFILE",
		"work_dir":               "/absolute/repo",
		"target_branch":          "sprint/beb-profile",
		"engine":                 "sh",
		"engine_args":            []string{"-c", "true"},
		"l2_packet":              "opaque BEB/L2 body remains uninterpreted",
		"trace_artifacts":        canonicalTraceArtifacts(),
		"allowed_modified_files": []string{"README.md"},
		"allowed_new_files":      []string{},
	}
	for key, value := range overrides {
		payload[key] = value
	}
	data, err := json.Marshal(payload)
	if err != nil {
		t.Fatalf("marshal validation profile payload: %v", err)
	}
	return data
}

func tracePayloadJSON(t *testing.T, artifacts []TraceArtifact) []byte {
	t.Helper()
	data, err := json.Marshal(map[string]interface{}{
		"action":                 "execute",
		"beb_id":                 "BEB_TRACE",
		"work_dir":               "/absolute/repo",
		"engine":                 "sh",
		"engine_args":            []string{"-c", "true"},
		"l2_packet":              "opaque BEB/L2 body remains uninterpreted",
		"validation_commands":    []string{"true"},
		"allowed_modified_files": []string{"README.md"},
		"allowed_new_files":      []string{},
		"trace_artifacts":        artifacts,
	})
	if err != nil {
		t.Fatalf("marshal trace payload: %v", err)
	}
	return data
}

func assertStrings(t *testing.T, got []string, want []string) {
	t.Helper()
	if len(got) != len(want) {
		t.Fatalf("slice length = %d (%v), want %d (%v)", len(got), got, len(want), want)
	}
	for i := range want {
		if got[i] != want[i] {
			t.Fatalf("slice[%d] = %q in %v, want %q in %v", i, got[i], got, want[i], want)
		}
	}
}

func assertTraceArtifacts(t *testing.T, got []TraceArtifact, want []TraceArtifact) {
	t.Helper()
	if len(got) != len(want) {
		t.Fatalf("trace_artifacts length = %d (%v), want %d (%v)", len(got), got, len(want), want)
	}
	for i := range want {
		if got[i] != want[i] {
			t.Fatalf("trace_artifacts[%d] = %#v, want %#v", i, got[i], want[i])
		}
	}
}

func TestReportJSONTags(t *testing.T) {
	report := Report{
		Status:            "SUCCESS",
		Action:            "execute",
		Workdir:           "/tmp/blk-pipe-repo",
		BebID:             "BEB_011",
		CommitHash:        "abc123",
		StagedFiles:       []string{"src/allowed.txt"},
		DestroyedFiles:    []string{"src/unauthorized.txt"},
		EngineExitCode:    0,
		EngineOutputBytes: 1234,
		Error:             "",
	}

	got, err := json.Marshal(report)
	if err != nil {
		t.Fatalf("json.Marshal(Report) error = %v", err)
	}

	wantFragments := []string{
		`"status":"SUCCESS"`,
		`"action":"execute"`,
		`"workdir":"/tmp/blk-pipe-repo"`,
		`"beb_id":"BEB_011"`,
		`"commit_hash":"abc123"`,
		`"staged_files":["src/allowed.txt"]`,
		`"destroyed_files":["src/unauthorized.txt"]`,
		`"engine_exit_code":0`,
		`"engine_output_bytes":1234`,
	}
	for _, fragment := range wantFragments {
		if !strings.Contains(string(got), fragment) {
			t.Fatalf("marshaled Report = %s, want fragment %s", got, fragment)
		}
	}
	if strings.Contains(string(got), "ceb_id") {
		t.Fatalf("marshaled Report = %s, must not emit legacy ceb_id", got)
	}
}
