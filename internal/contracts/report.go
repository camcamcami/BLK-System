package contracts

type Report struct {
	Status            string   `json:"status"`
	Action            string   `json:"action"`
	Workdir           string   `json:"workdir"`
	CommitHash        string   `json:"commit_hash"`
	StagedFiles       []string `json:"staged_files"`
	DestroyedFiles    []string `json:"destroyed_files"`
	EngineExitCode    int      `json:"engine_exit_code"`
	EngineOutputBytes int64    `json:"engine_output_bytes"`
	Error             string   `json:"error"`
}
