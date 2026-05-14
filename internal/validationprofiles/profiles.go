package validationprofiles

import "fmt"

type CommandSpec struct {
	Profile    string
	Name       string
	Argv       []string
	Env        []string
	Display    string
	Capability string
}

var registry = map[string][]CommandSpec{
	"go-test": {
		{Profile: "go-test", Name: "go-test", Argv: []string{"go", "test", "./..."}, Display: "go test ./...", Capability: "local-go-test"},
	},
	"go-vet": {
		{Profile: "go-vet", Name: "go-vet", Argv: []string{"go", "vet", "./..."}, Display: "go vet ./...", Capability: "local-go-vet"},
	},
	"go-full": {
		{Profile: "go-full", Name: "go-test", Argv: []string{"go", "test", "./..."}, Display: "go test ./...", Capability: "local-go-test"},
		{Profile: "go-full", Name: "go-vet", Argv: []string{"go", "vet", "./..."}, Display: "go vet ./...", Capability: "local-go-vet"},
	},
	"python-unittest": {
		{
			Profile:    "python-unittest",
			Name:       "python-unittest-discover",
			Argv:       []string{"python3", "-m", "unittest", "discover", "-s", "python", "-p", "test_*.py"},
			Env:        []string{"PYTHONPATH=python", "PYTHONDONTWRITEBYTECODE=1"},
			Display:    "PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'",
			Capability: "local-python-unittest",
		},
	},
	"docs-doctrine-gates": {
		{
			Profile:    "docs-doctrine-gates",
			Name:       "active-doctrine-gates",
			Argv:       []string{"python3", "-m", "unittest", "python.test_active_doctrine_review_gates", "-v"},
			Env:        []string{"PYTHONPATH=python", "PYTHONDONTWRITEBYTECODE=1"},
			Display:    "PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v",
			Capability: "local-doctrine-gate",
		},
	},
	"kuronode-power-of-ten-static-fixture": {
		{
			Profile:    "kuronode-power-of-ten-static-fixture",
			Name:       "kuronode-power-of-ten-static-fixture",
			Argv:       []string{"python3", "-m", "unittest", "python.test_kuronode_power_of_ten_static_profile", "-q"},
			Env:        []string{"PYTHONPATH=python", "PYTHONDONTWRITEBYTECODE=1"},
			Display:    "PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_kuronode_power_of_ten_static_profile -q",
			Capability: "fixture-only-python-unittest",
		},
	},
}

// Validate proves profile names are known and non-duplicated without resolving
// any caller-provided command text. Profile argv/env specs are repository-owned.
func Validate(names []string) error {
	seen := make(map[string]struct{}, len(names))
	for i, name := range names {
		if name == "" {
			return fmt.Errorf("validation_profiles[%d] must not be empty", i)
		}
		if _, ok := seen[name]; ok {
			return fmt.Errorf("validation_profiles contains duplicate profile %q", name)
		}
		seen[name] = struct{}{}
		specs, ok := registry[name]
		if !ok {
			return fmt.Errorf("validation_profiles[%d] references unknown profile %q", i, name)
		}
		if err := validateSpecs(name, specs); err != nil {
			return err
		}
	}
	return nil
}

// Resolve returns a defensive copy of deterministic repository-owned display
// strings for the requested profile names. These strings are evidence only; the
// profile execution path uses ResolveSpecs structured argv/env specs.
func Resolve(names []string) ([]string, error) {
	specs, err := ResolveSpecs(names)
	if err != nil {
		return nil, err
	}
	return DisplayCommands(specs), nil
}

// ResolveSpecs returns deterministic repository-owned argv/env specs for the
// requested profile names. The returned specs are deep copies and must be passed
// to exec without shell interpretation.
func ResolveSpecs(names []string) ([]CommandSpec, error) {
	if err := Validate(names); err != nil {
		return nil, err
	}
	specs := []CommandSpec{}
	for _, name := range names {
		specs = append(specs, copySpecs(registry[name])...)
	}
	return specs, nil
}

// DisplayCommands returns stable human-readable evidence strings for resolved
// specs. They are not used as executable shell strings for repository profiles.
func DisplayCommands(specs []CommandSpec) []string {
	commands := make([]string, 0, len(specs))
	for _, spec := range specs {
		commands = append(commands, spec.Display)
	}
	return commands
}

// ArgvCommands returns a defensive copy of resolved argv evidence.
func ArgvCommands(specs []CommandSpec) [][]string {
	argv := make([][]string, 0, len(specs))
	for _, spec := range specs {
		argv = append(argv, append([]string{}, spec.Argv...))
	}
	return argv
}

// ProfileCapabilities returns stable capability evidence for the named profiles.
func ProfileCapabilities(names []string) []string {
	specs, err := ResolveSpecs(names)
	if err != nil {
		return nil
	}
	return CapabilitiesForSpecs(specs)
}

// CapabilitiesForSpecs returns stable capability labels from already-resolved specs.
func CapabilitiesForSpecs(specs []CommandSpec) []string {
	capabilities := make([]string, 0, len(specs))
	for _, spec := range specs {
		capabilities = append(capabilities, spec.Capability)
	}
	return capabilities
}

// KnownProfiles returns a defensive copy of the registry display commands for
// documentation and tests. Callers must not infer authority from map iteration order.
func KnownProfiles() map[string][]string {
	copy := make(map[string][]string, len(registry))
	for name, specs := range registry {
		copy[name] = DisplayCommands(copySpecs(specs))
	}
	return copy
}

func KnownProfileSpecs() map[string][]CommandSpec {
	copy := make(map[string][]CommandSpec, len(registry))
	for name, specs := range registry {
		copy[name] = copySpecs(specs)
	}
	return copy
}

func validateSpecs(profile string, specs []CommandSpec) error {
	if len(specs) == 0 {
		return fmt.Errorf("validation profile %q must resolve to at least one command spec", profile)
	}
	for i, spec := range specs {
		if spec.Profile == "" {
			return fmt.Errorf("validation profile %q spec %d missing profile", profile, i)
		}
		if spec.Name == "" {
			return fmt.Errorf("validation profile %q spec %d missing name", profile, i)
		}
		if len(spec.Argv) == 0 {
			return fmt.Errorf("validation profile %q spec %d must include argv", profile, i)
		}
		for j, arg := range spec.Argv {
			if arg == "" {
				return fmt.Errorf("validation profile %q spec %d argv[%d] must not be empty", profile, i, j)
			}
		}
		if len(spec.Argv) >= 2 && spec.Argv[0] == "sh" && spec.Argv[1] == "-c" {
			return fmt.Errorf("validation profile %q spec %d must not use sh -c shell wrapper", profile, i)
		}
		if spec.Display == "" {
			return fmt.Errorf("validation profile %q spec %d missing display evidence", profile, i)
		}
		if !isAllowedCapability(spec.Capability) {
			return fmt.Errorf("validation profile %q spec %d has unsupported capability %q", profile, i, spec.Capability)
		}
	}
	return nil
}

func isAllowedCapability(capability string) bool {
	switch capability {
	case "local-go-test", "local-go-vet", "local-python-unittest", "local-doctrine-gate", "fixture-only-python-unittest":
		return true
	default:
		return false
	}
}

func copySpecs(specs []CommandSpec) []CommandSpec {
	copy := make([]CommandSpec, len(specs))
	for i, spec := range specs {
		copy[i] = CommandSpec{
			Profile:    spec.Profile,
			Name:       spec.Name,
			Argv:       append([]string{}, spec.Argv...),
			Env:        append([]string{}, spec.Env...),
			Display:    spec.Display,
			Capability: spec.Capability,
		}
	}
	return copy
}
