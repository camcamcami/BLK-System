import copy
import hashlib
import json
import unittest

from kuronode_power_of_ten_static_profile import (
    BLOCKED_STATUS,
    EXACT_EXCLUDED_AUTHORITIES,
    PASS_STATUS,
    evaluate_kuronode_power_of_ten_static_profile,
)

HASH_A = "sha256:" + "a" * 64


def expected_bundle_hash(files):
    stable = json.dumps(copy.deepcopy(files), sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(stable).hexdigest()


def valid_request(files=None):
    return {
        "profile_name": "kuronode-power-of-ten-static",
        "request_status": "KURONODE_POWER_OF_TEN_STATIC_PROFILE_FIXTURE_ONLY",
        "request_id": "KURONODE-P10-STATIC-056-001",
        "operator_identity": "discord:684235178083745819",
        "trace_artifacts": [{"kind": "BLK", "id": "BLK-058", "version_hash": HASH_A}],
        "source_bundle_id": "KURONODE-TYPESCRIPT-BUNDLE-056-001",
        "source_bundle_hash": expected_bundle_hash(valid_files() if files is None else files),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
        "operator_note": "fixture-only static profile descriptors",
    }


def valid_files():
    return [
        {
            "path": "src/renderer/GraphView.tsx",
            "language": "typescript",
            "content": """
export function validateNodeCount(nodes: readonly Node[]): Result {
  const MAX_NODES = 500;
  if (nodes.length > MAX_NODES) {
    return { ok: false, reason: "too-many-nodes" };
  }
  return { ok: true };
}

export function disposeGraph(worker: Worker): void {
  worker.terminate();
}
""".strip(),
        }
    ]


class KuronodePowerOfTenStaticProfileTest(unittest.TestCase):
    def _evaluate(self, files=None, request=None):
        selected_files = copy.deepcopy(valid_files() if files is None else files)
        selected_request = copy.deepcopy(valid_request(selected_files) if request is None else request)
        return evaluate_kuronode_power_of_ten_static_profile(
            files=selected_files,
            request=selected_request,
        )

    def test_passes_safe_fixture_descriptors_without_runtime_side_effects(self):
        result = self._evaluate()

        self.assertEqual(result["profile_status"], PASS_STATUS)
        self.assertEqual(result["profile_name"], "kuronode-power-of-ten-static")
        self.assertEqual(result["checked_file_count"], 1)
        self.assertEqual(result["findings"], [])
        self.assertFalse(result["live_kuronode_scan_performed"])
        self.assertFalse(result["source_mutation_performed"])
        self.assertFalse(result["blk_test_mcp_started"])
        self.assertFalse(result["codex_started"])
        self.assertFalse(result["package_manager_invoked"])
        self.assertFalse(result["protected_body_read"])
        self.assertFalse(result["beo_published"])
        self.assertFalse(result["rtm_generated"])
        self.assertEqual(set(result["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        self.assertIn("profile_hash", result)

    def test_blocks_core_blk058_static_violations(self):
        cases = [
            (
                "recursion",
                "export function walk(node: Node): void { walk(node); }",
                "RECURSION_FORBIDDEN",
            ),
            (
                "while true",
                "export function poll(): void { while (true) { break; } }",
                "UNBOUNDED_WHILE_TRUE_FORBIDDEN",
            ),
            (
                "eval",
                "export function run(input: string): void { eval(input); }",
                "DYNAMIC_CODE_EXECUTION_FORBIDDEN",
            ),
            (
                "new Function",
                "const make = new Function('x', 'return x');",
                "DYNAMIC_CODE_EXECUTION_FORBIDDEN",
            ),
            (
                "var",
                "export function f(): void { var x = 1; void x; }",
                "VAR_DECLARATION_FORBIDDEN",
            ),
            (
                "explicit any",
                "export function parse(input: any): Result { return { ok: true, input }; }",
                "EXPLICIT_ANY_FORBIDDEN",
            ),
            (
                "floating promise",
                "export function save(model: Model): void { void saveModel(model); }",
                "FLOATING_PROMISE_FORBIDDEN",
            ),
            (
                "non null assertion",
                "export function pos(graph: Graph): number { return graph.nodes['a']!.x; }",
                "NON_NULL_ASSERTION_FORBIDDEN",
            ),
        ]
        for label, content, rule in cases:
            files = [{"path": "src/main/example.ts", "language": "typescript", "content": content}]
            with self.subTest(label=label):
                result = self._evaluate(files=files)
                self.assertEqual(result["profile_status"], BLOCKED_STATUS)
                self.assertIn(rule, {finding["rule"] for finding in result["findings"]})

    def test_blocks_functions_over_sixty_physical_lines(self):
        lines = ["export function longFunction(): number {"]
        lines.extend(f"  const value{i} = {i};" for i in range(61))
        lines.append("  return value0;")
        lines.append("}")

        result = self._evaluate(files=[{"path": "src/renderer/Long.ts", "language": "typescript", "content": "\n".join(lines)}])

        self.assertEqual(result["profile_status"], BLOCKED_STATUS)
        self.assertIn("FUNCTION_TOO_LONG", {finding["rule"] for finding in result["findings"]})

    def test_blocks_lifecycle_constructs_without_cleanup_vocabulary(self):
        cases = [
            "export function start(): void { const worker = new Worker('worker.js'); worker.postMessage('x'); }",
            "export function start(): void { setInterval(() => tick(), 1000); }",
            "export function start(): void { const observer = new MutationObserver(() => {}); observer.observe(node, {}); }",
        ]
        for content in cases:
            files = [{"path": "src/renderer/lifecycle.ts", "language": "typescript", "content": content}]
            with self.subTest(content=content):
                result = self._evaluate(files=files)
                self.assertEqual(result["profile_status"], BLOCKED_STATUS)
                self.assertIn("LIFECYCLE_CLEANUP_REQUIRED", {finding["rule"] for finding in result["findings"]})

    def test_rejects_bad_paths_non_typescript_descriptors_and_protected_refs(self):
        cases = [
            ([{"path": "README.md", "language": "markdown", "content": "text"}], "file path must target .ts or .tsx"),
            ([{"path": "../src/main.ts", "language": "typescript", "content": "export const x = 1;"}], "file path must be a normalized relative path"),
            ([{"path": "docs%252Factive%252FREQ-001.ts", "language": "typescript", "content": "export const x = 1;"}], "protected BLK-req body reference"),
            ([{"path": "src/main.ts", "language": "python", "content": "export const x = 1;"}], "language must be typescript or tsx"),
        ]
        for files, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(ValueError, message):
                    self._evaluate(files=files)

    def test_rejects_authority_laundering_metadata_and_exact_exclusion_mismatch(self):
        request = valid_request()
        request["operator_note"] = "Production BLK-test MCP is authorized after this PASS"
        with self.assertRaisesRegex(ValueError, "authority-laundering text"):
            self._evaluate(request=request)

        request = valid_request()
        request["operator_note"] = "After PASS run tsc, eslint, npm install, and scan the live Kuronode repository."
        with self.assertRaisesRegex(ValueError, "authority-laundering text"):
            self._evaluate(request=request)

        request = valid_request()
        request["excluded_authorities"] = sorted(EXACT_EXCLUDED_AUTHORITIES - {"LIVE_CODEX_EXECUTION"})
        with self.assertRaisesRegex(ValueError, "excluded_authorities must match exact denied authority set"):
            self._evaluate(request=request)

        request = valid_request()
        request["extra_authority"] = "APPROVED_FOR_LIVE_EXECUTION"
        with self.assertRaisesRegex(ValueError, "unexpected field"):
            self._evaluate(request=request)

    def test_blocks_source_text_that_attempts_to_claim_runtime_or_publication_authority(self):
        cases = [
            "// BEO publication authorized; RTMGeneration complete\nexport const ok = true;",
            "// Git mutation authorized after PASS\nexport const ok = true;",
            "import secret from '../../docs/active/REQ-001.md';\nexport const ok = true;",
        ]
        for content in cases:
            files = [
                {
                    "path": "src/renderer/comment.ts",
                    "language": "typescript",
                    "content": content,
                }
            ]
            with self.subTest(content=content):
                result = self._evaluate(files=files)
                self.assertEqual(result["profile_status"], BLOCKED_STATUS)
                self.assertIn("AUTHORITY_LAUNDERING_TEXT_FORBIDDEN", {finding["rule"] for finding in result["findings"]})

    def test_rejects_source_bundle_hash_mismatch(self):
        request = valid_request()
        request["source_bundle_hash"] = "sha256:" + "c" * 64
        with self.assertRaisesRegex(ValueError, "source_bundle_hash does not match submitted file descriptors"):
            self._evaluate(request=request)

    def test_blocks_hostile_static_analysis_bypass_shapes(self):
        files = [
            {
                "path": "src/renderer/bypass.ts",
                "language": "typescript",
                "content": "export const walk = (node: Node): void => { walk(node); };",
            },
            {
                "path": "src/renderer/cast.ts",
                "language": "typescript",
                "content": "export const value = payload as any;",
            },
            {
                "path": "src/renderer/comment_cleanup.ts",
                "language": "typescript",
                "content": "// cleanup someday\nexport function start(): void { const worker = new Worker('worker.js'); worker.postMessage('x'); }",
            },
        ]
        result = self._evaluate(files=files)
        rules = {finding["rule"] for finding in result["findings"]}
        self.assertEqual(result["profile_status"], BLOCKED_STATUS)
        self.assertIn("RECURSION_FORBIDDEN", rules)
        self.assertIn("EXPLICIT_ANY_FORBIDDEN", rules)
        self.assertIn("LIFECYCLE_CLEANUP_REQUIRED", rules)

        lines = ["export class LongClass {"]
        lines.append("  longMethod(): number {")
        lines.extend(f"    const value{i} = {i};" for i in range(61))
        lines.append("    return value0;")
        lines.append("  }")
        lines.append("}")
        class_result = self._evaluate(
            files=[{"path": "src/renderer/LongClass.ts", "language": "typescript", "content": "\n".join(lines)}]
        )
        self.assertIn("FUNCTION_TOO_LONG", {finding["rule"] for finding in class_result["findings"]})


if __name__ == "__main__":
    unittest.main()
