def should_report(module_name: str, module: dict) -> str:
    signals = module.get("risk_signals", [])

    high_value_keywords = ["idor", "access control", "authorization", "data exposure"]

    for s in signals:
        for k in high_value_keywords:
            if k in s.lower():
                return "REPORT"

    if module.get("worth_deeper_testing"):
        return "MANUAL REVIEW"

    return "IGNORE"
