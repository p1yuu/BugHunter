import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "SecAI-Research-Agent/1.0"
}

TIMEOUT = 10

AUTH_KEYWORDS = [
    "login", "signin", "auth", "session", "account", "user"
]

TOKEN_KEYWORDS = [
    "token", "jwt", "bearer", "authorization"
]


def analyze_auth_and_session(url):
    result = {
        "url": url,
        "auth_endpoints_detected": [],
        "login_forms_detected": [],
        "cookies_observed": [],
        "cookie_flag_issues": [],
        "token_handling_signals": [],
        "client_side_auth_logic": [],
        "analysis_notes": [],
        "worth_deeper_testing": False
    }

    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        soup = BeautifulSoup(resp.text, "html.parser")
    except requests.exceptions.RequestException as e:
        result["analysis_notes"].append(str(e))
        return result

    # --- Forms (Login detection) ---
    for form in soup.find_all("form"):
        inputs = form.find_all("input")
        names = " ".join([(i.get("name") or "").lower() for i in inputs])

        if any(k in names for k in ["password", "passwd"]):
            result["login_forms_detected"].append({
                "action": urljoin(url, form.get("action") or ""),
                "method": (form.get("method") or "get").lower()
            })

    # --- Auth-related links ---
    for link in soup.find_all("a", href=True):
        href = link["href"].lower()
        if any(k in href for k in AUTH_KEYWORDS):
            result["auth_endpoints_detected"].append(
                urljoin(url, link["href"])
            )

    # --- Cookies ---
    for cookie in resp.cookies:
        cookie_info = {
            "name": cookie.name,
            "secure": cookie.secure,
            "httponly": cookie.has_nonstandard_attr("HttpOnly"),
            "samesite": cookie._rest.get("SameSite")
        }
        result["cookies_observed"].append(cookie_info)

        if not cookie.secure:
            result["cookie_flag_issues"].append(
                f"Cookie '{cookie.name}' missing Secure flag"
            )
        if not cookie.has_nonstandard_attr("HttpOnly"):
            result["cookie_flag_issues"].append(
                f"Cookie '{cookie.name}' missing HttpOnly flag"
            )
        if not cookie._rest.get("SameSite"):
            result["cookie_flag_issues"].append(
                f"Cookie '{cookie.name}' missing SameSite attribute"
            )

    # --- Scripts (Token / client-side auth clues) ---
    for script in soup.find_all("script"):
        code = (script.string or "").lower()
        if not code.strip():
            continue

        if any(k in code for k in TOKEN_KEYWORDS):
            result["token_handling_signals"].append(
                "Client-side token handling logic detected"
            )

        if any(k in code for k in ["isloggedin", "isadmin", "role"]):
            result["client_side_auth_logic"].append(
                "Client-side authentication / role logic detected"
            )

    # Deduplicate
    result["auth_endpoints_detected"] = list(set(result["auth_endpoints_detected"]))
    result["cookie_flag_issues"] = list(set(result["cookie_flag_issues"]))
    result["token_handling_signals"] = list(set(result["token_handling_signals"]))
    result["client_side_auth_logic"] = list(set(result["client_side_auth_logic"]))

    # Decision logic
    if (
        result["login_forms_detected"]
        or result["cookie_flag_issues"]
        or result["token_handling_signals"]
        or result["client_side_auth_logic"]
    ):
        result["worth_deeper_testing"] = True

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print({
            "tool": "authentication",
            "status": "error",
            "error": "No target URL provided"
        })
        sys.exit(1)

    target = sys.argv[1].strip()
    data = analyze_auth_and_session(target)

    print({
        "tool": "authentication",
        "module": "authentication_intel_pro_max",
        "target": target,
        "status": "completed",
        "data": data
    })
