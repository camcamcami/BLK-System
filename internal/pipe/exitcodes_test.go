package pipe

import "testing"

func TestExitCodes(t *testing.T) {
	tests := map[string]int{
		"ExitSuccess":              ExitSuccess,
		"ExitFatalSystemPanic":     ExitFatalSystemPanic,
		"ExitInvalidPayload":       ExitInvalidPayload,
		"ExitValidationFailed":     ExitValidationFailed,
		"ExitUnauthorizedMutation": ExitUnauthorizedMutation,
		"ExitInvalidRevertAnchor":  ExitInvalidRevertAnchor,
		"ExitOutputFlood":          ExitOutputFlood,
		"ExitEngineTimeout":        ExitEngineTimeout,
		"ExitGitDirty":             ExitGitDirty,
		"ExitInternalError":        ExitInternalError,
	}

	want := map[string]int{
		"ExitSuccess":              0,
		"ExitFatalSystemPanic":     1,
		"ExitInvalidPayload":       8,
		"ExitValidationFailed":     2,
		"ExitUnauthorizedMutation": 3,
		"ExitInvalidRevertAnchor":  4,
		"ExitOutputFlood":          5,
		"ExitEngineTimeout":        6,
		"ExitGitDirty":             7,
		"ExitInternalError":        9,
	}

	for name, got := range tests {
		if got != want[name] {
			t.Fatalf("%s = %d, want %d", name, got, want[name])
		}
	}
}

func TestExitCodesInvalidPayloadAndValidationFailureAreDistinct(t *testing.T) {
	if ExitInvalidPayload == ExitValidationFailed {
		t.Fatalf("invalid payload and validation failure share code %d", ExitInvalidPayload)
	}
}

func TestExitCodesEngineFailuresDoNotUseInvalidRevertAnchor(t *testing.T) {
	if ExitFatalSystemPanic == ExitInvalidRevertAnchor {
		t.Fatalf("fatal engine/system failures share code %d with invalid revert anchor", ExitFatalSystemPanic)
	}
	if ExitFatalSystemPanic == 4 {
		t.Fatalf("fatal engine/system failures must not use legacy engine-failure code 4")
	}
}
