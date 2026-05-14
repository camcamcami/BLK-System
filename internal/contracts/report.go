package contracts

import "encoding/json"

type DiffSummary struct {
	FilesChanged int      `json:"files_changed"`
	Insertions   int      `json:"insertions"`
	Deletions    int      `json:"deletions"`
	Files        []string `json:"files"`
}

type Report struct {
	Status                        string            `json:"status"`
	ExitCode                      int               `json:"exit_code"`
	Action                        string            `json:"action"`
	Workdir                       string            `json:"workdir"`
	WorkDir                       string            `json:"work_dir,omitempty"`
	TargetBranch                  string            `json:"target_branch,omitempty"`
	TargetHash                    string            `json:"target_hash,omitempty"`
	PayloadTrustBoundary          string            `json:"payload_trust_boundary,omitempty"`
	BebID                         string            `json:"beb_id,omitempty"`
	CommitHash                    string            `json:"commit_hash"`
	PreEngineHash                 string            `json:"pre_engine_hash,omitempty"`
	GitDiff                       string            `json:"git_diff"`
	EngineLogs                    string            `json:"engine_logs"`
	TraceArtifacts                []TraceArtifact   `json:"trace_artifacts"`
	ValidationLogs                map[string]string `json:"validation_logs"`
	ValidationCommandSource       string            `json:"validation_command_source"`
	ValidationTrustBoundary       string            `json:"validation_trust_boundary"`
	ValidationProfiles            []string          `json:"validation_profiles"`
	ValidationProfileCapabilities []string          `json:"validation_profile_capabilities"`
	ResolvedValidationCommands    []string          `json:"resolved_validation_commands"`
	ResolvedValidationArgv        [][]string        `json:"resolved_validation_argv"`
	DiffSummary                   *DiffSummary      `json:"diff_summary,omitempty"`
	UntrackedFiles                []string          `json:"untracked_files"`
	StagedFiles                   []string          `json:"staged_files"`
	DestroyedFiles                []string          `json:"destroyed_files"`
	EngineExitCode                int               `json:"engine_exit_code"`
	EngineOutputBytes             int64             `json:"engine_output_bytes"`
	Error                         string            `json:"error"`
}

func NewReport() Report {
	return Report{
		ValidationLogs:                map[string]string{},
		ValidationProfiles:            []string{},
		ValidationProfileCapabilities: []string{},
		ResolvedValidationCommands:    []string{},
		ResolvedValidationArgv:        [][]string{},
		TraceArtifacts:                []TraceArtifact{},
		UntrackedFiles:                []string{},
		StagedFiles:                   []string{},
		DestroyedFiles:                []string{},
	}
}

func (r Report) MarshalJSON() ([]byte, error) {
	type reportAlias Report
	alias := reportAlias(r)
	if alias.ValidationLogs == nil {
		alias.ValidationLogs = map[string]string{}
	}
	if alias.TraceArtifacts == nil {
		alias.TraceArtifacts = []TraceArtifact{}
	}
	if alias.ValidationProfiles == nil {
		alias.ValidationProfiles = []string{}
	}
	if alias.ValidationProfileCapabilities == nil {
		alias.ValidationProfileCapabilities = []string{}
	}
	if alias.ResolvedValidationCommands == nil {
		alias.ResolvedValidationCommands = []string{}
	}
	if alias.ResolvedValidationArgv == nil {
		alias.ResolvedValidationArgv = [][]string{}
	}
	if alias.UntrackedFiles == nil {
		alias.UntrackedFiles = []string{}
	}
	if alias.StagedFiles == nil {
		alias.StagedFiles = []string{}
	}
	if alias.DestroyedFiles == nil {
		alias.DestroyedFiles = []string{}
	}
	return json.Marshal(alias)
}
