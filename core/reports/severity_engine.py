def assess_severity(module_name: str, module: dict) -> dict:
    signals = " ".join(module.get("risk_signals", [])).lower()

    if "idor" in signals or "broken access control" in signals:
        return {
            "level": "High",
            "justification": "Unauthorized access to other users’ data is possible without authentication bypass."
        }

    if "api" in signals:
        return {
            "level": "Medium",
            "justification": "Public or weakly protected API endpoints may expose sensitive functionality."
        }

    return {
        "level": "Low",
        "justification": "No direct impact observed; exploitation would likely be limited."
    }
