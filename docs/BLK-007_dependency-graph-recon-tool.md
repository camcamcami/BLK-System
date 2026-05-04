# BLK-007 — Dependency Graph Reconnaissance Tool

**Status:** Active Planning Doctrine
**Purpose:** Specify the read-only `analyze_dependency_graph` reconnaissance tool Hermes uses to resolve TypeScript dependencies before writing bounded execution briefs.
**Target Environment:** Ubuntu 22.04 / 24.04

---

**Source Version:** 1.2

---

## 1. Objective

Create a new, isolated Python module called `recon.py` that exposes one function:

```python
analyze_dependency_graph(target_file: str, work_dir: str) -> dict
```

---

## 2. Security & Architectural Constraints (Non-Negotiable)

- **Do NOT** add this logic to `BlkPipeAdapter.py`.
- **Do NOT** give Hermes a generic shell execution tool.
- The tool must be read-only and single-purpose.

## 2.5 Known Operational Limitation (V1.0)

This tool currently only resolves **outbound dependencies** (files the target imports). It does **not** scan the entire workspace for **inbound dependents** (files that import the target file).

- **Rationale:** This is a deliberate V1 optimization. Performing a full workspace scan (`npx madge <work_dir> --depends <target_file>`) would require parsing the entire repository's AST during every planning phase, introducing unacceptable latency.
- **Impact:** If Hermes modifies an exported contract (e.g. a function signature or interface), upstream files that depend on it may not be included in `AllowedModifiedFiles`, potentially causing an Exit 3 on the next iteration.
- **Future Work:** If telemetry shows a high rate of contract-breaking Exit 3 failures, V2 will introduce inbound dependency resolution.

---

## 3. Environment Setup (Ubuntu)

```bash
npm install --save-dev madge
npx madge --version
touch recon.py
```

---

## 4. Implementation — `recon.py`

```python
import subprocess
import json
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


def analyze_dependency_graph(target_file: str, work_dir: str) -> Dict[str, Any]:
    """
    Deterministic dependency resolver for Hermes.
    Uses locally installed madge to parse TypeScript imports.
    """
    try:
        result = subprocess.run(
            ["npx", "madge", target_file, "--json"],
            cwd=work_dir,
            capture_output=True,
            text=True,
            check=True,
            timeout=45
        )

        raw_data = json.loads(result.stdout)
        dependencies: List[str] = []
        for deps in raw_data.values():
            dependencies.extend(deps)

        unique_deps = sorted(list(set(dependencies)))

        return {
            "target": target_file,
            "dependencies": unique_deps,
            "error": None
        }

    except subprocess.TimeoutExpired:
        return {
            "target": target_file,
            "dependencies": [],
            "error": "Timeout while parsing dependencies"
        }

    except subprocess.CalledProcessError as e:
        return {
            "target": target_file,
            "dependencies": [],
            "error": f"madge error: {e.stderr[:300]}"
        }

    except json.JSONDecodeError:
        return {
            "target": target_file,
            "dependencies": [],
            "error": "Invalid JSON from madge"
        }

    except Exception as e:
        return {
            "target": target_file,
            "dependencies": [],
            "error": str(e)[:200]
        }
```

---

## 5. Integration with Hermes Orchestrator

### Tool Registration Schema (Corrected — Error field removed from parameters)

```json
{
    "name": "analyze_dependency_graph",
    "description": "Returns all TypeScript files that the target file depends on. Use this BEFORE writing any BEB to build accurate AllowedModifiedFiles lists. On success, returns a 'dependencies' array. On failure, returns an 'error' string.",
    "parameters": {
        "type": "object",
        "properties": {
            "target_file": {
                "type": "string",
                "description": "Relative path to the primary file (e.g. 'packages/core/src/ipc_router.ts')"
            },
            "work_dir": {
                "type": "string",
                "description": "Absolute path to the project root"
            }
        },
        "required": ["target_file", "work_dir"]
    }
}
```

---

## 6. Update to BLK-003 Orchestration (State 1.2)

```markdown
#### State 1.2 — The Scope Reconnaissance

Before constructing the BEB and finalizing the YAML frontmatter, Hermes **MUST** call the `analyze_dependency_graph` tool on the primary target file.

- Hermes **MUST** populate the `AllowedModifiedFiles` array using **only** the exact paths returned in the `dependencies` field of the tool response.
- Hermes is **STRICTLY FORBIDDEN** from guessing, hallucinating, or adding any file paths that were not explicitly returned by the tool.
- If the original task directive explicitly requires additional files, Hermes may append them **after** the tool results, but must document the justification in the BEB.
```

---

## 7. Testing & Final Checklist

**Test Commands:**

```bash
python3 -c "
from recon import analyze_dependency_graph
result = analyze_dependency_graph('packages/core/src/ipc_router.ts', '/path/to/kuronode')
print(result)
"
```

**Final Checklist:**
- [ ] `madge` installed as `devDependency`
- [ ] `recon.py` created with the exact code above
- [ ] Tool registered with the corrected JSON schema (no `error` in parameters)
- [ ] State 1.2 and State 1.3 added to BLK-003 orchestration
- [ ] Tool tested successfully on real files

---

**You are now ready to implement.**
