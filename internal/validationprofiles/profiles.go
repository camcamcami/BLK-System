package validationprofiles

import "fmt"

var registry = map[string][]string{
	"go-test":             {"go test ./..."},
	"go-vet":              {"go vet ./..."},
	"go-full":             {"go test ./...", "go vet ./..."},
	"python-unittest":     {"PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'"},
	"docs-doctrine-gates": {"PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v"},
}

// Validate proves profile names are known and non-duplicated without resolving
// any caller-provided command text. Profile command arrays are repository-owned.
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
		if _, ok := registry[name]; !ok {
			return fmt.Errorf("validation_profiles[%d] references unknown profile %q", i, name)
		}
	}
	return nil
}

// Resolve returns a defensive copy of the deterministic repository-owned command
// arrays for the requested profile names.
func Resolve(names []string) ([]string, error) {
	if err := Validate(names); err != nil {
		return nil, err
	}
	commands := []string{}
	for _, name := range names {
		commands = append(commands, registry[name]...)
	}
	return append([]string{}, commands...), nil
}

// KnownProfiles returns a defensive copy of the registry for documentation and
// tests. Callers must not infer authority from map iteration order.
func KnownProfiles() map[string][]string {
	copy := make(map[string][]string, len(registry))
	for name, commands := range registry {
		copy[name] = append([]string{}, commands...)
	}
	return copy
}
