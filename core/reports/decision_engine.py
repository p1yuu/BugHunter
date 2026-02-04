def should_report(final_report: dict) -> dict:
    signals = final_report.get("strategic_summary", {}).get("global_risk_signals", [])

    high_value_keywords = [
        "idor",
        "broken access",
        "unauthenticated",
        "authorization",
        "token",
        "session",
        "api",
        "data exposure"
    ]

    low_value_keywords = [
        "missing header",
        "verbose error",
        "fingerprinting",
        "server header"
    ]

    score = 0
    reasons = []

    for s in signals:
        sl = s.lower()
        if any(k in sl for k in high_value_keywords):
            score += 2
            reasons.append(f"High-impact signal: {s}")
        elif any(k in sl for k in low_value_keywords):
            score -= 1

    return {
        "should_report": score >= 2,
        "confidence": "high" if score >= 4 else "medium" if score >= 2 else "low",
        "reasons": list(set(reasons))
    }
