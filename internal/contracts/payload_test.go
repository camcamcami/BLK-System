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
			name: "protected requirements doc path",
			edit: func(p *Payload) { p.AllowedModifiedFiles = []string{"docs/requirements/active/REQ-001.md"} },
			want: "docs/requirements",
		},
		{
			name: "protected use case doc path",
			edit: func(p *Payload) { p.AllowedNewFiles = []string{"docs/use_cases/UC-001.md"} },
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
		`"error":""`,
	}
	for _, fragment := range wantFragments {
		if !strings.Contains(string(got), fragment) {
			t.Fatalf("marshaled Report = %s, want fragment %s", got, fragment)
		}
	}
}
