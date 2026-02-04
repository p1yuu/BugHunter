def calculate_cvss(final_report: dict) -> dict:
    signals = final_report.get("strategic_summary", {}).get("global_risk_signals", [])

    vector = []
    score = 0.0

    for s in signals:
        sl = s.lower()
        if "idor" in sl or "access control" in sl:
            score += 3.5
            vector.append("Broken Access Control")
        if "unauthenticated" in sl:
            score += 2.5
            vector.append("Unauthenticated Access")
        if "token" in sl or "session" in sl:
            score += 2.0
            vector.append("Session Handling Weakness")
        if "xss" in sl:
            score += 2.0
            vector.append("Client-Side Injection")

    score = min(score, 9.5)

    if score >= 8:
        severity = "Critical"
    elif score >= 6:
        severity = "High"
    elif score >= 4:
        severity = "Medium"
    else:
        severity = "Low"

    return {
        "cvss_score": round(score, 1),
        "severity": severity,
        "justification": list(set(vector)) or ["Low exploitability via passive signals"]
    }
