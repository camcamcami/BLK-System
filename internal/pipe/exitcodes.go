package pipe

const (
	ExitSuccess              = 0
	ExitFatalSystemPanic     = 1
	ExitInvalidPayload       = 2
	ExitValidationFailed     = 2
	ExitUnauthorizedMutation = 3
	ExitInvalidRevertAnchor  = 4
	ExitOutputFlood          = 5
	ExitEngineTimeout        = 6
	ExitGitDirty             = 7
	ExitInternalError        = 9
)
