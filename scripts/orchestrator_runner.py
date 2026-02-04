import json
import subprocess
import sys
from pathlib import Path

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent
TOOLS_DIR = BASE_DIR / "tools"

# --- Tool registry ---
TOOL_REGISTRY = {
    "http_headers": "http_headers_intel_pro_max.py",
    "tls_configuration": "tls_configuration_intel_pro_max.py",
    "asset_discovery": "asset_discovery_intel_pro_max.py",
}

def run_tool(tool_name: str, target: str):
    if tool_name not in TOOL_REGISTRY:
        return {
            "tool": tool_name,
            "status": "skipped",
            "reason": "No matching tool registered"
        }

    tool_path = TOOLS_DIR / TOOL_REGISTRY[tool_name]

    if not tool_path.exists():
        return {
            "tool": tool_name,
            "status": "error",
            "reason": "Tool file not found"
        }

    try:
        result = subprocess.run(
            [sys.executable, str(tool_path), target],
            capture_output=True,
            text=True,
            timeout=60
        )

        return {
            "tool": tool_name,
            "status": "completed",
            "output": result.stdout.strip(),
            "errors": result.stderr.strip()
        }

    except Exception as e:
        return {
            "tool": tool_name,
            "status": "failed",
            "reason": str(e)
        }

def main():
    print("Paste orchestrator JSON output and press Enter twice:\n")

    # Read multiline JSON from stdin
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)

    orchestrator_json = json.loads("\n".join(lines))

    target = orchestrator_json.get("target")
    scopes = orchestrator_json.get("analysis_scope", [])

    print(f"\n[+] Target: {target}")
    print(f"[+] Analysis scope: {scopes}\n")

    results = []

    for scope in scopes:
        print(f"[*] Running module: {scope}")
        tool_result = run_tool(scope, target)
        results.append(tool_result)

    final_output = {
        "target": target,
        "analysis_mode": "passive",
        "modules_executed": results
    }

    print("\n=== FINAL AGGREGATED OUTPUT ===\n")
    print(json.dumps(final_output, indent=2))

if __name__ == "__main__":
    main()
