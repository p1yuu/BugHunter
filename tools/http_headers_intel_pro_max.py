import sys
import requests

HEADERS = {
    "User-Agent": "SecAI-Research-Agent/1.0",
    "Accept": "*/*",
    "Origin": "https://evil.example"
}

TIMEOUT = 10

SECURITY_HEADERS = {
    "Content-Security-Policy": "CSP not defined",
    "X-Frame-Options": "Clickjacking protection missing",
    "X-Content-Type-Options": "MIME sniffing protection missing",
    "Strict-Transport-Security": "HSTS not enforced",
    "Referrer-Policy": "Referrer policy missing",
    "Permissions-Policy": "Permissions policy missing"
}


def analyze_cors_and_headers(url):
    result = {
        "url": url,
        "cors_policy": {},
        "cors_risk_signals": [],
        "security_headers_present": [],
        "security_headers_missing": [],
        "browser_trust_issues": [],
        "analysis_notes": [],
        "worth_deeper_testing": False
    }

    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    except requests.exceptions.RequestException as e:
        result["analysis_notes"].append(str(e))
        return result

    headers = resp.headers

    # --- CORS Analysis ---
    acao = headers.get("Access-Control-Allow-Origin")
    acac = headers.get("Access-Control-Allow-Credentials")

    if acao:
        result["cors_policy"]["Access-Control-Allow-Origin"] = acao

        if acao == "*" and acac == "true":
            result["cors_risk_signals"].append(
                "CORS misconfiguration: wildcard origin with credentials enabled"
            )

        if acao == HEADERS["Origin"]:
            result["cors_risk_signals"].append(
                "Origin reflected in Access-Control-Allow-Origin"
            )
    else:
        result["analysis_notes"].append("No CORS headers detected")

    if acac:
        result["cors_policy"]["Access-Control-Allow-Credentials"] = acac

    # --- Security Headers ---
    for header, msg in SECURITY_HEADERS.items():
        if header in headers:
            result["security_headers_present"].append(
                f"{header}: {headers.get(header)}"
            )
        else:
            result["security_headers_missing"].append(header)
            result["browser_trust_issues"].append(msg)

    # --- CSP Weakness Indicators ---
    csp = headers.get("Content-Security-Policy", "")
    if csp:
        if "unsafe-inline" in csp or "unsafe-eval" in csp:
            result["browser_trust_issues"].append(
                "Weak CSP directives detected (unsafe-inline / unsafe-eval)"
            )

    # --- Decision Logic ---
    if (
        result["cors_risk_signals"]
        or result["security_headers_missing"]
        or result["browser_trust_issues"]
    ):
        result["worth_deeper_testing"] = True

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print({
            "tool": "cors_and_headers_intel",
            "module": "cors_and_headers_intel_pro_max",
            "status": "error",
            "error": "No target URL provided"
        })
        sys.exit(1)

    target = sys.argv[1].strip()
    data = analyze_cors_and_headers(target)

    print({
        "tool": "cors_and_headers_intel",
        "module": "cors_and_headers_intel_pro_max",
        "target": target,
        "status": "completed",
        "data": data
    })
