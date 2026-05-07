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
