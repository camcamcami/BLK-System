package pipe

import "testing"

func TestExitCodes(t *testing.T) {
	tests := map[string]int{
		"ExitSuccess":              ExitSuccess,
		"ExitInvalidPayload":       ExitInvalidPayload,
		"ExitUnauthorizedMutation": ExitUnauthorizedMutation,
		"ExitEngineFailed":         ExitEngineFailed,
		"ExitOutputFlood":          ExitOutputFlood,
		"ExitEngineTimeout":        ExitEngineTimeout,
		"ExitGitDirty":             ExitGitDirty,
		"ExitInternalError":        ExitInternalError,
	}

	want := map[string]int{
		"ExitSuccess":              0,
		"ExitInvalidPayload":       2,
		"ExitUnauthorizedMutation": 3,
		"ExitEngineFailed":         4,
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
