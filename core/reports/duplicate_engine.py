def duplicate_risk(final_report: dict) -> dict:
    signals = final_report.get("strategic_summary", {}).get("global_risk_signals", [])

    duplicate_prone = [
        "missing header",
        "csp",
        "server header",
        "cookie flag"
    ]

    risk = "low"

    for s in signals:
        if any(k in s.lower() for k in duplicate_prone):
            risk = "high"
            break

    return {
        "duplicate_risk": risk,
        "advice": (
            "Likely duplicate unless chained with impact"
            if risk == "high"
            else "Low likelihood of duplication"
        )
    }
