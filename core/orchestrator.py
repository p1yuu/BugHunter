import sys
import os
from typing import Dict, Any

# allow importing from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

"""
SecAI Orchestrator
-----------------
Runs all passive intelligence modules safely and aggregates results.
"""

# =========================
# Tool Imports (CORRECT)
# =========================

from tools.target_surface_intel_pro_max import analyze_target
from tools.http_behavior_intel_pro_max import analyze_http_behavior
from tools.http_headers_intel_pro_max import analyze_cors_and_headers

from tools.input_surface_intel_pro_max import analyze_input_surface
from tools.input_validation_intel_pro_max import analyze_input_handling
from tools.api_surface_intel_pro_max import analyze_api_surface

from tools.authentication_intel_pro_max import analyze_auth_surface
from tools.authorization_intel_pro_max import analyze_authorization

from tools.client_side_js_intel_pro_max import analyze_client_side_js

from tools.file_handling_intel_pro_max import analyze_file_handling
from tools.error_handling_intel_pro_max import analyze_errors

from executive_summary import generate_executive_summary


# =========================
# Safe Runner
# =========================

def safe_run(name: str, fn, target: str) -> Dict[str, Any]:
    try:
        return fn(target)
    except Exception as e:
        return {
            "module": name,
            "error": str(e),
            "worth_deeper_testing": False
        }


# =========================
# Orchestrator Core
# =========================

def run_full_intelligence(target: str) -> Dict[str, Any]:

    report = {
        "target": target,
        "mode": "passive-intelligence",
        "modules": {},
        "strategic_summary": {
            "high_value_surfaces": [],
            "low_value_surfaces": [],
            "global_risk_signals": []
        }
    }

    modules = {
        "target_surface": analyze_target,
        "http_behavior": analyze_http_behavior,
        "cors_and_headers": analyze_cors_and_headers,

        "input_surface": analyze_input_surface,
        "input_handling": analyze_input_handling,
        "api_surface": analyze_api_surface,

        "authentication": analyze_auth_surface,
        "authorization": analyze_authorization,

        "client_side_js": analyze_client_side_js,

        "file_handling": analyze_file_handling,
        "error_handling": analyze_errors
    }

    for name, fn in modules.items():
        output = safe_run(name, fn, target)
        report["modules"][name] = output

        if output.get("worth_deeper_testing"):
            report["strategic_summary"]["high_value_surfaces"].append(name)
        else:
            report["strategic_summary"]["low_value_surfaces"].append(name)

        for key in ["risk_signals", "risk_indicators", "cors_risk_signals"]:
            if isinstance(output.get(key), list):
                report["strategic_summary"]["global_risk_signals"].extend(output[key])

    # dedupe
    for k in report["strategic_summary"]:
        report["strategic_summary"][k] = list(set(report["strategic_summary"][k]))

    return report


# =========================
# CLI
# =========================

from reports.narrative_report import generate_narrative_report
from executive_summary import generate_executive_summary
from reports.auto_attack_guide import generate_auto_attack_guide
from reports.exporter import export_markdown
from reports.decision_engine import should_report
from reports.cvss_engine import calculate_cvss
from reports.duplicate_engine import duplicate_risk
from reports.hackerone_writer import generate_hackerone_report
from reports.attack_chain_engine import generate_attack_chains
from reports.poc_generator import generate_poc_examples
from reports.anti_duplicate_writer import write_anti_duplicate

if __name__ == "__main__":
    target = input("Target URL (https://example.com): ").strip()

    # =========================
    # FULL INTELLIGENCE
    # =========================
    final_report = run_full_intelligence(target)

    # =========================
    # STRATEGIC SUMMARY
    # =========================
    print("\n=== STRATEGIC SUMMARY ===\n")
    for k, v in final_report["strategic_summary"].items():
        print(f"{k}: {v}")

    # =========================
    # EXECUTIVE SUMMARY
    # =========================
    summary = generate_executive_summary(final_report)
    print("\n=== EXECUTIVE SUMMARY ===\n")
    for k, v in summary.items():
        print(f"{k}: {v}")

    # =========================
    # BUG BOUNTY NARRATIVE REPORT
    # =========================
    narrative = generate_narrative_report(final_report)
    print("\n=== BUG BOUNTY NARRATIVE REPORT ===\n")
    print(narrative)

    # =========================
    # AUTO ATTACK GUIDE
    # =========================
    attack_guide = generate_auto_attack_guide(final_report)
    print("\n=== AUTO ATTACK GUIDE ===\n")
    print(attack_guide)

    # Export attack guide
    path = export_markdown(target, attack_guide)
    print(f"\n📄 Saved to: {path}")

    # =========================
    # HACKERONE READY REPORT
    # =========================
    decision = should_report(final_report)
    cvss = calculate_cvss(final_report)
    duplicate = duplicate_risk(final_report)
    attack_chains = generate_attack_chains(final_report)
    anti_dup_text = generate_anti_duplicate_text(final_report)

    h1_report = generate_hackerone_report(
        target=target,
        narrative=narrative,
        cvss=cvss,
        decision=decision,
        duplicate=duplicate,
        chains=attack_chains,
        poc=generate_poc_examples(),
        anti_dup=anti_dup_text
    )

    print("\n=== HACKERONE READY REPORT ===\n")
    print(h1_report)
