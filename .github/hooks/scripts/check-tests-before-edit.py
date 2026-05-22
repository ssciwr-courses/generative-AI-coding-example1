#!/usr/bin/env python3
"""Pre-edit hook: block edits to src/ unless all tests pass."""

import json
import subprocess
import sys

hook_input = json.load(sys.stdin)

tool_name = hook_input.get("toolName", "")
tool_input = hook_input.get("toolInput", {})

EDIT_TOOLS = {"replace_string_in_file", "create_file", "multi_replace_string_in_file"}
GUARDED_PREFIX = "src/"

# Only run for edit tools targeting src/
if tool_name not in EDIT_TOOLS:
    sys.exit(0)

file_path = tool_input.get("filePath", "")
if not file_path:
    # multi_replace_string_in_file has replacements array
    replacements = tool_input.get("replacements", [])
    paths = [r.get("filePath", "") for r in replacements]
    in_src = any(GUARDED_PREFIX in p for p in paths)
else:
    in_src = GUARDED_PREFIX in file_path

if not in_src:
    sys.exit(0)

# Run the test suite
result = subprocess.run(
    ["python", "-m", "pytest", "src/test/", "-q", "--tb=no"],
    capture_output=True,
    text=True,
)

if result.returncode != 0:
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "Tests are currently failing. Fix the tests before editing src/.\n"
                + result.stdout.strip()
            ),
        }
    }
    print(json.dumps(output))
    sys.exit(0)
