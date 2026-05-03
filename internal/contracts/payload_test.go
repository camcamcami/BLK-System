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
		ValidationCommands:   []string{"go test ./...", "go vet ./..."},
		AllowedModifiedFiles: []string{"src/allowed.txt"},
		AllowedNewFiles:      []string{"src/new.txt"},
		TimeoutSeconds:       60,
		MaxOutputBytes:       52428800,
	}
}

func TestPayloadValidateAcceptsValidPayload(t *testing.T) {
	if err := validPayload().Validate(); err != nil {
		t.Fatalf("Validate() error = %v, want nil", err)
	}
}

func TestPayloadDecodeLegacyPayloadStillValidates(t *testing.T) {
	data := []byte(`{"action":"execute","workdir":"/absolute/repo","engine_command":["sh","-c","printf legacy > README.md"],"allowed_modified_files":["README.md"],"allowed_new_files":[],"timeout_seconds":5,"max_output_bytes":4096}`)

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
	assertStrings(t, payload.ValidationCommands, []string{})
	assertStrings(t, payload.AllowedModifiedFiles, []string{"README.md"})
	assertStrings(t, payload.AllowedNewFiles, []string{})
	if payload.TimeoutSeconds != 5 {
		t.Fatalf("TimeoutSeconds = %d, want 5", payload.TimeoutSeconds)
	}
	if payload.MaxOutputBytes != 4096 {
		t.Fatalf("MaxOutputBytes = %d, want 4096", payload.MaxOutputBytes)
	}
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
	data := []byte(`{"action":"execute","ceb_id":"CEB_011","work_dir":"/absolute/repo","target_branch":"sprint/ceb-011","engine":"sh","engine_args":["-c","printf after > README.md"],"l2_packet":"## fake packet","validation_commands":["go test ./..."],"allowed_modified_files":["README.md"],"allowed_new_files":["docs/new.md"]}`)

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
			data: []byte(`{"action":"execute","workdir":"/absolute/repo","engine_command":["sh","-c","true"],"allowed_modified_files":["docs/requirements/active/REQ-001.md"],"allowed_new_files":[],"timeout_seconds":5,"max_output_bytes":4096}`),
			want: "docs/requirements",
		},
		{
			name: "legacy allowed_new_files use case path",
			data: []byte(`{"action":"execute","workdir":"/absolute/repo","engine_command":["sh","-c","true"],"allowed_modified_files":[],"allowed_new_files":["docs/use_cases/staging/UC-001.md"],"timeout_seconds":5,"max_output_bytes":4096}`),
			want: "docs/use_cases",
		},
		{
			name: "v47 allowed_modified_files requirements path",
			data: v47PayloadJSON(`"allowed_modified_files":["docs/requirements/active/REQ-001.md"]`),
			want: "docs/requirements",
		},
		{
			name: "v47 allowed_new_files use case path",
			data: v47PayloadJSON(`"allowed_new_files":["docs/use_cases/staging/UC-001.md"]`),
			want: "docs/use_cases",
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
			name: "protected BLK-req use case artifact path",
			edit: func(p *Payload) { p.AllowedNewFiles = []string{"docs/use_cases/staging/UC-001.md"} },
			want: "docs/use_cases",
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
		`"ceb_id":"CEB_011"`,
		`"work_dir":"/absolute/repo"`,
		`"target_branch":"sprint/ceb-011"`,
		`"engine":"sh"`,
		`"engine_args":["-c","printf after > README.md"]`,
		`"l2_packet":"## fake packet"`,
		`"validation_commands":["go test ./..."]`,
		`"allowed_modified_files":["README.md"]`,
		`"allowed_new_files":[]`,
	}
	if extra != "" {
		fields = append(fields, extra)
	}
	return []byte(`{` + strings.Join(fields, `,`) + `}`)
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

func TestReportJSONTags(t *testing.T) {
	report := Report{
		Status:            "SUCCESS",
		Action:            "execute",
		Workdir:           "/tmp/blk-pipe-repo",
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
}
