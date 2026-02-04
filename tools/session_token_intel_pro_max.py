import requests
import re
import base64
import json
from urllib.parse import urlparse, parse_qs

HEADERS = {
    "User-Agent": "SecAI-Research-Agent/1.0",
    "Accept": "*/*"
}

TIMEOUT = 10

SESSION_COOKIE_NAMES = [
    "session", "sessid", "phpsessid",
    "jsessionid", "auth", "token", "sid"
]

JWT_REGEX = r"eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+"


def decode_jwt_header(token):
    try:
        header_b64 = token.split(".")[0] + "==="
        decoded = base64.urlsafe_b64decode(header_b64)
        return json.loads(decoded)
    except Exception:
        return None


def analyze_session_and_tokens(url):
    result = {
        "url": url,
        "cookies_detected": [],
        "cookie_flag_issues": [],
        "session_fixation_signals": [],
        "jwt_tokens_detected": [],
        "jwt_header_analysis": [],
        "token_leakage_signals": [],
        "risk_signals": [],
        "analysis_notes": [],
        "worth_deeper_testing": False
    }

    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    except requests.exceptions.RequestException as e:
        result["analysis_notes"].append(str(e))
        return result

    # --- Cookie Analysis ---
    for cookie in resp.cookies:
        cookie_info = {
            "name": cookie.name,
            "secure": cookie.secure,
            "httponly": cookie.has_nonstandard_attr("HttpOnly"),
            "path": cookie.path,
            "domain": cookie.domain
        }
        result["cookies_detected"].append(cookie_info)

        lname = cookie.name.lower()
        if any(k in lname for k in SESSION_COOKIE_NAMES):
            if not cookie.secure:
                result["cookie_flag_issues"].append(
                    f"{cookie.name} missing Secure flag"
                )
            if not cookie.has_nonstandard_attr("HttpOnly"):
                result["cookie_flag_issues"].append(
                    f"{cookie.name} missing HttpOnly flag"
                )

    # --- Token leakage in URL ---
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    for p in params:
        if "token" in p.lower() or "session" in p.lower():
            result["token_leakage_signals"].append(
                f"Sensitive token-like parameter in URL: {p}"
            )

    # --- Token leakage in HTML ---
    jwt_matches = re.findall(JWT_REGEX, resp.text)
    for token in jwt_matches:
        result["jwt_tokens_detected"].append(token)

        header = decode_jwt_header(token)
        if header:
            result["jwt_header_analysis"].append(header)

            if header.get("alg", "").lower() == "none":
                result["risk_signals"].append(
                    "JWT uses alg=none (critical misconfiguration)"
                )

    # --- Session fixation signal ---
    if resp.history:
        for h in resp.history:
            if h.cookies:
                result["session_fixation_signals"].append(
                    "Session cookie set before authentication (possible fixation)"
                )

    # --- Decision logic ---
    if (
        result["cookie_flag_issues"]
        or result["jwt_tokens_detected"]
        or result["token_leakage_signals"]
        or result["session_fixation_signals"]
    ):
        result["worth_deeper_testing"] = True

    # Deduplicate
    for k in result:
        if isinstance(result[k], list):
            result[k] = list(set(
                json.dumps(i, sort_keys=True) if isinstance(i, dict) else i
                for i in result[k]
            ))
            result[k] = [
                json.loads(i) if i.startswith("{") else i
                for i in result[k]
            ]

    return result


if __name__ == "__main__":
    target = input("Target URL (https://example.com): ").strip()
    report = analyze_session_and_tokens(target)

    print("\n=== SESSION / COOKIE / TOKEN INTELLIGENCE ===\n")
    for k, v in report.items():
        print(f"{k}: {v}")
