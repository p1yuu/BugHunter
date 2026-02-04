def generate_attack_chains(final_report: dict) -> list:
    signals = final_report.get("strategic_summary", {}).get("global_risk_signals", [])
    chains = []

    if any("idor" in s.lower() for s in signals) and any("api" in s.lower() for s in signals):
        chains.append({
            "title": "IDOR → API Data Exfiltration",
            "impact": "Unauthorized access to other users' data",
            "why_it_matters": (
                "Object identifiers exposed in API endpoints may allow "
                "attackers to enumerate or access resources belonging to other users."
            )
        })

    if any("cookie" in s.lower() for s in signals) and any("session" in s.lower() for s in signals):
        chains.append({
            "title": "Weak Cookie Flags → Session Hijacking",
            "impact": "Account takeover under certain conditions",
            "why_it_matters": (
                "Missing Secure / HttpOnly flags increase the risk of session theft "
                "via client-side vectors."
            )
        })

    return chains
