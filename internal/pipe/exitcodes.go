package pipe

const (
	ExitSuccess              = 0
	ExitInvalidPayload       = 2
	ExitUnauthorizedMutation = 3
	ExitEngineFailed         = 4
	ExitOutputFlood          = 5
	ExitEngineTimeout        = 6
	ExitGitDirty             = 7
	ExitInternalError        = 9
)
