package validationprofiles

import (
	"reflect"
	"strings"
	"testing"
)

func TestResolveKnownProfilesToRepositoryOwnedCommands(t *testing.T) {
	commands, err := Resolve([]string{"go-full", "docs-doctrine-gates"})
	if err != nil {
		t.Fatalf("Resolve() error = %v, want nil", err)
	}

	want := []string{
		"go test ./...",
		"go vet ./...",
		"PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v",
	}
	if !reflect.DeepEqual(commands, want) {
		t.Fatalf("Resolve() = %#v, want %#v", commands, want)
	}
}

func TestResolveKuronodePowerOfTenFixtureProfile(t *testing.T) {
	commands, err := Resolve([]string{"kuronode-power-of-ten-static-fixture"})
	if err != nil {
		t.Fatalf("Resolve() error = %v, want nil", err)
	}

	want := []string{"PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_kuronode_power_of_ten_static_profile -q"}
	if !reflect.DeepEqual(commands, want) {
		t.Fatalf("Resolve() = %#v, want %#v", commands, want)
	}
}

func TestResolveKuronodeWorktreeStaticProfile(t *testing.T) {
	commands, err := Resolve([]string{"kuronode-worktree-static"})
	if err != nil {
		t.Fatalf("Resolve() error = %v, want nil", err)
	}

	want := []string{"git diff --check -- ."}
	if !reflect.DeepEqual(commands, want) {
		t.Fatalf("Resolve() = %#v, want %#v", commands, want)
	}

	specs, err := ResolveSpecs([]string{"kuronode-worktree-static"})
	if err != nil {
		t.Fatalf("ResolveSpecs() error = %v, want nil", err)
	}
	if !reflect.DeepEqual(specs[0].Argv, []string{"git", "diff", "--check", "--", "."}) {
		t.Fatalf("kuronode-worktree-static argv = %#v", specs[0].Argv)
	}
	if specs[0].Capability != "local-git-diff-check" {
		t.Fatalf("kuronode-worktree-static capability = %q", specs[0].Capability)
	}
}

func TestKuronodePowerOfTenFixtureProfileCommandDeniesLiveAuthority(t *testing.T) {
	commands, err := Resolve([]string{"kuronode-power-of-ten-static-fixture"})
	if err != nil {
		t.Fatalf("Resolve() error = %v, want nil", err)
	}
	if len(commands) != 1 {
		t.Fatalf("len(commands) = %d, want 1", len(commands))
	}

	forbidden := []string{
		"npm", "npx", "pnpm", "yarn", "bun", "pip", "uv ", "go get",
		"curl", "wget", "ssh", "scp", "rsync", "http://", "https://",
		"tsc", "eslint", "prettier", " node ", "node -", "deno", "docker",
		"codex", "blk-test", "beo", "rtm", "docs/active", "docs/protected",
		"Kuronode-v1", "../", "git ",
	}
	lower := strings.ToLower(commands[0])
	for _, token := range forbidden {
		if strings.Contains(lower, strings.ToLower(token)) {
			t.Fatalf("kuronode fixture profile command %q contains forbidden token %q", commands[0], token)
		}
	}
}

func TestResolveReturnsDefensiveCopy(t *testing.T) {
	first, err := Resolve([]string{"go-test"})
	if err != nil {
		t.Fatalf("Resolve() error = %v, want nil", err)
	}
	first[0] = "curl https://example.invalid"

	second, err := Resolve([]string{"go-test"})
	if err != nil {
		t.Fatalf("Resolve() second error = %v, want nil", err)
	}
	if !reflect.DeepEqual(second, []string{"go test ./..."}) {
		t.Fatalf("second Resolve() = %#v, registry was mutated", second)
	}
}

func TestValidateRejectsUnknownDuplicateAndEmptyProfiles(t *testing.T) {
	tests := []struct {
		name     string
		profiles []string
		want     string
	}{
		{name: "unknown", profiles: []string{"curl-production"}, want: "unknown profile \"curl-production\""},
		{name: "duplicate", profiles: []string{"go-test", "go-test"}, want: "duplicate profile \"go-test\""},
		{name: "empty", profiles: []string{""}, want: "must not be empty"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := Validate(tt.profiles)
			if err == nil {
				t.Fatal("Validate() error = nil, want non-nil")
			}
			if !strings.Contains(err.Error(), tt.want) {
				t.Fatalf("Validate() error = %q, want substring %q", err.Error(), tt.want)
			}
		})
	}
}

func TestKnownProfilesReturnsDefensiveCopy(t *testing.T) {
	known := KnownProfiles()
	known["go-test"][0] = "curl https://example.invalid"

	commands, err := Resolve([]string{"go-test"})
	if err != nil {
		t.Fatalf("Resolve() error = %v, want nil", err)
	}
	if !reflect.DeepEqual(commands, []string{"go test ./..."}) {
		t.Fatalf("Resolve() after KnownProfiles mutation = %#v", commands)
	}
}

func TestResolveSpecsReturnsStructuredArgvWithoutShell(t *testing.T) {
	specs, err := ResolveSpecs([]string{"python-unittest", "docs-doctrine-gates", "kuronode-power-of-ten-static-fixture"})
	if err != nil {
		t.Fatalf("ResolveSpecs() error = %v, want nil", err)
	}
	if len(specs) != 3 {
		t.Fatalf("len(specs) = %d, want 3", len(specs))
	}
	wantFirstArgv := []string{"python3", "-m", "unittest", "discover", "-s", "python", "-p", "test_*.py"}
	if !reflect.DeepEqual(specs[0].Argv, wantFirstArgv) {
		t.Fatalf("python-unittest argv = %#v, want %#v", specs[0].Argv, wantFirstArgv)
	}
	for _, spec := range specs {
		if len(spec.Argv) == 0 {
			t.Fatalf("profile %q has empty argv", spec.Profile)
		}
		if len(spec.Argv) >= 2 && spec.Argv[0] == "sh" && spec.Argv[1] == "-c" {
			t.Fatalf("profile %q still resolves to shell wrapper argv: %#v", spec.Profile, spec.Argv)
		}
		joined := strings.Join(spec.Argv, " ")
		for _, forbidden := range []string{" sh -c ", "bash -c", "&&", ";", "|", "`"} {
			if strings.Contains(joined, forbidden) {
				t.Fatalf("profile %q structured argv contains shell token %q in %#v", spec.Profile, forbidden, spec.Argv)
			}
		}
	}
}

func TestResolveSpecEvidenceReturnsDefensiveCopies(t *testing.T) {
	first, err := ResolveSpecs([]string{"python-unittest"})
	if err != nil {
		t.Fatalf("ResolveSpecs() error = %v, want nil", err)
	}
	first[0].Argv[0] = "curl"
	first[0].Env[0] = "PYTHONPATH=/tmp/evil"

	second, err := ResolveSpecs([]string{"python-unittest"})
	if err != nil {
		t.Fatalf("ResolveSpecs() second error = %v, want nil", err)
	}
	if !reflect.DeepEqual(second[0].Argv, []string{"python3", "-m", "unittest", "discover", "-s", "python", "-p", "test_*.py"}) {
		t.Fatalf("ResolveSpecs() leaked argv mutation: %#v", second[0].Argv)
	}
	if !reflect.DeepEqual(second[0].Env, []string{"PYTHONPATH=python", "PYTHONDONTWRITEBYTECODE=1"}) {
		t.Fatalf("python-unittest Env = %#v, want deterministic Python env", second[0].Env)
	}
}

func TestProfileCapabilitiesAreExplicitAndSafe(t *testing.T) {
	capabilities := ProfileCapabilities([]string{"go-full", "python-unittest", "docs-doctrine-gates", "kuronode-power-of-ten-static-fixture", "kuronode-worktree-static"})
	want := []string{"local-go-test", "local-go-vet", "local-python-unittest", "local-doctrine-gate", "fixture-only-python-unittest", "local-git-diff-check"}
	if !reflect.DeepEqual(capabilities, want) {
		t.Fatalf("ProfileCapabilities() = %#v, want %#v", capabilities, want)
	}
	for _, capability := range capabilities {
		lower := strings.ToLower(capability)
		for _, forbidden := range []string{"network", "package", "npm", "pip", "curl", "protected", "beo", "rtm", "sandbox"} {
			if strings.Contains(lower, forbidden) {
				t.Fatalf("capability %q contains forbidden authority token %q", capability, forbidden)
			}
		}
	}
}
