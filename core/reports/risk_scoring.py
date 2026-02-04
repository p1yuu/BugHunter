def calculate_risk_score(signals: list) -> int:
    score = 0
    for s in signals:
        s = s.lower()
        if "idor" in s or "access control" in s:
            score += 40
        elif "api" in s:
            score += 25
        elif "cookie" in s or "session" in s:
            score += 15
        elif "csp" in s or "client" in s:
            score += 10
    return min(score, 100)
