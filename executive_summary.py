def generate_executive_summary(orchestrator_output: dict):
    summary = {
        "overall_risk_level": "Low",
        "top_testing_priorities": [],
        "critical_signals": [],
        "low_value_areas": [],
        "analyst_notes": []
    }

    score = 0

    WEIGHTS = {
        "api": 3,
        "auth": 4,
        "authorization": 5,
        "client": 2,
        "headers": 2,
        "files": 3,
        "inputs": 3,
        "errors": 2
    }

    for module, data in orchestrator_output.items():
        if not isinstance(data, dict):
            continue

        if data.get("worth_deeper_testing"):
            weight = 2
            for key, w in WEIGHTS.items():
                if key in module.lower():
                    weight = w
                    break

            score += weight

            summary["top_testing_priorities"].append({
                "module": module,
                "reason": "worth_deeper_testing=True",
                "weight": weight
            })

            if "risk_signals" in data and data["risk_signals"]:
                summary["critical_signals"].append({
                    "module": module,
                    "signals": data["risk_signals"][:3]
                })

        else:
            summary["low_value_areas"].append(module)

    # Risk level decision
    if score >= 12:
        summary["overall_risk_level"] = "High"
    elif score >= 6:
        summary["overall_risk_level"] = "Medium"

    summary["analyst_notes"].append(
        "Summary generated via passive signal correlation only."
    )
    summary["analyst_notes"].append(
        "Priorities ranked by likelihood × impact heuristic."
    )

    # Sort priorities by weight
    summary["top_testing_priorities"] = sorted(
        summary["top_testing_priorities"],
        key=lambda x: x["weight"],
        reverse=True
    )[:5]

    return summary
